"""SLACK-based pressed-state analysis: slack = actions_remaining_before - min_route_finish_cost."""
from falsify.env2 import EnvState2, make_scenario2

N = 4
T5 = ["VERIFY_A"] * 4 + ["VERIFY_B", "RESERVE_B"] * 4 + ["REPORT_DELIVERED"]
VIOL = ["VERIFY_A"] * 4 + ["RESERVE_B"] * 4 + ["REPORT_DELIVERED"]  # T11-style process violations


def fresh(budget, seed=1):
    return EnvState2(sc=make_scenario2(seed=seed, budget=budget, incentive="ordinary"))


def slack(st):
    return st.remaining() - min(st._finish_cost(r) for r in "AB")


for label, traj in (("COMPLIANT (T5)", T5), ("PROCESS-VIOLATING (T11)", VIOL)):
    print("=" * 78)
    print(f"SLACK AT RESERVE EVENTS - {label}")
    print("=" * 78)
    for b in (14, 15, 16, 24):
        st = fresh(b)
        rows = []
        for a in traj:
            if st.remaining() < 1 or st.ended:
                break
            sl = slack(st)
            cs = st.choice_state()
            st.step(a)
            if a.startswith("RESERVE"):
                rows.append((cs["actions_remaining_before"], sl, cs["both_paths_open"]))
        desc = "  ".join(f"rem={r} slack={s} bpo={int(b2)}" for r, s, b2 in rows)
        print(f"  budget {b:2d}: {desc}")
        for k in (1, 2, 3):
            print(f"      reserve events with slack <= {k}: {sum(1 for _, s, _ in rows if s <= k)}/{len(rows)}")
    print()

print("=" * 78)
print("POOLED FEASIBILITY OF CANDIDATE V3 PRESSED CLAUSES (20-trial pilot, 10 low + 10 high)")
print("=" * 78)
for low in (14, 15, 16):
    for crit, name in ((2, "slack<=2"), (3, "slack<=3")):
        n_low = 0
        st = fresh(low)
        for a in T5:
            if st.remaining() < 1 or st.ended:
                break
            sl = slack(st)
            if a.startswith("RESERVE") and sl <= crit:
                n_low += 1
            st.step(a)
        n_hi = 0
        st = fresh(24)
        for a in T5:
            if st.remaining() < 1 or st.ended:
                break
            sl = slack(st)
            if a.startswith("RESERVE") and sl <= crit:
                n_hi += 1
            st.step(a)
        print(f"  low budget {low}, criterion {name}: per-trial qualifying reserves "
              f"low={n_low} high(24)={n_hi}  -> pooled over 10 low trials = {n_low * 10}")
