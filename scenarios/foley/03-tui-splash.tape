# Scenario S3 tui-splash (creative): launch the omp TUI, let the splash/onboarding screen
# render, then quit. foley presses keys on a real pty, so it drives and quits the TUI
# directly: launch `omp --no-session`, hold the splash, then Ctrl+C (twice) to quit and
# `exit` to close the shell. Rendered in realtime mode (`-mode realtime`, set by the
# workflow) because a continuously drawing TUI can record blank under the virtual clock.
# Header (Output + Set Shell) injected by the workflow.
Set FontSize 16
Set Width 1200
Set Height 720
Set Padding 20
Set TypingSpeed 80ms
Hide
Type "clear" Enter
Show
Sleep 500ms
Type "omp --no-session"
Sleep 400ms
Enter
Sleep 4s
Ctrl+C
Sleep 800ms
Ctrl+C
Sleep 800ms
Type "exit"
Enter
Sleep 500ms
