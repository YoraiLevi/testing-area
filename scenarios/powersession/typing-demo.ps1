# S4 typing-demo: scenarios.md shell-prompt fallback. PowerSession cannot inject
# keystrokes into a detached new console, so the sample prompt is "typed" here
# char-by-char (visible progressive rendering) and the script exits, ending the
# recording. Handed to PowerSession via `--command "pwsh.exe -File ..."`.
$prompt = 'explain what this repository does'
Write-Host -NoNewline 'PS> '
foreach ($ch in $prompt.ToCharArray()) {
    Write-Host -NoNewline $ch
    Start-Sleep -Milliseconds 55
}
Write-Host ''
Start-Sleep -Seconds 1
