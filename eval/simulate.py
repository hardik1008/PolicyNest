"""Before/after simulation of time to certificate on the applications workbook (directional, not a forecast).
Writes eval/out/simulation.json.

Scenario "engine": for every certified journey, the review zone (DOCS_SUBMITTED -> KYC_VERIFIED) is replaced by
  - 10 minutes when the file was never returned (a conservative ceiling; the engine decides in seconds);
  - otherwise the applicant's own time to answer the FIRST fix request (kept as observed) + 10 minutes,
    because the engine asks for everything in one message, so later loops and every queue wait disappear.
Everything else in the journey (applying, training, exam) is kept exactly as observed.
Scenario "engine + instant training link": as above, and the KYC -> TRAINING_STARTED gap is capped at 1 hour (assumption).
Drop-off: if silence after a fix request fell from today's rate to the 10% target, how many more applicants would certify,
using today's certification rate of applicants who did reply. This is a what-if, not a prediction."""
import pandas as pd, numpy as np, json, pathlib
root=pathlib.Path(__file__).resolve().parent.parent; ds=root/'04_DATASETS'; out=root/'eval'/'out'
apps=pd.read_csv(ds/'applications.csv').drop_duplicates('application_id')
ev=pd.read_csv(ds/'stage_events.csv'); ev['t']=pd.to_datetime(ev.event_time,format='ISO8601')
first=ev.sort_values('t').groupby(['application_id','event']).t.first().unstack()
H=lambda a,b,df=first:(df[b]-df[a]).dt.total_seconds()/3600
cert=first[first.CERTIFIED.notna()].copy()
total=H('APPLICATION_STARTED','CERTIFIED',cert)
zone=H('DOCS_SUBMITTED','KYC_VERIFIED',cert)
returned=cert.DOC_RETURNED.notna()
reply=H('DOC_RETURNED','DOC_REUPLOADED',cert)
eng=np.where(returned, reply.fillna(0)+10/60, 10/60)
sim=total-zone+eng
k2t=H('KYC_VERIFIED','TRAINING_STARTED',cert)
sim2=sim-k2t+np.minimum(k2t,1.0)
def stats(x): x=pd.Series(x).dropna()/24; return {'median':round(float(x.median()),2),'p25':round(float(x.quantile(.25)),2),'p90':round(float(x.quantile(.9)),2)}
bins=list(range(0,16))+[1e9]
def hist(x): x=pd.Series(x).dropna()/24; c=pd.cut(x,bins,right=False).value_counts(sort=False); return [int(v) for v in c.values]
ret_ids=set(ev[ev.event=='DOC_RETURNED'].application_id)
silent=set(ev[(ev.event=='AUTO_EXPIRED')&ev.note.str.contains('No response',na=False)].application_id)
apps['returned']=apps.application_id.isin(ret_ids)
replied=apps[apps.returned&~apps.application_id.isin(silent)]
conv=float((replied.status=='CERTIFIED').mean())
extra=(len(silent)-round(0.10*len(ret_ids)))*conv
res={'certified':int(len(cert)),'returned_share_of_certified':round(float(returned.mean()),4),
 'today':stats(total),'engine':stats(sim),'engine_plus_training_link':stats(sim2),
 'hist_bins_days':[f'{b}' for b in bins[:-1]],'hist_today':hist(total),'hist_engine':hist(sim),
 'review_zone_median_hours_today':round(float(zone.median()),1),'review_zone_median_hours_engine':round(float(pd.Series(eng).median()),2),
 'silence':{'returned_apps':len(ret_ids),'silent_today':len(silent),'rate_today':round(len(silent)/len(ret_ids),4),'target_rate':0.10,'repliers_certify_rate':round(conv,4),'extra_agents_if_target':int(round(extra)),'certified_today':int((apps.status=='CERTIFIED').sum())}}
(out/'simulation.json').write_text(json.dumps(res,indent=1)); print(json.dumps(res,indent=1))
# Reviewer minutes per application (estimate): only cases the engine routes to a person get a reviewer, and each is
# assumed to take today's mean review time per application from the test set (no faster copilot assumed).
docs=pd.read_csv(ds/'documents.csv'); per_app=docs.groupby('application_id').reviewer_minutes.sum()
pred=pd.read_csv(out/'eval_predictions.csv'); routed=float((pred.human.astype(str)=='True').mean())
res['reviewer_minutes']={'today_mean_per_application':round(float(per_app.mean()),1),'routed_share':round(routed,4),'estimate_per_application':round(float(per_app.mean())*routed,2)}
(out/'simulation.json').write_text(json.dumps(res,indent=1)); print(res['reviewer_minutes'])
