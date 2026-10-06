# Error and reliability boundaries

Error handling is about ownership, not visual cleanliness.

Before changing an error path establish:

1. where the failure originates;
2. which layer understands its meaning;
3. which layer can recover;
4. which layer should add context;
5. which layer should log;
6. which layer decides whether the operation continues.

## Swallowed errors

An empty or minimal catch is suspicious when it destroys meaningful failure information.

It may still be intentional for:

- best-effort telemetry;
- feature detection;
- cleanup;
- optional enrichment;
- compatibility probing.

Understand the owner before changing behavior.

Never blindly convert:

`catch {}`

into:

`log + throw`.

That changes observable semantics.

## Fallbacks

An empty array, empty string, null, cached value, or default object may represent:

- legitimate degradation;
- product behavior;
- backward compatibility;
- masking of infrastructure failure.

Determine which before removing it.

## Logging

Avoid duplicate logging across layers.

The layer that has sufficient context and ownership should normally log.

Lower-level code may enrich or propagate errors without logging when an outer boundary owns observability.

Do not remove logs solely because console output resembles debug residue; CLI or system output may be contractual.

Do not casually rewrite log templates, structured field names, event names, metric labels, or severity. Dashboards, alerts, parsers, support procedures, and tests may depend on them even when no static caller is visible.

## Error and output wording

Error messages, status text, stdout, and stderr are potentially observable behavior.

Before rewording, check:

- tests and snapshots;
- callers that parse or display the text;
- CLI and API compatibility expectations;
- monitoring, support, or localization workflows;
- whether the repository treats error codes or typed values as the stable contract instead.

Improve wording only when the task permits it and the compatibility surface is understood. Do not replace precise domain language with generic claims such as "operation failed gracefully" or "an unexpected issue occurred".

## Retry

Before modifying retry logic determine:

- which failures are retryable;
- retry owner;
- maximum attempts;
- backoff;
- jitter;
- timeout;
- idempotency;
- side effects.

Retries without idempotency analysis are high risk.

## Timeout and cancellation

Do not add or remove timeout/cancellation behavior without understanding:

- caller expectations;
- resource ownership;
- cleanup;
- nested timeout interactions.

## Transactions

Transaction scope is semantic.

Moving calls inside or outside a transaction can change consistency and locking behavior even when code looks simpler.

Treat transaction refactors as R3 or R4.

## Partial failure

Distributed or multi-step work may intentionally succeed partially.

Do not force all-or-nothing behavior unless the domain contract requires it.

## Reliability rule

A cleaner-looking error path is not automatically a more correct one.

Preserve operational semantics unless evidence justifies change.
