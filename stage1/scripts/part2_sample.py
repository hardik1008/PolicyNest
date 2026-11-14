"""Part 2, step 1: draw the 20 applications with a fixed seed, using only inputs and the hard-case flag.
Usage: python part2_sample.py <scratch folder>   -> writes <scratch>/sample_ids.txt and ../tables/part2_sample_ids.csv
Design fixed before drawing: 10 hard cases at random; 10 non-hard cases = 3 with a bad-quality document, 1 low face score,
1 with a PAN that is malformed or not type P, 1 on the IRDAI registry, 1 with education declared below Class 10 or unusual, 3 plain at random.
(Strata use only things visible in the inputs, never the decision.)"""
import sys, os, csv, random, re, collections
from common import *
S = sys.argv[1]
A = {r['application_id']: r for r in csv.DictReader(open(os.path.join(S, 'inputs_apps.csv'), encoding='utf-8'))}
F = {r['application_id']: r['is_hard_case'] == '1' for r in csv.DictReader(open(os.path.join(S, 'flags.csv')))}
D = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(S, 'docs_inputs.csv'), encoding='utf-8')):
    D[r['application_id']][r['doc_type']] = r
rng = random.Random(20261114)
ids = sorted(A)
def quality(a): return any(d['image_quality'] != 'OK' for d in D[a].values())
def face_low(a):
    s = D[a]['SELFIE']['face_match_score']; return s != '' and float(s) < 0.60
def pan_bad(a):
    p = A[a]['declared_pan']; return not re.fullmatch(r'[A-Z]{3}P[A-Z][0-9]{4}[A-Z]', p)
def registry(a): return A[a]['irdai_posp_registry_hit'] == '1'
def edu(a): return A[a]['declared_education'] not in ('Class 12', 'Graduate', 'Post-graduate', 'Class 10')
nonhard = [a for a in ids if not F[a]]
hard = [a for a in ids if F[a]]
chosen = rng.sample(hard, 10)
used = set(chosen)
def draw(pred, k):
    pool = [a for a in nonhard if a not in used and pred(a)]
    got = rng.sample(pool, k); used.update(got); return got, len(pool)
strata = [('bad-quality document', quality, 3), ('face score < 0.60', face_low, 1), ('PAN malformed or not type P', pan_bad, 1),
          ('IRDAI registry hit', registry, 1), ('education unusual', edu, 1), ('plain', lambda a: True, 3)]
rows = [[a, 'hard (random)'] for a in chosen]
for name, pred, k in strata:
    got, n = draw(pred, k); print(name, 'pool', n, got); rows += [[a, name] for a in got]
rows.sort()
write_csv('part2_sample_ids.csv', ['application_id', 'stratum'], rows)
open(os.path.join(S, 'sample_ids.txt'), 'w').write('\n'.join(r[0] for r in rows))
print(len(rows), 'hard', sum(1 for r in rows if F[r[0]]))
print(collections.Counter(A[a]['declared_education'] for a in ids))
