"""Embed the latest evaluation results into PolicyNest.html (between EVAL:START and EVAL:END).
Run after:  node eval/run_eval.js policynest_mvp/PolicyNest.html 04_DATASETS eval/out"""
import json, pathlib, re
root=pathlib.Path(__file__).resolve().parent.parent
out=root/'eval'/'out'
data={'now':json.loads((out/'eval_results.json').read_text()),'extra':json.loads((out/'extra.json').read_text()),'first':json.loads((out/'baseline_3.3.0.json').read_text()),'sim':json.loads((out/'simulation.json').read_text())}
p=root/'policynest_mvp'/'PolicyNest.html'; s=p.read_text(encoding='utf-8')
js='/* EVAL:START */var EVAL='+json.dumps(data,ensure_ascii=False,separators=(',',':'))+';/* EVAL:END */'
s,n=re.subn(r'/\* EVAL:START \*/.*?/\* EVAL:END \*/',lambda m:js,s,flags=re.S)
assert n==1, 'markers not found'
p.write_text(s,encoding='utf-8'); print('embedded', data['now']['run_at'])
