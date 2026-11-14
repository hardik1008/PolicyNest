# MCP servers relevant to the PolicyNest MVP

Research date: 14 Nov 2026. Research only: nothing installed, signed up for or configured.
Data sources: GitHub REST API (`stargazers_count`, `pushed_at`) queried 14 Nov 2026 for the repos marked "GH API"; npm registry and PyPI JSON for release dates; the official MCP registry API (`registry.modelcontextprotocol.io/v0/servers?search=`) and the Claude connector directory (`search_mcp_registry`). After about 16 unauthenticated calls the GitHub API hit its rate limit (60 requests an hour), so some star counts come from a GitHub page fetch ("GH page") or are missing ("n/a").
"Verified" means the repo, package or registry entry and its date were checked against a primary source today. "Unverified" means it is known only from a directory or aggregator listing.
Constraint context: Node is NOT installed on this Windows machine, so every `npx` server needs Node first. Python/uvx and remote-hosted servers are flagged as "no Node". PolicyNest is a static page with no backend and a strict CSP, so none of these servers can run *inside* the app. They are either dev tooling for Claude or parts of a future backend.

## 1. Official modelcontextprotocol/servers repo: what is maintained and what is useful here

### Takeaway
Seven reference servers remain: Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking and Time. All were republished on 11 Nov 2026. Their own README calls them educational references, not production servers. Fetch and Git are Python (uvx) and run without Node. Filesystem and Memory need Node. SQLite, Puppeteer, Google Drive, PostgreSQL and the rest are archived.

### Cited Findings
- `modelcontextprotocol/servers`: 91,985 stars, last push 2026-11-12, not archived (GH API, Verified) — [GitHub API](https://api.github.com/repos/modelcontextprotocol/servers)
- Current reference servers are Everything, Fetch, Filesystem, Git, Memory, Sequential Thinking and Time. The README says they are "intended as reference implementations to demonstrate MCP features and SDK usage", not production-ready — [modelcontextprotocol/servers README](https://github.com/modelcontextprotocol/servers)
- Archived to `servers-archived`: AWS KB Retrieval, Brave Search, EverArt, GitHub, GitLab, Google Drive, Google Maps, PostgreSQL, **Puppeteer**, Redis, Sentry, Slack, **SQLite** — [README](https://github.com/modelcontextprotocol/servers). The `servers-archived` repo is archived, with its last push on 2025-05-28 (Verified) — [GitHub API](https://api.github.com/repos/modelcontextprotocol/servers-archived)
- `mcp-server-fetch` 2026.11.11 and `mcp-server-git` 2026.11.11 were both uploaded to PyPI on 2026-11-11 (Python, run with uvx, **no Node**, Verified) — [PyPI fetch](https://pypi.org/pypi/mcp-server-fetch/json), [PyPI git](https://pypi.org/pypi/mcp-server-git/json)
- `@modelcontextprotocol/server-filesystem` 2.3.0 (2026-11-11) and `@modelcontextprotocol/server-memory` 2.1.1 (2026-11-11) are on npm and **need Node** (Verified) — [npm filesystem](https://registry.npmjs.org/@modelcontextprotocol/server-filesystem), [npm memory](https://registry.npmjs.org/@modelcontextprotocol/server-memory)
- None of these need auth or cost anything. They are maintained by the official modelcontextprotocol project.

### Inferences
- **Fetch** (no Node) is useful for checking the live site, https://policynest.embarko.app, and CDN URLs. It cannot render JavaScript, so it does not test the app (E5).
- **Git** (no Node) matters only if the project becomes a git repo. Today it is not one.
- **Filesystem and Memory** add little. Claude Code already has its own file tools, and the project keeps context in CLAUDE.md and PRODUCT.md.
- The archived **SQLite** server should not be chosen for the eval CSVs. Use DuckDB/MotherDuck instead (section 6).
- Privacy: all run locally, so the DPDP fit is good. Avoid pointing Fetch or Memory at specimen documents in `05_SPECIMEN_DOCUMENTS/sample_specimens`, which may belong to real people.

### Gaps
- The README did not state the languages of Sequential Thinking and Time. Whether Time runs without Node was not verified.

## 2. Browser testing and accessibility (E5, D6 regression runs, §8 gap 2 usability prep, A9 theme checks)

### Takeaway
Microsoft Playwright MCP and Google's Chrome DevTools MCP are the two dominant, very active official servers, but both are Node (`npx`) packages. This Claude environment already has built-in browser tools (Claude Browser pane and Claude in Chrome), which cover most of what they would add without installing Node. For accessibility, Deque's axe MCP Server is commercial and sold through sales. The free options are community-built and Node-based.

### Cited Findings
| Server | Maintainer | Stars / last push | Latest release | Runtime | Auth / cost | Status |
|---|---|---|---|---|---|---|
| [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp) | Vendor official (Microsoft) | 39,625 / 2026-11-13 | `@playwright/mcp` 0.0.85, 2026-11-09 | Node (npx) | None / free, Apache-2.0 | Verified ([GH API](https://api.github.com/repos/microsoft/playwright-mcp), [npm](https://registry.npmjs.org/@playwright/mcp)) |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | Vendor official (Google Chrome DevTools team) | 55,918 / 2026-11-13 | `chrome-devtools-mcp` 1.13.0, 2026-11-11 | Node (npx) | None / free, Apache-2.0 | Verified ([GH API](https://api.github.com/repos/ChromeDevTools/chrome-devtools-mcp), [npm](https://registry.npmjs.org/chrome-devtools-mcp)) |
| [priyankark/lighthouse-mcp](https://github.com/priyankark/lighthouse-mcp) | Community; listed in the MCP Registry | 219 / 2026-11-13 | n/a | Node (npm `lighthouse-mcp`) | None / free, MIT | Verified (GH API) |
| [danielsogl/lighthouse-mcp-server](https://github.com/danielsogl/lighthouse-mcp-server) | Community; 13+ tools (performance, accessibility, SEO, security) | 75 / 2026-11-09 | n/a | Node (`npx @danielsogl/lighthouse-mcp`) | None / free, MIT | Verified (GH API) |
| [ronantakizawa/a11ymcp](https://github.com/ronantakizawa/a11ymcp) | Community; axe-core plus Puppeteer | 96 / 2026-03-10 | n/a | Node (JavaScript) | None / free, MIT | Verified (GH API) |
| [Deque axe MCP Server](https://www.deque.com/axe/mcp-server/) | Vendor official (Deque) | Closed source | Included in Axe DevTools for Web (blog, Feb 2026) | n/a | Paid Axe DevTools subscription; the docs say "talk to sales" | Unverified price ([Deque blog](https://www.deque.com/blog/axe-devtools-for-web-now-includes-axe-mcp-server-for-earlier-fixes-and-faster-delivery/), [Deque docs](https://docs.deque.com/devtools-server/4.0.0/en/axe-mcp-server)) |

- Deque's own claims: 20–30% fewer remediation hours in one case study and "40% faster" in another. These are vendor figures — [Deque case study](https://www.deque.com/axe-mcp-server-faster-accessibility-remediation/)
- Lighthouse MCP by priyankark wraps Google Lighthouse and is published to the MCP Registry — [awesome.ecosyste.ms listing](https://awesome.ecosyste.ms/projects/github.com%2Fpriyankark%2Flighthouse-mcp) (aggregator; GitHub data verified above)

### Inferences
- Without Node, the cheapest route is the browser tooling Claude already has in this session. CLAUDE.md's test recipe (drive `[data-act=...]` with JS, `DataTransfer` uploads) already works this way. Playwright or Chrome DevTools MCP would add repeatable scripted runs, Lighthouse/performance traces and CSP-violation logs (useful for the Embarko CSP issues), but only after Node is installed.
- An a11y audit of the bento UI in both themes (A9) could use the free axe-core-based community server or the Lighthouse accessibility category. Deque's commercial server conflicts with the "no paid keys" MVP stance.
- Privacy: these run locally against the public site with specimen data, so the DPDP fit is good. Do not run them on pages that hold real applicants' documents.

### Gaps
- No Python/uvx Playwright MCP from Microsoft was found. Python community ports were not searched.
- Deque's pricing is not public.

## 3. OCR and document AI (D6 OCR on real phone photos, D1/D2)

### Takeaway
For D6, local engines (Tesseract via `mcp-ocr`, PaddleOCR's official `paddleocr-mcp`) fit DPDP best and run on Python without Node. Cloud OCR servers (Mistral, Azure, AWS, Google) are all community-built or hosted by third parties, need API keys, and send PII documents to a foreign cloud. They suit benchmarking on synthetic or public datasets (MIDV-500) only. I found no official Textract, Document AI or Azure Document Intelligence MCP server.

### Cited Findings
| Server | Maintainer | Stars / last push | Release | Runtime | Auth / cost | Privacy fit | Status |
|---|---|---|---|---|---|---|---|
| [PaddleOCR `paddleocr-mcp`](https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/deployment/mcp_server.html) | Vendor official (PaddlePaddle); OCR and PP-StructureV3; local, AI Studio or self-hosted backends | Parent repo 92,693 / 2026-09-16 | PyPI 0.8.5, 2026-06-11 | Python, **no Node** | None for local / free, Apache-2.0 | Good when run locally | Verified ([GH API](https://api.github.com/repos/PaddlePaddle/PaddleOCR), [PyPI](https://pypi.org/pypi/paddleocr-mcp/json)) |
| [rjn32s/mcp-ocr](https://github.com/rjn32s/mcp-ocr) (Tesseract) | Community | 40 / 2026-06-08 | PyPI `mcp-ocr` 0.2.0, 2026-06-08 | Python, **no Node**; Tesseract binary needs manual steps on Windows | None / free, MIT | Good (local) | Verified (GH API, [PyPI](https://pypi.org/pypi/mcp-ocr/json)). PyPI metadata still has placeholder URLs ("yourusername"), so it is a small project. |
| [everaldo/mcp-mistral-ocr](https://github.com/everaldo/mcp-mistral-ocr) | Community | 40 / 2026-02-21 | n/a | Python or Docker | `MISTRAL_API_KEY` / paid Mistral API | Weak: documents go to Mistral's cloud | Verified (GH API) |
| [lemopian/mistral-ocr-mcp](https://github.com/lemopian/mistral-ocr-mcp) | Community | 8 / 2026-06-15 | n/a | Python (uv) | Mistral key | Weak | Verified (GH API) |
| [ORDIS-Co-Ltd/mistral-ocr-mcp](https://github.com/ORDIS-Co-Ltd/mistral-ocr-mcp) | Community | n/a | PyPI `mistral-ocr-mcp` 0.2.4, 2026-07-31 | Python | Mistral key | Weak | Release verified ([PyPI](https://pypi.org/pypi/mistral-ocr-mcp/json)); stars unverified |
| [awslabs `document-loader-mcp-server`](https://awslabs.github.io/mcp/servers/document-loader-mcp-server) | Vendor official (AWS Labs); document parsing, **not Textract** | Monorepo 9,919 / 2026-11-13 | PyPI 1.0.25, 2026-11-09 | Python, **no Node** | Not checked | Depends on configuration | Verified ([GH API](https://api.github.com/repos/awslabs/mcp), [PyPI](https://pypi.org/pypi/awslabs.document-loader-mcp-server/json)) |
| AWS Textract | No official awslabs server found. A ChatForest review says none exists; an Archestra catalog lists an unconfirmed Docker image | — | — | — | — | — | Unverified, sources conflict ([ChatForest](https://chatforest.com/reviews/ocr-document-intelligence-mcp-servers/), [Archestra](https://archestra.ai/mcp-catalog/awslabs__mcp)) |
| Azure Document Intelligence | Community only: `@kaenova/document-intelligence-mcp` (Node), Orion Vision | — | — | Node | Azure key | Weak | Unverified ([pkgstats](https://www.pkgstats.com/pkg:@kaenova/document-intelligence-mcp), [playbooks](https://playbooks.com/mcp/cognitive-stack-azure-form-recognizer)) |
| Google Document AI | No official Google server found. Activepieces offers a hosted third-party one | — | — | Remote | OAuth | Weak | Unverified ([Activepieces](https://www.activepieces.com/mcp/google-document-ai)) |
| Sarvam `sarvam-mcp` Document AI tools | Vendor official (Sarvam); Indic OCR parsing to markdown/JSON, schema extraction | See section 7 | PyPI 0.2.14, 2026-11-10 | Python, **no Node** | Sarvam key / paid | Indian vendor, but still a third-party cloud | Verified ([PyPI](https://pypi.org/pypi/sarvam-mcp/json), [docs](https://docs.sarvam.ai/api/developer-tools/mcp)) |

- Microsoft's `microsoft/mcp` (Azure MCP Server etc.) has 3,853 stars and a last push on 2026-11-14 (GH API, Verified) — [GitHub API](https://api.github.com/repos/microsoft/mcp). I did not check whether it exposes Document Intelligence.

### Inferences
- For D6 / §8 gap 3, the best fit is a local `paddleocr-mcp` or `mcp-ocr` (no Node, no key, no PII leaving the machine). Claude could use it to benchmark Tesseract.js output against a second engine on MIDV-500 or team-made photos. The app itself still has to stay on in-browser Tesseract.js because of the CSP and the no-backend design.
- Cloud OCR (Mistral, Azure, AWS) breaks the "no API keys" MVP decision. With real applicants it would send PAN and Aadhaar images to a third-party cloud. If ever used post-MVP, it needs Aadhaar masking *before* upload and a data processing agreement. Use it on synthetic data only.

### Gaps
- No accuracy figures for any OCR MCP server on Indian ID cards were found.
- The windows install burden of `paddleocr-mcp` (it needs the PaddlePaddle runtime) was not checked.

## 4. WhatsApp / SMS messaging (S1 conversational onboarding, F1 follow-up message)

### Takeaway
Meta has no official WhatsApp MCP server. Twilio's is the most credible vendor-backed option, but it is Node-only and its npm package has not been updated since July 2025. India-specific providers (MSG91, Gupshup) have no first-party MCP servers, only aggregator wrappers (Composio, viaSocket, Zapier). All of these are post-MVP backend pieces: they need keys, a WhatsApp Business account and approved templates, and they would carry applicants' phone numbers and names.

### Cited Findings
- **twilio-labs/mcp**: 114 stars, last push 2026-02-14, MIT (README text says ISC); `@twilio-alpha/mcp` 0.7.0, released 2025-07-07; run with `npx`, so **Node** is needed. It exposes "all of Twilio's API as MCP Tools", filterable with `--services`. Auth is Account SID plus API key and secret. The README warns against running community MCP servers alongside it because of injection risk (Verified) — [GH API](https://api.github.com/repos/twilio-labs/mcp), [npm](https://registry.npmjs.org/@twilio-alpha/mcp), [repo](https://github.com/twilio-labs/mcp)
- The Claude connector directory lists a **remote Twilio connector** (`mcp.twilio.com`) with only `twilio__search` / `twilio__retrieve` tools. It looks like docs or search access, not message sending. I could not fetch its docs page (HTTP 405), so this is Unverified — [Twilio MCP docs](https://mcp.twilio.com/docs)
- The Claude connector directory also lists **Bird** (remote, `mcp.bird.com`): "Send email, SMS, and WhatsApp…", with 300+ tools. It is a vendor-hosted remote server, so **no Node** (Unverified; seen only in the directory listing) — [Bird MCP](https://mcp.bird.com/)
- **lharries/whatsapp-mcp**: 6,879 stars, last push 2025-07-13, Go. It drives a *personal* WhatsApp account through the unofficial whatsmeow library rather than the Business API (Verified, GH API) — [GitHub API](https://api.github.com/repos/lharries/whatsapp-mcp)
- **nakulben/whatsapp-mcp**: Meta Cloud API templates and sends, Python; 4 stars, last push 2026-04-04 (Verified, GH API) — [GitHub API](https://api.github.com/repos/nakulben/whatsapp-mcp)
- Other community Cloud API servers: FredShred7/whatsapp-mcp-server (Node), Jem-HR/pywa-mcp-server (Python, PyWA), Gonzalez8/whatsapp-business-mcp (Docker, API-path whitelist). No dates or stars because of the rate limit (Unverified) — [Glama](https://glama.ai/mcp/servers/p8jhe2q40u), [LobeHub pywa](https://lobehub.com/it/mcp/jem-hr-pywa-mcp-server), [claudemarket](https://www.claudemarket.ai/mcp/Gonzalez8/whatsapp-business-mcp)
- The official MCP registry's "whatsapp" search returns mostly commercial remote servers (`ai.izap/whatsapp` with frequent versions, `ai.darkfunnels/whatsapp-sales-agent`). It has no Meta entry (Verified via the registry API) — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=whatsapp)
- **MSG91**: available only through third-party hosts (Composio, which says its MCP "will be deprecated soon"; viaSocket; Unified.to). **Gupshup**: no MCP server found, only Zapier-exposed actions — [Composio](https://mcp.composio.dev/msg91), [viaSocket](https://viasocket.com/mcp/msg91), [Zapier](https://zapier.com/apps/msg91/integrations/gupshup)

### Inferences
- For the MVP, F1 stays simulated. No messaging MCP server should be connected while the "no API keys" decision stands.
- For S1 post-MVP, the right architecture is a backend that calls the WhatsApp Business Platform (directly or through a BSP such as Twilio, Gupshup or MSG91) with approved templates. MCP would only help Claude prototype or send test messages. Avoid lharries/whatsapp-mcp: it uses an unofficial personal-account library, so it is unsuitable and likely against WhatsApp's terms for business messaging.
- DPDP: follow-up messages contain the applicant's name and the list of fixes, never Aadhaar. Templates should keep to that. Aggregators (Composio, viaSocket, Zapier) add another processor in the data path.

### Gaps
- Twilio's WhatsApp-sender support inside the MCP tool set was not confirmed.
- Pricing for Bird, iZap, Composio and viaSocket was not checked.

## 5. DigiLocker (S2 pull verified documents)

### Takeaway
I found no DigiLocker MCP server, official or community. The registry search for "digilocker" returned nothing. Integration goes through the OAuth 2.0 requester APIs (which need partner onboarding) or KYC aggregators.

### Cited Findings
- `registry.modelcontextprotocol.io/v0/servers?search=digilocker` returned zero servers (Verified, 14 Nov 2026) — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=digilocker)
- DigiLocker's requester APIs use OAuth 2.0 — [Requester API Specification v1.12 (API Setu)](https://cf-media.api-setu.in/resources/Requester-APISpecification-V1_12.pdf)
- An API directory lists a Digio MCP definition (`digio-mcp.yml`) for DigiKYC, which covers DigiLocker among other sources. It is unclear whether it exposes DigiLocker tools (Unverified) — [API Evangelist: Digio](https://providers.apievangelist.com/providers/digio/)
- Cashfree documents a DigiLocker verification API (a REST API, not MCP) — [Cashfree docs](https://www.cashfree.com/docs/secure-id/digilocker/digilocker.md)

### Inferences
- S2 is a backend job: a registered requester or a KYC aggregator, OAuth consent by the applicant, issued-document XML/PDF. MCP adds nothing until someone builds a wrapper, and a wrapper would hold Aadhaar-linked data, which is high DPDP risk.

### Gaps
- Whether the Digio MCP file is real and public was not confirmed.

## 6. Spreadsheet / data access for the eval CSVs (E2, E3, E4, §8 gap 4)

### Takeaway
MotherDuck's official `mcp-server-motherduck` is the best fit. It is Python/uvx (**no Node**), runs on a local in-memory DuckDB with no account or token, is read-only by default, is in the official registry, and was released on 11 Nov 2026. The archived SQLite reference server should be avoided.

### Cited Findings
- `mcp-server-motherduck` 1.1.1 was uploaded to PyPI on 2026-11-11. The official registry has `io.github.motherduckdb/mcp-server-motherduck` up to 1.0.8 as a PyPI package (Verified) — [PyPI](https://pypi.org/pypi/mcp-server-motherduck/json), [registry](https://registry.modelcontextprotocol.io/v0/servers?search=duckdb)
- 540 stars (GH page). It runs with `uvx mcp-server-motherduck --db-path :memory:` and needs no MotherDuck token. Write access is off unless `--read-write` is passed (Verified, GH page) — [repo](https://github.com/motherduckdb/mcp-server-motherduck)
- The SQLite reference server is archived — [modelcontextprotocol/servers README](https://github.com/modelcontextprotocol/servers)
- Not checked because of the rate limit: `haris-musa/excel-mcp-server` and `xing5/mcp-google-sheets` (community; Google Sheets needs Google OAuth) — Unverified.

### Inferences
- With DuckDB, Claude can run SQL over `eval/out/*.csv` and the datasets in `02_…`/`04_…` (DuckDB reads CSV natively through `read_csv_auto`; the MCP README does not mention CSV explicitly) for fairness slices (E3) and the simulation (E4), all locally. The DPDP fit is good because the data is synthetic and stays local.
- Python is already used (`eval/simulate.py`, `embed.py`), so plain pandas or duckdb in Python may be just as good with no MCP at all.

### Gaps
- Stars and last-commit dates for the Excel and Google Sheets servers.

## 7. Hindi translation / transliteration (§8 gap 5 Hindi pop-ups and UI; F1 Hindi follow-up)

### Takeaway
Sarvam AI's official `sarvam-mcp` (Python/uvx, **no Node**, PyPI 0.2.14 on 2026-11-10) covers Indic translation, transliteration and Indic OCR. It is the strongest India-specific option. DeepL has an official server (Node) and a remote hosted one. Neither page confirmed Hindi support, and DeepL's Hindi support was not checked. No AI4Bharat/IndicTrans MCP server was found. All need keys. For static UI strings, a one-off translation during development carries no applicant PII.

### Cited Findings
- **Sarvam `sarvam-mcp`** (vendor official): install with `uvx sarvam-mcp` or `pip install sarvam-mcp`, Python 3.11+, Windows supported. Needs `SARVAM_API_KEY`. Tools: translation (`mayura:v1`, `sarvam-translate:v1`), transliteration, language ID, STT/TTS, Document AI parsing, document translation. The docs page states no pricing or data retention terms — [Sarvam docs](https://docs.sarvam.ai/api/developer-tools/mcp), [PyPI](https://pypi.org/pypi/sarvam-mcp/json) (repo `github.com/sarvamai/sarvam-mcp`; stars not retrieved, rate limited)
- Sarvam also runs a docs-search remote MCP at `https://docs.sarvam.ai/_mcp/server` (no key for docs) and a Voice Agents remote MCP at `https://mcp.sarvam.ai/voice-agents` (Unverified; from search summary) — [Sarvam conversations MCP](https://docs.sarvam.ai/conversations/mcp)
- **DeepL `deepl-mcp-server`** (vendor official, DeepL org): 120 stars (GH page), MIT. npm 1.3.15, 2026-10-14. Needs Node 18+ and `DEEPL_API_KEY`. Tools translate-text, translate-document, rephrase-text, glossaries. The README recommends DeepL's **remote MCP server** (sign in with a DeepL account, **no Node**) — [repo](https://github.com/DeepLcom/deepl-mcp-server), [npm](https://registry.npmjs.org/deepl-mcp-server)
- The official registry's "deepl" search shows only `io.github.pipeworx-io/deepl` (a third-party gateway), not DeepL's own entry (Verified) — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=deepl)
- Registry search for "sarvam" returned nothing, so Sarvam is not in the official registry, although it is on PyPI (Verified) — [registry](https://registry.modelcontextprotocol.io/v0/servers?search=sarvam)
- Community Sarvam wrappers exist (npm `sarvam-mcp-server`, safayavatsal/Sarvam-MCP). One Glama listing says it is unaffiliated (Unverified) — [Glama](https://glama.ai/mcp/servers/safayavatsal/Sarvam-MCP)

### Inferences
- For §8 gap 5 (Hindi pop-ups and UI), the low-risk path is to translate the fixed English string table once during development (Sarvam's "string-table localization" workflow fits) and have a native Hindi speaker review it. Then hard-code the strings. The live app makes no runtime calls and sends no PII.
- The `cheer` toasts contain the applicant's first name. Translate templates with placeholders, never real names.

### Gaps
- Sarvam pricing, free credits, data retention and residency are not stated on the MCP page.
- Whether DeepL supports Hindi was not confirmed in this research.
- No Google Translate official MCP server and no AI4Bharat IndicTrans MCP server were found. A self-hosted IndicTrans2 would need a custom wrapper. AI4Bharat/IndicTrans2 repo stats were not retrieved because of the rate limit.

## Mapping summary (goal ID or §8 gap → best candidate)

### Takeaway
The servers worth considering now, with no Node and no keys, are Fetch, MotherDuck/DuckDB (local), and paddleocr-mcp or mcp-ocr (local). The browser tools built into this environment cover testing. Everything else is post-MVP and needs keys plus a DPDP review.

### Cited Findings
| Goal / gap | Candidate | Now or post-MVP | Node needed? | Keys? |
|---|---|---|---|---|
| E5 / A9 / §8-2 test runs | Built-in Claude browser tools; Playwright MCP; Chrome DevTools MCP; Lighthouse MCP | Now (built-in); MCPs once Node is installed | Yes for the MCPs | No |
| D6 / §8-3 phone-photo OCR benchmark | `paddleocr-mcp`, `mcp-ocr` (local) | Now (dev only) | No | No |
| D6 cloud comparison | Mistral OCR MCP, Sarvam Document AI | Synthetic data only | No | Yes |
| E2–E4 / §8-4 eval data | `mcp-server-motherduck` (local DuckDB) | Now | No | No |
| §8-5 Hindi UI, F1 | `sarvam-mcp`; DeepL remote | Dev-time string translation | No | Yes |
| S1 WhatsApp | Twilio MCP (Node); Bird (remote); community Cloud API servers | Post-MVP | Varies | Yes |
| S2 DigiLocker | None exists | Post-MVP, backend | — | — |
| R6 reviewer queue | No MCP needed (app feature) | — | — | — |

Sources: as cited in sections 1–7.

### Inferences
- R6 (multi-case queue) and R7 (redesign) are app features. No MCP server addresses them.

### Gaps
- GitHub stars and push dates for Jem-HR/pywa-mcp-server, haris-musa/excel-mcp-server, xing5/mcp-google-sheets, googleapis/genai-toolbox, sarvamai/sarvam-mcp and AI4Bharat/IndicTrans2 were not retrieved, because the GitHub API's unauthenticated rate limit was hit.
