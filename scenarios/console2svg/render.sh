#!/usr/bin/env bash
# Render the four omp scenarios with console2svg into out/<os>-<shell>-<scenario>.<ext>.
# console2svg is CLI-driven: `capture -- <cmd>` runs <cmd> in its own PTY, captures the
# terminal animation, and writes the requested format via its bundled resvg + ffmpeg
# pipeline (native output is SVG; the output extension selects the format). We run the
# capture once per format so each scenario emits svg, gif, mp4, and webm.
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

# console2svg picks the encoder from the -o extension, so we run each capture once per
# format (svg native; gif/mp4/webm via the bundled ffmpeg pipeline).
FORMATS="svg gif mp4 webm"

# S1 launch-exit: run omp --version, let it exit cleanly, hold the last frame.
for ext in $FORMATS; do
  run capture -v -c -d macos -w "$W" -h "$H" --sleep 1 \
    -o "out/${le}.${ext}" -- omp --version || true
done

# S2 help-tour: colored, long output from omp --help.
for ext in $FORMATS; do
  run capture -v -c -d macos -w "$W" -h "$H" --sleep 1 \
    -o "out/${ht}.${ext}" -- omp --help || true
done

# S3 tui-splash: launch the omp TUI headlessly; it never self-exits, so --timeout
# stops the capture after the splash/onboarding screen has rendered.
for ext in $FORMATS; do
  run capture -v -d macos -w "$W" -h "$H" --timeout 6 --sleep 0.5 \
    -o "out/${ts}.${ext}" -- omp --no-session || true
done

# S4 typing-demo: console2svg cannot inject keystrokes into an already-running TUI
# headlessly, so per scenarios.md we fall back to keystroke animation at a shell
# prompt: `-c` animates the sample prompt being typed as a command line.
for ext in $FORMATS; do
  run capture -v -c -d macos -w "$W" -h "$H" --sleep 1.5 \
    -o "out/${td}.${ext}" -- echo "explain what this repository does" || true
done

echo "=== gifs (path size) ==="
find out -type f -name '*.gif' -printf '%p %s\n' 2>/dev/null || find out -type f -name '*.gif'
echo "=== out ==="; ls -la out || true
