#!/usr/bin/env bash
# Animate a command being typed at a prompt, run it, then hold the final screen.
#
# console2svg records terminal *changes* over time. A fast, non-interactive command
# (omp --version / --help) flushes its output and exits before console2svg's capture
# loop samples a populated screen, so on Linux the capture collapses to a single empty
# frame ("$ <cmd>" with no output at all). Typing the command out with per-key sleeps
# and then holding the result gives console2svg genuine time-varying, populated content,
# so every platform produces a real multi-frame animation that shows the command output.
#
# Usage: typed-run.sh <command> [args...]
set -u

CPS="${TYPED_CPS:-0.04}"   # seconds per character while "typing"
HOLD="${TYPED_HOLD:-1.0}"  # seconds to hold the final screen after the command finishes

cmd="$*"
printf '$ '
for (( i = 0; i < ${#cmd}; i++ )); do
  printf '%s' "${cmd:i:1}"
  sleep "$CPS"
done
printf '\n'
eval "$cmd"
sleep "$HOLD"
