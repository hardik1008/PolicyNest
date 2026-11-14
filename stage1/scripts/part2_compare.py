"""Part 2, step 3 (only after part2_hand_decisions.csv is written and hashed): open the sealed truth for the 20 cases and compare.
Usage: python part2_compare.py <scratch folder>/blind"""
import sys, os, csv, collections
from common import *
S = sys.argv[1]
T = {r['application_id']: r for r in csv.DictReader(open(os.path.join(S, 'sealed', 'truth.csv'), encoding='utf-8'))}
H = {r['application_id']: r['is_hard_case'] == '1' for r in csv.DictReader(open(os.path.join(S, 'flags.csv')))}
L = {r['doc_id']: r for r in csv.DictReader(open(os.path.join(S, 'sealed', 'doc_labels.csv'), encoding='utf-8'))}
D = collections.defaultdict(list)
for r in csv.DictReader(open(os.path.join(S, 'docs_inputs.csv'), encoding='utf-8')):
    D[r['application_id']].append(L[r['doc_id']]['human_verdict'])
def roll(v):
    if 'REJECT' in v: return 'REJECT'
    if any(x in ('REUPLOAD', 'NEEDS_INFO') for x in v): return 'NEEDS_MORE_INFO'
    return 'APPROVE'
M = {r['application_id']: r for r in csv.DictReader(open(os.path.join(OUT, 'part2_hand_decisions.csv'), encoding='utf-8'))}
rows = []
for a, m in M.items():
    t = T[a]
    rows.append([a, 'TRUE' if H[a] else 'FALSE', m['my_decision'], m['my_reason_codes'], t['final_decision'], t['decision_reasons'],
                 'agree' if m['my_decision'] == t['final_decision'] else 'DISAGREE', roll(D[a]),
                 'agree' if roll(D[a]) == t['final_decision'] else 'differs'])
write_csv('part2_comparison.csv', ['application_id', 'is_hard_case', 'my_decision', 'my_reasons', 'truth_decision', 'truth_reasons', 'my_vs_truth', 'reviewers_doc_verdicts_rolled_up', 'rollup_vs_truth'], rows)
print(sum(r[6] == 'agree' for r in rows), 'of', len(rows), '| hard:', sum(1 for r in rows if r[1] == 'TRUE'), '| rollup agrees', sum(r[8] == 'agree' for r in rows))
allroll = sum(roll(D[a]) == T[a]['final_decision'] for a in T); print('rollup on all 600', allroll, len(T))
