# PolicyNest usability test plan

Status: **plan only. No sessions have been run, and no result below is a measurement.** Written 14 Nov 2026 with the `usability-test-plan` skill, for PRODUCT.md §8 priority 1 and brief Stage 3 (five people playing applicants, two playing reviewers).

Product under test: https://policynest.embarko.app (the live site, exam pass mark 40%).

## 1. Objectives and research questions

The brief needs two numbers it cannot get from data: **applicant clarity (target ≥ 4 / 5)** and **reviewer minutes per application (target < 5)**. The study answers five questions:

1. **Journey.** Can a new applicant with no help get from "Your details" to a certificate on a phone, and where do they hesitate?
2. **Clarity of the one follow-up message.** After a defect (T5 blurry marksheet plus a parent's cheque, T3 spelling variant), do applicants know exactly what to send, and do they rate the message ≥ 4 / 5, in English and in Hindi?
3. **Clarity of a rejection.** After T6 (company PAN), do applicants understand why, in plain words, and do they know a dispute is possible?
4. **Re-upload.** After a follow-up, can they fix everything once and see that only the changed documents were re-checked (T10)?
5. **Reviewer speed and confidence.** Can a reviewer decide T4 (different person), T8 (face match 0.68) and a disputed rejection from the side-by-side evidence in under 5 minutes each, and reach the expected decision?

## 2. Method

- **Moderated, think-aloud**, one participant at a time, about 45 minutes per applicant and 30 minutes per reviewer. Remote screen share is fine; in person is better for the phone.
- **Applicants use their own phone** (Android or iPhone, mobile data, not Wi-Fi if possible) so camera, keyboard and signal are realistic.
- **Reviewers use a laptop**, since the console is a desk tool.
- **Participants play roles.** They are not real applicants, so the results are directional evidence, not a forecast. Say so in the report.
- **No real people's documents, ever** (brief §8). Two routes, both synthetic:
  - the app's **"Use specimen"** path, which builds document text from typed details and skips the camera;
  - a **synthetic image pack** (a made-up person's six documents, with a blurry marksheet and a parent's cheque variant), shown on a screen or printed and photographed. This exercises the real upload slots and the OCR on phone photos, which also feeds PRODUCT.md gap D6. **The pack does not exist yet** (see §9).

## 3. Participants

| Group | n | Who | Screening |
|---|---|---|---|
| Applicants | 5 | People like the brief's agents: a shopkeeper, a mechanic, a homemaker, and similar | Uses a smartphone daily and WhatsApp; **not** an insurance, KYC or software professional; has not seen PolicyNest; at least **2 prefer Hindi** for messages; ages spread across 20 to 55 |
| Reviewers | 2 | Anyone with back-office, KYC, compliance or operations experience | Has checked documents for a living or in a past job; has not seen the console |

- **Recruitment:** friends and family of the team, plus one or two referrals. Do not recruit people who helped build or review the product.
- **Sample size:** the brief sets 5 and 2. Five applicants is enough to surface the biggest problems and a rough clarity average. **Two reviewers is too few for any statistic**: report their timings and quotes as case evidence only, never as an average.
- **Incentive:** a small thank-you; do not tie it to finishing tasks.

## 4. Tasks

Each task is read aloud as a scenario. The moderator does not name buttons.

### Applicant tasks (phone)

| # | Scenario read to the participant | Variant to set | Success criterion | Target time |
|---|---|---|---|---|
| A1 | "You want to become an insurance agent. Open the link and enter your details." | Pre-filled sample details | Details saved without help; consent noticed | 3 min |
| A2 | "Upload your documents. Here are the six papers of your character *Rahul*." | Image pack (clean) or "Use specimen" | All six slots verified; each file in the correct slot | 5 min |
| A3 | "Finish everything until you are certified." (T1) | Clean | Reaches the certificate unaided, including training and exam | 6 min |
| A4 | "The company has sent you a message. Read it and tell me what you need to do." (T5, then T10) | PAN clean; marksheet **Blurry, DOB unreadable · T5**; bank **Parent's account · T5** | Says both fixes unprompted; fixes both in one go; sees the result after re-upload | 7 min |
| A5 | "Your name is spelt differently on two papers. What does the message ask?" (T3) | Marksheet **Spelling variant · T3** | States "send a corrected document or a signed declaration" | 4 min |
| A6 | "The company says you cannot register. Why, and what can you do?" (T6) | PAN **Company PAN · T6** | Explains the reason in own words; finds the Dispute option | 4 min |

Order: A1 to A3 first (clean flow), then A4 to A6 in a **rotated order** across participants so no single message is always read last. For participants who prefer Hindi, repeat the A4 message in Hindi with the English / Hindi switch and ask for a second rating.

**Optional stretch task (A2b):** photograph a printed synthetic card with the phone camera and upload it. Record whether OCR accepts it and how long the participant takes. This is the only way this study produces real phone-photo evidence.

### Reviewer tasks (laptop)

The console holds one application at a time. Before each task the moderator sets up the case by running the applicant path with the variant, then hands over at **"Open review console"**.

| # | Scenario | Variant | Success criterion | Target time |
|---|---|---|---|---|
| R1 | "A case has been routed to you. Decide it." | Aadhaar **Different person · T4** | Recommends reject, writes a note, understands it goes to a person to confirm | < 5 min |
| R2 | "Another case: the selfie looks borderline." | Selfie **Borderline score 0.68 · T8** | Compares the photos and chooses an outcome with a reason | < 5 min |
| R3 | "An applicant disputes their rejection." | PAN **Company PAN · T6**, then press Dispute | Chooses Uphold, Ask or Overturn and can say why | < 5 min |

**Timing caveat:** reviewer sessions are best run **after the console redesign (PRODUCT.md R7)**, so the test is of the design that ships. If you run them before, treat them as a baseline for the current console and plan a re-test.

## 5. Metrics

| Metric | How | Pass line | Source of the line |
|---|---|---|---|
| **Clarity score** | Participant rates each follow-up and rejection message "How clear was what you had to do?" 1 to 5 | Mean ≥ 4.0 | Brief Table 7 |
| **Comprehension check** | Participant states the fix(es) in their own words; scored right / partly / wrong | ≥ 4 of 5 right on A4 | Proposed |
| Task success | Done unaided / done with a hint / failed, per task | ≥ 4 of 5 unaided on A3 | Proposed |
| Time on task | Stopwatch from scenario end to participant's "done" | Within the target times above | Proposed |
| Errors | Counted: wrong slot, refused file, misread message, wrong button, backtrack | Reported, no line | n/a |
| **Ease score (SEQ)** | After each task, "How easy was this?" 1 to 7 | Reported per task | Standard |
| **SUS** | 10-item System Usability Scale after the last task | Reported; with n = 5 use as a rough signal only | Standard |
| **Reviewer minutes** | Stopwatch per case, R1 to R3 | < 5 min per case | Brief Table 7 |
| Reviewer decision | Matches the expected decision? Confidence 1 to 5 | Reported | n/a |

Lines marked "Proposed" are my suggestions, not from the brief; change them freely. Never report a pass line you did not measure.

## 6. Facilitation guide

**Introduction (3 min)** (read aloud):
"Thank you for helping. We are testing a website for becoming an insurance agent, not you, so nothing you do is wrong. Please think aloud: say what you are looking at and what you expect. I will not be able to help during the tasks, but I will note where things are unclear. You can stop at any time. All documents here are made up, and please do not use any real papers. With your permission I will record the screen, not your face. Your name is not written anywhere; you will be P1 to P5."

**Consent (DPDP Act 2023: purpose, minimal data):** collect only a participant ID, age band, occupation, language preference, and device. State the purpose (improving the product and reporting usability results) and that notes are anonymous. Get a yes before recording. Delete recordings after analysis.

**Task delivery:** read the scenario once, hand over, start the timer when the participant begins and stop at their "done". Do not name buttons or screens.

**Probes (neutral, use sparingly):**
- "What are you thinking right now?"
- "What do you expect to happen next?"
- After a message: "In your own words, what do you need to do?"
- "Was anything in that message confusing or unfamiliar?"
- If silent for more than 20 seconds: "What are you looking for?"

**Hint ladder** (record the level used): 1 repeat the scenario, 2 "what would you try?", 3 point to the area, 4 do it for them (task failed).

**Debrief (5 min):** SUS and any remaining ratings; "What was the best part?"; "What was the most confusing part?"; "Would you trust a decision made like this? Should you be told it was made by software?" (problem-owner question 6 in the brief); "Would you use this to become an agent?"

## 7. Data collection

- **Record:** screen (with consent), the timer, and the ratings sheet. For reviewers also record the evidence panel they looked at first.
- **Observation sheet**, one row per event, kept in a shared sheet:

| Participant | Task | Time (mm:ss) | Hint level | Observation | Quote | Severity | Screen / element |
|---|---|---|---|---|---|---|---|

- **Severity scale:** 0 not a problem, 1 cosmetic, 2 minor (slows the person), 3 major (they stall or fail), 4 blocker (cannot finish).
- **Note-taking rule:** write what happened and what they said, in separate columns. Keep interpretation for the analysis.
- **Ratings sheet:** per participant and task: success, time, errors, SEQ, clarity (and language), comprehension; plus SUS at the end.
- **Moderator vs notetaker:** use two people if you can, so the moderator keeps eye contact.

## 8. Analysis plan

1. Fill the per-participant results table. Compute the **clarity mean** with each message listed separately (A4 English, A4 Hindi, A5, A6), plus success counts and median times.
2. Cluster observations by screen and element, then rank by **severity × how many participants hit it**.
3. For each problem, name the PRODUCT.md goal it touches (for example A4 to F1 and F2, A6 to C6) and propose one concrete change.
4. Report separately: applicants (n = 5, with numbers) and reviewers (n = 2, as cases, no averages).
5. **Update PRODUCT.md §6** (applicant clarity and reviewer minutes rows) with the measured values and the date, replacing "Not measured". Leave the 0.38-minute simulated estimate in place, labelled as simulated, and add the observed minutes beside it.
6. State the limits in the report: role-players, n = 5 and n = 2, synthetic documents, a one-case console.
7. Re-test after fixes if any severity 3 or 4 problem is found.

## 9. Pilot test checklist (run once before the real sessions)

**Preparation**
- [ ] Site loads on one Android phone and one iPhone on mobile data, and the console is clean (no errors).
- [ ] The **synthetic image pack is made**: six clean documents for one made-up person, plus a blurry marksheet and a parent's cheque. *Not done yet.*
- [ ] Printed copies (for the optional photo task), or a second screen to photograph.
- [ ] Hindi renders correctly on both phones (Devanagari text, no boxes).
- [ ] The English / Hindi switch on the follow-up works on the phone.
- [ ] The exam passes at 40% and fails at 20%.
- [ ] A page refresh gives a clean new application (state is not kept), so reset between participants.
- [ ] For reviewer tasks: you can set up T4, T8 and a disputed T6 in under 2 minutes each.

**Dry run with one colleague** (not a participant)
- [ ] The scenarios read naturally aloud; no task names a button.
- [ ] The whole applicant session fits in 45 minutes, the reviewer session in 30.
- [ ] The stopwatch, observation sheet and ratings sheet work.
- [ ] The consent script takes under 3 minutes.
- [ ] Recording works and is deleted afterwards.

## 10. Risks

- The "Use specimen" path skips the camera, so photo quality is tested only through the optional image-pack route.
- Role-players may be more patient or more confused than real applicants.
- Two reviewers cannot give a stable time average.
- The console redesign is pending, so early reviewer results may describe a screen that changes.

## Further reading

- *Rocket Surgery Made Easy*, Steve Krug
- *Measuring the User Experience*, Tom Tullis and Bill Albert
