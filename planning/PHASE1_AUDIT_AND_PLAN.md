# Phase 1: skill audit and plan

Written 14 Nov 2026. No code was changed in this phase. Live site audited: https://policynest.embarko.app (build of 14 Nov).

## Skills run

| Skill | Run on | How |
|---|---|---|
| `web-design-guidelines` | `policynest_mvp/PolicyNest.html` | Fetched the current Vercel rules; searched the source for each rule |
| `accessibility` | Live site, built-in browser | In-page checks of names, contrast (WCAG ratios), target sizes and horizontal scroll on all five views in both themes at 1280 px and 375 px; real Tab presses with a focus log. No Lighthouse or axe was available, so treat this as a manual audit: passing it is not WCAG conformance |
| `kpi-dashboard-design` | R6 queue and the ops-lead view | Framework applied to brief Table 4 and the cockpit spec; data sources checked |
| `usability-testing` | Stage 3 tests | Principles applied to a 5 + 2 test plan |
| `find-skills` | Not run | Every gap had a skill or needs none |
| `frontend-design` | Not run yet | Reserved for R7, once your references arrive |

## Findings

### web-design-guidelines (source)

```text
PolicyNest.html:1056,1099 - file input hidden as 1x1 px; its <label class="btn"> gets no focus style → keyboard focus invisible on every upload (confirmed live)
PolicyNest.html:425 - aria-live="polite" on the whole #view-apply section → every re-render is read out; announce a short status line instead
PolicyNest.html:890 - sidebar navigation uses <button data-view>; navigation should be <a href="#apply"> (Ctrl+click, middle-click, right-click to copy)
PolicyNest.html:404-431 - no skip link; 5 sidebar stops before content on every view
PolicyNest.html:1-3 - no <meta name="theme-color">; no <link rel="preconnect"> for fonts.googleapis.com / fonts.gstatic.com / CDN
PolicyNest.html:357 - outline:0 on .sp.now .sc (stepper dot, not focusable: low impact)
PolicyNest.html:112 - :focus used for inputs (OK, ring present); global :focus-visible at :23 is good
PolicyNest.html:1429 - reviewer note: placeholder should end with … ; field is a one-line <input> for a free-text note (use <textarea>)
PolicyNest.html:1016 - typed fields: name/email lack spellcheck=false on PAN/IFSC/email; email lacks autocomplete="email", mobile lacks autocomplete="tel"
PolicyNest.html - no beforeunload warning, while a refresh silently discards the whole application (by design: "no state is kept")
PolicyNest.html - no touch-action:manipulation, no -webkit-tap-highlight-color
PolicyNest.html - URL holds the view only (#apply), not the step or the reviewer case: no deep links to a case
✓ transition: all, user-scalable=no, onPaste blocking, div/span click handlers, images without alt, prefers-reduced-motion, color-scheme, safe-area insets, text-wrap:balance, form labels
```

### accessibility (live site)

| # | Finding | WCAG | Severity | Evidence |
|---|---|---|---|---|
| A-1 | Upload buttons: keyboard focus invisible (input is 1×1 px, label has no focus style) | 2.4.7 | Critical | `#up-PAN` focused, size 1×1, label outline none |
| A-2 | White text on brand orange `#FF6B1A`: 2.85:1 light, 2.60:1 dark (needs 4.5:1) | 1.4.3 | Critical | `.chip.o`, `.ic` doc tiles, stepper number `.sc`, evaluation diagonal `.h.diag` |
| A-3 | Amber "DRAFT" pill `#B7791F` on `#FDF2D8`: 3.27:1; grey chip `#5D626B` on `#F3F4F6`: 2.85–3.07:1 | 1.4.3 | Serious | `.pill.info`, `.chip`, `.chip.w` |
| A-4 | Toast Dismiss button 16×21 px | 2.5.8 | Serious | below 24×24 |
| A-5 | Heading levels skip: h1 → h3 on the Documents step | 1.3.1 | Moderate | |
| A-6 | No skip link | 2.4.1 | Moderate | focus log |
| A-7 | Whole Application view is a live region | 4.1.3 | Moderate | over-announcement |
| A-8 | Phone (375 px): sticky top bar is 129 px, 16% of an 812 px screen; content starts at ~255 px | 2.4.11 (risk) | Moderate | no focused field was hidden in the test, but little margin |
| ✓ | lang="en", landmarks (aside/nav/header/main), every control named, theme toggle labelled, focus order logical, no horizontal scroll at 375 px, no target under 24 px except A-4, both themes otherwise pass | | | |

Not tested: screen reader (NVDA), 200% zoom, Windows high contrast. Contrast on gradient cards (6 elements) could not be measured automatically.

### kpi-dashboard-design (R6)

- An operational dashboard: daily or real-time, for the team; **5–7 KPIs**, each with a target, a comparison and the method shown on the card; drill down from queue to case.
- Brief Table 4 asks the ops lead for: **queue age, AI decision mix, overrides, drop-off by stage.**
- **Data reality (checked):** the engine sends **11 of 600** test applications to a person, all different-person names (NAME_MISMATCH). The test set has **no** face scores 0.60–0.75, **no** surname changes and **no** unlisted boards. A queue seeded only from the test set is therefore 11 cases of one kind.
- Queue age, reviewer minutes and overrides have **no real source**. They can come only from this browser session or be labelled simulated. `stage_events.csv` gives real (synthetic data pack) drop-off by stage for *today's* process; `ops_team.csv` gives 22 reviewers with speed index and cost.
- Cockpit spec (§2) asks for F1/F2/F3 hotkeys, an SLA countdown and click-a-field-to-highlight-the-box. F1 opens browser help on Windows, and bounding boxes are not kept (raw OCR is not stored), so both need a decision.

### usability-testing (Stage 3)

- Goal: find friction (applicants, reviewers) **and** measure one number: clarity of the follow-up message, target ≥ 4/5 from five real users.
- Fidelity: the production site with specimen variants. No Wizard of Oz needed.
- **Watch, don't ask:** tasks with think-aloud; ask "why" only when someone leaves the expected path.
- **Test two options, not one:** rate two wordings of the same follow-up (current vs a plainer one), in random order.
- **Zero skin in the game:** participants should not be classmates on the team; at least two should match the POSP profile (shopkeeper, homemaker, phone-first, Hindi-comfortable).

## Plan, one section per gap (PRODUCT.md §8)

Engine block = lines between `ENGINE:START` and `ENGINE:END` in `PolicyNest.html` (currently lines 502–781). **Node is not installed on this machine**, so `eval/run_eval.js` cannot be re-run here today. Any engine change needs either Node installed (your OK) or a browser harness that runs the same engine block.

### Gap 0 (cross-cutting): fixes from the audits

- **Changes** (`PolicyNest.html` CSS and UI code, outside the engine): A-1 focus ring on upload labels (`.vbtns:has(input:focus-visible) label`); A-2/A-3 text-on-orange to dark ink or a darker orange shade for text-bearing fills, amber/grey chips darkened to ≥ 4.5:1; A-4 toast button 24×24; A-5 h2 for document cards; A-6 skip link; A-7 live region narrowed to one status line; A-8 compact top bar under 600 px; nav as `<a href="#…">`; theme-color and preconnect; a `beforeunload` warning once an application has data; `autocomplete`/`spellcheck` on fields; reviewer note as `<textarea>`.
- **Answers:** web-design-guidelines and accessibility findings above.
- **Verify in browser:** re-run the same in-page audit script on all five views, both themes, 1280 and 375 px (expect zero contrast fails outside gradients, zero targets < 24 px); Tab through Documents and see a ring on each upload; reload with data and see the browser's leave warning.
- **Risk:** engine none; evaluation none. **Design risk:** A-2 changes how the brand orange is used, a visual decision that is yours.

### Gap 1: usability tests (5 applicants, 2 reviewers)

- **Changes:** new `planning/USABILITY_TEST_PLAN.md` (script, tasks, consent, rating sheet). Optional small UI change: a second wording of the follow-up message for the A/B rating, and a "copy message" button. No backend: ratings go on a paper or form sheet, not into the app (no state is kept).
- **Applicant tasks:** (1) clean case to certificate; (2) T5 blurry marksheet + parent's cheque: read the message, say what you would do, rate clarity 1–5 for wording A and B; (3) T6 rejection: explain in your words why; (4) find where your application stands. **Reviewer tasks:** T4 different person, T8 face 0.68, a dispute; time each decision.
- **Measures:** task success, time, errors, clarity mean per wording (target ≥ 4/5), reviewer minutes per routed case (real, small sample), quotes.
- **Answers:** usability-testing; brief Stage 3; Table 7 applicant clarity.
- **Verify:** sessions held; results table in `planning/`; PRODUCT.md clarity row filled only from real ratings.
- **Risk:** engine low. If wording B lives in `followupText` (engine block), decisions do not change but the evaluation must be re-run to prove it.

### Gap 2: multi-case reviewer queue (R6) and console redesign (R7)

- **Changes:** `PolicyNest.html` UI only: a queue table at the top of the Review console, a case view (the current reviewer task, generalised to any case), an ops-lead strip of ≤ 6 KPIs, hash deep links `#review/<APP-ID>`. New `eval/queue.py` (Python, runs here) to build a seed of routed cases from `eval/out/eval_predictions.csv` + `documents.csv` (name, DOB, masked IDs, check results), embedded by `eval/embed.py` like the evaluation data.
- **Queue columns:** case, why routed (rulebook §9 item and rule), AI recommendation, where the AI was unsure (the checks kept for a person, plus any field with confidence < 0.75), age against the 4-working-hour SLA, status.
- **Ops-lead KPIs (method on every card):** queue size and oldest age; AI decision mix (in-sample, 600); share routed to a person (1.8%, in-sample); overrides (reviewer ≠ AI, this session only); drop-off by stage today (data pack `stage_events`); reviewer minutes (this session's measured clock, else "simulated estimate 0.38").
- **Answers:** kpi-dashboard-design (5–7 KPIs, methodology, drill-down), web-design-guidelines (URL reflects state), brief Should have "reviewer dashboard showing the queue, what the AI decided, and where it was unsure", Table 4 ops lead.
- **Verify in browser:** open `#review`, see the seeded cases plus the live applicant's case once routed; open a case by link; approve, ask and reject one each; the overrides count and the Audit trail update; keyboard-only run; 375 px.
- **Risk:** engine none (seed is produced by the existing engine run, stored as data). Evaluation none. **Blocked:** R7 waits for your references; PRODUCT.md says build R6 once, after R7.

### Gap 3: OCR on real phone photos (D6)

- **Changes:** new `ocr_bench/`: team-made specimen cards (printed synthetic PAN-, Aadhaar-, marksheet- and cheque-style documents with fictional data and SPECIMEN marked), photographed on 2–3 phones in good light, dim light, with glare and cropped; a `labels.json` with the true fields; a bench page that runs the app's own `readDoc`/`classify`/`parseDoc` in the browser and reports type-gate accuracy and field accuracy per slot and per condition. Optional later: client-side blur check (frontend spec §2.1), since image quality is the largest single rule (13.2 points in the ablation).
- **Not used:** `05_SPECIMEN_DOCUMENTS/sample_specimens` (may be real people). MIDV-500 has no Indian documents; useful only for the type gate's refusal of foreign IDs.
- **Answers:** PRODUCT D6; brief "use a public dataset or specimen documents your team creates".
- **Verify:** the bench page in the browser on the live site; a results table; D6 moves to Built only with a measured number.
- **Risk:** any tuning of `classify` or `parseDoc` (`parseDoc` is in the engine) changes the evaluation; re-run it after. The type gate must still refuse wrong documents.

### Gap 4: fresh held-out labelled set

- **Changes:** new `eval/holdout/`: 30–40 synthetic applications written in the test-set format, **labelled by hand from the rulebook before the engine sees them**, with the labels file hashed and dated first. Covers the three Human-only rules the test set lacks (face 0.60–0.75, surname change, unlisted board) and a dispute, plus mixed defects. `run_eval.js` (or the browser harness) gets a `--set holdout` option; the report gets a separate section.
- **Answers:** PRODUCT §8.4; brief "Prefer NEEDS_MORE_INFO…" and §9 Human-only coverage.
- **Verify:** numbers reported as "held-out, team-made, n = …"; any rule changed after seeing them turns the set in-sample, which is then said.
- **Risk:** none to the engine unless results prompt changes. Bias: the same people write rules and labels; a second labeller (you or a teammate) reduces it.

### Gap 5: discovery-call notes

- **Changes:** none in code. `planning/DISCOVERY_QUESTIONS.md`: the brief's ten questions, each with the assumption the product makes today, for you to take to the problem owner or mark "not asked".
- **Verify:** you supply notes, or PRODUCT.md says plainly that none exist.
- **Risk:** none.


### Gap 6: executive presentation (rubric 10%)

- **Changes:** a deck (Slides artifact, exportable to .pptx/PDF) of about 10 slides: problem and numbers (brief Table 3), today's journey, what the AI decides and what stays with a person, live demo path (T1, T5, T4), evaluation **labelled in-sample** with the first-run figures shown first, simulation **labelled directional**, usability results (only once gap 1 has run), risks and what is simulated, next steps.
- **Answers:** PRODUCT §9 rubric (presentation 10%); brief Stage 3 "a clear statement of what still needs a human".
- **Verify:** every number on a slide traced to `eval/EVALUATION_REPORT.md`, `PRODUCT.md` or a usability result; demo path rehearsed on the live site.
- **Risk:** none to the engine. Main risk is overstating the 100%: the deck must lead with "in-sample".

## Not planned: Hindi pop-ups and interface

PRODUCT.md moved this to Future (S4) during this session, so it has no plan section. The earlier draft is kept here for reference:


- **Changes:** a string table `T(key)` outside the engine for `cheer`/`cheerDoc` and interface copy; a language toggle beside the theme toggle (remembered in localStorage); Hindi rejection reasons if `rejectReasons` (engine) is English-only.
- **Answers:** PRODUCT S4; brief "conversational follow-up in English and Hindi".
- **Verify:** switch to Hindi, run T1 and T5: every toast and label in Hindi, nothing cut off at 375 px; a native speaker reviews the copy.
- **Risk:** engine only if `rejectReasons` gains Hindi (re-run evaluation). Layout risk from longer Devanagari strings.

## Notes for the spec audit

- `MISSING_SOURCE_MATERIALS.md` §2.1 quotes the brief on why images were withheld. That sentence is not in `PS-01_CHALLENGE_BRIEF.md`. Treat the quote as unverified.
