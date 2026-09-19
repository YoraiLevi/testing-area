#!/usr/bin/env bash
# Install Oh My Pi (omp) on a Linux/macOS CI runner and expose it on PATH.
# Robust against omp.sh rate limits: retry the official installer, then fall back to
# the Bun registry package (which provides the `omp` binary).
set -euo pipefail

add_paths() {
  for d in "$HOME/.local/bin" "$HOME/.bun/bin" "$HOME/.omp/bin" "/usr/local/bin"; do
    if [ -d "$d" ]; then
      echo "$d" >> "${GITHUB_PATH:-/dev/null}"
      export PATH="$d:$PATH"
    fi
  done
}

install_via_curl() {
  for i in 1 2 3 4 5; do
    echo "omp: official installer attempt $i"
    if curl -fsSL https://omp.sh/install | sh; then return 0; fi
    sleep $((i * 5))
  done
  return 1
}

install_via_bun() {
  echo "omp: falling back to Bun registry install"
  if ! command -v bun >/dev/null 2>&1; then
    curl -fsSL https://bun.sh/install | bash
    export BUN_INSTALL="${BUN_INSTALL:-$HOME/.bun}"
    export PATH="$BUN_INSTALL/bin:$PATH"
  fi
  for i in 1 2 3; do
    if bun install -g @oh-my-pi/pi-coding-agent; then return 0; fi
    sleep $((i * 5))
  done
  return 1
}

echo "::group::install omp"
install_via_curl || install_via_bun
echo "::endgroup::"

add_paths
command -v omp
omp --version
