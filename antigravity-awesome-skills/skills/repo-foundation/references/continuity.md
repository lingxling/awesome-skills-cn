# Continuity: session handover and reconciling state

Use this reference when resuming work in a new session, taking over a repository, or when recorded notes disagree with the actual codebase.

---

## 1. Reconciling notes with code reality

When taking over an ongoing project, compare documented status with the actual state of the working tree.

Code shows what the software does right now. That alone doesn't prove it meets the requirements or acceptance criteria.

When notes and code conflict, cross-check requirements and tests first.
Go back to the user's original requirements, preserved contracts, and actual test coverage.
Passing tests are not a rubber stamp.
Green tests don't declare a feature complete if acceptance criteria or edge cases were never tested.
Don't edit notes just to legitimize whatever code happens to be there.
Investigate before updating.
Notes say pending but code looks done? Verify against the requirement and run or add acceptance checks.
If truly complete and verified, update the notes.
If partial or defective, fix the code.
Don't rubber-stamp the notes.
Never do a blind rollback.
Don't delete working code just because some stale note doesn't mention it.
If intent is ambiguous, ask the user.

---

## 2. Working in dirty workspaces

Users often call agents into workspaces with uncommitted work. Inspect `git status` (or directory state when not using Git) before modifying files; inventory comes first only in the sense that mutation must wait for it.
Identify uncommitted changes belonging to the user and do not discard or clobber them.
Protecting user changes does *not* forbid editing the entire file.
You may modify distinct, relevant parts of the same file as long as the user's uncommitted changes remain intact and functional.
Only stop and ask if there is an actual conflict or if the user's intent cannot be determined.
The baseline for verification and diffing includes the base commit plus the pre-existing uncommitted modifications.
Your changes must stay distinguishable from earlier user changes.
Never execute `git commit`, `git stash`, or `git reset` automatically to create a clean slate unless the user explicitly commands it.
No forced commits.

---

## 3. Handing over a session

When ending a session or preparing a handoff for another agent or developer, reuse existing channels.
Record state in existing project tracking mechanisms (e.g., project issue trackers, `TODO` lists, or brief handover notes).
Do not create ad-hoc handoff files for routine features.
A concise handoff says what got done and verified, the working tree status, remaining limits or next steps, and which verification commands ran with what outcome.
Do not append ongoing session logs or raw conversation transcripts to permanent repository instruction files (like `AGENTS.md`).
Keep instructions focused on lasting architecture and workflows.
