#!/usr/bin/env sh
# S3 tui-splash (creative): launch the omp TUI, let the splash/onboarding screen render,
# then quit. asciinema's `rec -c` runs a single command to completion and cannot inject a
# quit keystroke into an interactive TUI headlessly, so a background watchdog escalates
# SIGINT -> SIGTERM -> SIGKILL to end the session. If no valid GIF results the cell is
# recorded `broken` with a reason (scenarios.md / Principle III).
set -u
printf '%s\n' '$ omp --no-session'
omp --no-session &
omppid=$!
(
  sleep 5
  kill -INT "$omppid" 2>/dev/null || true
  sleep 2
  kill -TERM "$omppid" 2>/dev/null || true
  sleep 2
  kill -KILL "$omppid" 2>/dev/null || true
) &
watchdog=$!
wait "$omppid" 2>/dev/null || true
kill "$watchdog" 2>/dev/null || true
sleep 1
