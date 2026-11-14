"""Reason-level coverage, one-message coverage and the reviewer roll-up baseline -> eval/out/extra.json"""
import pandas as pd, json, pathlib
root=pathlib.Path(__file__).resolve().parent.parent; ds=root/'04_DATASETS'; out=root/'eval'/'out'
r=pd.read_csv(out/'eval_predictions.csv').fillna('')
M={'POOR_QUALITY':['IMAGE_BLURRY','IMAGE_CROPPED'],'NAME_SPELLING':['NAME_SPELLING_VARIANT'],'FACE_LOW':['FACE_MATCH_LOW'],'NAME_MISMATCH_HARD':['NAME_MISMATCH']}
st={};n=full=0
for _,x in r.iterrows():
    ec={c.strip() for c in x.codes.split(';') if c.strip()}
    ts=[t.strip() for t in x.truth_reasons.split(';') if t.strip() and 'ADDRESS_STATE' not in t]
    for t in ts:
        s=st.setdefault(t,[0,0]); s[0]+=1; s[1]+=bool(ec & set(M.get(t,[t])))
    if x.truth=='NEEDS_MORE_INFO':
        n+=1; full+=all(ec & set(M.get(t,[t])) for t in ts)
d=pd.read_csv(ds/'documents.csv'); t=pd.read_csv(ds/'application_truth.csv')
rank={'ACCEPT':0,'REUPLOAD':1,'NEEDS_INFO':1,'REJECT':2}
roll=d.assign(k=d.human_verdict.map(rank)).groupby('application_id').k.max().map({0:'APPROVE',1:'NEEDS_MORE_INFO',2:'REJECT'})
t['roll']=t.application_id.map(roll)
h=r[r.human.astype(str)=='True']
res={'reasons':st,'nmi_full':[full,n],'reviewer_rollup_acc':float((t.roll==t.final_decision).mean()),'human_routed_truth':h.truth.value_counts().to_dict()}
(out/'extra.json').write_text(json.dumps(res,indent=1)); print(res)
