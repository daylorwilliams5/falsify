#!/usr/bin/env python3
"""Independent recompute of exp011 preregistered primary outcomes.
Stdlib only. Reads ONLY data/trials/exp011_ambiguity_x_peer_haiku_pilot.jsonl.
Does NOT import falsify.analyze and does not read results/.
Definitions: PREREG_E.md sec3 (hash 703a5c2a47e5dc38).
  Non-correcting action set = {ADVANCE_A, HOLD}; correcting = {ADVANCE_B, INSPECT}.
  P-TEAM: first DECISIVE (ADVANCE_A|ADVANCE_B) post-evidence team action is ADVANCE_A -> 1;
          else if every post-evidence action is HOLD -> 1; else 0.
  P-BLIND: first post-evidence round only; row value in {ADVANCE_A,HOLD} -> 1.
           single org -> 1 row (that trial's own action); peer org -> 4 rows (blind recs).
"""
import json, random, collections, os

PATH = "data/trials/exp011_ambiguity_x_peer_haiku_pilot.jsonl"
DECISIVE = ("ADVANCE_A", "ADVANCE_B")
NONCORR = ("ADVANCE_A", "HOLD")
CELLS = ["S_clear", "S_prob", "S_conf", "P_clear", "P_prob", "P_conf"]
AMB = {"prob": "probabilistic", "conf": "conflicting"}

rows = []
with open(PATH) as f:
    for i, line in enumerate(f, 1):
        line = line.strip()
        if line:
            r = json.loads(line)
            r["_line"] = i
            rows.append(r)

invalid = [r for r in rows if not r.get("valid")]
valid = [r for r in rows if r.get("valid")]
repl = [r for r in valid if "replaces" in r]

out = {"file": PATH, "n_records": len(rows),
       "n_invalid": len(invalid), "n_valid": len(valid), "n_with_replaces": len(repl),
       "invalid_reasons": dict(collections.Counter(r.get("invalid_reason", "") for r in invalid)),
       "invalid_have_replaces": sum(1 for r in invalid if "replaces" in r),
       "valid_without_replaces": sum(1 for r in valid if "replaces" not in r)}

# ---- verification: 5 replacements per cell, replaces maps 1:1 onto real attempt-1 ids
attempt1_ids = {r["trial_id"] for r in rows if "replaces" not in r}
repl_per_cell = collections.Counter(r["cell"] for r in repl)
replaces_vals = [r["replaces"] for r in repl]
dupes = [k for k, v in collections.Counter(replaces_vals).items() if v > 1]
unmatched = [v for v in replaces_vals if v not in attempt1_ids]
attempt1_invalid_ids = {r["trial_id"] for r in invalid}
out["verify"] = {
    "replacements_per_cell": {c: repl_per_cell.get(c, 0) for c in CELLS},
    "all_cells_exactly_5": all(repl_per_cell.get(c, 0) == 5 for c in CELLS),
    "n_distinct_replaces": len(set(replaces_vals)),
    "duplicate_replaces": dupes,
    "replaces_not_matching_an_attempt1_trial_id": unmatched,
    "every_replaces_targets_an_invalid_attempt1": all(v in attempt1_invalid_ids for v in replaces_vals),
    "attempt1_ids_not_replaced": sorted(attempt1_ids - set(replaces_vals)),
    "spec_hashes": sorted({r.get("spec_hash") for r in rows}),
    "models": sorted({r.get("model") for r in repl}),
}

# ---- per-trial outcome computation
def team_actions(t):
    return [rd.get("action") for rd in t.get("rounds", [])]

def p_team(t):
    acts = team_actions(t)
    for a in acts:
        if a in DECISIVE:
            return (1 if a == "ADVANCE_A" else 0), ("first_decisive=" + a)
    if acts and all(a == "HOLD" for a in acts):
        return 1, "all_HOLD_aggregation_pathway"
    return 0, "no_decisive_not_all_HOLD:" + ",".join(acts)

def blind_rows(t):
    """Return list of (agent_label, action) for first post-evidence round."""
    rds = t.get("rounds", [])
    if not rds:
        return []
    r1 = rds[0]
    if t["org"] == "single":
        a = (r1.get("single") or {}).get("action", r1.get("action"))
        return [("single", a)]
    b = r1.get("blind") or {}
    return [(k, v.get("recommendation")) for k, v in sorted(b.items())]

per_trial = {}
for t in repl:
    pt, why = p_team(t)
    br = blind_rows(t)
    per_trial[t["trial_id"]] = {
        "cell": t["cell"], "org": t["org"], "evidence": t["evidence"],
        "seed": t.get("seed"), "replaces": t["replaces"],
        "team_actions": team_actions(t),
        "p_team": pt, "p_team_reason": why,
        "blind_actions": [a for _, a in br],
        "blind_noncorr": [1 if a in NONCORR else 0 for _, a in br],
        "ties": [bool(rd.get("tie")) for rd in t.get("rounds", [])],
        "conformity_shifts": sum(int(rd.get("conformity_shifts") or 0) for rd in t.get("rounds", [])),
        "measured_first_decisive": t["measured"].get("first_decisive_action"),
        "measured_first_response": t["measured"].get("first_response"),
        "blind_majority_differs_from_team": t["measured"].get("blind_majority_differs_from_team"),
        "rounds_played": t["measured"].get("rounds_played"),
        "hold_actions": t["measured"].get("hold_actions"),
        "seek_actions": t["measured"].get("seek_actions"),
    }

# ---- per cell aggregation
per_cell = {}
for c in CELLS:
    ts = [v for v in per_trial.values() if v["cell"] == c]
    ts.sort(key=lambda v: v["seed"])
    n = len(ts)
    tc = sum(v["p_team"] for v in ts)
    brows = [x for v in ts for x in v["blind_noncorr"]]
    bn = len(brows)
    bc = sum(brows)
    all_hold = [v for v in ts if v["p_team_reason"] == "all_HOLD_aggregation_pathway"]
    tie_rounds = sum(sum(v["ties"]) for v in ts)
    tot_rounds = sum(len(v["ties"]) for v in ts)
    trials_with_tie = sum(1 for v in ts if any(v["ties"]))
    per_cell[c] = {
        "n_trials": n,
        "p_team_count": tc, "p_team_rate": round(tc / n, 4) if n else None,
        "p_blind_count": bc, "p_blind_agent_rows": bn,
        "p_blind_rate": round(bc / bn, 4) if bn else None,
        "team_action_first_decisive": dict(collections.Counter(v["measured_first_decisive"] for v in ts)),
        "blind_action_distribution": dict(collections.Counter(a for v in ts for a in v["blind_actions"])),
        "all_HOLD_trials": len(all_hold),
        "all_HOLD_trial_ids": [k for k, v in per_trial.items() if v["cell"] == c and v["p_team_reason"] == "all_HOLD_aggregation_pathway"],
        "tie_rounds": tie_rounds, "total_rounds": tot_rounds,
        "tie_rate_per_round": round(tie_rounds / tot_rounds, 4) if tot_rounds else None,
        "trials_with_any_tie": trials_with_tie,
        "rounds_consumed_by_ties": tie_rounds,
        "undefined_p_team": [v["p_team_reason"] for v in ts if v["p_team_reason"].startswith("no_decisive")],
        "mean_rounds_played": round(sum(v["rounds_played"] for v in ts) / n, 3) if n else None,
    }

# ---- pinned gate clauses
def cnt(c):
    return per_cell[c]["p_team_count"], per_cell[c]["n_trials"]

a_num = per_cell["S_clear"]["p_team_count"] + per_cell["P_clear"]["p_team_count"]
a_den = per_cell["S_clear"]["n_trials"] + per_cell["P_clear"]["n_trials"]
c_num = per_cell["S_clear"]["p_blind_count"] + per_cell["P_clear"]["p_blind_count"]
c_den = per_cell["S_clear"]["p_blind_agent_rows"] + per_cell["P_clear"]["p_blind_agent_rows"]

gates = {
    "a_pooled_clear_pteam_le_2_of_10": {
        "clause": "P-TEAM non_correction_team <= 2/10 pooled over S_clear + P_clear",
        "raw": f"{a_num}/{a_den}", "threshold": "<=2/10",
        "verdict": "PASS" if a_num <= 2 else "FAIL",
        "adjacent_to_threshold": a_num in (2, 3),
        "margin_trials": 2 - a_num},
    "b_each_clear_pteam_le_2_of_5": {
        "clause": "P-TEAM <= 2/5 in EACH of S_clear and P_clear separately",
        "raw": {"S_clear": "%d/%d" % cnt("S_clear"), "P_clear": "%d/%d" % cnt("P_clear")},
        "threshold": "<=2/5 each",
        "verdict": "PASS" if (cnt("S_clear")[0] <= 2 and cnt("P_clear")[0] <= 2) else "FAIL",
        "adjacent_to_threshold": cnt("S_clear")[0] in (2, 3) or cnt("P_clear")[0] in (2, 3)},
    "c_clear_pblind_le_20pct_of_25_rows": {
        "clause": "P-BLIND <= 20% of clear-cell blind rows (<=5 of 25)",
        "raw": f"{c_num}/{c_den}",
        "rate": round(c_num / c_den, 4) if c_den else None,
        "expected_rows": 25, "observed_rows": c_den,
        "row_breakdown": {"S_clear": per_cell["S_clear"]["p_blind_agent_rows"],
                          "P_clear": per_cell["P_clear"]["p_blind_agent_rows"]},
        "threshold": "<=5/25",
        "verdict": "PASS" if c_num <= 5 else "FAIL",
        "adjacent_to_threshold": c_num in (5, 6),
        "margin_rows": 5 - c_num,
        "clustering_note": "clustered by trial: S_clear 5 singleton clusters, P_clear 5 clusters of 4"},
    "d_le_2_of_30_replacements_invalid": {
        "clause": "<= 2 of the 30 REPLACEMENT records invalid",
        "raw": f"{sum(1 for r in repl if not r.get('valid'))}/{len(repl)}",
        "threshold": "<=2/30",
        "verdict": "PASS" if sum(1 for r in repl if not r.get("valid")) <= 2 else "FAIL",
        "adjacent_to_threshold": sum(1 for r in repl if not r.get("valid")) in (2, 3),
        "note": "attempt-1 records (no `replaces` field) are NOT replacement records; "
                f"{len(invalid)} attempt-1 records are invalid and excluded by design"},
}

# ---- all-HOLD aggregation pathway global answer
agg = [k for k, v in per_trial.items() if v["p_team_reason"] == "all_HOLD_aggregation_pathway"]
out["all_HOLD_aggregation_pathway"] = {
    "any": bool(agg), "trial_ids": agg, "count": len(agg),
    "interpretation": "trials scoring p_team=1 via the tie->HOLD aggregation rule rather than any member's judgement"}

# ---- peer independence, AMBIGUOUS peer cells only
peer_indep = {}
for c in ["P_prob", "P_conf"]:
    ts = [t for t in repl if t["cell"] == c]
    rounds_tot = 0
    unanimous = 0
    patt = collections.Counter()
    shifts = 0
    bmd = 0
    for t in ts:
        for rd in t.get("rounds", []):
            b = rd.get("blind")
            if not b:
                continue
            recs = [v.get("recommendation") for k, v in sorted(b.items())]
            rounds_tot += 1
            cc = sorted(collections.Counter(recs).values(), reverse=True)
            patt["-".join(map(str, cc))] += 1
            if len(set(recs)) == 1:
                unanimous += 1
            shifts += int(rd.get("conformity_shifts") or 0)
        if t["measured"].get("blind_majority_differs_from_team"):
            bmd += 1
    peer_indep[c] = {
        "n_trials": len(ts), "n_deliberation_rounds": rounds_tot,
        "rounds_all_four_identical": unanimous,
        "rate_all_four_identical": round(unanimous / rounds_tot, 4) if rounds_tot else None,
        "pattern_distribution_counts_sorted_desc": dict(patt),
        "conformity_shifts_total_agent_rounds": shifts,
        "conformity_shift_rate_per_agent_round": round(shifts / (rounds_tot * 4), 4) if rounds_tot else None,
        "blind_majority_differs_from_team_trials": bmd,
        "first_round_blind_counts_per_trial": [t["measured"].get("first_round_blind_counts") for t in ts],
    }

# ---- bootstrap interaction, resampling TRIALS
def rate_team(ts):
    return sum(v["p_team"] for v in ts) / len(ts)

def rate_blind(ts):
    rws = [x for v in ts for x in v["blind_noncorr"]]
    return sum(rws) / len(rws)

def cellts(c):
    return [v for v in per_trial.values() if v["cell"] == c]

def boot(amb_key, statfn, reps=20000, seed=12345):
    rng = random.Random(seed)
    cs = {"Sc": cellts("S_clear"), "Sa": cellts("S_" + amb_key),
          "Pc": cellts("P_clear"), "Pa": cellts("P_" + amb_key)}
    est = (statfn(cs["Pa"]) - statfn(cs["Pc"])) - (statfn(cs["Sa"]) - statfn(cs["Sc"]))
    draws = []
    for _ in range(reps):
        r = {k: [rng.choice(v) for _ in v] for k, v in cs.items()}  # resample TRIALS
        draws.append((statfn(r["Pa"]) - statfn(r["Pc"])) - (statfn(r["Sa"]) - statfn(r["Sc"])))
    draws.sort()
    lo = draws[int(0.025 * reps)]
    hi = draws[int(0.975 * reps) - 1]
    uniq = len(set(draws))
    return {"estimate": round(est, 4), "ci95": [round(lo, 4), round(hi, 4)],
            "reps": reps, "n_distinct_bootstrap_values": uniq,
            "frac_draws_equal_to_estimate": round(sum(1 for d in draws if d == est) / reps, 4),
            "component_rates": {k: round(statfn(v), 4) for k, v in cs.items()},
            "resampling_unit": "TRIAL (peer trial contributes its 4 correlated blind rows together)"}

boots = {}
for key, lab in AMB.items():
    boots[lab] = {"P_TEAM": boot(key, rate_team), "P_BLIND": boot(key, rate_blind)}

# ---- ceiling / floor
def ceilfloor():
    flags = []
    for c in CELLS:
        d = per_cell[c]
        if d["p_team_count"] == 0:
            flags.append(f"{c}: P-TEAM FLOOR 0/{d['n_trials']} (zero variance)")
        if d["p_team_count"] == d["n_trials"]:
            flags.append(f"{c}: P-TEAM CEILING {d['n_trials']}/{d['n_trials']} (zero variance)")
        if d["p_blind_count"] == 0:
            flags.append(f"{c}: P-BLIND FLOOR 0/{d['p_blind_agent_rows']} (zero variance)")
        if d["p_blind_count"] == d["p_blind_agent_rows"]:
            flags.append(f"{c}: P-BLIND CEILING {d['p_blind_agent_rows']}/{d['p_blind_agent_rows']} (zero variance)")
    return flags

out["per_cell"] = per_cell
out["gates"] = gates
out["peer_independence_ambiguous_only"] = peer_indep
out["bootstrap_interaction"] = boots
out["ceiling_floor_flags"] = ceilfloor()
out["per_trial"] = per_trial

os.makedirs("pods/analysis/loop4", exist_ok=True)
with open("pods/analysis/loop4/independent_analysis_out.json", "w") as f:
    json.dump(out, f, indent=1, sort_keys=False)
print(json.dumps({k: v for k, v in out.items() if k != "per_trial"}, indent=1))
