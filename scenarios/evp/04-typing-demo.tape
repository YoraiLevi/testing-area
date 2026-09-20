# Scenario S4 typing-demo (creative): the omp TUI input box cannot be driven/quit
# headlessly, so per scenarios.md S4 this falls back to animating the sample prompt at a
# shell prompt (still exercises keystroke animation). The substitution is recorded in the
# result reason. The text is typed but never sent; Ctrl+C aborts the line, then the shell
# exits. Output paths are supplied by the workflow via `evp --output`.
Env PS1 "$ "
Set Cols 100
Set Rows 24
Set FontSize 16
Set Padding 20
Set TypingSpeed 120ms
Hide
Type "clear"
Enter
Show
Sleep 500ms
Type "explain what this repository does"
Sleep 2s
Ctrl+C
Sleep 300ms
Type "exit"
Enter
Sleep 500ms
