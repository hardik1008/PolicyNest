"""FR-62: seed the reviewer queue for the Review console.

Writes eval/out/queue_seed.json.
  * the 11 test-set applications the engine routes to a person (human == "true" in eval_predictions.csv);
  * 5 constructed cases (fictional names; every made-up value is listed in constructed_fields).
Ages are simulated and deterministic (seeded from the case index) and labelled "simulated".
The AI recommendation is the engine's own `pred` column. Dataset truth labels are NOT written to the queue.
Aadhaar and PAN numbers are never written. The output is deterministic: generated_at is the engine run time
(eval_results.json run_at), not the wall clock.

Usage: python eval/queue.py
"""
import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'eval' / 'out'
DS = ROOT / '04_DATASETS'

NAME_MISMATCH_WHY = ("Different person's name (NAME_MISMATCH) - rulebook s.5 and s.9: "
                     "the system may recommend, a person confirms")

NOTE = ('Seeded reviewer queue for the Review console (FR-62). '
        '11 cases are test-set applications the engine routes to a person. All 11 engine-routed test-set cases are '
        'different-person name cases (NAME_MISMATCH); APP-26016 also carries DOB_MISMATCH and APP-26115 also carries '
        'BANK_NAME_MISMATCH. The other Human-only kinds exist only as constructed cases because the test set has none. '
        'Each constructed case is flagged constructed: true and lists its made-up fields in constructed_fields; '
        'constructed values are not evidence. Constructed cases were not run through the engine. '
        'Ages are simulated and deterministic. The AI recommendation for test-set cases is the engine output; '
        'dataset truth labels are deliberately not included. Aadhaar and PAN numbers are omitted.')

PAN_SIDE_SKIP = ('PAN', 'SELFIE')


def read_csv(path):
    with open(path, encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f))


def simulated_age_hours(key):
    """Deterministic simulated age, 2 to 96 hours."""
    return random.Random(f'pn-queue-{key}').randint(2, 96)


def norm(s):
    return ' '.join((s or '').upper().split())


def differing(docs, field, pan_value):
    """Document types (other than PAN and SELFIE) whose extracted field differs from the PAN value."""
    return [d['doc_type'] for d in docs
            if d['doc_type'] not in PAN_SIDE_SKIP and d.get(field) and pan_value
            and norm(d[field]) != norm(pan_value)]


def reason_for(code, docs, pan_name, pan_dob):
    """Plain reason per engine code, naming the document from the case data."""
    if code == 'NAME_MISMATCH':
        who = differing(docs, 'name_extracted', pan_name) or ['the other documents']
        return f"name on {', '.join(who)} differs from the PAN name beyond the rulebook's tiers"
    if code == 'BANK_NAME_MISMATCH':
        return 'account-holder name on CANCELLED_CHEQUE does not match the PAN name'
    if code == 'DOB_MISMATCH':
        who = differing(docs, 'dob_extracted', pan_dob) or ['the other documents']
        return f"date of birth on {', '.join(who)} differs from the PAN date of birth"
    return f'engine code {code} is not passed (no reason text defined in eval/queue.py)'


def why_routed_for(codes):
    if 'NAME_MISMATCH' in codes:
        return NAME_MISMATCH_WHY
    return 'Engine routed to a person: ' + ('; '.join(codes) or 'no code recorded')


def test_set_case(index, pred, docs_for_app, state):
    codes = [c.strip() for c in pred['codes'].split(';') if c.strip()]
    names = {d['doc_type']: (d['name_extracted'] or None) for d in docs_for_app}
    pan_rows = [d for d in docs_for_app if d['doc_type'] == 'PAN']
    pan_name = pan_rows[0]['name_extracted'] if pan_rows else None
    pan_dob = pan_rows[0]['dob_extracted'] if pan_rows else None
    selfie = [d for d in docs_for_app if d['doc_type'] == 'SELFIE']
    face = float(selfie[0]['face_match_score']) if selfie and selfie[0]['face_match_score'] else None
    unsure = [{'document': d['doc_type'], 'reason': 'OCR confidence below 0.75 (rulebook s.4.1): not used'}
              for d in docs_for_app if d['ocr_confidence'] and float(d['ocr_confidence']) < 0.75]
    unsure += [{'check': c, 'reason': reason_for(c, docs_for_app, pan_name, pan_dob)} for c in codes]
    return {
        'id': pred['id'],
        'kind': 'test-set case',
        'constructed': False,
        'source': 'test set (04_DATASETS); engine output eval/out/eval_predictions.csv',
        'why_routed': why_routed_for(codes),
        'ai_recommendation': pred['pred'],
        'engine_decision': pred['engine'],
        'codes': codes,
        'name_on_pan': pan_name,
        'names_on_other_documents': {k: v for k, v in names.items() if k not in PAN_SIDE_SKIP},
        'face_match_score': face,
        'state_declared': state or None,
        'documents': [{'document': d['doc_type'],
                       'ocr_confidence': float(d['ocr_confidence']) if d['ocr_confidence'] else None}
                      for d in docs_for_app],
        'where_unsure': unsure,
        'age_hours': simulated_age_hours(index),
        'age_label': 'simulated',
    }


# Constructed cases. Codes are engine check codes (grep "FACE_MATCH_\|NAME_MISMATCH" policynest_mvp/PolicyNest.html),
# except where a case_note says otherwise. The engine was NOT run on these cases.
CONSTRUCTED = [
    {
        'id': 'CONSTRUCTED-01',
        'why_routed': 'Face match 0.68, inside the 0.60 to 0.75 band (rulebook s.4.6 and s.9: a person compares the photos)',
        'ai_recommendation': 'No automatic outcome; route to reviewer',
        'codes': ['FACE_MATCH_BORDERLINE'],
        'name_on_pan': 'ASHA TESTCASE RAO',
        'names_on_other_documents': {'AADHAAR_FRONT': 'ASHA TESTCASE RAO'},
        'face_match_score': 0.68,
        'where_unsure': [{'check': 'FACE_MATCH_BORDERLINE', 'reason': 'score 0.68 in the 0.60 to 0.75 band'}],
        'constructed_fields': ['ai_recommendation', 'name_on_pan', 'names_on_other_documents', 'face_match_score'],
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
        'constructed_fields': ['ai_recommendation', 'name_on_pan', 'names_on_other_documents', 'face_match_score'],
    },
    {
        'id': 'CONSTRUCTED-03',
        'why_routed': 'Class 10 board not on the recognised list (rulebook s.4.4 and s.9: Human only)',
        'ai_recommendation': 'No automatic outcome; route to reviewer',
        'codes': ['BOARD_UNLISTED'],
        'name_on_pan': 'MEERA TESTFIELD DAS',
        'names_on_other_documents': {'CLASS10_MARKSHEET': 'MEERA TESTFIELD DAS'},
        'board_read': 'Sample Regional Board (constructed; not on the recognised list)',
        'face_match_score': 0.90,
        'where_unsure': [{'check': 'BOARD_UNLISTED', 'reason': 'board not on the recognised list'}],
        'constructed_fields': ['ai_recommendation', 'name_on_pan', 'names_on_other_documents', 'board_read', 'face_match_score'],
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
        'constructed_fields': ['ai_recommendation', 'name_on_pan', 'names_on_other_documents', 'pan_holder_type_read',
                               'face_match_score', 'applicant_dispute'],
    },
    {
        'id': 'CONSTRUCTED-05',
        'why_routed': ('Two selfie failures in a row below 0.60 (rulebook s.4.6 and s.7: internal fraud-desk referral, '
                       'same day, to compliance; the applicant sees only a neutral message)'),
        'ai_recommendation': 'Internal fraud-desk referral (second consecutive failure)',
        'codes': ['FACE_MATCH_LOW', 'FACE_MATCH_LOW_REPEAT'],
        'code_note': 'queue-only code; the repeat-failure rule (rulebook s.4.6) is counted outside the engine',
        'name_on_pan': 'TARUN SAMPLEKUMAR GHOSH',
        'names_on_other_documents': {'AADHAAR_FRONT': 'TARUN SAMPLEKUMAR GHOSH'},
        'face_match_scores': [0.54, 0.57],
        'where_unsure': [
            {'check': 'FACE_MATCH_LOW', 'reason': 'selfie score below 0.60'},
            {'check': 'FACE_MATCH_LOW_REPEAT', 'reason': 'two consecutive selfie scores below 0.60 (counted outside the engine)'},
        ],
        'constructed_fields': ['ai_recommendation', 'name_on_pan', 'names_on_other_documents', 'face_match_scores'],
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
    for p in routed:
        assert 'NAME_MISMATCH' in [c.strip() for c in p['codes'].split(';')], p['id']

    cases = [test_set_case(i, p, docs_by_app[p['id']], state_by_app.get(p['id'], ''))
             for i, p in enumerate(routed)]
    for j, c in enumerate(CONSTRUCTED):
        c.update({
            'kind': 'constructed case',
            'constructed': True,
            'values_marked': 'constructed',
            'source': 'constructed for the review console; not from the test set; not run through the engine',
            'engine_decision': None,
            'documents': None,
            'state_declared': None,
            'age_hours': simulated_age_hours(100 + j),
            'age_label': 'simulated',
        })
        cases.append(c)
    assert len(cases) == 16

    out = {
        # Engine run time from eval_results.json, so the file is byte-identical across runs.
        'generated_at': results['run_at'],
        'engine_sha256': results['engine_sha256'],
        'note': NOTE,
        'cases': cases,
    }
    (OUT / 'queue_seed.json').write_text(json.dumps(out, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print('wrote', OUT / 'queue_seed.json', 'cases:', len(cases))


if __name__ == '__main__':
    main()
