#!/usr/bin/env bash
# Install the pinned asciinema CLI (v3.2.1) and agg converter (v1.9.0) as prebuilt release
# binaries into /usr/local/bin. Linux (x86_64) and macOS (arm64/x86_64) only.
set -euo pipefail

ASCIINEMA_VERSION="v3.2.1"
AGG_VERSION="v1.9.0"
BIN_DIR="/usr/local/bin"

uname_s="$(uname -s)"
uname_m="$(uname -m)"

# Linux: use the statically-linked musl builds so the binaries do not depend on the
# runner's (older) glibc. ubuntu-22.04 ships glibc 2.35, but agg's -gnu build requires
# GLIBC_2.38, so -gnu fails there while -musl runs everywhere.
case "$uname_s" in
  Linux)  triple_os="unknown-linux-musl" ;;
  Darwin) triple_os="apple-darwin" ;;
  *) echo "install-recorder: unsupported OS $uname_s" >&2; exit 1 ;;
esac

case "$uname_m" in
  x86_64|amd64)  arch="x86_64" ;;
  arm64|aarch64) arch="aarch64" ;;
  *) echo "install-recorder: unsupported arch $uname_m" >&2; exit 1 ;;
esac

triple="${arch}-${triple_os}"
asciinema_url="https://github.com/asciinema/asciinema/releases/download/${ASCIINEMA_VERSION}/asciinema-${triple}"
agg_url="https://github.com/asciinema/agg/releases/download/${AGG_VERSION}/agg-${triple}"

echo "::group::install asciinema ${ASCIINEMA_VERSION} (${triple})"
sudo curl -fsSL "$asciinema_url" -o "${BIN_DIR}/asciinema"
sudo chmod +x "${BIN_DIR}/asciinema"
asciinema --version
echo "::endgroup::"

echo "::group::install agg ${AGG_VERSION} (${triple})"
sudo curl -fsSL "$agg_url" -o "${BIN_DIR}/agg"
sudo chmod +x "${BIN_DIR}/agg"
agg --version
echo "::endgroup::"
