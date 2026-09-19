#!/usr/bin/env bash
# Render the four omp scenarios with console2svg into out/<os>-<shell>-<scenario>.gif.
# console2svg is CLI-driven: `capture -- <cmd>` runs <cmd> in its own PTY, captures the
# terminal animation, and writes the requested format (GIF here) via its bundled
# resvg + ffmpeg pipeline (native output is SVG; the .gif extension triggers conversion).
#
# Usage: render.sh <cell_os> <shell>
set -u

# actions/setup-python exports LD_LIBRARY_PATH to its own libdir, which breaks the
# native libraries console2svg's capture + ffmpeg conversion load; clear it here.
unset LD_LIBRARY_PATH

CELL_OS="${1:?cell_os required}"
SHELL_LABEL="${2:?shell required}"
W=100
H=24

mkdir -p out

echo "console2svg: $(command -v console2svg || echo MISSING)"
console2svg --version 2>/dev/null || true
echo "ffmpeg: $(command -v ffmpeg || echo MISSING)"
echo "omp: $(command -v omp || echo MISSING)"

run() {
  echo "== rendering: console2svg $* =="
  console2svg "$@"
  echo "  exit=$? for: console2svg $*"
}

le="${CELL_OS}-${SHELL_LABEL}-launch-exit"
ht="${CELL_OS}-${SHELL_LABEL}-help-tour"
ts="${CELL_OS}-${SHELL_LABEL}-tui-splash"
td="${CELL_OS}-${SHELL_LABEL}-typing-demo"

# S1 launch-exit: run omp --version, let it exit cleanly, hold the last frame.
run capture -v -c -d macos -w "$W" -h "$H" --sleep 1 \
  -o "out/${le}.gif" -- omp --version || true

# S2 help-tour: colored, long output from omp --help.
run capture -v -c -d macos -w "$W" -h "$H" --sleep 1 \
  -o "out/${ht}.gif" -- omp --help || true

# S3 tui-splash: launch the omp TUI headlessly; it never self-exits, so --timeout
# stops the capture after the splash/onboarding screen has rendered.
run capture -v -d macos -w "$W" -h "$H" --timeout 6 --sleep 0.5 \
  -o "out/${ts}.gif" -- omp --no-session || true

# S4 typing-demo: console2svg cannot inject keystrokes into an already-running TUI
# headlessly, so per scenarios.md we fall back to keystroke animation at a shell
# prompt: `-c` animates the sample prompt being typed as a command line.
run capture -v -c -d macos -w "$W" -h "$H" --sleep 1.5 \
  -o "out/${td}.gif" -- echo "explain what this repository does" || true

echo "=== gifs (path size) ==="
find out -type f -name '*.gif' -printf '%p %s\n' 2>/dev/null || find out -type f -name '*.gif'
echo "=== out ==="; ls -la out || true
