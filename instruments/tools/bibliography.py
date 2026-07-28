"""Validate the shared SSV BibTeX database and per-paper citation wiring."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPERS = ROOT / "papers"
DATABASE = PAPERS / "cited" / "references.bib"
VERIFICATION = PAPERS / "cited" / "verification.json"

CITE_RE = re.compile(
    r"\\(?:cite|citep|citet|citealp|citeauthor|citeyear)\s*"
    r"(?:\[[^]]*\]\s*){0,2}\{([^}]*)\}"
)
BIB_KEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)
SHARED_DIRECTIVE_RE = re.compile(
    r"\\bibliography\s*\{\s*\.\./cited/references\s*\}"
)
STYLE_RE = re.compile(r"\\bibliographystyle\s*\{\s*unsrt\s*\}")

# These spellings represented duplicate works in the old inline bibliographies.
# Keeping them forbidden prevents aliases from quietly returning.
LEGACY_ALIASES = {
    "TGD-I", "ssv1", "ssv2", "ssv3", "ssv4", "ssv8", "ssvG",
    "SSV-VIIa", "SSV-VIIb",
    "Volovik", "Volovik2003", "Barcelo", "Zloshchastiev2020",
    "BialynickiBirula1976", "Villois", "Gross", "Pitaevskii",
    "GW170817_MMA",
}


def _without_comments(text: str) -> str:
    lines = []
    for line in text.splitlines():
        lines.append(re.split(r"(?<!\\)%", line, maxsplit=1)[0])
    return "\n".join(lines)


def citation_keys(path: Path) -> set[str]:
    text = _without_comments(path.read_text(encoding="utf-8"))
    keys: set[str] = set()
    for match in CITE_RE.finditer(text):
        keys.update(key.strip() for key in match.group(1).split(",") if key.strip())
    return keys


def database_key_list(path: Path = DATABASE) -> list[str]:
    return BIB_KEY_RE.findall(_without_comments(path.read_text(encoding="utf-8")))


def database_keys(path: Path = DATABASE) -> set[str]:
    return set(database_key_list(path))


def shared_issues(
    database: Path = DATABASE,
    verification: Path = VERIFICATION,
) -> list[str]:
    """Defects in the series-wide database, independent of one paper."""
    issues: list[str] = []
    if not database.is_file():
        return [f"missing shared bibliography: {database}"]
    keys = database_key_list(database)
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    if duplicates:
        issues.append(f"duplicate BibTeX keys: {duplicates}")
    aliases = sorted(set(keys) & LEGACY_ALIASES)
    if aliases:
        issues.append(f"legacy alias keys in shared bibliography: {aliases}")

    if verification.is_file():
        registry = json.loads(
            verification.read_text(encoding="utf-8")
        ).get("sources", {})
        missing = sorted(set(registry) - set(keys))
        if missing:
            issues.append(
                f"quote-registry sources absent from references.bib: {missing}")
    else:
        issues.append(f"missing quote registry: {verification}")
    return issues


def issues_for(
    paper: str,
    papers: Path = PAPERS,
    database: Path = DATABASE,
    verification: Path = VERIFICATION,
) -> list[str]:
    """Defects in one paper's use of the shared bibliography."""
    issues = shared_issues(database, verification)
    main = papers / paper / "main.tex"
    if not main.is_file():
        return issues + [f"{paper}: missing main.tex"]
    text = _without_comments(main.read_text(encoding="utf-8"))
    if "\\bibitem" in text or "\\begin{thebibliography}" in text:
        issues.append(f"{paper}: inline bibliography is forbidden")
    if len(SHARED_DIRECTIVE_RE.findall(text)) != 1:
        issues.append(
            f"{paper}: must contain one "
            r"\bibliography{../cited/references}")
    if len(STYLE_RE.findall(text)) != 1:
        issues.append(f"{paper}: must use bibliography style unsrt")

    cited = citation_keys(main)
    aliases = sorted(cited & LEGACY_ALIASES)
    if aliases:
        issues.append(f"{paper}: citations use legacy alias keys: {aliases}")
    if database.is_file():
        missing = sorted(cited - database_keys(database))
        if missing:
            issues.append(f"{paper}: undefined shared citation keys: {missing}")
    return issues


def report(paper: str) -> str:
    issues = issues_for(paper)
    cited = citation_keys(PAPERS / paper / "main.tex")
    lines = [
        f"{paper}: {len(cited)} cited keys, "
        f"{len(database_keys())} shared entries",
        f"{len(issues)} bibliography issue(s)",
    ]
    lines.extend(f"  FAIL {issue}" for issue in issues)
    return "\n".join(lines)


if __name__ == "__main__":  # pragma: no cover
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paper")
    args = parser.parse_args()
    print(report(args.paper))
    raise SystemExit(1 if issues_for(args.paper) else 0)
