# Claude connectors and Claude Code plugins for building, testing, deploying and running PolicyNest

Research date: 14 Nov 2026. Method: GitHub API (unauthenticated; the 60-request limit ran out partway through, so some repos have no star count), raw `marketplace.json` files, code.claude.com docs, claude.com/marketplace, and the claude.ai MCP registry (`search_mcp_registry`, three queries). Nothing was installed, signed up for or connected.

Legend: **V** = Verified on the live page, repo or registry today. **U** = Unverified. "Dev" = dev tooling only (never shipped to applicants). "Ship" = would run in or behind the live site. Every connector and service below needs an account, so any "Ship" item conflicts with the "no API keys" MVP rule.

## Which official Anthropic plugin marketplaces exist and which plugins fit

### Takeaway
Anthropic has two general marketplaces: `claude-plugins-official`, which is added by default, and `claude-community`. It also has topic marketplaces (`anthropics/skills`, `anthropics/knowledge-work-plugins`). The `anthropics/claude-code` marketplace is deprecated. The official one lists 317 plugins today. The best fits for PolicyNest are frontend-design, playwright, chrome-devtools-mcp, code-review / pr-review-toolkit, security-guidance, the knowledge-work `design` plugin (for `/accessibility` and `/research-synthesis`), and the `webapp-testing` skill. All of them are dev tooling and need no API key.

### Cited Findings
- There are two general-purpose Anthropic marketplaces. Official is `anthropics/claude-plugins-official` (name `claude-plugins-official`, added automatically on first interactive run). Community is `anthropics/claude-plugins-community` (name `claude-community`, third-party plugins that authors submitted, added by hand). Topic marketplaces such as `anthropics/skills` and `anthropics/knowledge-work-plugins` are added with `/plugin marketplace add` — [Anthropic's marketplaces](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md) (V)
- The `claude-code-plugins` marketplace in `anthropics/claude-code` is deprecated; its plugins now update from claude-plugins-official — [same page](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md) (V). The `anthropics/claude-code/plugins` folder now holds only a README ([GitHub API](https://api.github.com/repos/anthropics/claude-code/contents/plugins), V).
- "Anthropic doesn't review third-party marketplaces"; Claude Marketplace on the web shows install counts and marks some plugins "Anthropic verified" — [same page](https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md) (V)
- claude.com/marketplace/plugins listed 531 plugins in total but showed no install counts on the page fetched. It marked these as Anthropic verified: Frontend Design, Superpowers, Code Review, Context7, Playwright, Security Guidance, Vercel, PR Review Toolkit. Figma and Chrome DevTools had no verified mark, and Cloudflare and Canva were not on the page fetched — [Claude Marketplace](https://claude.com/marketplace/plugins) (V; the listing may have been truncated)
- Official marketplace size: 317 plugin entries in `.claude-plugin/marketplace.json` — [marketplace.json](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) (V)
- Repo stats (GitHub API, 14 Nov 2026): claude-plugins-official 47,255 stars, last push 2026-11-14; claude-code 155,623 stars, last push 2026-11-14; knowledge-work-plugins 35,712 stars, last push 2026-11-13; anthropics/skills 194,361 stars, last push 2026-11-14 — [GitHub API](https://api.github.com/repos/anthropics/claude-plugins-official) (V)

#### Candidate plugins (all from claude-plugins-official unless noted; free to install; auth: none unless noted)

| Plugin | Maintainer | Fits goal / gap | What it does (from catalog) | Stars / last push of source | Ship? | Status |
|---|---|---|---|---|---|---|
| `frontend-design` | Anthropic | R7 review-console redesign, A5/A9 look | "distinctive, production-grade frontend interfaces"; Anthropic verified | in claude-plugins-official (47,255 / 2026-11-14) | Dev | V ([entry](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/frontend-design)). Already loaded in this session as the skill `frontend-design:frontend-design`. |
| `playwright` | Microsoft MCP, packaged by Anthropic | §8 gap 2 (scripted journeys ahead of the usability tests), T1–T10 regression, D6 photo-upload tests | Browser automation and e2e testing MCP; config runs `npx @playwright/mcp@latest` | microsoft/playwright-mcp 39,625 / 2026-11-13 | Dev | V ([entry](https://github.com/anthropics/claude-plugins-official/tree/main/external_plugins/playwright), [repo](https://github.com/microsoft/playwright-mcp)). **Needs Node.js (npx), which this machine does not have.** |
| `chrome-devtools-mcp` | Google Chrome DevTools team (vendor) | Debugging CSP errors on Embarko, Tesseract worker loading, performance on slow phones | Live Chrome control, performance traces, network and console with source maps | ChromeDevTools/chrome-devtools-mcp 55,918 / 2026-11-13 | Dev | V ([repo](https://github.com/ChromeDevTools/chrome-devtools-mcp)). Probably needs Node (U). |
| `browser-use` | Browser Use (vendor) | Same as playwright | Real browser: your own Chrome or Browser Use Cloud | browser-use/plugins 31 / 2026-10-17 | Dev | V (catalog). The cloud browser probably needs an account or key (U). |
| `code-review`, `pr-review-toolkit` | Anthropic | Engine-block quality before each rule change (§9) | Multi-agent PR review with confidence scoring; agents for tests, error handling and simplification | in official repo | Dev | V (catalog). The project is not a git repo, so both work best once it is. |
| `security-guidance` | Anthropic | Guardrails §7 (DPDP: no full Aadhaar, no secrets); XSS in a single-file JS app | Pattern warnings on edits and an agentic reviewer for XSS, secrets and 25+ other checks | in official repo | Dev | V (catalog) |
| `playground` | Anthropic | Prototyping the R6 queue or reviewer evidence layouts as single-file HTML | "self-contained single-file explorers with visual controls" | in official repo | Dev | V (catalog) |
| `modern-web-guidance` | Google Chrome (vendor) | Accessibility and current web best practices for vanilla JS | "latest web best practices" | GoogleChrome/modern-web-guidance (stars not fetched, rate limit) | Dev | V (catalog entry only) |
| `context7` | Upstash (vendor) | Current Tesseract.js 5 / pdf.js 3.11 docs | Hosted remote MCP, "no local Node.js or npx required" | not fetched | Dev | V (catalog). Free-tier terms and key requirement not checked (U). |
| `deepeval` | Confident AI (vendor) | §8 gap 4, held-out evaluation | Evals, datasets, reports for AI apps | confident-ai/deepeval (not fetched) | Dev | V (catalog). Python; its reporting service needs an account (U). Weak fit: the engine is rule-based, not an LLM. |
| `huggingface-skills` | Hugging Face (vendor) | D6 / §8 gap 3: find public ID-document photo datasets (MIDV-500-type) | Build, train, evaluate models, datasets, spaces | huggingface/skills 11,346 / 2026-11-13 | Dev | V |
| `figma` | Figma (vendor) | R7 (if the user's review-console references are in Figma) | Read design files, tokens, components into code | figma/mcp-server-guide 2,185 / 2026-11-13 | Dev | V. Needs a Figma account (OAuth, U). |
| `canva` | Canva (vendor) | Pitch or demo assets; R7 references if made in Canva | Create, edit, resize, brand-check designs | canva-sdks/canva-skills 162 / 2026-11-11 | Dev | V |
| `superdesign` | Superdesign dev, Inc. (vendor) | R7 design drafts | "branchable design drafts" on a canvas | not fetched | Dev | V (catalog). Account probably needed (U). |
| `twilio-developer-kit` | Twilio (vendor) | S1 WhatsApp, F1 real SMS/WhatsApp follow-up | Skills for SMS, Voice, WhatsApp, Verify | twilio/ai 41 / 2026-11-11 | Ship (eventually) | V. Twilio itself needs an account and keys, so it breaks the no-key rule. Future only. |
| `vercel`, `netlify-skills`, `cloudflare`, `render`, `railway`, `hostinger` | Vendors | Deployment alternatives to Embarko | Deploy and manage sites | vercel/vercel-plugin 336 / 2026-11-13; netlify/context-and-tools 53 / 2026-11-10; cloudflare/skills 3,367 / 2026-11-10 | Dev | V (catalog). Each needs an account or OAuth. No need while Embarko works. |
| `claude-md-management`, `project-artifact` | Anthropic | Keeping CLAUDE.md / PRODUCT.md current; a shareable status page in place of the lost status note | Audit CLAUDE.md; publish a living project status artifact | in official repo | Dev | V (catalog) |
| `design` (knowledge-work-plugins) | Anthropic | Accessibility goal; §8 gap 2 (usability tests); R7 critique; §8 gap 5 (UX copy for Hindi strings) | Commands `/critique`, `/accessibility` (WCAG, contrast, screen reader, keyboard), `/ux-copy`, `/research-synthesis`, `/handoff`; skill `accessibility-review` (WCAG 2.1 AA) | knowledge-work-plugins 35,712 / 2026-11-13 | Dev | V ([README](https://github.com/anthropics/knowledge-work-plugins/tree/main/design)). Install: `claude plugin install design@knowledge-work-plugins`. |
| `webapp-testing` skill (anthropics/skills) | Anthropic | T1–T10 regression, D6 upload tests | "testing local web applications using Playwright" with native **Python** Playwright scripts | anthropics/skills 194,361 / 2026-11-14 | Dev | V ([SKILL.md](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md)). Python fits this machine better than npx. |
| `superpowers` | obra (community author, listed in official) | General TDD and debugging discipline | Brainstorming, subagent development, TDD | not fetched (rate limit) | Dev | V (catalog, Anthropic verified on marketplace) |

- No plugin in the official catalog mentions OCR, DigiLocker, Aadhaar/KYC, i18n/translation or "accessibility" in its name. The only catalog descriptions that mention WCAG were the Shopify `liquid-skills` (Shopify themes only) and the knowledge-work `design` plugin — [marketplace.json keyword scan](https://github.com/anthropics/claude-plugins-official/blob/main/.claude-plugin/marketplace.json) (V)

### Inferences
- Without Node.js, the Python `webapp-testing` skill (plus `pip install playwright`) is the most practical way to automate T1–T10 and phone-photo uploads. The Playwright MCP plugin and chrome-devtools-mcp both expect `npx`.
- This session already has `accessibility`, `usability-testing`, `web-design-guidelines`, `frontend-design` and `code-review` skills loaded. Accessibility and usability-test planning may need no new install.
- No plugin closes R6 (multi-case queue) or S2 (DigiLocker). Those are build work, not tooling.

### Gaps
- No install counts: claude.com/marketplace showed none on the page fetched.
- Star counts are missing for obra/superpowers, GoogleChrome/modern-web-guidance, confident-ai/deepeval and upstash/context7 because the GitHub API limit ran out.
- Cost of each vendor's paid tier was not checked; the plugins themselves are open-source repos.

## Which claude.ai directory connectors fit, and is Embarko listed?

### Takeaway
Yes, **Embarko is in the claude.ai connector registry** (`deploy_app`, `embarko_onboarding`, `submit_feedback`), which matches the deploy route CLAUDE.md describes. Figma, Canva, Vercel, Netlify, Cloudflare, Google Drive, Google Sheets, Notion, Linear, Hugging Face, Twilio, BrowserStack, Sentry and Supabase connectors are all listed. All are OAuth/account-based dev or ops tools; none should be shipped inside the no-key MVP. Canva and Google Drive are already connected for this user.

### Cited Findings (all from the claude.ai MCP registry, queried 14 Nov 2026, V unless noted)

| Connector | Server URL | Tools (sample) | Fits | Auth | Connected now? |
|---|---|---|---|---|---|
| **Embarko** | https://mcp.viasocket.com/mcp/6aa6e50e3f46d251d268bd9d-75344 | deploy_app, embarko_onboarding, submit_feedback | E5 public URL; redeploy without curl/token | Account sign-in (U on type) | No |
| Vercel | https://mcp.vercel.com/ | list_projects, list_deployments, get_deployment_events, search docs | Hosting alternative | OAuth (U) | No |
| Netlify | https://mcp.netlify.com/mcp | deploy, project, team services | Hosting alternative | OAuth (U) | No |
| Cloudflare Developer Platform | https://bindings.mcp.cloudflare.com/mcp | workers, KV namespaces | Hosting alternative; KV could store R6 queue state later (would add a server) | OAuth (U) | No |
| Figma | https://mcp.figma.com/mcp | get_design_context, get_screenshot, get_variable_defs, generate_diagram | R7 review-console references | OAuth (U) | No |
| Canva | https://mcp.canva.com/mcp | search-designs, get-design-content, import-design-from-url | R7 references, demo assets | OAuth | **Yes** |
| Google Drive | https://drivemcp.googleapis.com/mcp/v1 | search_files, read_file_content, create_file | Share eval CSVs and usability-test notes | OAuth | **Yes** |
| Google Sheets | https://sheetsmcp.googleapis.com/mcp/v1 | get_values, update_values | §8 gaps 2 and 4: usability-test score sheet, held-out labelling sheet | OAuth | No |
| Notion | https://mcp.notion.com/mcp | search, create-pages, query-data-sources | PRODUCT.md spec, discovery-call notes (§8 gap 6) | OAuth | No |
| Linear | https://mcp.linear.app/mcp | create_issue, list_issues | Tracking the §8 gap list | OAuth | No |
| Hugging Face | https://huggingface.co/mcp | dataset_search, model_search, paper_search, space_search | D6: find public ID-document photo datasets | Optional HF account | No |
| Twilio | https://mcp.twilio.com/docs | twilio__search, twilio__retrieve (docs search only) | S1 WhatsApp / F1 real messaging research | Docs-only tools (U) | No |
| BrowserStack | https://mcp.browserstack.com/mcp | accessibilityExpert, fetchAccessibilityIssues, createTestRun | Accessibility audits; D6 testing on real phones/browsers | Account (paid service, U) | No |
| Sentry | https://mcp.sentry.dev/mcp | find_issues, get_issue_details | Error monitoring once friends use the live site | Account; the site would need the Sentry SDK and a DSN (a key) | No |
| Supabase | https://mcp.supabase.com/mcp | projects, databases | Persistence for an R6 multi-case queue (adds a backend and keys) | OAuth | No |
| LILT, Smartling | https://mcp.lilt.com/mcp, https://mcp.smartling.com/mcp | translate_text (LILT, with human verification); jobs and strings (Smartling) | §8 gap 5: Hindi UI strings | Paid accounts (U) | No |

- No DigiLocker, Aadhaar/KYC or OCR-specific connector came back from the registry for "digilocker, aadhaar, kyc, ocr, document extraction". The nearest hit was PaperOffice (a document management system with `po_aiocr_analyze`), which is not relevant to on-device OCR — [MCP registry query] (V)
- No WhatsApp connector came back from the registry. On the open web, WhatsApp MCP options are third-party: Wati (WhatsApp Business, OAuth, astra-mcp.wati.io/mcp), Wassenger (API-key URL), Blueticks, 2Chat, and an MIT open-source personal-WhatsApp bridge — [web search summary](https://www.wati.io/en/blog/connect-claude-to-whatsapp-business-api/), [Wassenger](https://wassenger.com/help/mcp) (U: search-snippet level, pages not opened)

### Inferences
- The Embarko connector is the natural deploy path once signed in. It avoids handling `~/.embarko/credentials` in the shell. Keep curl as the fallback.
- For R7, ask the user where the review-console references live. If they are in Figma, connect Figma; if in Canva, Canva is already connected.
- Google Sheets (with Drive already connected) is the simplest home for a five-user usability-test score sheet and a held-out labelling sheet. These are dev artefacts only.
- Everything for S1 (WhatsApp) and S2 (DigiLocker) needs a business account, a contract or government onboarding (DigiLocker requires partner registration), so neither fits the no-key MVP. Keep them as Future.

### Gaps
- The registry entries do not state auth type or pricing; "OAuth" above is inferred from the hosted-MCP pattern, not confirmed per connector.
- The claude.com/connectors web directory page was not fetched; the registry stands in for it.
- The Embarko connector's maintainer is not stated. Its URL is hosted on viasocket.com, which suggests viaSocket runs it for Embarko (U).
- DigiLocker partner API terms were not researched here; they are out of this task's scope.

## Mapping summary by PRODUCT.md goal / §8 gap

### Takeaway
Tooling exists for testing, accessibility, design, data and deployment. Nothing off the shelf closes R6, D6 or S2; those need build work or a dataset.

### Cited Findings
- R6 multi-case queue: no plugin. Supabase or Cloudflare connectors could add storage, but that adds a backend and keys — [MCP registry] (V)
- R7 review-console redesign: frontend-design, design (`/critique`), Figma or Canva connector — see the table above (V)
- §8 gap 2, usability tests: design `/research-synthesis` plus the already-loaded `usability-testing` skill; Google Sheets for scores — [design README](https://github.com/anthropics/knowledge-work-plugins/tree/main/design) (V)
- §8 gap 3 / D6, real phone-photo OCR: Hugging Face connector or skills to find datasets; webapp-testing or Playwright to script uploads; BrowserStack for real devices (paid) — sources above (V)
- §8 gap 4, held-out evaluation: Google Sheets / Drive for labelling; deepeval is a weak fit — sources above (V)
- §8 gap 5, Hindi UI: design `/ux-copy`; LILT or Smartling (paid) for translation with human review — [MCP registry] (V)
- Accessibility: design `/accessibility`, the `accessibility` skill already in this session, BrowserStack `accessibilityExpert` — sources above (V)
- S1 WhatsApp: twilio-developer-kit plugin, Twilio docs connector; future only (needs keys) — [catalog](https://github.com/twilio/ai) (V)
- S2 DigiLocker: none found (V, negative result)
- Deployment: Embarko connector (primary); Vercel, Netlify and Cloudflare as alternatives (V)

### Inferences
- A minimal no-cost dev kit for the next build session: `design@knowledge-work-plugins`, the `webapp-testing` skill (Python Playwright), `security-guidance`, the already-loaded `frontend-design`, the Embarko connector, and Google Sheets. Nothing in it ships to applicants or adds API keys to the site.

### Gaps
- None of these tools were tested against this project. Fit is judged from catalog descriptions only.
