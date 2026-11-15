# Feature triage: the "Full project implementation" log vs PolicyNest

Written 15 Nov 2026. Source: `D:\FULL_PROJECT_IMPLEMENTATION_AND_TECH_FIXES_LOG.md` (a different build: Next.js + FastAPI on Railway). Each feature is checked against what PolicyNest already does and against the standing decisions in `CLAUDE.md`:

- no API keys;
- no calls to government or bank services;
- one ideal case;
- real on-device OCR;
- never invent numbers;
- no server-side store;
- no fraud wording to applicants.

**Rule used:** add a feature only if it helps an applicant, reviewer or judge on *this* product, can be built in the single-file browser app, and is honest about what is real.

## A. Not imported: the log's headline numbers

These are claims about that other build, not measurements of PolicyNest, and several contradict the data pack. They are **not** copied into any PolicyNest screen or document:

- "73% abandonment": the pack says 27.3% of returned applicants go silent, and 31.7% of starters drop out.
- "403x faster", "<30 min TAT" and "<8% drop-off": none of these was measured.
- "99.50% accuracy": PolicyNest measures 100.0% in-sample on its own engine, with 98.0% on the first run.

PolicyNest keeps reporting only what `eval/` measures, labelled in-sample or simulated.

## B. Already in PolicyNest (no work)

| Log feature | PolicyNest equivalent |
|---|---|
| Automatic document recognition | `classify` and the per-slot type gate (A4) |
| OCR with confidences | Tesseract.js / pdf.js on the device; a confidence per document (D1, D2) |
| Honorific removal, initials, order swap, middle name | `norm()` and the rulebook name tiers (`nameTier`) |
| Cross-document triangulation, PAN as anchor | `decide()` (C1–C3) |
| Rulebook rules: age, PAN 4th character P, Class 10 pass | engine checks with § citations |
| Correction recommendation, consolidated rework | one follow-up message in English and Hindi (F1) |
| Incremental reprocessing, stale-result protection, automatic re-decision | `recheck()`, `S.changed`, rounds (F2, F3) |
| State machine, audit trail with hashes | states, events with engine hash (E1, FR-56) |
| Uncertainty → person, edge-case escalation | NEEDS_MORE_INFO, Human-only routing (R1, R2, §4.6) |
| 600-case ground-truth evaluation | `eval/run_eval.js`, Evaluation page (E2) |
| Explainable decisions | every check cites its rule |
| Progressive feedback, instant acknowledgement | instant feedback after each upload (A14) |
| Micro-review side-by-side cards | reviewer task with evidence side by side (R3) |
| 30-minute session, persisted timer, auto-advance | the sitting (A12), autosave with consent, next-document advance |
| Grounded copilot with citations | Onboarding Copilot (A15) |
| Aadhaar last-4 only (DPDP) | typed field is 4 digits; OCR masks; nothing else stored (D5) |
| "Simulate capture" for laptops without cameras | "Use specimen" with variants in Demo controls |
| Simulated penny drop, IRDAI registry | `SIM`, labelled simulated |

## C. Add (13 items)

| # | Feature (from the log) | What PolicyNest gets | Why it is worth it | Honest limits |
|---|---|---|---|---|
| C1 | Image-quality intelligence, pre-capture validation, fast path | Before OCR: a canvas check for **blur** (Laplacian variance), **glare** (share of clipped-white pixels), **too dark** and **too small**, with instant plain-language advice and "use anyway" | Image quality is the biggest single rule (13.2 points in the ablation); the frontend spec §2.1 asks for it; it saves a slow OCR run on a bad photo | Heuristic thresholds, labelled as a photo check, not a verdict; OCR confidence (§4.1) still decides |
| C2 | Client-side preprocessing: EXIF orientation, downscale | Phone photos are turned upright and downscaled to ≤ 1920 px before OCR and thumbnails | Faster OCR and less memory on phones (D6 risk) | None |
| C3 | Live camera capture | Each slot gets **Take photo** (opens the phone camera via `capture`) beside **Choose file**; the selfie opens the **front** camera (FR-18); the selfie slot accepts images only | Phone-first applicants (PRODUCT §3) | No in-page video stream or corner detection (heavier; the native camera app is better on phones) |
| C4 | SHA-256 document hashing (duplicate check) | The same file uploaded into two slots is refused ("this is the same file you used for your PAN card") | Catches a common mistake at once | Within one application only; no cross-application fraud graph (see D) |
| C5 | Document versioning | Each slot keeps a version list (v1, v2, …: round, time, file hash prefix) shown on the document card and logged in the Audit trail | A compliance officer can see what was replaced and when | Only metadata is kept, never the image (D5) |
| C6 | Vernacular voice guidance (Web Speech API) | **Read aloud** on the follow-up message (Hindi or English voice) and on each document's guidance, with Stop; hidden where the browser has no voice | Many POSPs prefer Hindi and are phone-first; it is free and on-device | Voice quality depends on the device; nothing is sent anywhere |
| C7 | Bilingual WhatsApp share, 160-character SMS | The follow-up shown as a **phone-style message preview**, with **Copy message**, **Open in WhatsApp** (a `wa.me` link the applicant chooses to open) and a **≤ 160-character SMS** version | Makes the "one consolidated message" visible and reusable; judges see the message as an applicant would | Sending stays simulated; no number is pre-filled; no PAN or Aadhaar in the text |
| C8 | IFSC master lookup | An **offline** IFSC helper: format check as you type plus the bank name from a bundled table of bank codes (first four letters) | Catches typos at once with no network call | The bank name only, no branch (live lookups are out of scope, PRD §15) |
| C9 | 1-click evaluator persona and demo selector | A **scenario launcher** in Demo controls: pick T1–T10 and the sample applicant and the right specimen variants are set in one click | U1: judges first; today a judge must know which pickers to set | Labelled as a demo; only inside Demo controls |
| C10 | Public certificate verification, print styling | The certificate gets **Print / save as PDF** (print CSS, FR-35) and an **integrity seal**: the SHA-256 of its fields, plus a "verify this certificate" panel that recomputes it | A judge can print it and see the seal check out | Labelled "demonstration certificate; the seal shows the fields were not edited on this device, not that IRDAI issued it" |
| C11 | Rulebook transparency (admin rules page, explainable outcomes) | A read-only **Rules applied** panel on the Audit trail: every check the engine runs, with its rulebook section | Compliance officer reading (brief Table 4) | Derived from the engine's own output; no rule editing |
| C12 | Exhaustive automated test suite | `tools/t1_t10.py`: a Python Playwright runner that drives T1–T10 through the page (local or live) and prints pass or fail | Every check so far was hand-written in a browser; this makes it one command | Needs Playwright (already installed on this machine) |
| C13 | Upload acknowledgement with document scenario cards (small UX) | A "what a good photo looks like" hint per slot (four corners, daylight, no glare), shown before the first upload | Fewer re-uploads; matches the defect taxonomy wording | Text and icons only |

## D. Not adding, and why

| Log feature | Reason |
|---|---|
| 1-click DigiLocker pull (client-generated "signed" documents) | Generating "tamper-proof" proofs in the browser would present fake documents as verified (GR-10). DigiLocker stays Future (S2) |
| Account Aggregator, NPCI penny drop with a UTR number | A made-up UTR is an invented number; penny drop is already simulated and labelled |
| India Post PIN API, Razorpay IFSC API (live calls) | Standing decision: no calls to government or bank services; PRD §15 lists keyless public lookups as out of scope; it would also send applicant data to third parties. C8 gives an offline IFSC helper instead |
| Gemini Vision OCR, bounding boxes | Needs an API key and a server; raw OCR and boxes are deliberately not stored (D5) |
| 8-tier name matcher with phonetic and fuzzy auto-pass | Rulebook §5: a spelling variant is NEEDS_INFO, never an automatic match, so auto-passing "Choudhary = Chowdhury" would break the rulebook and the 100% in-sample result |
| Cross-application fraud ring graph, mule-bank and SIM-stacking rings, "freeze payouts" | There is one application per browser and no server, so the rings would be fabricated; the brief puts fraud investigation beyond flagging out of scope |
| Login, register, roles, admin users and reviewers, notifications inbox | No accounts or server by design (ADR 0003); the sidebar already switches views |
| Event bus, async queues, SSE, connectors, server-side versioning, risk-tier routing | Server infrastructure; routing and queue screens wait for your console references (R6, R7) |
| Next.js, ESLint, Railway, PowerShell and git fixes, Vitest suite | Specific to that codebase |

## E. Build plan

- **One writer at a time on `PolicyNest.html`.** Each lane: a Haiku builder, then a Sonnet audit, then Haiku fixes. The engine block is never touched, and `tools/check_pack.py` must pass after each lane.
  - L1 capture and photo: C1, C2, C3, C4, C5, C13.
  - L2 message and voice: C6, C7.
  - L3 helpers for applicants and judges: C8, C9, C11.
  - L4 certificate: C10.
- **In parallel (separate file):** L5 `tools/t1_t10.py` (C12).
- **Then:** a browser check of every item, a T1–T10 run with the new tool, and a deploy only with your OK.
