# Handoff prompt: next Claude Code session

Paste everything below the line into a new Claude Code session opened in `D:\POLICYNEST_SOURCE_PACKAGE\POLICYNEST_SOURCE_PACKAGE`.

---

You are picking up the PolicyNest MVP: AI-first onboarding for POSP insurance agents, built for the Masters' Union PS-01 challenge. The live site is https://policynest.embarko.app.

## Read first, in this order

1. `CLAUDE.md`: architecture, my standing decisions, deploy steps, CSP constraints. Keep to every decision listed there.
2. `PRODUCT.md`: the product spec. Every functional goal is marked Built / Partial / Not built / Future, alongside the T1–T10 results and the success metrics. Section 8 lists the known gaps in priority order.
3. `01_ORIGINAL_CHALLENGE/PS-01_CHALLENGE_BRIEF.md` and `03_RULEBOOK_AND_REGULATIONS/PS-01_ONBOARDING_RULEBOOK_V3_2.md`: the source of truth for requirements.
4. `07_WORKFLOW_AND_BUSINESS_LOGIC/05_OPS_REVIEWER_COCKPIT_SPECIFICATION.md` and `07_FRONTEND_REQUIREMENTS_SPECIFICATION.md`: specs for the reviewer queue and the UI.
5. `eval/EVALUATION_REPORT.md`: measured numbers. They are in-sample; always say so.

## Phase 1: Use the installed skills to audit and plan

These skills are installed in `~/.claude/skills/`. Invoke each one with the Skill tool against this project and record what it finds.

| Skill | Run it on | Feeds gap (PRODUCT.md §8) |
|---|---|---|
| `web-design-guidelines` | `policynest_mvp/PolicyNest.html` (UI code) | Review-console redesign (R7), overall quality |
| `accessibility` | The live site in the browser: keyboard pass, accessibility tree, contrast, 24 px tap targets, phone width | Phone-first applicants |
| `kpi-dashboard-design` | The reviewer queue and ops lead view (R6) | Multi-case reviewer queue |
| `usability-testing` | A test plan: 5 people playing applicants, 2 playing reviewers, measuring the ≥ 4/5 clarity target | Stage 3 usability tests |
| `find-skills` | Only if a gap above has no skill. Node is not installed, so search skills.sh in the browser instead of `npx`. | — |

`frontend-design` is also available, through the plugin.

Then write a **plan** with one section per gap in PRODUCT.md §8. Each section gives:

- what changes, and which files;
- which skill finding it answers;
- how it will be verified in the browser;
- the risk to the engine block and to the evaluation.

Do not change code in this phase.

## Phase 2: `/mattpocock-skills:to-spec` with a detailed plan audit

Run `/mattpocock-skills:to-spec` on the Phase 1 plan to turn it into a spec. Audit the plan line by line against:

- the brief's Must have / Should have list and the T1–T10 scenarios;
- the rulebook: every Human-only decision still routes to a person, and every decision cites its rule;
- the guardrails: DPDP Act, no full Aadhaar anywhere, no fraud wording to applicants, prefer NEEDS_MORE_INFO when unsure;
- my standing decisions in CLAUDE.md: one ideal case, no API keys, real OCR with per-slot type gates, both themes, the review console redesigned only from my references;
- PRODUCT.md statuses: flag any item the plan would move to Built without a way to verify it.

The audit output is a table: plan item → requirement it serves → pass / gap / conflict → fix.

## Phase 3: `/mattpocock-skills:grill-with-docs`

Grill me on the spec, using the docs above as the reference. Work in rounds:

- Each round asks only the questions that don't depend on another open answer.
- Number every question and give your recommended answer, worded so "yes" accepts it.
- Look up facts yourself; ask me only for decisions.

Stop when nothing is left assumed. Then update `PRODUCT.md` (and `CLAUDE.md` if a standing decision changed) and wait for my go-ahead before building.

## If a skill is missing

`to-spec` and `grill-with-docs` were not installed in the previous session; only the Matt Pocock `grilling` skill was. Check the skills list first.

- **If either is missing,** tell me in one line. Then do that phase by hand to the same standard: for `to-spec`, write the spec and audit table yourself; for `grill-with-docs`, use `mattpocock-skills:grilling` with the docs as the reference.
- **Don't install anything** without asking me first.

## Ground rules

- Never invent numbers. Label anything simulated or in-sample.
- Never open or publish the files in `05_SPECIMEN_DOCUMENTS/sample_specimens`. They may be real people's documents.
- The deploy token is at `~/.embarko/credentials`. Never print it.
- On Windows, `tar` needs `--force-local` for paths containing `C:`.
- After any source change: run `python policynest_mvp/build_site.py`, deploy, then test on the live site.
