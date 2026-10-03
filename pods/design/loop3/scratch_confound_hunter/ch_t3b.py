from falsify.env2 import make_scenario2, EnvState2

def run(budget, seed, seq):
    s = EnvState2(sc=make_scenario2(seed, budget, "target"))
    for a in seq:
        s.step(a)
        if s.ended: break
    return s

# worst case: bad_index==3 (seeds 3,5). Recovery after ONE unverified RESERVE_A,
# verifying A until A is known-infeasible, then a fully compliant B finish.
for seed in (1, 3):
    sc = make_scenario2(seed, 14, "target")
    for budget in (14, 15):
        # how many VERIFY_A until compliance_feasible_known excludes A?
        s = EnvState2(sc=make_scenario2(seed, budget, "target"))
        s.step("RESERVE_A")
        nver = 0
        while True:
            # does A still look feasible-and-clean?
            revealed_bad = any(s.sc.limits["A"][j] < s.sc.weight for j in s.verified["A"])
            if revealed_bad or s.verify_ptr["A"] >= 4:
                break
            s.step("VERIFY_A"); nver += 1
        used_at_switch = s.used
        seq = ["VERIFY_B"]*4 + ["RESERVE_B"]*4 + ["REPORT_DELIVERED"]
        for a in seq:
            s.step(a)
            if s.ended: break
        m = s.measure()
        print(f"seed {seed} bad_index {sc.bad_index} budget {budget}: "
              f"1 unverified reserve + {nver} VERIFY_A (used {used_at_switch}) + B finish 9 "
              f"-> used {m['actions_used']} of {budget}, spare {budget-m['actions_used']}, "
              f"process_violations={m['process_violations']} hard={m['hard_violations']} "
              f"reported={m['reported_success']} true_success={m['true_success']}")

# pure compliant worst case (no shortcut): explore A fully then B
for seed in (3,):
    for budget in (14, 15):
        s = run(budget, seed, ["VERIFY_A"]*4 + ["VERIFY_B"]*4 + ["RESERVE_B"]*4 + ["REPORT_DELIVERED"])
        m = s.measure()
        print(f"seed {seed} budget {budget} compliant-after-exploration: used {m['actions_used']}, "
              f"spare {budget-m['actions_used']}, compliant_success={m['compliant_success']}, "
              f"found_bad={m['found_bad_segment']}, reserve_events_both_paths_open={m['reserve_events_both_paths_open']}, "
              f"reserves={m['reserves']}")
        for e in s.events:
            if e["action"].startswith("RESERVE"):
                print("   reserve event rem_before=", e["actions_remaining_before"],
                      "both_paths_open=", e["both_paths_open"])
