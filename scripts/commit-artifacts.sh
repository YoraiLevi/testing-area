#!/usr/bin/env bash
# Commit produced recordings/results back to testing-vhs without racing concurrent
# tool workflows. Usage: commit-artifacts.sh "<commit message>" [path ...]
# Default staged paths: assets results. NEVER commits README (report.yml owns it).
set -euo pipefail

MSG="${1:-chore: update recordings}"
shift || true
PATHS=("$@")
if [ "${#PATHS[@]}" -eq 0 ]; then
  PATHS=(assets results)
fi

git config user.name "recorder-trials-bot"
git config user.email "actions@users.noreply.github.com"

git add -- "${PATHS[@]}" 2>/dev/null || true
if git diff --cached --quiet; then
  echo "commit-artifacts: nothing to commit"
  exit 0
fi
git commit -m "$MSG"

for attempt in 1 2 3 4 5 6; do
  if git pull --rebase --autostash origin testing-vhs && \
     git push origin HEAD:testing-vhs; then
    echo "commit-artifacts: pushed on attempt $attempt"
    exit 0
  fi
  sleep $(( (RANDOM % 6) + attempt ))
done

echo "commit-artifacts: push failed after retries" >&2
exit 1
