# `instruments/` — computational scripts for the SSV programme

This directory holds the numerical and symbolic "instruments" behind the
Saturated Superfluid Vacuum (SSV) papers: the scripts that derive, verify, or
falsify the claims made in `papers/`. Every result note in `papers/*/results/`
and every `\texttt{instruments/...}` reference in a paper points back here, and
each such reference is pinned to an exact version in that paper's *Code and
Issue References* appendix (see "Provenance" below).

## Layout

```
instruments/
  paper_i/  paper_ii/  paper_iv/  paper_v/        scripts grouped by paper
  paper_vi_a/  paper_vi_b/  paper_vii_b/  paper_viii/
  shared_numerics/        helpers shared across papers
  tools/                  repo tooling (e.g. gen_provenance.py)
  _fitted_quarantine/     retired scripts that used fitted/calibrated inputs;
                          kept for the record, NOT to be trusted as derivations
  test/<paper>/           the test suite, mirroring the code layout
                          e.g. test/paper_i/test_cp1_safety_checks.py
  conftest.py             puts the module dirs on sys.path for the tests
  requirements.txt        Python dependencies
  setup_env.sh / .ps1     one-shot environment setup (see below)
```

Scripts import their siblings by bare module name (e.g. `import vortex_profile`),
which works because each script's own directory is on the path when it runs, and
`conftest.py` adds the module directories when the tests run.

## Environment setup

Requires **Python 3.12** (3.10–3.12 should all work). Dependencies: numpy,
scipy, sympy, numba, matplotlib, pytest (see `requirements.txt`).

**Linux / macOS**
```bash
bash instruments/setup_env.sh
source .venv/bin/activate
```

**Windows (PowerShell)**
```powershell
powershell -ExecutionPolicy Bypass -File instruments\setup_env.ps1
.\.venv\Scripts\Activate.ps1
```

Both create a virtual environment at `<repo>/.venv` and install the pinned
dependencies. (Set the `PYTHON` env var to choose a specific interpreter.)

## Running things

```bash
pytest instruments/test                     # whole suite
pytest instruments/test/paper_i             # one paper's tests
python instruments/paper_i/trefoil_ny_derivation.py   # run a script directly
```

Most scripts print a self-contained report when run directly; the heavy 3D
solvers take CLI arguments (run with `--help`).

## Provenance (keeping the papers checkable)

`tools/gen_provenance.py` scans a paper's `main.tex` for GitHub references —
issues (`\#NN`), scripts (`\texttt{instruments/...py}`) and result-note reports
— and writes `papers/<PAPER>/provenance.tex`, the *Code and Issue References*
appendix. Each script/report is pinned to a GitHub permalink at the commit that
last modified it, so a citation always resolves to the exact version used.

```bash
python instruments/tools/gen_provenance.py --all         # regenerate every paper
python instruments/tools/gen_provenance.py --check --all # CI: fail on broken refs
```

Regenerate before building a paper. The test
`test/tools/test_gen_provenance.py` enforces that every cited path exists, so a
reference can never silently break.
