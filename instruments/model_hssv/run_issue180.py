"""Run every executable issue-180 control and write the combined receipt."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import relativistic_logse_bridge
import shared_eft_audit
import ssv_target_audit

ROOT = Path(__file__).resolve().parents[2]
RECEIPT = ROOT / "papers" / "H-SSV" / "results" / "issue-180" / "receipt.json"


def run_all() -> dict[str, Any]:
    target = ssv_target_audit.run()
    bridge = relativistic_logse_bridge.run()
    shared = shared_eft_audit.run()
    return {
        "issue": 180,
        "status": "closure-grade",
        "decision": "K3",
        "decision_scope": (
            "H-SSV as specified: stable covariant EFT with the literal "
            "Paper-I SSV condensate limit"
        ),
        "gates": {
            "P0": "FAIL -- literal homogeneous SSV background is modulationally unstable",
            "P1": "FAIL -- exact minimal covariant parent is unbounded below",
            "P2": "PASS FORMALLY -- the parent maps to the target with a controlled remainder",
            "P3": "FAIL -- covariant Goldstone branch has omega^2<0 at small k",
            "P4_S_route": "FAIL -- one scalar Goldstone is not two photon helicities",
            "P4_H_route": (
                "CONTROL ONLY -- independent Maxwell works after withdrawing "
                "the SSV-photon identity, but does not repair P0/P3"
            ),
            "P5": "NOT REACHED for literal SSV because upstream stability gates fail",
            "P6": "COMPLETE -- no-go ledger recorded in 05-no-go-audit.md",
        },
        "instruments": {
            "target": target,
            "relativistic_bridge": bridge,
            "shared_eft_control": shared,
        },
        "adjacent_model": {
            "classification": "K2 candidate outside the frozen target",
            "changes_required": [
                "reverse or otherwise change the logarithmic curvature at the background",
                "supply Maxwell and Einstein fields independently",
                "withdraw the scalar-Goldstone photon identification",
            ],
            "why_not_issue_180_success": (
                "these changes alter the SSV limit and still leave the "
                "Goldstone cone subluminal in the controlled NR regime"
            ),
        },
    }


def main() -> None:
    report = run_all()
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"Wrote {RECEIPT}")


if __name__ == "__main__":
    main()
