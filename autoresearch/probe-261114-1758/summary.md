# Probe summary

- Topic: PS-01 AI-first onboarding, from the brief, rulebook, specimens and both workbooks
- Mode: autonomous; rounds: 9; constraints: 46; status: SATURATED
- Unresolved conflicts: 9 (conflicts.md)

## Net-new constraints by round

| Round | Personas | Net new | Total | Saturation window |
|---|---|---|---|---|
| 1 | Domain Expert, End User | 8 | 8 | 0/3 |
| 2 | Skeptic, Edge-Case Hunter | 10 | 18 | 0/3 |
| 3 | Ops Engineer, Security Reviewer | 10 | 28 | 0/3 |
| 4 | Contradiction Finder, Scope Guardian | 9 | 37 | 0/3 |
| 5 | Domain Expert, Skeptic, Edge-Case Hunter | 4 | 41 | 0/3 |
| 6 | End User, Contradiction Finder | 3 | 44 | 0/3 |
| 7 | Ops Engineer | 1 | 45 | 1/3 |
| 8 | Edge-Case Hunter | 1 | 46 | 2/3 |
| 9 | Skeptic, Contradiction Finder, End User | 0 | 46 | 3/3 |

## Ready-to-run config

```
/autoresearch
Goal: Raise application-level decision accuracy on the 600-application test set without losing REJECT recall
Scope: policynest_mvp/PolicyNest.html (ENGINE block only)
Metric: accuracy vs application_truth.final_decision (higher is better)
Verify: node eval/run_eval.js policynest_mvp/PolicyNest.html <datasets dir> eval/out   (then read accuracy from eval/out/eval_results.json)
Guard: REJECT recall >= 98% and no APPROVE of a true REJECT
Iterations: 15
```
Caveat: the engine is already at 100.0% in-sample (CLAUDE.md), so this loop has no headroom on the 600. Use it only with a held-out split or the 3,000-application workbook.
