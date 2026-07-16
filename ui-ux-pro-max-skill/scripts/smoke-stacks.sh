#!/usr/bin/env bash
# Smoke test: every stack registered in STACK_CONFIG must return at least one
# search result for a neutral query. Catches registry/CSV regressions early
# (e.g. a stack added to STACK_CONFIG but missing its CSV, or a CSV emptied
# by a botched merge).
#
# Usage:  scripts/smoke-stacks.sh [query]
# Env:    EXPECTED_STACK_COUNT — default 22. Bump deliberately when adding
#         or removing a stack so accidental drift still fails loudly.
#
# Exit codes:
#   0 — all stacks returned ≥1 result
#   1 — at least one stack returned 0 results
#   2 — environment problem (search.py missing, registry size mismatch)

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$REPO_ROOT/src/ui-ux-pro-max/scripts"
SEARCH="$SCRIPTS_DIR/search.py"

QUERY="${1:-performance}"
EXPECTED_COUNT="${EXPECTED_STACK_COUNT:-22}"

if [ ! -f "$SEARCH" ]; then
  echo "FAIL: search.py not found at $SEARCH" >&2
  exit 2
fi

# Single source of truth: pull stacks from STACK_CONFIG so this script never
# goes stale relative to the registry.
STACKS=()
while IFS= read -r line; do
  line="${line%$'\r'}"  # strip CR on Windows where python's print emits CRLF
  [ -n "$line" ] && STACKS+=("$line")
done < <(PYTHONPATH="$SCRIPTS_DIR" python3 -c "
from core import AVAILABLE_STACKS
for s in AVAILABLE_STACKS:
    print(s)
")

if [ "${#STACKS[@]}" -ne "$EXPECTED_COUNT" ]; then
  echo "FAIL: STACK_CONFIG has ${#STACKS[@]} stacks, expected $EXPECTED_COUNT" >&2
  echo "      Set EXPECTED_STACK_COUNT to override after an intentional change." >&2
  exit 2
fi

echo "Smoke-testing ${#STACKS[@]} stacks with query '$QUERY':"
fail=0
for s in "${STACKS[@]}"; do
  count=$(python3 "$SEARCH" "$QUERY" --stack "$s" -n 1 --json 2>/dev/null \
    | python3 -c "import json,sys; print(json.load(sys.stdin).get('count',0))")
  if [ "${count:-0}" -gt 0 ]; then
    printf '  PASS  %-18s %d\n' "$s" "$count"
  else
    printf '  FAIL  %-18s 0\n' "$s"
    fail=$((fail + 1))
  fi
done

total=${#STACKS[@]}
echo
if [ "$fail" -gt 0 ]; then
  echo "FAIL: $fail/$total stacks returned 0 results for '$QUERY'" >&2
  exit 1
fi
echo "OK: $total/$total stacks returned ≥1 result"
