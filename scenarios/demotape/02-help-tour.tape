# S2 help-tour — exercise color + long/scrolling output fidelity via omp --help.
# The @4s modifier holds after Enter so the colored help has time to render.
Sleep 1
Run@4s "omp --help"
Sleep 2
Type "exit"
Enter
Sleep 1
