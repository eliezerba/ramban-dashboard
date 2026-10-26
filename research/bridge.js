(()=>{'use strict';
 let returnHash='#question-a',busy=false;
 const status=document.getElementById('researchBridgeStatus'),back=document.getElementById('researchReturn');
 const safeHash=h=>typeof h==='string'&&/^#[A-Za-z0-9_:-]+$/.test(h)?h:'#question-a';
 async function run(m){
  if(busy){status.textContent='המעבר הקודם עדיין מתבצע.';return false;}
  if(!['text','network','quant'].includes(m.layer)){status.textContent='שכבה לא תקינה.';return false;}
  busy=true;status.textContent='מאמת את המקור…';
  try{
   if(m.type==='ramban:source-request'){
    const e=window.RAMBAN_RESEARCH_BRIDGE.evidence[m.evidenceId];if(!e)throw Error('ראיה לא מוכרת.');
    await window.RambanDashboard.openResearchRecord(e,m.layer);returnHash=safeHash(m.returnHash||'#ev-'+e.evidence_id);
   }else if(m.type==='ramban:pair-request'){
    await window.RambanDashboard.openResearchPair(m.section,m.a,m.b,m.layer);returnHash=safeHash(m.returnHash);
   }else return false;
   back.hidden=false;back.textContent='חזרה להפניה בארבע שאלות המחקר';status.textContent='המקור נפתח בהקשר שנבחר.';return true;
  }catch(e){status.textContent=e.message||'המעבר נכשל.';return false;}finally{busy=false;}
 }
 window.addEventListener('message',event=>{
  const frame=document.getElementById('researchStudyFrame');if(!frame||event.source!==frame.contentWindow)return;
  if(location.origin!=='null'&&event.origin!==location.origin)return;
  const m=event.data;if(m?.version!=='1.1'||!['ramban:source-request','ramban:pair-request'].includes(m.type))return;
  run(m);
 });
 back.addEventListener('click',async()=>{await window.RambanDashboard.showResearch();document.getElementById('researchStudyFrame')?.contentWindow.postMessage({type:'ramban:return-reference',version:'1.1',hash:returnHash},location.origin==='null'?'*':location.origin);});
 const params=new URLSearchParams(location.search);if(params.has('evidence'))run({type:'ramban:source-request',evidenceId:params.get('evidence'),layer:params.get('layer')||'text'});else if(params.has('researchSection'))run({type:'ramban:pair-request',section:params.get('researchSection'),a:params.get('a'),b:params.get('b'),layer:params.get('layer')||'text'});
})();
