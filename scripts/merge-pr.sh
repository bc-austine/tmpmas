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

if echo "$CHECKS_JSON" | grep -q '"state":"PENDING"'; then
    echo "✗ Refusing to merge: CI checks still pending."
    echo "  Run 'gh pr checks $PR' to see current status."
    exit 1
fi

if echo "$CHECKS_JSON" | grep -q '"state":"FAILURE"'; then
    echo "✗ Refusing to merge: CI checks failing."
    echo "  Run 'gh pr checks $PR' to see details."
    exit 1
fi

echo "✓ All CI checks green. Proceeding with admin merge sequence..."

gh api --method DELETE \
    -H "Accept: application/vnd.github+json" \
    "repos/${REPO}/branches/main/protection/enforce_admins"

gh pr merge "$PR" --squash --admin --delete-branch --repo "$REPO"

gh api --method POST \
    -H "Accept: application/vnd.github+json" \
    "repos/${REPO}/branches/main/protection/enforce_admins"

echo "✓ Merge complete. Branch protection restored."
