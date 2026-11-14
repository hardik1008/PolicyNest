# KYC verification vendors, DigiLocker, IRDAI, UIDAI offline e-KYC and messaging: post-MVP replacements for PolicyNest's simulated checks

Research date: 14 Nov 2026. Research only: no sign-ups, no keys, no authenticated calls.
Verification labels: **Verified** = live docs page fetched and read this session. **Partly verified** = seen only as a search snippet of the vendor's own docs (page not fetched in full). **Unverified** = secondary or marketing source only, or not researched.

PolicyNest mapping (from PRODUCT.md / MISSING_SOURCE_MATERIALS.md §2.2 / brief): C3 checks currently simulated = PAN verification, penny-drop name, face match, IRDAI/IIB POSP registry; UIDAI Aadhaar e-KYC is listed as a simulated service; S1 = WhatsApp onboarding (Future); S2 = DigiLocker pull with photo fallback (Future); F1 = follow-up message via simulated WhatsApp/SMS. The brief's guardrail says "Real Aadhaar e-KYC, real penny-drop or real IRDAI registry calls — use the values in the data pack" (01_ORIGINAL_CHALLENGE/PS-01_CHALLENGE_BRIEF.md line 93), and MISSING_SOURCE_MATERIALS.md asks for adapter interfaces (`IPennyDropAdapter`, `IIRDAIRegistryAdapter`) that switch to real vendors when keys exist in `.env`.

## 1. Do these vendors need a backend, or can a static, CSP-locked page call them?

### Takeaway
Every vendor checked authenticates with a long-lived secret (client ID + secret, API key + secret, appId + appKey) that must stay on a server; one vendor (Cashfree) additionally requires server IP whitelisting in production. The only browser-side pattern found is HyperVerge's Web SDK, and even that needs a backend to mint a short-lived token. PolicyNest on Embarko static hosting would need at least a small serverless/back-end proxy before any real check can go live.

### Cited Findings
- **Sandbox.co.in (Quicko)** — `POST /authenticate` with headers `x-api-key` and `x-api-secret` returns a JWT access token valid 24 hours; token sent in the `authorization` header without "Bearer"; separate live/test key sets; test host `https://test-api.sandbox.co.in`, production `https://api.sandbox.co.in`. The page says nothing about browser/CORS use. **Verified** — [Sandbox API reference: Authenticate](https://developer.sandbox.co.in/api-reference/authenticate)
- **Cashfree Secure ID** — sandbox base `https://sandbox.cashfree.com/verification`, production on `api.cashfree.com`; requests use client ID and client secret headers; going live requires switching to production credentials and **whitelisting your server IP** (non-whitelisted IP returns an error); official **server** SDKs for Node.js, Java, Python, PHP (example `x_api_version` 2024-12-01). **Partly verified** — [Verify PAN sync](https://www.cashfree.com/docs/api-reference/vrs/v2/pan/verify-pan-sync.md), [Go-live checklist](https://www.cashfree.com/docs/secure-id/get-started/integration/go-live-checklist.md), [Server SDKs](https://www.cashfree.com/docs/api-reference/vrs/v2/sdk/verification-suite-server-sdks.md), [Endpoints](https://www.cashfree.com/docs/api-reference/vrs/v2/end-point.md)
- **Setu** — reverse penny-drop sandbox `https://dg-sandbox.setu.co`, headers `x-client-id`, `x-client-secret`, `x-product-instance-id`; credentials obtained by emailing onboarding@setu.co (not self-serve); DigiLocker API reference shows bearer auth on the same hosts (sandbox `dg-sandbox.setu.co`, prod `dg.setu.co`). **Partly verified** — [Setu RPD API integration](https://docs.setu.co/data/bav/reverse-penny-drop/api-integration), [Setu DigiLocker API reference](https://docs.setu.co/data/digilocker/api-reference)
- **HyperVerge** — backend calls `POST ind-state.idv.hyperverge.co/v2/auth/token` with non-expiring appId + appKey (from the HyperVerge One dashboard credentials tab) plus expiry, transaction ID and workflow ID; the short-lived token is passed to the Web SDK in the browser. Docs: "Always generate JWT tokens securely from your backend to protect your appId and appKey." FAQ says CORS errors usually mean your domain is not whitelisted (so browser SDK calls are domain-allowlisted). **Partly verified** — [HyperVerge authentication](https://documentation.hyperverge.co/other-resources/authentication), [Web SDK integration guide](https://documentation.hyperverge.co/sdks/web/integration_guide_websdk), [FAQ](https://documentation.hyperverge.co/other-resources/faq)
- **DigiLocker (official)** — the DigiLocker FAQ reportedly says a firm needs a registered Indian mobile number and a server located in India for API access. **Unverified** (search snippet; the PDF on digilocker.gov.in rendered as images and could not be read) — [DigiLocker / Entity Locker onboarding FAQ](https://www.digilocker.gov.in/assets/FAQ%20DL%20EL_onboarding.pdf)
- **WhatsApp Cloud API** — Meta's pricing page refers to billing resolved "from your app token" and status webhooks, implying a token-holding sender and a webhook receiver. **Verified** (implication, not an explicit statement) — [Meta: Pricing on the WhatsApp Business Platform](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)

### Inferences
- Embarko's static hosting plus CSP (no `blob:`, no `data:` fetch, `connect-src` presumably restricted) cannot safely hold any of these secrets. A minimal backend (serverless function or small server, India region for DigiLocker and DPDP comfort) is required for every live integration; the browser would call only that backend.
- The HyperVerge-style "backend mints a short-lived token, browser SDK runs the capture" pattern is the best fit for face match/liveness, because the selfie is captured in the browser anyway.
- The CSP would need `connect-src` (and possibly `script-src`/`frame-src`) entries for whatever backend/SDK domain is added; worth checking whether Embarko lets the app set its own CSP.

### Gaps
- No vendor doc read states CORS policy explicitly (Sandbox.co.in, Cashfree, Setu all silent on browser use). Assume server-only.
- Embarko's ability to host serverless functions or customise CSP was not researched here.

## 2. Vendor-by-vendor: what maps to PolicyNest, sandbox access, auth, pricing

### Takeaway
Cashfree Secure ID and Sandbox.co.in are the most self-serve options with public docs and test environments; Setu is strong on DigiLocker and reverse penny-drop but credentials come through its onboarding team; HyperVerge is the clearest face-match/liveness option with a browser SDK. Karza/Perfios, Bureau.id, Signzy, IDfy, Decentro and Surepass could not be verified in this session. No vendor's per-call price was confirmed on its own site.

### Cited Findings
**Sandbox.co.in (Quicko)**
- Developer portal lists a KYC product guide, API reference with "test scenarios", public Postman collections, Quickstart. Specific KYC endpoints (PAN, bank, OKYC, DigiLocker) were not visible on the landing page. **Verified (landing page only)** — [developer.sandbox.co.in](https://developer.sandbox.co.in/)
- Auth: API key + secret → 24 h JWT; test vs live keys and hosts (see §1). **Verified** — [Authenticate](https://developer.sandbox.co.in/api-reference/authenticate)
- Pricing: not published on the pages read. Signup requirements: not stated on the pages read.

**Cashfree Secure ID / Verification Suite**
- PAN: sync verify (`/verification/pan`, body PAN + name), PAN Lite, PAN 360, bulk PAN. **Partly verified** — [Verify PAN sync](https://www.cashfree.com/docs/api-reference/vrs/v2/pan/verify-pan-sync.md), [PAN 360](https://www.cashfree.com/docs/api-reference/vrs/v2/pan/pan-360.md), [PAN Lite](https://www.cashfree.com/docs/api-reference/vrs/v2/pan/pan-lite.md)
- Bank: Bank Account Verification Sync V2 (`/bank-account/sync`, account + IFSC; Deutsche Bank and Paytm Payments Bank not supported); reverse penny-drop, UPI penny-drop and mobile penny-drop endpoints exist. **Partly verified** — [BAV sync V2](https://www.cashfree.com/docs/api-reference/vrs/v2/bav-v2/bank-account-verification-sync-v2.md), [Reverse penny drop](https://www.cashfree.com/docs/api-reference/vrs/v2/reverse-penny-drop/create-reverse-penny-drop-request.md), [UPI penny drop](https://www.cashfree.com/docs/api-reference/vrs/v2/upi-penny-drop/create-upi-penny-drop-request.md)
- DigiLocker: create DigiLocker URL and get document endpoints. **Partly verified** — [Create DigiLocker URL](https://www.cashfree.com/docs/api-reference/vrs/v2/digilocker/create-digilocker-url.md), [Get document from DigiLocker](https://www.cashfree.com/docs/api-reference/vrs/v2/digilocker/get-document-from-digilocker.md)
- Also Smart OCR and e-Sign endpoints. **Partly verified** — [Smart OCR](https://www.cashfree.com/docs/api-reference/vrs/v2/smart-ocr/smart-ocr.md)
- Sandbox test data for success/failure cases (PAN, bank numbers, others), usable only in sandbox. **Partly verified** — [Data to test integration](https://www.cashfree.com/docs/api-reference/vrs/data-to-test-integration.md)
- Account activation (business KYC) is a separate help page; requirements not read. — [Account activation](https://www.cashfree.com/docs/help/account/account-activation.md)
- Pricing: a Cashfree page mentions free credits for PAN verification in the dashboard; per-call prices not confirmed. **Unverified** — [Cashfree verify PAN (KYC stack)](https://www.cashfree.com/docs/secure-id/kyc-stack/verify-pan)

**Setu**
- Reverse penny-drop: customer pays ₹1 to a VPA registered for your organisation; statuses include created, payment successful (returns bank details), payment failed; caveat that status may stay `BAV_REVERSE_PENNY_DROP_CREATED` if the banking partner sends no credit alert; sandbox has mock payments. **Partly verified** — [Reverse penny drop](https://docs.setu.co/data/bav/reverse-penny-drop), [Quickstart](https://docs.setu.co/data/bav/reverse-penny-drop/quickstart), [How to test RPD in sandbox](https://support.setu.co/support/solutions/articles/81000410536-how-do-we-test-rpd-in-sandbox-)
- DigiLocker: consent-based fetch; `POST /api/digilocker/` with redirect URL, `GET /api/digilocker/:id/status`, `GET /api/digilocker/documents`. **Partly verified** — [Setu DigiLocker quickstart](https://docs.setu.co/data/digilocker/quickstart), [API reference](https://docs.setu.co/data/digilocker/api-reference)
- Access: credentials via onboarding@setu.co (sales-led). Pricing: not published on pages seen. Forward penny-drop sandbox page not found.

**HyperVerge**
- Face match / liveness via HyperKYC workflows and Web SDK; token minted server-side (see §1). Face-match and liveness REST paths (`ind-faceid.hyperverge.co/v1/photo/verifyPairAuthentication`) were seen only in a third-party guide. **Partly verified** (token flow) / **Unverified** (endpoints) — [HyperVerge Web SDK quick start](https://documentation.hyperverge.co/sdks/web/quick_start_web_sdk), [third-party guide](https://javajack.github.io/broking-kyc/vendors/verification/hyperverge)
- Pricing and sandbox terms: not published on pages seen.

**Karza (now Perfios)**
- Perfios blog describes Karza's Aadhaar XML authentication suite: provider extracts the XML with the share phrase and validates the UIDAI signature. **Unverified** (vendor blog) — [Perfios/Karza blog](https://perfios.ai/resources/blogs/aadhaar-xml-authentication-api-suite-by-karza/)
- A marketplace listing (SoftwareOne) claims "10k+ free API credits with Sandbox access, no credit card required" for Perfios Hub. **Unverified** (reseller page) — [SoftwareOne: Perfios Hub](https://platform.softwareone.com/product/perfios-hub/PCP-3266-4695)

**Surepass**
- Penny-drop API: ₹1 transfer to confirm holder name; pricing via sales. Has an IRDAI "insurance agent" verification product page and OVSE compliance blogs. **Unverified** (marketing) — [Surepass penny drop](https://surepass.io/penny-drop-api/), [Surepass insurance agent](https://surepass.io/?p=13168), [Surepass OVSE guide](https://surepass.io/blog/what-are-aadhaar-ovse-compliance-guidelines/)

**Decentro**
- Third-party write-up: PAN verification, penny drop, penniless and reverse penny-drop under one endpoint. **Unverified** — [javajack broking-KYC notes: Decentro](https://javajack.github.io/broking-kyc/vendors/verification/decentro)

**Bureau.id, Signzy, IDfy**
- No India sandbox/pricing/auth facts found in this session. **Unverified / not researched.**

**Third-party price indications (do not treat as vendor prices)**
- One aggregator lists penny-drop at roughly ₹3–8 per call; TruID markets ₹2 per verification and free sandbox. **Unverified** — [roopya.money](https://roopya.money/?p=1624), [TruID](https://truid.pages.dev/)

### Inferences
- For a first real integration, Cashfree (PAN + bank sync + reverse penny-drop + DigiLocker in one suite, documented sandbox test data) or Sandbox.co.in (self-serve-looking test keys) are the lowest-friction choices; both still need business account activation before production.
- Reverse penny-drop (applicant pays ₹1 by UPI) gives the account-holder name without needing the account number typed, which fits PolicyNest's "account last four only" privacy stance.
- The existing `SIM` object in PolicyNest.html maps cleanly to adapter calls: PAN verify → name + status + PAN type; penny-drop → holder name; face match → score; registry → hit/no hit.

### Gaps
- Per-call prices: not confirmed on any vendor's own site.
- Business KYC/GST/contract requirements per vendor: not read (Cashfree activation page not fetched).
- Data residency/DPDP statements: none read for any vendor. Treat as open question for each vendor's DPA.
- Last docs update dates: not visible on pages read.

## 3. DigiLocker official partner (Requester) API and Entity Locker

### Takeaway
Direct DigiLocker integration is for registered organisations only: apply via the API Setu partner portal, sign the Requester Terms of Use (June 2025), integrate OAuth 2.0 authorization-code flow (PKCE referenced), pass testing/audit, then go live. No official self-serve sandbox for requesters was confirmed; aggregators (Setu, Cashfree) offer their own sandboxes on top.

### Cited Findings
- API Setu DigiLocker page lists: partner portal sign-up (partners.apisetu.gov.in), Partner Organisation Onboarding SOP, Partner's Configuration Manual – Requester, **Terms of Use for Requester (June 2025)**, Requester API Specification **v1.12 (Oct 2023)**, Meri Pehchaan API Specification **v2.4 (listed as Sep 2026)**, Issuer API Spec v1.13 and Issuer XML formats v1.9 (May 2024). **Verified** — [apisetu.gov.in/digilocker](https://apisetu.gov.in/digilocker)
- Onboarding steps listed on API Setu: apply online, get API key, develop host APIs, integrate with DigiLocker, perform testing/audit, go live; "DigiLocker will consider your eligibility and get back to you." **Partly verified** — [API Setu](https://api.apisetu.gov.in), [Requester workflow PDF](https://cdn.apisetu.gov.in/portal/assets/workflow_requester.pdf)
- NeGD onboarding SOP (5 June 2024) sets eligibility criteria for partner organisations, including an official organisation email domain; Requester terms say onboarding must be initiated by a senior authorised representative. **Partly verified** (search snippets of official PDFs) — [Partners SOP](https://cf-media.api-setu.in/resources/Partners-SOP.pdf), [Requester Terms of Use June 2025](https://cf-media.api-setu.in/resources/DigiLocker-Terms-of-User-Requester-june-2025.pdf)
- OAuth 2.0 authorization code grant; Requester spec v1.12 references PKCE; FAQ says the code verifier should be created dynamically per OAuth 2.0. **Partly verified** — [Requester API Specification v1.12](https://cf-media.api-setu.in/resources/Requester-APISpecification-V1_12.pdf), [Meri Pehchaan spec v2.3](https://cf-media.api-setu.in/resources/Requester-MeriPehchaan-APISpecification-V2_3.pdf)
- Entity Locker has a separate Requester API spec (28 Nov 2024). **Partly verified** — [Requester – Entity Locker API Specification](https://entity.digilocker.gov.in/assets/img/Requester%20-%20Entity%20Locker%20API%20Specification_28_11_24.pdf)
- An "API Setu & DigiLocker Sandbox" portal exists at sandbox.api-setu.in, described as testing API Setu APIs with pre-filled sample data; its relationship to requester OAuth testing is unconfirmed. **Unverified** — [sandbox.api-setu.in](https://sandbox.api-setu.in/)
- A third-party blog states no fee schedule, sandbox or onboarding lead time is published for direct DigiLocker. **Unverified** — [didit.me DigiLocker API blog](https://didit.me/blog/digilocker-api/)

### Inferences
- PKCE exists in the spec, but the token exchange still involves a client secret per standard requester flow (unconfirmed); and the FAQ's "server in India" requirement means a pure static-page integration is not possible.
- Entity Locker is for organisations' own documents, not for pulling an individual applicant's PAN/marksheet; the relevant product for S2 is the individual Requester / Meri Pehchaan flow.
- For PolicyNest S2, going through an aggregator (Setu or Cashfree DigiLocker) is the realistic post-MVP path; direct NeGD onboarding would be InsuranceDekho's (the regulated entity's) job.
- DigiLocker-issued PAN, Aadhaar and CBSE/state-board marksheets would remove OCR uncertainty for those slots; photo upload remains the fallback (brief's S2 wording).

### Gaps
- Exact eligibility list (entity types), whether an individual or student team can register: not confirmed; the FAQ PDF could not be read (image-only).
- Fees for direct DigiLocker: not found.

## 4. IRDAI / IIB POSP and agent registry lookup

### Takeaway
No public IRDAI API for POSP/agent lookup was found. There is a free, no-login public "Agent Locator" search page; commercial vendors (AuthBridge, Surepass, Meon) sell "insurance agent verification" APIs that presumably wrap such sources. The brief's IIB/IRDAI Central POSP Registry exclusivity check appears to be insurer/intermediary-only.

### Cited Findings
- IRDAI Agent Locator on agencyportal.irdai.gov.in (Consumer Tools), search by name, licence number, agent ID, PIN, insurer; free and no login. **Unverified** (insurer blogs, not IRDAI) — [Niva Bupa: verify agent via IRDAI agent locator](https://www.nivabupa.com/health-insurance-articles/how-to-verify-an-insurance-agent-online-with-the-irda-portal-agent-locator.html), [policyholder.gov.in individual agents](https://policyholder.gov.in/individual-agents)
- One source says there is no single consolidated public tool; the agency portal and insurer onboarding systems work together. **Unverified** — [PB Partners: IRDA PAN lookup](https://www.pbpartners.com/articles/generic/irda-pan-lookup-tools)
- Commercial "insurance agent verification" APIs: **Unverified** (marketing) — [AuthBridge](https://authbridge.com/checks/insurance-agent-verification/), [Surepass](https://surepass.io/?p=13168), [Meon](https://meon.co.in/insurance-agent-verification-api)

### Inferences
- Keep the IRDAI registry check simulated (or as a reviewer-manual step citing the public Agent Locator) post-MVP; a real exclusivity check needs InsuranceDekho's own access to the IIB/IRDAI POSP registry.
- Scraping the public locator from a static page is not viable (CORS, terms) and should not be planned.

### Gaps
- Whether IIB or IRDAI expose a registry API to intermediaries, and its terms: not found.
- Whether POSPs (as opposed to licensed agents) appear in the public Agent Locator: not confirmed.

## 5. NSDL/Protean and UTIITSL PAN verification for entities

### Takeaway
Protean's Online PAN Verification is for approved entities: online registration, Income Tax Department approval, Digital Signature Certificate for verification, annual registration fee. Not available to a student project; KYC vendors are the practical route.

### Cited Findings
- Entity must register with Protean; registration subject to ITD approval; after approval and fee receipt an eight-digit user ID is issued; DSC mandatory for PAN verification; fee refunded if ITD rejects. **Partly verified** — [Protean OPV FAQ](https://tinpan.proteantech.in/faqs/online-pan-verification/faq-pan-verify-general.html), [OPV registration](https://tinpan.proteantech.in/services/online-pan-verification/pan-verification-register.html), [OPV overview](https://tinpan.proteantech.in/services/online-pan-verification/pan-verification-overview.html)
- Annual fee conflicts across third-party sources: ₹1,200 + GST vs ₹12,000 + GST. **Unverified / conflicting** — [taxheal](https://taxheal.com/?p=76654), [Zoop](https://www.zoop.one/blog/pan-verification-guide)

### Gaps
- UTIITSL entity PAN verification: not researched (no results retrieved).
- Official current Protean fee: not confirmed.

## 6. UIDAI Aadhaar offline e-KYC (XML) and Secure QR: can it be verified fully client-side as a keyless "Now" option?

### Takeaway
Technically yes: both the Paperless Offline e-KYC XML and the Secure QR are signed by UIDAI (RSA-2048), the public certificate is downloadable, and verification needs no UIDAI call, so it could run in the browser with WebCrypto. Legally it is less simple: offline verification is governed by the Aadhaar (Authentication and Offline Verification) Regulations 2021, and a 2025 amendment reportedly requires OVSEs to register (Reg. 13A) and dropped "(XML)" from Reg. 16C(1). Treat it as a demo with synthetic data only until the amendment text is read.

### Cited Findings
- UIDAI: XML is machine-readable and digitally signed; verify using the signature value in the `s` tag, the rest of the XML without the `s` tag, and the UIDAI public key; XML zipped and protected with the resident's "Share Phrase"; certificate choice depends on download date (separate certificates for XML downloaded before 18 Jun 2019 and before 7 Jun 2020). **Partly verified** (UIDAI FAQ pages seen as snippets; the English offline e-KYC pages returned 404 when fetched) — [UIDAI: how to validate digital signatures in e-Aadhaar](https://uidai.gov.in/en/283-faqs/aadhaar-online-services/e-aadhaar/1892-how-to-validate-digital-signatures-in-e-aadhaar.html), [UIDAI: Aadhaar Paperless Offline e-KYC](https://uidai.gov.in/ecosystem/authentication-devices-documents/about-aadhaar-paperless-offline-e-kyc.html)
- The UIDAI XML signature has no KeyInfo, so the verifier must load the UIDAI certificate itself (Chilkat sample uses `uidai_auth_sign_prod_2023.cer`). **Unverified** (commercial code sample) — [Chilkat Aadhaar offline e-KYC example](https://example-code.com/csharp_winrt/aadhaar_paperless_offline_e-kyc.asp)
- Secure QR: visual code with demographics and photograph, digitally signed by UIDAI with a 2048-bit signature; a reader shows "QR Code not verified" if the signature fails; UIDAI links a "Secure QR code specification". **Partly verified** (snippet; page 404 on fetch) — [UIDAI Secure QR Code Reader](https://uidai.gov.in/ecosystem/authentication-devices-documents/qr-code-reader.html)
- Open-source PHP package `itxshakil/aadhaar-offline` verifies Secure QR against configured UIDAI certificates: the 256-byte RSA signature covers every byte before it; author notes it has not been tested on a real card. **Unverified** — [packagist: itxshakil/aadhaar-offline](https://packagist.org/packages/itxshakil/aadhaar-offline)
- Offline verification is defined as using Aadhaar for KYC locally without sending data to UIDAI; "any organization can validate genuineness ... through validation of UIDAI's digital signature present in the QR code or offline XML file" (UIDAI OVSE FAQ, as quoted in snippet). **Partly verified** (official PDF returned 503 when fetched) — [UIDAI FAQ OVSE](https://uidai.gov.in/images/FAQ_OVSE.pdf), [UIDAI Dos and Don'ts for OVSEs](https://www.uidai.gov.in/images/DosandDon_ts_for_Offline_Verification_Seeking_entities.pdf), [Aadhaar (Authentication and Offline Verification) Regulations 2021](https://www.uidai.gov.in/images/The_Aadhaar_Authentication_and_Offline_Verifications_Regulations_2021.pdf)
- 2025 amendment (dated 9.12.2025 in file name): reportedly inserts Reg. 13A requiring OVSEs to register and verify only for lawful purposes, and deletes "(XML)" from Reg. 16C(1). **Unverified** (search snippet; PDF text could not be extracted) — [Aadhaar (Authentication and Offline Verification) Amendment Regulations 2025](https://banklaw.in/manage/images/services/1791517688Aadhaar(Authenticn&OfflineVerifn)AmendmnetRegulation2025-9.12.2025.pdf), [Tsaaro commentary](https://tsaaro.com/blogs/rethinking-offline-aadhaar-verification-special-emphasis-on-how-the-amendment-changes-things-and-the-potential-impacts.)
- STQC rules say the signed code can be read only using UIDAI's Windows-based application (context: device certification). **Unverified** (snippet) — [STQC QRCS rules](https://www.stqc.gov.in/sites/default/files/QRCS-CS-02-Rules-Procedure-QRCS-Device-Certification_1.pdf)

### Inferences
- A browser implementation is feasible inside PolicyNest's constraints: unzip the XML with the share code in JS, canonicalise and verify the RSA-SHA256 signature with WebCrypto against an embedded UIDAI certificate; or decode the Secure QR (large decimal integer → bytes → decompress → fields; last 256 bytes = signature) with a JS QR reader and verify the same way. No key, no server, no CSP change if the certificate is inlined. Layout details beyond the "256-byte signature over preceding bytes" point come from third-party code, not the UIDAI spec, and must be checked against the spec.
- XML canonicalisation in browser JS is the fiddly part (no built-in XML-DSig); the Secure QR route is byte-level and simpler.
- Compliance: real Aadhaar data is in scope of the Aadhaar Act and DPDP; if the 2025 amendment requires OVSE registration, a public demo should verify only UIDAI's own sample files or synthetic test data, and must not store the XML, photo or full number (PolicyNest already masks to last four).
- This would cover "address state" and DOB/name cross-checks with signed data, but it does not prove the applicant is the holder (no OTP), so it complements, not replaces, face match.

### Gaps
- Text of the 2025 amendment and whether XML offline verification is still permitted: not confirmed.
- Whether UIDAI publishes sample signed XML/QR test files usable for a demo: not found.
- Current certificate file and validity (2023 cert name seen only in a code sample).

## 7. Messaging for S1/F1: WhatsApp Business Cloud API and SMS (DLT)

### Takeaway
WhatsApp Cloud API now charges per delivered template message by category and country; since 1 Oct 2026 service messages beyond 1,000/number/month and utility messages inside the 24-hour window are charged. India rates are in Meta's INR rate card (not read). SMS in India requires TRAI DLT registration (entity → header → template) before any OTP or follow-up message can be sent. Twilio, Gupshup, MSG91 and Kaleyra were not researched in this session.

### Cited Findings
- Per-message pricing since 1 Jul 2025; five categories (marketing, utility, authentication = templates; service, Meta Business Agent = non-template); paid only when delivered; user-to-business free; business can only message opted-in users; templates required outside the 24-hour customer service window. **Verified** — [Meta: WhatsApp pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)
- Effective 1 Oct 2026: service messages chargeable after 1,000 free per business phone number per month; utility messages inside an open window now charged; payment method needed by 30 Sep 2026. India not in the 1 Oct 2026 rate changes; India marketing rate rose 1 Jan 2026; INR billing for India-based customers from 1 Jan 2026, migration to INR required by 31 Dec 2026. Rate cards as CSV/PDF per currency. No last-updated date shown. **Verified** — [Meta: WhatsApp pricing](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing.md)
- Third-party reported India rates: utility/authentication about ₹0.11–0.16, marketing about ₹0.86–1.09; sources conflict. **Unverified** — [baat.ai](https://baat.ai/blog/whatsapp-api-pricing-india), [MyOperator](https://myoperator.com/blog/whatsapp-business-api-pricing-india-2026)
- DLT: three phases (Principal Entity registration → 19-digit Entity ID; Sender ID/header; content template approval, each template tied to one header); approved Template ID must be passed when sending; done on an operator DLT portal (e.g. Jio TrueConnect). **Unverified** (SMS vendor docs, not TRAI) — [Plivo DLT registration](https://www.plivo.com/docs/sms/concepts/dlt-registration-process), [WebEngage TRAI DLT](https://docs.webengage.com/docs/trai-sms-dlt-regulations-india), [Netcore DLT FAQs](https://cedocs.netcorecloud.com/docs/dlt-faqs)

### Inferences
- PolicyNest's F1 follow-up is a utility template; S1 conversational onboarding would mostly be service messages inside the applicant-opened window, now chargeable after the free tier.
- Both channels need a server: WhatsApp for the access token and the inbound webhook, SMS for the DLT-registered sender account. A BSP (Gupshup, Kaleyra, MSG91, Twilio) can hold templates and the WABA, but still needs server-side API keys.
- The consolidated English/Hindi follow-up text must be pre-approved as a template (WhatsApp) and a DLT template (SMS); variable slots should hold the item list.

### Gaps
- Twilio, Gupshup, MSG91, Kaleyra: docs, sandbox, auth and pricing not researched in this session.
- Official India INR rate card figures not read.
- TRAI primary text (TCCCPR 2018 and 2025 amendments) not read; header suffix rule (-P/-S/-T/-G, May 2025) unconfirmed.
