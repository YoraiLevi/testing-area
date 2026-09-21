#!/usr/bin/env bash
# Render the four omp scenarios with console2svg into out/<os>-<shell>-<scenario>.<ext>.
# console2svg is CLI-driven: `capture -- <cmd>` runs <cmd> in its own PTY, captures the
# terminal animation, and writes the requested format via its bundled resvg + ffmpeg
# pipeline (native output is SVG; the output extension selects the format). We run the
# capture once per format so each scenario emits svg, gif, mp4, and webm.
#
# S1/S2/S4 run their (fast, non-interactive) command through typed-run.sh, which types
# the command out and holds the result. Without it, console2svg's Linux capture of an
# instant command is a single empty frame (the command exits before capture samples the
# output); the typed animation makes the capture populated and genuinely multi-frame.
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
FPS=10                 # capture frame rate for the typed scenarios (keeps GIF size modest)
BG="#12141c"           # solid background: a gradient window frame bloats the GIF palette
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TYPED="$SCRIPT_DIR/typed-run.sh"

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

# S1 launch-exit: type `omp --version`, run it, hold. The typed animation keeps the PTY
# populated over time so the capture is a real animation showing the version output
# (a bare `omp --version` exits before capture and renders as one empty frame on Linux).
for ext in $FORMATS; do
  run capture -v -d macos --background "$BG" -w "$W" -h "$H" --fps "$FPS" \
    -o "out/${le}.${ext}" -- bash "$TYPED" omp --version || true
done

# S2 help-tour: same typed-run wrapper over `omp --help` (long, colored output).
for ext in $FORMATS; do
  run capture -v -d macos --background "$BG" -w "$W" -h "$H" --fps "$FPS" \
    -o "out/${ht}.${ext}" -- bash "$TYPED" omp --help || true
done

# S3 tui-splash: launch the omp TUI headlessly; it never self-exits, so --timeout
# stops the capture after the splash/onboarding screen has rendered. Already animated
# by the live TUI, so it keeps the plain capture (no typed-run wrapper).
for ext in $FORMATS; do
  run capture -v -d macos -w "$W" -h "$H" --timeout 6 --sleep 0.5 \
    -o "out/${ts}.${ext}" -- omp --no-session || true
done

# S4 typing-demo: console2svg cannot inject keystrokes into the running omp TUI
# headlessly, so per scenarios.md we animate the sample prompt at a shell prompt.
for ext in $FORMATS; do
  run capture -v -d macos --background "$BG" -w "$W" -h "$H" --fps "$FPS" \
    -o "out/${td}.${ext}" -- bash "$TYPED" echo "explain what this repository does" || true
done

echo "=== gifs (path size) ==="
find out -type f -name '*.gif' -printf '%p %s\n' 2>/dev/null || find out -type f -name '*.gif'
echo "=== out ==="; ls -la out || true
