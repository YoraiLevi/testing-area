# Install Oh My Pi (omp) on a Windows CI runner and expose it on PATH.
# Robust against omp.sh rate limits: retry the official installer, then fall back to
# the Bun registry package (which provides the `omp` binary).
$ErrorActionPreference = "Stop"

function Add-OmpPaths {
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
}

function Install-ViaOfficial {
  for ($i = 1; $i -le 5; $i++) {
    Write-Host "omp: official installer attempt $i"
    try { Invoke-RestMethod https://omp.sh/install.ps1 | Invoke-Expression; return $true }
    catch { Start-Sleep -Seconds ($i * 5) }
  }
  return $false
}

function Install-ViaBun {
  Write-Host "omp: falling back to Bun registry install"
  if (-not (Get-Command bun -ErrorAction SilentlyContinue)) {
    Invoke-RestMethod https://bun.sh/install.ps1 | Invoke-Expression
    $env:PATH = "$env:USERPROFILE\.bun\bin;$env:PATH"
  }
  for ($i = 1; $i -le 3; $i++) {
    try { bun install -g '@oh-my-pi/pi-coding-agent'; return $true }
    catch { Start-Sleep -Seconds ($i * 5) }
  }
  return $false
}

Write-Host "::group::install omp"
if (-not (Install-ViaOfficial)) { if (-not (Install-ViaBun)) { throw "omp install failed" } }
Write-Host "::endgroup::"

Add-OmpPaths
Get-Command omp
omp --version
