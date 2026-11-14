/* PS-01 test-set evaluation. Runs the exact engine block from PolicyNest.html on all 600 applications.
   Usage: node eval/run_eval.js <PolicyNest.html> <datasets dir> <out dir> */
const fs=require('fs'),path=require('path'),Papa=require('papaparse');
const [,,HTML,DS,OUT]=process.argv;
const html=fs.readFileSync(HTML,'utf8');
const block=html.slice(html.indexOf('/* ENGINE:START'),html.indexOf('/* ENGINE:END */'));
/* ADR 0001: pin every result to the exact code it scored. SHA-256 of the block above (from the ENGINE:START
   comment up to, not including, the ENGINE:END comment), with CRLF normalised to LF. */
const ENGINE_SHA256=require('crypto').createHash('sha256').update(block.replace(/\r\n/g,'\n'),'utf8').digest('hex');
const E=new Function(block+';return {parseDoc,decide,decisionOf,followupItems,nameTier};')();
const csv=f=>Papa.parse(fs.readFileSync(path.join(DS,f),'utf8'),{header:true,skipEmptyLines:true}).data;
const docs=csv('documents.csv'),truth=csv('application_truth.csv');
const apps={};csv('applications.csv').forEach(r=>{if(!apps[r.application_id])apps[r.application_id]=r});
const K={PAN:'PAN',AADHAAR_FRONT:'AADHAAR_FRONT',AADHAAR_BACK:'AADHAAR_BACK',CLASS10_MARKSHEET:'CLASS10',CANCELLED_CHEQUE:'BANK',SELFIE:'SELFIE'};
const byApp={};docs.forEach(d=>{(byApp[d.application_id]=byApp[d.application_id]||[]).push(d)});
const rows=[];let ms=0;
for(const t of truth){
  const id=t.application_id,a=apps[id]||{},x={};
  for(const d of byApp[id]||[]){const k=K[d.doc_type];const conf=d.ocr_confidence===''?null:+d.ocr_confidence;
    if(k==='SELFIE') x.SELFIE={src:'Test-set selfie',conf:conf,missing:[]};
    else x[k]=Object.assign({src:'Test-set OCR'},E.parseDoc(k,d.ocr_text,conf));
    if(k==='SELFIE'&&d.face_match_score!=='') x.face=+d.face_match_score; }
  x.penny=t.penny_drop_name_returned||null; x.registry=String(t.irdai_posp_registry_hit).toLowerCase()==='true';
  const f={name:t.declared_name,dob:String(t.declared_dob).slice(0,10),pan:t.declared_pan,state:t.declared_state,education:t.declared_education};
  const start=new Date(String(a.created_at||'2026-06-01').replace(' ','T'));
  const t0=process.hrtime.bigint();
  const r=E.decide(f,x,start);
  ms+=Number(process.hrtime.bigint()-t0)/1e6;
  const human=r.checks.filter(c=>c.res==='HUMAN');
  /* What the engine finally says. HUMAN_REVIEW is scored by the AI's recommendation: a different-person name is a
     recommended REJECT; other Human-only items (face 0.60-0.75, surname change, unlisted board) go to a person with
     no automatic outcome, scored as NEEDS_MORE_INFO (the applicant is not approved without a person). */
  let pred=r.decision;
  if(pred==='HUMAN_REVIEW') pred=human.some(c=>c.code==='NAME_MISMATCH')?'REJECT':'NEEDS_MORE_INFO';
  const items=r.decision==='NEEDS_MORE_INFO'?E.followupItems(r.checks,x):[];
  rows.push({id,truth:t.final_decision,engine:r.decision,pred,human:r.decision==='HUMAN_REVIEW',
    codes:[...new Set(r.checks.filter(c=>c.res!=='PASS'&&c.res!=='INFO'&&c.res!=='PENDING').map(c=>c.code||c.res))].join('; '),
    truth_reasons:t.decision_reasons||'',name_cat:t.name_match_category,hard:t.is_hard_case,state:a.state||t.declared_state,gender:a.gender||'',
    followup_items:items.length,followup_messages:items.length?1:0});
}
const L=['APPROVE','NEEDS_MORE_INFO','REJECT'];
const cm={};L.forEach(a=>{cm[a]={};L.forEach(b=>cm[a][b]=0)});rows.forEach(r=>cm[r.truth][r.pred]++);
const n=rows.length,acc=rows.filter(r=>r.truth===r.pred).length/n;
const pr=c=>{const tp=cm[c][c],p=L.reduce((s,a)=>s+cm[a][c],0),t=L.reduce((s,b)=>s+cm[c][b],0);return {precision:p?tp/p:null,recall:t?tp/t:null,tp,predicted:p,actual:t}};
const stp=rows.filter(r=>!r.human&&r.truth===r.pred).length/n;
const rejCaught=rows.filter(r=>r.truth==='REJECT'&&(r.pred==='REJECT'||r.human)).length/rows.filter(r=>r.truth==='REJECT').length;
const wrongApprove=rows.filter(r=>r.pred==='APPROVE'&&r.truth!=='APPROVE');
function group(key){const g={};rows.forEach(r=>{const k=r[key]||'(blank)';g[k]=g[k]||{n:0,ok:0};g[k].n++;if(r.truth===r.pred)g[k].ok++});return Object.fromEntries(Object.entries(g).sort((a,b)=>b[1].n-a[1].n).map(([k,v])=>[k,{n:v.n,accuracy:+(v.ok/v.n).toFixed(4)}]))}
const nmi=rows.filter(r=>r.engine==='NEEDS_MORE_INFO');
const res={run_at:new Date().toISOString(),engine:(html.match(/var ENGINE="([^"]+)"/)||[])[1],engine_sha256:ENGINE_SHA256,n,accuracy:acc,engine_ms_per_application:ms/n,confusion_rows_truth_cols_pred:cm,REJECT:pr('REJECT'),NEEDS_MORE_INFO:pr('NEEDS_MORE_INFO'),APPROVE:pr('APPROVE'),
  reject_recall_incl_routed_to_human:rejCaught,straight_through_rate:stp,routed_to_human:rows.filter(r=>r.human).length,
  wrongful_approvals:wrongApprove.length,follow_up:{applications:nmi.length,messages_per_application:nmi.length?nmi.reduce((s,r)=>s+r.followup_messages,0)/nmi.length:null,mean_items:nmi.length?nmi.reduce((s,r)=>s+r.followup_items,0)/nmi.length:null},
  by_gender:group('gender'),by_state:group('state'),by_name_pattern:group('name_cat')};
fs.mkdirSync(OUT,{recursive:true});
fs.writeFileSync(path.join(OUT,'eval_results.json'),JSON.stringify(res,null,1));
fs.writeFileSync(path.join(OUT,'eval_predictions.csv'),Papa.unparse(rows));
console.log(JSON.stringify({accuracy:acc,REJECT:pr('REJECT'),NEEDS_MORE_INFO:pr('NEEDS_MORE_INFO'),APPROVE:pr('APPROVE'),stp,rejCaught,wrongApprove:wrongApprove.length,human:res.routed_to_human},null,1));
console.log(cm);
