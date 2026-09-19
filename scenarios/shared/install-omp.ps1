# Install Oh My Pi (omp) on a Windows CI runner and expose it on PATH.
$ErrorActionPreference = "Stop"

Write-Host "::group::install omp"
Invoke-RestMethod https://omp.sh/install.ps1 | Invoke-Expression
Write-Host "::endgroup::"

# Add likely install locations to PATH for subsequent steps.
$dirs = @(
  "$env:LOCALAPPDATA\omp",
  "$env:USERPROFILE\.bun\bin",
  "$env:USERPROFILE\.omp\bin"
)
foreach ($d in $dirs) {
  if (Test-Path $d) {
    Add-Content -Path $env:GITHUB_PATH -Value $d
    $env:PATH = "$d;$env:PATH"
  }
}

# Fail loudly if omp is not runnable.
Get-Command omp
omp --version
