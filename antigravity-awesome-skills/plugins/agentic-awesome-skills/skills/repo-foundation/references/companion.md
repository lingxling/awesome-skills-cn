# Companion Coordination (`repo-native-refactor`)

Read this when a meaningful checkpoint is done and you consider one cleanup pass.

- **Complementary roles:** Foundation builds, implements, and adapts; Refactor audits, tightens prose, removes residue, and aligns conventions within scope. Foundation does not reimplement refactor's taxonomy or risk bands; Refactor does not revert intentional, requested behavioral changes.
- **Discovery and fallback:** Locate companion through host-supported discovery only; do not hardcode paths, download, or assume mentioning the name triggers execution. Foundation operates fully without companion. Mention its absence only when that leaves a requested review incomplete. Same-agent self-review is not independent review.
- **Invocation timing:** Use a pass when the user requests review or a substantial contract, ownership, or semantic change warrants a scoped audit. Skip automatic passes for lightweight fixes unless concrete unresolved concerns warrant one; an explicit review request still applies.
- **Minimal handoff contract:** Transfer objective/scope/intentional changes, baseline & user changes, contracts & precedents, check status & limitations from existing context without creating handoff files.
- **Post-cleanup and loop limits:** Rerun affected checks on final code state after refactor edits. Perform at most one refactor pass per checkpoint by default; iterate only on concrete findings or failing checks. If a product decision is missing, ask the user; do not guess or unilaterally redesign.
