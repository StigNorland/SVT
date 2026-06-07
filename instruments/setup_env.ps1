<#
  Set up the SSV Python environment on Windows (PowerShell).
    Usage:  powershell -ExecutionPolicy Bypass -File instruments\setup_env.ps1
  Creates a virtual environment at <repo>\.venv and installs the dependencies.
#>
$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

$Py = if ($env:PYTHON) { $env:PYTHON } else { "python" }
Write-Host "Using interpreter: $(& $Py --version) ($Py)"

& $Py -m venv .venv
& .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r instruments\requirements.txt

Write-Host ""
Write-Host "Done. To use this environment:"
Write-Host "    .\.venv\Scripts\Activate.ps1"
Write-Host "    pytest instruments\test          # run the test suite"
Write-Host "    python instruments\paper_i\trefoil_ny_derivation.py   # run a script"
