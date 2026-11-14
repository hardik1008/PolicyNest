# PolicyNest Stage 1 pack: process map, 20 hand-decided applications, first business case

PS-01 "AI-First Onboarding", Stage 1 ("Understand and scope"). Written 14 Nov 2026. All data is synthetic.

**What this pack is.** It fills the three Stage 1 rows that `PRODUCT.md` §9 marks "Not found": the process map, the 20 hand-decided applications, and the first business case. Every number comes from a file in `D:\` (named in the table or in `tables/`) or from an assumption written next to it. Estimates are labelled **ESTIMATE**; measured values are labelled **MEASURED**. Scripts that produced everything are in `scripts/` (standard library only; they read the .xlsx files directly).

**Who did what.** The 20 decisions in Part 2 were made by Claude (an AI assistant), not by a human team. The brief asks for "your team", so a team member should read them and adopt or overrule them before they are shown as the team's own.

## Headlines

| | |
|---|---|
| Journey | 3,000 starts, 1,732 certified (57.7%). 42.3% lost: 482 never start training after approval (the biggest single loss), 314 rejected, 258 never upload, 211 go silent after a return, 3 still in progress. |
| Where time goes | 17.9 h to upload, **17.3 h in a queue** (P90 38.2 h), 23.3 h from approval to training start, 69.5 h of training. Median 8.41 days start to certificate, P90 13.0 days. |
| One-at-a-time rounds | Smaller than the brief suggests: 703 of the 774 returned applications were returned once. Only **75 extra rounds** exist in nine months. |
| Hand decisions | **20 of 20 match** `final_decision` (10 hard cases). Written and hashed before the answer key was opened. A perfect score on 20 only shows accuracy is probably above ~85%; the 600-case run is the real evidence. |
| Business case, reviewer time | ESTIMATE: 946 reviewer hours in nine months (₹4.1 lakh at ₹430/h). Hitting the straight-through floor saves ~568 h (₹2.4 lakh); hitting the <5-minute target saves ~718 h (₹3.1 lakh). That is only 0.4 to 0.5 of one full-time reviewer, so the saving is capacity, not headcount. |
| Business case, applicants | ESTIMATE: 68,104 file-hours of waiting in queues and reviews; 40,500 of them removed if 60% of passes are decided in 10 minutes. Median time to certificate 8.4 → 7.4 days (6.1 with the training link sent at approval). |
| Business case, drop-offs | The data does **not** show that faster review reduces silence or non-start (Part 3.4), so drop-off savings are what-if arithmetic, not a forecast: +40 to +343 certified agents in nine months for assumed behaviour changes. |

---

## Part 1. Process map of today's journey

**Source:** `PS-01_posp_applications.xlsx`, sheets `applications` and `stage_events`. Script `scripts/part1_process_map.py`; table `tables/process_map_steps.csv`.

### 1.1 Data preparation

- `applications` has 3,018 rows; **18 are exact duplicates** (checked field by field), leaving **3,000** applications. `stage_events` has 21,188 rows with **no duplicate events** and covers exactly those 3,000 applications. Dedup was done on `application_id` before any count.
- Dates in the workbook are Excel serial numbers; times below are elapsed clock hours (not working hours).
- Event order per application was checked: 16 distinct paths exist, all explained by the diagram below. Every application's final status matches its last event (0 mismatches).
- A step's "lost" count is the number of applications whose last event happened at that step (`AUTO_EXPIRED` or `REJECTED`). "Entering" counts applications, not events. Times are per instance (an application returned twice contributes two instances to the fix step).

### 1.2 The step table (MEASURED)

| # | Step | Actor | Entering | Lost | Lost % of entering | Median | P90 |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | Apply (`APPLICATION_STARTED`) | Applicant | 3,000 | – | – | – | – |
| 2 | Upload documents | Applicant | 3,000 | 258 (no upload in 7 days) | 8.6% | 17.9 h | 46.3 h |
| 3 | Wait for a reviewer | Queue (nobody acts) | 2,742 | 0 | 0.0% | **17.3 h** | **38.2 h** |
| 4 | First review | Ops reviewer, 22 people | 2,742 | 314 rejected | 11.5% | 0.23 h (14 min) | 0.35 h (21 min) |
| 4a | Applicant fixes returned documents | Applicant | 774 returned | 211 (no reply in 10 days) | 27.3% | **39.0 h** | 88.6 h |
| 4b | Wait for re-check | Queue | 582 replied | 0 | 0.0% | 14.6 h | 33.6 h |
| 4c | Re-check | Ops reviewer | 582 | 0 | 0.0% | 0.2 h | 0.3 h |
| 5 | Start training | Applicant | 2,217 approved | **482** (not started in 14 days) | **21.7%** | **23.3 h** | 60.6 h |
| 6 | Training (15 h) | Applicant on the training platform | 1,735 | 0 | 0.0% | 69.5 h (2.9 d) | 146.3 h |
| 7 | Exam (retakes included) | Applicant | 1,735 | 0 (160 failed once, all passed on retake) | 0.0% | 19.8 h | 65.5 h |
| 8 | Certificate | System | 1,735 | 0 (3 not yet issued at 30 Sep) | 0.0% | 10.7 h | 28.9 h |
| | **Start to certificate** | | 3,000 | 1,268 not certified | 42.3% | **201.9 h = 8.41 days** | 312.2 h = 13.0 days |

Round-trip for one return (4a + 4b + 4c, sum of medians): 53.8 h, about **2.2 days**, which agrees with the brief's "roughly two days". The best quartile of certified agents takes 157.7 h (6.6 days). Step 4 is the elapsed time from "review started" to the reviewer's outcome in the log; it is shorter than the 20.7 reviewer minutes in the test set (see 3.1).

First-review outcomes (MEASURED): 1,654 approved straight away (60.3%), 774 returned (28.2%), 314 rejected (11.5%).

Reasons recorded in the event notes (`tables/process_map_return_and_reject_reasons.csv`):

| Returns (849 events on 774 applications) | Events | Rejections (314) | Applications |
|---|---:|---|---:|
| Image blurry or cropped | 423 | EDU_NOT_ELIGIBLE | 87 |
| Name spelling differs (PAN vs marksheet) | 130 | ALREADY_REGISTERED | 75 |
| DOB on Aadhaar differs from PAN | 115 | NAME_MISMATCH_HARD | 53 |
| Account holder name differs | 111 | UNDERAGE | 49 |
| Photo does not match PAN photo | 70 | PAN_FORMAT_INVALID | 37 |
| | | PAN_NOT_INDIVIDUAL | 13 |

### 1.3 Text diagram

```
 3,000 START ──► UPLOAD DOCS ───────► QUEUE ─────► FIRST REVIEW ─────────► APPROVED (KYC) ─────► START TRAINING
  (applicant)    median 17.9 h        median 17.3 h   (reviewer, ~14 min)    1,654 direct           median 23.3 h
     │           P90 46.3 h           P90 38.2 h            │                + 563 after fix            │
     │                │                    2,742           │                = 2,217                    │
     ▼                ▼                                      │                                           ▼
 258 LOST         2,742 ───────────────────────────────────► ├─► 314 REJECTED (ineligible)         482 LOST (14 days
 (7 days, no                                                 │                                       no training start)
  upload)                                                    │                                           │
                                                             └─► 774 RETURNED ──► APPLICANT FIXES ──┐    ▼
                                                                  (849 requests)   median 39.0 h    │  1,735 TRAINING ──► EXAM ──► CERTIFICATE
                                                                                   P90 88.6 h       │   median 69.5 h     19.8 h     10.7 h
                                                                                  211 LOST (10 days)│   (160 fail once,   (all pass   1,732 certified
                                                                                       │            │    pass on retake)  on retake)  + 3 pending
                                                                                  582 reply ──► QUEUE 14.6 h ──► RE-CHECK ──► approved (563)
                                                                                                                       or returned again (71 second returns)
```

Conservation check: 3,000 − 258 − 314 − 211 − 482 − 3 pending = **1,732** certified. ✓

### 1.4 What the map shows

1. **The largest leak is after approval, not before.** 482 approved applicants (21.7% of 2,217) never open the training; the log shows no reminder or system action in that window. It is 16.1% of all starts. It does not vary with how long KYC took (Part 3.4).
2. **Queue plus re-queue is the clearest product-controllable delay**: 17.3 h median before every first review and 14.6 h before every re-check (68,104 file-hours in total, Part 3.2). The review itself is short.
3. **Silence after a return is 27.3%** and depends on what is asked: name-spelling returns 36%, DOB 32%, poor image 26%, bank name 22%, face 16% (Part 3.4). The spelling and DOB requests ask for a corrected document or an affidavit.
4. **One-at-a-time returns are a small share of rounds.** 703 applications were returned once, 67 twice and 4 three times: 849 returns on 774 applications, so **75 extra rounds** (8.8% of returns). Cutting every follow-up to one round would remove those 75, not the 774. The 2-day round trip is real, but most of its cost is the first return, which a one-message follow-up does not avoid; what the product removes is the queue (17.3 h + 14.6 h) and the wait for a person.
5. **Applicants own most of the median time.** Upload (17.9 h), fix (39.0 h), training (69.5 h), exam (19.8 h) are applicant steps; the product can only influence them with clearer messages, instant links and reminders.

### 1.5 Where this differs from the package's own baseline note

`02_BUSINESS_REQUIREMENTS/03_OPERATIONAL_BASELINE_METRICS.md` was checked against the workbook. These **match**: all funnel counts, queue 17.3 h and 38.2 h, end-to-end 8.4 and 13.0 days, the 17.9 h median upload, the 23.3 h approval-to-training median, ₹430 average hourly cost, 9,920 touches. These **do not reproduce** from `stage_events`:

| Item | Package note | From the workbook |
|---|---|---|
| Upload P90 | 42.1 h | 46.3 h |
| Approval → training start P90 | 72.0 h | 60.6 h |
| Training median / P90 | 3.1 d / 6.4 d | 2.90 d / 6.09 d |
| Exam pass → certificate median / P90 | 1.1 d / 2.5 d | 0.45 d (10.7 h) / 1.2 d (28.9 h) |
| 9-month reviewer cost | ₹14.7 lakh | ₹4.1–5.0 lakh (Part 3.1) |

`06_DATA_DICTIONARY/COMPLETE_DATA_DICTIONARY.md` also does not describe this workbook (it quotes 3,018 applications as the cohort, 114.2 h median, ₹1,450 per agent, 33.2% drop-off, 38.4% first-pass yield, ₹280–520 hourly rates, `REV-` reviewer ids; the workbook has `OPS-` ids, hourly rates of ₹380–₹480 and 31.7% dropped). Use the workbook, not that file.

---

## Part 2. 20 applications decided by hand

**Source:** `PS-01_document_review_test_set.xlsx` (sheets `documents`, `application_truth`) and `PS-01_onboarding_rulebook.docx` (v3.2; its text is identical to `03_RULEBOOK_AND_REGULATIONS/PS-01_ONBOARDING_RULEBOOK_V3_2.md`). Scripts `scripts/part2_*.py`; tables `tables/part2_*.csv`.

### 2.1 Method (what was done, in order)

1. **Split the workbook** so the answer was out of sight. `inputs_apps.csv` held only what an applicant side knows (declared name, DOB, PAN, education, state, the penny-drop name and the registry hit). `docs_inputs.csv` held every document's image-quality tag, OCR confidence, OCR text and parser fields, with the reviewers' `human_verdict`, `human_reason_code` and `reviewer_minutes` removed. `final_decision`, `decision_reasons`, `name_match_category` and the reviewers' document verdicts were put in a sealed file. Only `is_hard_case` was read, to choose the sample.
2. **Draw the sample with a fixed seed (20261114)** and a design fixed beforehand using only inputs: 10 hard cases at random; 10 not-hard cases = 3 with a poor-quality document, 1 with a face score below 0.60, 1 with a malformed or non-individual PAN, 1 with an IRDAI registry hit, 1 with an unusual declared education, 3 plain. (A first draw had a faulty PAN pattern; it was fixed before any case was opened.) Result: 20 cases, **10 hard**, listed in `tables/part2_sample_ids.csv`.
3. **Read each case and decide** from the OCR text and the rulebook, writing the decision, every reason code, the rulebook section and whether a person must confirm. I also used the `created_at` date from the applications workbook (the rulebook's "age on the date the application is started") and did not read its `status` or `rejection_reason`.
4. **Freeze the decisions.** `tables/part2_hand_decisions.csv` was written for all 20 and its SHA-256 saved in `tables/part2_hand_decisions.sha256` (`30a317d7…ce3ff`) **before** `final_decision` was opened for any of them.
5. **Compare** (`scripts/part2_compare.py` → `tables/part2_comparison.csv`).

### 2.2 Result: 20 of 20 decisions agree

| App | Hard | My decision (codes) | Truth `final_decision` (truth codes) | Match | What decided it |
|---|:--:|---|---|:--:|---|
| APP-26016 | yes | REJECT (NAME_MISMATCH, DOB_MISMATCH) | REJECT (NAME_MISMATCH_HARD; DOB_MISMATCH) | ✓ | Marksheet name SOUMYA DUTTA vs ANKIT MITTAL; Aadhaar DOB 2004 vs PAN 2005. Person confirms the name rejection |
| APP-26017 | | REJECT (PAN_FORMAT_INVALID) | REJECT (PAN_FORMAT_INVALID) | ✓ | PAN `OUKPC227OR`, typed and on the card alike: digit block `227O` |
| APP-26061 | yes | APPROVE | APPROVE (ADDRESS_STATE_MISMATCH, informational) | ✓ | Aadhaar in Haryana, form says Uttar Pradesh: informational only |
| APP-26100 | | NEEDS_MORE_INFO (FACE_MATCH_LOW) | NEEDS_MORE_INFO (FACE_LOW) | ✓ | Selfie 0.42; ask for a fresh selfie |
| APP-26131 | yes | APPROVE | APPROVE (ADDRESS_STATE_MISMATCH, informational) | ✓ | Selfie 0.76, just above the 0.75 line; Aadhaar state differs |
| APP-26216 | yes | NEEDS_MORE_INFO (DOB_MISMATCH, BANK_NAME_MISMATCH) | NEEDS_MORE_INFO (DOB_MISMATCH; BANK_NAME_MISMATCH) | ✓ | Aadhaar DOB 14/03 vs 14/04; cheque and penny-drop name two other people |
| APP-26260 | | NEEDS_MORE_INFO (IMAGE_BLURRY) | NEEDS_MORE_INFO (POOR_QUALITY) | ✓ | Blurry PAN (OCR 0.647). Turned 18 on 14/06/2026, started 02/07, so not underage |
| APP-26322 | | APPROVE | APPROVE | ✓ | Clean; NIOS marksheet accepted |
| APP-26336 | | APPROVE | APPROVE | ✓ | Clean |
| APP-26391 | yes | NEEDS_MORE_INFO (NAME_SPELLING_VARIANT) | NEEDS_MORE_INFO (NAME_SPELLING) | ✓ | AJAY on PAN, AJAI on Aadhaar and marksheet |
| APP-26402 | yes | APPROVE | APPROVE | ✓ | SURESH SHETTY → SURESH KUMAR SHETTY: middle name added = match |
| APP-26405 | yes | APPROVE | APPROVE | ✓ | Nothing visible to ask; truth's name category is MIDDLE_MISSING but no middle name appears in any document text |
| APP-26442 | yes | NEEDS_MORE_INFO (DOB_MISMATCH) | NEEDS_MORE_INFO (DOB_MISMATCH) | ✓ | Aadhaar DOB 03/08 vs PAN 03/09. Eligible by age on either date |
| APP-26461 | | REJECT (ALREADY_REGISTERED, NAME_MISMATCH) | REJECT (ALREADY_REGISTERED; NAME_MISMATCH_HARD) | ✓ | Registry hit; marksheet in the name NILESH DESAI. Person confirms the name rejection |
| APP-26464 | yes | APPROVE | APPROVE | ✓ | OMKAR CHAVAN → CHAVAN OMKAR: swapped order = match |
| APP-26475 | | NEEDS_MORE_INFO (IMAGE_CROPPED) | NEEDS_MORE_INFO (POOR_QUALITY) | ✓ | PAN cropped: name and DOB lines missing |
| APP-26478 | | NEEDS_MORE_INFO (IMAGE_GLARE) | NEEDS_MORE_INFO (POOR_QUALITY) | ✓ | Aadhaar front under glare (OCR 0.599) |
| APP-26590 | | REJECT (ALREADY_REGISTERED, FACE_MATCH_LOW) | REJECT (ALREADY_REGISTERED; FACE_LOW) | ✓ | Registry hit; also selfie 0.54 |
| APP-26610 | | REJECT (EDU_NOT_ELIGIBLE) | REJECT (EDU_NOT_ELIGIBLE) | ✓ | Marksheet says Result: FAIL; declared Class 8 |
| APP-26644 | yes | APPROVE | APPROVE | ✓ | DEBJANI SAHOO → DEBJANI KUMARI SAHOO: middle name added = match |

Full reasoning, with rulebook sections, for each case is in `tables/part2_hand_decisions.csv`. Side-by-side with the key and with the reviewers' rolled-up document verdicts: `tables/part2_comparison.csv`.

| Measure | Value |
|---|---|
| Decisions that agree | **20 of 20** (8 APPROVE, 7 NEEDS_MORE_INFO, 5 REJECT; the truth has the same split) |
| Hard cases | 10 of 10 agree |
| Reason codes | Every reason I listed is in the truth's reasons and vice versa, including the three two-reason cases (APP-26016, 26461, 26590), after mapping vocabulary |
| Cases I routed to a person | 2 (APP-26016, 26461: the NAME_MISMATCH rejections, rulebook §9) |
| For comparison, the reviewers' own document verdicts rolled up with the rulebook's §6 rule | 17 of 20 on this sample; **522 of 600 (87.0%)** on the whole test set, reproduced here. The three misses (APP-26131, 26402, 26590) are reviewer-error rows: `NEEDS_INFO / REVIEWER_DISCRETION` on clean documents, and a registry hit that is not a document verdict |

### 2.3 Disagreements and doubts, honestly

- **There was no disagreement on a decision.** So there is no disagreement to explain, and 20 of 20 is not evidence of 100%: with 20 cases a perfect score only supports "the true rate is probably above about 85%" (rule of three: 3/20). The accuracy claim rests on the 600-case run (`eval/EVALUATION_REPORT.md`), which this pack does not redo.
- **The blindness is only about the answer key.** I had read `PRODUCT.md` and `CLAUDE.md` first, which describe rules the previous session drew from this same data (for example that a typed PAN equal to the card is not corrected). That could have helped on APP-26017. A fresh reviewer, or a second person doing the same 20, would be a cleaner test.
- **Where I was least sure when I decided (before opening the key):** APP-26017 (the `O` in the digit block could have been OCR noise, but the typed PAN has the same `O`, and the documented noise runs the other way); APP-26016 and APP-26461 (a different candidate name, while the father's name and DOB match the PAN: the rulebook has no row for that, so I treated the name as a different person and routed it to a person); APP-26610 (the marks look like passes but the result line says FAIL; the rulebook only falls back to marks when no result line exists).
- **Differences in wording, not in decisions.** The truth's `decision_reasons` use `POOR_QUALITY`, `FACE_LOW`, `NAME_SPELLING`, `NAME_MISMATCH_HARD` and `ADDRESS_STATE_MISMATCH (INFORMATIONAL ONLY)`, while the `reason_codes` sheet lists `IMAGE_BLURRY / IMAGE_CROPPED / IMAGE_GLARE`, `FACE_MATCH_LOW`, `NAME_SPELLING_VARIANT` and `NAME_MISMATCH`. I used the rulebook's and `reason_codes` names, which are finer for image problems. The engine's evaluation has to map between the two.
- **Not covered by this sample, or by the test set:** a surname change after marriage, a marksheet from an unlisted board, and a face score between 0.60 and 0.75 (rulebook §9 Human-only). They are not in the 600, so the 20 could not include them.
- Inputs are OCR text, not images, as in the data pack; blur and glare are as tagged by the data.

---

## Part 3. First business case

**Targets used.** The `PRODUCT.md` §6 targets (the brief's Table 7): straight-through ≥ 60%; reviewer minutes < 5 per application, "time on routed cases only, spread over all applications"; follow-up rounds per returned application = 1; time to decision < 10 minutes for straight-through cases. No drop-off target exists in either file; Part 3.4 says what that means.

**Scope.** The nine months Jan–Sep 2026 (3,000 applications). Annual figures multiply by 12/9, assuming flat volume (monthly starts range 314 to 384, `monthly_funnel`).

### 3.1 Reviewer hours and rupees

Rate: the 22 reviewers' `loaded_cost_inr_per_hour` takes four values (₹380, 420, 450, 480); the plain mean is **₹430.0** and the mean weighted by applications handled is ₹430.01. **MEASURED.** Effort per full review: the 600 test applications' `reviewer_minutes` summed over six documents: mean **20.7 min** (median 20.2). It is flat across outcomes (approve 20.7, needs info 20.9, reject 20.2), so the test set's mix does not bias it; the brief says 21. **MEASURED on the test set, ASSUMED to apply to all 2,742 reviewed files.**

| Line | Hours, 9 months | Hours/month | ₹ at 430/h | Status |
|---|---:|---:|---:|---|
| **Baseline A**: 2,742 first reviews × 20.7 min | 946 | 105 | ₹4.07 lakh | ESTIMATE |
| Baseline B: A + 638 re-checks at one document each (3.45 min each) | 983 | 109 | ₹4.23 lakh | ESTIMATE (re-check effort is an assumption) |
| Baseline C: every one of 3,380 review sessions a full 20.7 min | 1,167 | 130 | ₹5.02 lakh | ESTIMATE, upper bound |
| Sensitivity D: first reviews at the log's own 14.0 min (mean elapsed, `stage_events`) | 641 | 71 | ₹2.76 lakh | ESTIMATE, lower bound |
| **Saved at the straight-through floor** (60% need no reviewer; routed 40% still 20.7 min, i.e. 8.3 min per file) | **568** | 63 | **₹2.44 lakh** | ESTIMATE |
| **Saved at the minutes target** (< 5 min per file) | **718** | 80 | **₹3.09 lakh** | ESTIMATE |

Annual equivalents (× 12/9): floor 757 h (₹3.3 lakh), target 957 h (₹4.1 lakh). Under sensitivity D the savings fall to 385 h (floor) and 413 h (target). Per reviewed file the baseline is ₹148; spread over the 1,732 certified agents it is ₹235 (A) to ₹290 (C) each.

Things to read carefully:

- **The two targets pull against each other.** If 60% of files go straight through and the other 40% still take 20.7 minutes, the average is 8.3 minutes, above the 5-minute target. Meeting both needs routed cases to take **12.5 minutes or less** (5 ÷ 0.4), which is what the side-by-side evidence view must achieve. The saving range above is bracketed by the two.
- **₹14.7 lakh is not used.** The package's note multiplies all 9,920 `manual_touches` by a full 20.7-minute review. But `manual_touches` equals the number of reviewer events **plus one for every application plus one more for each of the 160 failed exams**: 6,760 reviewer events + 3,000 + 160 = 9,920. Even the 258 applicants who never uploaded a document (no reviewer at all) have 1 touch. The measure is not "reviewer actions", so the data supports ₹4.1–5.0 lakh, not ₹14.7 lakh. This is checked in `tables/_part3_numbers.json` (`touches_minus_reviewer_events` = 3,160).
- **This is capacity, not cash, unless reviewers are redeployed.** Baseline A is 105 hours a month across 22 reviewers: **4.8 hours each per month**. The team is clearly doing other work, or the minutes cover only document inspection. Saving 63–80 hours a month is about 0.4–0.5 of one full-time reviewer (assuming 160 hours a month). Savings in rupees only become real if the problem owner confirms which of the reviewers' time is released. This needs a question to InsuranceDekho (not answerable from the data).
- The product-side figure in `PRODUCT.md` (0.38 minutes per application, in-sample simulation) is not used here; it is more optimistic than the target and has not been run with reviewers.

### 3.2 Applicant waiting hours and time to certificate

| Line | Value | Status |
|---|---:|---|
| File-hours spent waiting in the queue and in review, today: 2,742 first passes | 56,681 h | MEASURED |
| Same, 638 re-check passes on 582 files | 11,423 h | MEASURED |
| Total, 3,380 passes (mean 20.1 h per pass) | **68,104 h** | MEASURED |
| If every pass takes 10 minutes (the time-to-decision target) | 563 h | ASSUMPTION |
| Saved if every pass meets it | 67,541 h | ESTIMATE, upper end |
| **Saved if only 60% of passes do (floor)** | **40,524 h** | ESTIMATE |

Time to certificate, replaying the 1,732 observed certified journeys (`tables/bc_days_to_certificate.csv`): the review zone is replaced by 10 minutes; for returned files the applicant's own reply time to the first return is kept and any later round disappears; everything else (upload, training, exam) is kept as observed.

| Scenario | Median | P90 | Status |
|---|---:|---:|---|
| Today | 8.41 days | 13.0 days | MEASURED |
| Product decides each pass in 10 minutes, one round | 7.40 days | 11.5 days | ESTIMATE |
| As above and the training link goes out at approval (gap to start capped at 1 hour) | 6.11 days | 10.3 days | ESTIMATE; the 1-hour cap is an ASSUMPTION |

That is **26.7 hours (mean) or 21.8 hours (median) earlier per certified agent**: 1,732 agents × 26.7 h ≈ 46,300 hours, about **1,930 agent-days earlier** in nine months (ESTIMATE). The package's own simulation (`eval/out/simulation.json`, 7.4 and 6.1 days) is reproduced by this independent re-implementation. The value of an agent-day is not in the data (3.5).

### 3.3 What the product cannot reduce

- The 314 rejections (10.5%) are ineligible people (underage, not an individual PAN, already registered, class 10 not passed, different person). The product must keep them out; it only tells them faster.
- The 258 applicants who never upload and the 482 who never start training are decisions the applicant takes outside the product's decision step.

### 3.4 Drop-offs: what the data does and does not support

Observed losses (MEASURED, `tables/process_map_loss_reasons.csv`): no upload 258; silence after a return 211 (27.3% of 774 returned); no training start 482 (21.7% of 2,217 approved).

Does speed explain them? **No, not in this data** (`tables/bc_dropoff_drivers.csv`):

| Cut | Rate by group |
|---|---|
| Silence after a return, by hours queued before the first review (quartiles) | 26.9%, 22.2%, 31.1%, 28.9% (no steady rise) |
| No training start, by hours from documents to approval (quartiles) | 23.6%, 19.5%, 23.5%, 20.4% (flat) |
| No training start, returned before approval vs not | 21.1% vs 21.9% |
| Silence by what was asked | name spelling 36.2% (130 returns), DOB 31.8% (110), poor image 25.7% (377), bank name 22.5% (102), face 16.4% (55) |
| Certified after one return / two returns | 57.5% of 703 / 53.7% of 67 (three returns: 4 of 4) |
| By channel | certification: Agent app 55.8%, Field referral 60.2%, Web 58.9%; never uploaded: 9.6%, 7.4%, 7.6% |

Reading: a faster decision, on its own, is not shown to reduce either loss. What does differ is the **content of the request** (spelling and DOB returns lose a third of applicants). Consolidating to one round matters little for drop-off: the 67 applications returned twice certified 3.8 points less often than those returned once, so removing the second return is worth about 3 agents (the 4 returned three times all certified).

So the drop-off savings below are **what-if arithmetic on assumed behaviour changes, not a forecast**. Rule used: recovered silent applicants certify at the rate of those who replied after a return (76.3% of 582); recovered non-starters certify at the rate of those who started training (99.8% of 1,735; marginal people may do worse). Nothing is assumed for the 258 who never upload, since the data gives no handle on them.

| Silence after a return falls by | No-training-start falls by | Silent applicants recovered | Non-starters recovered | **Extra certified agents** (9 months) | Certification rate would be |
|---|---|---:|---:|---:|---:|
| 25% | 0% | 53 | 0 | 40 | 59.1% |
| 25% | 25% | 53 | 120 | 161 | 63.1% |
| 25% | 50% | 53 | 241 | 281 | 67.1% |
| 50% | 0% | 106 | 0 | 80 | 60.4% |
| 50% | 25% | 106 | 120 | 201 | 64.4% |
| 50% | 50% | 106 | 241 | 321 | 68.4% |
| 63% (27.3% → 10%) | 0% | 134 | 0 | 102 | 61.1% |
| 63% | 25% | 134 | 120 | 222 | 65.1% |
| 63% | 50% | 134 | 241 | 343 | 69.2% |

The 10% silence row is the same assumption used in the app's E4 simulation (+106 there, +102 here). Both recover 134 applicants; E4 converts them at 78.9% (certified among the 563 returned applicants who were never silent), this pack at 76.3% (all 582 who replied at least once).

### 3.5 What cannot be sized from the data

- **The value of an extra certified agent, or of an agent-day earlier.** The data pack has no commission, premium or revenue per agent. The pack therefore does not give a rupee value for the drop-off or time-to-certificate gains. Arithmetic only: every ₹10,000 of value per extra agent turns the grid's 40 to 343 agents into ₹4 to ₹34 lakh. The reviewer-hours saving (₹2.4–3.1 lakh) is matched by the **smallest** drop-off scenario (40 agents) if one certified agent is worth about ₹6,100 to ₹7,700 or more. The product's case rests on that number, which is a question for InsuranceDekho.
- **Reviewer headcount and utilisation** (3.1), and the real effort of a re-check.
- **Any cost of the product itself** (OCR and model calls, build, run): not in the data; the brief says "a few rupees per application" for model cost, which this pack does not use.
- **How much of the drop-off the product can influence.** Part 3.4 shows no link to speed.

---

## 4. What `PRODUCT.md` §9 can now say

| §9 row | Now | Evidence |
|---|---|---|
| Stage 1: Process map from stage_events, time and drop-off per step | **Done** (replace "Not found") | Part 1, `tables/process_map_*.csv`; checked against the workbook (18 duplicate rows removed, 3,000 applications) |
| Stage 1: 20 test applications decided by hand, ≥ 8 hard | **Done, with one caveat**: written by Claude, to be adopted or overruled by a team member | Part 2: 20 cases, 10 hard, 20 of 20 agree, hash frozen before the key was opened |
| Stage 1: First business case: hours and drop-offs saved | **Done as a first version** (change "Partial"). Hours and ₹ are estimates from targets; drop-offs are what-if scenarios | Part 3 |
| Stage 1: Answers from the problem-owner meeting | **Unchanged: not done** | Part 3.5 lists the questions it should cover (value per agent, reviewer utilisation, cost of the product) |
| Stage 1: Which decisions the product makes / routes | Unchanged (Done) | |
| Stage 2 and 3 rows, executive presentation | Unchanged | |

Wording in `PRODUCT.md` that this pack suggests revisiting (not edited here):
- §1: "a reviewer asks for one fix at a time, and each round trip adds about two days" is right about the two days, but one-at-a-time is a small part of the rounds (75 extra rounds on 774 returned applications).
- §1 and §4.6 (E4): the drop-off what-if has no basis in speed; see 3.4.
- §6 reviewer-minutes row: the 60% straight-through floor and the 5-minute target are consistent only if a routed case takes 12.5 minutes or less.

## 5. Limits of this pack

- Part 1 and 3 use elapsed clock time, not working time, and the log's status snapshot is 30 Sep 2026.
- Reviewer effort comes from the test set (600 applications) and the log gives a smaller number (14.0 min); the truth is between them. No time-and-motion data exists.
- The 20 hand decisions are one author's reading; they are not an independent human check.
- Nothing here touches `PRODUCT.md`, the app, or the live site.

## 6. Files

| Path | What |
|---|---|
| `STAGE1_PACK.md` | This document |
| `tables/process_map_steps.csv` | Part 1 step table |
| `tables/process_map_loss_reasons.csv`, `process_map_return_and_reject_reasons.csv`, `process_map_returns_per_app.csv`, `_part1_checks.json` | Part 1 supporting counts and checks |
| `tables/part2_sample_ids.csv`, `part2_hand_decisions.csv`, `part2_hand_decisions.sha256`, `part2_comparison.csv` | Part 2: sample, frozen decisions, hash, comparison |
| `tables/bc_reviewer_hours.csv`, `bc_waiting_hours.csv`, `bc_days_to_certificate.csv`, `bc_returns_vs_outcome.csv`, `bc_dropoff_drivers.csv`, `bc_dropoff_whatif.csv`, `_part3_numbers.json` | Part 3 tables |
| `scripts/` | `xl.py`, `common.py` (read .xlsx with zipfile), `part1_process_map.py`, `part2_prepare.py`, `part2_sample.py`, `part2_view.py`, `part2_compare.py`, `part3_business_case.py` |

To re-run: `python scripts/part1_process_map.py`, then `part3_business_case.py` (they read `D:\PS-01_*.xlsx`; set `PS01_APPS` / `PS01_DOCS` to change the paths). Part 2 needs a scratch folder: `part2_prepare.py <folder>`, `part2_sample.py <folder>`, `part2_view.py <folder> APP-...`, and only after the decisions are written, `part2_compare.py <folder>`.
