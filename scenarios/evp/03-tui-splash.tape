# Scenario S3 tui-splash (creative): launch the omp TUI, let the splash / onboarding
# screen render, then quit. The omp TUI does not exit on headless quit keystrokes, so the
# workflow runs a background SIGINT->SIGTERM->SIGKILL watchdog that ends the omp process
# after the splash is captured. Once omp exits, control returns to the shell and the
# `exit` below closes the EVP session so the streamed GIF/SVG is finalized. Output paths
# are supplied by the workflow via `evp --output`.
Set Shell bash --norc
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
Type "omp --no-session"
Sleep 500ms
Enter
Sleep 8s
Type "exit"
Enter
Sleep 500ms
