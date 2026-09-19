# Scenario S4 typing-demo (creative): launch the omp TUI and type a sample prompt into the
# input box WITHOUT sending it (no Enter), pause so the typed text is visible, then end the
# take. foley presses keys on a real pty, so it types straight into the omp TUI input (no
# shell-prompt fallback needed). foley v0.1.0's vtengine cannot encode Ctrl+<letter> chords,
# so no Ctrl+C quit is sent; foley finalizes the take when the tape ends. Realtime mode
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
Sleep 2500ms
