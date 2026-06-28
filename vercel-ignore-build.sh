#!/usr/bin/env bash
# Vercel "Ignored Build Step" — skip the build when only files under book/
# changed since the last successfully deployed commit.
#
#   exit 0 → cancel the build (skip; doesn't count against deploy quota)
#   exit 1 → proceed with the build
#
# Why VERCEL_GIT_PREVIOUS_SHA and not HEAD^:
#   If five book commits land in a row, comparing HEAD^ to HEAD would only
#   see the most recent commit's diff (all book), correctly skipping. But
#   when Lee then pushes a code fix on top of those five book commits, HEAD^
#   would be the most recent book commit — making the diff look like only
#   the code change, missing context. VERCEL_GIT_PREVIOUS_SHA gives us the
#   last commit Vercel actually deployed, so the diff always covers the
#   full window of changes that haven't yet been built.

set -u

# First deploy on this branch — VERCEL_GIT_PREVIOUS_SHA is unset. Build.
if [ -z "${VERCEL_GIT_PREVIOUS_SHA:-}" ]; then
  echo "[ignore-build] no VERCEL_GIT_PREVIOUS_SHA — first deploy, building."
  exit 1
fi

# Diff against the last successfully deployed commit. If git can't reach
# that SHA (e.g. shallow clone hasn't fetched it), default to building —
# better to over-deploy than to leave a real code change un-deployed.
if ! changed=$(git diff --name-only "$VERCEL_GIT_PREVIOUS_SHA" HEAD 2>/dev/null); then
  echo "[ignore-build] could not diff against $VERCEL_GIT_PREVIOUS_SHA — building."
  exit 1
fi

# Filter to files that are NOT under book/.
non_book=$(printf '%s\n' "$changed" | grep -v '^book/' | grep -v '^$' || true)

if [ -z "$non_book" ]; then
  echo "[ignore-build] only book/ files changed since $VERCEL_GIT_PREVIOUS_SHA — skipping build."
  exit 0
else
  echo "[ignore-build] non-book changes detected since $VERCEL_GIT_PREVIOUS_SHA:"
  echo "$non_book" | sed 's/^/  /'
  exit 1
fi
