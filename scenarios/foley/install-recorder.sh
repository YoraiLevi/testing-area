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

# ffmpeg is foley's only runtime dependency, and foley requires ffmpeg >= 6. macOS brew
# ships a current ffmpeg, but ubuntu's apt tops out at 4.x (foley rejects it: "ffmpeg 4 < 6"),
# so on Linux install a static ffmpeg 7.x from BtbN's GitHub builds into /usr/local/bin
# (ahead of /usr/bin on PATH). Only (re)install when the present ffmpeg is older than 6.
ffmpeg_major() {
  command -v ffmpeg >/dev/null 2>&1 || { echo 0; return; }
  ffmpeg -version 2>/dev/null | head -1 | grep -oE 'version n?[0-9]+' | head -1 | grep -oE '[0-9]+' || echo 0
}

if [ "$(ffmpeg_major)" -lt 6 ]; then
  echo "::group::install ffmpeg (>= 6, foley requirement)"
  if [ "$os" = "darwin" ]; then
    brew install ffmpeg
  else
    case "$arch" in
      amd64) ff_arch="linux64" ;;
      arm64) ff_arch="linuxarm64" ;;
    esac
    ff_url="https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-${ff_arch}-gpl.tar.xz"
    ff_tmp="$(mktemp -d)"
    curl -fsSL "$ff_url" -o "${ff_tmp}/ffmpeg.tar.xz"
    tar xJf "${ff_tmp}/ffmpeg.tar.xz" -C "${ff_tmp}"
    ff_bin="$(find "${ff_tmp}" -maxdepth 2 -type f -name ffmpeg | head -1)"
    sudo cp -f "$(dirname "$ff_bin")/ffmpeg" "$(dirname "$ff_bin")/ffprobe" "${BIN_DIR}/"
    sudo chmod +x "${BIN_DIR}/ffmpeg" "${BIN_DIR}/ffprobe"
  fi
  echo "ffmpeg -> $(command -v ffmpeg): $(ffmpeg -version 2>/dev/null | head -1)"
  echo "::endgroup::"
fi

echo "::group::foley doctor"
foley doctor || true
echo "::endgroup::"
