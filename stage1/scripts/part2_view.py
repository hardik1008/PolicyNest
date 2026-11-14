"""Part 2, step 2: show ONE application's inputs (declared facts, penny-drop, registry, every document's OCR text).
Shows no decision, no reviewer verdict, no reason code.   Usage: python part2_view.py <scratch folder> APP-26016 [APP-...]"""
import sys, os, csv, collections, datetime
S = sys.argv[1]
def xd(v):
    return (datetime.datetime(1899, 12, 30) + datetime.timedelta(days=float(v))).strftime('%d/%m/%Y') if v.replace('.', '', 1).isdigit() else v
sys.stdout.reconfigure(encoding='utf-8')
A = {r['application_id']: r for r in csv.DictReader(open(os.path.join(S, 'inputs_apps.csv'), encoding='utf-8'))}
D = collections.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(S, 'docs_inputs.csv'), encoding='utf-8')):
    D[r['application_id']][r['doc_type']] = r
for a in sys.argv[2:]:
    x = A[a]
    print('=' * 100)
    print(a)
    print(f"  FORM: name={x['declared_name']!r} dob={xd(x['declared_dob'])} pan={x['declared_pan']} edu={x['declared_education']} state={x['declared_state']}")
    print(f"  PENNY-DROP name returned: {x['penny_drop_name_returned']!r}    IRDAI POSP registry hit: {x['irdai_posp_registry_hit']}")
    for t in ['PAN', 'AADHAAR_FRONT', 'AADHAAR_BACK', 'CLASS10_MARKSHEET', 'CANCELLED_CHEQUE', 'SELFIE']:
        d = D[a][t]
        print(f"  --- {t}: quality={d['image_quality']} ocr_conf={d['ocr_confidence']} parsed: name={d['name_extracted']!r} dob={d['dob_extracted']!r} id={d['id_number_extracted']!r} face={d['face_match_score']!r}")
        for line in d['ocr_text'].splitlines():
            print('      |', line)
