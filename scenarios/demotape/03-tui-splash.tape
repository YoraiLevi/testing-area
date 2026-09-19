# S3 tui-splash — launch the omp TUI, let the splash / onboarding screen render,
# then quit. Demo Tape drives a real PTY through ttyd, so Ctrl+C delivers a true
# SIGINT to the foreground TUI. The workflow additionally guards this scenario
# with a background SIGINT -> SIGTERM -> SIGKILL watchdog in case omp cannot be
# quit by keystroke headlessly.
Sleep 1
Type "omp"
Enter
Sleep 4
Ctrl+C
Sleep 1
Ctrl+C
Sleep 2
