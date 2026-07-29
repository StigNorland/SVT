"""Build an SSV paper, running every gate first (#198 Part D).

The standing rules already say what a correct build does — validate the shared
bibliography and citation evidence (rule 12), regenerate provenance (rule 11),
regenerate values (rule 14), run ``pdflatex``/BibTeX to convergence with 0
errors (rule 8), and move the PDF to ``papers/pdf/`` under its human name
(rule 3).

This runs it, in order, and **refuses to build a paper whose registered numerical
relationships have drifted** (owner's instruction, 2026-07-28: *"we need to
record our failure mode and test at every compile"*). The point is the ordering:
the gates run *before* ``pdflatex``, so a reviewed result that no longer follows
from its inputs does not produce a PDF that looks finished.

    1. shared BibTeX database and paper citation keys valid rule 12
    2. citation quote/use evidence is structurally complete rule 12
    3. provenance regenerated + no unresolved refs         rule 11
    4. values receipt matches its instruments              rule 14
    5. every registered relationship still holds           #198 Part D
    6. values.tex rendered from the receipt                rule 14
    7. pdflatex -> BibTeX -> pdflatex x2, clean             rule 8
    8. PDF copied to papers/pdf/<Human Name>.pdf           rule 3

Gate 4 closes the failure mode Part A left open: an intentional instrument and
receipt update can move a generated number after a result was reviewed. It
detects that later drift; it does not judge whether the original conclusion was
semantically correct. See ``docs/failure-modes.md``.

Usage:
    python instruments/tools/build_paper.py SSV-I
    python instruments/tools/build_paper.py --all
    python instruments/tools/build_paper.py --all --gate-only   # no pdflatex
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS = REPO_ROOT / "papers"
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import claims  # noqa: E402
import bibliography  # noqa: E402
import conventions  # noqa: E402
import citation_evidence  # noqa: E402
import gen_provenance  # noqa: E402
import gen_values  # noqa: E402


def human_name(paper: str) -> str:
    """SSV-I -> 'SSV I', SSV-VII-b -> 'SSV VII-b' (rule 3's tracked names)."""
    return paper.replace("SSV-", "SSV ", 1)


class GateFailure(Exception):
    pass


# --------------------------------------------------------------------------
# gates
# --------------------------------------------------------------------------

def gate_citations(paper: str) -> str:
    issues = citation_evidence.evidence_issues()
    if issues:
        detail = "\n".join(f"      {issue}" for issue in issues)
        raise GateFailure(
            f"{len(issues)} citation-evidence defect(s):\n{detail}")
    return (
        f"{len(citation_evidence.citation_note_keys())} notes, "
        f"{len(citation_evidence.registered_keys())} evidence records complete"
    )


def gate_bibliography(paper: str) -> str:
    issues = bibliography.issues_for(paper)
    if issues:
        detail = "\n".join(f"      {issue}" for issue in issues)
        raise GateFailure(f"{len(issues)} bibliography defect(s):\n{detail}")
    cited = bibliography.citation_keys(PAPERS / paper / "main.tex")
    return (
        f"{len(cited)} cited keys, "
        f"{len(bibliography.database_keys())} shared entries"
    )


def gate_provenance(paper: str) -> str:
    r = gen_provenance.generate(paper, gen_provenance.repo_slug(), check=False)
    if r["missing"]:
        raise GateFailure(f"unresolved code/report references: {r['missing']}")
    return (f"{len(r['issues'])} issues, {len(r['paths'])} scripts, "
            f"{len(r['reports'])} reports")


def gate_values(paper: str) -> str:
    if not gen_values.has_values(paper):
        return "no generated values registered"
    local_drift = (
        gen_values.receipt_drift(paper)
        if paper in gen_values.REGISTRY else {}
    )
    shared_drift = (
        gen_values.shared_receipt_drift()
        if gen_values.shared_values_for(paper) else {}
    )
    if local_drift or shared_drift:
        raise GateFailure(
            f"receipt no longer matches its instruments: local "
            f"{sorted(local_drift)}, shared {sorted(shared_drift)} — run "
            f"`gen_values.py --all --compute`")
    literals = gen_values.surviving_shared_literals(paper)
    if literals:
        raise GateFailure(
            f"registered shared values survive as typed literals: {literals} — "
            f"use their \\ssv* macros (#213 Part C)")
    local_n = (
        len(gen_values.values_for(paper))
        if paper in gen_values.REGISTRY else 0
    )
    shared_n = len(gen_values.shared_values_for(paper))
    return (
        f"{local_n} local + {shared_n} shared values, receipts current; "
        f"no registered shared literal survives"
    )


def gate_claims(paper: str) -> str:
    registered = claims.claims_for(paper)
    if not registered:
        return "no claims registered"
    moved = claims.source_drift(paper)
    if moved:
        detail = "\n".join(f"      {c.site}  {c.key}" for c in moved)
        raise GateFailure(
            f"{len(moved)} registered statement(s) moved or changed:\n{detail}")
    bad = claims.failing(paper)
    if bad:
        detail = "\n".join(f"      {c.site}  {c.key}\n        asserts: {c.asserts}"
                           for c in bad)
        raise GateFailure(
            f"{len(bad)} conclusion(s) no longer follow from their values:\n{detail}")
    return f"{len(registered)} claims hold"


#: Phrases that narrate a paper's own edit history rather than its current
#: state (#207).  Deliberately a short, literal deny-list rather than anything
#: clever: it catches the *phrasing*, not the intent, and a determined author
#: can write history in fresh words and pass.  A drift guard, like rules 15 and
#: 16 — see FM15.
#:
#: What is NOT here, and must not be added: "withdrawn", "falsified",
#: "retracted", "rejected".  Those state a CURRENT verdict.  Banning them would
#: turn this gate into a tool for deleting negative results, which is the exact
#: defect #182 existed to find (standing rule 1).
CHANGE_RECORD_PHRASES = (
    "earlier version",
    "previous version",
    "previously claimed",
    "previously concluded",
    "previously printed",
    "previously credited",
    "previously stated",
    "previously derived",
    "previously headlined",
    "this replaces the result",
    "the superseded",
    "originally claimed",
    "as it stood",
    "in earlier drafts",
    "no longer says",
)


def gate_change_records(paper: str) -> str:
    """Rule 17: a paper states current status; its history lives in CHANGELOG.md."""
    changelog = PAPERS / paper / "CHANGELOG.md"
    if not changelog.is_file():
        raise GateFailure(
            f"no CHANGELOG.md — every paper needs one, so removed history has "
            f"somewhere to go (rule 17)")
    text = (PAPERS / paper / "main.tex").read_text(
        encoding="utf-8", errors="replace").lower()
    found = sorted(p for p in CHANGE_RECORD_PHRASES if p in text)
    if found:
        raise GateFailure(
            f"main.tex narrates its own edit history: {found} — state the "
            f"current status in the paper and move the history to "
            f"papers/{paper}/CHANGELOG.md (rule 17)")
    return f"current-status only; CHANGELOG.md present"


def gate_conventions(paper: str) -> str:
    """#213 Part A: one meaning, one dimension per symbol across the programme.

    Fails on a collision that is **not** already recorded in
    ``conventions.KNOWN_COLLISIONS`` or on a reserved spelling used with a
    non-standard meaning.  The four known collisions stay known: the
    cosmological constant and the MOND scale are standard notation in their own
    literatures, so resolving them is a declaration the author makes, not a
    rename this gate can impose.  What it does enforce is that no fourth
    arrives quietly.
    """
    reserved = conventions.reserved_symbol_violations(paper)
    if reserved:
        detail = "\n".join(f"      {item}" for item in reserved)
        raise GateFailure(
            f"{len(reserved)} reserved-symbol violation(s):\n{detail}")
    fresh, note = conventions.gate_report(paper)
    if fresh:
        detail = "\n".join(f"      {c.describe()}" for c in fresh)
        raise GateFailure(
            f"{len(fresh)} undeclared symbol collision(s):\n{detail}\n"
            f"      Declare the reuse in conventions.USES with a reason, or "
            f"rename the symbol.")
    return note


def render_values(paper: str) -> str:
    if not gen_values.has_values(paper):
        return "skipped"
    r = gen_values.generate(paper)
    return f"values.tex {'rewritten' if r['changed'] else 'unchanged'}"


# --------------------------------------------------------------------------
# latex
# --------------------------------------------------------------------------

def run_pdflatex(paper: str) -> str:
    d = PAPERS / paper

    def run(command: list[str], stage: str) -> None:
        try:
            result = subprocess.run(
                command,
                cwd=d, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
            )
        except OSError as exc:
            raise GateFailure(f"could not start {stage}: {exc}") from exc
        if result.returncode != 0:
            output = (result.stderr or result.stdout).strip().splitlines()
            tail = "\n      ".join(output[-5:]) if output else "(no process output)"
            raise GateFailure(
                f"{stage} exited {result.returncode}:\n      {tail}")

    run(["pdflatex", "-interaction=nonstopmode", "main.tex"],
        "pdflatex pass 1")
    run(["bibtex", "main"], "BibTeX")
    run(["pdflatex", "-interaction=nonstopmode", "main.tex"],
        "pdflatex pass 2")
    run(["pdflatex", "-interaction=nonstopmode", "main.tex"],
        "pdflatex pass 3")

    log_path = d / "main.log"
    if not log_path.is_file():
        raise GateFailure("pdflatex produced no main.log")
    log = log_path.read_text(encoding="utf-8", errors="replace")
    errors = [l for l in log.splitlines() if l.startswith("!")]
    if errors:
        raise GateFailure("pdflatex errors:\n      " + "\n      ".join(errors[:5]))
    if not (d / "main.pdf").is_file():
        raise GateFailure("pdflatex produced no main.pdf")
    undefined = re.findall(r"Warning: (?:Citation|Reference) `([^']+)' .*undefined", log)
    has_undefined_summary = re.search(
        r"(?:undefined references|undefined citations)", log, flags=re.IGNORECASE)
    if undefined or has_undefined_summary:
        detail = sorted(set(undefined)) or ["see main.log"]
        raise GateFailure(f"undefined references or citations: {detail}")
    return "BibTeX + 3 pdflatex passes, 0 errors, 0 undefined references"


def copy_pdf(paper: str) -> str:
    dest = PAPERS / "pdf" / f"{human_name(paper)}.pdf"
    shutil.copyfile(PAPERS / paper / "main.pdf", dest)
    return f"-> papers/pdf/{dest.name}"


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------

def build(paper: str, gate_only: bool) -> bool:
    print(f"\n=== {paper} ===")
    steps = [("bibliography(rule 12)", gate_bibliography),
             ("citations   (rule 12)", gate_citations),
             ("provenance  (rule 11)", gate_provenance),
             ("values      (rule 14)", gate_values),
             ("claims      (Part D) ", gate_claims),
             ("changelog   (rule 17)", gate_change_records),
             ("symbols     (#213 A) ", gate_conventions)]
    if not gate_only:
        steps += [("render values       ", render_values),
                  ("pdflatex    (rule 8) ", run_pdflatex),
                  ("publish     (rule 3) ", copy_pdf)]
    for label, fn in steps:
        try:
            print(f"  ok   {label}  {fn(paper)}")
        except GateFailure as exc:
            print(f"  FAIL {label}  {exc}")
            return False
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paper", nargs="?")
    ap.add_argument("--all", action="store_true",
                    help="every papers/SSV-*/main.tex")
    ap.add_argument("--gate-only", action="store_true",
                    help="run the gates, do not run pdflatex or publish")
    args = ap.parse_args()

    if args.all:
        papers = sorted(p.parent.name for p in PAPERS.glob("SSV-*/main.tex"))
    elif args.paper:
        papers = [args.paper]
    else:
        ap.error("give a paper name or --all")

    failed = [p for p in papers if not build(p, args.gate_only)]
    print()
    if failed:
        print(f"FAILED: {failed}")
        sys.exit(1)
    print(f"all {len(papers)} paper(s) passed every gate.")


if __name__ == "__main__":
    main()
