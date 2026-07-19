#!/usr/bin/env bash
# One-shot: initialize (if needed) and push BrandBrain to a GitHub repo.
# Usage:  ./setup-github.sh git@github.com:<you>/brandbrain.git
set -euo pipefail
REMOTE="${1:-}"
if [ -z "$REMOTE" ]; then
  echo "Usage: ./setup-github.sh <git-remote-url>"
  echo "Tip (GitHub CLI):  gh repo create brandbrain --private --source=. --push --remote=origin"
  exit 1
fi
[ -d .git ] || git init
git add -A
git commit -m "Initial commit: BrandBrain (frontend demo + backend scaffold + docs)" || echo "nothing to commit"
git branch -M main
git remote remove origin 2>/dev/null || true
git remote add origin "$REMOTE"
git push -u origin main
echo "Pushed to $REMOTE"
