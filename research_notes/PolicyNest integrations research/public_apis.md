# Free / keyless public APIs for the PolicyNest static app

Scope: what a browser-only page on https://policynest.embarko.app (CSP: connect-src https, no blob:/data: fetch, no server) can call with no API key. Probes were made on 14 Nov 2026 with `curl -i -H "Origin: https://policynest.embarko.app"`, non-personal samples only (IFSC HDFC0000001, pincode 110001, year 2026, domain example.com, the words "hello"/"namaste"). "Verified" below means: I saw HTTP status and the `Access-Control-Allow-Origin` (ACAO) header myself. Repo stats are from the GitHub REST API on 14 Nov 2026.

Probe-discipline note: most endpoints were called once. Exceptions, all with non-personal data: MyMemory was called twice (second call added a dummy `de=a@b.c` parameter); caldays.com and HolidayExplore India 2026 were fetched a second time to read the body (the first probe kept only headers); calendar-api-web.vercel.app was tried twice on wrong paths (404) before finding its real API host.

Source list: [public-apis/public-apis README](https://github.com/public-apis/public-apis) — MIT, 498,914 stars, pushed_at 2026-11-13T17:59:59Z ([GitHub API](https://api.github.com/repos/public-apis/public-apis)). The README's "CORS" column is self-reported by contributors; several India rows are new, small vercel/onrender projects. Treat its entries as leads, not endorsements.

## 1. IFSC lookup / validation

### Takeaway
Razorpay IFSC is the clear MVP pick: keyless, `ACAO: *`, HTTPS, 404 on unknown codes, maintained (release v2.0.62, Sep 2026). IFSC is not personal data, so it fits DPDP. A fully offline option exists: the same dataset as a static JSON on jsDelivr.

### Cited Findings
- `GET https://ifsc.razorpay.com/HDFC0000001` → **HTTP/1.1 200 OK**, `Access-Control-Allow-Origin: *`, `Content-Type: application/json`. Body has BANK "HDFC Bank", BRANCH, CITY, DISTRICT, STATE "MAHARASHTRA", ISO3166 "IN-MH", MICR, IMPS/NEFT/RTGS/UPI flags, SWIFT — [probe](https://ifsc.razorpay.com/HDFC0000001). **Verified.**
- `GET https://ifsc.razorpay.com/XXXX0000000` → **HTTP/1.1 404 Not Found**, `ACAO: *` (so a bad IFSC can be detected cleanly in the browser) — [probe](https://ifsc.razorpay.com/XXXX0000000). **Verified.**
- Repo razorpay/ifsc: MIT, 396 stars, pushed_at 2026-10-04T14:08:48Z, not archived — [GitHub API](https://api.github.com/repos/razorpay/ifsc).
- Latest release v2.0.62, published 2026-09-01T11:55:03Z, assets include `IFSC.csv`, `IFSC.json`, `IFSC-list.json` — [GitHub releases API](https://api.github.com/repos/razorpay/ifsc/releases/latest).
- jsDelivr serves the repo with `ACAO: *` (`https://cdn.jsdelivr.net/gh/razorpay/ifsc@latest/README.md` → 200) — [probe](https://cdn.jsdelivr.net/gh/razorpay/ifsc@latest/README.md). **Verified** (for the README file; the dataset file path/size was not checked).
- Listed in public-apis Finance as "Razorpay IFSC … No auth … HTTPS Yes … CORS Unknown" — [README](https://github.com/public-apis/public-apis). My probe shows CORS is in fact `*`.

### Inferences
- The engine already reads IFSC from the cheque; a live lookup can confirm the code exists and give bank name + state (useful as a soft cross-check against the applicant's address state, never a hard rule — branch state ≠ residence state).
- `IFSC-list.json` (codes only) could be bundled for an offline existence check if the CDN or API is unreachable.
- Rate limits: none published that I found.

### Gaps
- No published SLA or rate limit for ifsc.razorpay.com.
- Size of `IFSC.json` / `IFSC-list.json` not measured (matters if bundled; Embarko page limit unknown here).

## 2. Indian pincode → state / district / city

### Takeaway
api.postalpincode.in works keyless over HTTPS with `ACAO: *`; Zippopotam.us is a verified backup with coarser data. data.gov.in needs a key (post-MVP). A pincode is not personal data on its own, but sending it alongside a name would be; send it alone.

### Cited Findings
- `GET https://api.postalpincode.in/pincode/110001` → **HTTP/1.1 200 OK**, `ACAO: *`, JSON `[{"Message":"Number of pincode(s) found:21","Status":"Success","PostOffice":[{…"District":"Central Delhi","State":"Delhi",…}]}]` — [probe](https://api.postalpincode.in/pincode/110001). **Verified.**
- `GET https://api.postalpincode.in/postoffice/Connaught` → 200, `ACAO: *` (search by post-office name) — [probe](https://api.postalpincode.in/postoffice/Connaught). **Verified.**
- Plain `http://api.postalpincode.in/pincode/110001` → **403 Forbidden** (no redirect); the public-apis row links the http docs page `http://www.postalpincode.in/Api-Details` — use the https API host only — [README](https://github.com/public-apis/public-apis).
- Maintainer of postalpincode.in: not identified; it is a third-party service, not India Post. Listed in public-apis as "PostalPinCode … No auth … CORS Unknown" — [README](https://github.com/public-apis/public-apis).
- `GET https://api.zippopotam.us/IN/110001` → **200 OK**, `access-control-allow-origin: *`, places with `"state": "New Delhi"`, lat/long — [probe](https://api.zippopotam.us/IN/110001). **Verified.** Note state label "New Delhi" differs from postalpincode's "Delhi".
- Other keyless India pincode rows in the README (not probed): MyPincode (mypincode.live), SearchPinCode (searchpincode.in, CORS "Yes"), Indian Pincode (indianpincode.com, CORS "Yes"); India LGD Index (states/districts with LGD codes, keyless, vercel) — [README](https://github.com/public-apis/public-apis). **Unverified.**
- "Open Government, India" data.gov.in is listed with `apiKey` auth — [README](https://github.com/public-apis/public-apis). Post-MVP tier.

### Inferences
- Use: map the pincode OCR'd from the Aadhaar address (if parsed) or typed by the applicant to a state, and compare with the address state the engine already reads. State-name normalisation is needed (Delhi / New Delhi / NCT of Delhi).
- For resilience, a static India Post pincode directory (data.gov.in "All India Pincode Directory") could be bundled, but downloading it needs the portal (key or manual download) — not checked.

### Gaps
- No published rate limit or owner for api.postalpincode.in; uptime history unknown.

## 3. Transliteration and Hindi

### Takeaway
Two keyless, CORS-open endpoints work today: Google Input Tools (transliteration, unofficial/undocumented) and MyMemory (translation, anonymous quota). The LibreTranslate public instance now requires a key. AI4Bharat's hosted xlit API host did not resolve. For the Hindi follow-up message, pre-written templates (as the app already has) are safer than live MT.

### Cited Findings
- `GET https://inputtools.google.com/request?text=namaste&itc=hi-t-i0-und&num=3` → **200 OK**, `ACAO: *`, body `["SUCCESS",[["namaste",["नमस्ते","नमसते","नामस्ते"],…]]]` — [probe](https://inputtools.google.com/request?text=namaste&itc=hi-t-i0-und&num=3). **Verified (works), but undocumented**: no public terms/SLA found for this endpoint.
- `GET https://api.mymemory.translated.net/get?q=hello&langpair=en|hi` → **200 OK**, `ACAO: *`, `translatedText` "नमस्ते", `quotaFinished:false`. Matches include crowd-sourced junk (e.g. "Ciao Mondo!" for hello→hi) — [probe](https://api.mymemory.translated.net/get?q=hello&langpair=en|hi). **Verified.**
- LibreTranslate public instance: `GET https://libretranslate.com/languages` → 200, `ACAO: *`; CORS preflight on `/translate` → 200 `ACAO: *`; but `POST /translate` returns `{"error":"Visit https://portal.libretranslate.com to get an API key"}` — [probe](https://libretranslate.com/translate). **Verified: key required → post-MVP** (or self-host; AGPL-3.0, 17,698 stars, pushed_at 2026-11-14 — [GitHub API](https://api.github.com/repos/LibreTranslate/LibreTranslate)). The public-apis README still says "No" auth — [README](https://github.com/public-apis/public-apis) — that row is out of date.
- AI4Bharat/IndicXlit: MIT, 146 stars, pushed_at 2023-10-13 (no pushes for ~3 years) — [GitHub API](https://api.github.com/repos/AI4Bharat/IndicXlit). `https://xlit-api.ai4bharat.org/tl/hi/namaste` → `curl: (6) Could not resolve host` — **not available**.

### Inferences
- Privacy: transliterating/translating an applicant's *name* via Google or MyMemory sends personal data to a third party; under DPDP this needs notice/consent. Use only for UI hints (e.g. showing a Devanagari rendering of a typed name for the applicant to confirm), or avoid.
- Name matching across scripts (Hindi-script name on a document vs Latin on PAN) is better done with an on-device rule table than a remote API.

### Gaps
- MyMemory's anonymous daily quota was not confirmed from its docs in this session (commonly cited as a few thousand words/day — unverified).
- No terms of use located for inputtools.google.com.

## 4. OCR

### Takeaway
No keyless OCR API exists that would beat the in-browser Tesseract already used. OCR.space is CORS-open but needs a key (its public demo key "helloworld" works technically but is meant for testing) and would upload identity documents to a third party — a poor DPDP fit. Keep OCR on-device.

### Cited Findings
- `GET https://api.ocr.space/parse/imageurl?apikey=helloworld&url=https://example.com/x.png` → **200 OK**, `ACAO: *`, `Access-Control-Allow-Headers: Content-Type, apikey`, body error E217 (test URL 404) — [probe](https://api.ocr.space/parse/imageurl?apikey=helloworld&url=https://example.com/x.png). **Verified CORS**; listed as `apiKey` in public-apis — [README](https://github.com/public-apis/public-apis).
- Other OCR rows (Optiic, Hirak OCR, FynePDF, Micro-SaaS AI Suite) are all `apiKey` — [README](https://github.com/public-apis/public-apis).
- tesseract.js: Apache-2.0, 38,831 stars, pushed_at 2026-05-17 — [GitHub API](https://api.github.com/repos/naptha/tesseract.js).

### Inferences
- Sending PAN/Aadhaar images to any remote OCR means full identity data leaves the device; with Aadhaar it also risks sending the full 12-digit number (forbidden by the project's own rule). Not recommended even post-MVP without a DPA with the vendor.

### Gaps
- OCR.space free-tier limits not re-checked from its pricing page in this session.

## 5. Email and phone format validation

### Takeaway
Use libphonenumber-js from jsDelivr (library, no network call per number, `ACAO: *`) for Indian mobile format. For email, syntax checks belong on-device; two keyless disposable-domain checks are CORS-open (Kickbox Open, UserCheck/MailCheck.ai). All phone-validation APIs in the list need keys.

### Cited Findings
- `https://cdn.jsdelivr.net/npm/libphonenumber-js@1.11.4/bundle/libphonenumber-min.js` → **200**, `access-control-allow-origin: *` — [probe](https://cdn.jsdelivr.net/npm/libphonenumber-js@1.11.4/bundle/libphonenumber-min.js). Latest npm version 1.13.16 — [npm registry](https://registry.npmjs.org/libphonenumber-js/latest). Repo MIT, 3,003 stars, pushed_at 2026-11-10 — [GitHub API](https://api.github.com/repos/catamphetamine/libphonenumber-js). Upstream google/libphonenumber: Apache-2.0, 18,353 stars, pushed_at 2026-11-13 — [GitHub API](https://api.github.com/repos/google/libphonenumber). **Verified (CDN reachable).**
- Phone APIs in public-apis (Numverify, Numlookup, Veriphone, Abstract, Cloudmersive) are all `apiKey` — [README](https://github.com/public-apis/public-apis).
- `GET https://open.kickbox.com/v1/disposable/example.com` → **200**, `Access-Control-Allow-Origin: https://policynest.embarko.app` (origin reflected), `{"disposable":false}` — [probe](https://open.kickbox.com/v1/disposable/example.com). **Verified.**
- `GET https://api.usercheck.com/domain/example.com` (MailCheck.ai's docs point here) → **200**, `access-control-allow-origin: *` — [probe](https://api.usercheck.com/domain/example.com). **Verified.**
- Disify: `https://www.disify.com/api/domain/example.com` → **301** to `https://disify.com/…` (redirect target not probed) — **Unverified.**

### Inferences
- Send only the email *domain* (not the full address) to Kickbox/UserCheck; a domain like gmail.com is not personal data. Low value for a POSP flow; optional.
- Pin an exact libphonenumber-js version (CLAUDE.md: exact versions); the "min" metadata is enough for IN mobile validation.

### Gaps
- Rate limits for Kickbox Open and UserCheck keyless use not checked.

## 6. Indian public holidays for SLA day counting

### Takeaway
Nager.Date does **not** cover India (204 No Content; IN absent from its country list), and OpenHolidays returns an empty list for IN. Three keyless, `ACAO: *` sources do return India 2026, but they disagree (Holi 3 vs 4 March; 23 vs 16 holidays), and all are small or unknown projects. For an SLA calculator, a hard-coded central-government gazetted list for 2026 (from the DoPT notification) is more defensible; an API can be a cross-check.

### Cited Findings
- `GET https://date.nager.at/api/v3/PublicHolidays/2026/IN` → **HTTP/1.1 204 No Content**, `access-control-allow-origin: *` — [probe](https://date.nager.at/api/v3/PublicHolidays/2026/IN). `/api/v3/AvailableCountries` does not contain `"countryCode":"IN"` — [probe](https://date.nager.at/api/v3/AvailableCountries). **Verified: no India data.** (Repo active: MIT, 1,443 stars, pushed_at 2026-11-11 — [GitHub API](https://api.github.com/repos/nager/Nager.Date).)
- `GET https://openholidaysapi.org/PublicHolidays?countryIsoCode=IN&validFrom=2026-01-01&validTo=2026-12-31&languageIsoCode=EN` → 200, `ACAO: *`, body `[]` — [probe](https://openholidaysapi.org/PublicHolidays?countryIsoCode=IN&validFrom=2026-01-01&validTo=2026-12-31&languageIsoCode=EN). **Verified: no India data.**
- India Public Holidays API (public-apis row "Official Indian public holidays for the Central government and 36 states/UTs", keyless) — [README](https://github.com/public-apis/public-apis). Docs at calendar-api-web.vercel.app; the API itself is at `https://calendar-api-d7a8.onrender.com`. `GET /v1/holidays?country=IN&year=2026` → **200**, `access-control-allow-origin: *`, entries carry `"source":"https://www.india.gov.in/calendar"`, include "Holika dahan / Dolyatra" (3 Mar), "Holi" (4 Mar), "Diwali (Deepavali)" (8 Nov); supports `region` (2-letter state) and `/v1/holidays/range`, `/v1/date/is-holiday` — [docs](https://calendar-api-web.vercel.app/docs). Repo: github.com/shrinivas-sn/calendar-api (stars/pushed_at not returned by my API call). Render free hosting can cold-start slowly. **Verified CORS; reliability unknown.**
- `GET https://caldays.com/api/holidays/in` → **200**, `ACAO: *`, `"year":2026`, `"license":"CC BY 4.0"`, `"count":23`, Holi 2026-03-03, Diwali 2026-11-08; mixes regional holidays (Pongal, Thiruvalluvar Day, Gudi Padwa, Ugadi) — [probe](https://caldays.com/api/holidays/in). **Verified CORS.**
- `GET https://holidayexplore.com/api/v1/holidays?country=IN&year=2026` → **200**, `ACAO: *`, `"total_holidays":16`, Holi 2026-03-04, Republic Day typed "Public / Statutory Holiday"; also has `/api/v1/working-days` (400 without params) — [probe](https://holidayexplore.com/api/v1/holidays?country=IN&year=2026), [docs](https://holidayexplore.com/api-docs/). **Verified CORS.**
- Conflict: Holi 2026 is 3 Mar in caldays vs 4 Mar in HolidayExplore and the India Public Holidays API (which lists Holika dahan on 3 Mar) — [caldays](https://caldays.com/api/holidays/in); [HolidayExplore](https://holidayexplore.com/api/v1/holidays?country=IN&year=2026).
- Google public India holiday ICS (`calendar.google.com/calendar/ical/en.indian%23holiday%40group.v.calendar.google.com/public/basic.ics`) → 200 `text/calendar` but **no ACAO header** → a browser fetch from the site would be blocked — [probe](https://calendar.google.com/calendar/ical/en.indian%23holiday%40group.v.calendar.google.com/public/basic.ics). **Verified: not usable from the browser.**
- Calendarific, Abstract, Festivo, Checkiday need keys — [README](https://github.com/public-apis/public-apis). Post-MVP.

### Inferences
- SLA counting for a broker should use the employer's (InsuranceDekho/PolicyNest) holiday list, which no API provides. Recommend an embedded JSON of gazetted 2026 central holidays, labelled with its source, plus weekends; optionally show the API value as a check.

### Gaps
- The DoPT 2026 gazetted list itself was not fetched in this session, so which Holi date is "official" was not confirmed here.

## 7. Replacing simulated checks (PAN, penny-drop, IRDAI registry, face match)

### Takeaway
None of the four can honestly be replaced with a free, keyless, CORS-open real service. PAN verification, penny-drop and Aadhaar e-KYC are regulated, partner-only or paid, keyed APIs (and keys must never sit in a static page). There is no public IRDAI/IIB POSP registry API. Face match can move from a fixed 0.91 to a real **on-device** score using an in-browser library — the only one of the four that can become "real" in the MVP without a server.

### Cited Findings
- The source pack says no live PAN (NSDL/UTIITSL), penny-drop (NPCI/IMPS), IRDAI/IIB registry or UIDAI keys were provided, and proposes adapter interfaces that later connect to vendors such as Cashfree, Karza, Bureau or Sandbox.co.in — [MISSING_SOURCE_MATERIALS.md §2.2](../../MISSING_SOURCE_MATERIALS.md).
- public-apis lists "API Setu" (Indian government platform with KYC, business, education APIs) as "No" auth, CORS "Yes" — [README](https://github.com/public-apis/public-apis). I did not probe it; my understanding is that its KYC APIs require onboarding as a registered consumer, so the "No auth" label likely refers to browsing the catalogue. **Unverified.**
- Other KYC-adjacent rows are keyed: gstinapi (GSTIN verify, `apiKey`), Neetix Liveliness (face liveness + 1:1 match, `apiKey`), SkyBiometry, Hirak FaceAPI, Cloudmersive (`apiKey`) — [README](https://github.com/public-apis/public-apis).
- `https://www.irdai.gov.in/` → **308 Permanent Redirect** (website only; no API found) — [probe](https://www.irdai.gov.in/).
- The public-apis README has no PAN, penny-drop, IRDAI or IIB entry — [README](https://github.com/public-apis/public-apis) (grep for india/ifsc/face/etc. on the 14 Nov 2026 copy).

### Inferences
- PAN: the MVP can keep the format check (AAAAA9999A, 4th char "P" for individuals) on-device; real verification = post-MVP via a keyed vendor behind a server.
- Penny-drop: the free IFSC lookup (section 1) gives a *real* partial check (branch exists, IMPS enabled) without moving money; the holder-name match must stay simulated.
- IRDAI/IIB: keep simulated; label it.
- Face match: candidates are in-browser libraries (e.g. face-api.js or MediaPipe Face Landmarker via jsDelivr), which keep the selfie on the device — not verified in this session; weights would have to be served same-origin or from an allowed CDN under the CSP.
- Never put any vendor key in PolicyNest.html: anyone can read it. Keyed integrations need a server/proxy, which the current hosting does not have.

### Gaps
- Sandbox/test-mode terms for Cashfree, Setu, Sandbox.co.in, Karza and Bureau were not researched here (other researchers may cover them).
- No confirmation of current API Setu consumer onboarding rules.

## Summary table

| Need | Pick (MVP, keyless) | Probe result | Data leaving device | Status |
| --- | --- | --- | --- | --- |
| IFSC | ifsc.razorpay.com/{IFSC} | 200 / 404, ACAO `*` | IFSC only (not personal) | Verified |
| IFSC offline | razorpay/ifsc release JSON via jsDelivr | 200, ACAO `*` (README) | none | Partly verified |
| Pincode | api.postalpincode.in/pincode/{pin} (https only) | 200, ACAO `*`; http → 403 | pincode only | Verified |
| Pincode backup | api.zippopotam.us/IN/{pin} | 200, ACAO `*` | pincode only | Verified |
| Transliteration | inputtools.google.com (unofficial) | 200, ACAO `*` | text sent (avoid names) | Verified, no ToS |
| Translation | api.mymemory.translated.net | 200, ACAO `*` | text sent | Verified, noisy |
| Translation | libretranslate.com | key now required | — | Post-MVP |
| Transliteration | AI4Bharat xlit API | host does not resolve | — | Unavailable |
| OCR | keep Tesseract.js on-device | OCR.space: ACAO `*` but keyed | images (bad fit) | Keep local |
| Phone | libphonenumber-js@exact via jsDelivr | 200, ACAO `*` | none | Verified |
| Email disposable | open.kickbox.com / api.usercheck.com | 200, origin reflected / `*` | domain only | Verified |
| Holidays | Nager.Date | 204, no IN | — | Not usable |
| Holidays | calendar-api-d7a8.onrender.com, caldays.com, holidayexplore.com | 200, ACAO `*`, dates disagree | year only | Verified CORS; embed a list instead |
| Holidays ICS | Google public calendar | 200, no ACAO | — | Blocked in browser |
| PAN / penny-drop / IRDAI / Aadhaar | none keyless | — | — | Keep simulated; post-MVP keyed + server |
| Face match | on-device library | not probed | none | Unverified candidate |
