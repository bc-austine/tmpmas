#!/usr/bin/env bash
# verify-branch-protection.sh
# Read-only check that branch protection is enforced on main, with
# check-run context names matching what GitHub Actions actually reports.
#
# Per SM action A18. Run any time to confirm enforcement.
#
# Usage: ./scripts/verify-branch-protection.sh

set -euo pipefail

REPO="bc-austine/tmpmas"

echo "→ Checking branch protection on main for ${REPO}..."
PROTECTION=$(gh api "repos/${REPO}/branches/main/protection")

check_field() {
    local field="$1"
    local expected="$2"
    local actual
    actual=$(echo "$PROTECTION" | python -c "import sys, json; d=json.load(sys.stdin); print(d.get('$field', {}).get('enabled', 'MISSING'))")
    if [ "$actual" = "$expected" ]; then
        echo "  ✓ $field = $actual"
    else
        echo "  ✗ $field = $actual (expected $expected)"
        return 1
    fi
}

echo ""
echo "→ Protections enabled:"
check_field "enforce_admins" "True"
check_field "required_linear_history" "True"
check_field "allow_force_pushes" "False"
check_field "allow_deletions" "False"
check_field "required_conversation_resolution" "True"

echo ""
echo "→ Pull request reviews:"
echo "$PROTECTION" | python -c "
import sys, json
d = json.load(sys.stdin)
r = d.get('required_pull_request_reviews', {})
print('  required_approving_review_count:', r.get('required_approving_review_count'))
print('  dismiss_stale_reviews:', r.get('dismiss_stale_reviews'))
print('  require_last_push_approval:', r.get('require_last_push_approval'))
"

echo ""
echo "→ Required status check contexts:"
echo "$PROTECTION" | python -c "
import sys, json
d = json.load(sys.stdin)
for c in d.get('required_status_checks', {}).get('contexts', []):
    print('  -', c)
"

echo ""
echo "→ Cross-checking contexts against actual check-run names on main HEAD..."
HEAD_SHA=$(gh api "repos/${REPO}/commits/main" --jq '.sha')

# Temp files avoid CRLF / heredoc issues on Windows Git Bash.
TMP_REQUIRED=$(mktemp)
TMP_ACTUAL=$(mktemp)
trap 'rm -f "$TMP_REQUIRED" "$TMP_ACTUAL"' EXIT

# Required contexts, one per line, no carriage returns.
echo "$PROTECTION" \
    | python -c "import sys, json; print('\n'.join(json.load(sys.stdin).get('required_status_checks', {}).get('contexts', [])))" \
    | tr -d '\r' > "$TMP_REQUIRED"

# Actual check-run names on HEAD of main, deduplicated, no carriage returns.
gh api "repos/${REPO}/commits/${HEAD_SHA}/check-runs" --jq '.check_runs[].name' \
    | tr -d '\r' | sort -u > "$TMP_ACTUAL"

MISMATCH=0
while IFS= read -r name; do
    [ -z "$name" ] && continue
    if ! grep -qxF "$name" "$TMP_ACTUAL"; then
        echo "  ✗ Required context '$name' is not reported by any recent check run"
        MISMATCH=$((MISMATCH+1))
    fi
done < "$TMP_REQUIRED"

if [ "$MISMATCH" -eq 0 ]; then
    echo "  ✓ All required contexts match actual check-run names"
fi

echo ""
if [ "$MISMATCH" -eq 0 ]; then
    echo "✓ Branch protection verified — contexts match reported checks."
else
    echo "✗ $MISMATCH context(s) mismatch — review required."
    exit 1
fi
