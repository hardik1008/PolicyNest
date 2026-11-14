# Build with dev tools, ship almost nothing

*Research synthesis, 14 Nov 2026. Built from four research-note files in `research_notes/PolicyNest integrations research/`, mapped to the goal IDs and §8 gap list in `PRODUCT.md`. Nothing was installed, signed up for or connected while researching. "Verified" means a researcher saw the live page, repo, registry entry or an HTTP probe result on 14 Nov 2026. "Unverified" means it was seen only in a directory, a search snippet, a marketing page or a third-party write-up. Where a note said "partly verified" (vendor docs seen only as a search snippet), this report marks it **Unverified (partial)**.*

## 1. Summary

The most useful integrations for PolicyNest right now are **developer tools, not things shipped to applicants**. The top gaps in `PRODUCT.md` §8 are usability tests, the reviewer queue (blocked on review-console references), OCR on real phone photos, a held-out labelled set, the missing discovery-call notes and an executive presentation. No connector or API closes any of them on its own. Free Claude plugins and connectors do make them cheaper: the knowledge-work `design` plugin for usability-test synthesis, Google Sheets/Drive for score and labelling sheets, Canva (already connected) for the deck, the Python `webapp-testing` skill and the built-in browser for scripted test runs, and Hugging Face plus local OCR servers for the phone-photo benchmark ([design README](https://github.com/anthropics/knowledge-work-plugins/tree/main/design), [webapp-testing SKILL.md](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md)). Only a few public APIs can run inside the static site under its CSP with no key. The researchers probed these with the site's origin header and got `Access-Control-Allow-Origin` back: **Razorpay IFSC** (a real partial bank check), **api.postalpincode.in** (pincode to state), and **libphonenumber-js** from jsDelivr (mobile format) ([Razorpay IFSC probe](https://ifsc.razorpay.com/HDFC0000001), [postalpincode probe](https://api.postalpincode.in/pincode/110001)). The four simulated checks (PAN, penny-drop name, face match and the IRDAI registry) **must stay simulated in the MVP**. Every Indian KYC vendor checked uses a long-lived secret that has to sit on a server ([Sandbox.co.in auth](https://developer.sandbox.co.in/api-reference/authenticate), [HyperVerge auth](https://documentation.hyperverge.co/other-resources/authentication)). No public IRDAI POSP registry API was found, and DigiLocker needs registered-partner onboarding ([API Setu DigiLocker](https://apisetu.gov.in/digilocker)). The one route that could turn a simulated check into a real one with no key and no server is verifying a UIDAI-signed Aadhaar Secure QR or offline XML in the browser. It is legally unsettled until someone reads the December 2025 amendment, so treat it as a demo on synthetic data only.

## 2. Top 10 shortlist (impact on PRODUCT.md gaps ÷ effort)

Ranked so that the items at the top close a higher-priority §8 gap for the least work. Effort is judged from the notes: one install or an already-connected connector counts as low.

| Rank | Candidate | Category | Closes | Effort | Tier | Status | Link |
|---|---|---|---|---|---|---|---|
| 1 | `design` plugin (knowledge-work-plugins): `/research-synthesis`, `/critique`, `/accessibility`, `/ux-copy` | Plugin | §8 gap 1 (five applicants, two reviewers); R7 critique; S4 copy | One install, free | Dev | Verified | [README](https://github.com/anthropics/knowledge-work-plugins/tree/main/design) |
| 2 | Google Sheets connector, with Google Drive (already connected) | Connector | §8 gap 1 (clarity score sheet); §8 gap 4 (held-out labelling sheet) | Low; Drive is already on, Sheets needs a sign-in | Dev | Verified (registry) | [Sheets MCP](https://sheetsmcp.googleapis.com/mcp/v1), [Drive MCP](https://drivemcp.googleapis.com/mcp/v1) |
| 3 | Canva connector (already connected) | Connector | §8 gap 6 (executive presentation, 10% of the rubric); R7 references if they are in Canva | Very low | Dev | Verified (registry; connected) | [Canva MCP](https://mcp.canva.com/mcp) |
| 4 | `webapp-testing` skill (Python Playwright) plus the built-in Claude browser tools | Plugin/skill | T1–T10 regression; §8 gap 3 (scripted phone-photo uploads); E5 checks; scripted runs before gap 1 | Low; `pip install playwright`, no Node needed | Dev | Verified | [SKILL.md](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md) |
| 5 | Hugging Face connector or `huggingface-skills` | Connector/plugin | §8 gap 3 / D6: find public ID-document photo datasets (MIDV-500-type) | Low; HF account optional | Dev | Verified | [HF MCP](https://huggingface.co/mcp), [huggingface/skills](https://github.com/huggingface/skills) |
| 6 | Razorpay IFSC API (`ifsc.razorpay.com/{IFSC}`) | Public API | C3: a real partial bank check (branch exists, IMPS flag), alongside the simulated penny-drop name | Low; one `fetch`, 404 on bad codes | **Now** (ships) | Verified (probe: 200/404, ACAO `*`) | [probe](https://ifsc.razorpay.com/HDFC0000001), [repo](https://github.com/razorpay/ifsc) |
| 7 | `frontend-design` (already loaded) plus a Figma connector if the references are in Figma | Plugin/connector | R7 review-console redesign, which unblocks R6 / §8 gap 2 | Low, once the references arrive | Dev | Verified | [frontend-design](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design), [Figma MCP](https://mcp.figma.com/mcp) |
| 8 | `paddleocr-mcp` or `mcp-ocr` (local, Python) | MCP server | §8 gap 3 / D6: benchmark Tesseract.js against a second engine on public or team-made photos, with nothing leaving the machine | Medium; the PaddlePaddle runtime and the Tesseract binary on Windows are extra steps | Dev | Verified | [paddleocr-mcp docs](https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/deployment/mcp_server.html), [mcp-ocr](https://github.com/rjn32s/mcp-ocr) |
| 9 | `security-guidance` plugin | Plugin | §7 guardrails (no full Aadhaar, no secrets, XSS in a single-file app) | One install | Dev | Verified (catalog) | [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) |
| 10 | libphonenumber-js at an exact version from jsDelivr | Public library on a CDN | A2: Indian mobile-number format check on the device, with no network call per number | Low | **Now** (ships) | Verified (CDN probe: 200, ACAO `*`) | [jsDelivr file](https://cdn.jsdelivr.net/npm/libphonenumber-js@1.11.4/bundle/libphonenumber-min.js), [repo](https://github.com/catamphetamine/libphonenumber-js) |

Just outside the top 10: the **Embarko connector** for redeploys (E5) without handling the token in the shell ([Embarko MCP](https://mcp.viasocket.com/mcp/6aa6e50e3f46d251d268bd9d-75344), Verified listing). **MotherDuck/DuckDB MCP** for SQL over `eval/out/*.csv` (E2–E4, §8 gap 4) ([repo](https://github.com/motherduckdb/mcp-server-motherduck), Verified), though plain Python duckdb or pandas would do the same job. **api.postalpincode.in** for a pincode-to-state hint (A2, T9 information only) ([probe](https://api.postalpincode.in/pincode/110001), Verified, maintainer unknown).

Nothing on any list closes **§8 gap 5 (discovery-call notes)**. Those notes can only come from the problem owner. **R6 (multi-case queue)** is build work in the app; no tool does it for you.

## 3. Candidates by category

Column notes. "CSP/CORS fit" is about the live site: connect-src https only, no `blob:`/`data:` fetches, no server. Dev tools never run inside the site, so for them it reads "n/a (dev only)". "Cost" is what the notes found; anything not stated is "not published" or "not checked". Stars and dates come from the GitHub API, npm or PyPI on 14 Nov 2026, as recorded in the notes. Unauthenticated GitHub API calls hit their rate limit partway through, so some counts are "not fetched".

### 3a. Claude connectors and Claude Code plugins

| Name | What it does for PolicyNest | Goal ID | Auth | CSP/CORS fit | Cost | Status | Link |
|---|---|---|---|---|---|---|---|
| `design` (knowledge-work-plugins) | `/research-synthesis` for usability-test notes; `/accessibility` (WCAG 2.1 AA review); `/critique`; `/ux-copy` | §8 gap 1, R7, S4 | none | n/a (dev only) | Free to install | Verified | [README](https://github.com/anthropics/knowledge-work-plugins/tree/main/design) |
| `webapp-testing` skill (anthropics/skills) | Python Playwright scripts that drive the site, e.g. T1–T10 and upload tests | T1–T10, D6, §8 gap 3, E5 | none | n/a (dev only) | Free | Verified | [SKILL.md](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md) |
| `playwright` plugin (Microsoft MCP) | Same as above, as an MCP server; runs `npx @playwright/mcp@latest` | T1–T10, D6 | none | n/a (dev only) | Free, Apache-2.0 | Verified; **needs Node** | [entry](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright) |
| `chrome-devtools-mcp` | Console, network and performance traces; good for debugging Embarko CSP and worker-loading errors | E5, D1 | none | n/a (dev only) | Free, Apache-2.0 | Verified; probably needs Node (unverified) | [repo](https://github.com/ChromeDevTools/chrome-devtools-mcp) |
| `frontend-design` | Distinctive UI work; already loaded in this environment | R7, A5, A9 | none | n/a (dev only) | Free | Verified | [entry](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design) |
| `security-guidance` | Warns on risky edits; reviewer for XSS, secrets and 25+ other checks | §7 guardrails, D5 | none | n/a (dev only) | Free | Verified (catalog) | [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) |
| `code-review`, `pr-review-toolkit` | Review the engine block before each rule change | C1–C5, E2 | none | n/a (dev only) | Free | Verified (catalog); work best once the project is a git repo | [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) |
| `playground` | Single-file HTML explorers for prototyping the R6 queue layout | R6, R7 | none | n/a (dev only) | Free | Verified (catalog) | [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) |
| `claude-md-management`, `project-artifact` | Keep CLAUDE.md and PRODUCT.md current; a shareable status page to replace the lost status note | E1 (docs hygiene) | none | n/a (dev only) | Free | Verified (catalog) | [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) |
| `huggingface-skills` / Hugging Face connector | Dataset, model and paper search for ID-document photo sets | D6, §8 gap 3 | Optional HF account | n/a (dev only) | Not checked | Verified | [skills repo](https://github.com/huggingface/skills), [HF MCP](https://huggingface.co/mcp) |
| `context7` | Current Tesseract.js 5 / pdf.js 3.11 docs; hosted, no Node | D1 | Not checked (unverified) | n/a (dev only) | Free-tier terms not checked | Verified (catalog) | [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) |
| `deepeval` | Eval datasets and reports | §8 gap 4 | Account for its reporting service (unverified) | n/a (dev only) | Not checked | Verified (catalog); **weak fit**: the engine is rule-based, not an LLM | [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) |
| Embarko connector | `deploy_app`; redeploy without curl or the token | E5 | Account sign-in (type unverified) | n/a (deploys the site) | Not published | Verified (registry) | [Embarko MCP](https://mcp.viasocket.com/mcp/6aa6e50e3f46d251d268bd9d-75344) |
| Canva connector | Executive deck and demo assets; R7 references if made in Canva | §8 gap 6, R7 | OAuth | n/a (dev only) | Not checked | Verified; **already connected** | [Canva MCP](https://mcp.canva.com/mcp) |
| Figma connector / `figma` plugin | Read the review-console references into code | R7 → R6 | OAuth (inferred, unconfirmed) | n/a (dev only) | Not checked | Verified (registry) | [Figma MCP](https://mcp.figma.com/mcp), [figma/mcp-server-guide](https://github.com/figma/mcp-server-guide) |
| Google Drive / Google Sheets connectors | Usability score sheet; held-out labelling sheet; sharing eval CSVs | §8 gaps 1 and 4, E2 | OAuth | n/a (dev only) | Not checked | Verified; Drive **already connected** | [Drive MCP](https://drivemcp.googleapis.com/mcp/v1), [Sheets MCP](https://sheetsmcp.googleapis.com/mcp/v1) |
| Notion, Linear connectors | Hold discovery-call notes once they exist; track the §8 list | §8 gap 5 (storage only) | OAuth (inferred) | n/a (dev only) | Not checked | Verified (registry) | [Notion MCP](https://mcp.notion.com/mcp), [Linear MCP](https://mcp.linear.app/mcp) |
| BrowserStack connector | Accessibility audits; testing on real phones | D6, A9 | Account (paid service, unverified) | n/a (dev only) | Paid (price not published in notes) | Verified (registry) | [BrowserStack MCP](https://mcp.browserstack.com/mcp) |
| LILT, Smartling connectors | Translation of UI strings with human review | S4 | Paid accounts (unverified) | n/a (dev only) | Not published | Verified (registry) | [LILT MCP](https://mcp.lilt.com/mcp), [Smartling MCP](https://mcp.smartling.com/mcp) |
| `twilio-developer-kit` / Twilio docs connector | Skills and docs for SMS and WhatsApp | S1, F1 (real sending) | API key (Twilio account) | Needs a server | Not checked | Verified (catalog); docs-only connector unverified | [twilio/ai](https://github.com/twilio/ai), [Twilio MCP docs](https://mcp.twilio.com/docs) |
| Sentry, Supabase, Cloudflare, Vercel, Netlify connectors | Error monitoring; storage for a future queue; hosting alternatives | R6 (post-MVP storage), E5 | OAuth / DSN key | Each adds a backend or a key | Not checked | Verified (registry) | [Sentry](https://mcp.sentry.dev/mcp), [Supabase](https://mcp.supabase.com/mcp), [Cloudflare](https://bindings.mcp.cloudflare.com/mcp), [Vercel](https://mcp.vercel.com/), [Netlify](https://mcp.netlify.com/mcp) |

Maintainers and repo stats from the notes: Anthropic maintains `design`, `webapp-testing`, `frontend-design`, `security-guidance`, `code-review`, `playground` and `claude-md-management`. **claude-plugins-official** has 47,255 stars, last push 2026-11-14, 317 plugin entries ([GitHub API](https://api.github.com/repos/anthropics/claude-plugins-official)). **knowledge-work-plugins** has 35,712 stars, last push 2026-11-13. **anthropics/skills** has 194,361 stars, last push 2026-11-14. **microsoft/playwright-mcp** has 39,625 stars, last push 2026-11-13. **ChromeDevTools/chrome-devtools-mcp** (Google Chrome DevTools team) has 55,918 stars, last push 2026-11-13. **huggingface/skills** has 11,346 stars, last push 2026-11-13. **figma/mcp-server-guide** has 2,185 stars, last push 2026-11-13. **canva-sdks/canva-skills** has 162 stars, last push 2026-11-11. **twilio/ai** has 41 stars, last push 2026-11-11. Stars were not fetched for `context7`, `deepeval`, `superpowers` and `modern-web-guidance`. The Embarko connector's maintainer is not stated; the viasocket.com URL suggests viaSocket runs it (unverified). No install counts were found: the marketplace page showed none ([Claude Marketplace](https://claude.com/marketplace/plugins)). The official catalog has **no plugin for OCR, DigiLocker, Aadhaar/KYC or translation**, and the registry has no DigiLocker or WhatsApp connector.

### 3b. MCP servers

| Name | What it does for PolicyNest | Goal ID | Auth | CSP/CORS fit | Cost | Status | Link |
|---|---|---|---|---|---|---|---|
| `paddleocr-mcp` (PaddlePaddle, official) | Local OCR and layout engine to benchmark against Tesseract.js | D6, §8 gap 3 | none (local) | n/a (dev only; the app keeps Tesseract.js) | Free, Apache-2.0 | Verified | [docs](https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/deployment/mcp_server.html), [PyPI](https://pypi.org/pypi/paddleocr-mcp/json) |
| `mcp-ocr` (rjn32s, community, Tesseract) | Local Tesseract OCR from Claude | D6, §8 gap 3 | none | n/a (dev only) | Free, MIT | Verified; a small project (placeholder URLs in its PyPI metadata) | [repo](https://github.com/rjn32s/mcp-ocr), [PyPI](https://pypi.org/pypi/mcp-ocr/json) |
| `mcp-server-motherduck` (MotherDuck, official) | Local DuckDB SQL over the eval CSVs; read-only by default; no token | E2, E3, E4, §8 gap 4 | none (local, `:memory:`) | n/a (dev only) | Free | Verified | [repo](https://github.com/motherduckdb/mcp-server-motherduck), [PyPI](https://pypi.org/pypi/mcp-server-motherduck/json) |
| `mcp-server-fetch` (MCP reference) | Check the live site and CDN URLs; does not run JavaScript | E5 | none | n/a (dev only) | Free | Verified | [PyPI](https://pypi.org/pypi/mcp-server-fetch/json), [repo](https://github.com/modelcontextprotocol/servers) |
| `mcp-server-git` (MCP reference) | Git operations, useful only once the project becomes a repo | (tooling) | none | n/a (dev only) | Free | Verified | [PyPI](https://pypi.org/pypi/mcp-server-git/json) |
| Filesystem / Memory (MCP reference) | Little added; Claude Code already has file tools | none | none | n/a (dev only) | Free | Verified; need Node | [npm filesystem](https://registry.npmjs.org/@modelcontextprotocol/server-filesystem), [npm memory](https://registry.npmjs.org/@modelcontextprotocol/server-memory) |
| `@playwright/mcp` (Microsoft) | Scripted browser runs | T1–T10, D6 | none | n/a (dev only) | Free, Apache-2.0 | Verified; **needs Node** | [repo](https://github.com/microsoft/playwright-mcp), [npm](https://registry.npmjs.org/@playwright/mcp) |
| `chrome-devtools-mcp` (Google) | CSP violation logs, performance traces | E5, D1 | none | n/a (dev only) | Free, Apache-2.0 | Verified; **needs Node** | [repo](https://github.com/ChromeDevTools/chrome-devtools-mcp), [npm](https://registry.npmjs.org/chrome-devtools-mcp) |
| Lighthouse MCP servers (priyankark; danielsogl) | Accessibility, performance and best-practice audits of both themes | A9, accessibility | none | n/a (dev only) | Free, MIT | Verified; need Node | [priyankark](https://github.com/priyankark/lighthouse-mcp), [danielsogl](https://github.com/danielsogl/lighthouse-mcp-server) |
| `a11ymcp` (ronantakizawa) | axe-core accessibility checks | A9 | none | n/a (dev only) | Free, MIT | Verified; needs Node | [repo](https://github.com/ronantakizawa/a11ymcp) |
| Deque axe MCP Server | Commercial accessibility server | A9 | Paid subscription | n/a (dev only) | "Talk to sales" (not published) | Unverified (price) | [Deque](https://www.deque.com/axe/mcp-server/) |
| `sarvam-mcp` (Sarvam, official) | Indic translation, transliteration and Indic document parsing | S4 (dev-time string table) | API key | n/a (dev only; never at runtime) | Not published | Verified | [docs](https://docs.sarvam.ai/api/developer-tools/mcp), [PyPI](https://pypi.org/pypi/sarvam-mcp/json) |
| `deepl-mcp-server` (DeepL, official) | Translation; DeepL recommends its remote server (no Node) | S4 | API key / DeepL account | n/a (dev only) | Not checked | Verified; **Hindi support not confirmed** | [repo](https://github.com/DeepLcom/deepl-mcp-server) |
| Mistral OCR MCP servers (everaldo; lemopian; ORDIS) | Cloud OCR comparison | D6 (synthetic data only) | API key | Sends documents to a foreign cloud | Paid Mistral API | Verified (repos) | [everaldo](https://github.com/everaldo/mcp-mistral-ocr), [lemopian](https://github.com/lemopian/mistral-ocr-mcp), [ORDIS PyPI](https://pypi.org/pypi/mistral-ocr-mcp/json) |
| awslabs `document-loader-mcp-server` | Document parsing (not Textract) | D1 (comparison) | Not checked | n/a (dev only) | Not checked | Verified | [docs](https://awslabs.github.io/mcp/servers/document-loader-mcp-server) |
| `twilio-labs/mcp` | All Twilio APIs as tools | S1, F1 | API key + secret | Needs a server for real use | Not checked | Verified; needs Node; npm last released 2025-07-07 | [repo](https://github.com/twilio-labs/mcp), [npm](https://registry.npmjs.org/@twilio-alpha/mcp) |
| Bird (remote) | Email, SMS and WhatsApp sending | S1, F1 | Account | Needs a server | Not checked | Unverified (directory listing only) | [Bird MCP](https://mcp.bird.com/) |
| `lharries/whatsapp-mcp` | Drives a *personal* WhatsApp account through an unofficial library | **Avoid** | n/a | n/a | n/a | Verified (repo); unsuitable for business use | [GitHub API](https://api.github.com/repos/lharries/whatsapp-mcp) |
| DigiLocker MCP | None exists | S2 | n/a | n/a | n/a | Verified (zero results) | [registry search](https://registry.modelcontextprotocol.io/v0/servers?search=digilocker) |

Maintainers and repo stats from the notes: **modelcontextprotocol/servers** has 91,985 stars, last push 2026-11-12. Its README calls the seven remaining servers reference implementations, not production servers, and lists SQLite and Puppeteer as archived ([README](https://github.com/modelcontextprotocol/servers)). `mcp-server-fetch` and `mcp-server-git` 2026.11.11 were released 2026-11-11 and run on Python with no Node. **PaddleOCR** has 92,693 stars, last push 2026-09-16; `paddleocr-mcp` 0.8.5 was released 2026-06-11. **mcp-ocr** has 40 stars; 0.2.0 was released 2026-06-08. **mcp-server-motherduck** has 540 stars; 1.1.1 was released 2026-11-11. **playwright-mcp** 0.0.85 was released 2026-11-09. **chrome-devtools-mcp** 1.13.0 was released 2026-11-11. **priyankark/lighthouse-mcp** has 219 stars, last push 2026-11-13. **danielsogl/lighthouse-mcp-server** has 75 stars, last push 2026-11-09. **a11ymcp** has 96 stars, last push 2026-03-10. **sarvam-mcp** 0.2.14 was released 2026-11-10; stars not fetched, and it is not in the official registry. **deepl-mcp-server** has 120 stars; 1.3.15 was released 2026-10-14. **everaldo/mcp-mistral-ocr** has 40 stars, last push 2026-02-21. **twilio-labs/mcp** has 114 stars, last push 2026-02-14. **lharries/whatsapp-mcp** has 6,879 stars, last push 2025-07-13. **awslabs/mcp** has 9,919 stars; document-loader 1.0.25 was released 2026-11-09. No official AWS Textract, Google Document AI or Azure Document Intelligence MCP server was found ([ChatForest review](https://chatforest.com/reviews/ocr-document-intelligence-mcp-servers/), Unverified; sources conflict).

### 3c. Public APIs and libraries the static site could call

All probes sent `Origin: https://policynest.embarko.app` and used non-personal sample values only.

| Name | What it does for PolicyNest | Goal ID | Auth | CSP/CORS fit | Cost | Status | Link |
|---|---|---|---|---|---|---|---|
| Razorpay IFSC API | Confirms the IFSC read from the cheque exists; returns bank, branch, state and IMPS/UPI flags; 404 on a bad code | C3 (bank), A2 | none | **Good**: HTTPS, ACAO `*` | Free; no rate limit or SLA published | Verified (probe 200 and 404) | [probe](https://ifsc.razorpay.com/HDFC0000001), [404 probe](https://ifsc.razorpay.com/XXXX0000000) |
| razorpay/ifsc dataset via jsDelivr | Offline IFSC existence list if the API is down | C3 | none | Good (ACAO `*` on jsDelivr) | Free, MIT | Partly verified: README served; the dataset path and size were not checked | [jsDelivr probe](https://cdn.jsdelivr.net/gh/razorpay/ifsc@latest/README.md), [releases](https://api.github.com/repos/razorpay/ifsc/releases/latest) |
| api.postalpincode.in | Pincode to district and state, as a soft hint against the address state (information only, like T9) | A2, C3 (T9) | none | Good on **https only** (http returns 403) | Free; no limits published | Verified (probe) | [probe](https://api.postalpincode.in/pincode/110001) |
| Zippopotam.us (IN) | Backup pincode lookup with coarser data; labels Delhi "New Delhi" | A2 | none | Good (ACAO `*`) | Free | Verified (probe) | [probe](https://api.zippopotam.us/IN/110001) |
| libphonenumber-js (jsDelivr, exact version) | Indian mobile-number format check, all on the device | A2 | none | Good (a script from an allowed CDN) | Free, MIT | Verified (CDN probe) | [file](https://cdn.jsdelivr.net/npm/libphonenumber-js@1.11.4/bundle/libphonenumber-min.js), [npm latest](https://registry.npmjs.org/libphonenumber-js/latest) |
| Kickbox Open / UserCheck | Disposable-email-domain check (send the domain only) | A2 (low value) | none | Good (origin reflected / ACAO `*`) | Free; limits not checked | Verified (probe) | [Kickbox](https://open.kickbox.com/v1/disposable/example.com), [UserCheck](https://api.usercheck.com/domain/example.com) |
| Google Input Tools | English-to-Devanagari transliteration | S4 | none | Works (ACAO `*`) | No terms found | Verified that it works; **undocumented, no terms of use** | [probe](https://inputtools.google.com/request?text=namaste&itc=hi-t-i0-und&num=3) |
| MyMemory | en→hi translation with an anonymous quota | S4 | none | Works (ACAO `*`) | Quota not confirmed | Verified; output noisy (crowd-sourced junk matches) | [probe](https://api.mymemory.translated.net/get?q=hello&langpair=en|hi) |
| LibreTranslate public instance | Translation | S4 | **API key now required** | Preflight passes, but POST needs a key | Not checked; self-host is AGPL-3.0 | Verified (key required) | [probe](https://libretranslate.com/translate), [repo](https://github.com/LibreTranslate/LibreTranslate) |
| AI4Bharat xlit API | Transliteration | S4 | n/a | **Host does not resolve** | n/a | Verified unavailable | [IndicXlit repo](https://github.com/AI4Bharat/IndicXlit) |
| OCR.space | Remote OCR | D1 | API key | CORS-open, but uploads identity documents | Free tier not checked | Verified (CORS); **poor DPDP fit; do not use** | [probe](https://api.ocr.space/parse/imageurl?apikey=helloworld&url=https://example.com/x.png) |
| tesseract.js (current OCR) | On-device OCR already in the app | D1 | none | Already working via same-origin shims | Free, Apache-2.0 | Verified | [GitHub API](https://api.github.com/repos/naptha/tesseract.js) |
| India Public Holidays API (onrender) | Central and state holidays for SLA day counting | E4 (simulation) | none | Works (ACAO `*`); cold starts on free hosting | Free | Verified (CORS); reliability unknown | [docs](https://calendar-api-web.vercel.app/docs) |
| caldays.com, holidayexplore.com | India holidays for 2026 | E4 | none | Works (ACAO `*`) | Free | Verified (CORS); **the sources disagree** | [caldays](https://caldays.com/api/holidays/in), [HolidayExplore](https://holidayexplore.com/api/v1/holidays?country=IN&year=2026) |
| Nager.Date, OpenHolidays | Holidays | E4 | none | ACAO `*` | Free | Verified: **no India data** (204 and `[]`) | [Nager probe](https://date.nager.at/api/v3/PublicHolidays/2026/IN), [OpenHolidays probe](https://openholidaysapi.org/PublicHolidays?countryIsoCode=IN&validFrom=2026-01-01&validTo=2026-12-31&languageIsoCode=EN) |
| Google public India holiday ICS | Holidays | E4 | none | **Blocked**: no ACAO header | Free | Verified not usable from the browser | [probe](https://calendar.google.com/calendar/ical/en.indian%23holiday%40group.v.calendar.google.com/public/basic.ics) |
| API Setu catalogue | Government KYC, education and business APIs | S2, C3 | Listed "No auth"; KYC APIs believed to need consumer onboarding | Not probed | Not published | Unverified | [public-apis README](https://github.com/public-apis/public-apis) |

Maintainers and repo stats from the notes: **razorpay/ifsc** (Razorpay) has 396 stars, last push 2026-10-04, release v2.0.62 on 2026-09-01. **libphonenumber-js** (catamphetamine) has 3,003 stars, last push 2026-11-10, latest 1.13.16; upstream google/libphonenumber has 18,353 stars. **tesseract.js** has 38,831 stars, last push 2026-05-17. **Nager.Date** has 1,443 stars, last push 2026-11-11. **LibreTranslate** has 17,698 stars, last push 2026-11-14. **AI4Bharat/IndicXlit** has 146 stars, last push 2023-10-13. **public-apis** has 498,914 stars; its CORS column is self-reported and its LibreTranslate row is out of date ([GitHub API](https://api.github.com/repos/public-apis/public-apis)). Maintainers are **not found** for api.postalpincode.in (third party, not India Post), Google Input Tools (no public terms), caldays.com and holidayexplore.com. The India Public Holidays API repo is `shrinivas-sn/calendar-api`; its stars were not returned.

### 3d. Indian KYC vendors, DigiLocker and messaging (all post-MVP)

Every row needs a server, because the secret must never sit in `PolicyNest.html`, where anyone can read it.

| Name | What it does for PolicyNest | Goal ID | Auth | CSP/CORS fit | Cost | Status | Link |
|---|---|---|---|---|---|---|---|
| Cashfree Secure ID | PAN verify, bank account sync, reverse/UPI penny-drop, DigiLocker, Smart OCR in one suite; sandbox test data | C3 (PAN, penny-drop), S2 | API key (client ID + secret); production needs **server IP whitelisting** | Server only | Per-call price not published; free PAN credits mentioned (unverified) | Unverified (partial) | [Verify PAN](https://www.cashfree.com/docs/api-reference/vrs/v2/pan/verify-pan-sync.md), [go-live checklist](https://www.cashfree.com/docs/secure-id/get-started/integration/go-live-checklist.md), [test data](https://www.cashfree.com/docs/api-reference/vrs/data-to-test-integration.md) |
| Sandbox.co.in (Quicko) | KYC APIs with test keys and Postman collections | C3 | API key + secret → 24-hour JWT | Server only (browser use not stated) | Not published | Verified (auth page; landing page only for products) | [Authenticate](https://developer.sandbox.co.in/api-reference/authenticate), [portal](https://developer.sandbox.co.in/) |
| Setu | Reverse penny-drop (applicant pays ₹1 by UPI, returns holder name); DigiLocker fetch | C3, S2 | API key (client ID/secret); credentials by email to their onboarding team | Server only | Not published | Unverified (partial) | [Reverse penny drop](https://docs.setu.co/data/bav/reverse-penny-drop), [DigiLocker API](https://docs.setu.co/data/digilocker/api-reference) |
| HyperVerge | Face match and liveness; browser Web SDK with a short-lived token minted on a backend | C3 (face match), R2 | API key (appId + appKey, server-side) | Browser SDK is domain-allowlisted; a backend still mints tokens | Not published | Unverified (partial) | [Authentication](https://documentation.hyperverge.co/other-resources/authentication), [Web SDK](https://documentation.hyperverge.co/sdks/web/integration_guide_websdk) |
| Karza (Perfios) | Aadhaar XML authentication suite | C3 | Contract | Server only | Not published; a reseller claims free sandbox credits | Unverified | [Perfios blog](https://perfios.ai/resources/blogs/aadhaar-xml-authentication-api-suite-by-karza/) |
| Surepass | Penny-drop; an IRDAI "insurance agent" verification product | C3 (penny-drop, registry) | Contract (sales) | Server only | Via sales | Unverified (marketing) | [penny drop](https://surepass.io/penny-drop-api/), [agent verification](https://surepass.io/?p=13168) |
| Decentro | PAN, penny drop, penniless and reverse penny-drop | C3 | Not found | Server only | Not found | Unverified (third-party notes) | [javajack notes](https://javajack.github.io/broking-kyc/vendors/verification/decentro) |
| Bureau.id, Signzy, IDfy | Not researched | C3 | Not found | Not found | Not found | Unverified | not found |
| DigiLocker direct (API Setu requester) | Pull issued PAN, Aadhaar and marksheets with the applicant's OAuth consent | S2 | OAuth 2.0 + partner onboarding and terms of use (June 2025) | Needs a server (reportedly in India) | Fees not found | Verified (API Setu page); onboarding details unverified (partial) | [apisetu.gov.in/digilocker](https://apisetu.gov.in/digilocker), [Requester spec v1.12](https://cf-media.api-setu.in/resources/Requester-APISpecification-V1_12.pdf) |
| UIDAI offline e-KYC XML / Secure QR | Verify a UIDAI-signed Aadhaar QR or XML **in the browser** with WebCrypto: no key, no UIDAI call | C3 (name, DOB, state), D5 | none technically; **legal status unsettled** (offline verification regulations, Dec 2025 amendment) | Fits the CSP if the certificate is inlined | Free | Unverified (partial; UIDAI pages returned 404/503) | [UIDAI offline e-KYC](https://uidai.gov.in/ecosystem/authentication-devices-documents/about-aadhaar-paperless-offline-e-kyc.html), [Regulations 2021](https://www.uidai.gov.in/images/The_Aadhaar_Authentication_and_Offline_Verifications_Regulations_2021.pdf) |
| IRDAI Agent Locator | Free public search of licensed agents; no API | C3 (registry, reviewer manual step) | none (web page) | **Not callable** (no API; scraping not viable) | Free | Unverified (insurer blogs) | [Niva Bupa guide](https://www.nivabupa.com/health-insurance-articles/how-to-verify-an-insurance-agent-online-with-the-irda-portal-agent-locator.html), [policyholder.gov.in](https://policyholder.gov.in/individual-agents) |
| Protean (NSDL) Online PAN Verification | Direct PAN verification for approved entities | C3 (PAN) | Contract: ITD approval, DSC, annual fee | Server only | Fee conflicting across sources (not confirmed) | Unverified (partial) | [OPV overview](https://tinpan.proteantech.in/services/online-pan-verification/pan-verification-overview.html) |
| WhatsApp Business Cloud API (Meta) | Real F1 follow-ups and S1 conversational onboarding with approved templates | F1, S1 | Token (API key) + webhook | Server only | Per delivered template message; India INR rate card not read | Verified (pricing page) | [Meta pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md) |
| SMS in India (TRAI DLT) | Real SMS follow-ups; entity, header and template registration first | F1 | Contract (DLT registration) + provider key | Server only | Not found | Unverified (SMS vendor docs) | [Plivo DLT](https://www.plivo.com/docs/sms/concepts/dlt-registration-process) |
| MSG91, Gupshup | Indian SMS/WhatsApp providers; no first-party MCP | F1, S1 | API key | Server only | Not checked | Unverified | [Composio MSG91](https://mcp.composio.dev/msg91), [Zapier](https://zapier.com/apps/msg91/integrations/gupshup) |

Dates from the notes: API Setu lists Requester API Specification v1.12 (Oct 2023), Terms of Use for Requester (June 2025) and Meri Pehchaan spec v2.4 (listed as Sep 2026). Meta's per-message pricing has applied since 1 Jul 2025, with further changes on 1 Oct 2026 ([Meta pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)). No vendor's own site confirmed a per-call price. Third-party price indications exist but are not treated as vendor prices here.

## 4. Tiers

### Now: keyless and working in the static MVP

These can ship inside `PolicyNest.html` today without breaking the CSP or the no-key rule. All fetch calls send only non-personal values.

**Razorpay IFSC API** ([probe](https://ifsc.razorpay.com/HDFC0000001), Verified) turns one part of the simulated penny-drop into a real check. "This IFSC exists, the branch is in Maharashtra, IMPS is on" is real. The holder-name match stays simulated and must keep its "simulated" label. Branch state is not residence state, so the result should be information only, never a hard rule.

**api.postalpincode.in** ([probe](https://api.postalpincode.in/pincode/110001), Verified, maintainer unknown), with **Zippopotam.us** as backup ([probe](https://api.zippopotam.us/IN/110001), Verified), maps a typed pincode to a state. It needs state-name normalisation (Delhi / New Delhi / NCT of Delhi), and the pincode must be sent on its own, never next to a name.

**libphonenumber-js** at an exact pinned version from jsDelivr ([file](https://cdn.jsdelivr.net/npm/libphonenumber-js@1.11.4/bundle/libphonenumber-min.js), Verified) checks mobile format with no network call per number. Pin an exact version, as CLAUDE.md requires.

The **Kickbox Open** disposable-domain check ([probe](https://open.kickbox.com/v1/disposable/example.com), Verified) is optional and low value.

**Holidays:** embed a JSON of the 2026 central-government gazetted list, labelled with its source, rather than calling any holiday API. The three working APIs disagree with each other (see §5).

A **Now-but-not-yet** item: UIDAI Secure QR / offline XML signature checks in the browser are technically keyless and CSP-compatible ([UIDAI offline e-KYC](https://uidai.gov.in/ecosystem/authentication-devices-documents/about-aadhaar-paperless-offline-e-kyc.html), Unverified). Do not build this until the amendment is read, and then only with synthetic or UIDAI sample files.

### Post-MVP: needs keys, a server or a contract

Everything in table 3d sits here: Cashfree, Sandbox.co.in, Setu, HyperVerge, Karza/Perfios, Surepass, Decentro, DigiLocker direct, Protean, WhatsApp Cloud API, SMS DLT, MSG91/Gupshup. So do the messaging MCP servers (Twilio, Bird) and any translation service called at runtime (Sarvam, DeepL, LibreTranslate). Each needs a small backend, ideally in an India region, and the CSP's `connect-src` would have to allow it. Whether Embarko can host functions or let the app set its own CSP was not researched.

For a first real integration, the notes point to **Cashfree** (PAN, bank, reverse penny-drop and DigiLocker in one suite, with sandbox test data) ([Cashfree test data](https://www.cashfree.com/docs/api-reference/vrs/data-to-test-integration.md), Unverified partial) or **Sandbox.co.in** (self-serve-looking test keys) ([Authenticate](https://developer.sandbox.co.in/api-reference/authenticate), Verified). Face match fits the HyperVerge pattern, where a backend mints a short-lived token for the browser SDK ([HyperVerge auth](https://documentation.hyperverge.co/other-resources/authentication), Unverified partial). For S2, an aggregator (Setu or Cashfree DigiLocker) is the realistic route. Direct onboarding with NeGD (the government body behind DigiLocker) would be the regulated entity's job, i.e. InsuranceDekho's ([apisetu.gov.in/digilocker](https://apisetu.gov.in/digilocker), Verified). The IRDAI registry check should stay simulated, or become a manual reviewer step citing the public Agent Locator, because no registry API was found. The source pack's planned adapter interfaces (`IPennyDropAdapter`, `IIRDAIRegistryAdapter`) map cleanly onto the existing `SIM` object.

### Dev tooling: helps Claude build and test, never shipped

- **No Node needed:** the `design` plugin, the `webapp-testing` skill with Python Playwright, the built-in Claude browser tools, `frontend-design`, `security-guidance`, `code-review`, the Google Sheets/Drive, Canva, Figma, Hugging Face and Embarko connectors, `paddleocr-mcp` / `mcp-ocr`, `mcp-server-motherduck`, and `mcp-server-fetch`.
- **Need Node first:** Playwright MCP, Chrome DevTools MCP, the Lighthouse and a11y MCPs.
- **Dev-time only, with a key:** Sarvam or DeepL to translate the fixed English string table once for S4. A native Hindi speaker should review the output before it is hard-coded. Placeholders replace real names.
- **Paid:** BrowserStack, for real-device D6 testing.

## 5. Risks and things that could not be verified

**Unknown or undocumented endpoint owners.** api.postalpincode.in is a third-party service, not India Post, and the notes found no owner, rate limit or uptime history. Google Input Tools works but has no public documentation or terms of use, so it could change or vanish without notice. caldays.com, holidayexplore.com and the onrender India Public Holidays API are small or unknown projects. The onrender one runs on free hosting that cold-starts slowly. Razorpay IFSC publishes no SLA or rate limit either. Any of these should fail soft: the app must still decide when the lookup times out.

**Holiday sources disagree.** Holi 2026 is 3 March in caldays but 4 March in HolidayExplore and the India Public Holidays API, which puts Holika dahan on the 3rd. One source lists 23 holidays and another 16, and caldays mixes in regional holidays ([caldays](https://caldays.com/api/holidays/in), [HolidayExplore](https://holidayexplore.com/api/v1/holidays?country=IN&year=2026)). Nager.Date and OpenHolidays have no India data at all. The DoPT 2026 gazetted list was not fetched, so the "official" Holi date is unconfirmed. A broker's SLA should use the employer's own holiday list, which no API provides.

**The December 2025 Aadhaar offline-verification amendment was not read.** A file dated 9.12.2025 reportedly adds Reg. 13A, which requires offline verification seeking entities to register, and deletes "(XML)" from Reg. 16C(1). Its PDF text could not be extracted, and the UIDAI FAQ and offline e-KYC pages returned 404 or 503 ([amendment PDF](https://banklaw.in/manage/images/services/1791517688Aadhaar(Authenticn&OfflineVerifn)AmendmnetRegulation2025-9.12.2025.pdf), [Tsaaro commentary](https://tsaaro.com/blogs/rethinking-offline-aadhaar-verification-special-emphasis-on-how-the-amendment-changes-things-and-the-potential-impacts.)). Until it is read, browser-side Aadhaar QR/XML verification is demo-only on synthetic data. The current UIDAI certificate name was seen only in a commercial code sample, and no UIDAI sample test files were found.

**Node.js is not installed on this machine.** That rules out Playwright MCP, Chrome DevTools MCP, the Lighthouse and a11y MCP servers, the Filesystem and Memory reference servers, Twilio's MCP and DeepL's local server until Node is installed. The Python and uvx routes avoid the problem.

**GitHub rate-limit gaps.** Unauthenticated GitHub API calls ran out at 60 an hour. Stars or push dates are therefore missing for obra/superpowers, GoogleChrome/modern-web-guidance, confident-ai/deepeval, upstash/context7, sarvamai/sarvam-mcp, AI4Bharat/IndicTrans2, Jem-HR/pywa-mcp-server, haris-musa/excel-mcp-server, xing5/mcp-google-sheets, googleapis/genai-toolbox and shrinivas-sn/calendar-api. Where a table says "not fetched", the number is unknown, not zero.

**Privacy of sending names to translation APIs.** Transliterating or translating an applicant's name through Google Input Tools, MyMemory, Sarvam or DeepL sends personal data to a third party, which needs notice and consent under the DPDP Act. The safe pattern is to translate fixed templates with placeholders during development, keep cross-script name matching in an on-device rule table, and make no runtime translation calls. The same logic says: send the pincode alone, send only the email domain, and never send document images to remote OCR. A PAN or Aadhaar image would carry full identity data, and an Aadhaar image would carry the full 12-digit number, which the project's own rule forbids everywhere.

**Other open points.**

- Connector auth types and pricing are not stated in the registry; "OAuth" is inferred.
- The Embarko connector's maintainer is not stated (it is hosted on viasocket.com).
- DeepL's Hindi support was not confirmed.
- Sarvam's pricing, data retention and residency are not stated.
- No vendor's per-call price, business-KYC requirements or DPDP data-processing terms were read.
- The DigiLocker partner FAQ PDF was image-only, so whether a student team can register is unknown.
- Whether POSPs (as opposed to licensed agents) appear in the IRDAI Agent Locator is unconfirmed.
- No on-device face-match library was tested, and the notes give no verified link for one. Moving from the fixed 0.91 score to a real browser score stays an untested idea.
- No accuracy figures for any OCR MCP server on Indian ID cards were found.
- None of the dev tools were tried against this project; fit is judged from catalog descriptions.

**What is simulated versus real today.** OCR (Tesseract.js and pdf.js, on the device) is real. PAN verification, the penny-drop holder name, face match (fixed 0.91 unless a specimen variant sets it), the IRDAI registry ("no record") and the WhatsApp/SMS send are simulated. Nothing in this report changes that unless the Razorpay IFSC lookup is added, and even then only the "IFSC exists" part becomes real.

## 6. Sources

**Claude plugins and connectors**
- https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md
- https://api.github.com/repos/anthropics/claude-code/contents/plugins
- https://claude.com/marketplace/plugins
- https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json
- https://api.github.com/repos/anthropics/claude-plugins-official
- https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design
- https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright
- https://github.com/anthropics/knowledge-work-plugins/tree/main/design
- https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md
- https://github.com/huggingface/skills
- https://github.com/figma/mcp-server-guide
- https://github.com/twilio/ai
- https://mcp.viasocket.com/mcp/6aa6e50e3f46d251d268bd9d-75344
- https://mcp.vercel.com/
- https://mcp.netlify.com/mcp
- https://bindings.mcp.cloudflare.com/mcp
- https://mcp.figma.com/mcp
- https://mcp.canva.com/mcp
- https://drivemcp.googleapis.com/mcp/v1
- https://sheetsmcp.googleapis.com/mcp/v1
- https://mcp.notion.com/mcp
- https://mcp.linear.app/mcp
- https://huggingface.co/mcp
- https://mcp.twilio.com/docs
- https://mcp.browserstack.com/mcp
- https://mcp.sentry.dev/mcp
- https://mcp.supabase.com/mcp
- https://mcp.lilt.com/mcp
- https://mcp.smartling.com/mcp
- https://www.wati.io/en/blog/connect-claude-to-whatsapp-business-api/
- https://wassenger.com/help/mcp

**MCP servers**
- https://github.com/modelcontextprotocol/servers
- https://api.github.com/repos/modelcontextprotocol/servers
- https://api.github.com/repos/modelcontextprotocol/servers-archived
- https://pypi.org/pypi/mcp-server-fetch/json
- https://pypi.org/pypi/mcp-server-git/json
- https://registry.npmjs.org/@modelcontextprotocol/server-filesystem
- https://registry.npmjs.org/@modelcontextprotocol/server-memory
- https://github.com/microsoft/playwright-mcp
- https://api.github.com/repos/microsoft/playwright-mcp
- https://registry.npmjs.org/@playwright/mcp
- https://github.com/ChromeDevTools/chrome-devtools-mcp
- https://api.github.com/repos/ChromeDevTools/chrome-devtools-mcp
- https://registry.npmjs.org/chrome-devtools-mcp
- https://github.com/priyankark/lighthouse-mcp
- https://awesome.ecosyste.ms/projects/github.com%2Fpriyankark%2Flighthouse-mcp
- https://github.com/danielsogl/lighthouse-mcp-server
- https://github.com/ronantakizawa/a11ymcp
- https://www.deque.com/axe/mcp-server/
- https://www.deque.com/blog/axe-devtools-for-web-now-includes-axe-mcp-server-for-earlier-fixes-and-faster-delivery/
- https://docs.deque.com/devtools-server/4.0.0/en/axe-mcp-server
- https://www.deque.com/axe-mcp-server-faster-accessibility-remediation/
- https://paddlepaddle.github.io/PaddleOCR/main/en/version3.x/deployment/mcp_server.html
- https://api.github.com/repos/PaddlePaddle/PaddleOCR
- https://pypi.org/pypi/paddleocr-mcp/json
- https://github.com/rjn32s/mcp-ocr
- https://pypi.org/pypi/mcp-ocr/json
- https://github.com/everaldo/mcp-mistral-ocr
- https://github.com/lemopian/mistral-ocr-mcp
- https://github.com/ORDIS-Co-Ltd/mistral-ocr-mcp
- https://pypi.org/pypi/mistral-ocr-mcp/json
- https://awslabs.github.io/mcp/servers/document-loader-mcp-server
- https://api.github.com/repos/awslabs/mcp
- https://pypi.org/pypi/awslabs.document-loader-mcp-server/json
- https://chatforest.com/reviews/ocr-document-intelligence-mcp-servers/
- https://archestra.ai/mcp-catalog/awslabs__mcp
- https://www.pkgstats.com/pkg:@kaenova/document-intelligence-mcp
- https://playbooks.com/mcp/cognitive-stack-azure-form-recognizer
- https://www.activepieces.com/mcp/google-document-ai
- https://api.github.com/repos/microsoft/mcp
- https://pypi.org/pypi/sarvam-mcp/json
- https://docs.sarvam.ai/api/developer-tools/mcp
- https://docs.sarvam.ai/conversations/mcp
- https://glama.ai/mcp/servers/safayavatsal/Sarvam-MCP
- https://github.com/DeepLcom/deepl-mcp-server
- https://registry.npmjs.org/deepl-mcp-server
- https://registry.modelcontextprotocol.io/v0/servers?search=deepl
- https://registry.modelcontextprotocol.io/v0/servers?search=sarvam
- https://registry.modelcontextprotocol.io/v0/servers?search=digilocker
- https://registry.modelcontextprotocol.io/v0/servers?search=whatsapp
- https://registry.modelcontextprotocol.io/v0/servers?search=duckdb
- https://github.com/motherduckdb/mcp-server-motherduck
- https://pypi.org/pypi/mcp-server-motherduck/json
- https://api.github.com/repos/twilio-labs/mcp
- https://registry.npmjs.org/@twilio-alpha/mcp
- https://github.com/twilio-labs/mcp
- https://mcp.bird.com/
- https://api.github.com/repos/lharries/whatsapp-mcp
- https://api.github.com/repos/nakulben/whatsapp-mcp
- https://glama.ai/mcp/servers/p8jhe2q40u
- https://lobehub.com/it/mcp/jem-hr-pywa-mcp-server
- https://www.claudemarket.ai/mcp/Gonzalez8/whatsapp-business-mcp
- https://mcp.composio.dev/msg91
- https://viasocket.com/mcp/msg91
- https://zapier.com/apps/msg91/integrations/gupshup
- https://providers.apievangelist.com/providers/digio/
- https://www.cashfree.com/docs/secure-id/digilocker/digilocker.md

**Public APIs and libraries**
- https://github.com/public-apis/public-apis
- https://api.github.com/repos/public-apis/public-apis
- https://ifsc.razorpay.com/HDFC0000001
- https://ifsc.razorpay.com/XXXX0000000
- https://github.com/razorpay/ifsc
- https://api.github.com/repos/razorpay/ifsc
- https://api.github.com/repos/razorpay/ifsc/releases/latest
- https://cdn.jsdelivr.net/gh/razorpay/ifsc@latest/README.md
- https://api.postalpincode.in/pincode/110001
- https://api.postalpincode.in/postoffice/Connaught
- https://api.zippopotam.us/IN/110001
- https://inputtools.google.com/request?text=namaste&itc=hi-t-i0-und&num=3
- https://api.mymemory.translated.net/get?q=hello&langpair=en|hi
- https://libretranslate.com/translate
- https://api.github.com/repos/LibreTranslate/LibreTranslate
- https://github.com/LibreTranslate/LibreTranslate
- https://api.github.com/repos/AI4Bharat/IndicXlit
- https://github.com/AI4Bharat/IndicXlit
- https://api.ocr.space/parse/imageurl?apikey=helloworld&url=https://example.com/x.png
- https://api.github.com/repos/naptha/tesseract.js
- https://cdn.jsdelivr.net/npm/libphonenumber-js@1.11.4/bundle/libphonenumber-min.js
- https://registry.npmjs.org/libphonenumber-js/latest
- https://api.github.com/repos/catamphetamine/libphonenumber-js
- https://github.com/catamphetamine/libphonenumber-js
- https://api.github.com/repos/google/libphonenumber
- https://open.kickbox.com/v1/disposable/example.com
- https://api.usercheck.com/domain/example.com
- https://date.nager.at/api/v3/PublicHolidays/2026/IN
- https://date.nager.at/api/v3/AvailableCountries
- https://api.github.com/repos/nager/Nager.Date
- https://openholidaysapi.org/PublicHolidays?countryIsoCode=IN&validFrom=2026-01-01&validTo=2026-12-31&languageIsoCode=EN
- https://calendar-api-web.vercel.app/docs
- https://caldays.com/api/holidays/in
- https://holidayexplore.com/api/v1/holidays?country=IN&year=2026
- https://holidayexplore.com/api-docs/
- https://calendar.google.com/calendar/ical/en.indian%23holiday%40group.v.calendar.google.com/public/basic.ics
- https://www.irdai.gov.in/

**KYC vendors, DigiLocker, UIDAI, IRDAI, messaging**
- https://developer.sandbox.co.in/api-reference/authenticate
- https://developer.sandbox.co.in/
- https://www.cashfree.com/docs/api-reference/vrs/v2/pan/verify-pan-sync.md
- https://www.cashfree.com/docs/secure-id/get-started/integration/go-live-checklist.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/sdk/verification-suite-server-sdks.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/end-point.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/pan/pan-360.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/pan/pan-lite.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/bav-v2/bank-account-verification-sync-v2.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/reverse-penny-drop/create-reverse-penny-drop-request.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/upi-penny-drop/create-upi-penny-drop-request.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/digilocker/create-digilocker-url.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/digilocker/get-document-from-digilocker.md
- https://www.cashfree.com/docs/api-reference/vrs/v2/smart-ocr/smart-ocr.md
- https://www.cashfree.com/docs/api-reference/vrs/data-to-test-integration.md
- https://www.cashfree.com/docs/help/account/account-activation.md
- https://www.cashfree.com/docs/secure-id/kyc-stack/verify-pan
- https://docs.setu.co/data/bav/reverse-penny-drop/api-integration
- https://docs.setu.co/data/bav/reverse-penny-drop
- https://docs.setu.co/data/bav/reverse-penny-drop/quickstart
- https://support.setu.co/support/solutions/articles/81000410536-how-do-we-test-rpd-in-sandbox-
- https://docs.setu.co/data/digilocker/quickstart
- https://docs.setu.co/data/digilocker/api-reference
- https://documentation.hyperverge.co/other-resources/authentication
- https://documentation.hyperverge.co/sdks/web/integration_guide_websdk
- https://documentation.hyperverge.co/sdks/web/quick_start_web_sdk
- https://documentation.hyperverge.co/other-resources/faq
- https://javajack.github.io/broking-kyc/vendors/verification/hyperverge
- https://javajack.github.io/broking-kyc/vendors/verification/decentro
- https://perfios.ai/resources/blogs/aadhaar-xml-authentication-api-suite-by-karza/
- https://platform.softwareone.com/product/perfios-hub/PCP-3266-4695
- https://surepass.io/penny-drop-api/
- https://surepass.io/?p=13168
- https://surepass.io/blog/what-are-aadhaar-ovse-compliance-guidelines/
- https://roopya.money/?p=1624
- https://truid.pages.dev/
- https://www.digilocker.gov.in/assets/FAQ%20DL%20EL_onboarding.pdf
- https://apisetu.gov.in/digilocker
- https://api.apisetu.gov.in
- https://cdn.apisetu.gov.in/portal/assets/workflow_requester.pdf
- https://cf-media.api-setu.in/resources/Partners-SOP.pdf
- https://cf-media.api-setu.in/resources/DigiLocker-Terms-of-User-Requester-june-2025.pdf
- https://cf-media.api-setu.in/resources/Requester-APISpecification-V1_12.pdf
- https://cf-media.api-setu.in/resources/Requester-MeriPehchaan-APISpecification-V2_3.pdf
- https://entity.digilocker.gov.in/assets/img/Requester%20-%20Entity%20Locker%20API%20Specification_28_11_24.pdf
- https://sandbox.api-setu.in/
- https://didit.me/blog/digilocker-api/
- https://www.nivabupa.com/health-insurance-articles/how-to-verify-an-insurance-agent-online-with-the-irda-portal-agent-locator.html
- https://policyholder.gov.in/individual-agents
- https://www.pbpartners.com/articles/generic/irda-pan-lookup-tools
- https://authbridge.com/checks/insurance-agent-verification/
- https://meon.co.in/insurance-agent-verification-api
- https://tinpan.proteantech.in/faqs/online-pan-verification/faq-pan-verify-general.html
- https://tinpan.proteantech.in/services/online-pan-verification/pan-verification-register.html
- https://tinpan.proteantech.in/services/online-pan-verification/pan-verification-overview.html
- https://taxheal.com/?p=76654
- https://www.zoop.one/blog/pan-verification-guide
- https://uidai.gov.in/en/283-faqs/aadhaar-online-services/e-aadhaar/1892-how-to-validate-digital-signatures-in-e-aadhaar.html
- https://uidai.gov.in/ecosystem/authentication-devices-documents/about-aadhaar-paperless-offline-e-kyc.html
- https://example-code.com/csharp_winrt/aadhaar_paperless_offline_e-kyc.asp
- https://uidai.gov.in/ecosystem/authentication-devices-documents/qr-code-reader.html
- https://packagist.org/packages/itxshakil/aadhaar-offline
- https://uidai.gov.in/images/FAQ_OVSE.pdf
- https://www.uidai.gov.in/images/DosandDon_ts_for_Offline_Verification_Seeking_entities.pdf
- https://www.uidai.gov.in/images/The_Aadhaar_Authentication_and_Offline_Verifications_Regulations_2021.pdf
- https://banklaw.in/manage/images/services/1791517688Aadhaar(Authenticn&OfflineVerifn)AmendmnetRegulation2025-9.12.2025.pdf
- https://tsaaro.com/blogs/rethinking-offline-aadhaar-verification-special-emphasis-on-how-the-amendment-changes-things-and-the-potential-impacts.
- https://www.stqc.gov.in/sites/default/files/QRCS-CS-02-Rules-Procedure-QRCS-Device-Certification_1.pdf
- https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md
- https://baat.ai/blog/whatsapp-api-pricing-india
- https://myoperator.com/blog/whatsapp-business-api-pricing-india-2026
- https://www.plivo.com/docs/sms/concepts/dlt-registration-process
- https://docs.webengage.com/docs/trai-sms-dlt-regulations-india
- https://cedocs.netcorecloud.com/docs/dlt-faqs

*A note on goal-ID mapping: the research notes sometimes call Hindi UI "§8 gap 5" and discovery-call notes "§8 gap 6". The current PRODUCT.md moves Hindi pop-ups and interface to Future item **S4** and numbers the §8 list as: 1 usability tests, 2 R6 queue, 3 D6 phone-photo OCR, 4 held-out set, 5 discovery-call notes, 6 executive presentation. This report uses PRODUCT.md's numbering.*
