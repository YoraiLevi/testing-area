#!/usr/bin/env sh
# S4 typing-demo (creative): asciinema cannot inject keystrokes into the omp TUI input box
# headlessly, so per scenarios.md this falls back to animating the sample prompt at a shell
# prompt (still exercises keystroke animation). The substitution is recorded in the result
# reason.
set -u
text='explain what this repository does'
printf '%s' '$ '
sleep 1
i=1
len=$(printf '%s' "$text" | wc -c)
while [ "$i" -le "$len" ]; do
  printf '%s' "$(printf '%s' "$text" | cut -c "$i")"
  sleep 0.12
  i=$((i + 1))
done
sleep 2
printf '\n'
