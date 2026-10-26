from pathlib import Path
import json,re,itertools,hashlib,statistics,collections
import numpy as np
B=Path(__file__).resolve().parent
D=json.JSONDecoder().raw_decode((B.parent/'data.js').read_text().split(' = ',1)[1])[0];S=D['sources'];core=D['stage5']['core_entities'];pairs=list(itertools.combinations(core,2));pairidx={frozenset(p):i for i,p in enumerate(pairs)}
def tokenize(text):
 out=[]
 for m in re.finditer(r'\S+',text):
  w=re.sub(r'[^א-תA-Za-z0-9]','',m.group())
  if w:out.append((w,m.start(),m.end()))
 return out
T={k:tokenize(v['text']) for k,v in S.items()}
def grams(k,n):return {tuple(t[0] for t in T[k][i:i+n]) for i in range(len(T[k])-n+1)}
G={(k,n):grams(k,n) for k in S for n in [3,5,7]};BG={n:set().union(*(G[k,n] for k in S if k.endswith('|RAMBAN'))) for n in [3,5,7]}
def order(s):return tuple(map(int,s.split('_')))
sections=sorted({v['section'] for v in S.values()},key=order)
balanced=[s for s in sections if all(s+'|'+c in S for c in core+['RAMBAN'])]
q=json.JSONDecoder().raw_decode((B.parent.parent/'data/quant-reports.js').read_text().split(' = ',1)[1])[0]
raw={(str(r['section']),frozenset([r['comm_a'],r['comm_b']])):r['raw'] for r in q['quant']['כל_הזוגות_מדורגים']}
def jacc(s,a,b,n):
 aa=G[s+'|'+a,n]-BG[n];bb=G[s+'|'+b,n]-BG[n];return len(aa&bb)/len(aa|bb) if aa|bb else 0
rows=[{'section':s,'a':a,'b':b,'raw':raw.get((s,frozenset([a,b]))),'j3':jacc(s,a,b,3),'j5':jacc(s,a,b,5)} for s in balanced for a,b in pairs]
def ranks(x):
 x=np.asarray(x);return np.array([(np.sum(x<y)+(np.sum(x==y)-1)/2)/9 for y in x])
def stability(rr,metric,family=False,permutations=1000):
 secs=sorted(set(r['section'] for r in rr),key=order);arr=np.array([[next(r[metric] for r in rr if r['section']==s and (r['a'],r['b'])==p) for p in pairs] for s in secs]);X=np.array([ranks(v) for v in arr]);groups=[s.split('_')[0] if family else s for s in secs]
 def score(M):
  pred=np.array([M[[g!=groups[i] for g in groups]].mean(axis=0) for i in range(len(groups))]);den=np.sum((M-.5)**2);return float(1-np.sum((M-pred)**2)/den) if den else None
 obs=score(X);rng=np.random.default_rng(112);null=[]
 for _ in range(permutations):
  z=[]
  for row in X:
   perm=rng.permutation(5);mapping=[pairidx[frozenset([core[perm[core.index(a)]],core[perm[core.index(b)]]])] for a,b in pairs];z.append(row[mapping])
  null.append(score(np.array(z)))
 winners=[{'section':s,'pairs':[list(pairs[j]) for j in np.flatnonzero(v==v.max())]} for s,v in zip(secs,arr)]
 return {'sections':secs,'n_sections':len(secs),'metric':metric,'family_out':family,'cv_R2':obs,'null_95pct':float(np.quantile(null,.95)),'permutation_tail':(1+sum(v>=obs for v in null))/(len(null)+1),'permutations':permutations,'pair_mean_ranks':[{'a':a,'b':b,'rank_score':float(X[:,i].mean())} for i,(a,b) in enumerate(pairs)],'section_ranks':[{'section':s,'scores':list(map(float,v))} for s,v in zip(secs,X)],'top_pairs':winners}
A={'balanced_sections':balanced,'rows':rows,'tests':[]}
for metric in ['raw','j3']:
 for exclusion,family in [([],False),(['21','29'],False),([],True)]:
  rr=[r for r in rows if r['section'] not in exclusion];o=stability(rr,metric,family);o['excluded']=exclusion;A['tests'].append(o)
print('A',[(x['metric'],x['excluded'],x['family_out'],round(x['cv_R2'],3),x['permutation_tail']) for x in A['tests']],flush=True)
# B: 5-gram positions are merged on each text, avoiding overlapping-window inflation.
def spans(indices,n):
 runs=[]
 for i in sorted(indices):
  if runs and i<=runs[-1][1]:runs[-1][1]=max(runs[-1][1],i+n)
  else:runs.append([i,i+n])
 return runs
K,Q=core[:2];Bres=[]
for s in sorted(D['stage5']['scope_sections'],key=order):
 ak,bk=s+'|'+K,s+'|'+Q;aa,bb=G[ak,5],G[bk,5];common=aa&bb;local=common-G[s+'|RAMBAN',5];glob=common-BG[5]
 thirdkeys=[k for k,v in S.items() if v['entity'] not in [K,Q,'KeterShemTovMS_L','RAMBAN']]
 other=set().union(*(G[k,5] for k in thirdkeys));exclusive=glob-other
 def covered(k,gg,n=5):
  ts=T[k];indices=[i for i in range(len(ts)-n+1) if tuple(x[0] for x in ts[i:i+n]) in gg];return spans(indices,n)
 ar,br=covered(ak,glob),covered(bk,glob);ear,ebr=covered(ak,exclusive),covered(bk,exclusive)
 blockdetails=[]
 # exact maximal matches starting at a shared eligible 5-gram, one per diagonal; retain duplicated occurrence mapping explicitly
 idx=collections.defaultdict(list)
 for j in range(len(T[bk])-4):idx[tuple(x[0] for x in T[bk][j:j+5])].append(j)
 matches=[]
 for i in range(len(T[ak])-4):
  g=tuple(x[0] for x in T[ak][i:i+5])
  if g not in glob:continue
  for j in idx[g]:
   if i and j and T[ak][i-1][0]==T[bk][j-1][0] and tuple(x[0] for x in T[ak][i-1:i+4]) in glob:continue
   n=5
   while i+n<len(T[ak]) and j+n<len(T[bk]) and T[ak][i+n][0]==T[bk][j+n][0]:n+=1
   matches.append((i,j,n))
 for i,j,n in sorted(matches,key=lambda x:-x[2]):
  g5={tuple(x[0] for x in T[ak][t:t+5]) for t in range(i,i+n-4)}
  def quote(k,st,sz):
   start,end=T[k][st][1],T[k][st+sz-1][2];return {'start':start,'end':end,'quote':S[k]['text'][start:end]}
  blockdetails.append({'words':n,'a':quote(ak,i,n),'b':quote(bk,j,n),'exclusive_5grams':len(g5&exclusive),'third_work_matches':sorted({S[k]['entity'] for k in thirdkeys if g5&G[k,5]})})
 norms={}
 for n in [3,5,7]:
  vals=G[ak,n]&G[bk,n]-BG[n];norms[str(n)]=len(vals)
 Bres.append({'section':s,'a':K,'b':Q,'raw':raw.get((s,frozenset([K,Q]))),'a_tokens':len(T[ak]),'b_tokens':len(T[bk]),'local_5grams':len(local),'global_5grams':len(glob),'exclusive_5grams':len(exclusive),'a_runs':ar,'b_runs':br,'a_covered':sum(e-b for b,e in ar),'b_covered':sum(e-b for b,e in br),'a_coverage':sum(e-b for b,e in ar)/len(T[ak]),'b_coverage':sum(e-b for b,e in br)/len(T[bk]),'a_exclusive_runs':ear,'b_exclusive_runs':ebr,'sensitivity_n':norms,'matches':blockdetails})
Bresult={'rows':Bres,'summary':{}}
for exc in [[],['21','29']]:
 rr=[r for r in Bres if r['section'] not in exc];Bresult['summary']['all' if not exc else 'without_peaks']={'n':len(rr),'local_positive':sum(r['local_5grams']>0 for r in rr),'global_positive':sum(r['global_5grams']>0 for r in rr),'exclusive_positive':sum(r['exclusive_5grams']>0 for r in rr),'global_grams':sum(r['global_5grams'] for r in rr),'merged_a_regions':sum(len(r['a_runs']) for r in rr),'merged_b_regions':sum(len(r['b_runs']) for r in rr),'long8_sections':[r['section'] for r in rr if any(m['words']>=8 for m in r['matches'])],'exclusive8_sections':[r['section'] for r in rr if any(m['words']>=8 and m['exclusive_5grams'] for m in r['matches'])]}
print('B',Bresult['summary'],flush=True)
# C: paired base anchoring + transparent strings; no semantic inference from marker alone.
marker_patterns={'intent':r'כוונת הרב|כונת הרב|כוונת הרמב["״]?ן|כונת הרמב["״]?ן','teacher':r'(?<![א-ת])(?:מורי|רבותי|רבותיי|קבלתי|קיבלתי|שמעתי)(?![א-ת])','boundary':r'לא (?:אוכל|אוכַל|אוכל|ידעתי)|איני יכול|אין לי רשות|לא ארצה|איני רשאי'}
Crows=[];hits=[]
for s in sections:
 if s+'|RAMBAN' not in S:continue
 for c in core:
  k=s+'|'+c
  if k not in S:continue
  text=S[k]['text'];rec={'section':s,'entity':c,'tokens':len(T[k])}
  for n in [3,5]:
   bg=G[s+'|RAMBAN',n];gg=G[k,n]&bg
   bp=spans([i for i in range(len(T[s+'|RAMBAN'])-n+1) if tuple(x[0] for x in T[s+'|RAMBAN'][i:i+n]) in gg],n)
   cp=spans([i for i in range(len(T[k])-n+1) if tuple(x[0] for x in T[k][i:i+n]) in gg],n)
   rec['base_coverage'+str(n)]=sum(e-b for b,e in bp)/len(T[s+'|RAMBAN']) if T[s+'|RAMBAN'] else 0;rec['comment_coverage'+str(n)]=sum(e-b for b,e in cp)/len(T[k]) if T[k] else 0
  for label,pat in marker_patterns.items():
   mm=list(re.finditer(pat,text));rec[label]=len(mm);rec[label+'_per1000']=len(mm)*1000/len(T[k]) if T[k] else 0
   for m in mm:hits.append({'section':s,'entity':c,'marker':label,'match':m.group(),'start':m.start(),'end':m.end(),'context_start':max(0,m.start()-100),'context_end':min(len(text),m.end()+140),'context':text[max(0,m.start()-100):m.end()+140]})
  Crows.append(rec)
cs=[s for s in sections if all(s+'|'+c in S for c in ['IbnShuib',K,'RAMBAN'])]
oldC=sorted({e['section'] for e in D['evidence'] if e.get('question_id')=='C'}|{p['section'] for p in D['interpretive_profiles']+D['new_profiles']},key=order)
def csummary(ss):
 out={}
 for metric in ['tokens','base_coverage3','base_coverage5','comment_coverage3','comment_coverage5','intent_per1000','teacher_per1000','boundary_per1000']:
  x=[next(r[metric] for r in Crows if r['section']==s and r['entity']=='IbnShuib') for s in ss];y=[next(r[metric] for r in Crows if r['section']==s and r['entity']==K) for s in ss];diff=[a-b for a,b in zip(x,y)]
  out[metric]={'I_median':statistics.median(x),'K_median':statistics.median(y),'median_paired_difference':statistics.median(diff),'I_greater':sum(v>1e-12 for v in diff),'K_greater':sum(v< -1e-12 for v in diff),'ties':sum(abs(v)<=1e-12 for v in diff)}
 return {'sections':ss,'n':len(ss),'metrics':out}
C={'rows':Crows,'marker_patterns':marker_patterns,'marker_hits':hits,'previous_read_sections':oldC,'paired':csummary(cs),'outside_previous':csummary([s for s in cs if s not in oldC]),'balanced_author_profiles':[]}
for c in core:
 rr=[r for r in Crows if r['section'] in balanced and r['entity']==c];C['balanced_author_profiles'].append({'entity':c,'n':len(rr),**{m:statistics.mean(r[m] for r in rr) for m in ['base_coverage3','comment_coverage3','intent_per1000','teacher_per1000','boundary_per1000']}})
print('C',C['paired'], '\nC new',C['outside_previous'],flush=True)
# D: equal section and partner weighting; no causal arrows on similarity network.
Dr=[]
for n in [3,5]:
 for exc in [[],['21','29'],['6','11','18','19_2','32'],['6','11','18','19_2','32','21','29']]:
  ss=[s for s in balanced if s not in exc];vals=[]
  for c in core:
   by=[statistics.mean(jacc(s,c,o,n) for o in core if o!=c) for s in ss]
   vals.append({'entity':c,'mean_strength':statistics.mean(by),'median_strength':statistics.median(by),'per_section':[{'section':s,'strength':v} for s,v in zip(ss,by)]})
  vals.sort(key=lambda v:-v['mean_strength']);Dr.append({'n':n,'excluded':exc,'sections':ss,'ranking':vals})
searchpat=r'כתר[\s־-]+שם[\s־-]+טוב|כש["״\'׳]?ט|(?:שם[\s־-]+טוב(?:[\s־-]+(?:בן|אבן)[\s־-]+גאון)?)|(?:אבן|בן)[\s־-]+גאון|סתרי[\s־-]+סתרים'
mentions=[]
for k,v in S.items():
 for m in re.finditer(searchpat,v['text']):mentions.append({'section':v['section'],'entity':v['entity'],'start':m.start(),'end':m.end(),'match':m.group(),'context':v['text'][max(0,m.start()-150):m.end()+220]})
Dresult={'network_tests':Dr,'mention_pattern':searchpat,'mentions':mentions,'explicit_events':D['reception_events'],'recipient_work_labels':sorted({e['entity'] for e in D['reception_events']})}
print('D',[(r['n'],r['excluded'],[(v['entity'],round(v['mean_strength'],5)) for v in r['ranking']]) for r in Dr],flush=True);print('mentions',len(mentions),flush=True)
O={'version':'11.2','base_research_version':D['version'],'base_sha256':hashlib.sha256(json.dumps(D,ensure_ascii=False).encode()).hexdigest(),'analysis_scope':'fixed available corpus, exploratory robustness, not population inference','plan':json.loads((B/'analysis-plan.json').read_text()),'entities':D['entities'],'A':A,'B':Bresult,'C':C,'D':Dresult}
(B/'results.json').write_text(json.dumps(O,ensure_ascii=False,indent=2));(B/'marker_contexts.txt').write_text('\n\n'.join(f"{i} {h['section']} {h['entity']} {h['marker']}: {h['context']}" for i,h in enumerate(hits)));(B/'mentions.txt').write_text('\n\n'.join(f"{i} {h['section']} {h['entity']} {h['match']}: {h['context']}" for i,h in enumerate(mentions)))
