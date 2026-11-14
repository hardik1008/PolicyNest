"""Part 3: first business case. Inputs: applications workbook (deduplicated), stage_events, ops_team, and the test set's
reviewer_minutes. Every figure printed here is also written to ../tables/*.csv.  Estimates are labelled in the pack.
Usage: python part3_business_case.py"""
import collections, statistics, json
from common import *

book = read_xlsx(APPS_XLSX)
apps = {}
for a in sheet(book, 'applications'):
    apps.setdefault(a['application_id'], a)
ev = sheet(book, 'stage_events')
ops = sheet(book, 'ops_team')
docs = sheet(read_xlsx(DOCS_XLSX), 'documents')

H = lambda a, b: (b - a) * 24.0
by = collections.defaultdict(list)
for e in ev:
    by[e['application_id']].append((float(e['event_time']), e['event'], e['note'], e['actor']))
for l in by.values():
    l.sort()

res = {}
# ---------------------------------------------------------------- rates
rate = [float(o['loaded_cost_inr_per_hour']) for o in ops]
handled = [float(o['applications_handled_jan_sep']) for o in ops]
res['rate_mean'] = statistics.mean(rate)
res['rate_weighted_by_apps_handled'] = sum(r * h for r, h in zip(rate, handled)) / sum(handled)
res['rate_min_max'] = (min(rate), max(rate))
RATE = round(res['rate_mean'])               # 430
# ---------------------------------------------------------------- reviewer minutes (test set)
per_app = collections.defaultdict(float)
per_doc = collections.defaultdict(list)
for d in docs:
    per_app[d['application_id']] += float(d['reviewer_minutes'])
    per_doc[d['doc_type']].append(float(d['reviewer_minutes']))
MIN_PASS = statistics.mean(per_app.values())
MIN_DOC = statistics.mean(float(d['reviewer_minutes']) for d in docs)
res['minutes_per_app_mean'] = MIN_PASS
res['minutes_per_app_median'] = statistics.median(per_app.values())
res['minutes_per_doc_mean'] = MIN_DOC
res['minutes_per_app_n'] = len(per_app)
# ---------------------------------------------------------------- volumes
reviewed = sum(1 for l in by.values() if any(x[1] == 'REVIEW_STARTED' for x in l))
resumed = sum(1 for l in by.values() for x in l if x[1] == 'REVIEW_RESUMED')
touches = sum(int(a['manual_touches']) for a in apps.values())
reviewer_events = sum(1 for l in by.values() for x in l if x[3].startswith('OPS'))
exam_fail = sum(1 for l in by.values() for x in l if x[1] == 'EXAM_FAILED')
res.update(apps=len(apps), reviewed=reviewed, resumed=resumed, touches=touches, reviewer_events=reviewer_events, exam_fail=exam_fail)
res['touches_minus_reviewer_events'] = touches - reviewer_events
months = 9
# ---------------------------------------------------------------- reviewer effort: baseline and scenarios
base_low_h = reviewed * MIN_PASS / 60                       # first pass only
base_high_h = (reviewed + resumed) * MIN_PASS / 60          # every review session = a full pass
recheck_h = resumed * MIN_DOC / 60                          # re-check = one document's time (assumption)
base_mid_h = base_low_h + recheck_h
floor_saved = 0.60 * base_low_h                             # STP 60%, routed cases still cost a full pass
target_min = 5.0
target_saved = reviewed * (MIN_PASS - target_min) / 60      # reviewer minutes per application cut to 5
res.update(base_low_h=base_low_h, base_mid_h=base_mid_h, base_high_h=base_high_h, recheck_h=recheck_h,
           floor_saved_h=floor_saved, target_saved_h=target_saved)
package_claim = touches * MIN_PASS / 60                      # 03_OPERATIONAL_BASELINE_METRICS.md style: touches x full pass
res['package_style_touches_x_pass_h'] = package_claim
rows = []
def add(label, h, note):
    rows.append([label, f'{h:,.0f}', f'{h / months:,.1f}', f'{h * RATE:,.0f}', f'{h * RATE / 1e5:.2f}', note])
add('Baseline A: first review pass only (2,742 files x 20.7 min)', base_low_h, 'ESTIMATE. Minutes from the 600-application test set; all 2,742 reviewed files assumed to cost the same')
add('Baseline B: A + 638 re-checks at one document each (3.45 min)', base_mid_h, 'ESTIMATE. Re-check effort is an assumption; no data')
add('Baseline C: every one of 3,380 review sessions costs a full 20.7-min pass', base_high_h, 'ESTIMATE, upper bound')
add('Package style: 9,920 touches x 20.7 min (NOT USED)', package_claim, 'Not used. 3,000 touches are not reviewer actions (see pack section 3.2)')
add('Saved at the straight-through floor: 60% of files need no reviewer (vs A)', floor_saved, 'ESTIMATE. Routed 40% still cost the full 20.7 min, i.e. 8.3 min per file')
add('Saved at the minutes target: <5 min per file averaged over all files (vs A)', target_saved, 'ESTIMATE. Brief Table 7 target; 76% less reviewer time')
add('Extra saving, re-checks no longer done by a person (vs B-A)', recheck_h, 'ESTIMATE, low confidence')
write_csv('bc_reviewer_hours.csv', ['line', 'hours_9_months', 'hours_per_month', 'inr_at_430_per_hour', 'inr_lakh', 'status'], rows)
res['routed_minutes_per_file_at_floor'] = 0.4 * MIN_PASS
res['max_minutes_per_routed_case_for_target_at_60pct_stp'] = target_min / 0.4
res['team_hours_per_reviewer_per_month_baseline_A'] = base_low_h / 22 / months
# ---------------------------------------------------------------- elapsed waiting
q1, q2, rv1, rv2 = [], [], [], []
cert_e2e = {}
for aid, l in by.items():
    t = {}
    for x in l:
        t.setdefault(x[1], x[0])
    names = [x[1] for x in l]
    if 'DOCS_SUBMITTED' not in t:
        continue
    q1.append(H(t['DOCS_SUBMITTED'], t['REVIEW_STARTED']))
    # first-review elapsed
    k = names.index('REVIEW_STARTED')
    first_out = next(x for x in l[k + 1:] if x[1] in ('KYC_VERIFIED', 'DOC_RETURNED', 'REJECTED'))
    rv1.append(H(l[k][0], first_out[0]))
    for j, x in enumerate(l):
        if x[1] == 'DOC_REUPLOADED':
            q2.append(H(x[0], l[j + 1][0]))
            out = next(y for y in l[j + 2:] if y[1] in ('KYC_VERIFIED', 'DOC_RETURNED'))
            rv2.append(H(l[j + 1][0], out[0]))
sum_wait = sum(q1) + sum(q2) + sum(rv1) + sum(rv2)
passes = len(q1) + len(q2)
new_h = passes * (10 / 60.0)
res.update(wait_hours_total=sum_wait, wait_passes=passes, wait_mean_per_pass=sum_wait / passes, new_hours_at_10min=new_h,
           wait_saved_all_passes=sum_wait - new_h, wait_saved_at_60pct=0.6 * (sum_wait - new_h))
res['queue_first_mean_h'] = statistics.mean(q1)
res['queue_recheck_mean_h'] = statistics.mean(q2)
write_csv('bc_waiting_hours.csv', ['line', 'hours', 'note'], [
    ['applicant waiting hours today (queue + review elapsed), first passes: 2,742', f'{sum(q1) + sum(rv1):,.0f}', 'MEASURED from stage_events'],
    ['applicant waiting hours today, re-check passes: 582 files / 638 passes', f'{sum(q2) + sum(rv2):,.0f}', 'MEASURED from stage_events'],
    ['total', f'{sum_wait:,.0f}', f'mean {sum_wait / passes:.1f} h per pass over {passes} passes'],
    ['at the 10-minute target on every pass', f'{new_h:,.0f}', 'ASSUMPTION: Table 7 target applied to every pass'],
    ['saved if every pass meets the target', f'{sum_wait - new_h:,.0f}', 'ESTIMATE, upper end'],
    ['saved if only 60% of passes (the straight-through floor) are decided in 10 minutes', f'{0.6 * (sum_wait - new_h):,.0f}', 'ESTIMATE, floor'],
])
# ---------------------------------------------------------------- median days to certificate (same method as eval/simulate.py, written independently)
tot, sim, sim2 = [], [], []
for aid, l in by.items():
    t = {}
    for x in l:
        t.setdefault(x[1], x[0])
    if 'CERTIFIED' not in t:
        continue
    total = H(t['APPLICATION_STARTED'], t['CERTIFIED'])
    zone = H(t['DOCS_SUBMITTED'], t['KYC_VERIFIED'])
    ret = [x for x in l if x[1] == 'DOC_RETURNED']
    if ret:
        reply = next(H(ret[0][0], y[0]) for y in l if y[1] == 'DOC_REUPLOADED')
        eng = reply + 10 / 60.0
    else:
        eng = 10 / 60.0
    tot.append(total)
    sim.append(total - zone + eng)
    k2t = H(t['KYC_VERIFIED'], t['TRAINING_STARTED'])
    sim2.append(total - zone + eng - k2t + min(k2t, 1.0))
def st(v):
    v = sorted(v)
    return pct(v, 50) / 24, pct(v, 90) / 24
res['days_today'] = st(tot); res['days_engine'] = st(sim); res['days_engine_link'] = st(sim2)
res['hours_saved_per_certified_mean'] = statistics.mean(a - b for a, b in zip(tot, sim))
res['hours_saved_per_certified_median'] = statistics.median(a - b for a, b in zip(tot, sim))
write_csv('bc_days_to_certificate.csv', ['scenario', 'median_days', 'p90_days', 'status'], [
    ['today (1,732 certified)', f'{res["days_today"][0]:.2f}', f'{res["days_today"][1]:.2f}', 'MEASURED'],
    ['product decides each pass in 10 min; applicant reply times kept; one round only', f'{res["days_engine"][0]:.2f}', f'{res["days_engine"][1]:.2f}', 'ESTIMATE (replay of observed journeys)'],
    ['as above and the training link sent at once (KYC to start capped at 1 h)', f'{res["days_engine_link"][0]:.2f}', f'{res["days_engine_link"][1]:.2f}', 'ESTIMATE; the 1-hour cap is an ASSUMPTION'],
])
# ---------------------------------------------------------------- drop-off: where the 951 + 314 go, and what data says about drivers
lost_nodocs = lost_silent = lost_notrain = rejected = 0
returned_set = set(); replied_set = set(); silent_set = set()
for aid, l in by.items():
    names = [x[1] for x in l]
    if 'DOC_RETURNED' in names: returned_set.add(aid)
    if 'DOC_REUPLOADED' in names: replied_set.add(aid)
    last = l[-1]
    if last[1] == 'AUTO_EXPIRED':
        if 'No documents' in last[2]: lost_nodocs += 1
        elif 'No response' in last[2]: lost_silent += 1; silent_set.add(aid)
        else: lost_notrain += 1
    if last[1] == 'REJECTED': rejected += 1
res.update(lost_nodocs=lost_nodocs, lost_silent=lost_silent, lost_notrain=lost_notrain, rejected=rejected, returned=len(returned_set), replied=len(replied_set))
certified = {a for a in apps if apps[a]['status'] == 'CERTIFIED'}
verified = {a for a, l in by.items() if any(x[1] == 'KYC_VERIFIED' for x in l)}
trained = {a for a, l in by.items() if any(x[1] == 'TRAINING_STARTED' for x in l)}
res['cert_rate_given_replied'] = len(certified & replied_set) / len(replied_set)
res['cert_rate_given_training_started'] = len(certified & trained) / len(trained)
res['cert_rate_returned_once'] = None
rc = collections.Counter(); rc_cert = collections.Counter(); rc_silent = collections.Counter()
for aid in by:
    n = sum(1 for x in by[aid] if x[1] == 'DOC_RETURNED')
    if n:
        rc[n] += 1; rc_cert[n] += aid in certified; rc_silent[n] += aid in silent_set
write_csv('bc_returns_vs_outcome.csv', ['times_returned', 'apps', 'certified', 'certified_pct', 'ended_in_silence'],
          [[n, rc[n], rc_cert[n], f'{100 * rc_cert[n] / rc[n]:.1f}', rc_silent[n]] for n in sorted(rc)])
# silence by first return reason, by queue wait quartile; non-start by review-zone quartile, by channel
reason_map = lambda note: ('poor image' if 'blurry' in note else 'name spelling' if 'Name on PAN' in note else 'DOB mismatch' if 'DOB' in note else 'bank name' if 'Account holder' in note else 'face match' if 'Photo' in note else note)
rr = collections.defaultdict(lambda: [0, 0])
qw = []
for aid in returned_set:
    l = by[aid]
    first = next(x for x in l if x[1] == 'DOC_RETURNED')
    rr[reason_map(first[2])][0] += 1; rr[reason_map(first[2])][1] += aid in silent_set
    t = {}
    for x in l: t.setdefault(x[1], x[0])
    qw.append((H(t['DOCS_SUBMITTED'], t['REVIEW_STARTED']), aid in silent_set))
qw.sort()
n = len(qw); quart = [qw[i * n // 4:(i + 1) * n // 4] for i in range(4)]
rows = [['silence after first return, by reason', k, v[0], v[1], f'{100 * v[1] / v[0]:.1f}'] for k, v in sorted(rr.items(), key=lambda kv: -kv[1][0])]
rows += [['silence by queue-wait quartile (hours before the first review)', f'Q{i + 1}: {q[0][0]:.1f}-{q[-1][0]:.1f} h', len(q), sum(s for _, s in q), f'{100 * sum(s for _, s in q) / len(q):.1f}'] for i, q in enumerate(quart)]
ns = []
for aid in verified:
    t = {}
    for x in by[aid]: t.setdefault(x[1], x[0])
    ns.append((H(t['DOCS_SUBMITTED'], t['KYC_VERIFIED']), aid not in trained))
ns.sort(); n = len(ns); quart = [ns[i * n // 4:(i + 1) * n // 4] for i in range(4)]
rows += [['no training start after KYC, by review-zone quartile (hours docs to KYC)', f'Q{i + 1}: {q[0][0]:.1f}-{q[-1][0]:.1f} h', len(q), sum(s for _, s in q), f'{100 * sum(s for _, s in q) / len(q):.1f}'] for i, q in enumerate(quart)]
for label, grp in [('returned before KYC', True), ('not returned', False)]:
    g = [aid for aid in verified if (aid in returned_set) == grp]
    rows.append(['no training start after KYC, by path', label, len(g), sum(aid not in trained for aid in g), f'{100 * sum(aid not in trained for aid in g) / len(g):.1f}'])
ch = collections.defaultdict(lambda: [0, 0, 0, 0, 0])
for aid, a in apps.items():
    c = a['channel'] or '(blank)'
    ch[c][0] += 1; ch[c][1] += aid in certified
    ch[c][2] += not any(x[1] == 'DOCS_SUBMITTED' for x in by[aid])
    ch[c][3] += aid in verified; ch[c][4] += aid in verified and aid not in trained
for c, v in sorted(ch.items(), key=lambda kv: -kv[1][0]):
    rows.append(['outcome by channel (apps | certified | no docs | verified | verified but no training)', c, v[0], f'{v[1]} | {v[2]} | {v[3]} | {v[4]}', f'cert {100 * v[1] / v[0]:.1f}%; no docs {100 * v[2] / v[0]:.1f}%; no training {100 * v[4] / max(v[3], 1):.1f}%'])
write_csv('bc_dropoff_drivers.csv', ['cut', 'group', 'apps', 'lost_or_detail', 'rate'], rows)
for r in rows: print(r)
# ---------------------------------------------------------------- what-if grid (arithmetic on observed rates; NOT a forecast)
grid = []
cr, ct = res['cert_rate_given_replied'], res['cert_rate_given_training_started']
for sil_cut in (0.25, 0.50, 1 - 0.10 / (lost_silent / len(returned_set))):
    for tr_cut in (0.0, 0.25, 0.50):
        rec_sil = lost_silent * sil_cut
        rec_tr = lost_notrain * tr_cut
        extra = rec_sil * cr + rec_tr * ct
        grid.append([f'{100 * sil_cut:.0f}%', f'{100 * tr_cut:.0f}%', f'{rec_sil:.0f}', f'{rec_tr:.0f}', f'{extra:.0f}', f'{100 * (1732 + extra) / 3000:.1f}%'])
write_csv('bc_dropoff_whatif.csv', ['cut_in_silence_after_return', 'cut_in_no_training_start', 'recovered_silent_applicants', 'recovered_non_starters', 'extra_certified_agents_9_months', 'certification_rate_would_be'], grid)
for g in grid: print(g)
json.dump(res, open(os.path.join(OUT, '_part3_numbers.json'), 'w'), indent=1, default=str)
for k, v in res.items(): print(k, v)
