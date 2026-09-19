# Scenario S3 tui-splash (creative): launch the omp TUI, let the splash/onboarding screen
# render, then end the take. foley presses keys on a real pty, so it launches the TUI
# directly (`omp --no-session`). foley v0.1.0's vtengine cannot encode Ctrl+<letter> chords
# ("empty encoding for {Rune:99 Mods:2}"), so no interactive Ctrl+C quit is sent and no
# `exit` is typed (omp is the foreground process, not the shell); foley finalizes the take
# when the tape ends. Rendered in realtime mode (`-mode realtime`, set by the workflow)
# because a continuously drawing TUI can record blank under the virtual clock (foley.md
# "Two clocks"). Header (Output + Set Shell) injected by the workflow.
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
Sleep 5s
