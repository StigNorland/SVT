"""Pytest path setup for the instruments tree.

Test modules live under instruments/test/<paper>/ but import the scripts they
exercise either by bare module name (e.g. `import cp1_safety_checks`) or by
package path (e.g. `from paper_viii.relaxing_rho0_cosmology import ...`). This
conftest puts every instrument module directory — and the instruments root
itself — on sys.path so those imports resolve regardless of test location.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
_dirs = [ROOT] + list(ROOT.glob("paper_*")) + [ROOT / "shared_numerics", ROOT / "tools"]
for d in _dirs:
    if d.is_dir() and str(d) not in sys.path:
        sys.path.insert(0, str(d))
