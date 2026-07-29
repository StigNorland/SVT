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
    python instruments/tools/ssv_verify.py SSV-I --all-numbers
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
SECTION_RE = re.compile(
    r"\\(?:part|chapter|section|subsection|subsubsection)\*?\{([^{}]+)\}")
BEGIN_RE = re.compile(r"\\begin\{([^{}]+)\}")
END_RE = re.compile(r"\\end\{([^{}]+)\}")

HIGH_VALUE_ENVIRONMENTS = {
    "abstract", "resultbox", "falsbox", "gapbox",
}
HIGH_VALUE_SECTION_TERMS = {
    "abstract", "claim status", "conclusion", "result", "summary",
}
HIGH_VALUE_NUMERIC_CUES = re.compile(
    r"\b(?:derived|falsif\w*|withdrawn|retracted|no-go|match(?:es|ed|ing)?|"
    r"agreement|disagreement|within|factor|bound|prediction|observed|"
    r"candidate|coincidence|excluded|shortfall|larger|smaller|exceeds|"
    r"below|above|minimum|maximum)\b",
    flags=re.IGNORECASE,
)
MEDIUM_VALUE_NUMERIC_CUES = re.compile(
    r"(?:\\approx|\\sim|\\lesssim|\\gtrsim|\b(?:ratio|percent|error|grid|"
    r"resolution|sweep|uncertainty|mass|energy|radius|density|speed|"
    r"temperature|coefficient|offset|value)\b)",
    flags=re.IGNORECASE,
)
DISPLAY_MATH_ENVIRONMENTS = {
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "multline", "multline*",
}
LAYOUT_ONLY_LINE_RES = (
    re.compile(
        r"^\s*\\renewcommand\{\\arraystretch\}"
        r"(?:\[[^]]*\])?\{[^{}]*\}\s*$"
    ),
    re.compile(
        r"^\s*\\begin\{(?:array|tabular|tabularx|longtable)\}"
        r"(?:\[[^]]*\])?\{.*\}\s*$"
    ),
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
    include_all_numbers: bool = False
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
            "schema": "ssv-verify/v2",
            "paper": self.paper,
            "generated_utc": self.generated_utc,
            "recomputed_instruments": self.recomputed_instruments,
            "include_all_numbers": self.include_all_numbers,
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


def tex_contexts(tex: str) -> dict[int, dict[str, Any]]:
    """Return the current section and LaTeX environment stack per line."""
    contexts: dict[int, dict[str, Any]] = {}
    environments: list[str] = []
    section = ""
    for lineno, raw in enumerate(tex.splitlines(), start=1):
        line = _without_comments(raw)
        section_match = SECTION_RE.search(line)
        if section_match:
            section = section_match.group(1).strip()
        for match in BEGIN_RE.finditer(line):
            environments.append(match.group(1))
        contexts[lineno] = {
            "section": section,
            "environments": tuple(environments),
        }
        for match in END_RE.finditer(line):
            environment = match.group(1)
            for index in range(len(environments) - 1, -1, -1):
                if environments[index] == environment:
                    del environments[index]
                    break
    return contexts


def source_snippet(tex: str, lineno: int, radius: int = 1) -> str:
    """Join nearby non-comment source lines into a compact review excerpt."""
    lines = tex.splitlines()
    start = max(0, lineno - radius - 1)
    end = min(len(lines), lineno + radius)
    selected = [
        _without_comments(line).strip()
        for line in lines[start:end]
        if _without_comments(line).strip()
    ]
    return " ".join(selected)


def _numeric_priority(
    line: str,
    context: dict[str, Any],
) -> tuple[str, tuple[str, ...]]:
    """Prioritize review without turning a heuristic into a defect verdict."""
    reasons: list[str] = []
    environments = set(context["environments"])
    section = context["section"].lower()
    if environments & HIGH_VALUE_ENVIRONMENTS:
        reasons.append("high-value-environment")
    if any(
        re.search(rf"\b{re.escape(term)}s?\b", section)
        for term in HIGH_VALUE_SECTION_TERMS
    ):
        reasons.append("high-value-section")
    if HIGH_VALUE_NUMERIC_CUES.search(line):
        reasons.append("claim-language")
    if reasons:
        return "HIGH", tuple(reasons)
    if environments & DISPLAY_MATH_ENVIRONMENTS:
        return "LOW", ("display-math",)
    if MEDIUM_VALUE_NUMERIC_CUES.search(line):
        return "MEDIUM", ("quantitative-prose",)
    return "LOW", ("background-or-unclassified",)


def _is_layout_only_numeric_line(line: str) -> bool:
    """Return true for table-formatting commands with no manuscript datum."""
    return any(pattern.fullmatch(line) for pattern in LAYOUT_ONLY_LINE_RES)


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
    contexts = tex_contexts(tex)
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
        if _is_layout_only_numeric_line(line):
            continue
        used_macros = sorted(
            macro for macro in generated_macros if f"\\{macro}" in line
        )
        tokens = [match.group(0) for match in NUMERIC_CANDIDATE_RE.finditer(line)]
        if not tokens:
            continue
        context = contexts[lineno]
        priority, reasons = _numeric_priority(line, context)
        candidates.append({
            "review_id": f"NUM-{lineno}",
            "location": f"{source}:{lineno}",
            "tokens": tokens,
            "generated_macros_on_line": used_macros,
            "classification": (
                "MIXED_WITH_GENERATED_VALUE" if used_macros
                else "MANUAL_NUMERIC_CANDIDATE"
            ),
            "priority": priority,
            "priority_reasons": list(reasons),
            "section": context["section"],
            "environments": list(context["environments"]),
            "snippet": source_snippet(tex, lineno),
        })
    return candidates


def citation_uses(tex: str, key: str, source: str) -> list[dict[str, Any]]:
    """Return context-rich, line-level uses of a BibTeX key."""
    uses = []
    cite_re = re.compile(r"\\cite\w*\{([^{}]+)\}")
    contexts = tex_contexts(tex)
    for lineno, raw in enumerate(tex.splitlines(), start=1):
        line = _without_comments(raw)
        cited = {
            item.strip()
            for match in cite_re.finditer(line)
            for item in match.group(1).split(",")
        }
        if key in cited:
            context = contexts[lineno]
            uses.append({
                "review_id": f"CITE-{key}-{lineno}",
                "location": f"{source}:{lineno}",
                "section": context["section"],
                "environments": list(context["environments"]),
                "snippet": source_snippet(tex, lineno),
            })
    return uses


def _normalised_with_lines(text: str) -> tuple[str, list[int]]:
    """Collapse whitespace while retaining a source line for every character."""
    out: list[str] = []
    source_lines: list[int] = []
    pending_space = False
    pending_line = 1
    for lineno, line in enumerate(text.splitlines(keepends=True), start=1):
        for char in line:
            if char.isspace():
                if out:
                    pending_space = True
                    pending_line = lineno
                continue
            if pending_space:
                out.append(" ")
                source_lines.append(pending_line)
                pending_space = False
            out.append(char)
            source_lines.append(lineno)
    return "".join(out), source_lines


def current_claim_location(claim: claims.Claim) -> tuple[str, str]:
    """Resolve a registered anchor to its current line rather than stale metadata."""
    relative_path = claim.site.rsplit(":", 1)[0]
    source_path = REPO_ROOT / relative_path
    try:
        text = source_path.read_text(encoding="utf-8")
    except OSError:
        return relative_path, ""
    normalised, source_lines = _normalised_with_lines(text)
    anchor = re.sub(r"\s+", " ", claim.source_anchor).strip()
    index = normalised.find(anchor) if anchor else -1
    if index < 0 or index >= len(source_lines):
        return relative_path, ""
    lineno = source_lines[index]
    return f"{relative_path}:{lineno}", source_snippet(text, lineno)


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

    path = PAPERS / paper / "provenance.tex"
    actual = path.read_text(encoding="utf-8") if path.is_file() else None
    has_references = bool(issues or paths or reports)
    expected = (
        gen_provenance.render(
            paper, issues, paths, reports, gen_provenance.repo_slug())
        if has_references
        else None
    )
    _finding(
        audit, "S1-PROVENANCE-RENDER", "artifact-integrity",
        actual == expected,
        (
            "provenance.tex matches the current manuscript references."
            if has_references
            else "No provenance references require a generated appendix."
        ),
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

    audit.registered_claims = []
    for claim in registered:
        current_location, snippet = current_claim_location(claim)
        audit.registered_claims.append({
            "review_id": f"CLAIM-{claim.key}",
            "claim_id": claim.key,
            "registered_site": claim.site,
            "current_location": current_location,
            "current_snippet": snippet,
            "asserts": claim.asserts,
            "depends_on": list(claim.depends_on),
            "tolerance": claim.tolerance,
            "note": claim.note,
            "deterministic_predicate": (
                "PASS" if claim not in failing else "FAIL"),
            "semantic_question": (
                "Does the predicate test the stated conclusion, and is the "
                "conclusion warranted by the underlying derivation?"
            ),
        })

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
        uses = citation_uses(tex, key, source)
        queue.append({
            "review_id": f"CITATION-{key}",
            "cite_key": key,
            "uses": uses,
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
    audit.coverage["citation_use_count"] = sum(
        len(item["uses"]) for item in queue)
    audit.coverage["citation_high_priority"] = sum(
        item["priority"] == "HIGH" for item in queue)
    audit.coverage["citation_medium_priority"] = sum(
        item["priority"] == "MEDIUM" for item in queue)


def audit_paper(
    paper: str,
    recompute: bool = True,
    include_all_numbers: bool = False,
) -> Audit:
    paper_dir = PAPERS / paper
    main_tex = paper_dir / "main.tex"
    if not main_tex.is_file():
        raise FileNotFoundError(f"{main_tex.relative_to(REPO_ROOT)} not found")

    tex = main_tex.read_text(encoding="utf-8")
    audit = Audit(
        paper=paper,
        generated_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        recomputed_instruments=recompute,
        include_all_numbers=include_all_numbers,
    )

    _audit_bibliography_and_evidence(audit, paper)
    _audit_provenance(audit, paper, tex)
    generated_macros, _receipt = _audit_values(audit, paper, recompute)
    _audit_claims(audit, paper, generated_macros)
    _audit_change_record(audit, paper)
    _build_citation_queue(audit, paper, tex)
    numeric_inventory = extract_numeric_candidates(
        tex, generated_macros, f"papers/{paper}/main.tex")
    audit.numeric_review_queue = [
        item for item in numeric_inventory
        if include_all_numbers or item["priority"] != "LOW"
    ]
    audit.coverage["numeric_line_inventory_count"] = len(numeric_inventory)
    audit.coverage["numeric_token_inventory_count"] = sum(
        len(item["tokens"]) for item in numeric_inventory)
    audit.coverage["numeric_review_queue_count"] = len(
        audit.numeric_review_queue)
    audit.coverage["numeric_low_priority_omitted"] = sum(
        item["priority"] == "LOW" for item in numeric_inventory
        if not include_all_numbers)
    audit.coverage["numeric_priority_counts"] = {
        priority: sum(
            item["priority"] == priority for item in numeric_inventory)
        for priority in ("HIGH", "MEDIUM", "LOW")
    }
    audit.coverage["manual_numeric_candidate_count"] = sum(
        item["classification"] == "MANUAL_NUMERIC_CANDIDATE"
        for item in numeric_inventory
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
            f"### `{claim['review_id']}`",
            "",
            f"- Current location: `{claim['current_location']}`",
            f"- Registered site metadata: `{claim['registered_site']}`",
            f"- Current source: {claim['current_snippet']}",
            f"- Statement: {claim['asserts']}",
            f"- Inputs: `{', '.join(claim['depends_on']) or '(symbolic)'}`",
            f"- Tolerance: {claim['tolerance']}",
            f"- Predicate: **{claim['deterministic_predicate']}**",
            f"- Review question: {claim['semantic_question']}",
            "",
        ]

    lines += [
        "## Prioritized citation semantic review",
        "",
    ]
    prioritized_citations = [
        item for item in audit.citation_review_queue
        if item["priority"] != "NORMAL"
    ]
    prioritized_citations.sort(
        key=lambda item: {"HIGH": 0, "MEDIUM": 1}[item["priority"]])
    for item in prioritized_citations:
        lines += [
            f"### {item['priority']} — `{item['review_id']}`",
            "",
            f"- Recorded evidence verdict: "
            f"`{item['recorded_evidence_verdict']}`",
            f"- Evidence: `{item['evidence_note']}`",
        ]
        for use in item["uses"]:
            context = use["section"] or "(no section)"
            lines += [
                f"- `{use['review_id']}` — `{use['location']}` — "
                f"section: {context}",
                f"  - {use['snippet']}",
            ]
        lines.append("")

    lines += [
        "### Normal-priority citations",
        "",
        "Retained in the JSON queue; compacted here so routine `OK` sources do "
        "not bury the exception cases.",
        "",
        "| Key | Uses | Evidence |",
        "|---|---|---|",
    ]
    for item in audit.citation_review_queue:
        if item["priority"] != "NORMAL":
            continue
        locations = ", ".join(
            f"`{use['location']}`" for use in item["uses"]) or "(none)"
        lines.append(
            f"| `{item['cite_key']}` | {locations} | "
            f"`{item['evidence_note']}` |")

    lines += [
        "",
        "## Manual numeric review queue",
        "",
        f"Showing the first {min(numeric_limit, len(audit.numeric_review_queue))} "
        f"of {len(audit.numeric_review_queue)} prioritized lines. Candidate "
        "status is not a defect verdict. Low-priority lines are counted but "
        "omitted unless `--all-numbers` is used.",
        "",
        "| Priority | Review ID | Location | Tokens | Context | Snippet |",
        "|---|---|---|---|---|---|",
    ]
    numeric_queue = sorted(
        audit.numeric_review_queue,
        key=lambda item: (
            {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[item["priority"]],
            int(item["review_id"].split("-")[1]),
        ),
    )
    for item in numeric_queue[:numeric_limit]:
        snippet = item["snippet"].replace("|", r"\|")
        tokens = ", ".join(f"`{token}`" for token in item["tokens"])
        context = item["section"] or ", ".join(item["environments"]) or "prose"
        lines.append(
            f"| **{item['priority']}** | `{item['review_id']}` | "
            f"`{item['location']}` | {tokens} | {context} | {snippet} |")

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
    parser.add_argument(
        "--all-numbers", action="store_true",
        help="include low-priority numeric lines in the semantic review queue")
    parser.add_argument("--json-out", type=Path, help="write a new JSON report")
    parser.add_argument("--md-out", type=Path, help="write a new Markdown report")
    args = parser.parse_args()

    try:
        audit = audit_paper(
            args.paper,
            recompute=not args.no_recompute,
            include_all_numbers=args.all_numbers,
        )
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
