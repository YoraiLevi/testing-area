# Scenario S1 launch-exit (minimal, REQUIRED): show a prompt, run `omp --version`,
# pause so the version line is legible, then exit the shell cleanly. Rendered by foley
# in deterministic mode (byte-identical takes). The header (Output + Set Shell) is
# injected by the workflow. foley uses the vendored VHS `.tape` grammar, so this body
# is identical to its VHS counterpart.
Set FontSize 20
Set Width 1200
Set Height 600
Set Padding 20
Set TypingSpeed 80ms
Hide
Type "clear" Enter
Show
Sleep 500ms
Type "omp --version"
Sleep 500ms
Enter
Sleep 2s
Type "exit"
Enter
Sleep 500ms
