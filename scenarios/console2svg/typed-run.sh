#!/usr/bin/env bash
# Animate a command being typed at a prompt, run it, replay its output gradually,
# then hold the final screen with a blinking cursor.
#
# console2svg's video mode records the terminal *as it changes over time*. On Linux a
# fast, non-interactive command (omp --version / --help, echo) writes all of its output
# in a single instant burst and then exits, and that burst is dropped: the capture is an
# empty terminal (verified on Ubuntu with console2svg 0.9.3). Three things fix it:
#   1. Type the command out with per-key sleeps so the prompt line is recorded.
#   2. Capture the command output, then re-emit it one line at a time with a small delay
#      so it renders progressively and console2svg records it (a burst is not recorded,
#      gradual output is). FORCE_COLOR is set by console2svg, so ANSI colour survives.
#   3. Hold the final screen with a blinking block cursor. A screen that goes fully
#      static right after the output is dropped, so the blink keeps it changing (and
#      being sampled) while the output stays visible above it.
#
# Usage: typed-run.sh <command> [args...]
set -u

CPS="${TYPED_CPS:-0.04}"     # seconds per character while "typing" the command
LPS="${TYPED_LPS:-0.10}"     # seconds between output lines while replaying the result
BLINKS="${TYPED_BLINKS:-4}"  # blink cycles holding the final screen (each ~0.3s)
MAX="${TYPED_MAXLINES:-20}"  # cap replayed output lines (a screen is ~24 rows)

cmd="$*"
printf '$ '
for (( i = 0; i < ${#cmd}; i++ )); do
  printf '%s' "${cmd:i:1}"
  sleep "$CPS"
done
printf '\n'

out="$(eval "$cmd" 2>&1)"
if [ -n "$out" ]; then
  n=0
  while IFS= read -r line; do
    printf '%s\n' "$line"
    sleep "$LPS"
    n=$(( n + 1 ))
    if [ "$n" -ge "$MAX" ]; then
      printf '\033[2m...\033[0m\n'   # elide the rest of long output
      break
    fi
  done <<< "$out"
fi

for (( b = 0; b < BLINKS; b++ )); do
  printf '\033[7m \033[0m'   # inverse-video block: a visible cursor
  sleep 0.15
  printf '\b \b'             # erase it
  sleep 0.15
done
