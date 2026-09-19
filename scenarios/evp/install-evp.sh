#!/usr/bin/env bash
# Install the EVP terminal recorder (HalFrgrd/evp) as a prebuilt, statically-linked
# musl binary into /usr/local/bin. Pinned to `latest` per scripts/tools.json; the
# resolved release tag is exported (EVP_TAG) so the workflow can record it in
# extra.tool_version. Linux (x86_64/aarch64) and macOS (arm64/x86_64) only — EVP
# publishes no Windows build (see the tool's install.sh / action.yml).
set -euo pipefail

REPO="HalFrgrd/evp"
EVP_VERSION="${EVP_VERSION:-latest}"   # tools.json pin: latest
BIN_DIR="/usr/local/bin"

uname_s="$(uname -s)"
uname_m="$(uname -m)"

# Linux: use the static musl build so the binary carries no glibc dependency
# (ubuntu-22.04 ships glibc 2.35; a -gnu build needing GLIBC_2.38 would fail there).
case "$uname_s" in
  Linux)  triple_os="unknown-linux-musl" ;;
  Darwin) triple_os="apple-darwin" ;;
  *) echo "install-evp: unsupported OS $uname_s" >&2; exit 1 ;;
esac
case "$uname_m" in
  x86_64|amd64)  arch="x86_64" ;;
  arm64|aarch64) arch="aarch64" ;;
  *) echo "install-evp: unsupported arch $uname_m" >&2; exit 1 ;;
esac
triple="${arch}-${triple_os}"

# Public repo works unauthenticated, but the workflow's GITHUB_TOKEN raises the API
# rate limit and avoids flaky release lookups.
auth=()
if [ -n "${GITHUB_TOKEN:-}" ]; then
  auth=(-H "Authorization: Bearer ${GITHUB_TOKEN}")
fi

if [ "$EVP_VERSION" = "latest" ]; then
  api="https://api.github.com/repos/${REPO}/releases/latest"
else
  api="https://api.github.com/repos/${REPO}/releases/tags/${EVP_VERSION}"
fi

echo "::group::resolve evp release (${EVP_VERSION})"
release_json="$(curl -fsSL "${auth[@]}" "$api")"
TAG="$(printf '%s' "$release_json" | grep -m1 '"tag_name":' | sed -E 's/.*"tag_name": *"([^"]+)".*/\1/')"
[ -n "$TAG" ] || { echo "install-evp: could not resolve release tag from $api" >&2; exit 1; }
echo "resolved tag: $TAG"
echo "::endgroup::"

version_no_v="${TAG#v}"
stage="evp-${version_no_v}-${triple}"
url="https://github.com/${REPO}/releases/download/${TAG}/${stage}.tar.gz"

echo "::group::install evp ${TAG} (${triple})"
tmpdir="$(mktemp -d)"
curl -fsSL "${auth[@]}" -o "${tmpdir}/${stage}.tar.gz" "$url"
if curl -fsSL "${auth[@]}" -o "${tmpdir}/${stage}.tar.gz.sha256" "${url}.sha256" 2>/dev/null; then
  (cd "$tmpdir" && sha256sum -c "${stage}.tar.gz.sha256")
else
  echo "install-evp: no .sha256 published for ${TAG}; skipping verification" >&2
fi
tar -xzf "${tmpdir}/${stage}.tar.gz" -C "$tmpdir"
sudo install -m755 "${tmpdir}/${stage}/evp" "${BIN_DIR}/evp"
echo "::endgroup::"

command -v evp
evp --version

# Publish the resolved tag for extra.tool_version in the result records.
if [ -n "${GITHUB_ENV:-}" ]; then
  echo "EVP_TAG=${TAG}" >> "$GITHUB_ENV"
fi
