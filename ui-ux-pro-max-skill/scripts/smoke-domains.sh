#!/usr/bin/env bash
# Smoke test every registered non-stack search domain.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS_DIR="$REPO_ROOT/src/ui-ux-pro-max/scripts"
SEARCH="$SCRIPTS_DIR/search.py"
QUERY="${1:-dashboard performance button typography chart icon animation}" 
EXPECTED_COUNT="${EXPECTED_DOMAIN_COUNT:-12}"

if [ ! -f "$SEARCH" ]; then
  echo "FAIL: search.py not found at $SEARCH" >&2
  exit 2
fi

DOMAINS=()
while IFS= read -r line; do
  line="${line%$'\r'}"
  [ -n "$line" ] && DOMAINS+=("$line")
done < <(PYTHONPATH="$SCRIPTS_DIR" python3 -c "
from core import CSV_CONFIG
for domain in CSV_CONFIG:
    print(domain)
")

if [ "${#DOMAINS[@]}" -ne "$EXPECTED_COUNT" ]; then
  echo "FAIL: CSV_CONFIG has ${#DOMAINS[@]} domains, expected $EXPECTED_COUNT" >&2
  echo "      Set EXPECTED_DOMAIN_COUNT after an intentional registry change." >&2
  exit 2
fi

echo "Smoke-testing ${#DOMAINS[@]} domains with query '$QUERY':"
fail=0
for domain in "${DOMAINS[@]}"; do
  payload=$(python3 "$SEARCH" "$QUERY" --domain "$domain" -n 1 --json 2>/dev/null || true)
  count=$(printf '%s' "$payload" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data.get('count',0) if not data.get('error') else 0)" 2>/dev/null || echo 0)
  if [ "${count:-0}" -gt 0 ]; then
    printf '  PASS  %-14s %d\n' "$domain" "$count"
  else
    printf '  FAIL  %-14s 0\n' "$domain"
    fail=$((fail + 1))
  fi
done

total=${#DOMAINS[@]}
echo
if [ "$fail" -gt 0 ]; then
  echo "FAIL: $fail/$total domains returned 0 results for '$QUERY'" >&2
  exit 1
fi

echo "OK: $total/$total domains returned ≥1 result"
