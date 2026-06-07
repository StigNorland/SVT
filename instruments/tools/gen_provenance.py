"""Generate the "Code and Issue References" provenance appendix for SSV papers.

Every paper cites GitHub issues (`\\#NN`) and Python scripts (`\\texttt{instruments/...}`).
This tool makes each reference *checkable*: it scans a paper's `main.tex`, resolves
each issue to its GitHub URL and each script to a permalink pinned at the commit
that last modified it, and writes `papers/<PAPER>/provenance.tex` for the paper to
`\\input` inside an appendix.

Design (decided 2026-06-07):
  * per-script permalink, pinned to the commit that last modified the file;
  * auto-generated (regenerate before a build/release — it cannot drift);
  * rendered as an appendix section.

Usage:
    python instruments/tools/gen_provenance.py SSV-I        # one paper
    python instruments/tools/gen_provenance.py --all        # every papers/SSV-*/main.tex
    python instruments/tools/gen_provenance.py --all --check # report broken refs, write nothing
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PAPERS = REPO_ROOT / "papers"

ISSUE_RE = re.compile(r"\\#(\d+)")
SSVISSUE_RE = re.compile(r"\\ssvissue\{(\d+)\}")   # body refs after cross-ref wiring
TEXTTT_RE = re.compile(r"\\texttt\{([^{}]*)\}", re.DOTALL)


# --------------------------------------------------------------------------
# Git helpers
# --------------------------------------------------------------------------

def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True, text=True, check=True,
    ).stdout.strip()


def repo_slug() -> str:
    """e.g. 'StigNorland/SVT' from the origin remote URL."""
    url = _git("remote", "get-url", "origin")
    m = re.search(r"github\.com[:/](.+?)(?:\.git)?$", url)
    return m.group(1) if m else "StigNorland/SVT"


def head_commit() -> str:
    return _git("rev-parse", "--short", "HEAD")


def last_commit(path: str) -> str | None:
    """Short SHA of the commit that last modified `path`, or None if untracked."""
    sha = _git("log", "-1", "--format=%h", "--", path)
    return sha or None


# --------------------------------------------------------------------------
# Reference extraction
# --------------------------------------------------------------------------

def _normalise_path(raw: str) -> str:
    """Strip LaTeX whitespace/line-wraps and unescape `\\_` etc. in a path."""
    p = re.sub(r"\s+", "", raw)                 # paths contain no spaces; join wraps
    return p.replace("\\_", "_").replace("\\#", "#").replace("\\%", "%").replace("\\&", "&")


def _resolve_report(p: str, paper: str | None) -> str | None:
    """Resolve a cited .md report path to a repo-relative path that exists.
    Refs may be repo-root-relative (papers/SSV-I/results/x.md) or paper-relative
    (results/x.md, relative to papers/<PAPER>/). Returns None if it doesn't exist."""
    if (REPO_ROOT / p).is_file():
        return p
    if paper:
        rel = f"papers/{paper}/{p}"
        if (REPO_ROOT / rel).is_file():
            return rel
    return None


def extract_refs(tex: str, paper: str | None = None) -> tuple[list[int], list[str], list[str]]:
    """Return (issue numbers, instruments/*.py paths, result-note report paths)
    cited, each sorted and de-duplicated. Issues match both `\\#NN` and the
    cross-ref macro `\\ssvissue{NN}`. Report paths are repo-relative and resolved."""
    issues = sorted({int(n) for n in ISSUE_RE.findall(tex)}
                    | {int(n) for n in SSVISSUE_RE.findall(tex)})
    code, reports = set(), set()
    for raw in TEXTTT_RE.findall(tex):
        p = _normalise_path(raw)
        if p.startswith("instruments/") and p.endswith(".py"):
            code.add(p)
        elif p.endswith(".md"):
            rp = _resolve_report(p, paper)
            if rp:
                reports.add(rp)
    return issues, sorted(code), sorted(reports)


def missing_code_paths(paths: list[str]) -> list[str]:
    """Cited script paths that do not exist as tracked files in the repo."""
    return [p for p in paths if not (REPO_ROOT / p).is_file()]


def unresolved_issues(issues: list[int], slug: str) -> list[int]:
    """Issue numbers that do not resolve on GitHub (needs network + gh CLI).

    Used only by --verify-issues; offline runs skip this."""
    bad = []
    for n in issues:
        r = subprocess.run(["gh", "api", f"repos/{slug}/issues/{n}", "--jq", ".number"],
                           capture_output=True, text=True)
        if r.returncode != 0 or not r.stdout.strip():
            bad.append(n)
    return bad


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------

def _tex_path(path: str) -> str:
    """LaTeX-safe rendering of a path inside \\texttt (escape underscores)."""
    return path.replace("_", r"\_")


def _pinned_item(repo_relpath: str, base: str) -> list[str]:
    """An \\item for a file pinned to the commit that last modified it."""
    sha = last_commit(repo_relpath)
    if sha:
        return [f"  \\item \\texttt{{{_tex_path(repo_relpath)}}} @\\,\\texttt{{{sha}}} ---\\\\",
                f"        {{\\small\\url{{{base}/blob/{sha}/{repo_relpath}}}}}"]
    return [f"  \\item \\texttt{{{_tex_path(repo_relpath)}}} --- "
            r"\textbf{[untracked --- not found in the repository]}"]


def render(paper: str, issues: list[int], paths: list[str], reports: list[str],
           slug: str) -> str:
    base = f"https://github.com/{slug}"
    lines = [
        f"% Auto-generated by instruments/tools/gen_provenance.py — do not edit by hand.",
        f"% Regenerate: python instruments/tools/gen_provenance.py {paper}",
        r"\providecommand{\url}[1]{\texttt{#1}}% graceful fallback if hyperref absent",
        r"\section{Code and Issue References}",
        r"\label{app:provenance}",
        f"Each reference below is pinned so it can be checked directly against the "
        f"repository (\\url{{{base}}}): issues link to their tracker entry, and each "
        r"script or report links to the exact version --- the commit that last"
        r" modified it. Issue numbers in the text hyperlink to this list.",
        "",
    ]

    if issues:
        lines += [r"\paragraph{Issues.}", r"\begin{itemize}\setlength\itemsep{1pt}"]
        for n in issues:
            # \label{issue:N} is the target of the in-text \ssvissue{N} hyperlinks
            lines.append(f"  \\item\\label{{issue:{n}}} \\#{n} --- \\url{{{base}/issues/{n}}}")
        lines += [r"\end{itemize}", ""]

    if paths:
        lines += [
            r"\paragraph{Code (each pinned to the commit that last modified it).}",
            r"\begin{itemize}\setlength\itemsep{2pt}",
        ]
        for p in paths:
            lines += _pinned_item(p, base)
        lines += [r"\end{itemize}", ""]

    if reports:
        lines += [
            r"\paragraph{Reports (result notes, pinned to their last commit).}",
            r"\begin{itemize}\setlength\itemsep{2pt}",
        ]
        for r in reports:
            lines += _pinned_item(r, base)
        lines += [r"\end{itemize}", ""]

    if not issues and not paths and not reports:
        lines.append("This paper makes no external code or issue references.")
        lines.append("")

    return "\n".join(lines)


# --------------------------------------------------------------------------
# Driver
# --------------------------------------------------------------------------

def generate(paper: str, slug: str, check: bool) -> dict:
    main_tex = PAPERS / paper / "main.tex"
    if not main_tex.is_file():
        raise FileNotFoundError(main_tex)
    issues, paths, reports = extract_refs(main_tex.read_text(encoding="utf-8"), paper)
    missing = missing_code_paths(paths)
    prov = PAPERS / paper / "provenance.tex"
    skipped = not issues and not paths and not reports
    if not check:
        if skipped:
            prov.unlink(missing_ok=True)     # no refs ⇒ no appendix, no stale file
        else:
            prov.write_text(render(paper, issues, paths, reports, slug), encoding="utf-8")
    return {"paper": paper, "issues": issues, "paths": paths, "reports": reports,
            "missing": missing, "skipped": skipped}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paper", nargs="?", help="paper dir name, e.g. SSV-I")
    ap.add_argument("--all", action="store_true", help="all papers/SSV-*/main.tex")
    ap.add_argument("--check", action="store_true",
                    help="report broken refs, write nothing (exit 1 if any missing)")
    ap.add_argument("--verify-issues", action="store_true",
                    help="also check each issue resolves on GitHub (needs gh + network)")
    args = ap.parse_args()

    if args.all:
        papers = sorted(p.parent.name for p in PAPERS.glob("SSV-*/main.tex"))
    elif args.paper:
        papers = [args.paper]
    else:
        ap.error("give a paper name or --all")

    slug = repo_slug()
    any_problem = False
    for paper in papers:
        r = generate(paper, slug, args.check)
        bad_issues = unresolved_issues(r["issues"], slug) if args.verify_issues else []
        if r["skipped"]:
            tag = "skip "
        elif args.check:
            tag = "CHECK"
        else:
            tag = "wrote"
        msg = (f"{tag} {paper}: {len(r['issues'])} issues, {len(r['paths'])} scripts, "
               f"{len(r['reports'])} reports")
        if r["missing"]:
            msg += f"  ⚠ MISSING scripts: {r['missing']}"
        if bad_issues:
            msg += f"  ⚠ UNRESOLVED issues: {bad_issues}"
        print(msg)
        any_problem |= bool(r["missing"]) or bool(bad_issues)
    if any_problem:
        print("\nERROR: some references are not checkable — fix them.")
        sys.exit(1)


if __name__ == "__main__":
    main()
