#!/usr/bin/env bash
# merge-pr.sh — Safe merge for solo-developer workflow.
#
# Verifies all CI checks are green before executing the admin bypass.
# Refuses to proceed otherwise.
#
# Usage: ./scripts/merge-pr.sh [PR-number]

set -euo pipefail

REPO="bc-austine/tmpmas"
PR="${1:-}"

if [ -z "$PR" ]; then
    echo "Usage: $0 <PR-number>"
    exit 1
fi

echo "→ Checking CI status for PR #${PR}..."
CHECKS_JSON=$(gh pr checks "$PR" --repo "$REPO" --json state,name 2>&1 || true)

# Refuse if any check is NOT in a passing state.
# Acceptable states: SUCCESS, SKIPPED, NEUTRAL.
# Everything else (PENDING, FAILURE, CANCELLED, TIMED_OUT, ACTION_REQUIRED)
# means the PR is not safe to merge.
UNACCEPTABLE=$(echo "$CHECKS_JSON" | \
    grep -oE '"state":"[A-Z_]+"' | \
    grep -vE '"state":"(SUCCESS|SKIPPED|NEUTRAL)"' || true)

if [ -n "$UNACCEPTABLE" ]; then
    echo "✗ Refusing to merge: CI checks not all green."
    echo "  Non-passing states:"
    echo "$UNACCEPTABLE" | sort -u | sed 's/^/    /'
    echo "  Run 'gh pr checks $PR' to see details."
    exit 1
fi

# Guard against the empty-checks case (no checks have been registered yet).
if [ -z "$CHECKS_JSON" ] || [ "$CHECKS_JSON" = "[]" ]; then
    echo "✗ Refusing to merge: no CI checks found for PR #${PR}."
    echo "  Confirm the PR has triggered CI before merging."
    exit 1
fi

echo "✓ All CI checks green. Proceeding with standard merge (no --admin)."
echo "  Note: PR must already have an approving review from a non-author."
echo ""

gh pr merge "$PR" --squash --delete-branch --repo "$REPO"

echo "✓ Merge complete."
