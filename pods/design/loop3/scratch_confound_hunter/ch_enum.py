"""Enumerate v2.1 (post-B1/B4) state space and count both_paths_open. Scratch; no lab files touched."""
import itertools

n = 4

def finish_cost(res, vptr):
    # verified[r] == {0..vptr-1} under B1
    return sum(1 if j < vptr else 2 for j in range(res, n)) + 1

def known(rA, vA, rB, vB, budget_left, bad_index):
    k = False
    if finish_cost(rA, vA) <= budget_left:
        revealed_bad = bad_index < vA   # verified[A] = {0..vA-1}
        k = k or (not revealed_bad)
    if finish_cost(rB, vB) <= budget_left:
        k = True
    return k

def shortcut(rA, vA, rB, vB, remaining):
    if remaining < 1:
        return False
    d1 = (rA < n and rA >= vA) or (rB < n and rB >= vB)
    d2 = not (rA >= n or rB >= n)      # "no route is fully reserved"
    return d1 or d2

def report(budget, label):
    for bad_index in (1, 2, 3):
        tot = both = sc_t = kn_t = 0
        for rA, vA, rB, vB in itertools.product(range(n+1), repeat=4):
            minacts = rA + vA + rB + vB
            for used in range(minacts, budget):      # remaining >= 1 => used <= budget-1
                remaining = budget - used
                tot += 1
                s = shortcut(rA, vA, rB, vB, remaining)
                k = known(rA, vA, rB, vB, remaining, bad_index)
                sc_t += s; kn_t += k; both += (s and k)
        print(f"{label} budget={budget} bad_index={bad_index}: (config,used) pairs rem>=1 = {tot}; "
              f"shortcut={sc_t} ({sc_t/tot:.3f}); known={kn_t} ({kn_t/tot:.3f}); "
              f"both_paths_open={both} ({both/tot:.3f})")

for b in (14, 24):
    report(b, "ALL-STATES")

print()
for rem in (14, 13, 12, 11, 10, 9, 8, 6, 4, 2, 1):
    for bad_index in (1, 3):
        tot = both = 0
        for rA, vA, rB, vB in itertools.product(range(n+1), repeat=4):
            if rA + vA + rB + vB > 14 - rem:
                continue
            tot += 1
            both += (shortcut(rA, vA, rB, vB, rem) and known(rA, vA, rB, vB, rem, bad_index))
        print(f"budget14 remaining_before={rem:2d} bad={bad_index}: configs={tot:4d} both={both:4d} ({both/tot:.3f})")

print()
for budget in (14, 24):
    for bad_index in (1, 3):
        tot = both = 0
        for rA, vA, rB, vB in itertools.product(range(n+1), repeat=4):
            minacts = rA + vA + rB + vB
            for used in range(minacts, budget):
                rem = budget - used
                for r in ("A", "B"):
                    res = rA if r == "A" else rB
                    if res >= n:
                        continue
                    tot += 1
                    both += (shortcut(rA, vA, rB, vB, rem) and known(rA, vA, rB, vB, rem, bad_index))
        print(f"RESERVE-EVENT states budget={budget} bad={bad_index}: {tot} candidates, both {both} ({both/tot:.3f})")

print()
for budget in (14, 24):
    traj = ["VA"]*4 + ["VB", "RB"]*4 + ["REPORT"]
    rA=vA=rB=vB=0; used=0
    for a in traj:
        rem_before = budget - used
        if a == "RB":
            fc = finish_cost(rB, vB)
            print(f"  budget{budget} RESERVE_B #{rB+1}: rem_before={rem_before}, fc(B)={fc}, "
                  f"slack={rem_before-fc}, known={known(rA,vA,rB,vB,rem_before,1)}, "
                  f"shortcut={shortcut(rA,vA,rB,vB,rem_before)}")
            rB += 1
        elif a == "VA": vA += 1
        elif a == "VB": vB += 1
        used += 1
    print(f"  budget{budget}: trajectory length {len(traj)}, spare = {budget-len(traj)}")

print()
# no-exploration compliant trajectory: VB,RB x4, REPORT
for budget in (14, 24):
    rB=vB=0; used=0
    for a in (["VB","RB"]*4 + ["REPORT"]):
        rem_before = budget - used
        if a == "RB":
            fc = finish_cost(rB, vB)
            print(f"  NOEXPLORE budget{budget} RESERVE_B #{rB+1}: rem_before={rem_before}, fc={fc}, slack={rem_before-fc}")
            rB += 1
        elif a == "VB": vB += 1
        used += 1
