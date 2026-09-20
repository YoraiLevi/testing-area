# Scenario S2 help-tour (creative): run `omp --help`, pause to let the long, colored help
# render (exercises color and scrollback fidelity), then exit. Output paths are supplied
# by the workflow via `evp --output`.
Env PS1 "$ "
Set Cols 100
Set Rows 24
Set FontSize 16
Set Padding 20
Set TypingSpeed 80ms
Hide
Type "clear"
Enter
Show
Sleep 500ms
Type "omp --help"
Sleep 500ms
Enter
Sleep 3s
Type "exit"
Enter
Sleep 500ms
