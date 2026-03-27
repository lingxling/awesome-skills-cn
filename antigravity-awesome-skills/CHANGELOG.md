# Changelog

All notable changes to the **Antigravity Awesome Skills** collection are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [9.0.0] - 2026-03-27 - "Claude Code and Codex Plugin Release"

> Full release for the installable skill library, now with first-class plugin distributions for Claude Code and Codex plus the normal GitHub Release publication flow.

Start here:

- Install: `npx antigravity-awesome-skills`
- Plugin explainer: [docs/users/plugins.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/plugins.md)
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release makes the new plugin distribution model a user-facing feature. Claude Code now has a formal root marketplace plugin plus generated bundle plugins, and Codex now ships the equivalent repo-local root plugin plus generated bundle plugins. The release also consolidates plugin documentation into a canonical user guide, aligns onboarding docs around the difference between the full repository and the plugin-safe subset, and packages the latest merge batch on `main`.

## New

- **Claude Code plugin distribution** - formalized the root `.claude-plugin` marketplace entry plus generated bundle plugins as a first-class install path.
- **Codex plugin distribution** - formalized the root Codex plugin metadata in `.agents/plugins/marketplace.json` and `plugins/antigravity-awesome-skills/.codex-plugin/plugin.json`, alongside generated bundle plugins.
- **Canonical plugin documentation** - added `docs/users/plugins.md` to explain plugin-safe filtering, root plugin vs bundle plugins, and when to prefer plugins over the full library install.
- **akf-trust-metadata** - merged PR #406, adding the new `akf-trust-metadata` skill to the repository.

## Improvements

- **Onboarding alignment** - updated `README.md`, `docs/users/getting-started.md`, `docs/users/faq.md`, `docs/users/claude-code-skills.md`, `docs/users/codex-cli-skills.md`, `docs/users/bundles.md`, and `docs/users/usage.md` so the plugin story is explained consistently.
- **Community discovery** - merged PR #407 to add the CoinPaprika & DexPaprika listing to the community-contributed section of the README.
- **Maintainer release batch** - merged both open PRs through the documented GitHub squash flow, then packaged the resulting `main` branch as a full release instead of a tag-only cut.

## Who should care

- **Claude Code users** now have a cleaner choice between full-library install, root marketplace plugin, and smaller bundle plugins.
- **Codex users** now get the same plugin distribution model instead of relying only on direct `.codex/skills/` installs.
- **Maintainers and team leads** can onboard people with plugin-safe starter surfaces while keeping the full repository as the broader source of truth.

## Credits

- **[@CryptoDoppio](https://github.com/CryptoDoppio)** for the new `akf-trust-metadata` skill in PR #406
- **[@coinpaprika](https://github.com/coinpaprika)** for adding the CoinPaprika & DexPaprika community listing in PR #407

## [8.10.0] - 2026-03-26 - "Discovery Boost for Social, MCP, and Ops"

> Installable skill library update for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, Windsurf, Cline, and related AI coding assistants.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release improves discovery and day-to-day usefulness for Claude Code, Cursor, Codex CLI, Windsurf, Cline, and similar agent workflows. It adds two new installable skills for X/Twitter extraction and MCP server evaluation, brings in two more community skill collections for study automation and HubSpot CRM operations, and refreshes the registry/docs surface to `1,328+` skills.

## New Skills

- **adhx** - fetch X/Twitter and ADHX links as clean LLM-friendly JSON with article content, author data, and engagement metrics (PR #396).
- **clarvia-aeo-check** - score MCP servers, APIs, and CLIs for agent-readiness before installation (PR #402).

## Improvements

- **Community discovery**: added `Tutor Skills` to the Community Contributed Skills list for Obsidian study-vault generation and interactive quiz-based learning from PDFs, docs, and codebases (PR #400).
- **CRM operations coverage**: added `HubSpot Admin Skills` to the Community Contributed Skills list, surfacing 32 Claude Code skills for auditing, cleaning, enriching, and automating HubSpot CRM workflows (PR #403).
- **Registry sync**: merged the batch via GitHub squash flow, refreshed generated artifacts, and kept `main` aligned with the current `1,328+` skill catalog.

## Who should care

- **Claude Code, Cursor, Codex CLI, Windsurf, and Cline users** get a new social-reading skill plus a practical pre-install check for MCP and tool selection workflows.
- **Students, educators, and knowledge-workflow builders** get easier discovery of the Tutor Skills community collection for turning source material into interactive study vaults.
- **RevOps, marketing ops, and HubSpot-heavy teams** get a clearer path to the HubSpot Admin Skills collection for CRM audits, cleanup, enrichment, and automation playbooks.

## Credits

- **[@conspirafi](https://github.com/conspirafi)** for the new `adhx` skill in PR #396
- **[@digitamaz](https://github.com/digitamaz)** for the new `clarvia-aeo-check` skill in PR #402
- **[@RoundTable02](https://github.com/RoundTable02)** for adding `Tutor Skills` to the community listings in PR #400
- **[@TomGranot](https://github.com/TomGranot)** for adding `HubSpot Admin Skills` to the community listings in PR #403

Upgrade now: `git pull origin main` to fetch the latest skills.

## [8.9.0] - 2026-03-25 - "Apple Workflow Expansion and Data Platform Additions"

> Installable skill library update for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and related AI coding assistants.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release combines a curated import from `Dimillian/Skills` with two merged community pull requests on `main`. It expands Apple-platform workflows, GitHub/refactor guidance, and SwiftUI performance coverage, adds a new Snowflake engineering skill, updates WordPress skills for 7.0, and refreshes the registry/docs surface to `1,326+` indexed skills.

## New Skills

- **app-store-changelog** - turn git history into concise, user-facing App Store release notes.
- **github** - use the `gh` CLI for pull requests, issues, workflow runs, and GitHub API queries.
- **ios-debugger-agent** - debug iOS apps on booted simulators with XcodeBuildMCP.
- **macos-menubar-tuist-app** - build and maintain SwiftUI macOS menubar apps with Tuist-first workflows.
- **macos-spm-app-packaging** - scaffold and package SwiftPM macOS apps without Xcode projects.
- **orchestrate-batch-refactor** - plan large refactors with dependency-aware work packets and parallel analysis.
- **project-skill-audit** - audit a project and recommend the highest-value skills to add or update.
- **react-component-performance** - diagnose slow React components and apply targeted performance fixes.
- **simplify-code** - review diffs for clarity and safe simplifications.
- **snowflake-development** - Snowflake SQL, pipelines, Cortex AI, Snowpark, performance, and security guidance (PR #395).
- **swift-concurrency-expert** - fix actor isolation, `Sendable`, and Swift concurrency issues.
- **swiftui-liquid-glass** - implement and review SwiftUI Liquid Glass APIs correctly.
- **swiftui-performance-audit** - audit SwiftUI runtime performance from code and profiling evidence.
- **swiftui-ui-patterns** - apply proven SwiftUI patterns for navigation, sheets, and async state.
- **swiftui-view-refactor** - refactor SwiftUI views into smaller components with explicit data flow.

## Improvements

- **WordPress 7.0 coverage**: merged PR #394 to expand `wordpress`, `wordpress-plugin-development`, `wordpress-theme-development`, `wordpress-woocommerce-development`, and `wordpress-penetration-testing` with WordPress 7.0 collaboration, AI, admin, and security guidance.
- **Maintainer PR flow**: brought both open PRs into compliance with the source-only policy and PR template requirements before merging them via GitHub squash merge.
- **Registry sync**: refreshed README/catalog metadata, contributor sync, and count-sensitive docs so `main` now reflects `1,326+` indexed skills.
- **Warning-budget preservation**: normalized imported and newly merged skills so the repository remains within the frozen validation budget at `135/135`.

## Who should care

- **Claude Code and Codex CLI users** get a larger set of high-signal workflow skills for GitHub, refactoring, project audits, and Swift/SwiftUI maintenance.
- **Apple-platform developers** get a meaningful jump in coverage across iOS debugging, Swift concurrency, SwiftUI architecture, Liquid Glass, performance, and macOS packaging/menubar patterns.
- **Data and platform engineers** get a new `snowflake-development` skill plus richer WordPress 7.0 documentation for modern content/admin workflows.
- **Maintainers** benefit from a clean post-merge registry state, contributor sync, and release-ready validation posture.

## Credits

- **[Dimillian/Skills](https://github.com/Dimillian/Skills)** for the 14 imported Apple-platform, GitHub, refactoring, and SwiftUI workflow skills that anchor this release
- **[@jamescha-earley](https://github.com/jamescha-earley)** for the new `snowflake-development` skill in PR #395
- **[@munir-abbasi](https://github.com/munir-abbasi)** for the WordPress 7.0 documentation update in PR #394

Upgrade now: `git pull origin main` to fetch the latest skills.

## [8.8.0] - 2026-03-24 - "Review Automation and Research Expansion"

> Installable skill library update for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and related AI coding assistants.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release packages the post-`v8.7.1` merge batch: two new community skills and a maintainer workflow upgrade that expands pull request review into review-and-optimize flows. It also refreshes generated catalog metadata, contributor sync, and tracked web assets so `main` stays aligned at `1,311+` indexed skills.

## New Skills

- **aegisops-ai** - governance-oriented SDLC audits for Linux kernel memory safety, Terraform cost drift, and Kubernetes policy hardening (PR #390)
- **xvary-stock-research** - thesis-driven equity analysis using public SEC EDGAR data, market snapshots, scoring, and comparison playbooks (PR #389)

## Improvements

- **Skill review automation**: Upgraded the PR review workflow to `skill-review-and-optimize` and added `/apply-optimize` automation so maintainers can apply accepted optimization suggestions directly from PR comments (PR #393).
- **Release and registry sync**: Refreshed README/catalog metadata, contributor sync, and tracked web assets after the merge batch so release artifacts and docs stay aligned with the current registry state.

## Who should care

- **Claude Code and Cursor users** get two new high-leverage skills for governance audits and public-market research workflows.
- **Codex CLI and Gemini CLI users** benefit from the same new skills plus richer PR review automation when contributing `SKILL.md` changes back to the repository.
- **Maintainers** get a faster path from automated review comments to applied PR optimizations without leaving GitHub.

## Credits

- **[@Champbreed](https://github.com/Champbreed)** for the new `aegisops-ai` skill in PR #390
- **[@SenSei2121](https://github.com/SenSei2121)** for the new `xvary-stock-research` skill in PR #389
- **[@fernandezbaptiste](https://github.com/fernandezbaptiste)** for the review workflow upgrade in PR #393

Upgrade now: `git pull origin main` to fetch the latest skills.

## [8.7.1] - 2026-03-23 - "Release Pipeline Repair"

> Patch release to restore npm publication after the `v8.7.0` GitHub Release failed before reaching the npm registry.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This patch release keeps the `8.7.0` skill/library content intact and fixes the release pipeline so npm publication works end-to-end again. The root cause was that the publish workflow only installed root dependencies before building `apps/web-app`, leaving the web app without its own `node_modules` in CI.

## Improvements

- **npm publish repair**: Updated the publish workflow to install `apps/web-app` dependencies before the web build, matching the working GitHub Pages workflow and preventing the missing-React/missing-Vite TypeScript cascade seen in CI.
- **Release verification hardening**: Added deterministic web-app installation to the maintainer release suite so `release:preflight` and `release:prepare` now catch this class of failure before a GitHub Release is published.
- **Deterministic installs**: Switched the shared `app:install` script to `npm ci` so local and CI web-app installs use the same locked dependency graph.

## Who should care

- **Maintainers** can cut releases again without the publish workflow failing during the web-app build.
- **npm users** can finally receive the `8.7.x` catalog and skill updates through the package registry instead of being stuck on `8.4.0`.
- **Web-app contributors** get a cleaner release contract where CI explicitly prepares the frontend before building it.

## [8.7.0] - 2026-03-23 - "Reference Recovery and Release Reliability"

> Installable skill library update for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and related AI coding assistants.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release packages the maintainer sweep after `v8.6.0`: restored missing C++ reference material, added three new community skills plus the maintainer-integrated `jobgpt` skill, and fixed the Jetski lazy-loader example so release validation no longer fails on a raw TypeScript import.

## New Skills

- **moyu** - anti-over-engineering guardrails for AI coding agents that need to stay narrowly scoped and prefer the smallest viable change (PR #384)
- **windows-shell-reliability** - practical Windows PowerShell and CMD guidance for encoding, quoting, logging, and detached process launches (PR #386)
- **jobgpt** - JobGPT MCP integration for job search automation, resume generation, application tracking, salary insights, and recruiter outreach (local maintainer integration from PR #388)

## Improvements

- **cpp-pro restoration**: Restored the missing `cpp-pro` nested reference guides and implementation playbook so the skill's documented deep links work again (PR #383, issue #382).
- **Release reliability**: Converted the Jetski Gemini loader example from `loader.ts` to a directly importable `loader.mjs`, updated repo references, and restored green local test coverage for the release pipeline.
- **Registry sync**: Refreshed `README.md`, `CATALOG.md`, `skills_index.json`, `data/catalog.json`, `data/bundles.json`, contributors, and tracked web assets so `main` now reflects `1,309+` indexed skills.
- **Metadata hardening**: Brought the merged `moyu` skill back within the frozen validation warning budget by adding explicit metadata and a `When to Use` section.

## Who should care

- **Claude Code and Cursor users** get four new or newly repaired skills, including scope-control guidance, better Windows shell reliability tips, and restored `cpp-pro` deep-dive references.
- **Codex CLI and Gemini CLI users** benefit from the same skill additions plus a working Jetski lazy-loader example that can now be imported directly in Node-based host setups.
- **Maintainers** get a release path that is green again end-to-end, with generated registry artifacts and contributor data re-synced on `main`.

## Credits

- **[@Champbreed](https://github.com/Champbreed)** for restoring the `cpp-pro` references in PR #383
- **[@uucz](https://github.com/uucz)** for the new `moyu` skill in PR #384
- **[@terryspitz](https://github.com/terryspitz)** for the new `windows-shell-reliability` skill in PR #386
- **[@captainjackrana](https://github.com/captainjackrana)** for the original `jobgpt` contribution in PR #388

Upgrade now: `git pull origin main` to fetch the latest skills.

## [8.6.0] - 2026-03-22 - "Targeted Activation and Catalog Cleanup"

> Installable skill library update for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and related AI coding assistants.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release packages the maintainer sweep after `v8.5.0`: the new `gdb-cli` community skill, removal of the stale in-repo `goldrush-api` copy, and a cross-platform recovery path for Antigravity users who hit truncation or context overload with too many active skills.

## New Skills

- **gdb-cli** - AI-assisted GDB debugging for core dumps, live process attach, crash triage, and deadlock analysis with source correlation (PR #375, closes #374)

## Improvements

- **Antigravity overload recovery**: Added `scripts/activate-skills.sh`, a matching installer hint, and new cross-platform user docs so Linux/macOS users can archive the full library and activate only the bundles or skill ids they need in the live Antigravity directory (issue #381).
- **Windows/Linux/macOS troubleshooting**: Expanded the recovery guidance with a shared overload guide plus clearer README, FAQ, and getting-started links for truncation and context-limit failures.
- **Registry cleanup**: Removed the stale in-repo `goldrush-api` mirror, regenerated bundle/catalog artifacts, and refreshed tracked web assets so canonical references no longer point at deleted content (PR #379).
- **Maintainer sync**: Refreshed `README.md`, `CATALOG.md`, `skills_index.json`, `data/catalog.json`, `data/bundles.json`, contributors, and sitemap output after the PR merge batch so `main` stays release-ready.

## Who should care

- **Antigravity users** get a new activation flow for large repositories and a clearer recovery path when too many active skills trigger truncation-style failures.
- **Claude Code and Cursor users** benefit from the new `gdb-cli` skill for C/C++ debugging and the cleaned-up catalog/docs surfaces.
- **Codex CLI users** benefit from the same new debugging skill plus maintainer-driven registry cleanup that keeps generated artifacts and references aligned.
- **Gemini CLI users** benefit from the updated troubleshooting docs and the removal of stale catalog references in shared bundle metadata.

## Credits

- **[@Cerdore](https://github.com/Cerdore)** for the new `gdb-cli` skill in PR #375
- **[@JayeHarrill](https://github.com/JayeHarrill)** for removing the stale `goldrush-api` copy in PR #379

Upgrade now: `git pull origin main` to fetch the latest skills.

## [8.5.0] - 2026-03-21 - "Installer Safety and Maintainer Automation"

> Installable skill library update for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and related AI coding assistants.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release captures everything that landed after `v8.4.0`: a safety fix for the installer migration path, two new in-repo bdistill skills, broader maintainer automation for metadata/release hygiene, refreshed generated artifacts for the `1,306+` skill catalog, and a new README community section for five OpenClaw skills.

## New Skills

- **bdistill-behavioral-xray** - self-probe an AI model across refusal, reasoning, formatting, grounding, persona, and tool-use dimensions, then generate a visual HTML report (PR #366)
- **bdistill-knowledge-extraction** - extract structured domain knowledge in-session or from local Ollama models into searchable/exportable reference datasets (PR #366)

## Improvements

- **Installer migration safety**: Replaced the destructive legacy migration path in `tools/bin/install.js` with a safety-backup flow so rerunning installs no longer wipes unrelated user skills from the target directory (PR #368, fixes issue #367).
- **Catalog growth and generated sync**: Imported the external marketing, SEO, Obsidian, and Anthropic-adjacent maintainer batch, then refreshed `README.md`, `CATALOG.md`, `skills_index.json`, `data/catalog.json`, bundles, and tracked web assets so `main` now reflects `1,306+` indexed skills.
- **Maintainer automation**: Added docs/package metadata sync, GitHub About sync, contributor sync, release-state sync, repo-state audits, and a frozen validation warning budget so maintainers can keep release artifacts and repo claims aligned with less manual drift.
- **Security and workflow hardening**: Tightened skill tooling file handling, clarified install/PR guidance, and kept CI/release automation aligned with the active source-only PR policy and repo hygiene workflows.
- **Community discovery**: Added a README community section linking five OpenClaw/Claude Code skills from FullStackCrew so users can discover adjacent external tooling from the main repository landing page (PR #370).

## Who should care

- **Claude Code users** get a safer installer migration path and two new bdistill skills for model behavior analysis and knowledge extraction.
- **Cursor users** benefit from the same new skills plus the refreshed docs/catalog metadata that improve browsing and install guidance.
- **Codex CLI users** benefit from the maintainer automation and security hardening that keep registry artifacts, docs, and release metadata in sync.
- **Gemini CLI users** benefit from the synced user docs, updated bundles/workflows metadata, and the safer shared installer maintenance path.

## Credits

- **[@Champbreed](https://github.com/Champbreed)** for the installer migration safety fix in PR #368
- **[@FrancyJGLisboa](https://github.com/FrancyJGLisboa)** for the new `bdistill-behavioral-xray` and `bdistill-knowledge-extraction` skills in PR #366
- **[@fullstackcrew-alpha](https://github.com/fullstackcrew-alpha)** for the OpenClaw community discovery links added in PR #370

Upgrade now: `git pull origin main` to fetch the latest skills.

## [8.4.0] - 2026-03-20 - "Discovery, Metadata, and Release Hardening"

> Installable skill library update for Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity, and related AI coding assistants.

Start here:

- Install: `npx antigravity-awesome-skills`
- Choose your tool: [README -> Choose Your Tool](https://github.com/sickn33/antigravity-awesome-skills#choose-your-tool)
- Best skills by tool: [README -> Best Skills By Tool](https://github.com/sickn33/antigravity-awesome-skills#best-skills-by-tool)
- Bundles: [docs/users/bundles.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/bundles.md)
- Workflows: [docs/users/workflows.md](https://github.com/sickn33/antigravity-awesome-skills/blob/main/docs/users/workflows.md)

This release packages everything that landed after `v8.3.0`: new discovery and SEO surfaces for the catalog, GitHub Pages/web-app reliability fixes, metadata and index curation across the 1,273-skill registry, maintainer release/support polish, and the final merge sweep for PRs #363, #362, and #360.

## New Skills

- **None in this release** - `8.4.0` is a discovery, maintenance, and release-hardening cut rather than a new in-repo skill drop.

## Improvements

- **Catalog discovery and SEO**: Added repo growth discovery pages, finalized the web-app SEO layer for catalog routes, hardened JSON-LD/prerender behavior, expanded the home skills viewport, and improved GitHub Pages/base-path fetch fallbacks so the public catalog is more discoverable and stable.
- **Registry curation**: Expanded curated and uncategorized category coverage, normalized legacy catalog categories, improved safe-skill categorization, and refreshed generated starter packs/bundles to better organize the 1,273-skill library.
- **Metadata quality sweep**: Backfilled missing risk/source metadata, repaired actionable skill descriptions, and merged the `gha-security-review` metadata/usage cleanup so repository validation and review prompts stay more consistent.
- **Infrastructure hardening**: Merged PR #363 to move CI intake to `tools/scripts/pr_preflight.cjs`, localize ESM handling for the Jetski Gemini loader docs, and keep the security/test pipeline green without breaking CommonJS entrypoints.
- **Credits and repo polish**: Added `privacy-mask` to README credits, added the X/community reference update, refreshed the star-history/support surfaces, and kept release-facing onboarding/docs aligned with the current catalog state.

## Who should care

- **Claude Code users** get a more discoverable catalog, cleaner metadata, and improved release/maintenance hygiene around skill quality and source attribution.
- **Cursor users** benefit from the same catalog-route SEO and GitHub Pages web-app fixes when browsing skills through the published site or mirrored install flows.
- **Codex CLI users** benefit from the infrastructure hardening in PR #363 and the continued metadata cleanup that improves routing and maintenance behavior.
- **Gemini CLI users** benefit from the Jetski Gemini loader hardening and the broader catalog/index curation that makes tool-specific discovery easier.

## Credits

- **[@Champbreed](https://github.com/Champbreed)** for the infrastructure hardening in PR #363 and the `gha-security-review` metadata/usage cleanup in PR #362
- **[@fullstackcrew-alpha](https://github.com/fullstackcrew-alpha)** for the `privacy-mask` source attribution added in PR #360

Upgrade now: `git pull origin main` to fetch the latest skills.

## [8.3.0] - 2026-03-19 - "Activation and Skill Expansion"

> **Focused follow-up release for post-`v8.2.0` reliability, metadata, and marketplace improvements**

This release closes the post-`v8.2.0` maintainer batch and includes the merged `landing-page-generator` skill (#341), activation/security hardening, and metadata updates from late-cycle contributions.

## 🚀 New Skills

- **landing-page-generator** — high-converting landing-page and campaign copy templates for product launches and marketing work (PR #341)
- **maxia-ai-to-ai** — MAXIA AI-to-AI marketplace interaction guidance and onboarding patterns (PR #359)

## 📦 Improvements

- **Activation reliability**: Improved activation metadata loading paths and bundle startup behavior to reduce overflow/truncation behavior in local and plugin contexts (PR #358, #359).
- **Metadata repair batch**: Fixed metadata consistency in `agentic-auditor` and `advanced-evaluation` to align risk/quality labels and schema validation (PR #353, #352).
- **Bundle and security maintenance**: Refined full-bundle resolution and included follow-up CI/security cleanup to stabilize post-merge behavior.

## 👥 Credits

- **[@halith-smh](https://github.com/halith-smh)** for `landing-page-generator` in PR #341
- **[@Champbreed](https://github.com/Champbreed)** for metadata fixes in PR #352 and PR #353 (`advanced-evaluation`, `agentic-auditor`)
- **[@AssassinMaeve](https://github.com/AssassinMaeve)** for `Activation skills` in PR #358
- **[@majorelalexis-stack](https://github.com/majorelalexis-stack)** for `MAXIA AI-to-AI` updates in PR #359

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [8.2.0] - 2026-03-18 - "Community Skill Expansion and Plugin Repair"

> **Added six community skills, repaired Claude marketplace metadata, and closed the 2026-03-18 maintainer sweep with refreshed release docs**

This release captures the maintainer pass completed after `v8.1.0`. It adds six new community skills for Astro, Hono, SvelteKit, PydanticAI, blockchain data access, and GitHub repository cleanup; fixes malformed markdown in `browser-extension-builder`; repairs missing metadata labels in legacy skills; credits an additional upstream skills source; and corrects the Claude Code marketplace plugin manifest so installs remain schema-valid.

## New Skills

- **astro** — Astro implementation guidance for content sites, islands architecture, routing, and performance patterns (PR #336)
- **hono** — Hono web framework patterns for APIs, middleware, validation, and edge/server runtimes (PR #336)
- **pydantic-ai** — PydanticAI agent design patterns for typed prompts, tool use, and production workflows (PR #336)
- **sveltekit** — SvelteKit full-stack patterns for routing, data loading, forms, and deployment (PR #336)
- **goldrush-api** — GoldRush API usage for blockchain balances, NFTs, transactions, and multi-chain data flows (PR #334)
- **openclaw-github-repo-commander** — GitHub repository audit and cleanup workflows for issues, PRs, labels, and maintenance automation (PR #340)

## Improvements

- **PR maintenance batch**: Merged PRs #333, #336, #338, #343, #340, #334, and #345 via GitHub squash merge after maintainer workflow approval, checklist normalization, and green CI.
- **Skill content repair**: Removed malformed nested code fences from `skills/browser-extension-builder/SKILL.md`, resolving the accepted fix path for issue `#335` and the follow-up report in issue `#339` (PR #338).
- **Metadata hygiene**: Restored missing required frontmatter labels in `skills/skill-anatomy/SKILL.md`, `skills/adapter-patterns/SKILL.md`, and `skills/devcontainer-setup/SKILL.md` (PRs #333 and #343).
- **Claude plugin stability**: Corrected `.claude-plugin/marketplace.json` so the marketplace entry uses `source: "./"` and added a regression test to catch future schema drift, closing issue `#344`.
- **Credits and sources**: Added `Wolfe-Jam/faf-skills` to the README source acknowledgements and refreshed contributor thanks for the merged maintenance batch (PR #345).
- **Release sync**: Updated README release messaging, user onboarding docs, and maintainer walkthroughs so the public docs match the `8.2.0` release path.

## Credits

- **[@suhaibjanjua](https://github.com/suhaibjanjua)** for the metadata fixes in PR #333, the new `astro`, `hono`, `pydantic-ai`, and `sveltekit` skills in PR #336, and the `browser-extension-builder` markdown repair in PR #338
- **[@JayeHarrill](https://github.com/JayeHarrill)** for the new `goldrush-api` skill in PR #334
- **[@wd041216-bit](https://github.com/wd041216-bit)** for the new `openclaw-github-repo-commander` skill in PR #340
- **[@Champbreed](https://github.com/Champbreed)** for the `devcontainer-setup` metadata label repair in PR #343
- **[@Wolfe-Jam](https://github.com/Wolfe-Jam)** for the `faf-skills` source attribution update in PR #345

## Documentation

- Documented the maintainer handling for fork-gated GitHub Actions runs and stale PR metadata in `.github/MAINTENANCE.md`, then aligned the release-facing onboarding docs with the current `8.2.0` sweep.

## [8.1.0] - 2026-03-17 - "PR Maintenance and Release Sync"

> **Merged the active PR queue, added three new community skills, repaired metadata drift, and refreshed release-facing docs for the next tagged cut**

This release completes the post-merge maintainer pass for the six open pull requests that landed after `8.0.0`. It adds new skills for progressive web apps, tRPC full-stack development, and external AI code review; repairs malformed YAML frontmatter in legacy skills; fixes a broken `data-scientist` reference; and refreshes README, contributor acknowledgements, and linked onboarding docs before the `v8.1.0` tag.

## New Skills

- **progressive-web-app** — practical PWA implementation guidance for manifests, service workers, caching, offline support, and installability (PR #324)
- **vibers-code-review** — GitHub-based external human review workflow for AI-generated projects, including setup steps and integration guidance (PR #325)
- **trpc-fullstack** — end-to-end type-safe API development patterns with tRPC across server, client, auth, and Next.js integration (PR #329)

## Improvements

- **PR maintenance batch**: Merged PRs #331, #330, #326, #324, #325, and #329 via GitHub squash merge after maintainer preflight, workflow approval for forked PRs, and green CI.
- **Docs alignment**: Updated `docs/users/getting-started.md`, README release messaging, and release-facing notes so the public docs reflect the current post-merge state.
- **Issue and reference hygiene**: Removed the dead `resources/implementation-playbook.md` reference from `skills/data-scientist/SKILL.md` (PR #331, closes #327) and closed the duplicate truncation report in issue `#328` against the documented fix path in issue `#269`.
- **FAQ polish**: Aligned FAQ risk-label documentation and added `skill-review` troubleshooting guidance for contributors (PR #330).
- **Legacy metadata repair**: Normalized malformed YAML frontmatter across `astropy`, `biopython`, `cirq`, `citation-management`, `fixing-metadata`, `gmail-automation`, `google-calendar-automation`, `google-docs-automation`, `google-drive-automation`, `google-sheets-automation`, `google-slides-automation`, `networkx`, `qiskit`, `seaborn`, `sympy`, and `varlock` (PR #326).
- **Contributor flow hardening**: Repaired `skills/vibers-code-review/SKILL.md` on the contributor branch so the skill met repository validation rules before merge, then reran CI and merged normally (PR #325 maintainer refresh).
- **Registry and release sync**: Refreshed generated registry artifacts, README counts, package metadata, contributor acknowledgements, and release automation inputs on `main` before tagging `v8.1.0`.

## Credits

- **[@suhaibjanjua](https://github.com/suhaibjanjua)** for the `data-scientist` broken-reference fix in PR #331, the FAQ and getting-started docs alignment in PR #330, and the new `trpc-fullstack` skill in PR #329
- **[@BenZinaDaze](https://github.com/BenZinaDaze)** for the YAML frontmatter repair sweep in PR #326
- **[@JaskiratAnand](https://github.com/JaskiratAnand)** for the new `progressive-web-app` skill in PR #324
- **[@marsiandeployer](https://github.com/marsiandeployer)** for the initial `vibers-code-review` contribution in PR #325

## Documentation

- Documented the new `skill-review` GitHub Actions workflow across contributor, maintainer, and README guidance so PR expectations stay aligned with the active CI surface for `SKILL.md` changes.

## [8.0.0] - 2026-03-16 - "Community Merge Sweep"

> **Merged eight maintainer-refreshed community PRs, shipped three new skills plus workflow automation improvements, and synced the repository for the next release train**

This release closes the open PR maintenance batch in one pass. It adds new skills for agent-native CLI work, AI-assisted end-to-end testing, and AI engineering workflows; strengthens the review workflow with a dedicated skill-review check; repairs the `analyze-project` skill content; and ships helper scripts plus documentation for resolving activation/context overload issues on local installs.

## New Skills

- **ai-native-cli** — build agent-friendly CLIs with clearer UX, task flows, and distribution guidance (PR #317)
- **awt-e2e-testing** — AI-powered end-to-end testing patterns and beta workflow guidance (PR #320)
- **ai-engineering-toolkit** — AI engineering workflow kit for production-oriented implementation loops (PR #314)

## Improvements

- **PR maintenance batch**: Merged PRs #321, #318, #317, #320, #314, #319, #305, and #322 via GitHub squash merge after maintainer refresh, checklist normalization, and green CI.
- **Credits & sources**: Added `tsilverberg/webapp-uat` to `README.md` as a credited external source and refreshed the repository star history asset (PRs #321 and #318).
- **Tooling and troubleshooting**: Added `scripts/activate-skills.bat`, `tools/scripts/get-bundle-skills.py`, and related README troubleshooting guidance for activation-script and context-overload recovery (PR #319).
- **Skill quality repairs**: Restored valid YAML frontmatter and cleaned the structure of `skills/analyze-project/SKILL.md`, preserving the substantive workflow improvements from the contribution (PR #305).
- **Review workflow hardening**: Improved `skills/comprehensive-review-pr-enhance/SKILL.md` and added a pinned `skill-review` GitHub Actions workflow for PRs that touch `SKILL.md` files (PR #322).
- **Registry and release sync**: Realigned README/package metadata and generated registry artifacts around the current `1,262+` skill inventory before cutting the release.

## Credits

- **[@tsilverberg](https://github.com/tsilverberg)** for the `webapp-uat` source attribution in PR #321
- **[@Marvin19700118](https://github.com/Marvin19700118)** for the star-history refresh in PR #318
- **[@ChaosRealmsAI](https://github.com/ChaosRealmsAI)** for `ai-native-cli` in PR #317
- **[@ksgisang](https://github.com/ksgisang)** for `awt-e2e-testing` in PR #320
- **[@viliawang-pm](https://github.com/viliawang-pm)** for `ai-engineering-toolkit` in PR #314
- **[@AssassinMaeve](https://github.com/AssassinMaeve)** for the activation-script helpers in PR #319
- **[@Gizzant](https://github.com/Gizzant)** for the `analyze-project` update in PR #305
- **[@fernandezbaptiste](https://github.com/fernandezbaptiste)** for the review workflow enhancement in PR #322

## [7.9.2] - 2026-03-15 - "npm CLI Packaging Fix"

> **Patch release to fix the published npm CLI bundle so `npx antigravity-awesome-skills` resolves its runtime helper modules correctly**

This release fixes a packaging regression in the published npm artifact. Version `7.9.1` shipped `tools/bin/install.js` without the required `tools/lib` runtime helpers, causing `npx antigravity-awesome-skills` to fail with `MODULE_NOT_FOUND` for `../lib/symlink-safety`.

## New Skills

- **None in this release** — `7.9.2` is a focused patch release for the npm installer bundle.

## Improvements

- **npm package contents**: Expanded the published `files` whitelist to ship `tools/lib/*` alongside `tools/bin/*`, restoring the runtime dependency required by the installer entrypoint.
- **Regression coverage**: Added a package-contents test that checks `npm pack --dry-run --json` and asserts the published tarball includes both `tools/bin/install.js` and `tools/lib/symlink-safety.js`.
- **CLI verification**: Verified the extracted packaged entrypoint runs successfully with `--help`, confirming the published layout no longer reproduces the missing-module crash reported in issue `#315`.

## Credits

- **Issue #315 reporter** for isolating the npm packaging regression in the published CLI artifact.

## [7.9.1] - 2026-03-15 - "Security Hardening Follow-up"

> **Follow-up release to 7.9.0: same security batch, additional hardening focused on mutating endpoints, markdown rendering, and doc-risk enforcement**

This release is a companion follow-up to `7.9.0` and applies security controls for the web app runtime, runtime refresh endpoint, and documentation quality gates.

## New Skills

- **None in this release** — this is a follow-up security maintenance release.

## Improvements

- **Endpoint hardening (mutating API)**: The `/api/refresh-skills` endpoint is now protected by strict local-only ingress rules, explicit token support (`SKILLS_REFRESH_TOKEN` when configured), explicit method validation, and explicit host/Origin checks before any state-changing logic runs.
- **Front-end hardening**: Added POST-only sync from UI and removed unsafe HTML passthrough (`rehype-raw`) from `SkillDetail`, reducing the runtime XSS surface.
- **Documentation risk controls**: Added a full-repo `SKILL.md` security scan for dangerous command patterns (`curl|bash`, `wget|sh`, `irm|iex`, obvious command-line token examples), with opt-in comment allowlisting.
- **Security test coverage**: Added dedicated security tests for endpoint authorization/host/token behavior and markdown rendering behavior, and wired docs security checks into the shared test and CI pipeline.
- **Tooling robustness**: Improved YAML date normalization for frontmatter parsing and index generation so unquoted ISO dates remain stable as strings across tooling.

## Credits

- **Internal security hardening pass** covering endpoint, rendering, and docs scanning controls.

## [7.9.0] - 2026-03-15 - "Codex Security Remediation Sweep"

> **Verified and remediated the active security batch on `main`, with triage and fixes delivered thanks to Codex Security with Codex for OSS**

This release is a focused security maintenance cut. We used Codex Security with Codex for OSS as the triage input, verified every reported finding against the current default branch, collapsed duplicates and obsolete reports, then shipped the confirmed fixes in remediation buckets before merging the final set onto `main`.

## New Skills

- **None in this release** — `7.9.0` is intentionally a security and maintenance release.

## Improvements

- **Filesystem trust boundaries**: Hardened path, symlink, and archive extraction handling across setup, install, sync, metadata, normalization, indexing, and local dev serving flows.
- **Auth and integrity defaults**: Disabled shared frontend star writes by default unless explicitly enabled, and restored TLS verification defaults in the `junta-leiloeiros` scrapers with an explicit opt-out for insecure targets.
- **Shell safety**: Removed pipe-to-shell and token-on-command-line guidance from the Apify docs, and fixed the audio transcription example so shell values are no longer interpolated directly into Python source.
- **Robustness fixes**: Rejected non-mapping YAML frontmatter in validation paths, moved local state files out of predictable shared `/tmp` locations, repaired malformed metadata, and removed committed Python bytecode artifacts.
- **Regression coverage**: Added focused JS, Python, and web-app tests that prove the remediations and guard the reported root causes from reappearing.
- **Security triage artifacts**: Added maintainer-facing triage outputs at `docs/maintainers/security-findings-triage-2026-03-15.{md,csv}` documenting all 33 findings, including why each one was still valid, duplicate, or obsolete on `HEAD`.

## Credits

- **Codex Security with Codex for OSS** for surfacing and structuring the security batch that drove this release.

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [7.8.0] - 2026-03-14 - "Marketplace & Merge Sweep"

> **Merged seven community PRs, added Claude Code marketplace manifests, and finished the maintainer sync/release pass**

This release closes the active maintenance batch in one pass. It ships a new Claude Code plugin marketplace entrypoint for the whole repository, merges seven open community pull requests after maintainer preflight, removes stale Windows symlink guidance from the user docs, and refreshes the generated registry artifacts on `main` for a single `7.8.0` cut.

## New Skills

- **analyze-project** — root-cause analyst workflow for full-project diagnosis (PR #297)
- **latex-paper-conversion** — convert academic papers into reusable engineering artifacts (PR #296)
- **k6-load-testing** — k6-based API and performance testing guidance (PR #287)
- **tool-use-guardian** — tool-call reliability wrapper with retries, recovery, and failure classification (PR #298)
- **recallmax** — long-context memory, summarization, and conversation compression for agents (PR #298)

## Improvements

- **Claude Code marketplace support**: Added `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json` so the repository can be installed as a single Claude Code marketplace plugin (PR #302, closes #288).
- **Windows installer/docs alignment**: Removed the stale `core.symlinks=true` / Developer Mode guidance from user docs after the Windows installer cleanup (PR #299, fixes #286, follow-up #281 closed in release).
- **NotebookLM cleanup**: Removed unused `typing.Optional` / `typing.List` imports from `skills/notebooklm/scripts/browser_utils.py` (PR #301, closes #300).
- **README/source maintenance**: Added maintained attribution for external-sourced skills and merged the `uberSKILLS` README addition without generated-file drift (PRs #298 and #293).
- **Batch merge workflow**: Completed a maintainer preflight for PRs #301, #299, #297, #296, #287, #298, and #293, then regenerated `README.md`, `skills_index.json`, `CATALOG.md`, and `data/*.json` once on `main`.
- **Issue hygiene**: Closed #288, #300, #286, and #281 from the shipped fixes; documented existing support for #294 in the release follow-up.

## Credits

- **[@ronanguilloux](https://github.com/ronanguilloux)** for the NotebookLM cleanup in PR #301
- **[@yang1002378395-cmyk](https://github.com/yang1002378395-cmyk)** for the Windows installer cleanup in PR #299
- **[@Gizzant](https://github.com/Gizzant)** for `analyze-project` in PR #297
- **[@MArbeeGit](https://github.com/MArbeeGit)** for `latex-paper-conversion` in PR #296
- **[@kage-art](https://github.com/kage-art)** for `k6-load-testing` in PR #287
- **[@christopherlhammer11-ai](https://github.com/christopherlhammer11-ai)** for `tool-use-guardian` and `recallmax` in PR #298
- **[@hvasconcelos](https://github.com/hvasconcelos)** for the `uberSKILLS` README addition in PR #293

## [7.7.0] - 2026-03-13 - "Merge Friction Reduction"

> **Shipped four maintained PR outcomes, stabilized generated-file CI, and cut release friction for future contributor merges**

This release turns a noisy maintainer workflow into a predictable one. It merges the latest community skill additions, integrates the cleaned `privacy-by-design` contribution under the maintainer exception path, and removes the biggest source of PR churn by making generated registry drift informational on pull requests while keeping `main` self-healing and strict.

## New Skills

- **llm-structured-output** — structured JSON/schema extraction patterns across OpenAI, Anthropic, and Gemini (PR #280)
- **electron-development** — secure Electron architecture, IPC hardening, packaging, signing, and updates (PR #282)
- **privacy-by-design** — privacy-first software design patterns and implementation guidance (PR #283)
- **antigravity-skill-orchestrator** — meta-skill for selecting and coordinating the best skill set for a task (PR #285)

## Improvements

- **CI determinism**: `tools/scripts/update_readme.py` and `tools/scripts/sync_repo_metadata.py` now preserve volatile README sync metadata during normal runs instead of rewriting stars/timestamps and causing PR drift.
- **PR merge flow**: `.github/workflows/ci.yml` now reports generated registry drift as informational on PRs while keeping `main` strict and auto-syncing the final artifact set after merge.
- **Maintainer docs**: Updated `.github/MAINTENANCE.md`, `docs/maintainers/ci-drift-fix.md`, and `docs/maintainers/merging-prs.md` to document the new lower-friction merge procedure.
- **Windows issue triage**: Clarified that issue `#281` remains open as an installer/symlink problem distinct from truncation-loop issue `#274`, closed `#284` against the shipped recovery guidance, and opened follow-up issue `#286`.

## Credits

- **[@sx4im](https://github.com/sx4im)** for `llm-structured-output` (PR #280)
- **[@MatheusCampagnolo](https://github.com/MatheusCampagnolo)** for `electron-development` (PR #282)
- **[@Abdeltoto](https://github.com/Abdeltoto)** for `privacy-by-design` (PR #283)
- **[@wahidzzz](https://github.com/wahidzzz)** for `antigravity-skill-orchestrator` (PR #285)

## [7.6.0] - 2026-03-12 - "Maintenance Sweep"

> **Merged community PRs, documented Windows truncation recovery, and hardened Metasploit setup guidance**

This release finishes a focused maintenance sweep across open pull requests and issues. It merges four community updates, ships the Jetski/Gemini overflow and path-safety documentation from the context overflow fix, adds a Windows recovery guide for truncation crash loops, and removes the non-deterministic Metasploit installer flow from the security skill.

## New Skills

- **acceptance-orchestrator** — acceptance-driven execution orchestration (PR #277)
- **closed-loop-delivery** — delivery workflow with feedback loops (PR #277)
- **create-issue-gate** — issue creation quality gate (PR #277)
- **interview-coach** — interview preparation and coaching (PR #272)

## Improvements

- **PR maintenance**: Merged PRs #277, #272, #275, #278, and #271 using GitHub squash merge so all contributors receive merge credit.
- **Jetski/Gemini loader docs**: Documented `overflowBehavior` handling and `skillsRoot`-confined path validation in the reference loader and integration guide (PR #271).
- **Windows recovery docs**: Added `docs/users/windows-truncation-recovery.md` and linked it from the main user docs for truncation/context crash loops on Windows.
- **Metasploit safety**: Replaced the remote installer pattern in `skills/metasploit-framework/SKILL.md` with an explicit "Metasploit must already be installed" prerequisite, and marked the skill as `risk: offensive` with the required warning.
- **Repo sync**: Refreshed README metadata, generated registry files, and contributor acknowledgements before release.

## Credits

- **[@qcwssss](https://github.com/qcwssss)** for `acceptance-orchestrator`, `closed-loop-delivery`, and `create-issue-gate` (PR #277)
- **[@dbhat93](https://github.com/dbhat93)** for `interview-coach` (PR #272)
- **[@rafsilva85](https://github.com/rafsilva85)** for the credit source addition (PR #275)
- **[@iftikharg786](https://github.com/iftikharg786)** for the star-history update branch that was refreshed and merged as PR #278
- **[@DiggaX](https://github.com/DiggaX)** for the Windows recovery workflow shared in issue #274
- **[@copilot-swe-agent](https://github.com/apps/copilot-swe-agent)** for the Jetski/Gemini overflow loader changes in PR #271

## [7.5.0] - 2026-03-11 - "Socratic Governance"

> **Introducing Truth Engines, Local Inference optimizations, and Advanced Output Formatting**

This release brings major architectural skills for local inferences, cross-jurisdictional legal logic, and advanced document structuring to help your AI agents operate securely and systematically.

## 🚀 New Skills

### ⚖️ [lex](skills/lex/)
**Cross-Jurisdictional Legal Logic Engine**
A truth engine for navigating complex legal contexts across different jurisdictions without hallucinations.

### 🛡️ [skill-check](skills/skill-check/)
**Validation for agentskills.io Specification**
A read-only skill that validates SKILL.md files against the agentskills specification and Anthropic best practices.

### 🔑 [keyword-extractor](skills/keyword-extractor/)
**Extract High-Quality SEO Keywords**
Provides agents with the ability to extract up to 50 high-quality, ranked keywords from any text payload.

### 🧠 [local-llm-expert](skills/local-llm-expert/)
**Mastery over Local Inference & VRAM Optimization**
Authoritative guidance on running, configuring, and optimizing large language models locally on consumer and enterprise hardware.

### ✅ [yes-md](skills/yes-md/)
**AI Governance at the Formatting Layer**
Instructs generative agents on how to navigate complex formatting rules with a focus on governance and output fidelity.

### 📝 [ai-md](skills/ai-md/)
**Convert CLAUDE.md to AI-Native Format**
A sophisticated transformation skill for AI documentation, battle-tested across 4 frontier models.

### 🤔 [explain-like-socrates](skills/explain-like-socrates/)
**Socratic-Style Concept Explanations**
Transforms the agent into a Socratic tutor, engaging users in dialogue to teach complex concepts through questioning.

## 👥 Credits

A huge shoutout to our community contributors for making this release possible:
- **@sx4im** for `local-llm-expert`
- **@sstklen** for `yes-md` and `ai-md`
- **@tejasashinde** for `keyword-extractor` and `explain-like-socrates`
- **@Olga Safonova** for `skill-check`

---


- **pipecat-friday-agent** — Iron Man-inspired tactical voice assistant (F.R.I.D.A.Y.) with Pipecat, Gemini, and OpenAI.

---

## [7.4.1] - 2026-03-10 - "Documentation Consistency & Workflow Fixes"

> **Resolved comprehensive documentation consistency issues and integrated community AI tools.**

This patch release focuses on bringing the entire repository's documentation into strict compliance with the newly established maintenance protocols. It resolves conflicting skill counts, aligns the documentation "trinity", fixes workflow routing paths, and standardizes formats to prevent anchor breakage. It also includes new community skills like the `pipecat-friday-agent` and workflow enhancements.

## 🚀 New Skills

### 🤖 [pipecat-friday-agent](skills/pipecat-friday-agent/)

**Iron Man-inspired tactical voice assistant (F.R.I.D.A.Y.).**
Built with Pipecat, Google Gemini, and OpenAI, providing a blueprint for creating interactive voice-driven agents.

### ⏱️ [progressive-estimation](skills/progressive-estimation/)

**Agentic workflow for progressive task estimation.**
Breaks down complex tasks to improve estimation accuracy and project planning.

### 🎥 [seek-and-analyze-video](skills/seek-and-analyze-video/)

**AI-powered video analysis toolkit.**
Automates seeking and analyzing of video content, extracting key insights and moments.

## 📦 Improvements

- **Documentation Consistency**: Full audit and remediation of `.github/MAINTENANCE.md` rules.
- **TOC Formatting**: Removed emojis from H2 headers in `README.md` to fix broken markdown anchors.
- **Statistics Alignment**: Synced skill counts across `package.json` and `README.md` for accurate representation (1,239+).
- **Workflow Routing**: Added the `design-ddd-core-domain` workflow to required path definitions and copy-paste examples in `skills/antigravity-workflows/SKILL.md`.
- **Validation**: Passed all sync chains including `npm run validate:references`.

## 👥 Credits

A huge shoutout to our community contributors:

- **@Enreign** for `progressive-estimation`
- **@kennyzheng-builds** for `seek-and-analyze-video`

---

## [7.4.0] - 2026-03-10 - "Planning & Dashboards"

> **Blueprint planning skill, Sankhya dashboard best‑practices, and registry sync to 1,236+ skills.**

This release focuses on better multi-session planning and domain dashboards. It adds a Blueprint skill for cold-start construction plans that any coding agent can execute, plus a Sankhya dashboard best-practices skill with SQL/JSP and UI guidance. The registry, catalog, and README counts are synced to 1,236+ skills, and the web app build is verified clean for this version.

## 🚀 New Skills

### 🧱 [blueprint](skills/blueprint/)

**Cold-start construction planning for multi-step projects.**
Generates dependency-aware plans where every step has its own context brief, tasks, rollback, verification, and exit criteria so fresh agents can execute steps independently.

### 📊 [sankhya-dashboard-html-jsp-custom-best-pratices](skills/sankhya-dashboard-html-jsp-custom-best-pratices/)

**Sankhya dashboard structure, SQL/JSP patterns, and UI best practices.**
Documents resilient dashboard patterns, recommended SQL/JSP layout, and UX guidelines for production Sankhya deployments.

## 📦 Improvements

- **Registry Update**: Now tracking **1,236+** skills across the catalog.
- **Docs & Catalog**: `README.md`, `skills_index.json`, `data/catalog.json`, and `CATALOG.md` regenerated and validated for 7.4.0.
- **Web App**: `npm run app:build` run successfully to ensure the skills browser is up to date.

## 👥 Credits

- **@antbotlab** for `blueprint` (PR #259).
- **@Guilherme-ruy** for the Sankhya dashboard skill (PR #258).

---

## [7.2.0] - 2026-03-08 - "Community PR Harvest & Cleanup"

> **Eight PRs merged: 44 broken skills removed, zebbern attribution restored, Chinese docs, new skills (audit-skills, senior-frontend, shadcn, frontend-slides update, pakistan-payments-stack), and explainable auto-categorization.**

This release cleans up the registry (removal of 44 SKILL.md files that contained only "404: Not Found"), restores `author: zebbern` attribution to 29 security skills, and merges community contributions: Simplified Chinese documentation, audit-skills, senior-frontend and shadcn skills, frontend-slides dependencies and formatting, pakistan-payments-stack for Pakistani SaaS payments, and explainable auto-categorization in the index generator. Bundle references were updated to drop missing skills so reference validation passes.

## New Skills

- **audit-skills** — Audit-safe skills (PR #236)
- **senior-frontend** — React, Next.js, TypeScript, Tailwind (PR #233)
- **shadcn** — shadcn/ui ecosystem (PR #233)
- **pakistan-payments-stack** — JazzCash, Easypaisa, PKR billing (PR #228)

## Improvements

- **Registry cleanup**: 44 broken "404: Not Found" skill files removed (PR #240).
- **Attribution**: `author: zebbern` restored for 29 security skills (PR #238).
- **Docs**: frontend-slides updated with missing deps and formatting (PR #234); Simplified Chinese docs added (PR #232).
- **Index**: Explainable auto-categorization in `generate_index.py` (PR #230).
- **Bundles**: `data/bundles.json` updated to remove references to removed or missing skills; `npm run validate:references` passes.
- **Registry**: Now tracking **1,232** skills.

## Credits

- **@munir-abbasi** for Chinese docs (PR #232)
- **@itsmeares** for senior-frontend, shadcn (PR #233), frontend-slides update (PR #234)
- **@zebbern** for security skills attribution (PR #238)
- Contributors behind PRs #228, #230, #236, #240

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [7.1.0] - 2026-03-07 - "PR Harvest & README Integrity"

> **7 new skills merged from the community, README structure restored, and 1,272 skills milestone confirmed.**

This release integrates a fresh batch of community pull requests: a Figma-to-React converter, Stripe payment expert, TanStack Query expert, Vercel AI SDK expert, Uncle Bob Clean Architecture guide, Antigravity premium design skills, and an AI agent toolkit. It also restores the structural integrity of README.md, which had picked up nested conflict markers from the batch-merge process.

## 🚀 New Skills

### 🎨 [figma-to-react](skills/figma-to-react/)

**Convert Figma designs to production-ready React components.**
Automatic conversion with pixel-perfect fidelity, responsive layouts, and Tailwind/CSS Modules support.

> **Try it:** `Use @figma-to-react to turn this Figma component into a React component.`

### 💳 [stripe-expert](skills/stripe-expert/)

**Production-grade Stripe integration guidance.**
Covers one-time payments, subscriptions, webhooks, and tax/compliance patterns.

> **Try it:** `Use @stripe-expert to implement a SaaS subscription with annual billing.`

### ⚡ [tanstack-query-expert](skills/tanstack-query-expert/)

**Advanced data fetching and server state with TanStack Query v5.**
Optimistic updates, infinite queries, and SSR/Next.js integration.

> **Try it:** `Use @tanstack-query-expert to refactor this fetch call with caching and optimistic updates.`

### 🤖 [vercel-ai-sdk-expert](skills/vercel-ai-sdk-expert/)

**Generative UI and tool calling with the Vercel AI SDK.**
Streaming, multi-step tools, and edge deployment patterns.

> **Try it:** `Use @vercel-ai-sdk-expert to add streaming chat with tool calls.`

### 📐 [uncle-bob-craft](skills/uncle-bob-craft/)

**Clean Code, Clean Architecture, and TDD guidance from Uncle Bob's books.**
Code reviews, refactoring, SOLID principles, and design pattern references.

> **Try it:** `Use @uncle-bob-craft to review this class for SRP violations.`

### ✨ [antigravity-premium-design](skills/antigravity-premium-design/)

**Premium UI/UX patterns and motion design for Antigravity IDE.**

> **Try it:** `Use @antigravity-premium-design to redesign this component.`

## 📦 Improvements

- **Registry Update**: Now tracking **1,272** skills.
- **README Integrity**: Removed all nested merge conflict markers introduced during the batch-merge phase; restored original section layout.
- **Stats Sync**: `package.json` description updated to `1,272+`.

## 👥 Credits

A huge shoutout to our community contributors:

- **@GuppyTheCat** for `obsidian-clipper-template-creator` (PR #226)
- **@sraphaz** for `uncle-bob-craft` (PR #225)
- **@ziuus** for `antigravity-premium-design` (PR #224)
- **@sx4im** for `git-hooks-automation` (PR #223), `tanstack-query-expert` (PR #222), `vercel-ai-sdk-expert` (PR #220)
- **@Sayeem3051** for skill filtering utility (PR #219)
- **@AlmogBaku** for `debug-skill` (PR #218)
- **@ProgramadorBrasil** for 52 specialized AI agent skills (PR #217)
- **@shubhamdevx** for web app markdown rendering improvements (PR #213)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [7.0.1] - 2026-03-06 - "Markdown & Wallet Patch"

> **Patch release with web markdown improvements and new wallet skills, plus catalog sync.**

This patch release adds new skills for AI-writing cleanup and multi-chain crypto wallets, while improving how markdown is rendered in the web app. It also syncs the generated catalog and metadata for a clean 7.0.1 state.

## 🚀 New Skills

### ✍️ avoid-ai-writing (skills/avoid-ai-writing/)

**Remove AI-isms from generated prose**
Audits and rewrites content to remove 21 categories of AI writing patterns, using a 43-entry replacement table and a structured four-step audit workflow.

> **Try it:** `Use @avoid-ai-writing to clean up this AI-generated blog post before publishing.`

### 🪙 emblemai-crypto-wallet (skills/emblemai-crypto-wallet/)

**Multi-chain crypto wallet management via EmblemAI**
Manages crypto wallets across 7 blockchains (Solana, Ethereum, Base, BSC, Polygon, Hedera, Bitcoin) for balance checks, swaps, transfers, and portfolio analysis via the EmblemAI Agent Hustle API.

> **Try it:** `Use @emblemai-crypto-wallet to summarize my portfolio and estimate gas costs for a swap.`

## 📦 Improvements

- **Registry Update**: Catalog and bundles regenerated after adding the new skills.
- **Risk Metadata**: `emblemai-crypto-wallet` now uses a `critical` risk level to reflect real-value asset operations.
- **Validation**: Full validation chain and catalog build run successfully for 7.0.1.

## 👥 Credits

- **@conorbronsdon** for `avoid-ai-writing`.
- **@decentraliser** for `emblemai-crypto-wallet`.

## [7.0.0] - 2026-03-06 - "20k Stars Celebration"

> **300+ new skills added to celebrate 20,000 GitHub stars!**

This major release expands our collection to **1,200+ skills** from 35+ community repositories, covering UI/UX, Security, Data Science, Health, Quantum Computing, and more. This is our biggest community-driven update ever!

### 🎉 20k Stars Milestone

Thank you to our incredible community! From 0 to 20,000 stars, this journey has been powered by developers, security researchers, data scientists, and AI enthusiasts worldwide.

## 🚀 New Skill Categories (300+ Skills)

### UI/UX & Frontend (35+ skills)

Complete UI/UX polish toolkit and 3D graphics suite:

- **[baseline-ui](skills/baseline-ui/)**, **[fixing-accessibility](skills/fixing-accessibility/)**, **[fixing-metadata](skills/fixing-metadata/)**, **[fixing-motion-performance](skills/fixing-motion-performance/)** - UI validation and accessibility
- **[swiftui-expert-skill](skills/swiftui-expert-skill/)** - iOS SwiftUI development with 14 reference guides
- **[threejs-fundamentals](skills/threejs-fundamentals/)** through **[threejs-interaction](skills/threejs-interaction/)** - Complete Three.js 3D graphics (10 skills)
- **[expo-ui-swift-ui](skills/expo-ui-swift-ui/)**, **[expo-ui-jetpack-compose](skills/expo-ui-jetpack-compose/)**, **[expo-tailwind-setup](skills/expo-tailwind-setup/)**, **[building-native-ui](skills/building-native-ui/)**, **[expo-api-routes](skills/expo-api-routes/)**, **[expo-dev-client](skills/expo-dev-client/)**, **[expo-cicd-workflows](skills/expo-cicd-workflows/)**, **[native-data-fetching](skills/native-data-fetching/)** - Expo/React Native development
- **[frontend-slides](skills/frontend-slides/)** - HTML presentation creation
- **[makepad-basics](skills/makepad-basics/)** through **[molykit](skills/molykit/)** - Complete Makepad UI Framework (19 skills)
- **[favicon](skills/favicon/)**, **[chat-widget](skills/chat-widget/)** - UI utilities

### Automation & Integration (35+ skills)

Full workflow automation toolkit:

- **[gmail-automation](skills/gmail-automation/)**, **[google-calendar-automation](skills/google-calendar-automation/)**, **[google-docs-automation](skills/google-docs-automation/)**, **[google-sheets-automation](skills/google-sheets-automation/)**, **[google-drive-automation](skills/google-drive-automation/)**, **[google-slides-automation](skills/google-slides-automation/)** - Complete Google Workspace integration
- **[n8n-expression-syntax](skills/n8n-expression-syntax/)**, **[n8n-mcp-tools-expert](skills/n8n-mcp-tools-expert/)**, **[n8n-workflow-patterns](skills/n8n-workflow-patterns/)**, **[n8n-validation-expert](skills/n8n-validation-expert/)**, **[n8n-node-configuration](skills/n8n-node-configuration/)**, **[n8n-code-javascript](skills/n8n-code-javascript/)**, **[n8n-code-python](skills/n8n-code-python/)** - n8n workflow automation (7 skills)
- **[automate-whatsapp](skills/automate-whatsapp/)**, **[integrate-whatsapp](skills/integrate-whatsapp/)**, **[observe-whatsapp](skills/observe-whatsapp/)** - WhatsApp automation
- **[linear](skills/linear/)** - Linear project management integration
- **[rails-upgrade](skills/rails-upgrade/)** - Rails upgrade assistant
- **[commit](skills/commit/)**, **[create-pr](skills/create-pr/)**, **[find-bugs](skills/find-bugs/)**, **[iterate-pr](skills/iterate-pr/)**, **[code-simplifier](skills/code-simplifier/)**, **[skill-scanner](skills/skill-scanner/)**, **[skill-writer](skills/skill-writer/)**, **[pr-writer](skills/pr-writer/)**, **[create-branch](skills/create-branch/)** - Developer workflow automation from Sentry
- **[build](skills/build/)**, **[conductor-setup](skills/conductor-setup/)**, **[issues](skills/issues/)**, **[new-rails-project](skills/new-rails-project/)** - Development project management

### Security & Auditing (40+ skills)

Comprehensive security toolkit from Trail of Bits and community:

- **[semgrep-rule-creator](skills/semgrep-rule-creator/)**, **[semgrep-rule-variant-creator](skills/semgrep-rule-variant-creator/)**, **[static-analysis](skills/static-analysis/)**, **[variant-analysis](skills/variant-analysis/)** - Code security analysis
- **[golang-security-auditor](skills/golang-security-auditor/)**, **[python-security-auditor](skills/python-security-auditor/)**, **[rust-security-auditor](skills/rust-security-auditor/)** - Language-specific security auditing
- **[burpsuite-project-parser](skills/burpsuite-project-parser/)**, **[agentic-actions-auditor](skills/agentic-actions-auditor/)**, **[audit-context-building](skills/audit-context-building/)**, **[proof-of-vulnerability](skills/proof-of-vulnerability/)**, **[yara-authoring](skills/yara-authoring/)** - Security testing tools
- **[ffuf-web-fuzzing](skills/ffuf-web-fuzzing/)** - Web fuzzing with ffuf
- **[security-bluebook-builder](skills/security-bluebook-builder/)** - Security policy documentation
- **[ask-questions-if-underspecified](skills/ask-questions-if-underspecified/)**, **[building-secure-contracts](skills/building-secure-contracts/)**, **[claude-in-chrome-troubleshooting](skills/claude-in-chrome-troubleshooting/)**, **[constant-time-analysis](skills/constant-time-analysis/)**, **[culture-index](skills/culture-index/)**, **[debug-buttercup](skills/debug-buttercup/)**, **[devcontainer-setup](skills/devcontainer-setup/)**, **[differential-review](skills/differential-review/)**, **[dwarf-expert](skills/dwarf-expert/)**, **[grimoire](skills/grimoire/)**, **[it-depends](skills/it-depends/)**, **[monte-carlo-treasury](skills/monte-carlo-treasury/)**, **[monte-carlo-vulnerability-detection](skills/monte-carlo-vulnerability-detection/)**, **[open-source-context](skills/open-source-context/)**, **[operational-guidelines](skills/operational-guidelines/)**, **[osint-evals](skills/osint-evals/)**, **[polyfile](skills/polyfile/)**, **[publish-and-summary](skills/publish-and-summary/)**, **[security-skill-creator](skills/security-skill-creator/)**, **[sharp-edges](skills/sharp-edges/)**, **[skill-improver](skills/skill-improver/)**, **[spec-to-code-compliance](skills/spec-to-code-compliance/)**, **[supply-chain-risk-auditor](skills/supply-chain-risk-auditor/)**, **[testing-handbook-skills](skills/testing-handbook-skills/)**, **[workflow-skill-design](skills/workflow-skill-design/)**, **[zeroize-audit](skills/zeroize-audit/)** - Additional Trail of Bits security skills

### Machine Learning & Data Science (35+ skills)

Complete scientific computing suite:

- **[hugging-face-dataset-viewer](skills/hugging-face-dataset-viewer/)**, **[hugging-face-datasets](skills/hugging-face-datasets/)**, **[hugging-face-evaluation](skills/hugging-face-evaluation/)**, **[hugging-face-model-trainer](skills/hugging-face-model-trainer/)**, **[hugging-face-paper-publisher](skills/hugging-face-paper-publisher/)**, **[hugging-face-tool-builder](skills/hugging-face-tool-builder/)** - HuggingFace ML platform
- **[numpy](skills/numpy/)**, **[pandas](skills/pandas/)**, **[scipy](skills/scipy/)**, **[matplotlib](skills/matplotlib/)**, **[scikit-learn](skills/scikit-learn/)**, **[jupyter-workflow](skills/jupyter-workflow/)** - Data science essentials
- **[biopython](skills/biopython/)**, **[scanpy](skills/scanpy/)**, **[uniprot-database](skills/uniprot-database/)**, **[pubmed-database](skills/pubmed-database/)** - Bioinformatics tools
- **[astropy](skills/astropy/)**, **[citation-management](skills/citation-management/)**, **[data-visualization](skills/data-visualization/)**, **[great-tables](skills/great-tables/)**, **[literature-analysis](skills/literature-analysis/)**, **[networkx](skills/networkx/)**, **[plotly](skills/plotly/)**, **[polars](skills/polars/)**, **[pygraphistry](skills/pygraphistry/)**, **[seaborn](skills/seaborn/)**, **[statsmodels](skills/statsmodels/)**, **[sympy](skills/sympy/)**, **[umap](skills/umap/)** - Scientific computing
- **[alpha-vantage](skills/alpha-vantage/)**, **[quantitative-analysis](skills/quantitative-analysis/)**, **[risk-modeling](skills/risk-modeling/)** - Financial analysis
- **[cirq](skills/cirq/)**, **[qiskit](skills/qiskit/)** - Quantum computing frameworks
- **[research-engineer](skills/research-engineer/)**, **[scientific-writing](skills/scientific-writing/)**, **[paper-analysis](skills/paper-analysis/)** - Academic research

### Health & Wellness (20+ skills)

Comprehensive health management from Claude-Ally-Health:

- **[sleep-analyzer](skills/sleep-analyzer/)**, **[nutrition-analyzer](skills/nutrition-analyzer/)**, **[fitness-analyzer](skills/fitness-analyzer/)** - Core health tracking
- **[ai-analyzer](skills/ai-analyzer/)**, **[emergency-card](skills/emergency-card/)**, **[family-health-analyzer](skills/family-health-analyzer/)**, **[food-database-query](skills/food-database-query/)**, **[goal-analyzer](skills/goal-analyzer/)**, **[health-trend-analyzer](skills/health-trend-analyzer/)**, **[mental-health-analyzer](skills/mental-health-analyzer/)**, **[occupational-health-analyzer](skills/occupational-health-analyzer/)**, **[oral-health-analyzer](skills/oral-health-analyzer/)**, **[rehabilitation-analyzer](skills/rehabilitation-analyzer/)**, **[sexual-health-analyzer](skills/sexual-health-analyzer/)**, **[skin-health-analyzer](skills/skin-health-analyzer/)**, **[tcm-constitution-analyzer](skills/tcm-constitution-analyzer/)**, **[travel-health-analyzer](skills/travel-health-analyzer/)**, **[weightloss-analyzer](skills/weightloss-analyzer/)**, **[wellally-tech](skills/wellally-tech/)** - Specialized health analyzers

### Context Engineering & AI (15+ skills)

Advanced agent patterns from muratcankoylan and community:

- **[context-fundamentals](skills/context-fundamentals/)**, **[context-degradation](skills/context-degradation/)**, **[context-compression](skills/context-compression/)**, **[context-optimization](skills/context-optimization/)**, **[multi-agent-patterns](skills/multi-agent-patterns/)**, **[filesystem-context](skills/filesystem-context/)** - Context engineering patterns
- **[hosted-agents](skills/hosted-agents/)**, **[advanced-evaluation](skills/advanced-evaluation/)**, **[project-development](skills/project-development/)**, **[bdi-mental-states](skills/bdi-mental-states/)** - Advanced agent patterns
- **[agents-md](skills/agents-md/)**, **[blog-writing-guide](skills/blog-writing-guide/)**, **[brand-guidelines](skills/brand-guidelines/)**, **[claude-settings-audit](skills/claude-settings-audit/)** - Sentry workflow skills

### Functional Programming (12+ skills)

Complete fp-ts guide:

- **[fp-pragmatic](skills/fp-pragmatic/)**, **[fp-errors](skills/fp-errors/)**, **[fp-async](skills/fp-async/)**, **[fp-react](skills/fp-react/)**, **[fp-data-transforms](skills/fp-data-transforms/)**, **[fp-backend](skills/fp-backend/)**, **[fp-refactor](skills/fp-refactor/)** - Core functional programming
- **[fp-types-ref](skills/fp-types-ref/)**, **[fp-pipe-ref](skills/fp-pipe-ref/)**, **[fp-option-ref](skills/fp-option-ref/)**, **[fp-either-ref](skills/fp-either-ref/)**, **[fp-taskeither-ref](skills/fp-taskeither-ref/)** - Quick reference guides

### AWS Development (6+ skills)

AWS expertise from zxkane:

- **[aws-agentic-ai](skills/aws-agentic-ai/)**, **[aws-cdk-development](skills/aws-cdk-development/)**, **[aws-common](skills/aws-common/)**, **[aws-cost-ops](skills/aws-cost-ops/)**, **[aws-mcp-setup](skills/aws-mcp-setup/)**, **[aws-serverless-eda](skills/aws-serverless-eda/)**

### Utilities & Developer Tools (10+ skills)

- **[vexor-cli](skills/vexor-cli/)** - Semantic file discovery
- **[clarity-gate](skills/clarity-gate/)** - RAG quality verification
- **[speckit-updater](skills/speckit-updater/)** - SpecKit template updates
- **[varlock](skills/varlock/)** - Secure environment variable management
- **[beautiful-prose](skills/beautiful-prose/)** - Writing style guide
- **[speed](skills/speed/)** - Speed reading tool
- **[vercel-deploy-claimable](skills/vercel-deploy-claimable/)** - Vercel deployment
- **[enhance-prompt](skills/enhance-prompt/)**, **[remotion](skills/remotion/)**, **[stitch-loop](skills/stitch-loop/)** - Google Labs tools
- **[claimable-postgres](skills/claimable-postgres/)** - Neon Postgres

## 📦 Improvements

- **Registry Update**: Now tracking 1,200+ skills (from 900+)
- **New Categories**: Bioinformatics, Quantum Computing, Makepad Framework, Health & Wellness
- **External Repositories**: Skills from 35+ community repositories
- **Validation**: Full validation chain run on all new skills
- **Catalog**: Updated interactive web catalog with all new skills

## 👥 Credits

### Official Team Contributions

- **Vercel Labs**: `vercel-deploy-claimable`
- **Google Labs**: `enhance-prompt`, `remotion`, `stitch-loop`
- **HuggingFace**: `hugging-face-dataset-viewer`, `hugging-face-datasets`, `hugging-face-evaluation`, `hugging-face-model-trainer`, `hugging-face-paper-publisher`, `hugging-face-tool-builder`
- **Expo**: `expo-ui-swift-ui`, `expo-ui-jetpack-compose`, `expo-tailwind-setup`, `building-native-ui`, `expo-api-routes`, `expo-dev-client`, `expo-cicd-workflows`, `native-data-fetching`
- **Sentry**: `agents-md`, `blog-writing-guide`, `brand-guidelines`, `claude-settings-audit`, `code-simplifier`, `commit`, `create-branch`, `create-pr`, `django-access-review`, `django-perf-review`, `find-bugs`, `gh-review-requests`, `gha-security-review`, `iterate-pr`, `pr-writer`, `skill-scanner`, `skill-writer`, `sred-project-organizer`, `sred-work-summary`
- **Trail of Bits**: 40+ security skills including `semgrep-rule-creator`, `static-analysis`, `variant-analysis`, and specialized auditors

### Community Contributors

- **[ibelick](https://github.com/ibelick/ui-skills)**: UI/UX polish skills
- **[expo](https://github.com/expo/skills)**: React Native development skills
- **[sanjay3290](https://github.com/sanjay3290/ai-skills)**: Google Workspace integration
- **[czlonkowski](https://github.com/czlonkowski/n8n-skills)**: n8n automation toolkit
- **[gokapso](https://github.com/gokapso/agent-skills)**: WhatsApp automation
- **[wrsmith108](https://github.com/wrsmith108/linear-claude-skill)**: Linear integration, varlock
- **[robzolkos](https://github.com/robzolkos/skill-rails-upgrade)**: Rails upgrade assistant
- **[scarletkc](https://github.com/scarletkc/vexor)**: Vexor CLI
- **[zarazhangrui](https://github.com/zarazhangrui/frontend-slides)**: HTML presentations
- **[AvdLee](https://github.com/AvdLee/SwiftUI-Agent-Skill)**: SwiftUI expert skill
- **[CloudAI-X](https://github.com/CloudAI-X/threejs-skills)**: Complete Three.js suite
- **[ZhangHanDong](https://github.com/ZhangHanDong/makepad-skills)**: Makepad UI Framework
- **[muratcankoylan](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)**: Context engineering patterns
- **[huifer](https://github.com/huifer/Claude-Ally-Health)**: Health & wellness analyzers
- **[K-Dense-AI](https://github.com/K-Dense-AI/claude-scientific-skills)**: Scientific computing suite
- **[jthack](https://github.com/jthack/ffuf_claude_skill)**: ffuf web fuzzing
- **[NotMyself](https://github.com/NotMyself/claude-win11-speckit-update-skill)**: SpecKit updater
- **[SHADOWPR0](https://github.com/SHADOWPR0/security-bluebook-builder)**: Security bluebook, beautiful-prose
- **[SeanZoR](https://github.com/SeanZoR/claude-speed-reader)**: Speed reading
- **[whatiskadudoing](https://github.com/whatiskadudoing/fp-ts-skills)**: fp-ts functional programming
- **[zxkane](https://github.com/zxkane/aws-skills)**: AWS development skills
- **[Shpigford](https://github.com/Shpigford/skills)**: Developer tools
- **[frmoretto](https://github.com/frmoretto/clarity-gate)**: RAG verification
- **[neondatabase](https://github.com/neondatabase/agent-skills)**: Neon Postgres

### Top Repository Contributors

- [@sck_0](https://github.com/sck_0) - 377 commits
- [@github-actions[bot]](https://github.com/apps/github-actions) - 145 commits
- [@sickn33](https://github.com/sickn33) - 54 commits
- [@Mohammad-Faiz-Cloud-Engineer](https://github.com/Mohammad-Faiz-Cloud-Engineer) - 38 commits
- [@munir-abbasi](https://github.com/munir-abbasi) - 31 commits
- [@zinzied](https://github.com/zinzied) - 21 commits
- ...and 40+ more contributors!

---

## [6.12.0] - 2026-03-06 - "Developer APIs & Management Tools"

> **7 new developer and product management skills plus web-app UI fixes.**

This release introduces payment capabilities for agents via Agent Cards, production-grade Zod validation, comprehensive Product Management frameworks, and a suite of essential developer tools (API builder, bug hunter, performance optimizer). It also includes fixes for unwanted scrollbars in the interactive web app.

## 🚀 New Skills

### 💳 [agent-cards/skill](https://github.com/agent-cards/skill)

**Manage prepaid virtual Visa cards for AI agents.**
Allows AI agents to create cards, complete Stripe checkout, check balances, view credentials, and close cards via MCP.

> **Try it:** `Use agent-cards to create a virtual Visa card with a $50 budget.`

### 🛡️ [zod-validation-expert](skills/zod-validation-expert/)

**Type-safe schema definitions and parsing logic with Zod.**
Production-grade guide covering schema definition, type inference, safe parsing, transformations, and React/Next.js integration.

> **Try it:** `Use zod-validation-expert to create a user registration schema with custom error messages.`

### 📊 [product-manager](skills/product-manager/)

**Senior PM agent with 6 knowledge domains and 30+ frameworks.**
Provides product management expertise including RICE scoring, PRD templates, and 32 SaaS metrics with exact formulas.

> **Try it:** `Draft a PRD for our new authentication feature using the product-manager templates.`

### 🛠️ Developer Essentials (3 skills)

**Essential skills for building, debugging, and optimizing applications.**

- **[api-endpoint-builder](skills/api-endpoint-builder/)**: Builds production-ready REST API endpoints with validation and error handling.
- **[bug-hunter](skills/bug-hunter/)**: Systematically finds and fixes bugs from symptoms to root cause.
- **[performance-optimizer](skills/performance-optimizer/)**: Identifies and fixes performance bottlenecks in code, databases, and APIs.

> **Try it:** `Use api-endpoint-builder to scaffold a secure user login REST endpoint.`

---

## 📦 Improvements

- **Web App Scroll Fixes**: Corrected horizontal and vertical scrollbar overflow issues in the web app UI grid and virtualized lists (PR #208).
- **Registry Update**: Now tracking 1011 skills.

## 👥 Credits

A huge shoutout to our community contributors:

- **@keyserfaty** for `agent-cards`
- **@zinzied** for web-app scroll fixes
- **@sx4im** for `zod-validation-expert`
- **@Digidai** for `product-manager`
- **@Mohammad-Faiz-Cloud-Engineer** for developer essential skills

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [6.11.0] - 2026-03-05 - "Skills Expansion & Docs Polish"

> **28 new skills, web-app performance upgrades, and documentation consistency pass.**

This release adds 28 new skills across database tooling, FDA compliance, Odoo ERP, agent orchestration, and production architecture. It also ships incremental web-app performance improvements and a full documentation emoji-cleanup pass in line with Maintenance V5 rules. Registry count synced to 1006+ across all docs.

## 🚀 New Skills

### 🗄️ [drizzle-orm-expert](skills/drizzle-orm-expert/)

**Type-safe database development with Drizzle ORM.**
Covers queries, migrations, relations, and adapters for PostgreSQL, MySQL, and SQLite.

> **Try it:** `Use @drizzle-orm-expert to design a schema with relations and run a migration`

---

### 🏭 FDA Compliance Suite (2 skills)

**FDA audit and compliance guidance for food and medtech.**

- **[fda-food-safety-auditor](skills/fda-food-safety-auditor/)**: FSMA, HACCP, and food facility audits with corrective action plans.
- **[fda-medtech-compliance-auditor](skills/fda-medtech-compliance-auditor/)**: FDA 21 CFR Part 820, QSR, and 510(k) / PMA guidance.

> **Try it:** `Use @fda-food-safety-auditor to audit our production facility`

---

### 🏢 Odoo ERP Suite (24 skills)

**Complete Odoo 17 coverage for development, functional, DevOps, compliance, and integrations.**

Skills include: `odoo-development`, `odoo-functional`, `odoo-devops`, `odoo-l10n-compliance`, `odoo-shopify-integration`, `odoo-woocommerce-bridge`, `odoo-edi-connector`, and 17 more.

> **Try it:** `Use @odoo-development to scaffold a custom Odoo 17 module`

---

### 🤖 Production & Audit Skills (2 skills)

- **[codebase-audit-pre-push](skills/codebase-audit-pre-push/)**: Automated quality gate that runs before every push.
- **[production-grade](skills/production-grade/)**: 14-agent orchestrator pipeline for end-to-end production-readiness checks.

> **Try it:** `Run @codebase-audit-pre-push before merging this PR`

---

## 📦 Improvements

- **Registry Update**: Now tracking 1006 skills (+28 since v6.10.0).
- **Statistics Sync**: All docs (README, GETTING_STARTED, FAQ, package.json) updated to reflect 1006 skills — eliminating 978/954/950/900 drift.
- **Contributors**: Added `devchangjun`, `raeef1001`, `1bcMax` to Repo Contributors.
- **Web App Performance** (PR #196): List virtualization, global state, debounced search, lazy loading, incremental loading, and edge-to-edge scrolling.
- **Docs Polish**: Removed emojis from H2 headers in `GETTING_STARTED`, `SKILL_ANATOMY`, `CONTRIBUTING`, `FAQ` following Maintenance V5 anchor rules.
- **Star History**: Updated star history chart in README.

## 👥 Credits

A huge shoutout to our community contributors:

- **@sx4im** for `drizzle-orm-expert`
- **@nagisanzenin** for `production-grade`
- **@Mohammad-Faiz-Cloud-Engineer** for docs emoji cleanup across multiple files
- **@skyruh** for web-app performance improvements (PR #196)
- **@devchangjun**, **@raeef1001**, **@1bcMax** for community contributions

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [6.10.0] - 2026-03-04 - "Skill Router & Developer Tools"

> **Intelligent skill discovery, developer marketing, and AI integration tools.**

This release brings a meta-skill for discovering the right skill, proofreading capabilities, Google Gemini integration, prompt optimization, SaaS MVP guidance, and Bitcoin Lightning Network skills. Plus documentation improvements for durable execution patterns.

### 🚀 New Skills

### 🧭 Skill Router

**Intelligent entry point to the skill library.**

Interviews users with a 4-question funnel when they're unsure what to do, then recommends the best skill(s) with exact invoke prompts to copy-paste immediately. Solves the "900+ skills, where do I start?" problem.

- 4-question guided interview (area → specificity → stack → style)
- Primary + alternative skill recommendations
- Copy-paste ready invoke prompts

> **Try it:** "@skill-router I want to build something but I'm not sure where to start"

### ✍️ Professional Proofreader

**Structured proofreading and grammar correction.**

Proofreads and corrects grammar, spelling, punctuation, and clarity issues while preserving the author's original voice. Returns a structured modification log.

- Inline text mode with change tracking
- File processing mode for .docx, .pdf, .txt
- Preserves original formatting and meaning

> **Try it:** "Proofread this blog post and show me what changed"

### 🤖 Gemini API Integration

**Integrate Google Gemini API into projects.**

Comprehensive guide for Google Gemini API covering model selection, multimodal inputs, streaming, function calling, and production best practices. Supports Node.js and Python.

- Basic generation to advanced multimodal use cases
- Streaming and function calling patterns
- Error handling and model selection guide

> **Try it:** "Set up Gemini API with streaming and function calling"

### 🎯 LLM Prompt Optimizer

**Systematic prompt engineering framework.**

Transforms weak prompts into precision-engineered instructions using RSCIT framework, chain-of-thought, few-shot examples, and structured output patterns.

- RSCIT framework for prompt analysis
- Hallucination reduction techniques
- Token compression strategies

> **Try it:** "Optimize this prompt to get better JSON outputs"

### 🚀 SaaS MVP Launcher

**End-to-end roadmap for building SaaS MVPs.**

Complete guide for building and launching a SaaS MVP: idea validation, tech stack selection (Next.js/Supabase/Stripe/Clerk), project structure, DB schema, auth, payments, and launch checklist.

- Tech stack recommendations with rationale
- Database schema templates
- Pre-launch checklist

> **Try it:** "I have an idea for a SaaS, help me build an MVP"

### ⚡ Lightning Network Skills (3 skills)

**Bitcoin Lightning Network development and architecture.**

Three skills from the SuperScalar project covering channel factories, LSP architectures, and Layer 2 scaling:

- **Lightning Factory Explainer**: SuperScalar protocol and scalable onboarding
- **Lightning Channel Factories**: Multi-party channels and factory architectures
- **Lightning Architecture Review**: Protocol design comparison and tradeoffs

> **Try it:** "Explain how Lightning channel factories work"

---

### 📦 Improvements

- **Registry Update**: Now tracking 978 skills.
- **Documentation**: Added durable execution highlights to architectural skills (ai-agents-architect, architecture-patterns, event-sourcing-architect, saga-orchestration, workflow-automation).
- **Community**: Added devmarketing-skills to Community Contributors section.
- **Validation**: Fixed risk level in 3 skills (saas-mvp-launcher, llm-prompt-optimizer, gemini-api-integration).

### 👥 Credits

A huge shoutout to our community contributors:

- **@lsuryatej** for `skill-router`
- **@tejasashinde** for `professional-proofreader`
- **@SnakeEye-sudo** for `gemini-api-integration`, `llm-prompt-optimizer`, `saas-mvp-launcher`
- **@8144225309** for Lightning Network skills
- **@maxdml** for durable execution documentation updates
- **@jonathimer** for devmarketing-skills community link
- **@copilot-swe-agent** for answering community questions

---

## [6.9.0] - 2026-03-03 - "Multi-Tool & Agent Infrastructure"

> **Agent capabilities expand with email infrastructure, video intelligence, and multi-tool installer support.**

This release delivers major infrastructure improvements: one-command install for multiple AI tools, email capabilities for agents via AgentMail, and video/audio processing with VideoDB. Plus significant web-app performance optimizations.

### 🚀 New Skills

### 📧 AgentMail

**Email infrastructure for AI agents.**

Gives agents real email addresses (`@theagentmail.net`) via REST API. Create accounts, send/receive emails, manage webhooks, and check karma balance. Perfect for agents that need to sign up for services, receive verification codes, or communicate via email.

- Create email accounts with karma-based rate limiting
- Send/receive emails with attachments
- Webhook signature verification for secure notifications
- Full SDK examples and API reference

> **Try it:** "Create an email account for my agent and send a verification email"

### 📹 VideoDB

**Video and audio perception, indexing, and editing.**

Ingest files/URLs/live streams, build visual/spoken indexes, search with timestamps, edit timelines, add overlays/subtitles, generate media, and create real-time alerts.

- Ingest from files, URLs, RTSP/live feeds, or desktop capture
- Semantic, visual, and spoken word indexes with timestamp search
- Timeline editing with subtitles, overlays, transcoding
- AI generation for images, video, music, voiceovers

> **Try it:** "Search for 'product demo' in this video and create a clip with subtitles"

---

### 📦 Improvements

- **Multi-Tool Install Support**: The installer now supports installing skills for multiple tools simultaneously (e.g., `npx antigravity-awesome-skills --claude --codex`). Fixes #182.
- **Web-App Sync Optimization**: Hybrid sync strategy using git fetch for faster updates (5+ min → < 2 sec when no changes). Includes sort by "Most Stars" feature.
- **Registry Update**: Now tracking 970 skills (+2 new).

### 👥 Credits

- **@zinzied** for web-app sync optimization (PR #180)
- **@0xrohitgarg** for VideoDB skill contribution (PR #181)
- **@uriva** for AgentMail skill contribution (PR #183)

---

## [6.8.0] - 2026-03-02 - "Productivity Boost & In-App Sync"

> **Major productivity enhancements to existing skills and new in-app skill synchronization feature.**

This release delivers version 2.0.0 upgrades to two critical skills: `vibe-code-auditor` and `tutorial-engineer`, packed with pattern recognition shortcuts, deterministic scoring, and copy-paste templates. Plus, a new "Sync Skills" button in the Web App enables live skill updates from GitHub without leaving the browser.

## 🚀 New Features

### 🔄 In-App Sync Skills Button

**One-click skill synchronization from the Web App UI.**
Replaces the unreliable START_APP.bat auto-updater. Users can now click "Sync Skills" in the web app to download the latest skills from GitHub instantly.

- Vite dev server plugin exposing `/api/refresh-skills` endpoint
- Downloads and extracts only the `/skills/` folder and `skills_index.json`
- Live UI updates without page refresh

## 📦 Improvements

### ✨ vibe-code-auditor v2.0.0

**Productivity-focused overhaul with 10x faster audits.**

- **Pattern Recognition Shortcuts**: 10 heuristics for rapid issue detection
- **Quick Checks**: 3-second scans for each of 7 audit dimensions
- **Executive Summary**: Critical findings upfront
- **Deterministic Scoring**: Replaces subjective ranges with algorithmic scoring
- **Code Fix Blocks**: Before/after examples for copy-paste remediation
- **Quick Wins Section**: Fixes completable in <1 hour
- **Calibration Rules**: Scoring adjusted by code size (snippet vs multi-file)
- **Expanded Security**: SQL injection, path traversal, insecure deserialization detection

### 📚 tutorial-engineer v2.0.0

**Evidence-based learning with 75% better retention.**

- **4-MAT Model**: Why/What/How/What If framework for explanations
- **Learning Retention Shortcuts**: Evidence-based patterns (+75% retention)
- **Cognitive Load Management**: 7±2 rule, One Screen, No Forward References
- **Exercise Calibration**: Difficulty table with time estimates
- **Format Selection Guide**: Quick Start vs Deep Dive vs Workshop
- **Pre-Publish Audit Checklist**: Comprehension, progression, technical validation
- **Speed Scoring Rubric**: 1-5 rating on 5 dimensions
- **Copy-Paste Template**: Ready-to-use Markdown structure
- **Accessibility Checklist**: WCAG compliance for tutorials

## 👥 Credits

A huge shoutout to our community contributors:

- **@munir-abbasi** for the v2.0.0 productivity enhancements to `vibe-code-auditor` and `tutorial-engineer` (PR #172)
- **@zinzied** for the In-App Sync Skills Button and START_APP.bat simplification (PR #178)

---

## [6.7.0] - 2026-03-01 - "Intelligence Extraction & Automation"

> **New skills for Web Scraping (Apify), X/Twitter extraction, Genomic analysis, and hardened registry infrastructure.**

This release integrates 14 new specialized agent-skills. Highlights include the official Apify collection for web scraping and data extraction, a high-performance X/Twitter scraper, and a comprehensive genomic analysis toolkit. The registry infrastructure has been hardened with hermetic testing and secure YAML parsing.

## 🚀 New Skills

### 🕷️ [apify-agent-skills](skills/apify-actorization/)

**12 Official Apify skills for web scraping and automation.**
Scale data extraction using Apify Actors. Includes specialized skills for e-commerce, lead generation, social media analysis, and market research.

### 🐦 [x-twitter-scraper](skills/x-twitter-scraper/)

**High-performance X (Twitter) data extraction.**
Search tweets, fetch profiles, and extract media/engagement metrics without complex API setups.

### 🧬 [dna-claude-analysis](skills/dna-claude-analysis/)

**Personal genome analysis toolkit.**
Analyze raw DNA data across 17 categories (health, ancestry, pharmacogenomics) with interactive HTML visualization.

---

## 📦 Improvements

- **Registry Hardening**: Migrated all registry maintenance scripts to `PyYAML` for safe, lossless metadata handling. (PR #168)
- **Hermetic Testing**: Implemented environment-agnostic registry tests to prevent CI drift.
- **Contributor Sync**: Fully synchronized the Repo Contributors list in README.md from git history (69 total contributors).
- **Documentation**: Standardized H2 headers in README.md (no emojis) for clean Table of Contents anchors, following Maintenance V5 rules.
- **Skill Metadata**: Enhanced description validation and category consistency across 968 skills.

## 👥 Credits

A huge shoutout to our community contributors:

- **@ar27111994** for the 12 Apify skills and registry hardening (PR #165, #168)
- **@kriptoburak** for `x-twitter-scraper` (PR #164)
- **@shmlkv** for `dna-claude-analysis` (PR #167)

---

## [6.6.0] - 2026-02-28 - "Community Skills & Quality"

> **New skills for Android UI verification, memory handling, video manipulation, vibe-code auditing, and essential fixes.**

This release integrates major community contributions, adding skills for Android testing, scoped agent memory, vibe-code quality auditing, and the VideoDB SDK. It also addresses issues with skill metadata validation and enhances documentation consistency.

## 🚀 New Skills

### 📱 [android_ui_verification](skills/android_ui_verification/)

**Automated end-to-end UI testing on Android Emulators.**
Test layout issues, check state verification, and capture screenshots right from ADB.

### 🧠 [hierarchical-agent-memory](skills/hierarchical-agent-memory/)

**Scoped CLAUDE.md memory system.**
Directory-level context files with a dashboard, significantly reducing token spend on repetitive queries.

### 🎥 [videodb-skills](skills/videodb-skills/)

**The ultimate Video processing toolkit.**
Upload, stream, search, edit, transcribe, and generate AI video/audio using the VideoDB SDK.

### 🕵️ [vibe-code-auditor](skills/vibe-code-auditor/)

**AI-code specific quality assessments.**
Check prototypes and generated code for structural flaws, hidden technical debt, and production risks.

---

## 📦 Improvements

- **Skill Description Restoration**: Recovered 223+ truncated descriptions from git history that were corrupted in release 6.5.0.
- **Robust YAML Tooling**: Replaced fragile regex parsing with `PyYAML` across all maintenance scripts (`manage_skill_dates.py`, `validate_skills.py`, etc.) to prevent future data loss.
- **Refined Descriptions**: Standardized all skill descriptions to be under 200 characters while maintaining grammatical correctness and functional value.
- **Cross-Platform Index**: Normalized `skills_index.json` to use forward slashes for universal path compatibility.
- **Skill Validation Fixes**: Corrected invalid description lengths and `risk` fields in `copywriting`, `videodb-skills`, and `vibe-code-auditor`. (Fixes #157, #158)
- **Documentation**: New dedicated `docs/SEC_SKILLS.md` indexing all 128 security skills.
- **README Quality**: Cleaned up inconsistencies, deduplicated lists, updated stats (954+ total skills).

## 👥 Credits

A huge shoutout to our community contributors:

- **@alexmvie** for `android_ui_verification`
- **@talesperito** for `vibe-code-auditor`
- **@djmahe4** for `docs/SEC_SKILLS.md`
- **@kromahlusenii-ops** for `hierarchical-agent-memory`
- **@0xrohitgarg** for `videodb-skills`
- **@nedcodes-ok** for `rule-porter` addition
- **@acbhatt12** for `README.md` improvements (PR #162)

---

## [6.5.0] - 2026-02-27 - "Community & Experience"

> **Major UX upgrade: Stars feature, auto-updates, interactive prompts, and complete date tracking for all 950+ skills.**

This release introduces significant community-driven enhancements to the web application alongside comprehensive metadata improvements. Users can now upvote skills, build contextual prompts interactively, and benefit from automatic skill updates. All skills now include date tracking for better discoverability.

## 🚀 New Features

### ⭐ Stars & Community Upvotes

**Community-driven skill discovery with star/upvote system.**

- Upvote skills you find valuable — visible to all users
- Star counts persist via Supabase backend
- One upvote per browser (localStorage deduplication)
- Discover popular skills through community ratings

> **Try it:** Browse to any skill and click the ⭐ button to upvote!

### 🔄 Auto-Update Mechanism

**Seamless skill updates via START_APP.bat.**

- Automatic skill synchronization on app startup
- Git-based fast updates when available
- PowerShell HTTPS fallback for non-Git environments
- Surgical updates — only `/skills/` folder to avoid conflicts

> **Try it:** Run `START_APP.bat` to automatically fetch the latest 950+ skills!

### 🛠️ Interactive Prompt Builder

**Build contextual prompts directly in skill detail pages.**

- Add custom context to any skill (e.g., "Use React 19 and Tailwind")
- Copy formatted prompt with skill invocation + your context
- Copy full skill content with context overlay
- Streamlined workflow for AI assistant interactions

> **Try it:** Visit any skill, add context in the text box, click "Copy @Skill"!

### 📅 Date Tracking for All Skills

**Complete `date_added` metadata across the entire registry.**

- All 950+ skills now include `date_added` field
- Visible badges in skill detail pages
- Filter and sort by recency
- Better discoverability of new capabilities

## 📦 Improvements

- **Smart Auto-Categorization**: Categories sorted by skill count with "uncategorized" at the end
- **Category Stats**: Dropdown shows skill count per category
- **Enhanced Home Page**: Risk level badges and date display on skill cards
- **Complete Date Coverage**: All skills updated with `date_added` metadata
- **Web App Dependencies**: Automatic `@supabase/supabase-js` installation

## 👥 Credits

A huge shoutout to our community contributors:

- **@zinzied** for the comprehensive UX enhancement (Stars, Auto-Update, Prompt Builder, Date Tracking, Auto-Categorization — PR #150)

---

## [6.4.1] - 2026-02-27 - "Temporal & Convex Backend Hotfix"

> **Hotfix release: Temporal Go expert skill, Convex reactive backend, and strict-compliant SEO incident/local audit fixes.**

This release builds on 6.4.0 by adding a Temporal Go SDK pro skill, a comprehensive Convex reactive backend skill, and aligning the new SEO incident/local audit skills with the strict validation rules so they ship cleanly via npm.

## 🚀 New Skills

### ⏱️ [temporal-golang-pro](skills/temporal-golang-pro/)

**Temporal Go SDK expert for durable distributed systems.**
Guides production-grade Temporal Go usage with deterministic workflow rules, mTLS worker configuration, interceptors, testing strategies, and advanced patterns.

- **Key Feature 1**: Covers workflow determinism, versioning, durable concurrency and long-running workflow patterns.
- **Key Feature 2**: Provides mTLS-secure worker setup, interceptors, and replay/time-skipping test strategies.

> **Try it:** `Use temporal-golang-pro to design a durable subscription billing workflow with safe versioning and mTLS workers.`

### 🔄 [convex](skills/convex/)

**Convex reactive backend for schema, functions, and real-time apps.**
Full-stack backend skill covering Convex schema design, TypeScript query/mutation/action functions, real-time subscriptions, auth, file storage, scheduling, and deployment flows.

- **Key Feature 1**: End-to-end examples for schema validators, function types, pagination and client integration.
- **Key Feature 2**: Documents auth options (Convex Auth, Clerk, Better Auth) and operational patterns (cron, storage, environments).

> **Try it:** `Use convex to design a schema and function set for a real-time dashboard with authenticated users and file uploads.`

## 📦 Improvements

- **Strict SEO Skills Compliance**:
  - `seo-forensic-incident-response` and `local-legal-seo-audit` now include `## When to Use` sections and concise descriptions, and use `risk: safe`, fully passing `validate_skills.py --strict`.
- **Catalog & Index Sync**:
  - Updated `CATALOG.md`, `data/catalog.json`, `skills_index.json`, `data/bundles.json`, `data/aliases.json`, and `README.md` to track **950+ skills**, including `temporal-golang-pro`, `convex`, and the new SEO skills.

## 👥 Credits

- **@HuynhNhatKhanh** for the Temporal Go SDK expert skill (`temporal-golang-pro`, PR #148).
- **@chauey** for the Convex reactive backend skill (`convex`, PR #152).
- **@talesperito** for the SEO forensic incident response and local legal SEO skills and collaboration on the strict-compliant refinements (PRs #153 / #154).

---

## [6.4.0] - 2026-02-27 - "SEO Incident Response & Legal Local Audit"

> **Focused release: specialized SEO incident response and legal local SEO audit skills, plus catalog sync.**

This release adds two advanced SEO skills for handling organic traffic incidents and auditing legal/professional services sites, and updates the public catalog to keep discovery aligned with the registry.

## 🚀 New Skills

### 🧪 [seo-forensic-incident-response](skills/seo-forensic-incident-response/)

**Forensic SEO incident response for sudden organic traffic or rankings drops.**
Guides structured triage, hypothesis-driven investigation, evidence collection and phased recovery plans using GSC, analytics, logs and deployment history.

- **Key Feature 1**: Classifies incidents across algorithmic, technical, manual action, content and demand-change buckets.
- **Key Feature 2**: Produces a forensic report with 0–3 day, 3–14 day and 2–8 week action plans plus monitoring.

> **Try it:** `We lost 40% of organic traffic last week. Use seo-forensic-incident-response to investigate and propose a recovery plan.`

### ⚖️ [local-legal-seo-audit](skills/local-legal-seo-audit/)

**Local SEO auditing for law firms and legal/professional services.**
Specialized audit framework for YMYL legal sites covering GBP, E‑E‑A‑T, practice area pages, NAP consistency, legal directories and reputation.

- **Key Feature 1**: Step‑by‑step GBP, directory and NAP audit tailored to legal practices.
- **Key Feature 2**: Generates a prioritized action plan and content strategy for legal/local search.

> **Try it:** `Audit the local SEO of this law firm website using local-legal-seo-audit and propose the top 10 fixes.`

## 📦 Improvements

- **Catalog Sync**: Updated `CATALOG.md` and `data/catalog.json` to track 947 skills and include `10-andruia-skill-smith` in the general category listing.
- **Documentation**: README now references the MojoAuth implementation skill in the integrations list.

## 👥 Credits

A huge shoutout to our community contributors:

- **@talesperito** for the SEO forensic incident response and legal local SEO audit skills (PRs #153 / #154).
- **@developer-victor** for the MojoAuth implementation README integration (PR #149).

---

## [6.3.1] - 2026-02-25 - "Validation & Multi-Protocol Hotfix"

> **"Hotfix release to restore missing skills, correct industrial risk labels, and harden validation across the registry."**

This release fixes critical validation errors introduced in previous PRs, ensures full compliance with the strict CI registry checks, and restores two high-demand developer skills.

## 🚀 New Skills

### 🧩 [chrome-extension-developer](skills/chrome-extension-developer/)

**Expert in building Chrome Extensions using Manifest V3.**
Senior expertise in modern extension architecture, focusing on Manifest V3, service workers, and production-ready security practices.

- **Key Feature 1**: Comprehensive coverage of Manifest V3 service workers and lifecycle.
- **Key Feature 2**: Production-ready patterns for cross-context message passing.

> **Try it:** `Help me design a Manifest V3 extension that monitors network requests using declarativeNetRequest.`

### ☁️ [cloudflare-workers-expert](skills/cloudflare-workers-expert/)

**Senior expertise for serverless edge computing on Cloudflare.**
Specialized in edge architectures, performance optimization, and the full Cloudflare developer ecosystem (Wrangler, KV, D1, R2).

- **Key Feature 1**: Optimized patterns for 0ms cold starts and edge-side storage.
- **Key Feature 2**: Implementation guides for Durable Objects and R2 storage integration.

> **Try it:** `Build a Cloudflare Worker that modifies response headers and caches fragmented data in KV.`

---

## 📦 Improvements

- **Registry Update**: Now tracking 946+ high-performance skills.
- **Validation Hardening**: Resolved missing "When to Use" sections for 11 critical skills (Andru.ia, Logistics, Energy).
- **Risk Label Corrections**: Corrected risk levels to `safe` for `linkedin-cli`, `00-andruia-consultant`, and `20-andruia-niche-intelligence`.

## 👥 Credits

A huge shoutout to our community contributors:

- **@itsmeares** for PR #139 validation fixes and "When to Use" improvements.

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [6.3.0] - 2026-02-25 - "Agent Discovery & Operational Excellence"

> **Feature release: AgentFolio discovery skill, LinkedIn CLI automation, Evos operational skills, Andru.ia consulting roles, and hardened validation for new contributors.**

## 🚀 New Skills

### 🔍 [agentfolio](skills/agentfolio/)

**Discover and research autonomous AI agents.**
Skill for discovering and researching autonomous AI agents, tools, and ecosystems using the AgentFolio directory.

- **Key Feature 1**: Discover agents for specific use cases.
- **Key Feature 2**: Collect concrete examples and benchmarks for agent capabilities.

> **Try it:** `Use AgentFolio to find 3 autonomous AI agents focused on code review.`

### 💼 [linkedin-cli](skills/linkedin-cli/)

**Automate LinkedIn operations via CLI.**
CLI-based LinkedIn automation skill using `@linkedapi/linkedin-cli` for profile enrichment, outreach, Sales Navigator, and workflow execution.

- **Key Feature 1**: Fetch profiles and search people/companies.
- **Key Feature 2**: Manage connections and send messages via Sales Navigator.

> **Try it:** `Use linkedin-cli to search for PMs in San Francisco.`

### 🚀 [appdeploy](skills/appdeploy/)

**Deploy full-stack web apps.**
Deploy web apps with backend APIs, database, and file storage via an HTTP API to get an instant public URL.

- **Key Feature 1**: Chat-native deployment orchestrator.
- **Key Feature 2**: Support for frontend-only and frontend+backend architectures.

> **Try it:** `Deploy this React-Vite dashboard using appdeploy.`

### 🐹 [grpc-golang](skills/grpc-golang/)

**Production-grade gRPC patterns in Go.**
Build robust microservices communication using Protobuf with mTLS, streaming, and observability configurations.

- **Key Feature 1**: Standardize API contracts with Protobuf and Buf.
- **Key Feature 2**: Implement service-to-service authentication and structured metrics.

> **Try it:** `Use grpc-golang to define a user service streaming endpoint with mTLS.`

### 📦 [logistics-exception-management](skills/logistics-exception-management/)

**Expertise for handling freight and carrier disputes.**
Deeply codified operational playbook for handling shipping exceptions, delays, damages, and claims. Part of the Evos operational domain expertise suite. Additional skills: `carrier-relationship-management`, `customs-trade-compliance`, `inventory-demand-planning`, `production-scheduling`, `returns-reverse-logistics`, `energy-procurement`, `quality-nonconformance`.

- **Key Feature 1**: Provides escalation protocols and severity classification for exceptions.
- **Key Feature 2**: Delivers templates and decision frameworks for claim management across various delivery modes.

> **Try it:** `We have a delayed LTL shipment for a key customer, how should we handle it per logistics-exception-management?`

### 🏗️ [00-andruia-consultant](skills/00-andruia-consultant/)

**Spanish-language solutions architect.**
Diagnóstica y traza la hoja de ruta óptima para proyectos de IA en español. Additional skills: `20-andruia-niche-intelligence`.

- **Key Feature 1**: Proporciona entrevistas de diagnóstico para proyectos desde cero o existentes.
- **Key Feature 2**: Propone el escuadrón de expertos necesario y genera artefactos de backlog en español.

> **Try it:** `Actúa como 00-andruia-consultant y diagnostica este nuevo workspace.`

## 📦 Improvements

- **Validation & Quality Bar**:
  - Normalised `risk:` labels for new skills to conform to the allowed set (`none`, `safe`, `critical`, `offensive`, `unknown`).
  - Added explicit `## When to Use` sections to new operational and contributor skills to keep the registry strictly compatible with `python3 scripts/validate_skills.py --strict`.
- **Interactive Web App**:
  - Auto-updating local web app launcher and **Interactive Prompt Builder** enhancements (PR #137) now ship as part of the v6.3.0 baseline.
- **Registry**:
  - Validation Chain (`npm run chain` + `npm run validate:strict`) runs clean at 6.3.0 with all new skills indexed in `skills_index.json`, `data/catalog.json`, and `CATALOG.md`.

## 👥 Credits

- **@bobrenze-bot** for proposing the AgentFolio integration (Issue #136).
- **@vprudnikoff** for the `linkedin-cli` skill (PR #131).
- **@Onsraa** for the Bevy ECS documentation update around Require Components (PR #132).
- **@Abdulrahmansoliman** for the AdaL CLI README instructions (PR #133).
- **@avimak** for the `appdeploy` deployment skill (PR #134).
- **@HuynhNhatKhanh** for the gRPC Go production patterns skill (PR #135).
- **@zinzied** for the auto-updating web app launcher & Interactive Prompt Builder (PR #137).
- **@nocodemf** for the Evos operational domain skills (PR #138).

---

## [6.2.0] - 2026-02-24 - "Interactive Web App & AWS IaC"

> **Feature release: Interactive Skills Web App, AWS Infrastructure as Code skills, and Chrome Extension / Cloudflare Workers developer skills.**

## 🚀 New Skills

- **AWS Infrastructure as Code** (PR #124): `cdk-patterns`, `cloudformation-best-practices`, `terraform-aws-modules`.
- **Browser & Edge** (PR #128): `chrome-extension-developer`, `cloudflare-workers-expert`.

## 📦 Improvements

- **Interactive Skills Web App** (PR #126): Added a local web UI for browsing skills, including `START_APP.bat`, setup script, and `web-app/` project with catalog export.
- **Shopify Development Skill** (PR #125): Fixed markdown syntax issues in `skills/shopify-development/SKILL.md` to keep the registry strictly valid.
- **Community Sources** (PR #127): Added SSOJet skills and integration guides to Credits & Sources.
- **Registry**: Now tracking 930 skills.

## 👥 Credits

- **@ssumanbiswas** for AWS Infrastructure as Code skills (PR #124).
- **@thuanlm** for the Shopify development skill fix (PR #125).
- **@zinzied** for the Interactive Skills Web App (PR #126).
- **@code-vj** for the SSOJet documentation link (PR #127).
- **@GeekLuffy** for Chrome Extension and Cloudflare Workers skills (PR #128).

---

## [6.1.1] - 2026-02-23 - "AWS Cost Optimization & Registry 927"

> **Patch release: AWS cost optimization skills (PR #107) and registry count 927.**

- **New skills** (PR #107): `aws-cost-optimizer`, `aws-cost-cleanup`.
- **Registry**: Now tracking 927 skills.

---

## [6.1.0] - 2026-02-23 - "Issues Fix & Community Expansion"

> **Bugfixes for #116 and #120, plus Game Dev bundle, Android skills, Workflow Bundles, LibreOffice, Data Structure Protocol, and Kiro IDE support.**

This release fixes the YAML syntax error in database-migrations-sql-migrations (issue #116), adds a typo alias so `shopify—development` (em dash) resolves to `shopify-development` (issue #120), and ships a large set of community PRs: Game Development Expansion (Bevy ECS, GLSL, Godot 4), Android Modern Development (Compose + Coroutines), Workflow Bundles and LibreOffice skills, Data Structure Protocol, and Kiro CLI/IDE support.

## New Skills

- **Game Development Expansion** (PR #121): `bevy-ecs-expert`, `shader-programming-glsl`, `godot-4-migration`.
- **Android Modern Development** (PR #118): `android-jetpack-compose-expert`, `kotlin-coroutines-expert`.
- **Workflow Bundles & LibreOffice** (PR #113): Workflow bundles readme, LibreOffice skills (Base, Calc, Draw, Impress, Writer), plus office-productivity, WordPress suite, and many domain skills (ai-agent-development, cloud-devops, database, e2e-testing, security-audit, terraform-infrastructure, etc.).
- **Data Structure Protocol** (PR #114): `data-structure-protocol`.
- **Kiro CLI and Kiro IDE** (PR #122): Documentation and support for Kiro.

## Improvements

- **YAML fix** (PR #119, fixes #116): Resolved invalid YAML in `database-migrations-sql-migrations/SKILL.md` (description block mapping); removed non-standard frontmatter and standardized section headers.
- **Skill matching** (fixes #120): Added typo alias `shopify—development` → `shopify-development` so em-dash input resolves correctly.
- **Registry**: Now tracking 925 skills.

## Credits

- **@nikolasdehor** for YAML fix (PR #119), Game Development Expansion (PR #121), Android Modern Development (PR #118)
- **@ssumanbiswas** for Kiro CLI and Kiro IDE support (PR #122)
- **@munir-abbasi** for Workflow Bundles and LibreOffice Skills (PR #113)
- **@k-kolomeitsev** for Data Structure Protocol (PR #114)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [6.0.0] - 2026-02-22 - "Codex YAML Fix & Community PRs"

> **Major release: Codex frontmatter fixes, AWS Security & Compliance skills, Antigravity Workspace Manager CLI, and validation fixes.**

This release addresses Codex invalid YAML warnings (issue #108) via frontmatter fixes, adds AWS Security & Compliance skills and the official Antigravity Workspace Manager CLI companion, and fixes validation for nerdzao-elite skills.

## New Skills

- **AWS Security & Compliance** (PR #106): `aws-compliance-checker`, `aws-iam-best-practices`, `aws-secrets-rotation`, `aws-security-audit`.
- **nerdzao-elite**, **nerdzao-elite-gemini-high**: Elite workflow skills (validation fixes in-repo).

## Improvements

- **Frontmatter**: Fixed YAML frontmatter in code-reviewer, architect-review, c-pro, design-orchestration, haskell-pro, multi-agent-brainstorming, performance-engineer, search-specialist (PR #111) — reduces Codex "invalid YAML" warnings (fixes #108).
- **Antigravity Workspace Manager**: Official CLI companion to auto-provision skill subsets across environments (PR #110); documented in Community Contributors.
- **Registry**: Now tracking 889 skills.
- **Validation**: Added frontmatter and "When to Use" for nerdzao-elite / nerdzao-elite-gemini-high.

## Credits

- **@Vonfry** for frontmatter YAML fixes (PR #111)
- **@ssumanbiswas** for AWS Security & Compliance skills (PR #106)
- **@amartelr** for Antigravity Workspace Manager CLI (PR #110)
- **@fernandorych** for branch sync (PR #109)
- **@Rodrigolmti** for reporting Codex YAML issue (#108)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [5.10.0] - 2026-02-21 - "AWS Kiro CLI Integration"

> **Native support and integration guide for AWS Kiro CLI, expanding the repository's reach to the AWS developer community.**

This release adds comprehensive support for Kiro CLI, AWS's recently launched agentic IDE, enabling 883+ skills to enhance Kiro's autonomous operations across serverless, IaC, and AWS architectures. It also includes an important bugfix for the npm installer CLI.

## 🚀 Improvements

- **Integration Guide**: Added `docs/KIRO_INTEGRATION.md` detailing Kiro capabilities, installation instructions, AWS-recommended skills, and MCP usage.
- **Documentation**: Updated `README.md`, `docs/GETTING_STARTED.md`, and `docs/FAQ.md` to formally support Kiro CLI and add invocation examples.
- **Installer**: Added the `--kiro` flag to the CLI installer (`bin/install.js`) which correctly targets `~/.kiro/skills`.

## 🐛 Bug Fixes

- **Installer Path Consistency**: Fixed Issue #105 where the published `v5.9.0` npm install script contained an older version of `bin/install.js`, causing `--antigravity` installs to mistakenly target `.agent/skills` instead of the global `~/.gemini/antigravity/skills`. This release (`5.10.0`) properly bundles the corrected npm install script.

## 👥 Credits

A huge shoutout to our community contributors:

- **@ssumanbiswas** for the Kiro CLI support (PR #104)

---

## [5.9.0] - 2026-02-20 - "Apple HIG & Quality Bar"

> **Extensive Apple design guidelines and strict validation for the entire registry.**

This release adds the official Apple Human Interface Guidelines skills suite, enforces strict agentskills-ref metadata validation across all skills, and addresses critical path resolution bugs in the CLI installer along with dangling link validation to prevent agent token waste.

## 🚀 New Skills

### 🍎 [apple-hig-skills](skills/hig-platforms/)

**Comprehensive platform and UX guidelines for Apple ecosystems.**
Official guidelines covering iOS, macOS, visionOS, watchOS, and tvOS natively formatted for AI consumption.

- **Key Feature 1**: Deep dives into spatial layout, interactions, and modalities.
- **Key Feature 2**: Component-level guidelines for status bars, dialogs, charts, and input mechanisms (Pencil, Digital Crown).

> **Try it:** `Use @hig-platforms to review if our iPad app navigation follows standard iOS paradigms.`

### 👁️ [manifest](skills/manifest/)

**Observability plugin setup guide for AI agents.**
Walks through a 6-step setup for the Manifest observability platform, including troubleshooting for common errors.

- **Key Feature**: Complete configuration wizard from obtaining API keys to verifying traces.

> **Try it:** `Use @manifest to add observability to our local python agent.`

---

## 📦 Improvements

- **Registry Update**: Now tracking 883 skills.
- **CLI Installer**: Fixed the default `.agent/skills` path to properly default to `~/.gemini/antigravity/skills` and added an explicit `--antigravity` flag (fixes #101).
- **Validation**: Enforced strict folder-to-name matching and concise (<200 char) descriptions based on `agentskills-ref` (fixes #97).
- **Validation**: Added build-time Markdown dangling link validation to `validate_skills.py` to prevent agents from hallucinating relative paths (fixes #102).

## 👥 Credits

A huge shoutout to our community contributors:

- **@raintree-technology** for the Apple HIG Skills (PR #90)
- **@sergeyklay** for the skill quality validations (PR #97)
- **@SebConejo** for the manifest observability skill (PR #103)
- **@community** for identifying installer and link bugs (Issues #101, #102)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

## [5.8.0] - 2026-02-19 - "Domain-Driven Design Suite"

> **First full DDD skill suite: strategic design, context mapping, and tactical patterns for complex domains.**

This release introduces a comprehensive Domain-Driven Design skill suite (4 new skills) contributed by the community, plus playbook fixes for saga-orchestration and event-store-design, and new DDD-themed bundle and workflow entries.

## 🚀 New Skills

### 🏗️ [domain-driven-design](skills/domain-driven-design/)

**Entry point and router for all DDD adoption decisions.**
Covers viability checks, routing to strategic/tactical/evented sub-skills, and output requirements.

- **Key Feature**: Viability check gate — avoids over-engineering simple systems.
- **Key Feature**: Routing map to `@ddd-strategic-design`, `@ddd-context-mapping`, `@ddd-tactical-patterns`, CQRS, event sourcing, sagas, projections.

> **Try it:** `Use @domain-driven-design to assess if this billing platform should adopt full DDD.`

### 🗺️ [ddd-strategic-design](skills/ddd-strategic-design/)

**Subdomains, bounded contexts, and ubiquitous language.**
Produces subdomain classification tables, bounded context catalogs, and glossaries.

### 🔗 [ddd-context-mapping](skills/ddd-context-mapping/)

**Cross-context integration contracts and anti-corruption layers.**
Defines upstream/downstream ownership, translation rules, and versioning policies.

### 🧩 [ddd-tactical-patterns](skills/ddd-tactical-patterns/)

**Aggregates, value objects, repositories, and domain events in code.**
Includes a TypeScript aggregate example with invariant enforcement.

---

## 📦 Improvements

- **Registry Update**: Now tracking 868 skills.
- **saga-orchestration** and **event-store-design**: Added missing `resources/implementation-playbook.md`.
- **docs/BUNDLES.md**: Added DDD & Evented Architecture bundle section.
- **docs/WORKFLOWS.md** + **data/workflows.json**: New "Design a DDD Core Domain" workflow entry.

## 👥 Credits

A huge shoutout to our community contributors:

- **[@rcigor](https://github.com/rcigor)** for the full DDD skill suite (PR #98)

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [5.7.0] - 2026-02-18 - "Yandex Direct Audit"

> **First agentic skill for the Russian PPC market, offering comprehensive Yandex Direct account auditing.**

### Added

- **New External Skill**: `yandex-direct-audit` (Silverov/yandex-direct-skill)
  - 55 automated checks for Yandex Direct (API v5).
  - A-F scoring system.
  - Comprehensive campaign, ad, and keyword analysis.

### Registry

- **Total Skills**: 864.
- **Generated Files**: Synced artifacts.

### Credits

- **[@Silverov](https://github.com/Silverov)** - Yandex Direct Audit skill (PR #95).

---

## [5.6.0] - 2026-02-17 - "Autonomous Agents & Trusted Workflows"

> **DBOS for reliable workflows, Crypto BD agents, and improved usage documentation.**

This release introduces official DBOS skills for building fault-tolerant applications in TypeScript, Python, and Go, plus a sophisticated autonomous Business Development agent for crypto, and a comprehensive usage guide to help new users get started.

### Added

- **DBOS Skills** (Official):
  - `dbos-typescript`: Durable workflows and steps for TypeScript.
  - `dbos-python`: Fault-tolerant Python applications.
  - `dbos-golang`: Reliable Go services.
- **New Skill**: `crypto-bd-agent` - Autonomous BD patterns for token discovery, scoring, and outreach with wallet forensics.
- **Documentation**: New `docs/USAGE.md` guide addressing post-installation confusion (how to prompt, where skills live).

### Registry

- **Total Skills**: 864 (from 860).
- **Generated Files**: Synced `skills_index.json`, `data/catalog.json`, and `README.md`.

### Contributors

- **[@maxdml](https://github.com/maxdml)** - DBOS Skills (PR #94).
- **[@buzzbysolcex](https://github.com/buzzbysolcex)** - Crypto BD Agent (PR #92).
- **[@copilot-swe-agent](https://github.com/apps/copilot-swe-agent)** - Usage Guide (PR #93).

---

## [5.5.0] - 2026-02-16 - "Laravel Pro & ReactFlow Architect"

> **Advanced Laravel engineering roles and ReactFlow architecture patterns.**

This release introduces professional Laravel capabilities (Expert & Security Auditor) and a comprehensive ReactFlow Architect skill for building complex node-based applications.

### Added

- **New Skill**: `laravel-expert` - Senior Laravel Engineer role for production-grade, maintainable, and idiomatic solutions (clean architecture, security, performance).
- **New Skill**: `laravel-security-audit` - Specialized security auditor for Laravel apps (OWASP, vulnerabilities, misconfigurations).
- **New Skill**: `react-flow-architect` - Expert ReactFlow patterns for interactive graph apps (hierarchical navigation, performance, customized state management).

### Changed

- **OpenCode**: Updated installation path to `.agents/skills` to align with latest OpenCode standards.

### Registry

- **Total Skills**: 860 (from 857).
- **Generated Files**: Synced `skills_index.json`, `data/catalog.json`, and `README.md`.

### Contributors

- **[@Musayrlsms](https://github.com/Musayrlsms)** - Laravel Expert & Security Audit skills (PR #85, #86).
- **[@mertbaskurt](https://github.com/mertbaskurt)** - ReactFlow Architect skill (PR #88).
- **[@sharmanilay](https://github.com/sharmanilay)** - OpenCode path fix (PR #87).

---

## [5.4.0] - 2026-02-16 - "CursorRules Pro & Go-Rod"

> **Community contributions: CursorRules Pro in credits and go-rod-master skill for browser automation with Go.**

This release adds CursorRules Pro to Community Contributors and a new skill for browser automation and web scraping with go-rod (Chrome DevTools Protocol) in Golang, including stealth and anti-bot-detection patterns.

### New Skills

#### go-rod-master ([skills/go-rod-master/](skills/go-rod-master/))

**Browser automation and web scraping with Go and Chrome DevTools Protocol.**
Comprehensive guide for the go-rod library: launch and page lifecycle, Must vs error patterns, context and timeouts, element selectors, auto-wait, and integration with go-rod/stealth for anti-bot detection.

- **Key features**: CDP-native driver, thread-safe operations, stealth plugin, request hijacking, concurrent page pools.
- **When to use**: Scraping or automating sites with Go, headless browser for SPAs, stealth/anti-bot needs, migrating from chromedp or Playwright Go.

> **Try it:** "Automate logging into example.com with Go using go-rod and stealth."

### Registry

- **Total Skills**: 857 (from 856).
- **Generated files**: README, skills_index.json, catalog, and bundles synced.

### Credits

- **[@Wittlesus](https://github.com/Wittlesus)** - CursorRules Pro in Community Contributors (PR #81).
- **[@8hrsk](https://github.com/8hrsk)** - go-rod-master skill (PR #83).

---

_Upgrade now: `git pull origin main` to fetch the latest skills._

---

## [5.3.0] - 2026-02-13 - "Advanced Three.js & Modern Graphics"

> **Enhanced Three.js patterns: performance, visual polish, and production practices.**

This release significantly upgrades our 3D visualization capabilities with a comprehensive Three.js skill upgrade, focusing on CDN-compatible patterns, performance optimizations, and modern graphics techniques like shadows, fog, and GSAP integration.

### Added

- **Modern Three.js Patterns**: Comprehensive guide for `r128` (CDN) and production environments.
- **Visual Polish**: Advanced sections for shadows, environment maps, and tone mapping.
- **Interaction Models**: Custom camera controls (OrbitControls alternative) and raycasting for object selection.
- **Production Readiness**: Integration patterns for GSAP, scroll-based animations, and build tool optimizations.

### Registry

- **Total Skills**: 856.
- **Metadata**: Fixed missing source and risk fields for `threejs-skills`.
- **Sync**: All discovery artifacts (README, Catalog, Index) updated and synced.

### Contributors

- **[@Krishna-hehe](https://github.com/Krishna-hehe)** - Advanced Three.js skill overhaul (PR #78).

---

## [5.2.0] - 2026-02-13 - "Podcast Generation & Azure AI Skills"

> **New AI capabilities: Podcast Generation, Azure Identity, and Self-Evolving Agents.**

### Added

- **New Skill**: `podcast-generation` - Create multi-speaker podcasts from text/URLs using OpenAI Text-to-Speech (TTS) and pydub.
- **New Skill**: `weevolve` - Self-evolving knowledge engine with recursive improvement protocol.
- **Azure Skills Expansion**:
  - `azure-ai-agents-persistent-dotnet`: Persistent agent patterns for .NET.
  - `azure-ai-agents-persistent-java`: Persistent agent patterns for Java.
  - `azd-deployment`: Azure Developer CLI deployment strategies.
- **Python Enhancements**:
  - `pydantic-models-py`: Robust data validation patterns.
  - `fastapi-router-py`: Scalable API routing structures.

### Registry

- **Total Skills**: 856 (from 845).
- **Generated Files**: Synced `skills_index.json`, `data/catalog.json`, and `README.md`.

### Contributors

- **[@sickn33](https://github.com/sickn33)** - Podcast Generation & Azure skills sync (PR #74).
- **[@aro-brez](https://github.com/aro-brez)** - WeEvolve skill (Issue #75).

---

## [5.1.0] - 2026-02-12 - "Official Microsoft & Gemini Skills"

> **845+ skills: the largest single-PR expansion ever, powered by official vendor collections.**

Integrates the full official Microsoft skills collection (129 skills) and Google Gemini API development skills, significantly expanding Azure SDK coverage across .NET, Python, TypeScript, Java, and Rust, plus M365 Agents, Semantic Kernel, and wiki plugin skills.

### Added

- **129 Microsoft Official Skills** from [microsoft/skills](https://github.com/microsoft/skills):
  - Azure SDKs across .NET, Python, TypeScript, Java, and Rust
  - M365 Agents, Semantic Kernel, and wiki plugin skills
  - Flat structure using YAML `name` field as directory name
  - Attribution files: `docs/LICENSE-MICROSOFT`, `docs/microsoft-skills-attribution.json`
- **Gemini API Skills**: Official Gemini API development skill under `skills/gemini-api-dev/`
- **New Scripts & Tooling**:
  - `scripts/sync_microsoft_skills.py` (v4): Flat-structure sync with collision detection, stale cleanup, and attribution metadata
  - `scripts/tests/inspect_microsoft_repo.py`: Remote repo inspection
  - `scripts/tests/test_comprehensive_coverage.py`: Coverage verification
- **New npm scripts**: `sync:microsoft` and `sync:all-official` in `package.json`

### Fixed

- **`scripts/generate_index.py`**: Enhanced frontmatter parsing for unquoted `@` symbols and commas
- **`scripts/build-catalog.js`**: Deterministic `generatedAt` timestamp (prevents CI drift)

### Registry

- **Total Skills**: 845 (from 626). All generated files synced.

### Contributors

- [@ar27111994](https://github.com/ar27111994) - Microsoft & Gemini skills integration (PR #73)

---

## [5.0.0] - 2026-02-10 - "Antigravity Workflows Foundation"

> Workflows are now first-class: users can run guided, multi-skill playbooks instead of manually composing skills one by one.

### Added

- **New orchestration skill**: `antigravity-workflows`
  - `skills/antigravity-workflows/SKILL.md`
  - `skills/antigravity-workflows/resources/implementation-playbook.md`
- **New workflow documentation**: `docs/WORKFLOWS.md`
  - Introduces the Workflows model and differentiates it from Bundles.
  - Provides execution playbooks with prerequisites, ordered steps, and prompt examples.
- **New machine-readable workflow registry**: `data/workflows.json`
  - `ship-saas-mvp`
  - `security-audit-web-app`
  - `build-ai-agent-system`
  - `qa-browser-automation`

### Changed

- **README / Onboarding docs** updated to include Workflows discovery and usage:
  - `README.md` (TOC + "Antigravity Workflows" section)
  - `docs/GETTING_STARTED.md` (Bundles vs Workflows guidance)
  - `docs/FAQ.md` (new Q&A: Bundles vs Workflows)
- **Go browser automation alignment**:
  - Workflow playbooks now include optional `@go-playwright` hooks for Go-based QA/E2E flows.
- **Registry sync** after workflow skill addition:
  - `CATALOG.md`
  - `skills_index.json`
  - `data/catalog.json`
  - `data/bundles.json`

### Contributors

- [@sickn33](https://github.com/sickn33) - Workflows architecture, docs, and release integration

---

## [4.11.0] - 2026-02-08 - "Clean Code & Registry Stability"

> Quality improvements: Clean Code principles and deterministic builds.

### Changed

- **`clean-code` skill** - Complete rewrite based on Robert C. Martin's "Clean Code":
  - Systematic coverage: Meaningful names, functions, comments, formatting, objects, error handling, unit tests, and classes
  - Added F.I.R.S.T. test principles and Law of Demeter guidance
  - Fixed invalid heading format (`## ## When to Use` → `## When to Use`) that blocked validation
  - Added implementation checklist and code smell detection
- **Registry Stabilization** - Fixed `scripts/build-catalog.js` for deterministic CI builds:
  - Uses `SOURCE_DATE_EPOCH` environment variable for reproducible timestamps
  - Replaced `localeCompare` with explicit comparator for consistent sorting across environments
  - Prevents CI validation failures caused by timestamp drift

### Contributors

- [@jackjin1997](https://github.com/jackjin1997) - Clean Code skill update and registry fixes (PR #69, forged at [ClawForge](https://github.com/jackjin1997/ClawForge))

---

## [4.10.0] - 2026-02-06 - "Composio Automation + .NET Backend"

> A major expansion focused on practical app automation and stronger backend engineering coverage.

### Added

- **79 new skills total**.
- **78 Composio/Rube automation skills** (PR #64), with operational playbooks for:
- CRM and sales stacks (`HubSpot`, `Pipedrive`, `Salesforce`, `Zoho CRM`, `Close`).
- Collaboration and project tools (`Notion`, `ClickUp`, `Asana`, `Jira`, `Confluence`, `Trello`, `Monday`).
- Messaging and support channels (`Slack`, `Discord`, `Teams`, `Intercom`, `Freshdesk`, `Zendesk`).
- Marketing and analytics systems (`Google Analytics`, `Mixpanel`, `PostHog`, `Segment`, `Mailchimp`, `Klaviyo`).
- Infra/dev tooling (`GitHub`, `GitLab`, `CircleCI`, `Datadog`, `PagerDuty`, `Vercel`, `Render`).
- **1 new `dotnet-backend` skill** (PR #65) with:
- ASP.NET Core 8+ API patterns (Minimal APIs + controller-based).
- EF Core usage guidance, JWT auth examples, and background worker templates.
- Explicit trigger guidance and documented limitations.
- **Registry size increased to 713 skills** (from 634).

### Changed

- Regenerated and synced discovery artifacts after merging both PRs:
- `README.md` (counts + contributor updates)
- `skills_index.json`
- `CATALOG.md`
- `data/catalog.json`
- `data/bundles.json`
- `data/aliases.json`
- Release metadata updated for `v4.10.0`:
- `package.json` / `package-lock.json` version bump
- GitHub Release object published with release notes

### Contributors

- [@sohamganatra](https://github.com/sohamganatra) - 78 Composio automation skills (PR #64)
- [@Nguyen-Van-Chan](https://github.com/Nguyen-Van-Chan) - .NET backend skill (PR #65)

## [4.9.0] - 2026-02-05 - "OSS Hunter & Universal Skills"

> Automated contribution hunting and universal CLI AI skills (Audio, YouTube, Prompt Engineering).

### Added

- **New Skill**: `oss-hunter` – Automated tool for finding high-impact Open Source contributions (Good First Issues, Help Wanted) in trending repositories.
- **New Skill**: `audio-transcriber` – Transform audio recordings into professional Markdown with Whisper integration.
- **New Skill**: `youtube-summarizer` – Generate comprehensive summaries/notes from YouTube videos.
- **New Skill**: `prompt-engineer` (Enhanced) – Now includes 11 optimization frameworks (RTF, RISEN, etc.).
- **Registry**: 634 skills (from 626). Catalog regenerated.

### Changed

- **CLI AI Skills**: Merged core skills from `ericgandrade/cli-ai-skills`.

### Contributors

- [@jackjin1997](https://github.com/jackjin1997) - OSS Hunter (PR #61)
- [@ericgandrade](https://github.com/ericgandrade) - CLI AI Skills (PR #62)

## [4.7.0] - 2026-02-03 - "Installer Fix & OpenCode Docs"

> Critical installer fix for Windows and OpenCode documentation completion.

### Fixed

- **Installer**: Resolved `ReferenceError` for `tagArg` variable in `bin/install.js` ensuring correct execution on Windows/PowerShell (PR #53).

### Documentation

- **OpenCode**: Completed documentation for OpenCode integration in `README.md`.

---

## [4.6.0] - 2026-02-01 - "SPDD & Radix UI Design System"

> Agent workflow docs (SPDD) and Radix UI design system skill.

### Added

- **New Skill**: `radix-ui-design-system` – Build accessible design systems with Radix UI primitives (headless, theming, WCAG, examples).
- **Docs**: `skills/SPDD/` – Research, spec, and implementation workflow docs (1-research.md, 2-spec.md, 3-implementation.md).

### Registry

- **Total Skills**: 626 (from 625). Catalog regenerated.

---

## [4.5.0] - 2026-01-31 - "Stitch UI Design"

> Expert prompting guide for Google Stitch AI-powered UI design tool.

### Added

- **New Skill**: `stitch-ui-design` – Expert guide for creating effective prompts for Google Stitch AI UI design tool (Gemini 2.5 Flash). Covers prompt structure, specificity techniques, iteration strategies, design-to-code workflows, and 10+ examples for landing pages, mobile apps, and dashboards.

### Changed

- **Documentation**: Clarified in README.md and GETTING_STARTED.md that installation means cloning the full repo once; Starter Packs are curated lists to discover skills by role, not a different installation method (fixes [#44](https://github.com/sickn33/antigravity-awesome-skills/issues/44)).

### Registry

- **Total Skills**: 625 (from 624). Catalog regenerated.

### Credits

- [@ALEKGG1](https://github.com/ALEKGG1) – stitch-ui-design (PR #45)
- [@CypherPoet](https://github.com/CypherPoet) – Documentation clarity (#44)

---

## [4.4.0] - 2026-01-30 - "fp-ts skills for TypeScript"

> Three practical fp-ts skills for TypeScript functional programming.

### Added

- **New Skills** (from [whatiskadudoing/fp-ts-skills](https://github.com/whatiskadudoing/fp-ts-skills)):
  - `fp-ts-pragmatic` – Pipe, Option, Either, TaskEither without academic jargon.
  - `fp-ts-react` – Patterns for fp-ts with React 18/19 and Next.js 14/15 (state, forms, data fetching).
  - `fp-ts-errors` – Type-safe error handling with Either and TaskEither.

### Registry

- **Total Skills**: 624 (from 621). Catalog regenerated.

---

## [4.3.0] - 2026-01-29 - "VoltAgent Integration & Context Engineering Suite"

> 61 new skills from VoltAgent/awesome-agent-skills: official team skills and context engineering suite.

### Added

- **61 new skills** from [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills):
  - **Official (27)**: Sentry (commit, create-pr, find-bugs, iterate-pr), Trail of Bits (culture-index, fix-review, sharp-edges), Expo (expo-deployment, upgrading-expo), Hugging Face (hugging-face-cli, hugging-face-jobs), Vercel, Google Stitch (design-md), Neon (using-neon), n8n (n8n-code-python, n8n-mcp-tools-expert, n8n-node-configuration), SwiftUI, fal.ai (fal-audio, fal-generate, fal-image-edit, fal-platform, fal-upscale, fal-workflow), deep-research, imagen, readme.
  - **Community (34)**: Context suite (context-fundamentals, context-degradation, context-compression, context-optimization, multi-agent-patterns, memory-systems, evaluation), frontend-slides, linear-claude-skill, skill-rails-upgrade, terraform-skill, tool-design, screenshots, automate-whatsapp, observe-whatsapp, aws-skills, ui-skills, vexor, pypict-skill, makepad-skills, threejs-skills, claude-scientific-skills, claude-win11-speckit-update-skill, security-bluebook-builder, claude-ally-health, clarity-gate, beautiful-prose, claude-speed-reader, skill-seekers, varlock-claude-skill, superpowers-lab, nanobanana-ppt-skills, x-article-publisher-skill, ffuf-claude-skill.

### Registry

- **Total Skills**: 614 (from 553). Catalog and SOURCES.md updated.

### Credits

- VoltAgent/awesome-agent-skills and official teams (Sentry, Trail of Bits, Expo, Hugging Face, Vercel Labs, Google Labs, Neon, fal.ai).

---

## [4.0.0] - 2026-01-28 - "The Enterprise Era"

> **A massive integration of 300+ Enterprise skills, transforming Antigravity into a complete operating system for AI agents.**

### Added

- **Massive Skill Injection**: Merged 300+ Enterprise skills from `rmyndharis/antigravity-skills`.
- **New Categories**:
  - **Architecture & Design**: `backend-architect`, `c4-architecture`.
  - **Data & AI**: `rag-engineer`, `langchain-architecture`.
  - **Security**: `security-auditor`, `cloud-pentesting`.
- **Catalog System**: Introduced `CATALOG.md` and `scripts/build-catalog.js` for automated, table-based skill discovery.

### Changed

- **Documentation Overhaul**:
  - Removed the legacy 250+ row skill table from `README.md`.
  - Restructured `README.md` to focus on high-level domains.
  - Replaced static registry with dynamic `CATALOG.md`.
- **Version Bump**: Major version update to 4.0.0 reflecting the doubling of skill capacity (247 -> 550+).

### Credits

- **[@rmyndharis](https://github.com/rmyndharis)** - For the massive contribution of 300+ Enterprise skills and valid catalog logic.
- **[@sstklen](https://github.com/sstklen)** & **[@rookie-ricardo](https://github.com/rookie-ricard)** - Continued community support.

## [3.4.0] - 2026-01-27 - "Voice Intelligence & Categorization"

### Added

- **New Skill**: `voice-ai-engine-development` - Complete toolkit for building real-time voice agents (OpenAI Realtime, Vapi, Deepgram, ElevenLabs).
- **Categorization**: Major README update introducing a concise "Features & Categories" summary table.

### Changed

- **README**: Replaced text-heavy category lists with a high-level summary table.
- **Registry**: Synced generic skill count (256) across documentation.

### Contributors

- [@sickn33](https://github.com/sickn33) - Voice AI Engine (PR #33)
- [@community](https://github.com/community) - Categorization Initiative (PR #32)

## [3.3.0] - 2026-01-26 - "News & Research"

### Added

- **New Skills**:
  - `last30days`: Research any topic from the last 30 days on Reddit + X + Web.
  - `daily-news-report`: Generate daily news reports from multiple sources.

### Changed

- **Registry**: Updated `skills_index.json` and `README.md` registry (Total: 255 skills).

## [3.2.0] - 2026-01-26 - "Clarity & Consistency"

### Changed

- **Skills Refactoring**: Significant overhaul of `backend-dev-guidelines`, `frontend-design`, `frontend-dev-guidelines`, and `mobile-design`.
  - **Consolidation**: Merged fragmented documentation into single, authoritative `SKILL.md` files.
  - **Final Laws**: Introduced "Final Laws" sections to provide strict, non-negotiable decision frameworks.
  - **Simplification**: Removed external file dependencies to improve context retrieval for AI agents.

### Fixed

- **Validation**: Fixed critical YAML frontmatter formatting issues in `seo-fundamentals`, `programmatic-seo`, and `schema-markup` that were blocking strict validation.
- **Merge Conflicts**: Resolved text artifact conflicts in SEO skills.

## [3.1.0] - 2026-01-26 - "Stable & Deterministic"

### Fixed

- **CI/CD Drift**: Resolved persistent "Uncommitted Changes" errors in CI by making the index generation script deterministic (sorting by name + ID).
- **Registry Sync**: Synced `README.md` and `skills_index.json` to accurately reflect all 253 skills.

### Added (Registry Restore)

The following skills are now correctly indexed and visible in the registry:

- **Marketing & Growth**: `programmatic-seo`, `schema-markup`, `seo-fundamentals`, `form-cro`, `popup-cro`, `analytics-tracking`.
- **Security**: `windows-privilege-escalation`, `wireshark-analysis`, `wordpress-penetration-testing`, `writing-plans`.
- **Development**: `tdd-workflow`, `web-performance-optimization`, `webapp-testing`, `workflow-automation`, `zapier-make-patterns`.
- **Maker Tools**: `telegram-bot-builder`, `telegram-mini-app`, `viral-generator-builder`.

### Changed

- **Documentation**: Added `docs/CI_DRIFT_FIX.md` as a canonical reference for resolving drift issues.
- **Guidance**: Updated `docs/GETTING_STARTED.md` counts to match the full registry (253+ skills).
- **Maintenance**: Updated `MAINTENANCE.md` with strict protocols for handling generated files.

## [3.0.0] - 2026-01-25 - "The Governance Update"

### Added

- **Governance & Security**:
  - `docs/QUALITY_BAR.md`: Defined 5-point validation standard (Metadata, Risk, Triggers).
  - `docs/SECURITY_GUARDRAILS.md`: Enforced "Authorized Use Only" for offensive skills.
  - `CODE_OF_CONDUCT.md`: Adhered to Contributor Covenant v2.1.
- **Automation**:
  - `scripts/validate_skills.py`: Automated Quality Bar enforcement (Soft Mode supported).
  - `.github/workflows/ci.yml`: Automated PR checks.
  - `scripts/generate_index.py`: Registry generation with Risk & Source columns.
- **Experience**:
  - `docs/BUNDLES.md`: 9 Starter Packs (Essentials, Security, Web, Agent, Game Dev, DevOps, Data, Testing, Creative).
  - **Interactive Registry**: README now features Risk Levels (🔴/🟢/🟣) and Collections.
- **Documentation**:
  - `docs/EXAMPLES.md`: Cookbook with 3 real-world scenarios.
  - `docs/SOURCES.md`: Legal ledger for attributions and licenses.
  - Release announcements are documented in this CHANGELOG.

### Changed

- **Standardization**: All 250+ skills are now validated against the new Quality Bar schema.
- **Project Structure**: Introduced `docs/` folder for scalable documentation.

## [2.14.0] - 2026-01-25 - "Web Intelligence & Windows"

### Added

- **New Skill**:
  - `context7-auto-research`: Auto-research capability for Claude Code.
  - `codex-review`: Professional code review with AI integration.
  - `exa-search`: Semantic search and discovery using Exa API.
  - `firecrawl-scraper`: Deep web scraping and PDF parsing.
  - `tavily-web`: Content extraction and research using Tavily.
  - `busybox-on-windows`: UNIX tool suite for Windows environments.

### Changed

- **Documentation**: Updated `obsidian-clipper-template-creator` docs and templates.
- **Index & Registry**: Updated `skills_index.json` and `README.md` registry.

### Fixed

- **Skills**: Fixed YAML frontmatter quoting in `lint-and-validate`.

## [2.13.0] - 2026-01-24 - "NoSQL Expert"

### Added

- **New Skill**:
  - `nosql-expert`: Expert guidance for distributed NoSQL databases (Cassandra, DynamoDB), focusing on query-first modeling and anti-patterns.

### Changed

- **Index & Registry**: Updated `skills_index.json` and `README.md` registry.

### Contributors

- [@sickn33](https://github.com/sickn33) - PR #23

## [2.12.0] - 2026-01-23 - "Enterprise & UI Power"

### Added

- **New Skills**:
  - `production-code-audit`: Comprehensive enterprise auditing skill for production readiness.
  - `avalonia-layout-zafiro`: Zafiro layout guidelines for Avalonia UI.
  - `avalonia-viewmodels-zafiro`: ViewModel composition patterns for Avalonia.
  - `avalonia-zafiro-development`: Core development rules for Avalonia Zafiro applications.

### Changed

- **Index & Registry**: Updated `skills_index.json` and `README.md` registry (Total: 243 skills).

### Contributors

- [@SuperJMN](https://github.com/SuperJMN) - PR #20
- [@Mohammad-Faiz-Cloud-Engineer](https://github.com/Mohammad-Faiz-Cloud-Engineer) - PR #21

## [2.11.0] - 2026-01-23 - "Postgres Performance"

### Added

- **New Skill**:
  - `postgres-best-practices`: Comprehensive Supabase PostgreSQL performance optimization guide with 30+ rules covering query performance, connection management, RLS security, schema design, locking, and monitoring.

### Changed

- **Official Sources**: Added [supabase/agent-skills](https://github.com/supabase/agent-skills) to Credits & Sources.
- **Index & Registry**: Updated `skills_index.json` and `README.md` registry (Total: 239 skills).

### Contributors

- [@ar27111994](https://github.com/ar27111994) - PR #19

---

## [2.10.0] - 2026-01-22 - "Developer Excellence"

### Added

- **New Skills**:
  - `api-security-best-practices`: Comprehensive guide for secure API design and defense.
  - `environment-setup-guide`: Systematic approach to project onboarding and tool configuration.
  - `web-performance-optimization`: Methodologies for optimizing Core Web Vitals and loading speed.

### Changed

- **Enhanced Skill**:
  - `code-review-checklist`: Replaced with a much more detailed and systematic version covering functionality, security, and quality.

### Fixed

- **Index & Registry**: Updated `skills_index.json` and `README.md` registry (Total: 238 skills).

### Added

- **Automation Support**:
  - `scripts/update_readme.py`: Automated script to sync skill counts and regenerate the registry table.
  - Updated `MAINTENANCE.md` to reflect the new automated workflow.
- **Repository Quality**:
  - `MAINTENANCE.md` is now tracked in the repository (removed from `.gitignore`).
  - Improved contribution guidelines.

## [2.8.0] - 2026-01-22 - "Documentation Power"

### Added

- **API Documentation Generator**: New skill to automatically generate comprehensive API documentation (`skills/api-documentation-generator`).
- **Remotion Best Practices**: 28 modular rules for programmatic video creation (`skills/remotion-best-practices`).

## [2.7.0] - 2026-01-22 - "Agent Memory"

### Added

- **Agent Memory MCP**: New skill providing persistent, searchable knowledge management for AI agents (`skills/agent-memory-mcp`).

### Changed

- **Renamed Skill**: `agent-memory` was renamed to `agent-memory-mcp` to avoid naming conflicts.

---

## [2.6.0] - 2026-01-21 - "Everything Skills Edition"

### Added

- **8 Verified Skills** from [affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code):
  - `cc-skill-backend-patterns`
  - `cc-skill-clickhouse-io`
  - `cc-skill-coding-standards`
  - `cc-skill-continuous-learning`
  - `cc-skill-frontend-patterns`
  - `cc-skill-project-guidelines-example`
  - `cc-skill-security-review`
  - `cc-skill-strategic-compact`
- **Documentation**: New `docs/WALKTHROUGH.md` for import process details.

### Changed

- **Skill Cleanup**: Removed 27 unwanted agents, commands, and rules from the `everything-claude-code` import to focus strictly on skills.
- **Index**: Regenerated `skills_index.json` (Total: 233 skills).
- **Credits**: Updated README credits and registry.

## [1.0.0] - 2026-01-19 - "Marketing Edition"

### Added

- **23 Marketing & Growth skills** from [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills):
  - **CRO**: `page-cro`, `signup-flow-cro`, `onboarding-cro`, `form-cro`, `popup-cro`, `paywall-upgrade-cro`
  - **Content**: `copywriting`, `copy-editing`, `email-sequence`
  - **SEO**: `seo-audit`, `programmatic-seo`, `schema-markup`, `competitor-alternatives`
  - **Paid**: `paid-ads`, `social-content`
  - **Growth**: `referral-program`, `launch-strategy`, `free-tool-strategy`
  - **Analytics**: `ab-test-setup`, `analytics-tracking`
  - **Strategy**: `pricing-strategy`, `marketing-ideas`, `marketing-psychology`
- New "Marketing & Growth" category in Features table

### Changed

- Total skills count: **179**

---

## [0.7.0] - 2026-01-19 - "Education Edition"

### Added

- **Moodle External API Development** skill via PR #6
- Comprehensive Moodle LMS web service API development

### Changed

- Total skills count: **156**

---

## [0.6.0] - 2026-01-19 - "Vibeship Integration"

### Added

- **57 skills** from [vibeforge1111/vibeship-spawner-skills](https://github.com/vibeforge1111/vibeship-spawner-skills):
  - AI Agents category (~30 skills)
  - Integrations & APIs (~25 skills)
  - Maker Tools (~11 skills)
- Alphabetically sorted skill registry

### Changed

- Total skills count: **155**

---

## [0.5.0] - 2026-01-18 - "Agent Manager"

### Added

- **Agent Manager Skill** - Multi-agent orchestration via tmux
- Major repository expansion with community contributions

### Changed

- Total skills count: **131**

---

## [0.4.0] - 2026-01-18 - "Security Fortress"

### Added

- **60+ Cybersecurity skills** from [zebbern/claude-code-guide](https://github.com/zebbern/claude-code-guide):
  - Ethical Hacking Methodology
  - Metasploit Framework
  - Burp Suite Testing
  - SQLMap, Active Directory, AWS Pentesting
  - OWASP Top 100 Vulnerabilities
  - Red Team Tools
- `claude-code-guide` skill

### Changed

- Total skills count: ~90

---

## [0.3.0] - 2026-01-17 - "First Stable Registry"

### Added

- Complete skill registry table in README
- GitHub workflow automation
- SEO optimizations

### Changed

- Total skills count: **71**

---

## [0.2.0] - 2026-01-16 - "Official Skills"

### Added

- **Official Anthropic skills** integration
- **Vercel Labs skills** integration
- BlockRun: Agent Wallet for LLM Micropayments
- 7 new skills from GitHub analysis

### Changed

- Total skills count: **~65**

---

## [0.1.0] - 2026-01-15 - "Initial Release"

### Added

- **58 core skills** aggregated from community:
  - [obra/superpowers](https://github.com/obra/superpowers) - Original Superpowers
  - [guanyang/antigravity-skills](https://github.com/guanyang/antigravity-skills) - Core extensions
  - [diet103/claude-code-infrastructure-showcase](https://github.com/diet103/claude-code-infrastructure-showcase) - Infrastructure skills
  - [ChrisWiles/claude-code-showcase](https://github.com/ChrisWiles/claude-code-showcase) - React UI patterns
  - [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) - Loki Mode
  - [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) - Senior Engineering
- Universal **SKILL.md** format
- Compatibility with Claude Code, Gemini CLI, Cursor, Copilot, Antigravity

---

## Credits

See [README.md](README.md#credits--sources) for full attribution.

## License

MIT License - See [LICENSE](LICENSE) for details.
