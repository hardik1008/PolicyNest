# PolicyNest build log and hand-over

- **Last updated:** 15 Nov 2026, when the build was **paused** for a second planning review.
- **What this file is:** the record of what was built against `PRD.md`, how each step was checked, what is live, and where to pick up. Read it with `PRD.md` → "Decisions confirmed by the user, 15 Nov 2026" (the plan), `GRILL_LOG.md` (the decisions) and `RECONCILED_FINDINGS.md` (the findings).
- **Status in one line:** step 0 and pass 3 are done, committed and live. Pass 1, pass 2 and the rest of the plan have not started. Building waits for the user's go after the review.

## 1. Timeline

| When (15 Nov, IST) | Step | Commit | Deployed |
|---|---|---|---|
| — | Planning: reconciled findings, grill log, glossary, 9 ADRs, PRD (14 Nov); grill-me round with the user, 11 decisions confirmed (15 Nov) | in baseline | — |
| 00:44 | Git repository and baseline commit | `f3e5dba` | — |
| 00:48 | **Step 0:** Node, evaluation re-run, results pinned to the engine hash | `e3ed958` | — (no app change) |
| 00:52 | **Pass 3:** Copilot server does its own lookup; applicant-safe passages | `4c87e19` | Yes, with the user's go |
| after | Pass 3 deployed: proxy first, then site; live checks | — | Both live |

## 2. Step 0: foundation

**Done:**

- **Git repository** at the project root, branch `main`, no remote, commits under the user's own git identity.
  - `.gitignore` covers: `.env` and `.env.*` (`.env.example` is kept), `05_SPECIMEN_DOCUMENTS/sample_specimens/` (never opened, never committed), the autoresearch run's own inner repository (`autoresearch/*/workspace/`), `node_modules/`, `__pycache__/`, `.claude/settings.local.json`.
  - Checked before the first commit: none of those paths was staged.
- **Node.js 26.13.1 LTS** installed with `winget` (allowed by Phase 3 Q7).
  - The evaluation's one dependency (`papaparse@5.4.1`) is installed in the session scratch folder, **not** in the project, and found through `NODE_PATH`. To re-run elsewhere, run `npm i papaparse` in any folder and point `NODE_PATH` at its `node_modules`.
- **Evaluation re-run on today's engine:**
  - all figures **identical** to the 13 Nov run: accuracy 100.0%, REJECT and NEEDS_MORE_INFO precision and recall 1.0, 0 wrongful approvals, 11 routed to a person, straight-through 98.2%;
  - all **600 predictions identical line for line** (`eval_predictions.csv`); only the run time and the timing figure differ;
  - still **in-sample**.
- **Results pinned to the code** (ADR 0001, FR-57 runner side, FR-58):
  - `eval/run_eval.js` now writes `engine_sha256` into `eval/out/eval_results.json`;
  - the hash is SHA-256 of the block from `/* ENGINE:START` up to, not including, `/* ENGINE:END */`, with LF line endings;
  - value: **`c5da9cfb54f8e716b9630a7075a9f25db04e47cc696061ee7136e98019bce367`**;
  - it matches `policynest_mvp/PolicyNest.html`, `policynest_mvp/site/index.html` and the live site;
  - the `bd41…` value quoted on 14 Nov came from the same code with the end marker included: a different convention, not a code change.
- **Documents updated:** `eval/EVALUATION_REPORT.md` (re-run note), PRD, GRILL_LOG and RECONCILED_FINDINGS (canonical hash). RF-01 is marked resolved.

**Not done (optional in the plan):** region markers in `PolicyNest.html`. Under the lighter plan (U5), the main session edits the file alone, so they are not needed yet.

## 3. Pass 3: Copilot server

Requirements covered: FR-46 (server side), FR-47, FR-48, FR-49 (server side), FR-51, FR-65, FR-66. **`PolicyNest.html` was not changed.**

**Built:**

- **`policynest_mvp/build_site.py` (applicant-safe corpus):**
  - removes every sentence (in prose and lists) and every table row that contains fraud-desk wording (`fraud…`, `fake`, `forged`, `forgery`, `tamper…`, `suspicious`);
  - drops a passage left under 40 characters;
  - tags the rest `audience: "applicant"`;
  - refuses to build if any banned word is left.

  Result: 55 passages, 13 of which had internal wording removed, 0 fraud mentions. The useful rules stay. For example, rulebook §4.6 keeps "Ask for a fresh selfie in good light." and loses the fraud-desk sentence; §5 keeps every name rule except the "different person… flag to fraud desk" row; §7 loses only the fraud-desk SLA row. It writes the same file to `site/kb.json` (offline rulebook answers in the page) and `copilot_api/kb.json` (the server's lookup).
- **`policynest_mvp/copilot_api/main.py` (the Copilot server):**
  - **Retrieval:** its own BM25 over `kb.json`, using the same tokenising and scoring as the page. `passages` sent by a browser are **ignored**.
  - **Context schema:** keeps only the fields the page's `copilotContext()` sends, with types and lengths checked. Unknown fields are dropped; issue codes must look like codes.
  - **Inputs:** history trimmed to 6 turns of 800 characters. A question or user turn with a PAN-, Aadhaar- or account-shaped number gets `400 id_number`, **before any model call** (rulebook §4.3). An empty or non-object body gets `400`.
  - **Output:** an answer containing fraud wording or "you are approved/rejected" is replaced by a fixed safe sentence; a refusal returns a fixed sentence.
  - **Model:** Haiku models are called without the server-side fallback beta (Haiku 5.5 has none). Opus 5.5 at effort `low` is still the default.
  - **Kept unchanged:** origin allow-list without `null`, 24 KB body cap, 20 questions per 10 minutes per client, 30 per minute globally, 50 AI answers per UTC day, client address from the second `X-Forwarded-For` entry from the right.
  - **Response** now includes `sources` (the cites used). The page reads only `answer` and needs no change. On any non-200 reply the page gives rulebook answers.
- **`policynest_mvp/copilot_api/test_main.py`:** 14 contract tests, standard library only, model call stubbed (no key, no SDK). **All 14 pass.** They cover:
  - the corpus is applicant-safe;
  - browser passages are ignored;
  - the selfie question finds §4.6 with no fraud wording;
  - unknown context fields are dropped;
  - history is trimmed;
  - ID numbers are refused before a model call;
  - fraud wording and outcome predictions are replaced;
  - refusals give the fixed sentence;
  - `null` and unknown origins get 403;
  - bad bodies get 400;
  - a spoofed `X-Forwarded-For` does not reset the rate limit;
  - the daily cap;
  - health.

  Run: `python policynest_mvp/copilot_api/test_main.py`.
- **`CLAUDE.md`:** the proxy's new behaviour, the corpus rule, the tests and the deploy excludes are recorded under Deployment.

**Checked before deploying:**

- Retrieval spot-checks in Python on the shipped file: "my name is different on my marksheet" → Rulebook §9, §5, §4.4; "selfie failed twice" → §4.6, Rework spec §2.5, §3; "different person name" → §9, §5, Name-matching §2. None contains fraud wording.
- `site/kb.json` and `copilot_api/kb.json` are byte-identical.
- **A check in the browser pane could not run:** the pane was hidden and stuck on a site-permission check, so the Python check above stood in for it.

**Deployed (user's go, 15 Nov):**

1. **Proxy** `policynest-copilot`. The package held only `embarko.json`, `kb.json`, `main.py`, `requirements.txt` (no `.env`, caches or tests). Build status: live.
2. **Site** `policynest`: `site/` as built (index unchanged, new `kb.json`). Status: live.

**Live checks after deploy:**

| Check | Result |
|---|---|
| `GET /api/health` on the proxy | `{"ok": true, "llm": false, "model": "claude-opus-5-5", "daily_left": 50, "daily_cap": 50, "xff_hops": 2}` |
| `POST /api/copilot` with `Origin: null` | `403 origin_not_allowed` |
| `POST /api/copilot` from the live site's origin | `503 no_key` (expected: no key yet) |
| Live `kb.json` | 55 passages, all `applicant`, 0 fraud mentions, byte-identical to the local file |
| Live engine hash | matches `engine_sha256` in the evaluation results |

**Not checked live:**

- **An AI answer through the new lookup.** No key is set, and the server refuses before reaching the lookup. This path is covered only by the local tests.
- **T1–T10 in a browser.** The pane was hidden; the app page is byte-for-byte unchanged, and its engine hash matches.

## 4. What is live now

| Piece | State |
|---|---|
| Site `https://policynest.embarko.app` | 14 Nov app page (unchanged) with the 15 Nov applicant-safe `kb.json` |
| Proxy `https://policynest-copilot.embarko.app` | Pass 3 build; **AI answers off (no key)** |
| Engine | 3.4.0, hash `c5da9cfb…`, scores 600/600 in-sample on this hash |

## 5. Where to pick up

1. **User:** finish the planning review. Then, when ready, add `ANTHROPIC_API_KEY` in the `policynest-copilot` App setup tab at https://embarko.ai/app, and run one supervised round of real questions to check the guardrails live (PRD before-judging checklist).
2. **Pass 1** (accessibility and trust) is next in the plan. Its scope and requirement IDs are in PRD → "The confirmed plan". Two items in it are AI-proposed and still need confirming: FR-27 (reject-panel restart) and FR-38 (honest compliance ticks).
3. **Pass 2** (honest numbers), then the user's original list: queue data, the §4.6 two-selfie-failures rule, the held-out set, specimen prints and photo bench (optional), deck last.
4. **Human work before judging:** usability tests (5 + 2), the 20-case adoption, held-out labels, the deck (PRD checklist).

## 6. Open items and cautions

- **25 grill decisions are still AI-answered** (list in GRILL_LOG → "Still AI-answered").
- **Line endings:** git's `core.autocrlf` is on for this user, so it warns "LF will be replaced by CRLF". The engine hash normalises line endings, so this does not affect the evaluation check.
- **`PolicyNest.html` was not changed** in step 0 or pass 3. The first app-file change is pass 1. After it, re-check the engine hash, or re-run the evaluation if the engine block was touched.
- **Second autoresearch skill** at `~/.claude/skills/autoresearch` is still installed (RF-78).
- **No remote** is configured; nothing was pushed.
