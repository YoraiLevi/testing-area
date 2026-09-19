# Scenario S4 typing-demo (creative): the omp TUI input box cannot be driven/quit headlessly,
# so per scenarios.md S4 this falls back to animating the sample prompt at a shell prompt
# (still exercises keystroke animation). The substitution is recorded in the result reason.
# The text is typed but never sent; Ctrl+C aborts the line, then the shell exits. Betamax
# derives the grid from pixels, so Width/Height/FontSize/Padding approximate the 100x24
# geometry from scenarios.md. The `Set Shell` line and `--output` path are supplied by the
# workflow.
Env PS1 "$ "
Set FontSize 20
Set Width 1320
Set Height 640
Set Padding 24
Set TypingSpeed 120ms
Hide
Type "clear"
Enter
Sleep 400ms
Show
Sleep 500ms
Type "explain what this repository does"
Sleep 2s
Ctrl+C
Sleep 300ms
Type "exit"
Enter
Sleep 500ms
