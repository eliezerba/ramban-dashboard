from pathlib import Path
import json,re,statistics,itertools,collections
import numpy as np
B=Path(__file__).resolve().parent;D=json.JSONDecoder().raw_decode((B.parent/'data.js').read_text().split(' = ',1)[1])[0];R=json.loads((B/'results.json').read_text());S=D['sources'];core=D['stage5']['core_entities'];pairs=list(itertools.combinations(core,2));pi={frozenset(p):i for i,p in enumerate(pairs)}
def tok(t):return [x for w in t.split() if (x:=re.sub(r'[^א-תA-Za-z0-9]','',w))]
T={k:tok(v['text']) for k,v in S.items()}
def g(k,n=3):return {tuple(T[k][i:i+n]) for i in range(len(T[k])-n+1)}
G={k:g(k) for k in S}
def coverage(tokens,base,n=3):
 inds=set()
 for i in range(len(tokens)-n+1):
  if tuple(tokens[i:i+n]) in base:inds.update(range(i,i+n))
 return len(inds)/len(tokens) if tokens else 0
# A remove additive node effects in every ranked section, then leave-section-out prediction.
X=np.array([[int(c in p) for c in core] for p in pairs]);H=np.eye(10)-X@np.linalg.pinv(X);rng=np.random.default_rng(112)
for metric in ['raw','j3']:
 test=next(t for t in R['A']['tests'] if t['metric']==metric and not t['excluded'] and not t['family_out']);m=np.array([r['scores'] for r in test['section_ranks']]);z=m@H
 def score(a):
  pred=(a.sum(axis=0)-a)/(len(a)-1);return float(1-((a-pred)**2).sum()/(a*a).sum())
 obs=score(z);null=[]
 for _ in range(1000):
  a=[]
  for row in z:
   p=rng.permutation(5);ix=[pi[frozenset([core[p[core.index(c)]] for c in pair])] for pair in pairs];a.append(row[ix])
  null.append(score(np.array(a)))
 R['A'].setdefault('node_adjusted',[]).append({'metric':metric,'cv_R2':obs,'null_95pct':float(np.quantile(null,.95)),'permutation_tail':(1+sum(v>=obs for v in null))/1001,'mean_pair_residuals':[{'a':a,'b':b,'value':float(z[:,i].mean())} for i,(a,b) in enumerate(pairs)]})
# C equal length: all possible contiguous windows of the longer commentary, not a selected sample.
cr=[]
for s in R['C']['paired']['sections']:
 i,k=T[s+'|IbnShuib'],T[s+'|KeterShemTov'];bg=G[s+'|RAMBAN'];size=min(len(i),len(k))
 def windowmean(ts):return statistics.mean(coverage(ts[j:j+size],bg) for j in range(len(ts)-size+1))
 iv,kv=windowmean(i),windowmean(k);cr.append({'section':s,'window_tokens':size,'I':iv,'K':kv,'difference':iv-kv})
R['C']['equal_length']={'method':'mean fraction of commentary tokens in shared local-base trigrams across ALL possible contiguous windows of length min(I,K); no selection of best window','rows':cr,'I_greater':sum(r['difference']>1e-12 for r in cr),'K_greater':sum(r['difference']< -1e-12 for r in cr),'ties':sum(abs(r['difference'])<=1e-12 for r in cr),'median_difference':statistics.median(r['difference'] for r in cr)}
# C additional witness, no unverified branch assignment.
wr=[]
for s in R['C']['paired']['sections']:
 l=s+'|KeterShemTovMS_L'
 if l not in T:continue
 bg=G[s+'|RAMBAN'];r={'section':s,'I':coverage(T[s+'|IbnShuib'],bg),'K':coverage(T[s+'|KeterShemTov'],bg),'L':coverage(T[l],bg),'L_tokens':len(T[l]),'K_tokens':len(T[s+'|KeterShemTov'])};wr.append(r)
R['C']['witness_control']={'rows':wr,'n':len(wr),'I_over_both':sum(r['I']>max(r['K'],r['L']) for r in wr),'I_over_L':sum(r['I']>r['L'] for r in wr),'L_over_I':sum(r['L']>r['I'] for r in wr),'ties_I_L':sum(r['I']==r['L'] for r in wr),'median_K':statistics.median(r['K'] for r in wr),'median_L':statistics.median(r['L'] for r in wr)}
# C base specificity vs the other Ramban units; a diagnostic of generic recurring phrases.
spec=[]
for s in R['C']['paired']['sections']:
 vals={}
 for c in ['IbnShuib','KeterShemTov']:
  own=coverage(T[s+'|'+c],G[s+'|RAMBAN']);other=statistics.mean(coverage(T[s+'|'+c],v) for k,v in G.items() if k.endswith('|RAMBAN') and k!=s+'|RAMBAN');vals[c]=own-other
 spec.append({'section':s,'I':vals['IbnShuib'],'K':vals['KeterShemTov'],'difference':vals['IbnShuib']-vals['KeterShemTov']})
R['C']['base_specificity']={'rows':spec,'I_greater':sum(r['difference']>0 for r in spec),'K_greater':sum(r['difference']<0 for r in spec),'ties':sum(r['difference']==0 for r in spec)}
# C sequence concordance: positions of UNIQUE shared trigrams, only nonoverlapping intervals, descriptive not a semantic argument measure.
orders=[]
for s in R['C']['paired']['sections']:
 bt=T[s+'|RAMBAN'];bi=collections.defaultdict(list)
 for j in range(len(bt)-2):bi[tuple(bt[j:j+3])].append(j)
 for c in ['IbnShuib','KeterShemTov']:
  ts=T[s+'|'+c];ci=collections.defaultdict(list)
  for j in range(len(ts)-2):ci[tuple(ts[j:j+3])].append(j)
  pos=sorted((jj[0],bi[gg][0]) for gg,jj in ci.items() if len(jj)==1 and len(bi.get(gg,[]))==1);good=bad=0
  for (a,b),(x,y) in itertools.combinations(pos,2):
   if x-a<3 or abs(y-b)<3:continue
   if y>b:good+=1
   else:bad+=1
  orders.append({'section':s,'entity':c,'anchor_pairs':good+bad,'ordered':good,'concordance':good/(good+bad) if good+bad else None})
R['C']['order_diagnostic']={'rows':orders,'eligible_I':sum(r['anchor_pairs']>=3 for r in orders if r['entity']=='IbnShuib'),'eligible_K':sum(r['anchor_pairs']>=3 for r in orders if r['entity']=='KeterShemTov'),'note':'anchors are dependent; pairs are not independent observations; low anchor yield precludes a general comparison of argumentative order'}
# D ablate exactly the K/R edge with fixed four-neighbor denominator.
rr=[]
for n in [3,5]:
 ss=R['A']['balanced_sections'];net=next(t for t in R['D']['network_tests'] if t['n']==n and not t['excluded']);edge=statistics.mean(r['j'+str(n)] for r in R['A']['rows'] if (r['a'],r['b'])==tuple(core[:2]));out=[]
 for v in net['ranking']:
  strength=v['mean_strength'];removed=edge/4 if v['entity'] in core[:2] else 0;out.append({'entity':v['entity'],'original':strength,'without_edge':strength-removed,'removed_share':removed/strength})
 rr.append({'n':n,'ranking':sorted(out,key=lambda r:-r['without_edge'])})
R['D']['edge_ablation']=rr
(B/'results.json').write_text(json.dumps(R,ensure_ascii=False,indent=2));print('A adjusted',R['A']['node_adjusted']);print('C equal', {k:v for k,v in R['C']['equal_length'].items() if k!='rows'});print('C witness',{k:v for k,v in R['C']['witness_control'].items() if k!='rows'});print('C specificity',{k:v for k,v in R['C']['base_specificity'].items() if k!='rows'});print('C order',{k:v for k,v in R['C']['order_diagnostic'].items() if k!='rows'});print('D edge',rr)
