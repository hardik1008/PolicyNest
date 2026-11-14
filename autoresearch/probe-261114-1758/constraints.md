# Constraint registry: PS-01 AI-first onboarding

46 atomic constraints from 9 probe rounds (autonomous mode). Confidence is high where a file states it, medium where I derived it from the data or assumed something, as marked in the evidence.

## Decision logic

- **C01** (high, round 1, Domain Expert): Application decision precedence is REJECT over NEEDS_MORE_INFO over APPROVE, and every reason is listed, not only the first.
  - Evidence: Rulebook §6. Test-set truth carries 0/1/2/3 reasons on 342/195/56/7 applications.
- **C02** (high, round 1, Domain Expert): Informational findings (address state differs, PAN 5th character unusual) are recorded and never change the decision on their own.
  - Evidence: Rulebook §4.3, §6; Specimen 12 is APPROVE with ADDRESS_STATE_MISMATCH; 37 truth rows carry it.
- **C17** (medium, round 2, Edge-Case Hunter): A poor-quality document can sit beside a hard reject reason, so the applicant must get the rejection, not a re-upload request: 11 of the 60 truth REJECTs also list POOR_QUALITY.
  - Evidence: Truth reasons such as "ALREADY_REGISTERED; POOR_QUALITY"; Specimen 9 (EDU_NOT_ELIGIBLE; POOR_QUALITY).
- **C18** (high, round 2, Edge-Case Hunter): Education decisions come from the marksheet result, not the typed education: all 13 applicants who typed Class 8 are REJECT, and 13 who typed Class 10 are REJECT too (marksheet FAIL).
  - Evidence: education_x_decision in truth; Specimens 9 and 11.
- **C41** (high, round 5, Edge-Case Hunter): The workbook keeps one rejection_reason per rejected application, and it equals the first reason listed in truth for 60 of 60 REJECT cases; the order of the listed reasons therefore carries meaning.
  - Evidence: applications.rejection_reason vs application_truth.decision_reasons.

## Anchor

- **C03** (high, round 1, Domain Expert): The PAN is the anchor: its name and DOB are the reference for every other check; the typed PAN must equal the card, and a one-character difference is corrected from the card and logged.
  - Evidence: Rulebook §3, §4.2.

## Name matching

- **C04** (high, round 1, Domain Expert): Names: exact, initials, swapped order, middle missing and middle added all match; spelling variant is NEEDS_INFO; surname change is NEEDS_INFO and Human only; a different person is REJECT confirmed by a human.
  - Evidence: Rulebook §5. Test-set categories: EXACT 436, SWAP 36, SPELLING 36, MIDDLE_MISSING 29, INITIAL 28, MIDDLE_ADDED 23, DIFFERENT 12.
- **C05** (medium, round 1, Domain Expert): Name rules must also run on the penny-drop name, which is often abbreviated by the bank (for example P BISWAS for PAYEL BISWAS).
  - Evidence: Penny-drop name equals the full declared name (case-insensitive) on only 275 of 600 applications.
- **C30** (high, round 4, Contradiction Finder): Brief T4 says the Aadhaar and the marksheet carry a different person's name, but Specimen 6 (NAME_MISMATCH_HARD) has a different name on the marksheet only, with the Aadhaar exact. A different person on any one document must trigger it.
  - Evidence: Brief Table 6 vs specimen document.
- **C38** (high, round 5, Domain Expert): Name differences are not the main driver of non-approval: 151 of 436 EXACT applications are NEEDS_MORE_INFO or REJECT for other reasons. Of the 164 non-exact applications 79 are APPROVE, so a blunt "any difference, ask" rule would wrongly return 79.
  - Evidence: name_match_category x final_decision.
- **C39** (medium, round 5, Skeptic): A spelling variant can look like OCR noise: in Specimen 5 PAN reads THAKKAR while the Aadhaar and marksheet read THAKKARR, and the truth is NAME_SPELLING. Where the evidence is ambiguous, prefer NEEDS_INFO as the rulebook says.
  - Evidence: Specimen 5; rulebook §5 closing rule.

## Follow-up message

- **C06** (high, round 1, End User): One consolidated message says exactly what is wrong, what to send and how; English or Hindi; never mentions fraud, never shows another person's data, never includes a full PAN or Aadhaar.
  - Evidence: Rulebook §8; brief §8.
- **C07** (high, round 1, End User): The first follow-up must be complete, because applicants who are returned are fragile: 774 were returned, 192 never re-uploaded (all dropped) and 211 dropped before KYC.
  - Evidence: stage_events DOC_RETURNED/DOC_REUPLOADED joined to applications.status.

## Rejection message

- **C08** (medium, round 1, End User): A rejection message is plain language and gives a way forward where one exists (underage: date to reapply; ALREADY_REGISTERED: reapply after a no-objection certificate); a disputed case goes to a human.
  - Evidence: Rulebook §2, §8, §9.

## Evaluation

- **C09** (high, round 2, Skeptic): Judge the engine against application_truth.final_decision, never against document-level human_verdict (about 2.5% are deliberately wrong).
  - Evidence: Brief §5; test-set README.
- **C10** (medium, round 2, Skeptic): A reviewer-only baseline at application level is not the 97.5% in the brief: rolling the 3,600 document verdicts up by the §6 rule matches truth on 522 of 600 (87.0%), and 9 true REJECTs roll up to APPROVE.
  - Evidence: My roll-up of documents.human_verdict (REJECT > NEEDS_INFO/REUPLOAD > ACCEPT); the brief's 97.5% is document-level, so compare like with like.
- **C11** (medium, round 2, Skeptic): Accuracy from rules tuned on the 600 test applications is in-sample; report it as such and hold some applications out or use the wider applications workbook.
  - Evidence: CLAUDE.md records 98.0% rising to 100.0% after three rulebook-based refinements.

## Eligibility

- **C12** (high, round 2, Edge-Case Hunter): Age is measured on the application start date, not today. The test set has no start date, but all 600 join to the applications workbook with identical declared fields, so created_at is available.
  - Evidence: 600/600 name, DOB, PAN, education, state equal across workbooks; 51/600 were under 18 on some day in Jan to Sep, 6 are UNDERAGE in truth and all 6 were under 18 at created_at.

## Document reading

- **C13** (high, round 2, Edge-Case Hunter): O/0 and I/l noise must be tolerated, but a genuinely malformed PAN must still be rejected: 6 OK-quality PANs fail the format (4 are nine characters, 2 have a letter in a digit position), all are REJECT, and in all 6 the typed PAN equals the card.
  - Evidence: Test-set documents; Specimen 10 (OUKPC227OR). Rulebook §4.2 equality rule and README noise note.
- **C14** (high, round 2, Edge-Case Hunter): An OCR-confidence gate of 0.75 is not a clean quality test: all 3,490 OK documents score 0.815 or more, but 5 of 110 bad-quality documents also score 0.75 or more (maximum 0.80), and reviewers accepted 4 of the 110.
  - Evidence: documents.image_quality vs ocr_confidence vs human_verdict. Rulebook §4.1.

## Face match

- **C15** (high, round 2, Edge-Case Hunter): The test set has 22 selfies below 0.60 and none between 0.60 and 0.75, so the Human-only face band cannot be evaluated on it and needs constructed cases (T8).
  - Evidence: documents.face_match_score: 22 below 0.60, 0 in 0.60 to 0.75, 578 at 0.75 or more.

## Human-only rules

- **C16** (high, round 2, Edge-Case Hunter): The test set has no surname-change category and no unlisted board, so those two Human-only rules cannot be evaluated on it either. The 45 board spellings in the OCR text (O/0 and I/l noise) collapse to 15 real boards (13 state boards, CBSE and NIOS); the rulebook gives no recognised list to compare against.
  - Evidence: name_match_category has no surname-change value; board lines parsed from 3,490 OK marksheets.

## Targets

- **C19** (high, round 3, Ops Engineer): CORRECTED: straight-through means no human touch (brief glossary), so automatic follow-ups and rejections count as well as approvals. The stricter "approved first time, no follow-up" share is 364 of 600 (60.7%) in truth; the 60% target is not capped by it.
  - Evidence: application_truth.final_decision counts; brief Table 7.
- **C20** (medium, round 3, Ops Engineer): Reviewer minutes are flat across outcomes (APPROVE 20.7, NEEDS_MORE_INFO 20.9, REJECT 20.2; mean 20.7 per application), so savings come from skipping the read, not from simpler cases. An average under 5 minutes allows about 40% routed at 12 minutes each.
  - Evidence: documents.reviewer_minutes summed per application; the 12-minute routed cost is my assumption.

## Cost

- **C21** (high, round 3, Ops Engineer): Today's process: 9,920 human touches (3.31 per application) by 22 reviewers costing 380 to 480 rupees per hour, speed index 0.82 to 1.32.
  - Evidence: applications.manual_touches; ops_team.

## Speed

- **C22** (high, round 3, Ops Engineer): Median 17.9 hours from start to documents, 23.9 hours from documents to KYC, 23.3 hours from KYC to training start; 8.4 days to certificate (p90 13.0, best quartile 6.6). The rulebook SLA for first review is 4 working hours.
  - Evidence: applications timestamps; rulebook §7.

## Drop-off

- **C23** (high, round 3, Ops Engineer): 482 applicants cleared KYC and never started training (21.7% of 2,217). This is outside the document engine and needs a nudge or a link at KYC.
  - Evidence: applications.status DROPPED with kyc_verified_at and no training_started_at.

## Training data

- **C24** (high, round 3, Ops Engineer): The 15-hour rule cannot be verified from timestamps: 66 of 1,735 completions took under 15 hours of wall-clock time (shortest about 2 hours). A training platform log is needed. All 160 exam failures read "Score below 40%".
  - Evidence: training_started_at to training_completed_at; stage_events EXAM_FAILED notes.

## Privacy

- **C25** (high, round 3, Security Reviewer): Never store, log or send a full Aadhaar number; only the last four digits. The data is already masked (XXXX XXXX 9744).
  - Evidence: Brief §8; rulebook §3, §4.3.
- **C26** (high, round 3, Security Reviewer): Follow the Digital Personal Data Protection Act 2023: collect only what onboarding needs, state the purpose, use no real people's documents.
  - Evidence: Brief §8.

## Fraud handling

- **C27** (high, round 3, Security Reviewer): Fraud desk referrals (a different person, or two face-match failures in a row) are internal, same day, to the compliance officer; the applicant is never told.
  - Evidence: Rulebook §4.6, §7, §8.

## Duplicates

- **C28** (medium, round 3, Security Reviewer): 35 PANs appear in more than one application in the 3,000. Duplicate or repeat-applicant detection is not in the rulebook but is possible with this data.
  - Evidence: applications.pan_declared counts; not checked whether the repeats are the same person.

## Vocabulary

- **C29** (high, round 4, Contradiction Finder): The reason vocabulary differs between sheets. Truth uses FACE_LOW, POOR_QUALITY, NAME_SPELLING, NAME_MISMATCH_HARD and "ADDRESS_STATE_MISMATCH (INFORMATIONAL ONLY)" (5 labels, none in reason_codes); reason_codes defines 7 codes that never appear in truth. The engine needs a mapping layer and should be scored on the truth vocabulary.
  - Evidence: reason_codes sheet (14 codes) vs decision_reasons in application_truth.

## Bank

- **C31** (medium, round 4, Contradiction Finder): Cheque name and penny-drop name disagree in all 31 BANK_NAME_MISMATCH cases (Specimen 8: PALLAVI BHATT vs MOUMITA MISHRA), which is impossible for one real account. Treat it as a synthetic artifact: apply the rule to the penny-drop name and flag any disagreement.
  - Evidence: 31 of 31 mismatch cases; elsewhere only 30 of 577 OK cheques differ from the penny-drop name.
- **C46** (medium, round 8, Edge-Case Hunter): Joint accounts are accepted when the applicant is first holder, but the penny-drop returns one name string and there is no first-holder field, so a joint-account case should go to NEEDS_INFO or a human.
  - Evidence: Rulebook §4.5; test-set columns.

## Human routing

- **C32** (high, round 4, Contradiction Finder): Rulebook §6 says any REJECT reason makes the application REJECT, while §9 and the brief say NAME_MISMATCH is only recommended and a person confirms. The system output is "recommend REJECT, route to human", and scoring must count that as correct (Table 7: "rejects or routes to a human").
  - Evidence: Rulebook §6 and §9; brief §8 and Table 7.

## Metrics

- **C33** (high, round 4, Contradiction Finder): "27% never reply" has several definitions in the data: 192 returned applicants never re-uploaded (24.8%), 211 dropped before KYC (27.3%), and 330 of 774 returned applicants eventually dropped (42.6%). The before/after baseline must name one.
  - Evidence: stage_events and applications.status.

## Scope

- **C34** (medium, round 4, Scope Guardian): Out of scope per the brief: the training course, the exam, real e-KYC, penny-drop or registry calls, and fraud investigation beyond flagging. Our demo exam (pass mark 50%) contradicts the data (fail below 40%); treat it as a placeholder.
  - Evidence: Brief §3; PolicyNest.html exam text vs EXAM_FAILED notes.
- **C35** (high, round 4, Scope Guardian): Should-haves are re-check of a re-upload only, a reviewer dashboard with a queue, an audit trail with the rule and model version, and the simulation. WhatsApp, DigiLocker and a second journey are stretch and stay out until the must-haves are evaluated.
  - Evidence: Brief §3.
- **C36** (high, round 4, Scope Guardian): Optional documents (GST certificate, address proof) have no reason codes and no data; do not build checks for them.
  - Evidence: Rulebook §3; no rows in documents.
- **C37** (medium, round 4, Scope Guardian): Rulebook §7 service levels (4 working hours first review, 2 after re-upload, same-day fraud desk) only mean something with a queue; a one-case review console cannot meet or miss them.
  - Evidence: Rulebook §7; CLAUDE.md says the console holds one application.

## Fairness

- **C40** (medium, round 5, Skeptic): Female applicants are 29.5% of the 600 (177). Truth shows F 67.8% APPROVE / 6.8% REJECT against M 57.7% / 11.3%; these are differences in the labels themselves, so fairness must compare error rates (false approve, false reject) per group, not decision rates, and the groups are small (12 DIFFERENT cases overall).
  - Evidence: application_truth joined to applications.gender.

## Measurement

- **C42** (high, round 6, End User): The applicant-clarity target (4 of 5 from five real users) and real reviewer minutes cannot be produced from these files; they stay "not yet measured".
  - Evidence: Brief Table 7; no usability data in the pack.

## Rulebook gaps

- **C43** (high, round 6, Contradiction Finder): The rulebook is silent on: the recognised-board list (needed for a Human-only rule), the exam pass mark, the no-objection-certificate re-apply flow, how to verify "applicant is first holder" on a joint account, and how to detect a photocopy or photo of a screen.
  - Evidence: Rulebook §2, §4.1, §4.4, §4.5, §9.

## Channel

- **C44** (medium, round 6, End User): Clean-file rate differs by channel in the test set (Agent app 172/295 = 58.3%, Field referral 134/201 = 66.7%, Web 55/100 = 55.0%); informational, with small samples.
  - Evidence: application_truth joined to applications.channel.

## Audit

- **C45** (high, round 7, Ops Engineer): Every decision needs an audit record with the rule cited, the model version and both rounds of a re-check (T10), readable by a compliance officer.
  - Evidence: Brief §3 Should have, §9 Stage 3, T10.

