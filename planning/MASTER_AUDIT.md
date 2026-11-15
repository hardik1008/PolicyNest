# PolicyNest master audit: build dcdc610..53f2eb2

- **Date:** 15 Nov 2026. **Auditor:** Opus master auditor (read-only; this file is the only edit).
- **Scope:** the 16 commits `c3ce809` … `53f2eb2` since `dcdc610`, against `PRD.md` → "Decisions confirmed by the user, 15 Nov 2026" (pass 1, pass 2, the original list, regressions, guardrails GR-1..GR-13).
- **Method:** I read the code. I ran `python tools/check_pack.py`. I traced the engine hash through every commit. I traced every figure on `#evaluation` to `eval/out/*.json` and `stage1/tables/process_map_steps.csv`. I ran a local preview (`python -m http.server 8917`, stopped afterwards) and drove it with Python Playwright (headless system Chrome, `channel="chrome"`; nothing was installed). Every scenario ran in a fresh browser context.
  - **To read the state:** I added `window.__pn = {S, QUIZ, …}` to the served HTML at request time, in the browser only. The file on disk was not touched, and the engine block (which the page hashes) is unchanged.
  - **Ignored, as briefed:** CORS errors to `policynest-copilot.embarko.app` and the favicon 404.
  - **Caution for the next tester:** a process I did not start (PID 20948, `python -I -m http.server 8765 --directory .`) also listens on port 8765. It serves a different, older page that has the sample applicant pre-filled. My first run hit it by mistake. All results below come from port 8917, whose `index.html` I checked byte-identical (md5 `2659db31…`) to `policynest_mvp/site/index.html`.

## Verdict

**Not ready to deploy yet, but close.** The build does most of what pass 1, pass 2 and the original list ask for. T1–T10 all reach the brief's outcome, and T4 and T8 go to a person, never an automatic reject. T10 re-checks only the two changed documents (8 checks run, 15 carried over, both rounds on the Audit trail). The §4.6 two-selfie rule works outside the engine, with one internal referral and a neutral applicant screen. Reviewer notes never reach applicant screens or the saved copy, even after a reload. The focus mode, demo controls, empty start, phone mode and Evaluation page meet their acceptance tests. The engine is intact: the only engine edit is `75b9f3b`, the hash `c2063887…` matches in all three places, `eval_predictions.csv` is unchanged since `dcdc610`, and the page shows "match".

Four things stop a deploy:
1. **Blocker:** in T4 the applicant's own verification screen shows the other person's name, the internal tier label and "recommend REJECT". The same data is in the saved copy. This breaks GR-4 in a scenario every judge runs.
2. **Major:** every document pop-up says "0 of 6 done", and the "all six documents are in" pop-up never fires (an H4 regression).
3. **Major:** after a person rejects a case, the reject panel says the decision "was made automatically".
4. **Major:** `BUILD_LOG.md` and the PRD progress table still say passes 1 and 2 "have not started".

`PRODUCT.md` and `CLAUDE.md` are stale as expected (list in the last section). Nothing is deployed, so no status may move to Built yet.

**Findings: 1 blocker, 3 major, 10 minor.**

## Findings

| ID | Severity | Requirement | File:line | Evidence | Exact fix |
|---|---|---|---|---|---|
| F-01 | **blocker** | GR-4, GR-12, FR-29 | `policynest_mvp/PolicyNest.html:743` (the engine writes `ev`), rendered at `:1264` (`verifyCard`, `esc(c.ev)`); saved by `persist` `:1876` | **T4, applicant view `#apply`:**<ul><li>the screen shows "RAHUL KUMAR SHARMA → ANKIT YADAV · Tier 7 (Different person) · recommend REJECT; a reviewer must confirm";</li><li>it is still shown after the reviewer rejects;</li><li>`saved_other_name: true`: "ANKIT" is in `pn-onboarding-v1`.</li></ul>Older than this build, but GR-4's test ("another person's data … on applicant screens or in the saved copy") fails. | Do not edit the engine; fix the display outside it.<ol><li>Add `applicantEv(c)`. It returns a neutral line ("A person on our team checks this document") when `c.res==="HUMAN"`, when `c.reviewer`, or when `c.code` is `NAME_MISMATCH` or `IDENTITY_NOT_CONFIRMED`; otherwise it returns `c.ev`. Use it in `verifyCard`, and build `S.obs` from neutral text too.</li><li>In the `persist` replacer, drop `ev`, `ev0` and the non-PAN `name` fields (`S.ex[k].name`, `S.docs[k].ocr.fields.name`) whenever a name-mismatch code is present, and rebuild them on restore the way `recText` is rebuilt.</li><li>The review console keeps the full evidence.</li><li>Re-test T4 before and after a reload.</li></ol> |
| F-02 | major | FR-16, FR-37, PRODUCT A6 | `PolicyNest.html:588` | `n=DOCS.filter(docClean).length` hands `docClean` a DOCS object, not its key, so `n` is always 0.<ul><li>Seen: "Rahul, your PAN card is verified. 0 of 6 done. Great start, keep going."</li><li>Seen: "Rahul, 6 documents verified. 0 of 6 done. Keep going."</li><li>The `n===6` "all six documents are in!" pop-up can never fire.</li></ul>Introduced in `1166166` (H4). Commit `05a3b6e` says the all-six toast was fixed. | `n=DOCS.filter(function(d){return docClean(d.k)}).length`. Re-test spec-all (expect "all six documents are in!") and one upload at a time (expect "1 of 6 done"). |
| F-03 | major | GR-10, FR-27 | `PolicyNest.html:1296` (`rejectPanel`) | After a reviewer rejects (T4 confirmed; the selfie rule, then Reject), the panel says "These are fixed eligibility rules, so the decision was made automatically and every reason is listed." The audit says otherwise: round 2 is `by: "reviewer"` and `touches: 1`. | Branch on `S.touches>0` or the last `S.rounds` entry having `by==="reviewer"`, and say: "A person on our team reviewed your application and made this decision. Every reason is listed." Keep the current sentence only for rule-based rejections. |
| F-04 | major | Process honesty (task §7) | `BUILD_LOG.md:3`, `:5`, `:117–118`, `:124`; `PRD.md:3`, `:37–39` | `BUILD_LOG.md:5` says "Pass 1, pass 2 and the rest of the plan have not started"; the PRD progress table says "Pass 1 \| Not started", "Pass 2 \| Not started". 16 commits implement them. | Add a dated row per lane to the BUILD_LOG timeline (H1–H6, N1, N2, with commits and "not deployed"). Change PRD `:37–39` to "Built, audited, **not deployed**", with the commit ranges. Remove "build paused". |
| F-05 | minor | FR-31, GR-4 (saved copy) | `PolicyNest.html:558` (`ruleTrail`), `:1876` | The `ROUTED_TO_REVIEWER` event is applicant-audience and saved. Its note is neutral ("FACE_MATCH_LOW"), but its `rules` field is "FACE_MATCH_LOW_REPEAT §4.6". `S.checks` in the saved copy also holds `FACE_MATCH_LOW_REPEAT`. Nothing is rendered on applicant screens (the Audit page is the ops view). Commit `b581609` ("routed event shows the neutral code") is true of the note only. | In `ruleTrail`, map `FACE_MATCH_LOW_REPEAT`→`FACE_MATCH_LOW`. In the persist replacer, write the neutral code for checks. |
| F-06 | minor | FR-43 | `PolicyNest.html:1345` (`render`), `:1354` (`stepChanged`) | The verification animation re-renders `#view-apply` on every tick, and `stepChanged` focuses the h1 only when the step number changes. After the decision, `document.activeElement` is `BODY`. On the documents step the h1 does get focus. | After `finishDecision` and `recheck`, focus `#view-apply h1`. Or, in `render`, keep and restore focus by id when the view is re-rendered on the same step. |
| F-07 | minor | FR-37 (one progress measure) | `PolicyNest.html:1057` (`accepted()`) vs `:1245` (`docClean`) | With a blurry PAN, the Documents page shows "5 / 6" verified and the tile "Needs a clearer photo", while the Dashboard shows "6 of 6 accepted". | Use the `docClean` count on the Dashboard, labelled "verified". |
| F-08 | minor | FR-37 (fleet numbers only on Evaluation) | `PolicyNest.html:1143` | The Audit page shows a "today 3.3" chip next to Human touches (brief line 289). It is sourced but sits outside the Evaluation page. | Remove the chip, or label it "brief baseline: 3.3 per application" and accept the exception in the PRD. |
| F-09 | minor | FR-42 | CSS for `.badge` (light `--ok` fill); `.face` | In-page audit, light theme at 1280 and 375 px: the "✓" tile badge is near-black on the ok fill at **3.20:1**, four per view (Documents, Dashboard). The "RK" avatar initials on the verification sidebar are orange on light at **2.42:1** (large text needs 3:1). Dark theme: 0 failures. Gradients were not measured. | Give the badge `aria-hidden` and treat it as an icon (3:1 passes), or use a lighter ok fill behind near-black. Draw the `.face` initials in `--ink`. |
| F-10 | minor | FR-27, FR-20 | `PolicyNest.html:864` (engine block) | `rejectReasons` UNDERAGE calls `P.dob.split` even when the underage check came from the typed DOB (`:757`, PAN DOB unread) → TypeError. It cannot be reached in the UI, because `validate()` refuses a typed DOB under 18. There is no underage specimen variant, so FR-27's "date shown" acceptance cannot be observed. | In a lane that owns the engine: `var d=P.dob||…typed dob`, then re-run `run_eval.js` and re-pin. Or add an "underage" PAN variant outside the engine. |
| F-11 | minor | GR-1 / FR-09 (nice to have) | `PolicyNest.html:1876` | The saved copy holds the full typed account number (`"50100284417"`). FR-09 is outside the confirmed scope; recorded so it is not lost. | Save `acct` as its last four (FR-09) when that item is scheduled. |
| F-12 | minor | GR-10, FR-33 (nice to have) | `PolicyNest.html:1301` | The human-review panel says "You will hear from us within 4 working hours", while the sidebar says "Target: within 4 working hours". | "We aim to reply within 4 working hours (our service target)." |
| F-13 | minor | FR-68 | `PRODUCT.md`, `CLAUDE.md` | Stale lines; full list below. Expected, since they were not yet updated. | Apply the list below, keeping "built, not deployed" until the live check. |
| F-14 | minor | FR-69 | `planning/DISCOVERY_QUESTIONS.md:9` | It says "FR-69 asks for 14 questions; this file has 13", but PRD `:379` now says 13. | Change it to "FR-69 asks for 13 questions (nine from the brief, four added); this file has 13." |

## T1–T10 (local preview, `?demo=1`, specimen variants)

| # | Variants | Expected | Observed | Result |
|---|---|---|---|---|
| T1 | all clean | Approve, no human touch | APPROVE, `STP_PASS`. 23 checks, all with a rule. 0 touches. Time to decision "under 1 s · this demo, on this device". Training → exam 100% → CERTIFIED `PN-POSP-…` | Pass |
| T2 | CLASS10 clean (initials) | Approve without asking | APPROVE, no follow-up | Pass |
| T3 | CLASS10 spelling | NMI, NAME_SPELLING_VARIANT | NEEDS_MORE_INFO; `NAME_SPELLING_VARIANT §5`; one message | Pass |
| T4 | Aadhaar front and Class 10 different person | Route to a person, never auto-reject | HUMAN_REVIEW; 2× `NAME_MISMATCH:HUMAN §5`. Console: Reject (disabled until a note), Ask, Approve; "AI recommends: REJECT". **Applicant screen shows the other name (F-01)** | Pass on routing; fails GR-4 |
| T5 | CLASS10 blurry, BANK parent | Both fixes in one message | NMI; `IMAGE_BLURRY §4.1` and `BANK_NAME_MISMATCH §4.5` in one message ("we need 2 things") | Pass |
| T6 | PAN company | REJECT, PAN_NOT_INDIVIDUAL, plain words | REJECT `PAN_NOT_INDIVIDUAL §4.2`; plain text; buttons Dispute / Start a new application / Delete my saved progress. Dispute → HUMAN_REVIEW, console Uphold / Ask / Overturn | Pass |
| T7 | Aadhaar front DOB +1 yr | NMI, DOB_MISMATCH | NMI `DOB_MISMATCH §4.3`; the message asks for a document | Pass |
| T8 | Selfie 0.68 | Route to a person | HUMAN_REVIEW `FACE_MATCH_BORDERLINE §4.6`. Reviewer Approve → APPROVE, round 2 by reviewer, 1 touch | Pass |
| T9 | Aadhaar back other state | Information only; approve | APPROVE; "Address state §4.3" INFO | Pass |
| T10 | T5, then the fix panel → clean specimens → Send fixes | Re-check only what changed; both rounds in the audit | Round 2: changed `CLASS10, BANK`; "8 checks run, 15 carried over"; APPROVE. The Audit page shows both round cards. Pop-up "all your fixes are in" appeared before Resubmit | Pass |

Also run: real OCR (Tesseract) on a canvas PAN. The **Aadhaar-front slot refused it**: "This looks like a PAN card, not an Aadhaar card (front)…". The PAN slot read name, DOB and PAN at confidence 0.95 (FR-14 pass). No console errors in any flow, apart from the CORS and favicon errors I was told to ignore.

## Guardrails and cross-lane checks

| Check | Observed | Result |
|---|---|---|
| GR-2: no 12-digit run | No match for `(?<!\d)\d{12}(?!\d)` in the saved copy (T4 with save; mid-documents save) or in `queue_seed.json`; Aadhaar shown as `XXXX-XXXX-4417` | Pass |
| GR-4: canary reviewer note | Note `CANARY4` on a T4 reject: absent from `#apply`, the Dashboard and `pn-onboarding-v1`. Present on the Audit page with the "internal" chip in the same session. After a reload: gone from the Audit page, and the dispute console's note field is empty. Two-selfie case `CANARYSELFIE`: not saved | Pass |
| GR-4: fraud wording | Scanned for fraud/fake/forged/tamper/suspicious/twice/"in a row"/repeat/§7 on applicant views in T1–T10, the selfie flows and after reload: none. Saved copy: only the code `FACE_MATCH_LOW_REPEAT` (F-05) | Pass, with F-05 |
| GR-4: another person's data | T4: shown and saved (F-01) | **Fail** |
| GR-5: person confirms | T4 and T8 routed. Two selfie failures → HUMAN_REVIEW. Disputes → console | Pass |
| GR-6: every decision cites its rule | `checks without rule = 0` in every scenario. Decision events carry `rules`, `engine`, `hash c206388747e8` and the round | Pass |
| GR-10: simulated labels | "Simulated verification result" on cards, "simulated registry", "Simulated face-match score", "(simulated send)" | Pass |
| GR-10: no invented numbers | Embedded `EVAL.now/extra/first/sim` equal `eval_results.json`, `extra.json`, `baseline_3.3.0.json` and `simulation.json` exactly. All 10 `pmap` rows match `process_map_steps.csv`. "60.7%" = 364/600 from the confusion matrix. "6.9 / 5.7 / +105" from `PS-01_PROBLEM_BREAKDOWN_SLIDES_SUMMARY.md:105,107`. Targets 95/98/60% from brief `:328–330` | Pass |
| GR-13: focus exits never evidence | `FOCUS_EXIT` note: "Left the onboarding screen · warning shown · nothing reset" (no seconds); not used by `decide` | Pass |
| Sitting + save consent + restore | Saved with consent → reload → "Welcome back, Rahul · 3 of 6 documents verified" → Resume: sitting 2, 3 docs kept. Without consent: `localStorage` empty after a full document run | Pass |
| Demo controls + fix panel | The fix panel has its own Demo controls (variant picker plus Use specimen), open with `?demo=1` | Pass |
| Internal events + restore + console | After a reload, internal events and reviewer wording are stripped. The review console after a dispute shows no old note | Pass |
| Progress + recheck | The T10 round cards are correct. Dashboard vs Documents disagree on a blurry PAN (F-07) | Pass, with F-07 |
| Pop-up gating + re-uploads | Blurry PAN: no "verified" pop-up for the PAN, tile "Needs a clearer photo". Re-upload: "got it", then "all your fixes are in". Counts wrong (F-02) | Pass, with F-02 |
| Selfie rule + disputes + approvals | 0.52, then 0.52 → HUMAN_REVIEW, one `FRAUD_DESK_REFERRAL` (internal); applicant sees "Score 0.52 · a person compares the photos". 0.52, then 0.68 → run reset → borderline route; Ask, then 0.52 → `faceRun 1` → NMI. Approve → APPROVE. Reject → REJECT `IDENTITY_NOT_CONFIRMED §4.6`, still one referral → Dispute → Overturn → APPROVE | Pass, with F-03 and F-05 |

## Per-FR status

| FR | Status | Evidence / note |
|---|---|---|
| FR-41 | pass (code only) | `:461`: `label:has(+ input[type=file]:focus-visible){outline:3px solid var(--ink)}`. Keyboard ring not seen at runtime |
| FR-42 | pass with fixes | F-09. Orange fills carry near-black text; the dark theme has 0 failures |
| FR-43 | pass with fixes | `#sr-status` is the status region; `#view-apply` has no `aria-live`; the h1 is focused on the documents step. F-06 |
| FR-44 | pass | Skip link `#main`; nav links `#dashboard…#audit`; headings h1→h2; no duplicate upload or specimen names; phone header 76 px; no target under 24 px (`#f-save` is 20 px but inside a 46 px label). Field-error described-by not tested |
| FR-45 | pass | `<dialog>` with role `alertdialog`; Escape closes it and the sitting carries on |
| FR-05 | pass | With the clock shifted: "10 minutes left" at 20 min, "2 minutes left" at 28 min, "sitting has ended" at 30 min. Extend ×5 gave 10 min each time; Submit ends the sitting |
| FR-06 | pass | One `FOCUS_EXIT`, no duration; `fullscreenchange` adds 0 events and shows the banner |
| FR-07 | pass | 375 px touch emulation: Start → sitting, no full screen; tab switch → no dialog, 0 exits. Desktop "Start without full screen" works; a desktop Start logs "full screen requested" and no error |
| FR-01 | pass | Without `?demo=1`: every field empty, `#f-save` unticked, Dashboard "Consent … not given", no name |
| FR-02 | pass | One closed "Demo controls (synthetic documents)" panel; no visible "· T…" labels without `?demo=1`; open with it |
| FR-03 | pass | The checklist covers the six documents with what is accepted and refused, the steps after (15 h, 50%, 24 h retake), what is saved and for how long, the sitting's scope, language, and a shared-device line |
| FR-16 | pass with fixes | The gate is right; the counts are wrong (F-02) |
| FR-36 | pass | `check_pack` banned phrases pass; no time or success claims found |
| FR-55 | pass | Internal chip; label "Ops and compliance view (this demo shows both roles)"; never rendered for the applicant or saved |
| FR-27 | pass with fixes | Three actions present; Dispute-button wording in `75b9f3b`; F-03; the underage date cannot be observed (F-10) |
| FR-38 | pass | Fresh: consent "not given". Sample: "given (sample applicant)". "No other POSP registration found (simulated registry)". "15 hours of training: not checked in this demo" |
| FR-23 | pass | "under 1 s · Time to decision (this demo, on this device)"; no 17.3 h or 8.4 days on applicant views |
| FR-37 | pass with fixes | F-02, F-07, F-08 |
| FR-56 | pass | Decision events show the rule trail, round, `policy-engine 3.4.0` and `hash c206388747e8` |
| FR-57 (page) | pass | "Measured engine: c206388747e8 · Running engine: c206388747e8 · match". The build warns on a mismatch (code read: `build_site.py`); the one-character edit test was not run (no edits allowed) |
| FR-59 | pass | 7× "in-sample", "Routed to a person: 11 of 600", "no gap in-sample", the 60.7% row, "Directional", "simulated estimate" |
| FR-61 | pass | Table with source and "elapsed clock hours"; 10 rows equal the CSV |
| FR-62 | pass | 16 cases: 11 "test-set case" (the same 11 IDs as HUMAN_REVIEW in `eval_predictions.csv`) and 5 "constructed case" (borderline face, surname, unlisted board, PAN dispute, two selfie failures); ages `simulated`; no 12-digit run. `queue.py` was not re-run (it writes into `eval/out`) |
| FR-63 | pass | `kpis.json`: every item has a `source`; overrides `null`, "this browser session only" |
| FR-31 | pass, minor F-05 | See the selfie row above; engine hash unchanged |
| FR-60 (runner) | pass (not executed) | `eval/holdout/README.md` procedure (freeze → hash → verify → run → report apart); the template headers match the test-set CSVs |
| FR-69 | pass with fixes | 13 questions; nine word for word from the brief (`:189–209` checked); F-14 |
| FR-68 (part) | fail, as expected | See the list below |
| FR-14 | pass | Real-OCR PAN refused in the Aadhaar slot with the slot named |
| FR-19 | pass | T5 asks again for the blurry marksheet; no `text`, `thumb` or `url` key in the saved copy |
| FR-20 | pass | Engine edited only in `75b9f3b` (hash at each commit: `c5da9cfb…` up to `ff8bad9`, `c2063887…` from `75b9f3b` on); PINNED = `engine_sha256` = page |
| FR-21 | pass | T9 typed vs card is INFO |
| FR-22 | pass (stored results) | `eval_predictions.csv` is unchanged since `dcdc610` (`git diff --stat` empty). The evaluation was not re-run here (papaparse not installed) |
| FR-26 | pass | T10 |
| FR-28 | pass | T6 dispute → Uphold / Ask / Overturn |
| FR-29 | pass with fixes | Routing is right; applicant display F-01 |
| FR-30 | pass | T8 |
| FR-32 | pass | Reject disabled without a note; the reviewer's selfie approval stands; touches counted |
| FR-52 | pass | With `llm` off, the Copilot answers "From the Rulebook §3 … · AI answers not connected" with sources |

**Not tested:**
- the Hindi message and screen;
- iOS Safari;
- the file-picker exit flag (FR-08);
- Escape on the expiry dialog;
- the check-count chip with an INFO result (T9 Dashboard);
- the certificate's "time taken" line;
- a re-run of the evaluation, `queue.py` or `kpis.py`;
- an AI answer (no key);
- the live site (nothing deployed).

## Process honesty: claims vs code

- **Commit `05a3b6e`, "all-six toast":** not true at runtime (F-02).
- **Commit `b581609`, "routed event shows the neutral code":** true of `note`, not of `rules` (F-05).
- **Commit `75b9f3b`, "600 predictions byte-identical":** consistent. The predictions file has no diff since `dcdc610`, and `eval_results.json` changed only in `run_at`, `engine_sha256` and the timing.
- **Other claims I sampled:** the H1, H2, H3 and H5 commit messages match the code and the runtime results above.
- **`BUILD_LOG.md` and `PRD.md`:** untrue progress statements (F-04).
- **`PRODUCT.md` and `CLAUDE.md`:** not yet updated (expected; list below).

## Doc lines to update (FR-68). Keep "built, not deployed" until the live check

**PRODUCT.md**
- `:6` Written/updated line: add "15 Nov: passes 1–2, §4.6 rule, queue data, discovery questions built locally; not deployed".
- `:58` A6: "on every success" holds only after F-02 is fixed; add "progress counts fixed 15 Nov" once fixed.
- `:60` A11: add the sitting's scope (details and documents only), the language line and the shared-device line; the save-consent box is unticked by default.
- `:61` A12: "full screen" → "optional full screen ('Start without full screen'); no full screen and no exit warnings on touch devices; closing full screen shows a banner and is not an exit; timer can be hidden or turned off; `FOCUS_EXIT` has no duration".
- `:65` A8: check the certificate fields at the live check (time taken was not seen in this audit).
- `:67` A10: "Not built" → "Built locally 15 Nov (H1), not deployed; light-theme badge and avatar contrast open (F-09)"; delete "(state is still not kept)". State is kept with consent.
- New row, or added to A1/A2: an empty form, and Demo controls (specimens, variants, sample) behind a closed panel opened by `?demo=1`.
- `:108` R6: add "queue data built (`eval/out/queue_seed.json`, `kpis.json`); screens still wait for references".
- `:110` R8: "Not built" → "Built locally 15 Nov (`96722e8`, `b581609`), outside the engine; not deployed".
- `:117` E1: add "engine hash on each decision event; internal events marked and never saved".
- `:167` time to decision: "Seconds on the live site" → "under 1 s, measured to the decision (this demo, on this device)".
- `:182` §8 item 1: the image pack exists (`usability/image_pack/`); change "is not made yet".
- `:185` §8 item 4: the held-out procedure and templates exist (`eval/holdout/`); labels are not made.
- `:186` §8 item 5: "Notes … never provided" → see `planning/DISCOVERY_QUESTIONS.md` (13 questions, all "not asked").
- `:198` "the brief's ten questions" → "nine questions" (`planning/DISCOVERY_QUESTIONS.md`).
- `:208` Stage 1 process map: "Not found … Planned" → "Built locally on the Evaluation page (`stage1/tables/process_map_steps.csv`); not deployed".
- `:225` "Five situations stay with a person": add a sixth, two selfie scores below 0.60 in a row (§4.6).

**CLAUDE.md**
- `:39` "Go-ahead: nothing in this list is built until the user says go" → record what was built 15 Nov (accessibility, queue data, §4.6) and what remains (Node held-out labels, prints, bench, deck).
- `:64` Saving: add that `rnote`, internal events and the reviewer note and recommendation are never saved; restore strips legacy internal events.
- `:65` Sitting: `fullscreenchange` now shows a "return to full screen" banner, not a warning. Touch devices get no full screen and no warnings. Hide-timer and turn-off-limit controls; a native `<dialog>`, where Escape means keep working.
- `:76` "Use specimen": the variant pickers, specimens and "Load sample applicant" live in Demo controls, open with `?demo=1`.
- `:104` "Status against the brief (as of 13 Nov 2026)": re-date it and add the 15 Nov work.
- `:114` "disputes are not built" → disputes are built (step 3); the reject panel also has Start a new application and Delete my saved progress.
- `:121` How to test: use `?demo=1`. Then `[data-act=begin-nofs]` (or `begin`), then `[data-act=sample]` inside Demo controls, then `details-next` ×4. Note that `S` is inside an IIFE and is not on `window`.
- `:125` Engine check: the live site still runs `c5da9cfb…`; the current hash is `c2063887…` (`tools/check_pack.py` PINNED). Redeploy before any live T1–T10 check.
- The "Where things are" table: add `tools/check_pack.py`, `eval/queue.py`, `eval/kpis.py`, `eval/holdout/`, `planning/DISCOVERY_QUESTIONS.md`.

**BUILD_LOG.md / PRD.md:** see F-04. Also `planning/DISCOVERY_QUESTIONS.md:9`: see F-14.

## Preview server

Started `python -m http.server 8917 --bind 127.0.0.1 --directory policynest_mvp/site` (and briefly one on 8765). I stopped both: `curl http://127.0.0.1:8917/` now fails to connect (exit 7), and no python process of mine is listed. Other servers on ports 8000, 8765 (PID 20948) and 8803 were already running and are not mine; I left them alone. `git status` is clean.
