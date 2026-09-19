# Scenario S4 typing-demo (creative): launch the omp TUI and type a sample prompt into the
# input box WITHOUT sending it, pause so the typed text is visible, then quit. foley presses
# keys on a real pty, so it types straight into the omp TUI input (no shell-prompt fallback
# needed), then Ctrl+C (twice) to quit and `exit` to close the shell. Realtime mode
# (`-mode realtime`, set by the workflow). Header (Output + Set Shell) injected by the workflow.
Set FontSize 16
Set Width 1200
Set Height 720
Set Padding 20
Set TypingSpeed 120ms
Hide
Type "clear" Enter
Show
Sleep 500ms
Type "omp --no-session"
Sleep 400ms
Enter
Sleep 3500ms
Type "explain what this repository does"
Sleep 2s
Ctrl+C
Sleep 800ms
Ctrl+C
Sleep 800ms
Type "exit"
Enter
Sleep 500ms
