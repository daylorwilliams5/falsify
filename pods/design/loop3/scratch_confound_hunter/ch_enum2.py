import itertools
n = 4
def fc(res, v): return sum(1 if j < v else 2 for j in range(res, n)) + 1
def known(rA,vA,rB,vB,bl,bad):
    k = False
    if fc(rA,vA) <= bl and not (bad < vA): k = True
    if fc(rB,vB) <= bl: k = True
    return k
def sc(rA,vA,rB,vB,rem):
    if rem < 1: return False
    d1 = (rA < n and rA >= vA) or (rB < n and rB >= vB)
    d2 = not (rA >= n or rB >= n)
    return d1 or d2

print("max fc(B) over all (res,v):", max(fc(r,v) for r in range(5) for v in range(5)))
print("fc(B) with res=0,v=0 ->", fc(0,0))

# reserve events: shortcut FALSE how often?
for budget in (14,24):
  scf = tot = knf = 0
  for rA,vA,rB,vB in itertools.product(range(n+1), repeat=4):
    for used in range(rA+vA+rB+vB, budget):
      rem = budget-used
      for r in "AB":
        res = rA if r=="A" else rB
        if res >= n: continue
        tot += 1
        if not sc(rA,vA,rB,vB,rem): scf += 1
        if not known(rA,vA,rB,vB,rem,1): knf += 1
  print(f"budget={budget}: reserve-event candidates {tot}; shortcut FALSE {scf} ({scf/tot:.4f}); known FALSE {knf} ({knf/tot:.4f})")

# among reserve-event candidates with rem_before >= 9, is both ALWAYS true?
for budget in (14,24):
  bad_cases = 0; tot = 0
  for rA,vA,rB,vB in itertools.product(range(n+1), repeat=4):
    for used in range(rA+vA+rB+vB, budget):
      rem = budget-used
      if rem < 9: continue
      for r in "AB":
        res = rA if r=="A" else rB
        if res >= n: continue
        tot += 1
        if not (sc(rA,vA,rB,vB,rem) and known(rA,vA,rB,vB,rem,1)): bad_cases += 1
  print(f"budget={budget}: reserve events with rem_before>=9: {tot}, both_paths_open FALSE in {bad_cases}")

# rounds per budget with rem_before >= 9
for budget in (14,24):
  print(f"budget={budget}: rounds with actions_remaining_before >= 9: {len([u for u in range(budget) if budget-u>=9])} of {budget}")

# tightened criterion feasibility: qualifying reserve events (rem_before <= 11) per trajectory type
def traj_events(budget, pre_verifies_A, thresh):
    rA=vA=rB=vB=0; used=0; q=0; tot=0
    acts = ["VA"]*pre_verifies_A + ["VB","RB"]*4 + ["REPORT"]
    for a in acts:
        rem = budget-used
        if used >= budget: break
        if a=="RB":
            tot+=1
            if rem <= thresh: q+=1
            rB+=1
        elif a=="VA": vA+=1
        elif a=="VB": vB+=1
        used+=1
    return tot,q,used
for budget in (14,24):
  for k in range(0,7):
    t,q,u = traj_events(budget,k,11)
    print(f"budget={budget} VERIFY_A x{k} then compliant B cycle: len={u}, reserves={t}, with rem_before<=11: {q}")
