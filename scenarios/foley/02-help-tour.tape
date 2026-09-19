# Scenario S2 help-tour (creative): run `omp --help` (long, colorized) and pause so the
# colored help renders, then exit. Exercises color + scrollback fidelity. Deterministic
# mode. Header (Output + Set Shell) injected by the workflow.
Set FontSize 16
Set Width 1200
Set Height 720
Set Padding 20
Set TypingSpeed 60ms
Hide
Type "clear" Enter
Show
Sleep 500ms
Type "omp --help"
Sleep 400ms
Enter
Sleep 3500ms
Type "exit"
Enter
Sleep 500ms
