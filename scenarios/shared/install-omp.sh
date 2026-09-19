#!/usr/bin/env bash
# Install Oh My Pi (omp) on a Linux/macOS CI runner and expose it on PATH.
# Evidence subject for the recorder trials. No auth required for --version/--help.
set -euo pipefail

echo "::group::install omp"
curl -fsSL https://omp.sh/install | sh
echo "::endgroup::"

# The installer drops omp in one of these; add all that exist to PATH.
for d in "$HOME/.local/bin" "$HOME/.bun/bin" "$HOME/.omp/bin" "/usr/local/bin"; do
  if [ -d "$d" ]; then
    echo "$d" >> "${GITHUB_PATH:-/dev/null}"
    export PATH="$d:$PATH"
  fi
done

# Fail loudly if omp is not runnable (FR-007: never a false pass).
command -v omp
omp --version
