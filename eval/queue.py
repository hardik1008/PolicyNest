"""FR-62: seed the reviewer queue for the Review console.

Writes eval/out/queue_seed.json.
  * the 11 test-set applications the engine routes to a person (human == "true" in eval_predictions.csv);
  * 5 constructed cases (fictional names; every value is marked constructed).
Ages are simulated and deterministic (seeded from the case index) and labelled "simulated".
The AI recommendation is the engine's own `pred` column. Dataset truth labels are NOT written to the queue.
Aadhaar and PAN numbers are never written.

Usage: python eval/queue.py
"""
import csv
import datetime
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'eval' / 'out'
DS = ROOT / '04_DATASETS'

NAME_MISMATCH_WHY = ("Different person's name (NAME_MISMATCH) - rulebook s.5 and s.9: "
                     "the system may recommend, a person confirms")


def read_csv(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def simulated_age_hours(key):
    """Deterministic simulated age, 2 to 96 hours."""
    return random.Random(f'pn-queue-{key}').randint(2, 96)


def why_routed_for(codes):
    if 'NAME_MISMATCH' in codes:
        return NAME_MISMATCH_WHY
    return 'Engine routed to a person: ' + ('; '.join(codes) or 'no code recorded')


def test_set_case(index, pred, docs_for_app, state):
    codes = [c.strip() for c in pred['codes'].split(';') if c.strip()]
    names = {d['doc_type']: (d['name_extracted'] or None) for d in docs_for_app}
    selfie = [d for d in docs_for_app if d['doc_type'] == 'SELFIE']
    face = float(selfie[0]['face_match_score']) if selfie and selfie[0]['face_match_score'] else None
    unsure = [{'document': d['doc_type'], 'reason': 'OCR confidence below 0.75 (rulebook s.4.1): not used'}
              for d in docs_for_app if d['ocr_confidence'] and float(d['ocr_confidence']) < 0.75]
    unsure += [{'check': c, 'reason': 'engine check not passed'} for c in codes]
    return {
        'id': pred['id'],
        'kind': 'test-set case',
        'constructed': False,
        'source': 'test set (04_DATASETS); engine output eval/out/eval_predictions.csv',
        'why_routed': why_routed_for(codes),
        'ai_recommendation': pred['pred'],
        'engine_decision': pred['engine'],
        'codes': codes,
        'name_on_pan': names.get('PAN'),
        'names_on_other_documents': {k: v for k, v in names.items() if k not in ('PAN', 'SELFIE')},
        'face_match_score': face,
        'state_declared': state or None,
        'documents': [{'document': d['doc_type'],
                       'ocr_confidence': float(d['ocr_confidence']) if d['ocr_confidence'] else None}
                      for d in docs_for_app],
        'where_unsure': unsure,
        'age_hours': simulated_age_hours(index),
        'age_label': 'simulated',
    }


CONSTRUCTED = [
    {
        'id': 'CONSTRUCTED-01',
        'why_routed': 'Face match 0.68, inside the 0.60 to 0.75 band (rulebook s.4.6 and s.9: a person compares the photos)',
        'ai_recommendation': 'No automatic outcome; route to reviewer',
        'codes': ['FACE_MATCH_REVIEW'],
        'name_on_pan': 'ASHA TESTCASE RAO',
        'names_on_other_documents': {'AADHAAR_FRONT': 'ASHA TESTCASE RAO'},
        'face_match_score': 0.68,
        'where_unsure': [{'check': 'FACE_MATCH_REVIEW', 'reason': 'score 0.68 in the 0.60 to 0.75 band'}],
    },
    {
        'id': 'CONSTRUCTED-02',
        'why_routed': ('Surname changed after marriage (rulebook s.5 and s.9: NEEDS_INFO, Human only; '
                       'ask for a marriage certificate or gazette notification)'),
        'ai_recommendation': 'NEEDS_MORE_INFO after a person confirms the surname change',
        'codes': ['SURNAME_CHANGE'],
        'name_on_pan': 'KIRAN SAMPLEVALE NAIR',
        'names_on_other_documents': {'CLASS10_MARKSHEET': 'KIRAN SAMPLEVALE IYER'},
        'face_match_score': 0.91,
        'where_unsure': [{'check': 'SURNAME_CHANGE', 'reason': 'surname differs between PAN and marksheet (name tier 6, Human only)'}],
    },
    {
        'id': 'CONSTRUCTED-03',
        'why_routed': 'Class 10 board not on the recognised list (rulebook s.4.4 and s.9: Human only)',
        'ai_recommendation': 'No automatic outcome; route to reviewer',
        'codes': ['BOARD_NOT_RECOGNISED'],
        'name_on_pan': 'MEERA TESTFIELD DAS',
        'names_on_other_documents': {'CLASS10_MARKSHEET': 'MEERA TESTFIELD DAS'},
        'board_read': 'Sample Regional Board (constructed; not on the recognised list)',
        'face_match_score': 0.90,
        'where_unsure': [{'check': 'BOARD_NOT_RECOGNISED', 'reason': 'board not on the recognised list'}],
    },
    {
        'id': 'CONSTRUCTED-04',
        'why_routed': ('Applicant disputes a PAN_NOT_INDIVIDUAL rejection (rulebook s.9: any disputed case goes to a person; '
                       'outcomes Uphold / Ask / Overturn)'),
        'ai_recommendation': 'REJECT stands unless the reviewer overturns it',
        'codes': ['PAN_NOT_INDIVIDUAL'],
        'name_on_pan': 'DEVI SAMPLEPATH',
        'names_on_other_documents': {'AADHAAR_FRONT': 'DEVI SAMPLEPATH'},
        'pan_holder_type_read': 'company holder code (constructed value)',
        'face_match_score': 0.89,
        'applicant_dispute': 'Constructed: the applicant says the PAN was issued to them personally.',
        'where_unsure': [{'check': 'PAN_NOT_INDIVIDUAL', 'reason': 'applicant disputes the holder-type reading'}],
    },
    {
        'id': 'CONSTRUCTED-05',
        'why_routed': ('Two selfie failures in a row below 0.60 (rulebook s.4.6 and s.7: internal fraud-desk referral, '
                       'same day, to compliance; the applicant sees only a neutral message)'),
        'ai_recommendation': 'Internal fraud-desk referral (second consecutive failure)',
        'codes': ['FACE_MATCH_LOW', 'FACE_MATCH_LOW_REPEAT'],
        'name_on_pan': 'TARUN SAMPLEKUMAR GHOSH',
        'names_on_other_documents': {'AADHAAR_FRONT': 'TARUN SAMPLEKUMAR GHOSH'},
        'face_match_scores': [0.54, 0.57],
        'where_unsure': [{'check': 'FACE_MATCH_LOW_REPEAT', 'reason': 'two consecutive selfie scores below 0.60'}],
    },
]


def main():
    results = json.loads((OUT / 'eval_results.json').read_text(encoding='utf-8'))
    preds = read_csv(OUT / 'eval_predictions.csv')
    docs = read_csv(DS / 'documents.csv')
    apps = read_csv(DS / 'applications.csv')

    docs_by_app = {}
    for d in docs:
        docs_by_app.setdefault(d['application_id'], []).append(d)
    state_by_app = {}
    for a in apps:
        state_by_app.setdefault(a['application_id'], a['state'])

    routed = [p for p in preds if p['human'] == 'true']
    assert len(routed) == 11, len(routed)

    cases = [test_set_case(i, p, docs_by_app[p['id']], state_by_app.get(p['id'], ''))
             for i, p in enumerate(routed)]
    for j, c in enumerate(CONSTRUCTED):
        c.update({
            'kind': 'constructed case',
            'constructed': True,
            'values_marked': 'constructed',
            'source': 'constructed for the review console; not from the test set',
            'engine_decision': None,
            'documents': None,
            'state_declared': None,
            'age_hours': simulated_age_hours(100 + j),
            'age_label': 'simulated',
        })
        cases.append(c)
    assert len(cases) == 16

    out = {
        'generated_at': datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds'),
        'engine_sha256': results['engine_sha256'],
        'note': ('Seeded reviewer queue for the Review console (FR-62). 11 cases are test-set applications the engine '
                 'routes to a person; 5 are constructed (fictional names, every value marked constructed). '
                 'Ages are simulated and deterministic. The AI recommendation is the engine output; dataset truth '
                 'labels are deliberately not included. Aadhaar and PAN numbers are omitted.'),
        'cases': cases,
    }
    (OUT / 'queue_seed.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print('wrote', OUT / 'queue_seed.json', 'cases:', len(cases))


if __name__ == '__main__':
    main()
