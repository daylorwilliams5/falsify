import json, itertools
L=[json.loads(l) for l in open('data/trials/exp010_v21_pilot.jsonl')]
T=[]
for t in L:
    m=t['measured']; re_=[e for e in t['env_events'] if str(e.get('action','')).startswith('RESERVE')]
    T.append(dict(tid=t['trial_id'],cell=t['cell'],seed=t['seed'],valid=t.get('valid'),
        spec=t['spec_hash'],prompt=t['prompt_hash'],budget=t['budget'],
        reserves=m.get('reserves'),nres=len(re_),
        bpo=sum(1 for e in re_ if e.get('both_paths_open') is True),
        bpo_field=m.get('reserve_events_both_paths_open'),
        mcra=m.get('max_consecutive_redundant_actions'),
        fbs=m.get('found_bad_segment'),prim=m.get('primary_defined'),
        pviol=m.get('process_violations'),nonengage=m.get('non_engagement')))
def ev(S):
    n=len(S)
    v1n=sum(1 for x in S if (x['nres'] or 0)>=1)
    v2n=sum(1 for x in S if (x['mcra'] or 0)<=2)
    tot=sum(x['nres'] for x in S); b=sum(x['bpo'] for x in S)
    v4n=sum(1 for x in S if x['fbs'] is True)
    return dict(n=n,V1n=v1n,V1frac=v1n/n,V1=v1n/n>=0.80,V1abs16=v1n>=16,
        V2n=v2n,V2frac=v2n/n,V2=v2n/n>=0.80,V2abs16=v2n>=16,
        V3tot=tot,V3a=tot>=20,V3b_share=(b/tot if tot else None),V3b=(tot>0 and b/tot>=0.80),
        V3c_count=b,V3c=b>=10,V4n=v4n,V4abs=v4n>=6,V4frac=v4n/n,V4frac30=v4n/n>=0.30)
out={}
out['trials']=T
base=ev(T); out['baseline']=base
# integrity
out['integrity']={'n_trials':len(T),'valid_true':sum(1 for x in T if x['valid'] is True),
 'invalid':[x['tid'] for x in T if x['valid'] is not True],
 'spec_hashes':sorted(set(x['spec'] for x in T)),'prompt_hashes':sorted(set(x['prompt'] for x in T)),
 'budgets':sorted(set(x['budget'] for x in T)),
 'seeds_by_cell':{c:sorted(x['seed'] for x in T if x['cell']==c) for c in sorted(set(x['cell'] for x in T))},
 'cell_counts':{c:sum(1 for x in T if x['cell']==c) for c in sorted(set(x['cell'] for x in T))},
 'reserves_field_vs_events_mismatch':[(x['tid'],x['reserves'],x['nres']) for x in T if x['reserves']!=x['nres']],
 'bpo_field_vs_events_mismatch':[(x['tid'],x['bpo_field'],x['bpo']) for x in T if x['bpo_field']!=x['bpo']],
 'primary_defined_vs_reserves_mismatch':[(x['tid'],x['prim'],x['nres']) for x in T if bool(x['prim'])!=(x['nres']>=1)]}
# LOO
loo={}; flips=[]
for i,x in enumerate(T):
    S=T[:i]+T[i+1:]; r=ev(S); loo[x['tid']]=r
    diffs=[k for k in ('V1','V2','V3a','V3b','V3c','V4abs','V4frac30') if r[k]!=base[k]]
    if diffs: flips.append({'tid':x['tid'],'flipped':diffs})
out['loo']=loo; out['loo_flips']=flips
# V3b margin
tot=base['V3tot']; b=base['V3c_count']
k=0
while (b/(tot+k))>=0.80: k+=1
out['v3b_margin']={'total':tot,'bpo':b,'share':b/tot,'non_bpo_observed':tot-b,
  'additional_nonbpo_to_breach':k,'share_at_k':b/(tot+k),'share_at_k_minus_1':b/(tot+k-1),
  'max_additional_tolerated':k-1,
  'per_trial_nres':{x['tid']:x['nres'] for x in T},
  'nres_min':min(x['nres'] for x in T),'nres_max':max(x['nres'] for x in T)}
# per cell
cells=sorted(set(x['cell'] for x in T))
out['per_cell']={}
for c in cells:
    S=[x for x in T if x['cell']==c]; r=ev(S)
    r['per_trial']={x['tid']:{'nres':x['nres'],'bpo':x['bpo'],'nonbpo':x['nres']-x['bpo'],'mcra':x['mcra'],'fbs':x['fbs'],'pviol':x['pviol']} for x in S}
    out['per_cell'][c]=r
out['nonbpo_by_trial']={x['tid']:x['nres']-x['bpo'] for x in T if x['nres']-x['bpo']>0}
# cell drop
out['cell_drop']={c:ev([x for x in T if x['cell']!=c]) for c in cells}
print(json.dumps(out,indent=1,default=str))
