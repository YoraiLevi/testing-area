# S1 launch-exit: run omp --version, pause so the version line is legible, exit.
# Handed to PowerSession via `--command "pwsh.exe -File ..."`; when this script
# returns, the ConPTY child exits and PowerSession finishes recording.
omp --version
Start-Sleep -Seconds 2
