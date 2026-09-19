# S1 launch-exit — capture a real omp launch that starts and cleanly exits.
# omp is on PATH (installed by scenarios/shared/install-omp.sh); the shell,
# geometry, typing speed and output path are supplied by the workflow via CLI
# flags, so this file stays scenario-only and shell-agnostic.
Sleep 1
Run "omp --version"
Sleep 2
Type "exit"
Enter
Sleep 1
