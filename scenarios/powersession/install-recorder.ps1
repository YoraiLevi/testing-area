# Install the pinned PowerSession-rs recorder (v0.1.16) and agg converter
# (v1.9.0) as prebuilt Windows x64 binaries into %USERPROFILE%\bin and expose
# them on PATH for later steps. Using the release binaries avoids a slow
# from-source `cargo install` build on the runner.
$ErrorActionPreference = "Stop"

$bin = "$env:USERPROFILE\bin"
New-Item -ItemType Directory -Force -Path $bin | Out-Null

Write-Host "::group::install PowerSession v0.1.16 (win-x64)"
Invoke-WebRequest -Uri "https://github.com/Watfaq/PowerSession-rs/releases/download/v0.1.16/PowerSession.exe" -OutFile "$bin\PowerSession.exe"
Write-Host "::endgroup::"

Write-Host "::group::install agg v1.9.0 (win-x64)"
Invoke-WebRequest -Uri "https://github.com/asciinema/agg/releases/download/v1.9.0/agg-x86_64-pc-windows-msvc.exe" -OutFile "$bin\agg.exe"
Write-Host "::endgroup::"

Add-Content -Path $env:GITHUB_PATH -Value $bin
$env:PATH = "$bin;$env:PATH"

& "$bin\PowerSession.exe" -V
& "$bin\agg.exe" --version
