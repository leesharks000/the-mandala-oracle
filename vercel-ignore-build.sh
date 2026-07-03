#!/usr/bin/env bash
# Vercel "Ignored Build Step" — skip the build when only files under book/
# changed since the last successfully deployed commit.
#
#   exit 0 → cancel the build (skip; doesn't count against deploy quota)
#   exit 1 → proceed with the build
#
# Strategy:
#
#   1. If VERCEL_GIT_PREVIOUS_SHA is set, try to diff against it. Vercel does
#      shallow clones, so the SHA may not be reachable; in that case, we try
#      to fetch it explicitly, and if that also fails, we fall through to (2)
#      instead of defaulting to "build" (which was the original bug — every
#      book commit was building because the shallow clone defeated the diff).
#
#   2. As fallback, inspect just the most-recent commit via `git show`.
#      This works regardless of clone depth. The trade-off: in the rare case
#      where multiple commits stack and Vercel runs the ignore step only
#      against the latest, we'd miss any non-book change in earlier stacked
#      commits. In practice this is acceptable — Vercel evaluates the ignore
#      step per push, so each push gets its own check, and a code change that
#      happens to be stacked with book commits would still surface as the
#      tip of the new push and trigger a build.
#
#   3. The book commit messages also carry "[skip ci]" markers (set by
#      api/book.py). If Vercel honors those markers — which it does for
#      `[skip ci]` and `[ci skip]` per the Vercel docs — this script is
#      belt-and-suspenders. The marker is the primary defense; this script
#      is the secondary defense.

set -u

# MANUS override: redactions and revocations must always ship, even when they
# touch only book/ paths — a stranded redaction is a live privacy exposure.
case "${VERCEL_GIT_COMMIT_MESSAGE:-}" in
  *MANUS*|*redact*|*Redact*|*REDACT*|*revocation*) echo "[ignore-build] MANUS/redaction commit — building unconditionally."; exit 1;;
esac

# Determine which paths changed.
get_changed_paths() {
  local changed=""

  # Strategy 1: diff against VERCEL_GIT_PREVIOUS_SHA if reachable.
  if [ -n "${VERCEL_GIT_PREVIOUS_SHA:-}" ]; then
    # If the SHA isn't in the local clone (shallow), try to fetch it once.
    if ! git cat-file -e "$VERCEL_GIT_PREVIOUS_SHA^{commit}" 2>/dev/null; then
      git fetch --no-tags --depth=1 origin "$VERCEL_GIT_PREVIOUS_SHA" 2>/dev/null || true
    fi
    # Now try the diff; if the SHA is still unreachable (hook builds often
    # clone at depth 1 with no fetchable lone-SHA), deepen and retry once —
    # tip-only inspection strands range deployments whose tip is book-only.
    if ! git cat-file -e "$VERCEL_GIT_PREVIOUS_SHA^{commit}" 2>/dev/null; then
      git fetch --no-tags --deepen=100 origin "$(git rev-parse --abbrev-ref HEAD)" 2>/dev/null || \
      git fetch --no-tags --deepen=100 origin main 2>/dev/null || true
    fi
    if changed=$(git diff --name-only "$VERCEL_GIT_PREVIOUS_SHA" HEAD 2>/dev/null); then
      echo "$changed"
      return 0
    fi
    echo >&2 "[ignore-build] could not diff against $VERCEL_GIT_PREVIOUS_SHA — falling back to HEAD inspection."
  fi

  # Strategy 2: inspect just the most recent commit.
  # `git diff-tree -m` handles merge commits correctly (without -m, merges
  # return empty); the -r flag recurses into subdirectories.
  changed=$(git diff-tree -m --no-commit-id --name-only -r HEAD 2>/dev/null)
  if [ -z "$changed" ]; then
    # Couldn't even inspect HEAD — build to be safe.
    return 1
  fi
  echo "$changed"
}

if ! changed=$(get_changed_paths); then
  echo "[ignore-build] could not determine changed paths — building."
  exit 1
fi

# Filter to files that are NOT under book/.
non_book=$(printf '%s\n' "$changed" | grep -v '^book/' | grep -v '^$' || true)

if [ -z "$non_book" ]; then
  echo "[ignore-build] only book/ files changed — skipping build."
  echo "[ignore-build] changed paths:"
  printf '%s\n' "$changed" | sed 's/^/  /'
  exit 0
fi

echo "[ignore-build] non-book changes detected:"
printf '%s\n' "$non_book" | sed 's/^/  /'
exit 1
