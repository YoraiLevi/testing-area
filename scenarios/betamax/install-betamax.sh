#!/usr/bin/env bash
# Install the Betamax (joshka) terminal recorder as a prebuilt release binary into
# /usr/local/bin. Pinned to v0.1.21 per scripts/tools.json. Betamax publishes only
# Linux (x86_64/aarch64, -gnu) and macOS (x86_64/aarch64) archives — Windows is
# unsupported upstream because libghostty-vt-sys has no Windows native build. Each
# archive contains a single statically-linked `betamax` executable (the native VT
# library is linked in), so no companion shared library is needed.
#
# Note on glibc: the Linux archives are `-gnu` builds (no musl variant is published),
# so the workflow runs the Linux cells on ubuntu-24.04 (glibc 2.39) to avoid a
# GLIBC_2.3x-not-found failure that an older runner (ubuntu-22.04, glibc 2.35) could hit.
set -euo pipefail

REPO="joshka/betamax"
BETAMAX_VERSION="${BETAMAX_VERSION:-0.1.21}"   # tools.json pin: v0.1.21
TAG="betamax-v${BETAMAX_VERSION}"
BIN_DIR="/usr/local/bin"

uname_s="$(uname -s)"
uname_m="$(uname -m)"

case "$uname_s" in
  Linux)  triple_os="unknown-linux-gnu" ;;
  Darwin) triple_os="apple-darwin" ;;
  *) echo "install-betamax: unsupported OS $uname_s (Betamax supports Linux/macOS only)" >&2; exit 1 ;;
esac
case "$uname_m" in
  x86_64|amd64)  arch="x86_64" ;;
  arm64|aarch64) arch="aarch64" ;;
  *) echo "install-betamax: unsupported arch $uname_m" >&2; exit 1 ;;
esac
triple="${arch}-${triple_os}"

# cargo-binstall archive naming: betamax-<version>-<target>.tgz on tag betamax-v<version>.
stage="betamax-${BETAMAX_VERSION}-${triple}"
url="https://github.com/${REPO}/releases/download/${TAG}/${stage}.tgz"

# Public repo works unauthenticated, but the workflow's GITHUB_TOKEN raises the API
# rate limit and avoids flaky release-asset lookups.
auth=()
if [ -n "${GITHUB_TOKEN:-}" ]; then
  auth=(-H "Authorization: Bearer ${GITHUB_TOKEN}")
fi

echo "::group::install betamax ${TAG} (${triple})"
tmpdir="$(mktemp -d)"
curl -fsSL "${auth[@]}" -o "${tmpdir}/${stage}.tgz" "$url"
tar -xzf "${tmpdir}/${stage}.tgz" -C "$tmpdir"
sudo install -m755 "${tmpdir}/betamax" "${BIN_DIR}/betamax"
echo "::endgroup::"

command -v betamax
betamax --version

# Publish the pinned tag for extra.tool_version in the result records.
if [ -n "${GITHUB_ENV:-}" ]; then
  echo "BETAMAX_TAG=${TAG}" >> "$GITHUB_ENV"
fi
