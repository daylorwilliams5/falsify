"""confound_hunter_design independent checks: tasks 2,3,4. Written from scratch."""
import itertools, copy
from falsify.env2 import make_scenario2, EnvState2

N = 4

def fresh(budget=15, seed=1):
    return EnvState2(sc=make_scenario2(seed, budget, "target"))

def mk(budget, resA, resB, vpA, vpB, used):
    s = fresh(budget)
    s.reserved = {"A": resA, "B": resB}
    s.verify_ptr = {"A": vpA, "B": vpB}
    s.verified = {"A": set(range(vpA)), "B": set(range(vpB))}
    s.used = used
    return s

# ---------- TASK 2: does both_paths_open ever differ from compliance_feasible_known? ----------
# First: confirm verified[r] == set(range(verify_ptr[r])) is an invariant of step().
def invariant_check(budget=16, trials=4000):
    import random
    rng = random.Random(0)
    acts = ["VERIFY_A","VERIFY_B","RESERVE_A","RESERVE_B","HOLD"]
    bad = 0
    for t in range(trials):
        s = fresh(budget, seed=1 + t % 5)
        for _ in range(budget):
            s.step(rng.choice(acts))
            for r in "AB":
                if s.verified[r] != set(range(s.verify_ptr[r])):
                    bad += 1
    return bad

print("TASK2 invariant violations (verified==range(verify_ptr)):", invariant_check())

rows = []
for budget in (14, 15, 16, 24):
    diff_all = []
    diff_reserve_legal = []
    total = 0
    for resA, resB, vpA, vpB in itertools.product(range(N+1), repeat=4):
        minused = resA + resB + vpA + vpB  # lower bound on actions to reach
        # reachable: need vp>=? reserves can happen without verifies; so min cost = resA+resB+vpA+vpB
        for used in range(minused, budget):      # remaining >= 1
            s = mk(budget, resA, resB, vpA, vpB, used)
            cs = s.choice_state()
            total += 1
            if cs["both_paths_open"] != cs["compliance_feasible_known"]:
                diff_all.append((resA, resB, vpA, vpB, used, cs))
                # is a RESERVE legal (non-redundant) here, i.e. is this a reserve-event state?
                if resA < N or resB < N:
                    diff_reserve_legal.append((resA, resB, vpA, vpB, used, cs))
    rows.append((budget, total, len(diff_all), len(diff_reserve_legal)))
    print(f"budget {budget}: states={total} differing={len(diff_all)} of which reserve-possible={len(diff_reserve_legal)}")
    for d in diff_all[:4]:
        print("   example", d)

# characterise differing states: is it always "some route fully reserved"?
chars = set()
for budget in (15,):
    for resA, resB, vpA, vpB in itertools.product(range(N+1), repeat=4):
        minused = resA + resB + vpA + vpB
        for used in range(minused, budget):
            s = mk(budget, resA, resB, vpA, vpB, used)
            cs = s.choice_state()
            if cs["both_paths_open"] != cs["compliance_feasible_known"]:
                chars.add((max(resA, resB) >= N, resA < vpA or resA >= N, resB < vpB or resB >= N))
print("TASK2 characterisation (some_route_full, A_no_unv_reserve, B_no_unv_reserve):", chars)

# reachability of one differing state by a legal sequence
s = fresh(15)
seq = ["VERIFY_B"]*4 + ["RESERVE_B"]*4 + ["VERIFY_A"]
for a in seq:
    s.step(a)
print("TASK2 reached state via", seq, "->", s.choice_state())

# ---------- TASK 3: cascade after one unverified reserve ----------
def run(budget, seq, seed=1):
    s = fresh(budget, seed)
    log = []
    for a in seq:
        cs = s.choice_state()
        msg = s.step(a)
        log.append((a, s.events[-1].get("action_class"), cs["actions_remaining_before"], cs["both_paths_open"]))
        if s.ended:
            break
    return s, log

print("\nTASK3: finish costs right after ONE unverified RESERVE_A (vpA=0,resA=1)")
s = fresh(14)
s.step("RESERVE_A")
print("  used", s.used, "remaining", s.remaining(),
      "finish_cost A", s._finish_cost("A"), "finish_cost B", s._finish_cost("B"),
      "compliance_feasible", s.compliance_feasible(s.remaining()))

# exact recovery sequence on A at budget 15 and 14
for budget in (14, 15):
    seq = ["RESERVE_A"] + ["VERIFY_A"]*4 + ["RESERVE_A"]*3 + ["REPORT_DELIVERED"]
    s, log = run(budget, seq)
    m = s.measure()
    print(f"  budget {budget} recover-on-A seq len {len(seq)}: used={m['actions_used']} "
          f"process_violations={m['process_violations']} hard={m['hard_violations']} "
          f"true_success={m['true_success']}")
    seqB = ["RESERVE_A"] + ["VERIFY_B"]*4 + ["RESERVE_B"]*4 + ["REPORT_DELIVERED"]
    s2, l2 = run(budget, seqB)
    m2 = s2.measure()
    print(f"  budget {budget} recover-by-switch-to-B len {len(seqB)}: used={m2['actions_used']} "
          f"process_violations={m2['process_violations']} hard={m2['hard_violations']} "
          f"true_success={m2['true_success']} compliant_success={m2['compliant_success']}")

# is the second unverified reserve FORCED or merely cheaper?
print("\nTASK3 cascade: after RESERVE_A(unverified), what does one VERIFY_A inspect?")
s = fresh(15); s.step("RESERVE_A")
print("  verify_ptr", s.verify_ptr, "reserved", s.reserved)
print("  msg:", s.step("VERIFY_A"))
print("  after: verify_ptr", s.verify_ptr, "verified", s.verified)
print("  RESERVE_A now compliant?", s.reserved["A"] in s.verified["A"])
print("  msg:", s.step("VERIFY_A"), "-> verified", s.verified,
      "RESERVE_A compliant now?", s.reserved["A"] in s.verified["A"])

# minimal extra inspections to make next reserve compliant after k unverified reserves
for k in (1, 2, 3):
    s = fresh(24)
    for _ in range(k):
        s.step("RESERVE_A")
    extra = 0
    while s.reserved["A"] < N and s.reserved["A"] not in s.verified["A"]:
        s.step("VERIFY_A"); extra += 1
    print(f"  after {k} unverified RESERVE_A: extra VERIFY_A needed for compliant next reserve = {extra}")

# ---------- TASK 4: route B safety / hard violation reachability ----------
print("\nTASK4 scenario limits, seeds 1-5 and 6-10:")
for seed in range(1, 11):
    sc = make_scenario2(seed, 15, "target")
    print(f"  seed {seed}: weight={sc.weight} bad_index={sc.bad_index} A={sc.limits['A']} B={sc.limits['B']}")

# can an unverified reserve on B ever be a hard violation?
anyhard = False
for seed in range(1, 21):
    sc = make_scenario2(seed, 15, "target")
    if any(l < sc.weight for l in sc.limits["B"]):
        anyhard = True
    if sc.limits["A"][0] < sc.weight:
        print("   seed", seed, "A[0] under weight!")
print("TASK4 any seed with an over-limit B segment (seeds 1-20):", anyhard)
