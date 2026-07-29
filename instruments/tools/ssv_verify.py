"""Read-only pre-submission audit for one SSV paper.

The build gate answers whether registered invariants still hold.  This auditor
also exposes what remains outside those invariants so a semantic reviewer can
inspect it without mistaking an unreviewed item for a pass.

It never edits manuscripts, receipts, generated TeX, or evidence notes.  The
only optional writes are new JSON/Markdown reports explicitly named by the
caller.

Usage:
    python instruments/tools/ssv_verify.py SSV-I
    python instruments/tools/ssv_verify.py SSV-I --no-recompute
    python instruments/tools/ssv_verify.py SSV-I \
        --json-out /tmp/ssv-verify-SSV-I.json \
        --md-out /tmp/ssv-verify-SSV-I.md
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS = REPO_ROOT / "papers"
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import bibliography  # noqa: E402
import build_paper  # noqa: E402
import citation_evidence  # noqa: E402
import claims  # noqa: E402
import gen_provenance  # noqa: E402
import gen_values  # noqa: E402


NON_OK_CITATION_VERDICTS = {
    "MISATTRIBUTED", "MISREAD", "MISDERIVED", "UNSUPPORTED",
}
PENDING_CITATION_VERDICTS = {"PENDING-PRIMARY"}

# Deliberately a candidate finder, not a correctness checker.  Integer tokens
# are too noisy in LaTeX (years, labels, section numbers), so the pilot queues
# decimals, scientific notation, and percentages only.
NUMERIC_CANDIDATE_RE = re.compile(
    r"(?<![\d.])(?:"
    r"(?:\d+\.\d+|\d+)\s*\\?%"
    r"|(?:\d+\.\d+|\d+)\s*(?:\\times|×)\s*10\s*\^\s*\{?-?\d+\}?"
    r"|\d+\.\d+"
    r")"
)


@dataclass(frozen=True)
class Finding:
    check_id: str
    stage: str
    status: str
    severity: str
    message: str
    refs: tuple[str, ...] = ()


@dataclass
class Audit:
    paper: str
    generated_utc: str
    recomputed_instruments: bool
    findings: list[Finding] = field(default_factory=list)
    registered_claims: list[dict[str, Any]] = field(default_factory=list)
    citation_review_queue: list[dict[str, Any]] = field(default_factory=list)
    numeric_review_queue: list[dict[str, Any]] = field(default_factory=list)
    coverage: dict[str, Any] = field(default_factory=dict)

    @property
    def deterministic_failures(self) -> list[Finding]:
        return [f for f in self.findings if f.status == "FAIL"]

    @property
    def verdict(self) -> str:
        if self.deterministic_failures:
            return "DETERMINISTIC_FAIL"
        return "DETERMINISTIC_PASS_SEMANTIC_REVIEW_PENDING"

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "ssv-verify/v1",
            "paper": self.paper,
            "generated_utc": self.generated_utc,
            "recomputed_instruments": self.recomputed_instruments,
            "verdict": self.verdict,
            "summary": {
                "deterministic_checks": len(self.findings),
                "deterministic_failures": len(self.deterministic_failures),
                "registered_claims": len(self.registered_claims),
                "citation_claims_queued": len(self.citation_review_queue),
                "numeric_candidates_queued": len(self.numeric_review_queue),
            },
            "findings": [asdict(f) for f in self.findings],
            "coverage": self.coverage,
            "semantic_review_queue": {
                "registered_claims": self.registered_claims,
                "citations": self.citation_review_queue,
                "numeric_candidates": self.numeric_review_queue,
            },
        }


def _finding(
    audit: Audit,
    check_id: str,
    stage: str,
    ok: bool,
    pass_message: str,
    fail_message: str,
    refs: tuple[str, ...] = (),
) -> None:
    audit.findings.append(Finding(
        check_id=check_id,
        stage=stage,
        status="PASS" if ok else "FAIL",
        severity="INFO" if ok else "CRITICAL",
        message=pass_message if ok else fail_message,
        refs=refs,
    ))


def _without_comments(line: str) -> str:
    return re.sub(r"(?<!\\)%.*$", "", line)


def extract_numeric_candidates(
    tex: str,
    generated_macros: set[str],
    source: str = "main.tex",
) -> list[dict[str, Any]]:
    """Return prose-number candidates for human review.

    Presence in this list is not a defect.  It means the token is not a
    generated ``\\ssv...`` macro on the same line and deserves classification.
    """
    candidates: list[dict[str, Any]] = []
    lines = tex.splitlines()
    document_starts = [
        index for index, line in enumerate(lines)
        if r"\begin{document}" in _without_comments(line)
    ]
    first_content_line = document_starts[0] + 1 if document_starts else 0
    for lineno, raw in enumerate(lines, start=1):
        if lineno <= first_content_line:
            continue
        line = _without_comments(raw)
        if not line.strip():
            continue
        used_macros = sorted(
            macro for macro in generated_macros if f"\\{macro}" in line
        )
        for match in NUMERIC_CANDIDATE_RE.finditer(line):
            candidates.append({
                "location": f"{source}:{lineno}",
                "token": match.group(0),
                "generated_macros_on_line": used_macros,
                "classification": (
                    "MIXED_WITH_GENERATED_VALUE" if used_macros
                    else "MANUAL_NUMERIC_CANDIDATE"
                ),
                "snippet": line.strip(),
            })
    return candidates


def citation_locations(tex: str, key: str, source: str) -> list[str]:
    """Find line-level uses of a BibTeX key inside citation commands."""
    locations = []
    cite_re = re.compile(r"\\cite\w*\{([^{}]+)\}")
    for lineno, raw in enumerate(tex.splitlines(), start=1):
        line = _without_comments(raw)
        cited = {
            item.strip()
            for match in cite_re.finditer(line)
            for item in match.group(1).split(",")
        }
        if key in cited:
            locations.append(f"{source}:{lineno}")
    return locations


def _audit_bibliography_and_evidence(audit: Audit, paper: str) -> None:
    bib_issues = bibliography.issues_for(paper)
    _finding(
        audit, "S1-BIBLIOGRAPHY", "artifact-integrity", not bib_issues,
        "Shared bibliography and paper citation keys are structurally valid.",
        "Bibliography defects: " + "; ".join(bib_issues),
        (f"papers/{paper}/main.tex", "papers/cited/references.bib"),
    )

    evidence_issues = citation_evidence.evidence_issues()
    _finding(
        audit, "S1-CITATION-EVIDENCE", "artifact-integrity",
        not evidence_issues,
        "Citation evidence registry and note structure are complete.",
        "Citation-evidence defects: " + "; ".join(evidence_issues),
        ("papers/cited/verification.json", "papers/cited/notes/"),
    )


def _audit_provenance(audit: Audit, paper: str, tex: str) -> None:
    issues, paths, reports, broken = gen_provenance.extract_refs(tex, paper)
    _finding(
        audit, "S1-PROVENANCE-REFS", "artifact-integrity", not broken,
        f"All provenance references resolve ({len(paths)} scripts, "
        f"{len(reports)} reports, {len(issues)} issues).",
        "Unresolved provenance references: " + ", ".join(sorted(broken)),
        (f"papers/{paper}/main.tex",),
    )

    expected = gen_provenance.render(
        paper, issues, paths, reports, gen_provenance.repo_slug())
    path = PAPERS / paper / "provenance.tex"
    actual = path.read_text(encoding="utf-8") if path.is_file() else None
    _finding(
        audit, "S1-PROVENANCE-RENDER", "artifact-integrity",
        actual == expected,
        "provenance.tex matches the current manuscript references.",
        "provenance.tex is missing or stale; regeneration would change it.",
        (f"papers/{paper}/provenance.tex",),
    )


def _audit_values(
    audit: Audit,
    paper: str,
    recompute: bool,
) -> tuple[set[str], dict[str, Any]]:
    if paper not in gen_values.REGISTRY:
        audit.findings.append(Finding(
            "S1-VALUES", "artifact-integrity", "PASS", "INFO",
            "No generated values are registered for this paper.",
            (f"papers/{paper}/main.tex",),
        ))
        return set(), {}

    try:
        receipt = gen_values.read_receipt(paper)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        audit.findings.append(Finding(
            "S1-VALUES-RECEIPT", "artifact-integrity", "FAIL", "CRITICAL",
            str(exc), (f"papers/{paper}/results/values_receipt.json",),
        ))
        return set(), {}

    macros = set(receipt.get("values", {}))
    expected = gen_values.render(paper, receipt)
    values_path = gen_values.values_path(paper)
    actual = (
        values_path.read_text(encoding="utf-8")
        if values_path.is_file() else None
    )
    _finding(
        audit, "S1-VALUES-RENDER", "artifact-integrity", actual == expected,
        f"values.tex matches its receipt ({len(macros)} macros).",
        "values.tex is missing or stale relative to values_receipt.json.",
        (f"papers/{paper}/values.tex",
         f"papers/{paper}/results/values_receipt.json"),
    )

    if recompute:
        drift = gen_values.receipt_drift(paper)
        _finding(
            audit, "S1-VALUES-RECOMPUTE", "artifact-integrity", not drift,
            "The receipt matches a fresh, read-only instrument recomputation.",
            "Generated values or source fingerprints drifted: "
            + ", ".join(sorted(drift)),
            (f"papers/{paper}/results/values_receipt.json",),
        )
    else:
        audit.findings.append(Finding(
            "S1-VALUES-RECOMPUTE", "artifact-integrity", "SKIP", "WARNING",
            "Instrument recomputation was explicitly skipped.",
            (f"papers/{paper}/results/values_receipt.json",),
        ))
    return macros, receipt


def _audit_claims(
    audit: Audit,
    paper: str,
    generated_macros: set[str],
) -> None:
    registered = claims.claims_for(paper) if paper in claims.REGISTRY else []
    moved = claims.source_drift(paper) if registered else []
    failing = claims.failing(paper) if registered else []

    _finding(
        audit, "S1-CLAIM-ANCHORS", "artifact-integrity", not moved,
        f"All {len(registered)} registered claim anchors still match.",
        "Registered claim anchors moved or changed: "
        + ", ".join(c.key for c in moved),
        tuple(c.site.split(":")[0] for c in moved),
    )
    _finding(
        audit, "S1-CLAIM-PREDICATES", "artifact-integrity", not failing,
        f"All {len(registered)} registered claim predicates hold.",
        "Registered conclusions no longer follow from their values: "
        + ", ".join(c.key for c in failing),
        tuple(c.site for c in failing),
    )

    claimed_macros = {
        macro for claim in registered for macro in claim.depends_on
    }
    orphan_macros = generated_macros - claimed_macros
    _finding(
        audit, "S1-GENERATED-COVERAGE", "coverage", not orphan_macros,
        "Every generated macro feeds at least one registered claim.",
        "Generated macros with no registered conclusion: "
        + ", ".join(sorted(orphan_macros)),
        (f"instruments/tools/claims.py",),
    )

    audit.registered_claims = [{
        "claim_id": claim.key,
        "site": claim.site,
        "asserts": claim.asserts,
        "depends_on": list(claim.depends_on),
        "tolerance": claim.tolerance,
        "note": claim.note,
        "deterministic_predicate": "PASS" if claim not in failing else "FAIL",
        "semantic_question": (
            "Does the predicate test the stated conclusion, and is the "
            "conclusion warranted by the underlying derivation?"
        ),
    } for claim in registered]

    audit.coverage.update({
        "generated_macros": sorted(generated_macros),
        "generated_macros_guarded": sorted(generated_macros & claimed_macros),
        "registered_claim_count": len(registered),
    })


def _audit_change_record(audit: Audit, paper: str) -> None:
    try:
        message = build_paper.gate_change_records(paper)
    except build_paper.GateFailure as exc:
        _finding(
            audit, "S1-CHANGE-RECORD", "artifact-integrity", False, "",
            str(exc), (f"papers/{paper}/main.tex",
                       f"papers/{paper}/CHANGELOG.md"),
        )
    else:
        _finding(
            audit, "S1-CHANGE-RECORD", "artifact-integrity", True,
            message, "", (f"papers/{paper}/main.tex",
                          f"papers/{paper}/CHANGELOG.md"),
        )


def _build_citation_queue(
    audit: Audit,
    paper: str,
    tex: str,
) -> None:
    registry = citation_evidence.load_registry()
    catalog = registry.get("citation_notes", {})
    sources = registry.get("sources", {})
    source = f"papers/{paper}/main.tex"
    keys = sorted(bibliography.citation_keys(PAPERS / paper / "main.tex"))

    queue = []
    for key in keys:
        note_record = catalog.get(key, {})
        source_record = sources.get(key, {})
        verdict = source_record.get("verification", {}).get("status")
        review_status = note_record.get("review_status", "MISSING")
        if verdict in NON_OK_CITATION_VERDICTS:
            priority = "HIGH"
        elif verdict in PENDING_CITATION_VERDICTS or review_status == "MISSING":
            priority = "MEDIUM"
        else:
            priority = "NORMAL"
        queue.append({
            "cite_key": key,
            "locations": citation_locations(tex, key, source),
            "evidence_note": f"papers/cited/notes/{key}.md",
            "review_status": review_status,
            "recorded_evidence_verdict": verdict or review_status,
            "priority": priority,
            "semantic_question": (
                "Does every current manuscript use match the evidence note? "
                "A historical negative verdict may now be cited accurately "
                "as a negative result, so do not copy the verdict blindly."
            ),
        })
    audit.citation_review_queue = queue
    audit.coverage["citation_count"] = len(keys)
    audit.coverage["citation_high_priority"] = sum(
        item["priority"] == "HIGH" for item in queue)
    audit.coverage["citation_medium_priority"] = sum(
        item["priority"] == "MEDIUM" for item in queue)


def audit_paper(paper: str, recompute: bool = True) -> Audit:
    paper_dir = PAPERS / paper
    main_tex = paper_dir / "main.tex"
    if not main_tex.is_file():
        raise FileNotFoundError(f"{main_tex.relative_to(REPO_ROOT)} not found")

    tex = main_tex.read_text(encoding="utf-8")
    audit = Audit(
        paper=paper,
        generated_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        recomputed_instruments=recompute,
    )

    _audit_bibliography_and_evidence(audit, paper)
    _audit_provenance(audit, paper, tex)
    generated_macros, _receipt = _audit_values(audit, paper, recompute)
    _audit_claims(audit, paper, generated_macros)
    _audit_change_record(audit, paper)
    _build_citation_queue(audit, paper, tex)
    audit.numeric_review_queue = extract_numeric_candidates(
        tex, generated_macros, f"papers/{paper}/main.tex")
    audit.coverage["numeric_candidate_count"] = len(
        audit.numeric_review_queue)
    audit.coverage["manual_numeric_candidate_count"] = sum(
        item["classification"] == "MANUAL_NUMERIC_CANDIDATE"
        for item in audit.numeric_review_queue
    )
    return audit


def render_markdown(audit: Audit, numeric_limit: int = 40) -> str:
    data = audit.to_dict()
    lines = [
        f"# SSV Verify — {audit.paper}",
        "",
        f"Generated: `{audit.generated_utc}`",
        "",
        f"**Verdict: `{audit.verdict}`**",
        "",
        "The deterministic result and semantic queue are separate. A green "
        "predicate proves only that a registered relationship still holds; it "
        "does not prove that the relationship was intellectually sound when "
        "registered.",
        "",
        "## Deterministic checks",
        "",
        "| Check | Stage | Status | Finding |",
        "|---|---|---|---|",
    ]
    for finding in audit.findings:
        refs = ", ".join(f"`{ref}`" for ref in finding.refs)
        suffix = f" ({refs})" if refs else ""
        lines.append(
            f"| `{finding.check_id}` | {finding.stage} | "
            f"**{finding.status}** | {finding.message}{suffix} |")

    lines += [
        "",
        "## Coverage",
        "",
        "```json",
        json.dumps(audit.coverage, indent=2, sort_keys=True),
        "```",
        "",
        "## Registered-claim semantic review",
        "",
    ]
    for claim in audit.registered_claims:
        lines += [
            f"### `{claim['claim_id']}`",
            "",
            f"- Site: `{claim['site']}`",
            f"- Statement: {claim['asserts']}",
            f"- Inputs: `{', '.join(claim['depends_on']) or '(symbolic)'}`",
            f"- Tolerance: {claim['tolerance']}",
            f"- Predicate: **{claim['deterministic_predicate']}**",
            f"- Review question: {claim['semantic_question']}",
            "",
        ]

    lines += [
        "## Citation semantic review queue",
        "",
        "| Priority | Key | Recorded verdict | Current uses | Evidence |",
        "|---|---|---|---|---|",
    ]
    for item in audit.citation_review_queue:
        uses = ", ".join(f"`{loc}`" for loc in item["locations"]) or "(none)"
        lines.append(
            f"| **{item['priority']}** | `{item['cite_key']}` | "
            f"`{item['recorded_evidence_verdict']}` | {uses} | "
            f"`{item['evidence_note']}` |")

    lines += [
        "",
        "## Manual numeric review queue",
        "",
        f"Showing the first {min(numeric_limit, len(audit.numeric_review_queue))} "
        f"of {len(audit.numeric_review_queue)} candidates. Candidate status is "
        "not a defect verdict.",
        "",
        "| Location | Token | Classification | Snippet |",
        "|---|---|---|---|",
    ]
    for item in audit.numeric_review_queue[:numeric_limit]:
        snippet = item["snippet"].replace("|", r"\|")
        lines.append(
            f"| `{item['location']}` | `{item['token']}` | "
            f"{item['classification']} | {snippet} |")

    lines += [
        "",
        "## Summary",
        "",
        f"- Deterministic failures: "
        f"{data['summary']['deterministic_failures']}",
        f"- Registered claims awaiting semantic review: "
        f"{data['summary']['registered_claims']}",
        f"- Citation uses awaiting semantic review: "
        f"{data['summary']['citation_claims_queued']}",
        f"- Numeric candidates awaiting classification: "
        f"{data['summary']['numeric_candidates_queued']}",
        "",
    ]
    return "\n".join(lines)


def _write_new(path: Path, content: str) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing report: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper", help="paper directory name, e.g. SSV-I")
    parser.add_argument(
        "--no-recompute", action="store_true",
        help="skip fresh instrument execution; all other checks still run")
    parser.add_argument("--json-out", type=Path, help="write a new JSON report")
    parser.add_argument("--md-out", type=Path, help="write a new Markdown report")
    args = parser.parse_args()

    try:
        audit = audit_paper(args.paper, recompute=not args.no_recompute)
        payload = json.dumps(audit.to_dict(), indent=2) + "\n"
        if args.json_out:
            _write_new(args.json_out, payload)
        if args.md_out:
            _write_new(args.md_out, render_markdown(audit))
    except (FileNotFoundError, FileExistsError, KeyError, ValueError) as exc:
        print(f"ssv-verify: {exc}", file=sys.stderr)
        return 2

    if not args.json_out and not args.md_out:
        print(payload, end="")
    return 1 if audit.deterministic_failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
