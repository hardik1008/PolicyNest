"""FR-63: KPI objects for the Evaluation and Review pages.

Writes eval/out/kpis.json: a list of {id, label, value, unit, source, note}.
Every value is computed from a file in this repo. Nothing is typed in by hand.
Values that cannot be measured offline are null with a source that says so.

Usage: python eval/kpis.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'eval' / 'out'

SRC_PRED = 'in-sample, 600 test applications (eval/out/eval_predictions.csv)'
SRC_SIM_AGES = 'simulated ages (eval/out/queue_seed.json)'


def read_csv(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def main():
    queue = json.loads((OUT / 'queue_seed.json').read_text(encoding='utf-8'))
    preds = read_csv(OUT / 'eval_predictions.csv')
    sim = json.loads((OUT / 'simulation.json').read_text(encoding='utf-8'))
    steps = read_csv(ROOT / 'stage1' / 'tables' / 'process_map_steps.csv')

    cases = queue['cases']
    ages = [c['age_hours'] for c in cases]
    n_test = sum(1 for c in cases if not c['constructed'])
    n_cons = sum(1 for c in cases if c['constructed'])

    mix = Counter(p['engine'] for p in preds)
    total = len(preds)
    assert total == 600, total
    assert sum(mix.values()) == total
    routed = mix.get('HUMAN_REVIEW', 0)
    assert routed == sum(1 for p in preds if p['human'] == 'true')

    drop_off = [{'step': s['step'], 'entering': int(s['apps_entering']), 'lost': int(s['apps_lost']),
                 'lost_pct': float(s['lost_pct_of_entering'])} for s in steps]

    est = sim['reviewer_minutes']['estimate_per_application']
    today_mean = sim['reviewer_minutes']['today_mean_per_application']

    kpis = [
        {'id': 'queue_size', 'label': 'Reviewer queue (seeded cases)', 'value': len(cases), 'unit': 'cases',
         'source': 'eval/out/queue_seed.json (FR-62); ' + SRC_SIM_AGES,
         'note': f'{n_test} test-set cases routed to a person, {n_cons} constructed cases. Constructed values are not evidence.'},
        {'id': 'queue_oldest_age', 'label': 'Oldest case in queue', 'value': max(ages), 'unit': 'hours',
         'source': SRC_SIM_AGES, 'note': 'Age is simulated and labelled as such in the seed; not a live queue.'},
        {'id': 'ai_mix_approve', 'label': 'AI decision: approve', 'value': mix.get('APPROVE', 0), 'unit': 'applications',
         'source': SRC_PRED, 'note': 'Engine decision column (before the reviewer step).'},
        {'id': 'ai_mix_needs_more_info', 'label': 'AI decision: needs more info', 'value': mix.get('NEEDS_MORE_INFO', 0),
         'unit': 'applications', 'source': SRC_PRED, 'note': 'Engine decision column.'},
        {'id': 'ai_mix_reject', 'label': 'AI decision: reject', 'value': mix.get('REJECT', 0), 'unit': 'applications',
         'source': SRC_PRED, 'note': 'Engine decision column; excludes the routed cases.'},
        {'id': 'ai_mix_routed', 'label': 'AI decision: routed to a person', 'value': routed, 'unit': 'applications',
         'source': SRC_PRED, 'note': 'Engine decision HUMAN_REVIEW (rulebook s.9).'},
        {'id': 'share_routed_to_person', 'label': 'Share routed to a person', 'value': round(routed / total, 4),
         'unit': 'share', 'source': SRC_PRED, 'note': f'{routed} of {total} applications.'},
        {'id': 'overrides', 'label': 'Reviewer overrides of the AI', 'value': None, 'unit': 'share',
         'source': 'this browser session only; not measured offline',
         'note': 'Overrides exist only in the live page, per browser session. No figure is stored or claimed here.'},
        {'id': 'drop_off_by_stage_today', 'label': "Drop-off by stage, today's process", 'value': drop_off,
         'unit': 'applications lost per stage',
         'source': "data pack stage_events, today's process (stage1/tables/process_map_steps.csv)",
         'note': 'Entering and lost counts per step as recorded in the process map table.'},
        {'id': 'reviewer_minutes_per_application', 'label': 'Reviewer minutes per application', 'value': est,
         'unit': 'minutes', 'source': 'simulated estimate (eval/out/simulation.json)',
         'note': (f'Routed share times today\'s mean of {today_mean} reviewer minutes per application '
                  f'(simulation.json). A simulated estimate, not a measured reviewer time.')},
    ]

    for k in kpis:
        assert set(k) == {'id', 'label', 'value', 'unit', 'source', 'note'}, k['id']

    (OUT / 'kpis.json').write_text(json.dumps(kpis, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print('wrote', OUT / 'kpis.json', 'kpis:', len(kpis))


if __name__ == '__main__':
    main()
