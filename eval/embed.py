"""Embed the latest evaluation results into PolicyNest.html (between EVAL:START and EVAL:END).
Run after:  node eval/run_eval.js policynest_mvp/PolicyNest.html 04_DATASETS eval/out
Also embeds the Stage 1 process map (stage1/tables/process_map_steps.csv) as `pmap` (FR-61)."""
import csv, json, pathlib, re
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'eval'/'out'

def num(v):
    # keep the CSV value exactly: integers stay integers, decimals keep their written digits
    return int(v) if re.fullmatch(r'-?\d+', v.strip()) else float(v)

pmap=[]
with open(root/'stage1'/'tables'/'process_map_steps.csv', encoding='utf-8', newline='') as f:
    for r in csv.DictReader(f):
        pmap.append({'step':r['step'],'actor':r['actor'],'apps_entering':num(r['apps_entering']),
                     'apps_lost':num(r['apps_lost']),'lost_pct_of_entering':num(r['lost_pct_of_entering']),
                     'median_hours':num(r['median_hours']),'p90_hours':num(r['p90_hours'])})

def rj(path):
    # always UTF-8: on Windows the default codec is cp1252, which turns the middle dot and section sign into mojibake
    return json.loads(path.read_text(encoding='utf-8'))

data={'now':rj(out/'eval_results.json'),'extra':rj(out/'extra.json'),'first':rj(out/'baseline_3.3.0.json'),'sim':rj(out/'simulation.json'),'pmap':pmap,
      'pmap_meta':{'period':'Jan–Sep 2026','source':'stage1/tables/process_map_steps.csv'}}
p=root/'policynest_mvp'/'PolicyNest.html'; s=p.read_text(encoding='utf-8')
js='/* EVAL:START */var EVAL='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';/* EVAL:END */'
s,n=re.subn(r'/\* EVAL:START \*/.*?/\* EVAL:END \*/',lambda m:js,s,flags=re.S)
assert n==1, 'markers not found'
p.write_text(s,encoding='utf-8'); print('embedded', data['now']['run_at'], 'pmap rows', len(pmap))
