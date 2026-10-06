# Migration Examples (atomic vs transitional)

Read in Evolve mode when changing a public contract or persisted schema.

## Atomic replacement (preferred for single-node file state)

```python
import os
import tempfile
from pathlib import Path

def replace_file(dest: Path, new_bytes: bytes) -> None:
    tmp = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            dir=dest.parent,
            prefix=f".{dest.name}.",
            suffix=".tmp",
            delete=False,
        ) as file:
            tmp = Path(file.name)
            file.write(new_bytes)
            file.flush()
            os.fsync(file.fileno())

        os.replace(tmp, dest)
    finally:
        if tmp is not None:
            tmp.unlink(missing_ok=True)
```

Invariants: validate inputs + destination ownership before mutation; retain last valid
state until replacement succeeds. Stage on the destination filesystem with a unique
temporary name; close the file before replacement and clean up the temporary file on
success or failure. Verify successful replacement and preservation of the old state
when writing, syncing, or replacement fails.
This example addresses ordinary I/O failures. Power-loss durability and recovery after
forced termination require platform-specific guarantees and separate verification.

## Transitional compatibility (multi-caller migration)

Bad: change producer to `Decimal("5.00")` while callers expect `int 5` → hidden breakage.
Good:
1. Keep old readers working (accept `int | str | Decimal`, normalize internally).
2. Migrate callers one by one while preserving compatibility for remaining consumers.
3. Add contract and caller tests covering both surfaces during transition.
4. Remove compat shim only after all callers + docs updated.

## Docs sync checklist

- Update `README.md` + CLI help in the same diff as the contract change.
- Document only behavior implemented and verified in the delivered code state.
