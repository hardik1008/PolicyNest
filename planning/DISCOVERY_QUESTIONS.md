# PolicyNest discovery questions for the problem owner

Written 15 Nov 2026. Covers FR-69 (RF-67, RF-80, G-43, Q13).

**Status of every question: Not asked.** No discovery meeting took place (user decision, Q13). Nothing below is an answer. Each "today's assumption" is what the product assumes now, so the team can see what a meeting would have to confirm or change.

## Count check

The brief's section 10 has **nine** questions, not ten. Checked 15 Nov 2026 against `01_ORIGINAL_CHALLENGE/PS-01_CHALLENGE_BRIEF.md` (lines 189 to 209). The nine are copied below word for word. FR-69 asks for 14 questions; this file has 13 (nine from the brief, four added). No tenth question was invented. If the problem owner or the user wants a tenth, add it in the table and change FR-69 to match.

## Questions

Sources for "today's assumption" are named in each row. Figures come only from those files.

### The brief's questions (section 10)

| # | Question (brief wording) | Status | Today's assumption | Source |
|---|---|---|---|---|
| 1 | Which onboarding journey costs InsuranceDekho the most today — agents, customers or partners — and why? | Not asked | Agents. The primary user is the new POSP agent on a phone. The cost is the wait: a certified agent takes a median of 8.4 days, a file waits 17.3 hours before a reviewer opens it, and 25.8% of files are returned at least once. The product assumes the waiting and the one-at-a-time follow-ups cause this, not the steps themselves. Customer and partner journeys are not modelled. | PRODUCT.md §1 |
| 2 | Where do your reviewers disagree with each other most often, and how is that resolved? | Not asked | No disagreement data exists. The product has no rule for two reviewers who disagree. It records one reviewer decision per case. The brief says about 2.5% of reviewer verdicts are deliberately wrong, so the engine is judged on `application_truth.final_decision`, not on reviewer verdicts. | CLAUDE.md "Reviewer routing"; brief §5 |
| 3 | What error rate would compliance accept for an automated approval, and who would sign it off? | Not asked | Targets: decision accuracy at least 95%, REJECT recall at least 98%, zero wrongful approvals. Measured: 100% accuracy, 100% REJECT recall, 0 wrongful approvals, all in-sample on the same 600 applications. No one has been named to sign off. A fresh held-out set has not been run. | PRODUCT.md §6, §8 item 4; eval/EVALUATION_REPORT.md |
| 4 | Which external checks (DigiLocker, penny-drop, registry lookups) do you already use, and what do they cost per call? | Not asked | None are called. PAN, penny-drop, face match and the IRDAI registry are simulated. No API keys are used. DigiLocker is not used. No cost per call is known or assumed. The four simulated checks must stay simulated until a vendor is chosen. | PRODUCT.md §2; RF-70; CLAUDE.md "No API keys" |
| 5 | At which step do you lose the most applicants, and what do you believe causes it? | Not asked | The loss is after a fix request. 25.8% of files are returned, and 27% of those applicants never reply. The simulation puts silence at 27.3% (211 of 774 returned applications). The product assumes the cause is waiting and one-at-a-time follow-ups, not the steps. Applicants have not been tested on this. | PRODUCT.md §1; eval/out/simulation.json |
| 6 | Would applicants trust a decision made by an AI, and should they be told? | Not asked | A person confirms every name-mismatch rejection and every Human-only decision. Applicant messages never mention fraud or show another person's data. No wording tells applicants that software made the decision. The usability debrief asks this question. | PRODUCT.md §7; USABILITY_TEST_PLAN.md §6 |
| 7 | What does a reviewer's day look like, and what would they want an AI to take off them first? | Not asked | Today a reviewer spends about 21 minutes per file (simulation mean 20.7 minutes per application). The product assumes the AI takes all routine checks and leaves reviewers only judgement calls, about 1.83% of applications in the simulation. What reviewers want first is not known. | PRODUCT.md §1; eval/out/simulation.json |
| 8 | How would you measure success for a pilot in one region? | Not asked | The product's own targets: decision accuracy at least 95%, REJECT recall at least 98%, zero wrongful approvals, straight-through at least 60%, reviewer minutes under 5, applicant clarity at least 4 out of 5, and median days to certificate (baseline 8.4). No region is chosen. Applicant clarity is not measured yet. | PRODUCT.md §6 |
| 9 | What would stop you from putting a product like this into production? | Not asked | The product's own gaps: real phone-photo OCR is not tested (D6); no held-out labelled set; applicant and reviewer usability sessions not run; the multi-case reviewer queue not built; external checks simulated; DPDP Act rules (collect only what is needed, no full Aadhaar number) apply. | PRODUCT.md §7, §8 |

### Added questions

| # | Question | Status | Today's assumption | Source |
|---|---|---|---|---|
| 10 | What exam pass mark should apply? | Not asked | 50%, a demo rule from the state machine. The rulebook gives no pass mark. The data dictionary and regulatory matrix ("e.g. 50%") say 50%, but the data pack's exam-failure events say "Score below 40%". The app shows 50% and is labelled as a demo rule. | PRODUCT.md A7; GRILL_LOG.md G-01 |
| 11 | Which Class 10 boards are recognised? | Not asked | Rulebook §4.4 says: "any state board, CBSE, CISCE or NIOS". The app also accepts any board whose name contains "ICSE", which the rulebook does not name. A board off the list goes to a person. The test set has no unlisted-board case. | RF-67; rulebook §4.4 (line 89); policynest_mvp/PolicyNest.html (BOARD_NATIONAL); PRODUCT.md R2, §6 |
| 12 | What is one certified agent worth to InsuranceDekho? | Not asked | No value figure is in the product, and none is assumed. The only agent figure is a simulation: about 106 more agents would certify if silence after a fix request fell from 27.3% to 10%. Only a pilot can show whether that is true. | eval/out/simulation.json; eval/EVALUATION_REPORT.md |
| 13 | How much reviewer time would really be released? | Not asked | 0.38 minutes per application. This is a simulated estimate, not measured with reviewers. Today's mean is 20.7 minutes per application (the product text says about 21). The 0.38 figure assumes 1.83% of applications go to a person. Real reviewer minutes are not measured until the reviewer sessions run. | PRODUCT.md §6; eval/out/simulation.json; USABILITY_TEST_PLAN.md §5 |

## How to use this file

1. Take the table to the problem owner. Ask each "Not asked" question in plain words.
2. When an answer comes back, change the status to "Answered", write the answer and the date, and name the source.
3. If the answer changes a product figure, update PRODUCT.md and CLAUDE.md, not this file.
4. Do not mark a question answered from the assumption column. The assumption is the product's position, not the owner's.
