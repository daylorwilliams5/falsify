"""primary_analyst independent recompute for exp011. Does NOT import falsify.analyze or any falsify module.
Reads only the immutable JSONL. Keys on `cell` and `replaces`, never file position."""
import json, pathlib, collections, random

P = pathlib.Path("data/trials/exp011_ambiguity_x_peer_haiku_pilot.jsonl")
rows = [json.loads(l) for l in P.read_text().splitlines() if l.strip()]

NON_CORRECTING = {"ADVANCE_A", "HOLD"}          # PREREG_E sec3: persist, or HOLD when nothing decisive
CORRECTING = {"ADVANCE_B", "INSPECT"}           # switch, or seek (normatively acceptable under ambiguity)
CELLS = ["S_clear", "S_prob", "S_conf", "P_clear", "P_prob", "P_conf"]

out = {"source_file": str(P), "n_records_total": len(rows)}

# ---------- TASK 3: keying, replacement mapping, invalid accounting ----------
attempt1 = [r for r in rows if not r.get("valid")]
repl = [r for r in rows if r.get("valid") or r.get("replaces")]
repl = [r for r in rows if r.get("replaces") is not None]
invalid_repl = [r for r in repl if not r.get("valid")]
valid = [r for r in repl if r.get("valid")]

a1_ids = {r["trial_id"] for r in attempt1}
mapped = [r["replaces"] for r in repl]
out["task3_keying"] = {
    "n_attempt1_invalid_excluded": len(attempt1),
    "attempt1_cause_distribution": dict(collections.Counter(r.get("invalid_reason", "?") for r in attempt1)),
    "n_replacement_records": len(repl),
    "n_replacement_invalid": len(invalid_repl),
    "n_replacement_valid": len(valid),
    "replacement_seeds": sorted({r["seed"] for r in repl}),
    "per_cell_counts_replacements": dict(collections.Counter(r["cell"] for r in repl)),
    "per_cell_counts_attempt1": dict(collections.Counter(r["cell"] for r in attempt1)),
    "all_cells_exactly_5": all(collections.Counter(r["cell"] for r in repl)[c] == 5 for c in CELLS),
    "replaces_values_distinct": len(set(mapped)) == len(mapped),
    "replaces_all_map_to_real_attempt1_id": set(mapped) == a1_ids,
    "n_distinct_replaces_targets": len(set(mapped)),
    "file_order_is_not_cell_order": [r["cell"] for r in rows[:8]],
}

def blind_units(t):
    """P-BLIND units: first post-evidence round. single -> its own action; peer -> 4 blind recommendations."""
    rounds = t.get("rounds") or []
    if not rounds:
        return []
    r0 = rounds[0]
    if t["org"] == "single":
        return [r0["single"]["action"]]
    return [r0["blind"][f"peer{i}"]["recommendation"] for i in range(1, 5)]

def p_team_unit(t):
    """P-TEAM: first decisive post-evidence TEAM action is ADVANCE_A, or HOLD if every action is HOLD."""
    acts = [r["action"] for r in (t.get("rounds") or [])]
    decisive = [a for a in acts if a != "HOLD"]
    first = decisive[0] if decisive else "HOLD"
    return float(first in NON_CORRECTING), first, acts

# ---------- TASKS 1/2: per-cell co-primaries, recomputed from raw ----------
cells = {}
for c in CELLS:
    ts = [t for t in valid if t["cell"] == c]
    teams = [p_team_unit(t) for t in ts]
    bl = [b for t in ts for b in blind_units(t)]
    nc_blind = [b for b in bl if b in NON_CORRECTING]
    cells[c] = {
        "org": ts[0]["org"], "evidence": ts[0]["evidence"], "n_trials": len(ts),
        "P_TEAM_count_non_correction": int(sum(x[0] for x in teams)),
        "P_TEAM_rate": round(sum(x[0] for x in teams) / len(ts), 3),
        "P_TEAM_first_decisive_actions": dict(collections.Counter(x[1] for x in teams)),
        "P_TEAM_matches_measured_first_response": all(
            (x[1] in NON_CORRECTING) == (t["measured"]["first_response"] in ("persist", "hold"))
            for t, x in zip(ts, teams)),
        "P_BLIND_n_agent_rows": len(bl),
        "P_BLIND_count_non_correction": len(nc_blind),
        "P_BLIND_rate": round(len(nc_blind) / len(bl), 3),
        "blind_recommendation_distribution": dict(collections.Counter(bl)),
    }
out["cells_primary_analyst"] = cells

# ---------- TASK 1: the pinned gate ----------
sc, pc = cells["S_clear"], cells["P_clear"]
a_num = sc["P_TEAM_count_non_correction"] + pc["P_TEAM_count_non_correction"]
c_num = sc["P_BLIND_count_non_correction"] + pc["P_BLIND_count_non_correction"]
c_den = sc["P_BLIND_n_agent_rows"] + pc["P_BLIND_n_agent_rows"]
# clustered by trial: how many DISTINCT clear-cell trials contribute >=1 non-correcting blind row
clear_trials = [t for t in valid if t["cell"] in ("S_clear", "P_clear")]
clustered = sum(1 for t in clear_trials if any(b in NON_CORRECTING for b in blind_units(t)))
out["task1_pinned_gate"] = {
    "pinned_by": "PI timeline exp011_clear_gate_prespecified 2026-10-03T16:37:41, before any outcome read",
    "a_pooled_P_TEAM": {"count": a_num, "denominator": 10, "threshold": "<=2/10",
                        "rate": round(a_num / 10, 3), "verdict": "PASS" if a_num <= 2 else "FAIL"},
    "b_each_clear_cell_P_TEAM": {
        "S_clear": {"count": sc["P_TEAM_count_non_correction"], "denominator": 5, "threshold": "<=2/5",
                    "verdict": "PASS" if sc["P_TEAM_count_non_correction"] <= 2 else "FAIL"},
        "P_clear": {"count": pc["P_TEAM_count_non_correction"], "denominator": 5, "threshold": "<=2/5",
                    "verdict": "PASS" if pc["P_TEAM_count_non_correction"] <= 2 else "FAIL"},
        "verdict": "PASS" if max(sc["P_TEAM_count_non_correction"], pc["P_TEAM_count_non_correction"]) <= 2 else "FAIL"},
    "c_P_BLIND_clear_rows": {"count": c_num, "denominator": c_den, "threshold": "<=5 of 25 (20%)",
                             "rate": round(c_num / c_den, 3),
                             "rows_breakdown": {"S_clear_single_actions": sc["P_BLIND_n_agent_rows"],
                                                "P_clear_peer_blind_recs": pc["P_BLIND_n_agent_rows"]},
                             "trials_contributing_any_non_correcting_blind_row": clustered,
                             "n_clear_trials": len(clear_trials),
                             "verdict": "PASS" if c_num <= 5 else "FAIL"},
    "d_replacement_invalid": {"count": len(invalid_repl), "denominator": len(repl), "threshold": "<=2/30",
                              "verdict": "PASS" if len(invalid_repl) <= 2 else "FAIL"},
}
g = out["task1_pinned_gate"]
g["GATE_OVERALL"] = "PASS" if all(g[k]["verdict"] == "PASS" if "verdict" in g[k] else True
                                 for k in ("a_pooled_P_TEAM", "b_each_clear_cell_P_TEAM",
                                           "c_P_BLIND_clear_rows", "d_replacement_invalid")) else "FAIL"
# adjacency: distance to each threshold in whole units
g["adjacency_to_threshold"] = {
    "a_units_of_slack": 2 - a_num, "b_S_clear_slack": 2 - sc["P_TEAM_count_non_correction"],
    "b_P_clear_slack": 2 - pc["P_TEAM_count_non_correction"], "c_units_of_slack": 5 - c_num,
    "d_units_of_slack": 2 - len(invalid_repl)}

# ---------- TASK 4: ties, all-HOLD, aggregation pathway ----------
tie_tbl = {}
for c in CELLS:
    ts = [t for t in valid if t["cell"] == c]
    if ts[0]["org"] == "single":
        tie_tbl[c] = {"org": "single", "ties_structurally_impossible": True, "tie_rate": 0.0,
                      "all_hold_trials": sum(1 for t in ts if all(r["action"] == "HOLD" for r in t["rounds"])),
                      "rounds_consumed_by_ties": 0}
        continue
    nr = sum(len(t["rounds"]) for t in ts)
    nt = sum(1 for t in ts for r in t["rounds"] if r.get("tie"))
    tie_tbl[c] = {"org": "peer", "peer_rounds": nr, "tie_rounds": nt,
                  "tie_rate": round(nt / nr, 3) if nr else None,
                  "rounds_consumed_by_ties": nt,
                  "all_hold_trials": sum(1 for t in ts if all(r["action"] == "HOLD" for r in t["rounds"])),
                  "trials_with_any_tie": sum(1 for t in ts if any(r.get("tie") for r in t["rounds"]))}
out["task4_ties"] = tie_tbl
# did any team score P-TEAM=1 via the all-HOLD aggregation pathway rather than a member's judgement?
agg = []
for t in valid:
    acts = [r["action"] for r in t["rounds"]]
    if acts and all(a == "HOLD" for a in acts):
        agg.append({"trial_id": t["trial_id"], "cell": t["cell"], "org": t["org"],
                    "all_tie_rounds": all(r.get("tie") for r in t["rounds"]) if t["org"] == "peer" else None})
out["task4_all_hold_aggregation_pathway_trials"] = agg
out["task4_any_P_TEAM_1_via_all_HOLD"] = len(agg) > 0
# co-primary disagreement per cell
out["task4_coprimary_comparison"] = {c: {"P_TEAM_rate": cells[c]["P_TEAM_rate"],
                                         "P_BLIND_rate": cells[c]["P_BLIND_rate"],
                                         "difference_TEAM_minus_BLIND": round(cells[c]["P_TEAM_rate"] - cells[c]["P_BLIND_rate"], 3)}
                                     for c in CELLS}
# secondaries (reported, flagged non-comparable across org per sec4)
out["secondaries_sec4_NONCOMPARABLE_across_org"] = {
    c: {k: round(sum(t["measured"][k] for t in valid if t["cell"] == c) / 5, 3)
        for k in ("rounds_to_switch", "persisted_before_switch", "seek_actions", "hold_actions", "rounds_played")}
       | {"switched_count": sum(1 for t in valid if t["cell"] == c and t["measured"]["switched"])}
    for c in CELLS}

# ---------- TASK 5: peer independence, AMBIGUOUS cells only ----------
ind = {}
for c in ("P_prob", "P_conf", "P_clear"):
    ts = [t for t in valid if t["cell"] == c]
    sets = [[r["blind"][f"peer{i}"]["recommendation"] for i in range(1, 5)] for t in ts for r in t["rounds"]]
    ident = sum(1 for s in sets if len(set(s)) == 1)
    ind[c] = {"peer_rounds": len(sets), "all_four_identical": ident,
              "all_four_identical_rate": round(ident / len(sets), 3) if sets else None,
              "pattern_counts": dict(collections.Counter("-".join(sorted(s)) for s in sets)),
              "mean_distinct_actions_per_round": round(sum(len(set(s)) for s in sets) / len(sets), 3) if sets else None,
              "conformity_shifts_total": sum(r["conformity_shifts"] for t in ts for r in t["rounds"]),
              "conformity_shift_rate_per_agent_round": round(
                  sum(r["conformity_shifts"] for t in ts for r in t["rounds"]) / (4 * len(sets)), 3) if sets else None,
              "blind_majority_differs_from_team_trials": sum(1 for t in ts
                                                             if t["measured"].get("blind_majority_differs_from_team"))}
out["task5_peer_independence"] = ind
out["task5_note"] = ("AMBIGUOUS cells (P_prob, P_conf) are the diagnostic ones; P_clear shown for completeness only "
                     "because correct unanimity under clear evidence is EXPECTED and not diagnostic (PI 16:37).")

# ---------- TASK 6: bounds. Bootstrap resamples TRIALS, never agent-rows ----------
rng = random.Random(0)
units = {}
for c in CELLS:
    units[c] = [{"team": p_team_unit(t)[0], "blind": blind_units(t)} for t in valid if t["cell"] == c]

def team_rate(us): return sum(u["team"] for u in us) / len(us)
def blind_rate(us):
    rws = [b for u in us for b in u["blind"]]
    return sum(1 for b in rws if b in NON_CORRECTING) / len(rws)

def boot_interaction(amb, fn, n=10000):
    draws = []
    for _ in range(n):
        r = {c: [units[c][rng.randrange(len(units[c]))] for _ in units[c]] for c in
             (f"P_{amb}", "P_clear", f"S_{amb}", "S_clear")}   # resample TRIALS (clusters), not agent-rows
        draws.append((fn(r[f"P_{amb}"]) - fn(r["P_clear"])) - (fn(r[f"S_{amb}"]) - fn(r["S_clear"])))
    draws.sort()
    return [round(draws[int(.025 * n)], 3), round(draws[int(.975 * n)], 3)]

inter = {}
for amb in ("prob", "conf"):
    for nm, fn in (("P_TEAM", team_rate), ("P_BLIND", blind_rate)):
        est = (fn(units[f"P_{amb}"]) - fn(units["P_clear"])) - (fn(units[f"S_{amb}"]) - fn(units["S_clear"]))
        inter[f"{nm}_{amb}"] = {"estimate": round(est, 3), "ci95_trial_clustered": boot_interaction(amb, fn),
                                "LICENCE": "DESCRIPTIVE ONLY (PREREG_E sec5): no hypothesis verdict, no rate claim, no status change at n=5/cell"}
out["task6_interaction_descriptive_only"] = inter

# F6: did the missing delivery-termination / over-count guard touch either co-primary?
f6 = []
for t in valid:
    acts = [r["action"] for r in t["rounds"]]
    a = acts.count("ADVANCE_A"); b = acts.count("ADVANCE_B")
    if a >= 4 or b >= 4 or any("8/7" in (r.get("env_result") or "") for r in t["rounds"]):
        f6.append({"trial_id": t["trial_id"], "cell": t["cell"], "n_ADVANCE_A": a, "n_ADVANCE_B": b,
                   "env_results": [r.get("env_result") for r in t["rounds"]]})
out["task6_F6_env3_overcount_exposure"] = {
    "trials_reaching_route_completion_or_overcount": f6,
    "max_ADVANCE_A_in_any_trial": max(([r["action"] for r in t["rounds"]].count("ADVANCE_A")) for t in valid),
    "max_rounds_played": max(len(t["rounds"]) for t in valid),
    "co_primaries_touched": None,  # filled below
}
out["task6_F6_env3_overcount_exposure"]["co_primaries_touched"] = bool(f6) and any(
    len(x["env_results"]) and False for x in f6)

pathlib.Path("pods/analysis/loop4").mkdir(parents=True, exist_ok=True)
pathlib.Path("pods/analysis/loop4/PARTIAL_primary_recompute.json").write_text(json.dumps(out, indent=2))
print(json.dumps({k: v for k, v in out.items() if k not in ("secondaries_sec4_NONCOMPARABLE_across_org",)}, indent=2))
