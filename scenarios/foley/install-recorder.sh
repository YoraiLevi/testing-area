#!/usr/bin/env bash
# Install the pinned foley recorder (GH-Jaider/foley) as a prebuilt release binary into
# /usr/local/bin, plus ffmpeg (foley's only runtime dependency for gif/mp4/webm encoding).
# Linux (x86_64/arm64) and macOS (arm64/x86_64) only — foley is libghostty-vt based and has
# no Windows build. tools.json pins "latest"; the latest (and only) release is v0.1.0, pinned
# concretely here for reproducibility (SC-007) and recorded in extra.tool_version.
set -euo pipefail

FOLEY_TAG="v0.1.0"
FOLEY_VER="0.1.0"
BIN_DIR="/usr/local/bin"

uname_s="$(uname -s)"
uname_m="$(uname -m)"

case "$uname_s" in
  Linux)  os="linux" ;;
  Darwin) os="darwin" ;;
  *) echo "install-recorder: unsupported OS $uname_s" >&2; exit 1 ;;
esac

case "$uname_m" in
  x86_64|amd64)  arch="amd64" ;;
  arm64|aarch64) arch="arm64" ;;
  *) echo "install-recorder: unsupported arch $uname_m" >&2; exit 1 ;;
esac

# The linux tarball is a fully static binary (runs on any glibc/musl distro, so no
# GLIBC_2.38 trouble on ubuntu-22.04); darwin links normally but is self-contained
# (engine + fonts baked in). One file, no $FOLEY_FONTS needed.
tarball="foley_${FOLEY_VER}_${os}_${arch}.tar.gz"
url="https://github.com/GH-Jaider/foley/releases/download/${FOLEY_TAG}/${tarball}"
tmp="$(mktemp -d)"

echo "::group::install foley ${FOLEY_TAG} (${os}/${arch})"
curl -fsSL "$url" -o "${tmp}/foley.tar.gz"
tar xzf "${tmp}/foley.tar.gz" -C "${tmp}"
sudo mv "${tmp}/foley" "${BIN_DIR}/foley"
sudo chmod +x "${BIN_DIR}/foley"
foley --version
echo "::endgroup::"

# ffmpeg is foley's only runtime dependency; GHA runner images do not always ship it.
if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "::group::install ffmpeg"
  if [ "$os" = "darwin" ]; then
    brew install ffmpeg
  else
    sudo apt-get update -qq && sudo apt-get install -y -qq ffmpeg
  fi
  echo "::endgroup::"
fi

echo "::group::foley doctor"
foley doctor || true
echo "::endgroup::"
