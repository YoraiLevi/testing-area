# Scenario S2 help-tour (creative): run `omp --help`, pause to let the long, colored help
# render (exercises color and scrollback fidelity), then exit. Betamax derives the terminal
# grid from pixels, so Width/Height/FontSize/Padding approximate the 100x24 geometry from
# scenarios.md. The `Set Shell` line and `--output` path are supplied by the workflow.
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
Type "omp --help"
Sleep 500ms
Enter
Sleep 3s
Type "exit"
Enter
Sleep 500ms
