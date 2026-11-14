# Phase 2: spec and plan audit

Written 14 Nov 2026 from `PHASE1_AUDIT_AND_PLAN.md`. `/mattpocock-skills:to-spec` is not installed, so this spec and audit were written by hand to the same standard. Nothing here is built yet.

## Part A: spec

Each item has an ID, what it does, acceptance criteria (checked in the browser on the live site unless stated), and its status after the build. Items marked **[decision]** wait on Phase 3.

### Q: quality fixes (Gap 0)

| ID | What | Acceptance |
|---|---|---|
| Q1 | Visible focus on every upload control | Tab to each "Upload file" / "Replace" / "Upload new photo": a ring of ≥ 3:1 is visible on the label |
| Q2 | Text on the brand orange reaches 4.5:1 **[decision: dark ink on orange, or a darker orange]** | In-page audit: zero contrast fails on `.chip.o`, `.ic`, `.sc`, `.h.diag` in both themes |
| Q3 | Amber and grey chips reach 4.5:1 | Same audit: zero fails on `.pill.info`, `.chip`, `.chip.w` |
| Q4 | Toast dismiss ≥ 24×24 px | Target audit: zero targets < 24 px |
| Q5 | Heading order without skips; skip link to `<main>` | First Tab shows "Skip to content"; document cards are h2 |
| Q6 | Live region announces one status line, not the whole view | `aria-live` only on a status element |
| Q7 | Compact top bar under 600 px | At 375 px the bar is ≤ 80 px tall |
| Q8 | Sidebar items are links (`<a href="#apply">`) | Ctrl+click opens the view in a new tab |
| Q9 | Leave warning once an application has data (state is still not kept) | Reload after typing a name: the browser asks to confirm |
| Q10 | Form hygiene: `autocomplete` (email, tel), `spellcheck=false` on PAN/IFSC/email, reviewer note as `<textarea>`, `theme-color`, `preconnect` | Source check |

### U: usability tests (Gap 1)

| ID | What | Acceptance |
|---|---|---|
| U1 | Test plan document: tasks, script, consent, rating sheet | `planning/USABILITY_TEST_PLAN.md` exists; you approve it |
| U2 | Two wordings of the T5 follow-up for rating **[decision: build wording B into the app, or show it on paper]** | Both visible to participants in random order |
| U3 | Five applicant sessions, two reviewer sessions | Results table with task success, time, clarity per wording, reviewer minutes per routed case, quotes |
| U4 | PRODUCT.md clarity row filled | Only from U3's ratings; n stated |

### R: reviewer queue (Gap 2)

| ID | What | Acceptance |
|---|---|---|
| R6.1 | Seed of routed cases built from the engine's own output (`eval/queue.py` → embedded JSON) | 11 test-set cases (all NAME_MISMATCH) + constructed cases for face 0.60–0.75, surname change, unlisted board, dispute **[decision: include constructed cases]**; no full Aadhaar; each labelled "synthetic test-set case" or "constructed case" |
| R6.2 | Queue table: case, why routed (§9 item + rule), AI recommendation, where unsure, age vs 4-working-hour SLA, status | Rows sort by SLA; ages of seeded cases labelled **simulated** |
| R6.3 | Case view = today's reviewer task, generalised to any case; deep link `#review/APP-…` | Opening a link lands on that case |
| R6.4 | Ops-lead strip, ≤ 6 KPIs, method on each card | Each card states its source: in-sample, data pack, this session, or simulated |
| R6.5 | Keyboard actions **[decision: keys; F1 is browser help on Windows]** | Approve / Ask / Reject reachable without a mouse |
| R6.6 | Reviewer decisions log to the Audit trail with rule, round, engine version, reviewer time | Audit trail shows each; overrides count updates |
| R7 | Visual redesign of the console | **Blocked on your references.** R6 is built once, after R7 (PRODUCT §8) **[decision: wait, or build R6 logic now in today's style]** |

### O: phone-photo OCR (Gap 3)

| ID | What | Acceptance |
|---|---|---|
| O1 | Team-made specimen cards: fictional data, "SPECIMEN" printed across, not a copy of a real government layout **[decision: who makes and photographs them]** | ≥ 4 document types × 4 conditions (good, dim, glare, cropped) × 2 phones |
| O2 | `ocr_bench/labels.json` with the true fields | Written before the bench is run |
| O3 | Bench page running the app's own `readDoc`/`classify`/`parseDoc` in the browser | Reports type-gate accuracy, wrong-type refusal rate and field accuracy, per slot and condition |
| O4 | D6 status | Moves to Built only with O3's measured numbers; otherwise "Measured: …" |

### H: held-out set (Gap 4)

| ID | What | Acceptance |
|---|---|---|
| H1 | 30–40 constructed applications in the test-set format, labelled from the rulebook **before** any engine run; labels file hashed and dated | Hash recorded in the report |
| H2 | Covers the three Human-only rules absent from the test set, plus a dispute | Each such case routes to a person |
| H3 | Second labeller **[decision: who]** | Disagreements listed and resolved before the run |
| H4 | Evaluation runner for the held-out set **[decision: install Node, or a browser harness]** | Report section "held-out, team-made, n = …", kept apart from the in-sample figures |

### D: discovery notes (Gap 5)

| ID | What | Acceptance |
|---|---|---|
| D1 | `planning/DISCOVERY_QUESTIONS.md`: the brief's nine questions, each with today's assumption | You either add answers or confirm "not asked" |

### X: executive presentation (Gap 6)

| ID | What | Acceptance |
|---|---|---|
| X1 | ~10-slide deck **[decision: format and audience length]** | Every number traced to a file; in-sample stated on the accuracy slide; simulated stated on the simulation slide |

## Part B: line-by-line audit

Legend: **pass** = serves the requirement as written; **gap** = something is missing; **conflict** = clashes with a requirement or one of your standing decisions.

| Plan item | Requirement it serves | Result | Fix |
|---|---|---|---|
| Q1 focus on uploads | Brief Must have "interface an applicant can use"; WCAG 2.4.7 | pass | |
| Q2 orange contrast | WCAG 1.4.3; CLAUDE.md Look v3 (orange/lime/black) | **conflict** | Changing the orange touches your look. Proposed: keep the orange fill, switch its text to near-black (≈ 7:1). Phase 3 Q |
| Q3–Q5, Q10 | WCAG; web-design-guidelines | pass | |
| Q6 live region | WCAG 4.1.3 | pass | |
| Q7 compact bar | PRODUCT §3 applicant "on a phone"; frontend spec §2.1 360–420 px | pass | |
| Q8 links for nav | Guidelines; hash routes already exist | pass | |
| Q9 leave warning | PRODUCT §2 "no state is kept" | pass | Warns only; does not store anything, so the decision holds. Saving to sessionStorage would conflict and is not planned |
| U1–U3 tests | Brief Stage 3 (5 + 2); Table 7 clarity ≥ 4/5 | pass | |
| U2 wording B | Rulebook §8 message rules; guardrail "no fraud wording" | gap | Wording B must also say what is wrong, what to send and how, with no fraud wording and no full PAN. If it lives in `followupText` (engine block), re-run the evaluation, which needs Node (see H4) |
| U3 participants | DPDP Act (collect only what is needed) | gap | Consent sheet; record first names or codes only; participants use specimen details, never their own PAN/Aadhaar |
| U4 clarity row | PRODUCT status rule: nothing moves without measurement | pass | Filled only from real ratings |
| R6.1 seed | Brief Should have "reviewer dashboard showing the queue"; DPDP; "no full Aadhaar" | pass | Test-set OCR checked: 0 documents contain a 12-digit number. Seed stores last 4 only |
| R6.1 constructed cases | Rulebook §9 (all five Human-only items) | gap | Without them the queue shows only NAME_MISMATCH. Constructed cases must be labelled as such, never as test-set data |
| R6.2 SLA ages | Rulebook §7 (4 h, escalate after 8 h); guardrail "never invent numbers" | **conflict** | Seeded cases have no real arrival time. Show ages as **simulated**, or show only the live case's real age. Phase 3 Q |
| R6.2 "where unsure" | Brief Should have "where it was unsure"; brief Must have "confidence for each field" | pass | Uses kept-for-a-person checks plus any document with confidence < 0.75 (§4.1). The test set gives confidence per document, not per field: say "document confidence" |
| R6.3 case view | Rulebook §9: Human-only decisions go to a person; Must have "evidence side by side" | pass | The reviewer's Approve on a NAME_MISMATCH stays possible; the AI never auto-rejects (T4) |
| R6.4 KPIs | Brief Table 4 ops lead (queue age, decision mix, overrides, drop-off by stage) | pass | Each card names its source. "Overrides" is this session only. Drop-off by stage uses today's process from `stage_events`, labelled "today's baseline" |
| R6.5 hotkeys | Cockpit spec F1/F2/F3 | **conflict** | F1 opens browser help on Windows. Proposed: A / M / R with no modifier when focus is not in a text field, plus visible buttons. Phase 3 Q |
| R6.6 audit | Brief Should have audit trail with rule and model version; rulebook "every decision cites its rule" | pass | |
| R6 cockpit "click a field to highlight its box" | Cockpit spec §2.1 | gap | Raw OCR and word boxes are not kept (D5). Not planned; say so in PRODUCT |
| R7 redesign | CLAUDE.md: "review console redesigned only from my references" | **conflict** if built now | Do not restyle the console until the references arrive. Phase 3 Q on whether R6 logic waits too |
| R4 fraud desk | Rulebook §4.6: "two face-match failures in a row go to the fraud desk" | gap (existing) | Only the different-person referral is logged (`PolicyNest.html:1401`). Two selfie failures below 0.60 are not counted. Add to R6 or the engine. Phase 3 Q |
| O1 specimens | Brief "never real people's documents"; standing decision "real OCR with per-slot type gates" | pass | Fictional data, SPECIMEN mark. `sample_specimens` stays unopened |
| O1 lookalike risk | Indian law on imitation of government ID | gap | Use generic layouts with the same field labels, not a reproduction of the PAN or Aadhaar design, and keep prints in the team |
| O3 tuning | Type gates must still refuse wrong documents; evaluation uses `parseDoc` | gap | The bench must include wrong-type files and report refusals; any `parseDoc` change needs an evaluation re-run (H4 decision) |
| O4 D6 status | PRODUCT: nothing to Built without verification | pass | |
| H1–H2 held-out | PRODUCT §8.4; §6 "not evaluable on the test set" | pass | |
| H3 second labeller | Rigour (rubric 30%) | gap | One labeller who also wrote the rules is biased. Phase 3 Q |
| H4 runner | Evaluation must use the same engine code | gap | Node is not installed. Install (your OK) or build a browser harness. Phase 3 Q |
| H rule changes | Guardrail "say in-sample" | pass | If any rule changes after seeing held-out results, the set becomes in-sample and the report says so |
| D1 discovery | Brief Stage 1 "answers from your problem-owner meeting" | pass | Cannot be built by us; only you can supply answers |
| X1 deck | Rubric 10%; guardrail "never invent numbers" | pass | Accuracy slide leads with "in-sample"; usability slide only after U3 |
| All items: T1–T10 | Brief Table 6 | pass | No item changes the engine's decisions. Re-run T1–T10 on the live site after each deploy (Gap 0 and R6 touch the console and Documents screens that T4, T8 and T10 use) |
| All items: no API keys, one ideal case, both themes | CLAUDE.md standing decisions | pass | Every UI change is checked in both themes |
| Not in the plan | PRODUCT §9: Stage 1 "process map from stage_events" and "20 applications decided by hand, ≥ 8 hard" | gap | Not in §8, so not planned. H1's hand-labelled cases could double as the 20 hand decisions. Phase 3 Q |
| Not in the plan | `MISSING_SOURCE_MATERIALS.md` §2.1 quotes a brief sentence that is not in the brief | gap | Mark the quote as unverified, or remove it. Phase 3 Q |

## Part C: status moves this plan would make

| PRODUCT item | Today | After the plan | Verified by |
|---|---|---|---|
| R6 | Partial | Built | R6.1–R6.6 acceptance in the browser |
| R7 | Not built | unchanged until references | n/a |
| D6 | Not verified | "Measured" with numbers; Built only if the type gate and fields hold on phone photos | O3 bench |
| Applicant clarity | Not measured | a number, n = 5 | U3 |
| Reviewer minutes | Simulated estimate | real, small sample (2 reviewers), alongside the estimate | U3 |
| Held-out accuracy | none | a new row, "held-out, team-made" | H4 |
| Executive presentation | Not found | Done | X1 |

No item moves to Built without one of these checks.

## Part D: decisions from Phase 3 (grilling, 14 Nov 2026)

All recommended answers were accepted. These settle every **[decision]** tag above.

| # | Decision |
|---|---|
| Q1 | Text on orange fills becomes near-black (about 7:1); the orange itself is unchanged (Q2 spec item) |
| Q2 | Build the queue data now (R6.1 seed, R6.4 KPI figures); queue screens wait for the review-console references (R7), so they are built once |
| Q3 | The queue also holds constructed cases for face 0.60–0.75, surname change, unlisted board and a dispute, each labelled "constructed case" |
| Q4 | Test-set and constructed cases show ages labelled **simulated**; only the live applicant's case shows a real age |
| Q5 | Reviewer keys: A = Approve, M = Ask for more info, R = Reject, active when focus is not in a text field; buttons stay visible |
| Q6 | Add rulebook §4.6: two selfie failures below 0.60 in a row log an internal fraud-desk referral, outside the engine block |
| Q7 | Install Node.js LTS with `winget` so `eval/run_eval.js` runs here |
| Q8 | The user labels the held-out cases independently, before the engine sees them |
| Q9 | 20 of the held-out cases (≥ 8 hard) also serve as the Stage 1 "20 applications decided by hand" |
| Q10 | Wording B of the follow-up is shown on a printed card; the engine is not changed for it |
| Q11 | Five applicants from outside the team (≥ 2 fitting the POSP profile: phone-first, Hindi-comfortable); two reviewers who have not seen the app |
| Q12 | Claude makes printable specimen documents (generic layouts, fictional data, SPECIMEN across them); the user prints and photographs them on two phones |
| Q13 | No discovery meeting took place: the brief's nine questions are recorded as "not asked", each with today's assumption |
| Q14 | A deck of about 10 slides for a 7–10 minute talk, exportable to .pptx or PDF |
| Q15 | Accessibility fixes (Gap 0) come first |
| Q16 | Add the Stage 1 process map from `stage_events`, shown on the Evaluation page |
| Q17 | Mark the quote in `MISSING_SOURCE_MATERIALS.md` §2.1 as "not found in the brief" (do not delete it) |
| Q18 | On a second selfie failure the case goes to a reviewer; the applicant sees only the neutral "a person is checking a few details" message; the referral is internal |
| Q19 | Hindi-comfortable participants also rate the Hindi follow-up; the Hindi clarity score is reported separately, and the ≥ 4/5 target applies to each language |
| Q20 | Results go to `planning/usability/results.csv` with participant codes only (P1–P5, R1–R2): no names, phone numbers or documents, no online form |
| Q21 | Build order: Gap 0 accessibility → queue data (R6.1, R6.4) → Node and held-out set → process map → specimen print-outs and photo bench → deck last (after usability results). Usability sessions run in parallel whenever participants can be booked. No hard deadline. |

Still blocked: the queue screens and the console redesign (R6.2, R6.3, R6.5, R7) wait for the user's references.
