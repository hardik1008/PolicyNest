"""Part 1: process map of today's journey from stage_events (PS-01_posp_applications.xlsx).
Run:  python part1_process_map.py   -> writes ../tables/process_map_*.csv and prints the checks."""
import collections, json
from common import *

book = read_xlsx(APPS_XLSX)
apps_raw = sheet(book, 'applications')
ev_raw = sheet(book, 'stage_events')

# --- deduplicate applications (exact duplicate rows) --------------------------
apps = {}
dups = 0
for a in apps_raw:
    if a['application_id'] in apps:
        assert a == apps[a['application_id']], 'duplicate row is not exact'
        dups += 1
    else:
        apps[a['application_id']] = a
ev_keys = [tuple(e.values()) for e in ev_raw]
ev_dups = len(ev_keys) - len(set(ev_keys))
print('application rows', len(apps_raw), 'unique', len(apps), 'exact duplicate rows removed', dups)
print('stage_events rows', len(ev_raw), 'exact duplicate event rows', ev_dups)

by = collections.defaultdict(list)
for i, e in enumerate(ev_raw):
    by[e['application_id']].append((float(e['event_time']), i, e['event'], e['actor'], e['note']))
for l in by.values():
    l.sort()
assert set(by) == set(apps)


def hrs(a, b):
    return (b - a) * 24.0          # serial days -> hours


OUTCOME = {'KYC_VERIFIED', 'DOC_RETURNED', 'REJECTED'}
inst = collections.defaultdict(list)          # step -> hours, one value per instance
enter = collections.Counter()
lost = collections.Counter()
lost_reason = collections.defaultdict(collections.Counter)
first_outcome = collections.Counter()
last_event = {}
returned_apps = set()
replied_apps = set()
e2e = []

for aid, l in by.items():
    last_event[aid] = l[-1]
    names = [x[2] for x in l]
    t = {}
    for x in l:
        t.setdefault(x[2], x[0])
    enter['2 Upload documents'] += 1
    if 'DOCS_SUBMITTED' not in t:
        lost['2 Upload documents'] += 1
        lost_reason['2 Upload documents'][l[-1][4]] += 1
        continue
    inst['2 Upload documents'].append(hrs(t['APPLICATION_STARTED'], t['DOCS_SUBMITTED']))
    enter['3 Wait for a reviewer'] += 1
    inst['3 Wait for a reviewer'].append(hrs(t['DOCS_SUBMITTED'], t['REVIEW_STARTED']))
    enter['4 First review'] += 1
    j = names.index('REVIEW_STARTED')
    start = l[j][0]
    first = True
    kyc_t = None
    j += 1
    while j < len(l):
        n = l[j][2]
        if n in OUTCOME:
            if first:
                inst['4 First review'].append(hrs(start, l[j][0]))
                first_outcome[n] += 1
                first = False
            else:
                inst['4c Re-check after fix'].append(hrs(start, l[j][0]))
            if n == 'REJECTED':
                lost['4 First review'] += 1
                lost_reason['4 First review'][l[j][4]] += 1
            elif n == 'KYC_VERIFIED':
                kyc_t = l[j][0]
            elif n == 'DOC_RETURNED':
                returned_apps.add(aid)
                if j + 2 < len(l) + 0 and l[j + 1][2] == 'DOC_REUPLOADED':
                    replied_apps.add(aid)
                    inst['4a Applicant fixes returned documents'].append(hrs(l[j][0], l[j + 1][0]))
                    inst['4b Wait for re-check'].append(hrs(l[j + 1][0], l[j + 2][0]))
                    start = l[j + 2][0]
                    j += 2
                else:
                    lost['4a Applicant fixes returned documents'] += 1
                    lost_reason['4a Applicant fixes returned documents'][l[j + 1][4]] += 1
        j += 1
    if kyc_t is None:
        continue
    enter['5 Start training'] += 1
    if 'TRAINING_STARTED' not in t:
        lost['5 Start training'] += 1
        lost_reason['5 Start training'][last_event[aid][4]] += 1
        continue
    inst['5 Start training'].append(hrs(kyc_t, t['TRAINING_STARTED']))
    enter['6 Training (15 h)'] += 1
    inst['6 Training (15 h)'].append(hrs(t['TRAINING_STARTED'], t['TRAINING_COMPLETED']))
    enter['7 Exam'] += 1
    inst['7 Exam'].append(hrs(t['TRAINING_COMPLETED'], t['EXAM_PASSED']))
    if 'EXAM_FAILED' in t:
        lost_reason['7 Exam']['not lost: failed first attempt, passed on retake'] += 1
    enter['8 Certificate'] += 1
    if 'CERTIFIED' in t:
        inst['8 Certificate'].append(hrs(t['EXAM_PASSED'], t['CERTIFIED']))
        e2e.append(hrs(t['APPLICATION_STARTED'], t['CERTIFIED']))
    else:
        lost_reason['8 Certificate']['not lost: exam passed, certificate not yet issued at 30 Sep'] += 1

enter['4a Applicant fixes returned documents'] = len(returned_apps)
enter['4b Wait for re-check'] = len(replied_apps)
enter['4c Re-check after fix'] = len(replied_apps)

ACTOR = {
    '2 Upload documents': 'Applicant',
    '3 Wait for a reviewer': 'Queue: nobody acts; an ops reviewer picks the file up',
    '4 First review': 'Ops reviewer (22 reviewers, OPS-01..22)',
    '4a Applicant fixes returned documents': 'Applicant (after a reviewer returns the file)',
    '4b Wait for re-check': 'Queue: nobody acts; an ops reviewer resumes the file',
    '4c Re-check after fix': 'Ops reviewer',
    '5 Start training': 'Applicant (the log shows no system reminder)',
    '6 Training (15 h)': 'Applicant on the training platform',
    '7 Exam': 'Applicant (retakes included)',
    '8 Certificate': 'System',
}
order = list(ACTOR)
rows = []
for s in order:
    v = sorted(inst[s])
    n = enter[s]
    lo = lost[s]
    rows.append([s, ACTOR[s], n, lo, f'{100 * lo / n:.1f}', len(v), f'{pct(v, 50):.1f}', f'{pct(v, 90):.1f}',
                 f'{pct(v, 50) / 24:.2f}', f'{pct(v, 90) / 24:.2f}'])
write_csv('process_map_steps.csv', ['step', 'actor', 'apps_entering', 'apps_lost', 'lost_pct_of_entering',
                                    'timed_instances', 'median_hours', 'p90_hours', 'median_days', 'p90_days'], rows)
ee = sorted(e2e)
print('E2E certified n', len(ee), 'median h', pct(ee, 50), 'p90 h', pct(ee, 90), 'p25 h', pct(ee, 25))
for r in rows:
    print(r)
print('lost reasons')
for k, v in lost_reason.items():
    print(' ', k, dict(v))
print('first review outcome', first_outcome)
print('returned apps', len(returned_apps), 'replied at least once', len(replied_apps))

write_csv('process_map_loss_reasons.csv', ['step', 'reason_from_event_note', 'apps'],
          [[s, k, v] for s, c in lost_reason.items() for k, v in c.most_common()])

rc = collections.Counter()
rj = collections.Counter()
for e in ev_raw:
    if e['event'] == 'DOC_RETURNED':
        rc[e['note']] += 1
    if e['event'] == 'REJECTED':
        rj[e['note']] += 1
write_csv('process_map_return_and_reject_reasons.csv', ['event', 'note', 'events'],
          [['DOC_RETURNED', k, v] for k, v in rc.most_common()] + [['REJECTED', k, v] for k, v in rj.most_common()])
rr = collections.Counter(sum(1 for x in l if x[2] == 'DOC_RETURNED') for l in by.values())
write_csv('process_map_returns_per_app.csv', ['returns_in_the_application', 'apps'], sorted(rr.items()))
print('returns per app', sorted(rr.items()))

st = collections.Counter(a['status'] for a in apps.values())
mism = 0
for aid, a in apps.items():
    le = last_event[aid][2]
    exp = {'CERTIFIED': 'CERTIFIED', 'REJECTED': 'REJECTED', 'AUTO_EXPIRED': 'DROPPED'}.get(le, 'IN_PROGRESS')
    if exp != a['status']:
        mism += 1
print('status (dedup)', dict(st), 'mismatch with last event', mism)
json.dump({'application_rows': len(apps_raw), 'unique': len(apps), 'dups_removed': dups, 'event_rows': len(ev_raw),
           'event_dups': ev_dups, 'status': st, 'status_vs_last_event_mismatches': mism,
           'e2e_n': len(ee), 'e2e_median_h': pct(ee, 50), 'e2e_p90_h': pct(ee, 90), 'e2e_p25_h': pct(ee, 25)},
          open(os.path.join(OUT, '_part1_checks.json'), 'w'), indent=1)
