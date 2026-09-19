# Scenario S1 launch-exit (minimal): show a prompt, run `omp --version`, pause so the
# version line is legible, then exit the shell cleanly. Betamax has no Cols/Rows settings
# (grid is derived from pixels), so Width/Height/FontSize/Padding approximate the 100x24
# geometry from scenarios.md. The `Set Shell` line and the `--output` path are supplied by
# the workflow (`betamax run <tape> --output out/<cell>-<scenario>.gif`).
Env PS1 "$ "
Set FontSize 20
Set Width 1320
Set Height 640
Set Padding 24
Set TypingSpeed 80ms
Hide
Type "clear"
Enter
Sleep 400ms
Show
Sleep 500ms
Type "omp --version"
Sleep 500ms
Enter
Sleep 2s
Type "exit"
Enter
Sleep 500ms
