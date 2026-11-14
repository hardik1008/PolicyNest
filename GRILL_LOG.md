# PolicyNest: grill log (grill-with-docs, answered through ask-matt)

- **Written:** 14 Nov 2026, in the same session as `RECONCILED_FINDINGS.md` and `PRD.md`. Documents only; no app file changed.
- **Process followed:**
  - `grill-with-docs` (its SKILL.md says to run `grilling` and `domain-modeling`); both were loaded and followed;
  - questions in **rounds** over a design tree, each round asking the whole **frontier** (only questions whose prerequisites were already settled), numbered, each with a recommended answer worded so that "yes" accepts it;
  - facts were looked up by this session (source greps, the live site, the proxy health check, the engine-block hash: `RECONCILED_FINDINGS.md` §1), never asked;
  - glossary terms and ADRs were written as they settled (`GLOSSARY.md`, `docs/adr/0001` to `0009`).
- **The one deviation, as instructed:** the decisions belong to the user, but the user was not asked. Each question was routed through **ask-matt** to the skill or flow that owns it, and answered from that guidance, the rulebook v3.2, the brief, the `07_WORKFLOW_AND_BUSINESS_LOGIC` specs and CLAUDE.md's standing decisions. **Every answer below is "AI-answered — needs human confirmation".** Where a standing decision already settles a question, the answer restates it and says so.
- **Docs used as the reference:** `01_ORIGINAL_CHALLENGE/PS-01_CHALLENGE_BRIEF.md` (brief), `03_RULEBOOK_AND_REGULATIONS/PS-01_ONBOARDING_RULEBOOK_V3_2.md` (rulebook), `07_WORKFLOW_AND_BUSINESS_LOGIC/01`–`07` (specs), `CLAUDE.md`, `PRODUCT.md`, `planning/PHASE2_SPEC_AND_AUDIT.md` Part D (the user's 21 decisions of 14 Nov).
- **Precedence used to settle conflicts** (itself question G-19, ADR 0006): brief guardrails and the rulebook for decision logic → the user's standing decisions (CLAUDE.md, Phase 3 Part D) for product choices → `07_…` specs and research reports as advice.
- **Phase boundary (ask-matt PHASE-BOUNDARIES):** grill → spec was taken as **Continue** (question 1 of the tree: the spec needs the grilling as a primary source, and the window had room). No `/compact` or `/handoff`.

## Confirmed by the user, 15 Nov 2026 (grill-me round)

The user answered 11 questions in plain language, all "yes". The resulting scope and plan are in `PRD.md` → "Decisions confirmed by the user, 15 Nov 2026" (U1–U11). The entries below are **no longer AI-answered**.

| Grill-me question | User's answer | Settles |
|---|---|---|
| Q1 What is the project for? | Judges first, friends second; hardening only where they'd notice | New scope (PRD U1); narrows G-03, G-26 |
| Q2 Softer focus mode | Yes | **G-04, G-05 confirmed** |
| Q3 Demo controls, `?demo=1` link for friends | Yes | **G-06 confirmed** |
| Q4 Order of work | Accuracy check → accessibility + trust fixes → original list | **G-08 confirmed** (re-run first); **G-09, G-16 confirmed**; **G-26 confirmed only for hiding the internal note from the applicant's history**; G-03 moved to nice to have |
| Q5 Build process | Light: git, one editor at a time, engine check, 3 passes, no tickets, no separate integrator | **G-21 confirmed**; **G-20 confirmed in a lighter form**; G-39 replaced (main session merges) |
| Q6 Switch the AI on | Yes, after the server looks up passages itself | **G-07 confirmed**; G-23 taken into the same server fix |
| Q7 Model | Opus 5.5 at low effort | **G-02 confirmed** |
| Q8 Deploy rhythm | After each pass, with the user's OK and a live check | **G-40 confirmed** |
| Q9 Human work before judging | Usability and deck (must); 20-case adoption and held-out labels (small); photo bench optional | **G-34, G-37, G-44 confirmed**; G-36 only if the bench is done |
| Q10 Pass mark | 50%, demo rule, ask the problem owner | **G-01 confirmed** |
| Q11 Shared understanding | Yes; update PRD and GRILL_LOG only; building waits for a separate go | **G-46 confirmed** |

Decided by the user on 14 Nov and recorded in CLAUDE.md: **G-24** (client address = second entry from the right, measured on Embarko; no `null` origin) and **G-25** (50 AI answers per UTC day, not the 200 proposed here; plus 30 per minute globally). Both are built and live.

Standing decisions restated here, not re-asked: G-17 (near-black on orange), G-22 (console and queue screens wait for references).

**Still AI-answered (not confirmed):** G-03, G-10, G-11, G-12, G-13, G-14, G-15, G-18, G-19, G-23 (beyond the server fix), G-26 (beyond hiding the note), G-27, G-28, G-29, G-30, G-31, G-32, G-33, G-35, G-36, G-38, G-41, G-42, G-43, G-45. Of these, G-11, G-31 and G-33 fall inside pass 2 ("honest numbers") and G-10 and G-12 are proposed for pass 1; confirm them when each pass is briefed.

## Low-confidence answers: confirm these first

| Q | Decision | Confidence | Why it is low |
|---|---|---|---|
| G-02 (confirmed) | Copilot default model stays `claude-opus-5-5` at effort `low`; Haiku 5.5 through an env var | Low | A cost and latency trade-off that is the user's to make; the plan and the code disagree. |
| G-24 (confirmed) | Rate-limit key = the client address Embarko's edge adds, not the first `X-Forwarded-For` value | Low | Which header Embarko's proxy sets, and in which position, was not verified. |
| G-25 (decided: 50/day) | A daily question cap on the proxy (proposed default 200 per day, configurable) | Low | The number is a design parameter, not a measurement; the user must pick it. |
| G-36 (check authorised) | The synthetic image pack may be printed as it is, if the user confirms the layouts are generic | Low | The images were not opened in this session; Phase 3 Q12 asked for generic layouts. |
| G-37 | Claude's 20 hand decisions are shown as the team's only after a team member adopts or overrules each | Low | Only the team can do this; the brief says "your team". |

**Top five decisions needing human confirmation (by impact):** G-02 (Copilot model and cost), G-03 (what autosave keeps on the device), G-06 (sample identity and demo controls hidden behind a disclosure and `?demo=1`), G-20 with G-21 (keep one HTML file and build in parallel through owned regions in a new git repository), G-01 (exam pass mark 50%).

---

## Round 1: the frontier with no prerequisites

### G-01 · Exam pass mark
- **Question:** The rulebook sets no pass mark; four specification documents say 50%; the 160 exam-failure events in the data pack say "Score below 40%". Should the pass mark be 50%, recorded as a demo rule from the state machine rather than as an IRDAI figure?
- **ask-matt routing:** main flow step 1 → `/grill-with-docs` → `/grilling` (a decision) plus `/domain-modeling` (an ADR: surprising to a reader of the data pack, a real trade-off).
- **Answer:** Yes. 50% (3 of 5 on the demo paper), stated once in the facts table (G-32) and labelled "demo rule; the rulebook sets no pass mark".
- **Rationale:** CX-01. Every score below 40% is also below 50%, so the failure events are consistent with 50% too; four specs state 50%; the brief puts the exam out of scope, so the number matters only for consistency. Already live (V1, V16).
- **Confidence:** Medium. · **Findings:** RF-34, CX-01. · **ADR:** 0005.
- **Status:** AI-answered — needs human confirmation (and a problem-owner question: G-43).

### G-02 · Copilot default model
- **Question:** The plan said Haiku 5.5 by default; CLAUDE.md and the proxy say Opus 5.5 at effort `low`. Keep Opus 5.5 at `low` as the default, keep the server-side refusal fallback, and allow `COPILOT_MODEL=claude-haiku-5-5` as a switch?
- **ask-matt routing:** `/grilling` (decision). The facts came from the claude-api skill: list prices per million tokens, input/output, Haiku 5.5 $0.10/$0.50, Sonnet 5.5 $2/$10, Opus 5.5 $4/$20; `fallbacks="default"` with the `server-side-fallback-2026-07-01` beta and `output_config.effort` are valid for Opus 5.5; Haiku 5.5 has no server-side refusal fallback.
- **Answer:** Yes. Default `claude-opus-5-5`, effort `low`; Haiku 5.5 allowed through the env var; a daily cap (G-25) bounds spend whichever model runs.
- **Rationale:** CLAUDE.md is the later of the two decisions and records Opus. The claude-api guidance is to keep Opus unless the user names another model, and not to downgrade for cost on the user's behalf. The Copilot's risk is guardrail quality with applicants, not volume. Latency was not measured (RF-17).
- **Confidence:** Low. · **Findings:** RF-13, RF-17, CX-04.
- **Status:** **Confirmed by the user (14 Nov):** Opus 5.5 at effort `low` is the default.

### G-03 · What autosave keeps on the device
- **Question:** Autosave currently writes the typed full PAN, full account number, DOB, mobile and email to `localStorage` (V8). Should the saved copy keep only what resume and the engine actually read, with the typed account number cut to its last four digits, everything else that the engine does not read dropped, and the consent text listing exactly what is kept?
- **ask-matt routing:** `/grilling` (decision) → `/domain-modeling` (the term **saved progress**; ADR 0003 because it is hard to reverse once people have saves). Which fields the engine reads is a fact for the implementer to confirm with a test (G-38), not a question for the user.
- **Answer:** Yes. Rule: **nothing is saved that resume or the engine does not read**. Typed account number → last four. Mobile and email → kept only if a later step reads them; otherwise re-asked on resume. The PAN read from the card stays, because it is the anchor and re-checks need it; the consent text says so in words. Internal-audience events are never saved (G-26). A shared-device line sits beside the consent box ("Don't save on a shared phone").
- **Rationale:** DPDP minimisation and purpose limitation (brief §8, regulatory matrix), the plan's own promise ("parsed fields only… account last 4"), rulebook §4.3. Dropping the PAN too would break re-checks after resume, because images and raw text are not saved.
- **Confidence:** Medium. · **Findings:** RF-03, RF-06, CX-17. · **ADR:** 0003.
- **Status:** AI-answered — needs human confirmation.

### G-04 · Focus-exit logging
- **Question:** Keep the `FOCUS_EXIT` event (the user's design), but record only that it happened and the running count per sitting, never the seconds away, never where the applicant went, and never as reviewer or decision evidence?
- **ask-matt routing:** `/grilling` plus `/domain-modeling` (the term **focus exit**; ADR 0004).
- **Answer:** Yes. The note becomes "Left the onboarding screen · warning shown · nothing reset". The warning text says "the timer kept running", not how long. The Audit trail shows it as neutral information, not a violation.
- **Rationale:** RF-05. The sitting is a product choice with no rule behind it (CLAUDE.md, PL), so data about it must stay minimal (DPDP). The user's design asks to "warn and log FOCUS_EXIT", which the count still does.
- **Confidence:** Medium. · **Findings:** RF-05. · **ADR:** 0004.
- **Status:** AI-answered — needs human confirmation.

### G-05 · Full screen, phones and assistive tech
- **Question:** On phones and other touch-first devices, skip the full-screen request and the exit warnings (autosave still runs); on desktop, count only `visibilitychange` as an exit, not closing full screen; and offer "Start without full screen" on every device?
- **ask-matt routing:** `/grilling`. Device behaviour that cannot be settled on paper would go to the `/prototype` branch; here the facts are known platform behaviour (CR D1–D5, D12), so no prototype.
- **Answer:** Yes. Closing full screen shows the gentle "return to full screen" banner but is not logged as an exit. On a coarse pointer: no full screen, no exit modal. Optional Wake Lock while a sitting runs.
- **Rationale:** RF-20, RF-23, RF-24. iPhone Safari has no element full screen; in-app browsers deny it; the camera backgrounds the page on Android; screen-reader focus can leave the document. Warnings that misfire teach applicants to ignore them.
- **Confidence:** Medium. · **Findings:** RF-20, RF-22, RF-23, RF-24.
- **Status:** AI-answered — needs human confirmation.

### G-06 · Sample identity and the demo controls
- **Question:** Start every new application with an empty form and consent unticked; move "load the sample applicant", "Use specimen" and the variant dropdowns into one "Demo controls" disclosure that is collapsed by default, opened by `?demo=1` (the link given to friends who test the demo), with test labels like "· T4" shown only inside it?
- **ask-matt routing:** `/grilling` (decision against a standing decision: CLAUDE.md wants T2–T10 triggerable without real documents).
- **Answer:** Yes. Without `?demo=1`, the disclosure is still there, closed, labelled "Demo controls (synthetic documents)", so nobody is locked out of the specimen path.
- **Rationale:** RF-02 (DPDP consent must be an affirmative act), RF-25, CX-18. Keeps the user's "one ideal case" demo one click away.
- **Confidence:** Medium. · **Findings:** RF-02, RF-25, CX-18.
- **Status:** AI-answered — needs human confirmation.

### G-07 · Where retrieval runs, and what the browser sends
- **Question:** Move retrieval into the proxy: it loads the applicant-safe passages at start-up and runs the same BM25 itself; the browser sends only the question, a fixed-schema context of codes (first name, step, document statuses, issue codes, round) and the recent turns; passages sent by a client are ignored?
- **ask-matt routing:** `/codebase-design` (module shape: one deep module behind a small interface at the proxy seam) → `/grilling` to confirm. ADR 0002 (an integration boundary that is costly to change once clients depend on it).
- **Answer:** Yes. The browser keeps its own BM25 only for the offline "rulebook answers" mode. The context is validated against a schema: unknown keys dropped, free text replaced by codes (the app-generated refusal sentence becomes its code).
- **Rationale:** RF-10. Today anyone can post arbitrary "passages" and use the key as a general model. Server-side retrieval closes that without an account system.
- **Confidence:** High. · **Findings:** RF-10, RF-11, RF-12. · **ADR:** 0002.
- **Status:** AI-answered — needs human confirmation.

### G-08 · Pinning the evaluation to the code
- **Question:** Should every evaluation run record the SHA-256 of the engine block it scored, the Evaluation page show that hash beside the hash of the running page, and the build warn when they differ?
- **ask-matt routing:** `/grilling`; the check itself is a `/tdd`-style behaviour test at the engine seam (G-38). Node install was already approved (Phase 3 Q7); installing it is a human step that ask-matt routes to `/wizard` (named by ask-matt, not invoked here).
- **Answer:** Yes. Re-run the evaluation on today's engine (`bd41031462336892…`) as the first build step, before any engine-adjacent change.
- **Rationale:** RF-01. CLAUDE.md: "the engine block's SHA-256 must match the live site's, or the evaluation must be re-run". Accuracy is 30% of the rubric.
- **Confidence:** High. · **Findings:** RF-01, RF-45. · **ADR:** 0001.
- **Status:** AI-answered — needs human confirmation.

### G-09 · Cheering a poor photo
- **Question:** Show the success toast only when a document's instant feedback has nothing to fix and nothing that stops the application, and show the tile as "needs a clearer photo" otherwise?
- **ask-matt routing:** `/grilling`; small behaviour, built with `/tdd`.
- **Answer:** Yes. A low-confidence or partly-read document gets the inline card and a Copilot badge, never a "verified" toast.
- **Rationale:** RF-26; rulebook §4.1; the inline card already knows the answer (V13).
- **Confidence:** High. · **Findings:** RF-26, RF-14.
- **Status:** AI-answered — needs human confirmation.

### G-10 · REJECT as a dead end
- **Question:** Add "Start a new application" and "Delete my saved progress" to the reject panel, and replace "reply to this message" with the real route (the Dispute button)?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. The underage rejection also gives the date from which the person can apply again (rulebook §8 template).
- **Rationale:** RF-27; brief "a wrongful rejection loses a good agent"; rulebook §8 underage template.
- **Confidence:** High. · **Findings:** RF-27.
- **Status:** AI-answered — needs human confirmation.

### G-11 · Time to decision
- **Question:** Measure time to decision from the moment the last required document is accepted (or from Submit, whichever is later) to the moment the decision exists, excluding the reveal animation; label it "this demo, on this device"; and stop showing the 17.3-hour queue baseline beside it on the applicant's screens?
- **ask-matt routing:** `/grilling` plus `/domain-modeling` (the term **time to decision** per brief Table 7: "timestamp from upload to decision").
- **Answer:** Yes. The baseline comparison moves to the Evaluation page, with "queue wait only" stated.
- **Rationale:** RF-33, RF-32. The brief defines the metric from upload; today it times an animation.
- **Confidence:** High. · **Findings:** RF-33, RF-32.
- **Status:** AI-answered — needs human confirmation.

### G-12 · Compliance checklist
- **Question:** Tie each checklist tick to the state it claims (consent box ticked with a timestamp; an accepted Aadhaar document stored as last four only; the registry tick labelled "simulated")?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. A tick that cannot be checked is shown as "not checked in this demo", not ticked.
- **Rationale:** RF-04; brief "a decision you cannot explain is not a decision"; CLAUDE.md "be plain about what is simulated".
- **Confidence:** High. · **Findings:** RF-04.
- **Status:** AI-answered — needs human confirmation.

### G-13 · Hindi scope
- **Question:** Keep Hindi screens and pop-ups as Future (S4), keep Hindi for the follow-up and rejection messages (a brief Must-have), and state the split in the first-visit checklist ("messages in English or Hindi; screens in English")?
- **ask-matt routing:** `/grilling` (re-confirming a standing decision: "English only for now" for pop-ups; PRODUCT S4).
- **Answer:** Yes. The Copilot answers in Hindi only when the AI is connected and the applicant writes in Hindi; offline answers stay English and say so.
- **Rationale:** RF-15; brief Must-have needs only the follow-up in English or Hindi; standing decision.
- **Confidence:** Medium. · **Findings:** RF-15.
- **Status:** AI-answered — needs human confirmation.

### G-14 · Keyless public lookups
- **Question:** Leave Razorpay IFSC, the pincode lookup and libphonenumber out of the MVP, and list them as Future?
- **ask-matt routing:** `/grilling` against a standing decision ("no calls to government or bank services").
- **Answer:** Yes.
- **Rationale:** CX-05, RF-71. The standing decision outranks the research recommendation; the value is small; IFSC format is already checked on the device.
- **Confidence:** Medium. · **Findings:** RF-70, RF-71, RF-72. · **ADR:** 0008.
- **Status:** AI-answered — needs human confirmation.

### G-15 · Editing details after documents are verified
- **Question:** When name, DOB, PAN, Aadhaar last four or bank details change after upload, mark the affected documents "re-check" and refresh their instant feedback, instead of leaving them "verified"?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. A changed typed PAN re-checks everything anchored on the PAN, as a changed PAN document already does in the re-check rule.
- **Rationale:** RF-28; CX-08; brief Should-have "re-processing without re-checking everything else" works only if staleness is tracked.
- **Confidence:** High. · **Findings:** RF-28.
- **Status:** AI-answered — needs human confirmation.

### G-16 · Invented time copy
- **Question:** Remove "About 2 minutes" and "Many agents pass on their second try", and allow only time statements that come from the rules (15 hours, 24 hours, 4 working hours, 30 minutes for the sitting)?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes.
- **Rationale:** RF-29; CLAUDE.md "do not invent numbers".
- **Confidence:** High. · **Findings:** RF-29.
- **Status:** AI-answered — needs human confirmation.

### G-17 · Contrast and the orange
- **Question:** Build the agreed near-black text on orange fills (and on the hero gradient) first in the accessibility work, keeping the orange itself?
- **ask-matt routing:** `/grilling` (restating Phase 3 Q1, a standing decision).
- **Answer:** Yes. Brand ink `#141414` in both themes; the light focus ring moves to a colour that reaches 3:1 on white.
- **Rationale:** RF-41, RF-43; CLAUDE.md Contrast decision.
- **Confidence:** High. · **Findings:** RF-40 to RF-43.
- **Status:** AI-answered — needs human confirmation.

### G-18 · Rule codes on applicant screens
- **Question:** Show applicants plain labels only ("Your photo is clear", "Name matches your PAN") and keep rule sections, check-result codes and name tiers in the Audit trail and the review console?
- **ask-matt routing:** `/grilling` plus `/domain-modeling` (two vocabularies: applicant words and ops codes; both in GLOSSARY.md).
- **Answer:** Yes. The rulebook citation stays one tap away ("Why?") for applicants who want it.
- **Rationale:** RF-30, RF-31; rulebook §8 (say exactly what is wrong, what to send and how).
- **Confidence:** High. · **Findings:** RF-30, RF-31.
- **Status:** AI-answered — needs human confirmation.

### G-19 · Which source wins
- **Question:** When sources disagree, should the order be: brief guardrails and rulebook (for decision logic) → the user's standing decisions (for product choices) → `07_…` specs, data dictionary and research reports (advice)?
- **ask-matt routing:** `/domain-modeling` (an ADR: a constraint not visible in the code).
- **Answer:** Yes. Applied to CX-06 to CX-09 and CX-15.
- **Rationale:** The rulebook says the product "should apply the same rules"; the brief's guardrails are the challenge's constraints; the specs contradict each other and the rulebook in places (RF-62 to RF-65).
- **Confidence:** High. · **Findings:** RF-62 to RF-66. · **ADR:** 0006.
- **Status:** AI-answered — needs human confirmation.

### G-20 · One HTML file, many agents
- **Question:** Keep `PolicyNest.html` as one self-contained file (a standing architecture decision), and make parallel work safe by dividing it into named, owned regions, letting only one agent write the file at a time, and merging lanes in a fixed order through one integrator?
- **ask-matt routing:** `/codebase-design` (seams, locality) → `/grilling`. Multi-session build → `/to-spec` → `/to-tickets` → `/implement-spec` (implementer subagents on a frontier, one integration branch; named by ask-matt, not invoked here).
- **Answer:** Yes. Region markers (CSS tokens, CSS components, shell markup, each view's render functions, the engine block, the Copilot client, boot) are added once by the integrator. Non-HTML work (proxy, build script, evaluation, docs, bench) runs truly in parallel. Splitting into several source files joined by `build_site.py` is the fallback if merges conflict too often.
- **Rationale:** CLAUDE.md: "one self-contained file… no build tools"; the claude.ai artifact copy needs one file; the engine block must stay extractable for the evaluation. Two writers in one file would overwrite each other.
- **Confidence:** Medium. · **ADR:** 0007.
- **Status:** AI-answered — needs human confirmation.

### G-21 · A git repository
- **Question:** Turn the project folder into a git repository (with `.env`, `__pycache__`, `05_SPECIMEN_DOCUMENTS/sample_specimens` and the autoresearch workspace ignored) before the multi-agent build, so lanes can run in worktrees?
- **ask-matt routing:** `/grilling`; it is a precondition for `/implement-spec`'s integration branch.
- **Answer:** Yes, with the user's OK, and with `sample_specimens` never added.
- **Rationale:** RF-77, RF-09. Worktrees give each lane an isolated copy; history makes the engine SHA check and review possible.
- **Confidence:** Medium. · **ADR:** 0007.
- **Status:** AI-answered — needs human confirmation.

### G-22 · Queue screens and the console redesign
- **Question:** Keep the review-console redesign (R7), the queue screens (R6) and the A/M/R keys (R9) blocked until the user's references arrive, and build only the queue data and the §4.6 rule now?
- **ask-matt routing:** `/grilling` (restating Phase 3 Q2 and CLAUDE.md "the review console is unchanged on purpose").
- **Answer:** Yes.
- **Rationale:** Standing decision; builds the queue once.
- **Confidence:** High. · **Findings:** RF-52, RF-54.
- **Status:** AI-answered — needs human confirmation.

---

## Round 2: unblocked by round 1

### G-23 · Corpus audience and the output filter (after G-07)
- **Question:** Tag every passage at build time as `applicant` or `internal` (internal = fraud-desk handling, reviewer-only procedure, escalation contacts), retrieve only `applicant` passages for the Copilot, and add the same banned-word output filter on the server that the client has?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. The build fails if an `applicant` passage contains a banned term ("fraud", "fake", "forged", "tamper", "suspicious"). The fraud-desk rule is told to applicants only as "a person on our team will check".
- **Rationale:** RF-11 (13 of 55 chunks); rulebook §8; brief "messages never mention fraud".
- **Confidence:** High. · **Findings:** RF-11. · **ADR:** 0002.
- **Status:** AI-answered — needs human confirmation.

### G-24 · Client address, origins and the rate limit (after G-07)
- **Question:** Key the rate limit on the client address Embarko's edge appends (the right-most `X-Forwarded-For` entry, if that is what Embarko does), drop `null` from the production origins, and prune old entries from the rate table?
- **ask-matt routing:** `/grilling`; the header fact is research (`/research`, named by ask-matt) to be done by the implementer before coding.
- **Answer:** Yes, conditionally: if Embarko's header behaviour cannot be confirmed, fall back to a global per-minute cap plus the daily cap (G-25).
- **Rationale:** RF-10. The first `X-Forwarded-For` value is whatever the client sends.
- **Confidence:** Low (fact gap). · **Findings:** RF-10.
- **Status:** **Confirmed and built (14 Nov):** all three changes. Measured: Embarko's proxies append two entries ([client, edge]), so the proxy uses the second from the right (`XFF_TRUSTED_HOPS=2`). There is also a 30-per-minute global cap. Original wording: all three changes (Embarko client address once verified, else a global per-minute cap; drop `null` from production origins; prune the rate table).

### G-25 · Spend cap (after G-02, G-07)
- **Question:** Add a daily question cap on the proxy, configurable by env var, with a proposed default of 200 questions per day, after which the Copilot falls back to rulebook answers and says so?
- **ask-matt routing:** `/grilling`; setting the env var on Embarko is a human dashboard step (`/wizard` territory).
- **Answer:** Yes. 200 is a proposal, not a measured figure.
- **Rationale:** RF-10, RF-13. Bounds the cost of any model choice.
- **Confidence:** Low. · **Findings:** RF-10, RF-13.
- **Status:** **Decided by the user (14 Nov): 50 questions per day**, not 200, configurable by env var.

### G-26 · Internal events and the Audit trail (after G-03)
- **Question:** Give every event an audience (`applicant` or `internal`), keep internal events out of the saved copy, and label the Audit trail page "Ops and compliance view (this demo shows both roles)" with internal events marked "internal"?
- **ask-matt routing:** `/domain-modeling` (the term **internal event**) → `/grilling`.
- **Answer:** Yes. The applicant's own screens never render internal events.
- **Rationale:** RF-06; rulebook §8; brief "a working interface a reviewer and an applicant can each use".
- **Confidence:** Medium. · **Findings:** RF-06. · **ADR:** 0003.
- **Status:** AI-answered — needs human confirmation.

### G-27 · Where a resumed applicant lands (after G-03)
- **Question:** Adopt the critical review's resume table: the first incomplete details page; the first missing document; the verification result without the animation; the follow-up panel with the round and days left of 14; the human-review panel; the reject panel with Delete and Start again; training with hours kept; the exam with the retake time; the certificate; the checklist with an "expired" notice?
- **ask-matt routing:** `/grilling`; a state model like this would go to `/prototype` if it were in doubt; it follows the state machine, so it is not.
- **Answer:** Yes. Thumbnails are never saved, so restored documents show "verified earlier".
- **Rationale:** RF-21; state machine §2 (30 days in DRAFT, 14 days once rework is open).
- **Confidence:** High. · **Findings:** RF-21, RF-08.
- **Status:** AI-answered — needs human confirmation.

### G-28 · Telling the truth about "saved" (after G-03)
- **Question:** Show "saved on this device" only after a write followed by a successful read-back, request persistent storage after consent, and show an "open in Chrome or Safari" hint when the page runs in an in-app browser?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes.
- **Rationale:** RF-07; the demo link will be shared by WhatsApp and open in its in-app browser.
- **Confidence:** Medium. · **Findings:** RF-07.
- **Status:** AI-answered — needs human confirmation.

### G-29 · The 24-hour retake gap (after G-01, G-06)
- **Question:** Store the time of a failed exam, show when the retake opens (also after resume), and keep a "Demo: skip the 24-hour wait" button inside the demo controls?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes.
- **Rationale:** RF-34; rulebook §2 ("re-attempt allowed after 24 hours"); state machine.
- **Confidence:** High. · **Findings:** RF-34.
- **Status:** AI-answered — needs human confirmation.

### G-30 · Toasts and nudges
- **Question:** One channel per event (success → toast; a problem → inline card plus a Copilot badge), toasts pause on hover and focus, only one live region for toasts, and the Copilot drawer never opens on its own?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes.
- **Rationale:** RF-14; WCAG 2.2.1 for the 5.2 s timeout.
- **Confidence:** High. · **Findings:** RF-14.
- **Status:** AI-answered — needs human confirmation.

### G-31 · Fleet numbers off the applicant's screens
- **Question:** Move fleet benchmarks ("today 17.3 h", "today 8.4 days") and fixed check counts to the Evaluation page, and show applicants only their own progress?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. The certificate shows the applicant's own time and touches without a fleet comparison.
- **Rationale:** RF-32, RF-50.
- **Confidence:** High. · **Findings:** RF-32, RF-50.
- **Status:** AI-answered — needs human confirmation.

### G-32 · One table of facts (after G-01)
- **Question:** Keep the facts the product states (pass mark, training hours, retake gap, SLAs, sitting length, save windows) in one table that the screens and the offline Copilot answers both read, and have the build check that each fact appears in the rulebook or spec passage it cites?
- **ask-matt routing:** `/codebase-design` (one source of truth, locality) → `/grilling`.
- **Answer:** Yes.
- **Rationale:** RF-16; CR §6.
- **Confidence:** Medium. · **Findings:** RF-16.
- **Status:** AI-answered — needs human confirmation.

### G-33 · Honest Evaluation page (after G-08)
- **Question:** Add a "routed to a person" column (or split counts) to the confusion matrix, rename the fairness chip "no gap in-sample", add the 60.7% "approved first time" row, put "in-sample" on the headline tiles, and show the engine hash?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes.
- **Rationale:** RF-46, RF-45; CLAUDE.md "say in-sample".
- **Confidence:** High. · **Findings:** RF-45, RF-46, RF-51.
- **Status:** AI-answered — needs human confirmation.

### G-34 · The held-out set
- **Question:** Keep the agreed held-out set (Phase 3 Q8: about 30–40 constructed cases, labelled by the user independently, hashed before the engine sees them), and make sure it covers face 0.60–0.75, surname change, unlisted board, a dispute and two selfie failures below 0.60 in a row?
- **ask-matt routing:** `/grilling` (restating a standing decision); the labelling itself is human work.
- **Answer:** Yes. Any rule changed after seeing held-out results turns the set in-sample, and the report says so.
- **Rationale:** RF-47; brief §8 Human-only coverage; PRODUCT §6 "not evaluable on the test set".
- **Confidence:** High. · **Findings:** RF-47.
- **Status:** AI-answered — needs human confirmation.

### G-35 · Two selfie failures (rulebook §4.6)
- **Question:** Count face-match scores below 0.60 per application across rounds, outside the engine block (as decided), and on the second consecutive one route the case to a reviewer with an internal referral event while the applicant sees "a person is checking a few details"? Does a score of 0.60 or more reset the run?
- **ask-matt routing:** `/grilling` plus `/domain-modeling` (term **selfie failure**).
- **Answer:** Yes; a score of 0.60 or more (a pass or a human-review score) resets the consecutive count, because the rulebook says "in a row".
- **Rationale:** RF-53; rulebook §4.6 and §7 (same-day fraud-desk SLA); Phase 3 Q6 and Q18.
- **Confidence:** Medium. · **Findings:** RF-53.
- **Status:** AI-answered — needs human confirmation.

### G-36 · The image pack's layouts
- **Question:** Phase 3 Q12 asked for generic layouts that do not reproduce government ID designs; the pack follows the (synthetic) PS-01 specimen layouts. Print and photograph it as it is, if the user looks at it and confirms the layouts are generic and SPECIMEN is visible on every image?
- **ask-matt routing:** `/grilling`; needs a human look.
- **Answer:** Yes, after that check; prints stay with the team.
- **Rationale:** RF-79; P2 Part B lookalike row.
- **Confidence:** Low. · **Findings:** RF-79, RF-39.
- **Status:** **User (14 Nov):** Claude may open the generated image pack (never `sample_specimens`) to check layouts and the SPECIMEN mark; the user still confirms before printing.
- **Check done (14 Nov, Claude, 7 images):** every image carries the red "SPECIMEN, SYNTHETIC" banner and a diagonal watermark; the photo boxes hold a grey avatar, with no face; the Aadhaar number is masked to XXXX XXXX 6407; there are no emblems, logos, QR codes or holograms. Three things lean towards real designs: (1) both Aadhaar sides use the saffron/green bands and UIDAI's real tagline "Aadhaar - Aam Aadmi ka Adhikar"; (2) both cheques name a real bank, BANK OF BARODA, with its real IFSC prefix BARB; (3) the issuer names INCOME TAX DEPARTMENT, Government of India and Unique Identification Authority of India appear, but the OCR type gate needs these keywords, so they should stay. **Recommendation:** before printing, remove the tagline and the coloured bands, and swap the bank for a fictional one with a fictional IFSC (for example NEST0…). **Done (14 Nov, user said yes):** the generator `tools/make_pack.py` was changed. The Aadhaar bands are gone, and the tagline is replaced by "Synthetic test card, not an Aadhaar". The bank is now POLICYNEST DEMO BANK with IFSC NEST0371264, and the MICR line is zeroed. All 7 images and both print PDFs were regenerated. All five clean images pass real OCR in the app (local build, 14 Nov); the parent's-cheque variant gives the bank-name fix. A person still confirms before printing.

### G-37 · Claude's 20 hand decisions
- **Question:** Show the Stage 1 "20 decided by hand" only after a team member has adopted or overruled each of the 20, and say "first drafted by an AI, reviewed by the team"?
- **ask-matt routing:** `/grilling`; human work.
- **Answer:** Yes.
- **Rationale:** RF-57, CX-14; brief Stage 1 "decided by hand by your team".
- **Confidence:** Low. · **Findings:** RF-57.
- **Status:** AI-answered — needs human confirmation.

---

## Round 3: spec and build questions (unblocked by rounds 1–2)

### G-38 · Test seams (to-spec step 2)
- **Question:** Test at three seams, using existing ones: (1) the **engine block**, run in Node on the 600 cases and the held-out set (the existing `eval/run_eval.js`); (2) the **public page**, driven through its own controls in a browser for T1–T10 and the new behaviours (the method in CLAUDE.md "How to test"); (3) the **proxy's HTTP contract**, with Python standard-library tests and no key? No new seams inside the page.
- **ask-matt routing:** `/to-spec` step 2 ("prefer existing seams, the highest seam possible") and `/tdd`.
- **Answer:** Yes. Seam 2 is the highest and covers most requirements; seam 1 protects the scored metric; seam 3 protects the key.
- **Rationale:** to-spec: "the fewer seams, the better". All three already exist in some form.
- **Confidence:** High.
- **Status:** AI-answered — needs human confirmation (to-spec asks for this check with the user).

### G-39 · Agent roles and models
- **Question:** Orchestrator and integrator on Opus 5.5 (this kind of session); privacy, proxy and engine-adjacent lanes on Opus; UI lanes on Sonnet 5.5; read-only verification sweeps (contrast audit, grep checks, live checks) on Haiku 5.5?
- **ask-matt routing:** `/implement-spec` (implementers on a frontier) and PHASE-BOUNDARIES ("can the task be done AFK? → subagent").
- **Answer:** Yes.
- **Rationale:** Capability where the risk is (privacy, key, scored engine); speed where the work is well specified.
- **Confidence:** Medium.
- **Status:** AI-answered — needs human confirmation.

### G-40 · Deploy gate
- **Question:** Nothing is built until the user says go (standing decision), and no phase is deployed until the user approves it; each deploy is followed by live checks with a `?v=N` cache-buster and the engine-hash check?
- **ask-matt routing:** `/grilling` (restating a standing decision).
- **Answer:** Yes.
- **Rationale:** CLAUDE.md "Go-ahead"; outward-facing actions need confirmation.
- **Confidence:** High.
- **Status:** AI-answered — needs human confirmation.

### G-41 · Keeping PRODUCT.md and CLAUDE.md true
- **Question:** A docs lane updates PRODUCT.md statuses, CLAUDE.md, USABILITY_TEST_PLAN.md and `MISSING_SOURCE_MATERIALS.md` at the end of each phase, moving a goal to Built only after its acceptance check passed on the live site?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. The first docs pass fixes the stale lines found here (RF-74, RF-75, RF-69).
- **Rationale:** CLAUDE.md "Update it when a goal's status changes".
- **Confidence:** High. · **Findings:** RF-74, RF-75, RF-69, RF-57.
- **Status:** AI-answered — needs human confirmation.

### G-42 · When the usability sessions run
- **Question:** Run the five applicant sessions after the privacy, accessibility and flow fixes are live (so they test an empty form and the fixed messages), and the two reviewer sessions after the console redesign?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. Sessions may start earlier if participants are only free earlier; the report then names the build.
- **Rationale:** UT §4 timing caveat; RF-48, RF-75.
- **Confidence:** Medium. · **Findings:** RF-48.
- **Status:** AI-answered — needs human confirmation.

### G-43 · Problem-owner questions
- **Question:** Write `planning/DISCOVERY_QUESTIONS.md` with the brief's ten questions marked "not asked" (Phase 3 Q13) and add four more: the exam pass mark, the recognised-board list, the value of one certified agent, and how much reviewer time would really be released?
- **ask-matt routing:** `/to-questionnaire` (the gap is in someone else's head; named by ask-matt, not invoked here).
- **Answer:** Yes.
- **Rationale:** RF-67, RF-80, CX-01, S1P §3.5.
- **Confidence:** High. · **Findings:** RF-67, RF-80.
- **Status:** AI-answered — needs human confirmation.

### G-44 · The executive deck
- **Question:** Build the deck last (Phase 3 Q14, Q21), with accuracy labelled in-sample, the simulation labelled directional, and usability numbers only once measured?
- **ask-matt routing:** `/grilling` (restating a standing decision).
- **Answer:** Yes.
- **Rationale:** RF-80; rubric 10%.
- **Confidence:** High. · **Findings:** RF-80.
- **Status:** AI-answered — needs human confirmation.

---

## Round 4: closing the frontier

### G-45 · Is anything still assumed?
- **Question:** Are the only remaining unknowns facts that the build itself must establish (listed below), rather than decisions?
- **ask-matt routing:** `/grilling` ("the session is done when the frontier is empty").
- **Answer:** Yes. Facts for the build to establish, each with an owner in PRD §11:
  1. which typed fields the engine reads (G-03; a saved-keys test);
  2. Embarko's forwarded-for behaviour (G-24);
  3. Copilot latency and cost per question once a key is set (RF-17);
  4. OCR results on phone photos (RF-39);
  5. timer and full-screen behaviour on iOS, Android and in-app browsers (RF-24);
  6. whether today's engine still scores 600/600 (G-08).
- **Confidence:** High.
- **Status:** AI-answered — needs human confirmation.

### G-46 · Shared understanding
- **Question:** The grilling skill says not to act until the user confirms a shared understanding. Is this log, plus the PRD built on it, the thing the user confirms before any build starts?
- **ask-matt routing:** `/grilling`.
- **Answer:** Yes. The PRD's roadmap starts with a "user confirms GRILL_LOG" gate.
- **Confidence:** High.
- **Status:** AI-answered — needs human confirmation.

---

## Summary

- **Questions:** 46 in four rounds (22, 15, 7, 2).
- **Confidence:** 26 High, 15 Medium, 5 Low; the five Low ones are in the table at the top. (Counted: High G-07, 08, 09, 10, 11, 12, 15, 16, 17, 18, 19, 22, 23, 27, 29, 30, 31, 33, 34, 38, 40, 41, 43, 44, 45, 46; Medium G-01, 03, 04, 05, 06, 13, 14, 20, 21, 26, 28, 32, 35, 39, 42; Low G-02, 24, 25, 36, 37.)
- **Glossary entries written:** `GLOSSARY.md`.
- **ADRs written:** `docs/adr/0001` to `0009`.
- **Frontier:** empty once the user confirms; the remaining unknowns are facts with owners (G-45).
