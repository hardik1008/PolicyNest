# Held-out evaluation set (FR-60)

Purpose: test the engine on applications that were written by the team and labelled independently by the user, **before** the engine saw them. The in-sample result (600 test-set applications, 100.0%) was tuned on the same data and is not a clean estimate. This set is the only clean check we can run offline.

## What goes in

30 to 40 constructed applications, in the same three-file format as the test set:

| File | One row per | Header (copied from `04_DATASETS`) |
| --- | --- | --- |
| `documents.csv` | document (six per application: PAN, AADHAAR_FRONT, AADHAAR_BACK, CLASS10_MARKSHEET, CANCELLED_CHEQUE, SELFIE) | `template/documents.csv` |
| `application_truth.csv` | application (typed details plus the label) | `template/application_truth.csv` |
| `applications.csv` | application (`created_at` is read by the runner; `state` and `gender` feed the breakdowns) | `template/applications.csv` |

Header-only templates are in `eval/holdout/template/`. Copy them to a new folder and fill in rows. The header lines are byte-identical to `04_DATASETS/`.

Rules for the data:

- Synthetic only. Do not use real people's documents, and do not open `05_SPECIMEN_DOCUMENTS/sample_specimens`.
- Aadhaar: last four digits only, in `ocr_text` and in `application_truth.csv`. Never a full 12-digit number.
- `final_decision` must be one of `APPROVE`, `NEEDS_MORE_INFO`, `REJECT`. The scorer has no other label.

## Required coverage

The set must include at least one case for each of these. Count them and report the counts.

1. Selfie face-match score between 0.60 and 0.75 (rulebook s.4.6, s.9).
2. Surname changed after marriage (rulebook s.5 and s.9).
3. Class 10 marksheet from a board not on the recognised list (rulebook s.4.4 and s.9).
4. An applicant dispute (rulebook s.9). The engine has no dispute input, so a dispute case is scored on the decision it disputes. Put `DISPUTE` in `decision_reasons`. The score does not measure how a dispute is resolved.
5. Two selfie failures in a row below 0.60 (rulebook s.4.6, s.7: fraud-desk referral).

How the scorer maps routed cases (from `eval/run_eval.js`): a `HUMAN_REVIEW` with a NAME_MISMATCH is scored `REJECT`. Any other `HUMAN_REVIEW` is scored `NEEDS_MORE_INFO`. Label each routed case with the decision a correct reviewer would reach under the rulebook, not with the engine's routing.

## Procedure (order matters)

1. **Write the set.** Create `eval/holdout/set_<YYYYMMDD>/` with the three CSVs. Do not run the engine on it.
2. **Label before any engine run (the user labels).** The user fills `application_truth.csv` (`final_decision`, `decision_reasons`) independently, from the rulebook alone. The engine's author (Claude) does not see these labels, and does not see any engine output for these applications, before they are frozen. Keep notes of who labelled and when.
3. **Freeze the labels.** Hash all three CSVs and append them to `eval/holdout/LABELS.sha256`, together with the date and the `engine_sha256` current at that time (from `eval/out/eval_results.json`). Do this before step 5. If any CSV changes after this point, the set is no longer held out; start a new set.
   ```bash
   S=eval/holdout/set_<YYYYMMDD>
   { echo "# set_<YYYYMMDD> frozen $(date -u +%F) UTC; labelled by the user, independently of the engine"
     echo "# engine_sha256 at freeze: $(python -c 'import json; print(json.load(open("eval/out/eval_results.json"))["engine_sha256"])')"
     sha256sum $S/documents.csv $S/application_truth.csv $S/applications.csv; } >> eval/holdout/LABELS.sha256
   ```
   `eval/out/eval_results.json` records the engine as of its last run. If `policynest_mvp/PolicyNest.html` has changed since that run, re-run `run_eval.js` on the in-sample set first, so the frozen hash is the current one.
4. **Re-verify the hashes before the run.** All three CSVs must still match the hashes recorded in step 3. Cite the three hashes in the report.
   ```bash
   grep 'set_<YYYYMMDD>/' eval/holdout/LABELS.sha256 | sha256sum -c
   ```
   If any line says FAILED, stop: the set changed after it was frozen.
5. **Run.** `run_eval.js` needs `papaparse`, which is not in the repo. Install it in a folder outside the repo (for example `npm i papaparse` in a scratch folder) and point `NODE_PATH` at its `node_modules`. The version used for the committed results was not recorded; 5.7.1 gives identical predictions on the 600-application set.
   ```bash
   NODE_PATH=<folder>/node_modules node eval/run_eval.js policynest_mvp/PolicyNest.html eval/holdout/set_<YYYYMMDD> eval/holdout/out_<YYYYMMDD>
   ```
   Outputs: `eval_results.json` and `eval_predictions.csv` in the output folder.
6. **Check the engine hash.** `engine_sha256` in the results must equal the value recorded at freeze time in `LABELS.sha256`. If it does not, the engine changed after the set was frozen; say so in the report.
7. **Report.** State the result as "held-out, user-labelled, n = N", with the three CSV hashes, the labels date and the engine hash. Report it separately from the in-sample figures. Do not merge the two. Include the coverage counts from above.

## Files in this folder

- `README.md`: this file.
- `template/`: header-only CSVs (the three test-set headers).
- `LABELS.sha256`: created at step 3 only. It is not created yet, because no labels exist.
- `set_<YYYYMMDD>/` and `out_<YYYYMMDD>/`: created per run, not committed by default.
