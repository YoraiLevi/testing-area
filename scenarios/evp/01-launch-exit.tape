# Scenario S1 launch-exit (minimal): show a prompt, run `omp --version`, pause so the
# version line is legible, then exit the shell cleanly. Output paths are supplied by the
# workflow via `evp --output`. EVP uses a superset of the VHS .tape language.
Env PS1 "$ "
Set Cols 100
Set Rows 24
Set FontSize 20
Set Padding 20
Set TypingSpeed 80ms
Hide
Type "clear"
Enter
Show
Sleep 500ms
Type "omp --version"
Sleep 500ms
Enter
Sleep 2s
Type "exit"
Enter
Sleep 500ms
