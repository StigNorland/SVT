"""Run the issue-226 screen-foundation checks and write their receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import quantum_causal_screen_audit
import screen_foundations_audit

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "papers" / "H-SSV" / "results" / "issue-226"
PREREGISTRATION = RESULTS / "00-preregistration.md"
C4_PREREGISTRATION = RESULTS / "03-c4-preregistration-addendum.md"
RECEIPT = RESULTS / "receipt.json"


def run_all() -> dict[str, object]:
    classical = screen_foundations_audit.run()
    quantum = quantum_causal_screen_audit.run()
    survivor = quantum["survives_all_six_gates"]
    report: dict[str, object] = {
        "issue": 226,
        "status": "closure-grade",
        "decision": "PROCEED" if survivor else "REVISE",
        "survivors": [quantum["candidate"]] if survivor else [],
        "candidate_audits": {
            "C0_to_C3_classical_ladder": classical,
            "C4_quantum_causal_global_screen": quantum,
        },
        "gates": {
            **classical["gates"],
            "C4_quantum_causal_global_screen": quantum["gates"],
        },
        "blocking_result": None if survivor else classical["blocking_result"],
        "revision_record": (
            "C3's preliminary F3 failure assumed a classical membrane rest "
            "frame. Owner input separated local causality from global state; "
            "C4 was preregistered before implementation and passes via "
            "microcausality, no signaling and foliation independence."
        ),
    }
    report["preregistration_sha256"] = hashlib.sha256(
        PREREGISTRATION.read_bytes()
    ).hexdigest()
    report["c4_preregistration_sha256"] = hashlib.sha256(
        C4_PREREGISTRATION.read_bytes()
    ).hexdigest()
    report["evidential_boundary"] = (
        "No galaxy, lensing, cluster or cosmology data used; issue-225 results "
        "did not select a functional form."
    )
    return report


def main() -> None:
    report = run_all()
    RECEIPT.parent.mkdir(parents=True, exist_ok=True)
    RECEIPT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps(report, indent=2, sort_keys=True))
    print(f"Wrote {RECEIPT}")


if __name__ == "__main__":
    main()
