---
name: analyze-project
description: Forensic root cause analyzer for Antigravity sessions. Classifies scope deltas, rework patterns, root causes, hotspots, and auto-improves prompts/health.
version: "1.0"
tags: [analysis, diagnostics, meta, root-cause, project-health, session-review]
---

# /analyze-project — Root Cause Analyst Workflow

Analyze AI-assisted coding sessions in `brain/` and produce a diagnostic report that explains not just **what happened**, but **why it happened**, **who/what caused it**, and **what should change next time**.

This workflow is not a simple metrics dashboard.
It is a forensic analysis workflow for AI coding sessions.

---

## Primary Objective

For each session, determine:

1. What changed from the initial ask to the final executed work
2. Whether the change was caused primarily by:
   - the user/spec
   - the agent
   - the codebase/repo
   - testing/verification
   - legitimate task complexity
3. Whether the original prompt was sufficient for the actual job
4. Which subsystems or files repeatedly correlate with struggle
5. What concrete changes would most improve future sessions

---

## Core Principles

- Treat `.resolved.N` counts as **signals of iteration intensity**, not proof of failure
- Do not label struggle based on counts alone; classify the **shape** of rework
- Separate **human-added scope** from **necessary discovered scope**
- Separate **agent error** from **repo friction**
- Every diagnosis must include **evidence**
- Every recommendation must map to a specific observed pattern
- Use confidence levels:
  - **High** = directly supported by artifact contents or timestamps
  - **Medium** = supported by multiple indirect signals
  - **Low** = plausible inference, not directly proven

---

## Step 1: Discovery — Find Relevant Conversations

1. Read the conversation summaries available in the system context.
2. List all subdirectories in:
   `~/.gemini/antigravity/brain/
3. Build a **Conversation Index** by cross-referencing summaries with UUID folders.
4. Record for each conversation:
   - `conversation_id`
   - `title`
   - `objective`
   - `created`
   - `last_modified`
5. If the user supplied a keyword/path, filter on that. Otherwise analyze all workspace conversations.

> Output: indexed list of conversations to analyze.

---

## Step 2: Artifact Extraction — Build Session Evidence

For each conversation, read all structured artifacts that exist.

### 2a. Core Artifacts
- `task.md`
- `implementation_plan.md`
- `walkthrough.md`

### 2b. Metadata
- `*.metadata.json`

### 2c. Version Snapshots
- `task.md.resolved.0 ... N`
- `implementation_plan.md.resolved.0 ... N`
- `walkthrough.md.resolved.0 ... N`

### 2d. Additional Signals
- other `.md` artifacts
- report/evaluation files
- timestamps across artifact updates
- file/folder names mentioned in plans and walkthroughs
- repeated subsystem references
- explicit testing/validation language
- explicit non-goals or constraints, if present

### 2e. Record Per Conversation

#### Presence / Lifecycle
- `has_task`
- `has_plan`
- `has_walkthrough`
- `is_completed`
- `is_abandoned_candidate` = has task but no walkthrough

#### Revision / Change Volume
- `task_versions`
- `plan_versions`
- `walkthrough_versions`
- `extra_artifacts`

#### Scope
- `task_items_initial`
- `task_items_final`
- `task_completed_pct`
- `scope_delta_raw`
- `scope_creep_pct_raw`

#### Timing
- `created_at`
- `completed_at`
- `duration_minutes`

#### Content / Quality Signals
- `objective_text`
- `initial_plan_summary`
- `final_plan_summary`
- `initial_task_excerpt`
- `final_task_excerpt`
- `walkthrough_summary`
- `mentioned_files_or_subsystems`
- `validation_requirements_present`
- `acceptance_criteria_present`
- `non_goals_present`
- `scope_boundaries_present`
- `file_targets_present`
- `constraints_present`

---

## Step 3: Prompt Sufficiency Analysis

For each conversation, score the opening objective/request on a 0–2 scale for each dimension:

- **Clarity** — is the ask understandable?
- **Boundedness** — are scope limits defined?
- **Testability** — are success conditions or acceptance criteria defined?
- **Architectural specificity** — are files/modules/systems identified?
- **Constraint awareness** — are non-goals, constraints, or environment details included?
- **Dependency awareness** — does the prompt acknowledge affected systems or hidden coupling?

Create:
- `prompt_sufficiency_score`
- `prompt_sufficiency_band` = High / Medium / Low

Then note which missing ingredients likely contributed to later friction.

Important:
Do not assume a low-detail prompt is bad by default.
Short prompts can still be good if the task is narrow and the repo context is obvious.

---

## Step 4: Scope Change Classification

Do not treat all scope growth as the same.

For each conversation, classify scope delta into:

### 4a. Human-Added Scope
New items clearly introduced beyond the initial ask.
Examples:
- optional enhancements
- follow-on refactors
- “while we are here” additions
- cosmetic or adjacent work added later

### 4b. Necessary Discovered Scope
Work that was not in the opening ask but appears required to complete it correctly.
Examples:
- dependency fixes
- required validation work
- hidden integration tasks
- migration fallout
- coupled module updates

### 4c. Agent-Introduced Scope
Work that appears not requested and not necessary, likely introduced by agent overreach.

For each conversation record:
- `scope_change_type_primary`
- `scope_change_type_secondary` (optional)
- `scope_change_confidence`
- evidence for classification

---

## Step 5: Rework Shape Analysis

Do not just count revisions. Determine the **shape** of session rework.

Classify each conversation into one of these patterns:

- **Clean execution** — little change, smooth completion
- **Early replan then stable finish** — plan changed early, then execution converged
- **Progressive scope expansion** — work kept growing throughout the session
- **Reopen/reclose churn** — repeated task adjustments/backtracking
- **Late-stage verification churn** — implementation mostly done, but testing/validation caused loops
- **Abandoned mid-flight** — work started but did not reach walkthrough
- **Exploratory / research session** — iterations are high but expected due to problem discovery

Record:
- `rework_shape`
- `rework_shape_confidence`
- supporting evidence

---

## Step 6: Root Cause Analysis

For every non-clean session, assign:

### 6a. Primary Root Cause
Choose one:
- `SPEC_AMBIGUITY`
- `HUMAN_SCOPE_CHANGE`
- `REPO_FRAGILITY`
- `AGENT_ARCHITECTURAL_ERROR`
- `VERIFICATION_CHURN`
- `LEGITIMATE_TASK_COMPLEXITY`

### 6b. Secondary Root Cause
Optional if a second factor materially contributed.

### 6c. Evidence Requirements
Every root cause assignment must include:
- evidence from artifacts or metadata
- why competing causes were rejected
- confidence level

### 6d. Root Cause Heuristics

#### SPEC_AMBIGUITY
Use when the opening ask lacked boundaries, targets, criteria, or constraints, and the plan had to invent them.

#### HUMAN_SCOPE_CHANGE
Use when the task set expanded due to new asks, broadened goals, or post-hoc additions.

#### REPO_FRAGILITY
Use when hidden coupling, unclear architecture, brittle files, or environmental issues forced extra work.

#### AGENT_ARCHITECTURAL_ERROR
Use when the agent chose the wrong approach, wrong files, wrong assumptions, or hallucinated structure.

#### VERIFICATION_CHURN
Use when implementation mostly succeeded but tests, validation, QA, or fixes created repeated loops.

#### LEGITIMATE_TASK_COMPLEXITY
Use when revisions were reasonable given the difficulty and do not strongly indicate avoidable failure.

---

## Step 7: Subsystem / File Clustering

Across all conversations, cluster repeated struggle by subsystem, folder, or file mentions.

Examples:
- `frontend/auth/*`
- `db.py`
- `ui.py`
- `video_pipeline/*`

For each cluster, calculate:
- number of conversations touching it
- average revisions
- completion rate
- abandonment rate
- common root causes

Output the top recurring friction zones.

Goal:
Identify whether struggle is prompt-driven, agent-driven, or concentrated in specific repo areas.

---

## Step 8: Comparative Cohort Analysis

Compare these cohorts:

- first-shot successes vs re-planned sessions
- completed vs abandoned
- high prompt sufficiency vs low prompt sufficiency
- narrow-scope vs high-scope-growth
- short sessions vs long sessions
- low-friction subsystems vs high-friction subsystems

For each comparison, identify:
- what differs materially
- which prompt traits correlate with smoother execution
- which repo traits correlate with repeated struggle

Do not merely restate averages.
Extract causal-looking patterns cautiously and label them as inference where appropriate.

---

## Step 9: Non-Obvious Findings

Generate 3–7 findings that are not simple metric restatements.

Good examples:
- “Most replans happen in sessions with weak file targeting, not weak acceptance criteria.”
- “Scope growth usually begins after the first successful implementation, suggesting post-success human expansion.”
- “Auth-related sessions cluster around repo fragility rather than agent hallucination.”
- “Abandoned work is strongly associated with missing validation criteria.”

Bad examples:
- “Some sessions had many revisions.”
- “Some sessions were longer than others.”

Each finding must include:
- observation
- why it matters
- evidence
- confidence

---

## Step 10: Report Generation

Create `session_analysis_report.md` in the current conversation’s brain folder.

Use this structure:

# 📊 Session Analysis Report — [Project Name]

**Generated**: [timestamp]
**Conversations Analyzed**: [N]
**Date Range**: [earliest] → [latest]

---

## Executive Summary

| Metric | Value | Rating |
|:---|:---|:---|
| First-Shot Success Rate | X% | 🟢/🟡/🔴 |
| Completion Rate | X% | 🟢/🟡/🔴 |
| Avg Scope Growth | X% | 🟢/🟡/🔴 |
| Replan Rate | X% | 🟢/🟡/🔴 |
| Median Duration | Xm | — |
| Avg Revision Intensity | X | 🟢/🟡/🔴 |

Then include a short narrative summary:
- what is going well
- what is breaking down
- whether the main issue is prompt quality, repo fragility, or workflow discipline

---

## Root Cause Breakdown

| Root Cause | Count | % | Notes |
|:---|:---|:---|:---|
| Spec Ambiguity | X | X% | ... |
| Human Scope Change | X | X% | ... |
| Repo Fragility | X | X% | ... |
| Agent Architectural Error | X | X% | ... |
| Verification Churn | X | X% | ... |
| Legitimate Task Complexity | X | X% | ... |

---

## Prompt Sufficiency Analysis

- common traits of high-sufficiency prompts
- common missing inputs in low-sufficiency prompts
- which missing prompt ingredients correlate most with replanning or abandonment

---

## Scope Change Analysis

Separate:
- Human-added scope
- Necessary discovered scope
- Agent-introduced scope

Show top offenders in each category.

---

## Rework Shape Analysis

Summarize how sessions tend to fail:
- early replan then recover
- progressive scope expansion
- late verification churn
- abandonments
- reopen/reclose cycles

---

## Friction Hotspots

Cluster repeated struggle by subsystem/file/domain.
Show which areas correlate with:
- replanning
- abandonment
- verification churn
- agent architectural mistakes

---

## First-Shot Successes

List the cleanest sessions and extract what made them work:
- scope boundaries
- acceptance criteria
- file targeting
- validation clarity
- narrowness of change surface

---

## Non-Obvious Findings

List 3–7 high-value findings with evidence and confidence.

---

## Recommendations

Each recommendation must use this format:

### Recommendation [N]
- **Observed pattern**
- **Likely cause**
- **Evidence**
- **Change to make**
- **Expected benefit**
- **Confidence**

Recommendations must be specific, not generic.

---

## Per-Conversation Breakdown

| # | Title | Duration | Scope Δ | Plan Revs | Task Revs | Root Cause | Rework Shape | Complete? |
|:---|:---|:---|:---|:---|:---|:---|:---|:---|

Add short notes only where meaningful.

---

## Step 11: Auto-Optimize — Improve Future Sessions

### 11a. Update Project Health State
# Example path (update to your actual location):
# `~/.gemini/antigravity/.agent/skills/project-health-state/SKILL.md`

Update:
- session analysis metrics
- recurring fragile files/subsystems
- recurring failure modes
- last updated timestamp

### 11b. Generate Prompt Improvement Guidance
Create `prompt_improvement_tips.md`

Do not give generic advice.
Instead extract:
- traits of high-sufficiency prompts
- examples of effective scope boundaries
- examples of good acceptance criteria
- examples of useful file targeting
- common missing details that led to replans

### 11c. Suggest Missing Skills / Workflows
If multiple struggle sessions cluster around the same subsystem or repeated sequence, recommend:
- a targeted skill
- a repeatable workflow
- a reusable prompt template
- a repo note / architecture map

Only recommend workflows when the pattern appears repeatedly.

---

## Final Output Standard

The workflow must produce:
1. A metrics summary
2. A root-cause diagnosis
3. A subsystem/friction map
4. A prompt-sufficiency assessment
5. Evidence-backed recommendations
6. Non-obvious findings

If evidence is weak, say so.
Do not overclaim.
Prefer explicit uncertainty over fake precision.








**How to invoke this skill**  
Just say any of these in a new conversation:
- “Run analyze-project on the workspace”
- “Do a full session analysis report”
- “Root cause my recent brain/ sessions”
- “Update project health state”

The agent will automatically discover and use the skill.
