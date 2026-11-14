# PolicyNest onboarding

The language of PolicyNest's AI-first onboarding of POSP insurance agents: who takes part, what an application goes through, how documents are judged, and how results are reported. Terms settled during the grilling of 14 Nov 2026 (`GRILL_LOG.md`); every definition is AI-proposed and needs human confirmation.

## People

**Applicant**:
A person applying to become a POSP through PolicyNest, usually on a phone.
_Avoid_: candidate, user, agent (until certified)

**POSP**:
Point of Sales Person: an IRDAI-recognised part-time seller of simple insurance products, certified after 15 hours of training and an exam.
_Avoid_: agent (unqualified), partner

**Reviewer**:
A member of PolicyNest's Onboarding Ops team who decides the cases the rulebook reserves for a person.
_Avoid_: ops user, checker, verifier

**Ops lead**:
The person who watches queue age, the decision mix, overrides and drop-off by stage.
_Avoid_: admin, manager

**Compliance officer**:
The person who samples decisions and reads the audit trail to confirm no ineligible person is certified.
_Avoid_: auditor

**Problem owner**:
InsuranceDekho's representative who set the challenge and answers the discovery questions.

## The application

**Application**:
One applicant's attempt to be certified, from the first visit to a certificate, rejection or drop-out.
_Avoid_: case (outside the review console), file, journey

**Typed details**:
The values the applicant enters in the form: name, date of birth, PAN, Aadhaar last four, contact, education, state, city, bank account and IFSC.
_Avoid_: declared data, form data

**Anchor document**:
The PAN card, whose read name and date of birth are the reference for every other check.
_Avoid_: master document, source of truth

**Document slot**:
One of the six places an applicant adds a document: PAN, Aadhaar front, Aadhaar back, Class 10 marksheet, bank document, selfie.
_Avoid_: upload field

**Type gate**:
The rule that a slot accepts only its own kind of document and refuses anything else with a reason.
_Avoid_: classifier check

**Instant feedback**:
What the applicant is told about one document straight after adding it: what was read, what is fine, what to fix and what goes to a person.
_Avoid_: AI observation (that is the label on the card), preview

**Sitting**:
One timed, focused session of up to 30 minutes for typed details and documents, which can be extended and resumed.
_Avoid_: session (ambiguous), exam mode, test

**Focus exit**:
The applicant leaving the onboarding screen during a sitting; counted, never timed, never used as evidence.
_Avoid_: violation, cheating, tab switch

**Saved progress**:
The minimised copy of an application kept on the applicant's own device, only with their consent, until it expires.
_Avoid_: draft, backup, account

**Expired**:
Saved progress older than the state machine's limit (30 days in DRAFT, 14 days once a follow-up is open), which is deleted.
_Avoid_: timed out, dropped (that is the state)

## Decisions

**Decision**:
The application-level outcome: APPROVE, NEEDS_MORE_INFO or REJECT, with every reason and the rule each one applies.
_Avoid_: verdict, result, status

**Check**:
One rule applied to one or more documents, ending in a check result.
_Avoid_: test, validation

**Check result**:
The outcome of one check: pass, information only, needs information, re-upload, reject, a person decides, or waiting for a document.
_Avoid_: flag, status

**Reason code**:
The rulebook's name for why a check did not pass, such as NAME_SPELLING_VARIANT or PAN_NOT_INDIVIDUAL.
_Avoid_: error code, defect

**Name tier**:
Where a name comparison falls in the rulebook's name rules, from an exact match through spelling variant, surname change and different person.
_Avoid_: match score

**Human-only decision**:
A decision the rulebook reserves for a person: a different person's name, a face-match score from 0.60 to 0.75, an unlisted board, a surname change, and any disputed case.
_Avoid_: manual review, exception

**Routed case**:
An application sent to a reviewer because it contains a human-only decision or two selfie failures in a row.
_Avoid_: escalation, referral (that is the fraud-desk step)

**Selfie failure**:
A face-match score below 0.60; two in a row route the case to a reviewer.
_Avoid_: face fail, biometric failure

**Fraud-desk referral**:
An internal note that a case goes to the fraud desk; never shown or worded to the applicant.
_Avoid_: fraud flag (in anything an applicant can see)

**Dispute**:
An applicant's request that a person look again at a rejection; always a routed case.
_Avoid_: appeal, complaint

**Follow-up**:
The one message that lists every fix a NEEDS_MORE_INFO application needs, in English or Hindi.
_Avoid_: rework request, query, return

**Round**:
One pass of checks on an application; the first submission is round 1 and each set of fixes starts the next round.
_Avoid_: iteration, attempt

**Re-check**:
A later round that re-reads only the changed documents and re-runs only the checks that involve them.
_Avoid_: re-review, re-run

**Carried over**:
A check result kept from an earlier round because none of its documents changed.
_Avoid_: cached, skipped

**Simulated check**:
A check whose external result (PAN service, penny-drop name, face match, IRDAI registry) comes from fixed or data-pack values and is labelled as simulated.
_Avoid_: mock, fake

## Evidence and reporting

**Engine**:
The rule logic that turns read documents and typed details into checks and a decision.
_Avoid_: AI, model, policy engine (when the LLM is meant)

**Copilot**:
The assistant beside the applicant that suggests next steps and answers questions from the rulebook and the applicant's progress; it never decides.
_Avoid_: chatbot, AI agent

**Nudge**:
A suggestion the Copilot offers without being asked, shown as a badge, never by opening itself.
_Avoid_: notification, pop-up

**Passage**:
A section of the rulebook or a reference document that the Copilot may quote, tagged for applicants or for internal use.
_Avoid_: chunk (outside the build), snippet

**Internal event**:
An audit event meant for reviewers and compliance only, such as a fraud-desk referral.
_Avoid_: private log

**Audit trail**:
The ordered record of every action and decision with its rule, round and engine version.
_Avoid_: log, history

**Specimen**:
A synthetic document built for testing, marked as specimen, never a real person's document.
_Avoid_: sample, dummy, test document

**Specimen variant**:
A specimen with one deliberate defect, used to trigger a test scenario.
_Avoid_: test case

**Demo controls**:
The collapsed set of specimen and sample-applicant controls that lets anyone run the scenarios without real documents.
_Avoid_: debug panel, test harness (in anything an applicant can see)

**Test set**:
The data pack's 600 labelled applications.
_Avoid_: benchmark, dataset (unqualified)

**Held-out set**:
Applications labelled by the user and frozen before the engine sees them, used to measure accuracy out of sample.
_Avoid_: validation set, test set

**Constructed case**:
An application made by the team to cover a situation the test set lacks, always labelled as constructed.
_Avoid_: synthetic case (all data is synthetic), fake case

**In-sample**:
Measured on the same applications that the rules were refined on.
_Avoid_: accuracy (unqualified)

**Straight-through**:
An application handled from start to finish with no human touch, whatever its decision.
_Avoid_: auto-approved, STP rate (when only approvals are meant)

**Approved first time**:
An application approved in round 1 with no follow-up and no human touch.
_Avoid_: straight-through

**Time to decision**:
The time from the last required document being accepted to the decision existing.
_Avoid_: processing time, turnaround
