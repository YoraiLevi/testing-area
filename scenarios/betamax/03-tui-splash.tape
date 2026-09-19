# Scenario S3 tui-splash (creative): launch the omp TUI, let the splash / onboarding screen
# render, then quit. The omp TUI does not exit on headless quit keystrokes, so the workflow
# runs a background SIGINT->SIGTERM->SIGKILL watchdog that ends the omp process after the
# splash is captured. Once omp exits, control returns to the shell and the `exit` below
# closes the session so Betamax finalizes the GIF. Betamax derives the grid from pixels, so
# Width/Height/FontSize/Padding approximate the 100x24 geometry from scenarios.md. The
# `Set Shell` line and `--output` path are supplied by the workflow.
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
Type "omp --no-session"
Sleep 500ms
Enter
Sleep 8s
Type "exit"
Enter
Sleep 500ms
