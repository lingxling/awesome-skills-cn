# Refactor Examples by Risk Band (R0–R4)

Read this when `SKILL.md` Workflow steps 3–4 flag a candidate finding. Each band shows a minimal good vs bad intervention. Do not mutate on style alone. Each good example cites a concrete consequence.

## R0 - Mechanical (formatter-provable)

Bad: hand-reformat churn across 40 files in a feature diff.
```diff
- x=1
+ x = 1   # + 200 unrelated lines
```
Good: run repo formatter only on touched lines, zero semantic diff. Consequence avoided: review noise.

## R1 - Low Structural (local residue)

Bad: leave `import os` unused + `print(debug)` in shipped diff.
```python
import os  # unused
print("here", x)
```
Good:
```diff
-import os
-print("here", x)
```
Verify: affected unit test still passes. Consequence: dead weight + log leak.

## R2 - Contextual Structural (predicate extraction)

Bad: two callers implement divergent checks for the same owned validation policy:
```python
if not tenant or not tenant.strip(): raise ValueError
# ... 30 lines later in another module ...
if tenant is None or tenant == "": raise ValueError
```
Good: single affirmative predicate, same ownership/invariants:
```python
def _is_valid_tenant(v) -> bool:
    return isinstance(v, str) and bool(v.strip())
```
Consolidate only when shared ownership + same reason to change. Keep small local duplication if abstraction adds coupling. Consequence: divergent policy.

## R3 - Semantic (retry / serialization / transactions)

Bad: blanket retry hiding infra failure:
```python
for _ in range(5):
    try: return publish(ev)
    except Exception: continue
```
Good: idempotency-aware, bounded, owner-logged:
```python
for attempt in range(3):
    try:
        return publish(ev, idempotency_key=ev.id)
    except TransientError:
        if attempt == 2:
            raise
        log.warning(
            "publish retry",
            extra={"attempt": attempt + 1},
        )
```
Retry only transient failures; propagate the final failure after exhaustion and
non-transient errors immediately. Follow the repository's existing backoff and timeout
policy. Verify eventual success, exhausted retries, and a non-retryable failure.
Never mass-rewrite R3 without explicit instruction + verified tests.

## R4 - Critical Boundary (auth / migration / durability)

Bad: mutate contract in place without preserving last-valid state.
Good: preserve + report, do not guess:
```python
# preserve LEDGER_FILE: str contract, stage replacement, fsync, atomic rename
# if intent/ownership/migration semantics unclear, stop and report
```
Maximum conservatism. Missing evidence means preserve plus a completion report `Needs review`.
