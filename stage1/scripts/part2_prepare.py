"""Part 2, step 0: split the test-set workbook so the hand decisions are made blind.
Usage: python part2_prepare.py <scratch folder>
Writes to the scratch folder:
  inputs_apps.csv   applicant-side facts only: declared name/dob/pan/education/state, penny-drop name, IRDAI registry hit
  flags.csv         application_id, is_hard_case   (needed to pick the sample; nothing else from the truth sheet)
  docs_inputs.csv   documents WITHOUT human_verdict, human_reason_code, reviewer_minutes
  sealed/truth.csv  final_decision, decision_reasons, name_match_category   (not opened until the hand decisions are written)
  sealed/doc_labels.csv  human_verdict, human_reason_code, reviewer_minutes (same rule)"""
import sys, os, csv
from common import *

out = sys.argv[1]
os.makedirs(os.path.join(out, 'sealed'), exist_ok=True)
book = read_xlsx(DOCS_XLSX)
truth = sheet(book, 'application_truth')
docs = sheet(book, 'documents')


def w(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        c = csv.writer(f)
        c.writerow(header)
        c.writerows(rows)


ia = ['application_id', 'declared_name', 'declared_dob', 'declared_pan', 'declared_education', 'declared_state',
      'penny_drop_name_returned', 'irdai_posp_registry_hit']
w(os.path.join(out, 'inputs_apps.csv'), ia, [[t[k] for k in ia] for t in truth])
w(os.path.join(out, 'flags.csv'), ['application_id', 'is_hard_case'], [[t['application_id'], t['is_hard_case']] for t in truth])
w(os.path.join(out, 'sealed', 'truth.csv'), ['application_id', 'final_decision', 'decision_reasons', 'name_match_category'],
  [[t['application_id'], t['final_decision'], t['decision_reasons'], t['name_match_category']] for t in truth])
di = ['doc_id', 'application_id', 'doc_type', 'image_quality', 'ocr_confidence', 'ocr_text', 'name_extracted',
      'dob_extracted', 'id_number_extracted', 'face_match_score']
w(os.path.join(out, 'docs_inputs.csv'), di, [[d[k] for k in di] for d in docs])
dl = ['doc_id', 'human_verdict', 'human_reason_code', 'reviewer_minutes']
w(os.path.join(out, 'sealed', 'doc_labels.csv'), dl, [[d[k] for k in dl] for d in docs])
print('ok', len(truth), len(docs))
