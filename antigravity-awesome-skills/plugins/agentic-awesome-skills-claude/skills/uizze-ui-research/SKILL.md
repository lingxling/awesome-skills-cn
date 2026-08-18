---
name: uizze-ui-research
description: "Use when building or reviewing web and iOS UI and you need real references from the free UIZZE public catalog, a structured design contract, a consent-gated rendered HTML/CSS preview, or a hard pre-ship finish gate."
category: design
risk: safe
source: https://github.com/uizze/uizze/tree/main/skills/anti-ui-slop
source_repo: uizze/uizze
source_type: official
license: MIT
license_source: https://github.com/uizze/uizze/blob/main/LICENSE
date_added: "2026-07-12"
author: UIZZE
tags: [ui-design, ui-research, mcp, design-contracts, agent-workflows]
tools: [claude, cursor, codex, copilot, antigravity, lovable]
---

# UIZZE UI Research

## Overview

Use [UIZZE](https://uizze.com) to give coding agents real product-UI context before implementation rather than relying on a generic styling prompt. The public catalog supports a free manual workflow without an account. The hosted preview provides a bounded rendered HTML/CSS check, while the full UIZZE MCP requires an authorized connection for reference search and broader review workflows.

This skill turns UI research into an explicit workflow: retrieve relevant references, translate transferable patterns into a design contract, implement within the current project's system, and run the available validation or critique gates.

## When to Use This Skill

- You are designing a new product screen, flow, or component for web or iOS.
- You need real interface references before implementing an AI-generated UI.
- You are reviewing an implementation against explicit design constraints.
- You need to reduce generic or repetitive UI by grounding work in observed product patterns.

## How It Works

### Step 1: Confirm product scope and access mode

Identify the screen's primary user, job, action, existing design system, real content or data, and required loading, empty, error, success, and permission states. Use the free public catalog for manual research by default. If UIZZE MCP is already configured, use only the tools authorized for the task. If browsing is unavailable, ask the user for two or three relevant UIZZE links or screenshots. Do not block the manual workflow, bypass access controls, expose credentials, or claim that a manual review came from MCP.

### Step 2: Retrieve relevant visual context

Find the smallest useful set of screens, flows, components, or elements that match the product task. Focus on transferable patterns such as hierarchy, navigation, interaction states, spacing, density, and responsive behavior. Distinguish observed evidence from assumptions and record whether each finding came from manual browsing, the free preview, or the full MCP.

### Step 3: Make constraints explicit

Write a short design contract that names the screen job, content hierarchy, primary action, allowed project components and tokens, required states, responsive behavior, product-specific decisions, forbidden generic patterns, and verification criteria. Adapt patterns to the existing project design system instead of treating any reference as a visual template.

### Step 4: Implement within the product

Build with the repository's existing components and tokens. Preserve platform conventions and make the interface specific to the product's content and workflow rather than adding decorative cards, badges, gradients, or motion by default.

### Step 5: Run a hard finish gate

Inspect the rendered result when the environment supports it, use an available UIZZE validation, audit, or critique workflow only when authorized, and reject completion if the hierarchy, interaction outcomes, required states, design-system fit, or product-specific decisions are missing. Name each blocking issue, fix it, and rerun the gate plus the project's normal tests. Never claim a rendered or MCP-backed check that was not actually performed.

## Examples

### Research an iOS onboarding flow

```text
Use UIZZE to research real iOS onboarding flows for a subscription product. Identify transferable patterns for progressive disclosure and permission timing, turn them into a concise design contract, then propose an implementation that fits this app's existing design system.
```

### Review a web settings screen

```text
Use UIZZE to inspect relevant real product settings screens, audit this implementation against a design contract for hierarchy, form states, and navigation, then list the concrete changes needed before release.
```

## Best Practices

- ✅ Start with the smallest relevant set of references rather than collecting a broad gallery.
- ✅ Separate observed patterns from the current project's brand and component rules.
- ✅ Use validation findings as implementation feedback, not as permission to copy an interface.
- ❌ Do not reproduce another product's brand, proprietary copy, assets, or exact layout.
- ❌ Do not commit agent tokens, include them in prompts, or place them in client-side code.

## Security & Safety Notes

- Keep any full-connection credential in local agent configuration or a supported environment variable only; never commit it, paste it into prompts, or include it in client-side code.
- Hosted MCP workflows require authorized access; the free catalog and preview do not grant permission to use full workflows.
- Treat returned references as research context, not reusable visual assets.

## Common Pitfalls

- **Problem:** Treating a reference as a design to clone.
  **Solution:** Extract the interaction or hierarchy pattern, then implement it using the target project's own design system and content.
- **Problem:** Starting implementation before the agent has relevant UI context.
  **Solution:** Search for the smallest useful set of matching screens or flows first, then define constraints before coding.
- **Problem:** Exposing an agent token in a repository or chat transcript.
  **Solution:** Store credentials only in supported local configuration or environment variables and rotate a token if it is exposed.

## Related Skills

- `@stitch-ui-design` - Use when generating or iterating UI concepts in Google Stitch.

## Limitations

- This skill does not replace product-specific user research, accessibility review, project tests, or human design judgment.
- It cannot make a hosted UIZZE MCP workflow available without a valid authorized connection.
- Stop and ask for clarification if the product goal, existing design system, or access boundaries are missing.
