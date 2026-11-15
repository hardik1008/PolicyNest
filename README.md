# PolicyNest

**AI-first onboarding for POSP insurance agents.** This is a demo built for the Masters' Union Applied AI Challenge, problem PS-01 (problem owner: InsuranceDekho). PolicyNest Insurance Brokers is fictional, and all data is synthetic.

- **Live demo:** https://policynest.embarko.app. Add `?demo=1` to open the Demo controls and run the brief's test scenarios T1–T10 with synthetic documents.
- **What it does:**
  - reads the applicant's documents with on-device OCR;
  - cross-checks them against the onboarding rulebook, with the PAN card as the anchor;
  - decides approve, needs more info, or reject, citing a rule for every reason;
  - asks for everything missing in one message (English or Hindi);
  - routes judgement calls to a reviewer, with the evidence side by side.
- **Measured:** 600 of 600 test applications decided correctly (100.0%). This is **in-sample**: the rules were refined on the same set, and the first run scored 98.0%. Details are in [`eval/EVALUATION_REPORT.md`](eval/EVALUATION_REPORT.md).
- **Simulated, and labelled as such in the app:** PAN verification, penny drop, face match and the IRDAI registry. No government or bank service is called.

## Start here

| Document | What it covers |
|---|---|
| [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) | Everything built so far, how it was checked, metrics, and what is left |
| [`PRD.md`](PRD.md) | Requirements (FR-01 to FR-73) and the build plan |
| [`PRODUCT.md`](PRODUCT.md) | Goal-by-goal status |
| [`BUILD_LOG.md`](BUILD_LOG.md) | Build record with commits and live checks |
| [`docs/adr/`](docs/adr/) | Architecture decisions |

## Run locally

```bash
python policynest_mvp/build_site.py
python -m http.server 8000 --directory policynest_mvp/site
python tools/check_pack.py                     # static checks (engine hash, JS syntax, build)
python tools/t1_t10.py http://localhost:8000   # brief scenarios T1–T10 (needs Python Playwright)
```

The whole app is one file, [`policynest_mvp/PolicyNest.html`](policynest_mvp/PolicyNest.html). The rule engine sits between `ENGINE:START` and `ENGINE:END`; its SHA-256 is pinned, and the evaluation scores exactly that code.

The `01_…` to `08_…` folders hold the PS-01 challenge source package (brief, rulebook, synthetic datasets, specifications).
