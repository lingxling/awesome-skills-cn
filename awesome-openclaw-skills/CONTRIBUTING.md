# Contributing to Awesome OpenClaw Skills

A curated list of skills for OpenClaw. We organize links to skills published on [ClawHub](https://clawhub.ai), OpenClaw's public skills registry.

> This repository is a curated list of links — nothing more. Every skill listed here **must already be published** on [ClawHub](https://clawhub.ai). If your skill is not there, we cannot accept it here. Publish your skill to ClawHub first, then come back and submit a PR to add a link.

## Adding a Skill

### Entry Format

Add your skill to the end of the relevant category in `README.md`:

```markdown
- [skill-name](https://clawhub.ai/author/skill-name) - Short description of what it does.
```

If an author has multiple skills in the same area, please don't add them one by one. Instead, link to the most representative skill and write a general description. This keeps the list clean and avoids unnecessary clutter.

### Where to Add

- Find the matching category in `README.md` and add your entry at the end of that section.
- If no existing category fits, add to the closest match or suggest a new category in your PR description.

### Requirements

- **Skill must already be published on [ClawHub](https://clawhub.ai), OpenClaw's public skills registry.** We do not accept skills hosted elsewhere — no personal repos, no gists, no external links. If it's not on ClawHub, it doesn't belong here.
- **The skill's tests on ClawHub must be passing**, and its security status must be clean (not flagged as suspicious).
- Has documentation (SKILL.md)
- Description must be concise — 10 words or fewer
- Skill must have real community usage. We focus on community-adopted, proven skills published by development teams and proven in real-world usage. Brand new skills are not accepted — give your skill time to mature and gain users before submitting
- No crypto, blockchain, DeFi, or finance-related skills for now

### PR Description

Include the ClawHub link for your skill in the PR description, for example:
- `https://clawhub.ai/steipete/slack`

### PR Title

`Add skill: author/skill-name`

## Updating an Existing Entry

- Fix broken links, typos, or outdated descriptions via PR
- If a skill has been removed or deprecated, open an issue or submit a PR to remove it

## Security Policy

We only include skills whose security status on [ClawHub](https://www.clawhub.ai/) is **not flagged as suspicious**. Skills that are marked as suspicious on ClawHub will not be accepted into this list.

If you believe a skill currently in this list has a security concern or should be flagged, please [open an issue](https://github.com/VoltAgent/awesome-clawdbot-skills/issues) so we can review and remove it.

## Important

- This repository curates links only. Each skill lives on ClawHub, OpenClaw's public skills registry.
- Skill entries link to the skill's ClawHub listing at `https://clawhub.ai/author/skill-name`. Share that same ClawHub page in your PR so we can verify it is published.
- **Do not submit links pointing to `https://clawskills.sh/` URLs.** Always use the ClawHub link (`https://clawhub.ai/author/skill-name`). The clawskills.sh listings are managed and deployed by us separately — you do not need to add anything there.
- Verify your links work before submitting.
- We review all submissions and may decline skills that don't meet the quality bar.
- Do not submit duplicate skills that serve the same purpose as an existing entry.

## Help

- Check existing [issues](https://github.com/VoltAgent/awesome-openclaw-skills/issues) and PRs first
- Open a new issue for questions
- Visit the skill's SKILL.md for skill-specific help
