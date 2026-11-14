# PolicyNest: reconciled findings

- **Written:** 14 Nov 2026, by a documents-only session. No app file was changed and nothing was deployed.
- **What this is:** every finding from the research outputs, merged into one deduplicated list. Each finding gives its sources, the evidence, a severity, the `PRODUCT.md` goal it touches, and its status today. Contradictions between reports are listed in §3, each with a resolution and the reason for it.
- **What comes next:** `GRILL_LOG.md` stress-tests these findings against the source package and records a decision for each open point. `PRD.md` turns the result into requirements and a build roadmap. The finding IDs (`RF-nn`) and contradiction IDs (`CX-nn`) below are referenced from both.

## 0. Sources merged

| Code | Source | What it is | Trust notes |
|---|---|---|---|
| CR | `CRITICAL_REVIEW.md` (+ lens reports `LENS_*.md` and `REVIEW_HANDOVER.md` in the side-session notes folder) | Six-lens critical review, 14 Nov | It reviewed the live site **before** the S1–S5 build was deployed, plus the source while it was being edited. Several of its findings are now fixed or partly fixed (see the status column). The usability lens is an expert walkthrough, not user data. |
| IR | `INTEGRATIONS_RESEARCH.md` (byte-identical copy at `reports/PolicyNest integrations research.md`; raw notes in `research_notes/`) | Integrations research, 14 Nov | "Verified" means a live probe or page view on 14 Nov. Nothing was installed. |
| AR | `AUTORESEARCH_REPORT.md` and `autoresearch/probe-261114-1758/conflicts.md` | Rule-by-rule re-derivation on the 600 cases | In-sample and not blind (stated by its author). |
| UT | `USABILITY_TEST_PLAN.md` | Usability study plan | A plan only. No session has run. |
| EV | `eval/EVALUATION_REPORT.md`, `eval/out/*.json` | Engine evaluation on the 600 cases | In-sample. Run 13 Nov 19:30 UTC on engine 3.4.0. |
| HP | `HANDOFF_PROMPT.md` | Earlier hand-off instructions | Process document; one stale claim (to-spec and grill-with-docs not installed; both are installed now). |
| P1, P2 | `planning/PHASE1_AUDIT_AND_PLAN.md`, `planning/PHASE2_SPEC_AND_AUDIT.md` (Part D holds the 21 Phase 3 decisions) | Skill audit, hand-written spec and plan audit | Part D decisions are the user's and are binding. |
| S1P | `stage1/STAGE1_PACK.md` (+ `stage1/tables`, `stage1/scripts`) | Stage 1 process map, 20 hand-decided cases, business case | The 20 decisions were made by Claude, not by the team. |
| PL | `C:\Users\swarn\.claude\plans\composed-hopping-swing.md` | The approved focused-onboarding plan (S1–S6) | Built and deployed on 14 Nov; details differ from the plan in places. |
| IP | `usability/image_pack/README.md` | Synthetic image pack for the usability test | Exists now; UT says it does not (stale). |
| VER | **This session's own checks** on 14 Nov | Source greps, the live site, the proxy health endpoint and an engine-block hash | Listed in §1. |

## 1. What this session verified itself

| # | Check | Result |
|---|---|---|
| V1 | Live site `https://policynest.embarko.app/?v=<epoch>` | `200`. `Last-Modified: Sat, 14 Nov 2026 16:43:50 GMT`. Contains the focus bar, the save key `pn-onboarding-v1`, "pass mark is 50%" (3 occurrences, 0 of "40%"), and the Copilot URL. **The S1–S5 build is live**, so CR's statement that the live site is pre-plan is now out of date. |
| V2 | Live HTML vs local `policynest_mvp/site/index.html` | They differ only by a script that Embarko appends (a hosting badge, about 130 lines at the end). |
| V3 | Engine block SHA-256 (text between `/* ENGINE:START` and `/* ENGINE:END */`, LF line endings) | `bd41031462336892…` in **all three**: live, `PolicyNest.html`, `site/index.html`. Engine string `policy-engine 3.4.0`. |
| V4 | Is the evaluation pinned to that engine block? | **No.** `eval/out/eval_results.json` records the run time (2026-11-13T19:30Z) and the engine version string, but no hash of the code. Node is still not installed (`node: command not found`), so the evaluation could not be re-run. See RF-01. |
| V5 | `GET https://policynest-copilot.embarko.app/api/health` | `{"ok": true, "llm": false, "model": "claude-opus-5-5"}`. The proxy is up with no key. |
| V6 | `GET /kb.json` on the live site | `200`, 47,646 bytes, 55 chunks. **13 of the 55 chunks contain the word "fraud".** No chunk has an audience tag. |
| V7 | `copilot_api/main.py` | Client-supplied `passages` and `context` go into the prompt; the rate-limit key is the first `X-Forwarded-For` value; `null` is in the default origins; `_hits` is never pruned; the default model is `claude-opus-5-5` at effort `low`. The `fallbacks="default"` call with the `server-side-fallback-2026-07-01` beta and `output_config={"effort": …}` are valid API shapes for Opus 5.5 (checked against the claude-api skill). |
| V8 | `persist()` in `PolicyNest.html` | Saves the whole state object with only `url`, `thumb` and `text` keys dropped. The typed **full PAN, full bank-account number, DOB, mobile and email** are therefore written to `localStorage` in plain text, against the plan's "parsed fields only… account last 4". See RF-03. |
| V9 | Sample identity | `SAMPLE={name:"Rahul Kumar Sharma",…,consent:true}` and `fresh()` copies it into every new application. Still open. |
| V10 | Brand ink | `--brand-ink:#ffffff` in both theme blocks (light `#ff6b1a`, dark `#ff7a2e`). Near-black text on orange is **not built**, although it was agreed. |
| V11 | Upload focus | `.vcard input[type=file]` and `.fix input[type=file]` are 1×1 px with opacity 0; no `:has(input:focus-visible)` rule exists. Still open. |
| V12 | Live region | `<section id="view-apply" aria-live="polite">` is unchanged. Still open. |
| V13 | Low-confidence upload | The blurry specimen still gets `cheerDoc` ("verified" toast) at confidence 0.61, although the new inline feedback card now lists the fix. Partly fixed. |
| V14 | Focus-exit handling | No `blur` listener (fixed). The picker flag now clears on window focus after 1.5 s and after 60 s (fixed). Closing full screen still counts as an exit; there is no touch-device exemption and no "start without full screen" option. `FOCUS_EXIT` notes record "Left the onboarding screen for N s". |
| V15 | Reject panel | `rejectPanel()` still offers only "Dispute this decision": no restart, no delete. |
| V16 | Exam | UI and logic use 50% (`score>=50`). The 24-hour retake gap is still waived ("the demo lets you retry now"), and no fail time is stored. |
| V17 | Invented time copy | "About 2 minutes" (`stepHead`, step 0) and "Many agents pass on their second try" (exam fail toast) are still present. |
| V18 | Compliance checklist | `checklist()` still ticks "Consent recorded" and "Aadhaar kept as last four digits only" from `S.events.length>0`. |
| V19 | Copilot client | Blocks a question containing a PAN-, Aadhaar- or account-shaped number before sending (block, not redaction). Sends first name, step, document statuses, the app-generated refusal text, issue codes and the last six chat turns. Has a client-side output filter for fraud wording and "you are approved/rejected". |
| V20 | Audit trail | A confirmed different-person rejection logs `FRAUD_DESK_REFERRAL` into the same event list the applicant-facing Audit trail page shows, and that list is saved to `localStorage`. |
| V21 | Not present in the source | `checksFor` (the plan's engine helper: not built, feedback reuses `decide` instead), nav links as `<a href>`, a skip link, `beforeunload`, `navigator.storage.persist`, Wake Lock, `capture=` on the selfie input, `<dialog>`, `documentElement.lang` switching. |

## 2. Findings

Severity: **Critical** (privacy or compliance breach, or a wrong claim on a scored metric), **High** (blocks a brief Must-have or a standing decision, or misleads a scorer), **Medium**, **Low**. Status: **Open**, **Partly fixed**, **Fixed** (verified), **Stale** (the source document is out of date). "Verified" in the evidence column means checked by this session (§1).

### A. Privacy, consent and compliance

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-01 | **The headline accuracy is not pinned to the code that runs.** The evaluation ran on 13 Nov at 19:30 UTC; the engine block has been edited since in the same file, and no hash was recorded, so "the same code the site runs" cannot be shown for today's build. | Critical | VER, EV, P2 (H4), CLAUDE.md ("engine SHA must match") | V3, V4 (verified). Node absent. | E2, §6 | Open |
| RF-02 | **Another person's identity is pre-filled, and DPDP consent is pre-ticked.** The Compliance card then reports "Consent recorded". | Critical | CR R2, U2, U3, K14, F7 | V9 (verified) | A2, A11, §7 | Open |
| RF-03 | **Autosave writes full PAN, full bank-account number, DOB, mobile and email to the device in plain text.** The plan promised parsed fields only and a masked account. On a shared phone the next user can read them. | High | VER (new), PL S3 | V8 (verified) | A13, D5, §7 | Open (new) |
| RF-04 | **The Compliance checklist ticks items it never checks** ("Consent recorded", "Aadhaar kept as last four", and a simulated registry tick). | High | CR R14, K3 | V18 (verified) | E1, §7 | Open |
| RF-05 | **Focus-exit logging records "time away"**: behavioural monitoring with no rule behind it (the sitting is a product choice), against DPDP purpose limitation and minimisation. | High | CR R7, KPI lens | V14 (verified) | A12 | Open |
| RF-06 | **Internal fraud-desk wording reaches the applicant's device and screens.** `FRAUD_DESK_REFERRAL` is in the shared Audit trail list and in the saved state. The demo puts applicant and reviewer in one page, so this is acceptable for a demo only if the Audit trail is labelled as the ops view. | Medium | VER (new), rulebook §8 | V20 (verified) | E1, R4, §7 | Open (new) |
| RF-07 | **Saved progress cannot be guaranteed on iOS or in in-app browsers**, and the app shows "saved" without a read-back. `storage.persist()` is not requested. | Medium | CR R28, D6, D12 | V21 (no `storage.persist`), `persisted()===false` observed by CR | A13 | Open |
| RF-08 | **Expired saves are deleted on the device, but the state machine's DROPPED_OUT event and the 5-year KYC retention rule both need a server**, which a static demo does not have. Say so; do not claim either. | Low | CR §3 | `restore()` deletes and sets `DROPPED` (verified) | A13, E1 | Open (documentation) |
| RF-09 | **`.env` sits at the project root**; any zip of the folder would include it. `build_site.py` blocks keys in `site/` but not in packaging. `copilot_api/__pycache__` would be tarred into the proxy deploy. | Low | CR §3, VER | `ls` (verified); `.env` not opened | §7 | Open |

### B. Onboarding Copilot and the proxy

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-10 | **The proxy is an open LLM relay once a key is added**: the caller supplies the passages and the context, `Origin` is not authentication, and the rate limit trusts `X-Forwarded-For`. `null` is an allowed origin. `_hits` grows without bound. No spend cap. | High | CR R8, REVIEW_HANDOVER | V7 (verified) | A15 | Open (harmless today only because there is no key: V5) |
| RF-11 | **The retrieval corpus contains internal fraud-desk passages** the Copilot could quote to an applicant. A client-side output filter exists but no server-side one, and no audience tag. | High | CR R9 | V6 (13 of 55 chunks), V19 (verified) | A15, §7 | Partly fixed |
| RF-12 | **Typed ID numbers in a question**: the client blocks PAN-, Aadhaar- and account-shaped numbers before sending; the server does not check. | Medium | CR R10 | V19 (verified) | A15, D5 | Partly fixed |
| RF-13 | **Model default disagrees between the plan and the code**: the plan says `claude-haiku-5-5`, `main.py` and CLAUDE.md say `claude-opus-5-5` at effort `low`. First-party list prices per million tokens: Haiku 5.5 $0.10 / $0.50, Sonnet 5.5 $2 / $10, Opus 5.5 $4 / $20 (claude-api skill, cached 3 Nov 2026). | Medium | CR R8, PL S5, CLAUDE.md | V5, V7 (verified) | A15 | Open (decision, see CX-04) |
| RF-14 | **Toasts and Copilot nudges compete**: a clean run fires 9 toasts in about 25 s, each a fixed 5.2 s with no pause on hover or focus, and both the container and each toast are live regions. | Medium | CR R24, G11, G12 | CR measured live; toast code unchanged (verified) | A6, A15 | Open |
| RF-15 | **Hindi is limited** to the follow-up, rejection and reviewer-ask text; BM25 over English passages returns little for Romanised Hindi. The Copilot system prompt says "reply in Hindi if they write in Hindi". | Medium | CR R17, G7, U14–U17 | V21 (no `lang` switching) | S4, F1, A15 | Open (scope decided: S4 is Future) |
| RF-16 | **The facts the Copilot and the screens state (pass mark, hours, retake gap, SLAs) live in several places** and can drift apart. | Medium | CR §6 (G6) | `intentAnswer` and step heads each hard-code "50%" and "24 hours" (verified) | A7, A15 | Open |
| RF-17 | **The proxy is live but unproven with a key**: no answer has ever been generated; latency, cost per question and guardrail behaviour are unmeasured. | Medium | CR R27, D8, VER | V5 (verified) | A15 | Open |

### C. Focused sitting, autosave and resume

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-18 | Reload used to lose everything; **autosave and resume are now built** (with consent, `localStorage`). | was Critical | CR R1, U18, F1 | V1 (verified live) | A13 | Fixed (see RF-03, RF-07) |
| RF-19 | **The sitting's scope**: details and documents only; it ends at Submit. | was High | CR R5, F3 | `endSitting("SITTING_COMPLETE",…)` at Submit; `watching()` requires step < 2 (verified) | A12 | Fixed |
| RF-20 | **Focus-exit detection on phones and assistive tech**: `blur` is no longer used and the picker flag now clears; closing full screen still counts as an exit; no touch exemption; no "start without full screen". | High | CR R6, D1–D5, D12, F12, A11Y-04 | V14 (verified) | A12 | Partly fixed |
| RF-21 | **Resume landing per state** (CR §5 table): the save restores `S` and the step; the per-state landing (rework days left, exam retake time, reject panel with delete) is only partly there. | Medium | CR R18, F2, F11 | `restore()` resets focus and session only (verified) | A13 | Partly fixed |
| RF-22 | **Timer accessibility (WCAG 2.2.1 / 2.2.2)**: `role="timer"` exists and +10 minutes exists; unlimited extension, an off switch, a hide control and `<dialog>` warnings are not confirmed. | Medium | CR R23, A11Y-04 | V21 (no `<dialog>`); `role="timer"` present (verified) | A12, A10 | Partly fixed |
| RF-23 | **Full screen needs a direct user gesture**; failures must be handled. | Medium | CR R32, D3 | Not re-tested | A12 | Unverified |
| RF-24 | **The sitting has not been tested on iOS Safari, Android or in-app browsers.** | Medium | PRODUCT A12, CR §8 | — | A12 | Open |

### D. Applicant journey and trust

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-25 | **The test harness sits in the applicant's path** ("Use specimens for all", variant dropdowns labelled T4, T6…). It also undercuts the focused sitting. | High | CR R15, U4 | Variant `<select>` rendered per slot (verified) | A3, A11, A12 | Open |
| RF-26 | **A poor photo is cheered as "verified"** even though the inline card now says what to fix. | High | CR R11, G1, U5, F13 | V13 (verified) | A6, A14, D4 | Partly fixed |
| RF-27 | **REJECT is a dead end**: no "start a new application", no "delete my saved progress"; one rejection text says "reply to this message" with no reply channel. | High | CR R16, F4, U22 | V15 (verified) | C6 | Open |
| RF-28 | **Editing details after upload leaves every document "verified".** | Medium | CR R19, F5 | `back-details` only changes the page (verified) | C1, A14 | Open |
| RF-29 | **Invented time estimates** ("About 2 minutes", "Many agents pass on their second try") break the no-invented-numbers rule. | Medium | CR R21, K6, G5, U7 | V17 (verified) | A5, A6 | Open |
| RF-30 | **The applicant sees rule codes and enums** (§4.1, NEEDS_INFO, Tier 1), and a masked typing-error line that looks like a bug. | Medium | CR R26, U9, U10 | Verification table unchanged (inferred from source) | A5 | Open |
| RF-31 | **Refusals say what and how but not why, and show classifier internals** (confidence, word counts). The taxonomy's glare and crop wording is unused. | Medium | CR R25, G2, G3, U21 | Inline card added; refusal reasons unchanged | A4, A14 | Partly fixed |
| RF-32 | **Ops numbers on the applicant dashboard** ("today 17.3 h", "today 8.4 days"); the certificate compares demo minutes with fleet days. | Medium | CR R29, U8, K2 | `renderDash` strings (verified) | A5 | Open |
| RF-33 | **"Time to decision" is the length of the checks animation**, shown beside the 17.3 h queue baseline. | High | CR R13, K1 | `finishDecision(t0)` measures from the start of the reveal (verified) | §6 time to decision | Open |
| RF-34 | **Exam pass mark**: 50% is now live. The 24-hour retake gap is waived and the fail time is not stored. | was High | CR R12, K10, F10, G6, U11, AR | V1, V16 (verified) | A7 | Partly fixed (see CX-01) |
| RF-35 | **Certificate has no download or print**, and "Start a new application" wipes it. | Low | CR R34, U12 | — | A8 | Open |
| RF-36 | **The selfie slot accepts PDFs and has no camera hint** (`capture="user"`). | Low | CR R33, D10, U6 | V21 (verified) | A3, A4 | Open |
| RF-37 | **The follow-up mentions a declaration "format" that does not exist**, and "tell us which date is correct" offers only an upload. | Low | CR R37, G9, U20 | — | F1 | Open |
| RF-38 | **On-device OCR cost on low-end phones is unmeasured** (about 2.0 s for one synthetic PAN on an 8-core desktop with a warm cache). | Low | CR R38, D11 | CR measured | D1, D6 | Open |
| RF-39 | **OCR on real phone photos is not verified** (D6). A synthetic image pack and print layouts now exist; no photos have been taken or benched. | High | PRODUCT D6, P1 gap 3, IP | `usability/image_pack/` exists (verified) | D6 | Open |

### E. Accessibility (WCAG 2.2 AA, manual audit; no screen reader, axe or Lighthouse run)

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-40 | **Upload controls have no visible keyboard focus.** | Critical | CR R3, A11Y-01, P1 A-1 | V11 (verified) | A10 | Open |
| RF-41 | **White text on orange is 2.85:1 (light) and 2.60:1 (dark)**; near-black `#141414` gives 6.47:1 and 7.08:1. Agreed on 14 Nov, not built. White on the hero gradient: 2.35–2.85:1 (computed). | Critical | CR R4, A11Y-02, P1 A-2, P2 Q1 | V10 (verified) | A10 | Open |
| RF-42 | **The whole Application view is a live region.** | Medium | CR R22, A11Y-06, P1 A-7 | V12 (verified) | A10 | Open |
| RF-43 | **Other leftovers**: light focus ring 2.85:1; no skip link; six identical "Upload file" names; h1 → h3 on Documents; no `aria-describedby`/`aria-invalid`; 255 px of header at 375 px; DRAFT pill 3.27:1; grey chip 2.85–3.07:1; toast dismiss 16×21 px; sidebar items are buttons, not links. | Medium | CR R31, R33, P1 A-3…A-8, web-design findings | V21 (no skip link, no nav links) | A10 | Open |
| RF-44 | **Not tested**: screen readers, 200% zoom, Windows high contrast, gradient contrast by sampling. | Medium | P1, CR §8 | — | A10 | Open |

### F. Evaluation, metrics and honest labels

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-45 | **All accuracy figures are in-sample.** First run 98.0% (3.3.0); now 100.0% (3.4.0) after three rulebook-based refinements on the same 600. The autoresearch cross-check also reached 600/600 but its author had seen the data. | High (label) | EV, AR, PRODUCT §6 | `eval_results.json` (verified) | E2, §6 | Labelled; needs a held-out set (RF-47) |
| RF-46 | **REJECT precision and recall (60/60) count the 11 routed-to-a-person cases as REJECT**, and the matrix has no Person column. The fairness chip "no gap found" is hard-coded and cannot detect a gap at 100%. The page omits the 60.7% "approved first time" figure. | Medium | CR R30, K4, K11, K12, K13 | Fairness chip static (verified) | E2, E3 | Open |
| RF-47 | **No held-out labelled set exists**; the three Human-only rules (face 0.60–0.75, surname change, unlisted board) are absent from the 600 and so are unevaluated. | High | PRODUCT §6, §8.4, P2 H1–H4, AR, S1P | — | E2, R2 | Open |
| RF-48 | **Reviewer minutes per application (0.38) is a simulated estimate**; applicant clarity is not measured; no usability session has run. | High (label) | EV, UT, PRODUCT §6 | — | §6 | Open |
| RF-49 | **The two Table 7 targets pull against each other**: 60% straight-through and under 5 reviewer minutes are both met only if a routed case takes 12.5 minutes or less. | Medium | S1P §3.1 | Arithmetic: 5 ÷ 0.4 | §6 | Open (note) |
| RF-50 | **Hard-coded expected check counts** (24 vs 23 run live), two progress measures that disagree, and "checks passed" counting INFO as passed. | Low | CR R35, K5, K8, K9 | `exp` map in `renderDash` (verified) | A5 | Open |
| RF-51 | **Ten-most-wrong list**: the current engine has no wrong cases in-sample, so the Stage 2 deliverable can only show the first run's 12 errors and their fixes. | Low | PRODUCT §9 | EV "Changes after the first run" | Stage 2 | Partly done |

### G. Reviewer, queue and routing

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-52 | **The review console holds one application**; the brief's Should-have queue is not built. Queue data may be built now; queue screens wait for the user's references (R7). | High | PRODUCT R6, R7, P1 gap 2, P2 Q2 | — | R6, R7 | Open (blocked on references) |
| RF-53 | **Rulebook §4.6 "two face-match failures in a row go to the fraud desk" is not built.** Decided on 14 Nov (Q6, Q18). | High | P2 R4 row, Q6, Q18, PRODUCT R8 | No failure counter in the source (verified grep) | R8 | Open |
| RF-54 | **Reviewer keys A / M / R** decided instead of the spec's F1–F3. Not built. | Low | P2 Q5, PRODUCT R9 | — | R9 | Open |
| RF-55 | **The cockpit spec's "click a field to highlight its box" cannot be built**: raw OCR and word boxes are not stored. | Low | P2 Part B | D5 (by design) | R3 | Won't build (documented) |
| RF-56 | **"Reply within 4 working hours" is a promise nothing tracks.** | Medium | K7 | `humanPanel()` text (verified) | R3 | Open |

### H. Data and business case

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-57 | **Stage 1 deliverables now exist**: process map, 20 hand-decided cases (20/20, 10 hard, hash frozen before the key was opened) and a first business case. PRODUCT.md §9 still says "Not found". The 20 were decided by Claude, so a team member must adopt or overrule them. | High | S1P, PRODUCT §9 | `stage1/` files (verified present) | Stage 1 | Stale in PRODUCT.md |
| RF-58 | **One-at-a-time follow-ups are a small share of rounds**: 703 of 774 returned applications were returned once; 75 extra rounds in nine months. The product mainly removes queue time (17.3 h + 14.6 h), not rounds. | Medium | S1P §1.4 | `stage1/tables` | §1, E4 | Open (wording in PRODUCT §1) |
| RF-59 | **The data does not show that faster review reduces silence or non-start**; the +106 / +40 to +343 agents are what-if arithmetic. | Medium | S1P §3.4, EV | `bc_dropoff_drivers.csv` | E4 | Open (label) |
| RF-60 | **The biggest loss is after approval**: 482 approved applicants (21.7%) never start training. | Medium | S1P §1.4, brief Table 3 | — | E4 | Open (opportunity) |
| RF-61 | **Package figures that do not reproduce**: reviewer cost ₹14.7 lakh (data supports ₹4.1–5.0 lakh); four P90/median figures in `03_OPERATIONAL_BASELINE_METRICS.md`; the data dictionary describes a different workbook. | Medium | S1P §1.5, §3.1 | `_part3_numbers.json` | E4, Stage 1 | Open (label) |

### I. Conflicts inside the source package

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-62 | **Policy-engine spec §3.1 says to suppress image-quality issues for an ineligible applicant**; rulebook §6 says to give every reason. | Low | VER (new) | `01_POLICY_ENGINE_SPECIFICATION.md` §3.1 vs rulebook §6 | C4 | Resolved in CX-06 |
| RF-63 | **The state machine says "all 5 documents" and lists 6.** | Low | VER (new) | `03_APPLICATION_LIFECYCLE_STATE_MACHINE.md` §2 | A3 | Resolved (six) |
| RF-64 | **The guardrails spec adds a human-escalation band for age 17.95–18.00** that the rulebook does not have. | Low | VER (new) | `06_AI_DECISION_BOUNDARIES…` §1 | C3 | Resolved in CX-07 |
| RF-65 | **The rework spec locks verified documents against re-upload and uses different spelling-variant wording** from rulebook §8. | Low | VER (new) | `04_CONSOLIDATED_REWORK_ENGINE.md` §2.2, §3 | F1, F2 | Resolved in CX-08 |
| RF-66 | **Reason vocabulary**: `reason_codes` lists 14 codes; `application_truth` uses 5 others and never uses 7 of the 14. | Low | AR conflicts 1, S1P §2.3 | — | E2 | Mapped in eval |
| RF-67 | **Recognised-board list is not supplied**, yet unlisted boards are Human only. | Medium | AR conflicts 8, PRODUCT §6 | Rulebook §4.4, §9 | C3, R2 | Open (problem owner) |
| RF-68 | **T4 wording vs Specimen 6**: the brief puts the different name on Aadhaar and marksheet; the specimen has it on the marksheet only. | Low | AR conflicts 2 | — | T4 | Resolved: any one document triggers |
| RF-69 | **`MISSING_SOURCE_MATERIALS.md` §2.1 quotes a brief sentence that is not in the brief.** Decided: mark it "not found in the brief" (Q17). | Low | P1, P2 Q17 | The file has no such marker yet (verified grep) | — | Open |

### J. Integrations

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-70 | **The four simulated checks (PAN, penny-drop name, face match, IRDAI registry) must stay simulated**: every KYC vendor needs a server-side secret, no public IRDAI POSP API exists, and DigiLocker needs partner onboarding. | Info | IR §1, §3d | IR probes | C3, S2 | Confirmed |
| RF-71 | **Keyless lookups that would work under the CSP**: Razorpay IFSC (real "IFSC exists", ACAO `*`), api.postalpincode.in (the app collects no pincode), libphonenumber-js from jsDelivr. All three are third-party calls. | Low | IR §2, §4 | IR probes (verified by IR) | C3, A2 | Deferred (CX-05) |
| RF-72 | **UIDAI Secure QR / offline XML verification in the browser is legally unsettled** (December 2025 amendment unread). | Low | IR §5 | — | S2 | Not now |
| RF-73 | **Developer tools that help without shipping**: Python Playwright (`webapp-testing`), the built-in browser, the `design` plugin, Sheets/Drive, Canva for the deck. Node is still absent, which rules out the Node-only MCP servers. | Info | IR §2, §4 | `node` absent (verified) | §8 gaps | For the roadmap |

### K. Process and document hygiene

| ID | Finding | Sev | Sources | Evidence | Goal | Status |
|---|---|---|---|---|---|---|
| RF-74 | **PRODUCT.md is out of date in places**: §2 "No state is kept. A page refresh starts a new application" (autosave is built); §9 Stage 1 rows; A15 model; R8–R9. | Medium | VER | PRODUCT.md vs V1 | All | Open |
| RF-75 | **USABILITY_TEST_PLAN.md is out of date**: "exam pass mark 40%", "a page refresh gives a clean new application", "the image pack does not exist yet". | Medium | VER, IP | UT §1, §9 vs V1, IP | §8 gap 1 | Open |
| RF-76 | **CRITICAL_REVIEW.md describes a pre-deployment live site**; read its live observations as history, not current state. | Low | VER | V1 | — | Note |
| RF-77 | **The folder is not a git repository.** Worktrees, branches and the engine-change review the integrations report suggests all need one. | Medium | VER, IR §3a | No `.git` (verified) | Roadmap | Open |
| RF-78 | **A second, unused autoresearch skill is installed** at `~/.claude/skills/autoresearch` (its author offered to remove it). | Low | AR §1 | — | — | Open (housekeeping) |
| RF-79 | **The synthetic image pack follows the PS-01 specimen layouts**, while Phase 3 Q12 asked for generic layouts that do not imitate government IDs. The images were not opened in this session. | Low | IP, P2 Q12, P2 O1 lookalike row | IP README §0 | D6 | Open (check) |
| RF-80 | **No executive deck exists** (rubric 10%); no discovery-call notes exist. | High | PRODUCT §8, §9 | — | §9 | Open |

**Counts:** 80 findings. By current severity: 4 Critical (RF-01, RF-02, RF-40, RF-41), 18 High (including two "High (label)": RF-45, RF-48), 31 Medium, 22 Low, 2 Info; three more were High or Critical and are now fixed or partly fixed (RF-18, RF-19, RF-34). By status: 54 open, 9 partly fixed, 2 fixed (RF-18, RF-19), 6 resolved here as source conflicts, and 9 notes, labels or deferrals. New from this session's own checks: RF-01 (scope widened), RF-03, RF-06, RF-62 to RF-65 and RF-77.

## 3. Contradictions between sources, and their resolution

| ID | Contradiction | Sides | Resolution | Reason |
|---|---|---|---|---|
| CX-01 | **Exam pass mark: 40% or 50%** (the known open conflict) | **50%:** state machine (`03_…STATE_MACHINE.md` §1–2, "Score >= 50%"), data dictionary (`COMPLETE_DATA_DICTIONARY.md:35`), current-state process (`02_…CURRENT_STATE.md:28`, "50% (10/20)"), regulatory matrix (`:39`, "e.g. 50%"), and the app since 14 Nov. **40%:** every data-pack exam-failure event reads "Score below 40%" (160 events); the usability plan and the pre-14-Nov app said 40%. **Rulebook:** silent ("Pass the POSP examination"). | **50%.** Already live. Record it as a demo rule taken from the state machine, not a regulatory figure. | Four specification documents state 50% explicitly. The 40% text describes *failures*, and every score below 40% is also below 50%, so the event data are consistent with a 50% pass mark too: they do not contradict it. The rulebook, which outranks the specs, sets no number, and the brief puts the exam out of scope. Confirmation needed from the problem owner (GRILL_LOG G-01). |
| CX-02 | **Is the live site pre-plan?** | CR: live is pre-plan (12:45 GMT build). VER: live is the 16:43 GMT build with S1–S5. | **VER wins.** CR's live observations are history. | Measured today (V1). |
| CX-03 | **Straight-through rate: 98.2% or 60.7%?** | EV/PRODUCT: 98.2% = no human touch (brief glossary). AR and early notes: 60.7% read as the ceiling. | **98.2% is the brief's metric; 60.7% is reported beside it as "approved first time, no follow-up".** | The brief's glossary defines straight-through as "no human touch"; AR corrected itself. |
| CX-04 | **Copilot model: Haiku 5.5 or Opus 5.5?** | PL S5 and CR R8: Haiku by default. CLAUDE.md and `main.py`: Opus 5.5 at effort `low`. | **Keep `claude-opus-5-5` at `low` as the default; expose Haiku 5.5 through `COPILOT_MODEL`; add a spend cap.** Needs human confirmation (GRILL_LOG G-02). | CLAUDE.md is the user's later decision (14 Nov) and outranks the plan. The claude-api guidance is to keep Opus unless the user names another model; cost is the user's call. Volume is tiny, so the price gap matters less than the guardrail quality. |
| CX-05 | **Keyless public lookups (Razorpay IFSC, pincode) "now", or never?** | IR ranks them "Now (ships)". CLAUDE.md: "no calls to government or bank services". | **Defer to Future.** | A standing user decision outranks a research recommendation. IFSC lookup makes a bank-data call to a third party; the pincode lookup needs a field the app doesn't collect. Low value for the demo. |
| CX-06 | **Report every reason, or suppress quality issues for an ineligible applicant?** | Rulebook §6 "give every reason"; policy-engine spec §3.1 "suppress image issues". | **Rulebook: list every REJECT reason; do not ask an ineligible applicant to re-upload.** | The rulebook outranks the specs. Both agree that a REJECT is not combined with a re-upload request; they differ only on whether quality notes are mentioned. The engine already lists only REJECT reasons in a REJECT. |
| CX-07 | **Age 17.95–18.00: human or automatic?** | Guardrails spec: human band. Rulebook §2: "18 or older on the date the application is started", REJECT otherwise. | **Rulebook: automatic, on the application start date.** | Rulebook outranks; age is computed from the PAN DOB to the day. |
| CX-08 | **May an applicant replace an already-verified document?** | Rework spec §3: verified documents are locked. App: any document can be replaced. | **App behaviour stays; a replaced verified document is re-checked (RF-28 extends this to edited details).** | The rulebook is silent; locking would block correcting a mistake. The re-check keeps the audit trail honest. |
| CX-09 | **Wording of the spelling-variant follow-up** | Rulebook §8: "corrected document or a signed declaration in the attached format". Rework spec §2.2: "confirm your correct legal name or upload supporting proof". | **Rulebook wording; remove "attached format" until a template exists (RF-37).** | Rulebook outranks. |
| CX-10 | **Reviewer accuracy baseline: 97.5% or 87.0%?** | Brief Table 7: 97.5% at document level. AR and S1P: 87.0% (522/600) when rolled up per application. | **Report both, labelled by level.** | They measure different things; the roll-up rule is an assumption. |
| CX-11 | **"27% never reply"** | Brief: 27%. Data: 24.8% never re-upload, 27.3% drop before KYC, 42.6% returned and later dropped. | **Use 27.3% (no reply within 10 days after a return, 211 of 774), as S1P does.** | Matches the brief's figure and has a stated definition. |
| CX-12 | **Simulation: 7.4 / 6.1 days and +106, or the slides' 6.9 / 5.7 and +105?** | EV/S1P vs `PS-01_PROBLEM_BREAKDOWN_SLIDES_SUMMARY.md`. | **Use ours, reproduced independently by S1P; say the package slides differ and why the methods differ.** | Ours is reproducible from the workbook; the slides' method is not given. |
| CX-13 | **Reviewer cost: ₹14.7 lakh or ₹4.1–5.0 lakh?** | `03_OPERATIONAL_BASELINE_METRICS.md` vs S1P §3.1. | **₹4.1–5.0 lakh, labelled ESTIMATE.** | `manual_touches` counts one touch per application and per failed exam, not reviewer actions (checked arithmetic). |
| CX-14 | **Hand-decided 20: Claude's sample or the user's held-out labels?** | S1P: 20 decided by Claude from the test set. P2 Q9: 20 of the user-labelled held-out cases. | **Both, for different jobs.** Claude's 20 are a draft the team adopts or overrules for Stage 1; the user-labelled held-out set is still needed for out-of-sample accuracy. | The brief asks for "your team"; only a user-labelled, frozen set gives an independent check. |
| CX-15 | **Cockpit target: ≤ 90 s per case or < 5 min per application?** | Cockpit spec vs brief Table 7. | **Brief: < 5 minutes averaged over all applications; ≤ 12.5 minutes per routed case keeps both targets (RF-49).** | The brief outranks the specs. |
| CX-16 | **Instant feedback "via a `checksFor` helper inside the engine block" (plan) vs feedback built by calling `decide` and filtering outside it (code)** | PL S4 vs source | **Code's approach stands**: the engine block is unchanged by it. | Fewer engine edits; the evaluation still scores the engine block. |
| CX-17 | **IndexedDB (plan) or `localStorage` (code)?** | PL S3 vs source and PRODUCT A13 | **`localStorage` stands** for a small, minimised payload (RF-03). | The payload has no images; `localStorage` is enough and is already live. |
| CX-18 | **Test harness: hidden or visible to friends who try the demo?** | CR R15: hide it. CLAUDE.md: "Use specimen… so T2–T10 can be triggered without real documents" (needed for the demo). | **Behind a visible but collapsed "Demo controls" disclosure, plus `?demo=1` to open it.** Needs confirmation (GRILL_LOG G-06). | Keeps the user's demo path one click away while removing test labels from an applicant's first view. |

## 4. Where each finding lands

- **Decided in GRILL_LOG.md** (rounds 1–4): RF-01 to RF-80 and CX-01 to CX-18, each mapped to a grill question.
- **Built by PRD.md requirements**: every Open or Partly fixed finding maps to at least one `FR-` requirement (see the traceability table in PRD §12).
- **Needs a person** (cannot be settled by an AI): CX-01 and RF-67 (problem owner), RF-48 and RF-39 (real users and phones), RF-47 (user labels), RF-52 (user's console references), RF-80 (discovery notes), RF-57 (team adoption of the 20 decisions).
