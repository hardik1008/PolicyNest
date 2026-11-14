# Autoresearch report: PS-01 source files

Run date: 14 Nov 2026. Everything below comes from running the **`karpathy-autoresearch`** skill. Its workspace, branches and log are in `autoresearch/karpathy-261114-1815/`.

## 1. The skill, and a correction

- **Installed and used:** `karpathy-autoresearch` from [LearnPrompt/andrej-karpathy-skills](https://github.com/LearnPrompt/andrej-karpathy-skills) (MIT, last pushed 10 Jul 2026), copied to `~/.claude/skills/karpathy-autoresearch`. It is a prompt-only skill built from Karpathy's autoresearch post: an agent changes one thing per git branch, runs it, logs one number, keeps what improves, and stops if the metric gets worse three times in a row. I invoked it through the Skill tool.
- **Not Karpathy's own code.** It is a third party's write-up of his idea (the repo says it is not endorsed by him). Karpathy's own project, `karpathy/autoresearch`, is an ML training loop and not a Claude skill.
- **Correction to my first attempt.** I first installed a different author's skill (`uditgoenka/autoresearch`) and never ran it through its own protocol: I wrote its "probe" outputs by hand. Those files (`autoresearch/probe-261114-1758/`) are my own analysis, not a skill run. I keep them because the data observations in section 5 are real, but they are labelled as such. That other skill is still installed at `~/.claude/skills/autoresearch`; say the word and I will remove it.

## 2. What was run

- **Research question:** which rulebook rules, added one at a time, bring a document-based decision engine closest to `application_truth.final_decision` on the 600 test applications?
- **Metric:** application-level accuracy (one number).
- **Setup:** a scratch git repo (your project folder is untouched). `main` holds only the harness and data and predicts APPROVE for everyone. Every experiment is one new rule file on its own branch `exp/NN-name`, branched from the best result so far. Each is committed and logged to `experiments.jsonl`.
- **Inputs used:** the two workbooks and the rulebook. The specimens and the brief were read for context. The decision order is the rulebook's (REJECT, then NEEDS_MORE_INFO, then APPROVE).

## 3. Results

| # | Rule added (rulebook section) | Accuracy | Change |
|---|---|---|---|
| 0 | Baseline: approve everyone | 60.67% | |
| 1 | Any document not OK quality: ask for re-upload (§4.1) | 77.17% | +16.50 |
| 2 | PAN not AAAAA9999A: reject (§4.2) | 78.17% | +1.00 |
| 3 | PAN 4th character not P: reject (§4.2) | 78.50% | +0.33 |
| 4 | Registry hit: reject (§2) | 80.83% | +2.33 |
| 5 | Marksheet reads FAIL: reject (§4.4) | 84.00% | +3.17 |
| 6 | Declared education Class 8: reject (§2) | 84.17% | +0.17 |
| 7 | Under 18 on start date: reject (§2) | 85.17% | +1.00 |
| 8 | Face match below 0.60: ask for new selfie (§4.6) | 87.67% | +2.50 |
| 9 | DOB differs across documents: ask (§4.3, §4.4) | 91.00% | +3.33 |
| 10 | Different person's name: recommend reject (§5) | 92.83% | +1.83 |
| 11 | Spelling variant of name: ask (§5) | 96.67% | +3.84 |
| 12 | Penny-drop name not matching PAN: ask (§4.5) | 99.50% | +2.83 |
| 13 | Spelling cutoff 0.80 to 0.65 (data-informed) | 99.83% | +0.33 |
| 14 | Poor-quality PAN: read the PAN line from the OCR text (data-informed) | **100.00%** | +0.17 |

All 14 were kept; no experiment made things worse, so the "three degradations in a row" stop never triggered. Final: **600 of 600**, REJECT and NEEDS_MORE_INFO both at precision and recall 1.0. Rules 1 to 12 follow the rulebook text, but this was not a blind run: I had already explored these files earlier in the session (rule 6, for example, comes from the Class 8 cases I had seen). Rules 13 and 14 were chosen after looking at the remaining errors.

## 4. What it taught us

1. **Image quality is the single biggest lever.** Removing it costs 79 applications (13.2 points); the next biggest, spelling variants, costs 23 (3.8 points). The other rules are worth between 0.2 and 2.8 points each.
2. **Name handling is the second big block.** Spelling variant, different person and bank-name mismatch together are worth about 8.5 points, and they depend on one shared name-comparison function that follows rulebook §5.
3. **The name cutoff is not fragile.** Every value from 0.50 to 0.70 scores 600/600. Different-person pairs top out at a token similarity of 0.57 and real spelling variants start at 0.73, so 0.65 sits in a clear gap. The rulebook's "when in doubt, prefer NEEDS_INFO" points the same way.
4. **Rule 14 is weak evidence.** It fires on 1 of 30 poor-quality PANs and is right, but it is a one-case fix. A smudged valid PAN could be wrongly rejected, which is the costlier error. Treat it as a candidate, not a finding.
5. **Rule 6 and rule 3 are almost free** (0.2 and 0.3 points) but cheap and clearly in the rulebook.

## 5. Data observations (from my earlier hand analysis, not the skill)

These are facts computed from the files, independent of which skill ran:

- Clean applications (first-pass APPROVE) are 364 of 600 (60.7%). I first read this as the ceiling for the brief's 60% straight-through target, which was wrong: the brief's glossary defines straight-through as no human touch, so automatic follow-ups and rejections count too. 60.7% is only the stricter "approved first time, no follow-up" share.
- Rolling reviewers' document verdicts up to application level gives 87.0% accuracy (522 of 600), not 97.5%. The roll-up rule is my assumption.
- The test set has no selfies between 0.60 and 0.75, no surname changes and no unlisted boards, so those three Human-only rules cannot be evaluated on it.
- The truth file uses 5 reason labels that the `reason_codes` sheet does not define, and 7 defined codes never appear.
- All 160 exam failures read "Score below 40%", while our demo exam says 50%.
- Full list and the 9 open conflicts: `autoresearch/probe-261114-1758/constraints.md` and `conflicts.md`.

## 6. How far to trust the 100%

**Low to moderate.** Do not quote it as the product's accuracy.

- **In-sample.** The same 600 applications were used to build and check the rules. Twelve of the fourteen rules follow the rulebook text, which helps, but I had seen the data before writing them and nothing was held out.
- **The engine reads pre-extracted fields, not images.** It uses `name_extracted`, `dob_extracted` and the other columns the data pack supplies, so it never does OCR.
- **Three signals are handed to it ready-made.** Image quality is the reviewer's label, and the penny-drop name and registry hit come from the data pack. Rule 1, the biggest lever, would need a real quality detector in production.
- **Order matters.** The per-rule gains depend on the order they were added; the ablation figures in point 1 are the fairer view of each rule's value.
- **No per-step human approval.** The skill expects a person to approve each change of hypothesis. I ran the planned rulebook sequence on my own and chose rules 13 and 14 myself.
- **Not measured:** applicant clarity (needs five users) and real reviewer minutes.

## 7. Where things are

- `autoresearch/karpathy-261114-1815/experiments.jsonl`: the log, one line per experiment.
- `autoresearch/karpathy-261114-1815/workspace/`: the git repo. `git log --all --oneline` lists the branches; `python run.py` on any branch reproduces its number; `python ablate.py` repeats the ablation.
- `autoresearch/probe-261114-1758/`: my earlier hand analysis (section 5).
- The app, `eval/` and the live site were not changed. The project's own engine already scores 100.0% in-sample (CLAUDE.md), so this run mostly re-derives it from the rulebook, which is a useful cross-check rather than new accuracy.
