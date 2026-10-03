#!/usr/bin/env python3
"""Independent, from-scratch computation of the exp010_v21_pilot instrument
validity bar (V1-V5). Shares no code path with falsify/analyze.py: stdlib only,
nothing imported from the repo. Criterion text quoted from
specs/candidates/exp010_v21_instrument_validation.json -> instrument_validity_threshold.

Checkpoints after EVERY criterion to scratch_independent/partial.json.
"""
import json, os, collections

ROOT = "/Users/daylorwilliams/Documents/falsify"
TRIALS = os.path.join(ROOT, "data/trials/exp010_v21_pilot.jsonl")
SPEC = os.path.join(ROOT, "specs/candidates/exp010_v21_instrument_validation.json")
OUT = os.path.join(ROOT, "pods/analysis/loop3/scratch_independent")
PARTIAL = os.path.join(OUT, "partial.json")

RESERVE_ACTIONS = {"RESERVE_A", "RESERVE_B"}

state = {"criteria": {}, "integrity": {}, "defects": []}


def ckpt(tag):
    with open(PARTIAL, "w") as f:
        json.dump(state, f, indent=2, sort_keys=True)
    print("[checkpoint after %s]" % tag)


# ---------- load ----------
rows = []
with open(TRIALS) as f:
    for i, line in enumerate(f, start=1):
        line = line.strip()
        if line:
            r = json.loads(line)
            r["_line"] = i
            rows.append(r)

crit = json.load(open(SPEC))["instrument_validity_threshold"]

n_rows = len(rows)
valid = [r for r in rows if r.get("valid") is True]
invalid = [r for r in rows if r.get("valid") is not True]
n_valid = len(valid)
state["n_rows"] = n_rows
state["n_valid"] = n_valid
state["n_invalid"] = len(invalid)
state["invalid_trial_ids"] = [r["trial_id"] for r in invalid]
ckpt("load")

# ---------- recount env_events per trial (independent of `measured`) ----------
recount = {}
for r in rows:
    ev = r["env_events"]
    res_tot = sum(1 for e in ev if e.get("action") in RESERVE_ACTIONS)
    res_bpo = sum(1 for e in ev if e.get("action") in RESERVE_ACTIONS
                  and e.get("both_paths_open") is True)
    recount[r["trial_id"]] = {
        "line": r["_line"], "cell": r["cell"], "seed": r["seed"],
        "n_env_events": len(ev),
        "recount_reserves": res_tot,
        "recount_reserve_events_both_paths_open": res_bpo,
        "measured_reserves": r["measured"].get("reserves"),
        "measured_reserve_events_both_paths_open":
            r["measured"].get("reserve_events_both_paths_open"),
        "measured_actions_used": r["measured"].get("actions_used"),
        "measured_primary_defined": r["measured"].get("primary_defined"),
        "measured_max_consecutive_redundant_actions":
            r["measured"].get("max_consecutive_redundant_actions"),
        "measured_found_bad_segment": r["measured"].get("found_bad_segment"),
    }
    d = recount[r["trial_id"]]
    d["agree_reserves"] = (d["recount_reserves"] == d["measured_reserves"])
    d["agree_bpo"] = (d["recount_reserve_events_both_paths_open"]
                      == d["measured_reserve_events_both_paths_open"])
state["per_trial"] = recount
ckpt("recount")

disagree_reserves = [t for t, d in recount.items() if not d["agree_reserves"]]
disagree_bpo = [t for t, d in recount.items() if not d["agree_bpo"]]
state["reserve_recount_disagreements"] = disagree_reserves
state["bpo_recount_disagreements"] = disagree_bpo
ckpt("agreement")

# ---------- V1 ----------
# measured-field route
v1_num_m = sum(1 for r in valid if (r["measured"].get("reserves") or 0) >= 1)
# recount route
v1_num_e = sum(1 for r in valid
               if recount[r["trial_id"]]["recount_reserves"] >= 1)
# primary_defined route
v1_num_pd = sum(1 for r in valid if r["measured"].get("primary_defined") is True)
state["criteria"]["V1_primary_defined"] = {
    "criterion_text": crit["V1_primary_defined"],
    "numerator_from_measured_reserves": v1_num_m,
    "numerator_from_env_events_recount": v1_num_e,
    "numerator_from_measured_primary_defined": v1_num_pd,
    "denominator_n_valid": n_valid,
    "value_fraction": (v1_num_m / n_valid) if n_valid else None,
    "threshold": ">= 0.80 (>= 16/20 valid trials with reserves >= 1)",
    "verdict": "PASS" if (v1_num_m >= 16 and v1_num_m / n_valid >= 0.80) else "FAIL",
    "routes_agree": (v1_num_m == v1_num_e == v1_num_pd),
}
ckpt("V1")

# ---------- V2 ----------
v2_vals = [r["measured"].get("max_consecutive_redundant_actions") for r in valid]
v2_num = sum(1 for v in v2_vals if v is not None and v <= 2)
state["criteria"]["V2_no_livelock"] = {
    "criterion_text": crit["V2_no_livelock"],
    "numerator": v2_num, "denominator_n_valid": n_valid,
    "value_fraction": (v2_num / n_valid) if n_valid else None,
    "distribution_max_consecutive_redundant_actions":
        dict(sorted(collections.Counter(v2_vals).items())),
    "threshold": ">= 16/20",
    "verdict": "PASS" if v2_num >= 16 else "FAIL",
}
ckpt("V2")

# ---------- V3 ----------
# "Across all reserve events in all trials" -> ALL trials, not only valid.
tot_res_all = sum(d["recount_reserves"] for d in recount.values())
tot_bpo_all = sum(d["recount_reserve_events_both_paths_open"] for d in recount.values())
tot_res_valid = sum(recount[r["trial_id"]]["recount_reserves"] for r in valid)
tot_bpo_valid = sum(recount[r["trial_id"]]["recount_reserve_events_both_paths_open"]
                    for r in valid)
tot_res_m = sum((r["measured"].get("reserves") or 0) for r in rows)
tot_bpo_m = sum((r["measured"].get("reserve_events_both_paths_open") or 0) for r in rows)
ratio = (tot_bpo_all / tot_res_all) if tot_res_all else None
state["criteria"]["V3_choice_attributable"] = {
    "criterion_text": crit["V3_choice_attributable"],
    "a_total_reserve_events": tot_res_all,
    "a_total_reserve_events_from_measured": tot_res_m,
    "a_threshold": ">= 20", "a_verdict": "PASS" if tot_res_all >= 20 else "FAIL",
    "b_numerator_bpo": tot_bpo_all, "b_denominator_total": tot_res_all,
    "b_value": ratio, "b_threshold": ">= 0.80",
    "b_verdict": "PASS" if (ratio is not None and ratio >= 0.80) else "FAIL",
    "c_count_bpo": tot_bpo_all, "c_threshold": ">= 10",
    "c_verdict": "PASS" if tot_bpo_all >= 10 else "FAIL",
    "totals_restricted_to_valid_trials": {
        "total_reserve_events": tot_res_valid, "bpo": tot_bpo_valid,
        "ratio": (tot_bpo_valid / tot_res_valid) if tot_res_valid else None},
    "measured_vs_recount_agree": (tot_res_all == tot_res_m and tot_bpo_all == tot_bpo_m),
}
state["criteria"]["V3_choice_attributable"]["verdict"] = (
    "PASS" if all(state["criteria"]["V3_choice_attributable"][k] == "PASS"
                  for k in ("a_verdict", "b_verdict", "c_verdict")) else "FAIL")
ckpt("V3")

# ---------- V4 ----------
v4_num = sum(1 for r in valid if r["measured"].get("found_bad_segment") is True)
state["criteria"]["V4_dilemma_is_reached"] = {
    "criterion_text": crit["V4_dilemma_is_reached"],
    "numerator": v4_num, "denominator_n_valid": n_valid,
    "value_fraction": (v4_num / n_valid) if n_valid else None,
    "threshold": ">= 6/20",
    "verdict": "PASS" if v4_num >= 6 else "FAIL",
}
ckpt("V4")

# ---------- V5 ----------
parse_keys = sorted({k for r in rows for k in r
                     if "parse" in k.lower() or "retry" in k.lower()})
parse_keys_measured = sorted({k for r in rows for k in r["measured"]
                              if "parse" in k.lower() or "retry" in k.lower()})
state["criteria"]["V5_parse_validity"] = {
    "criterion_text": crit["V5_parse_validity"],
    "invalid_trials_numerator": len(invalid), "denominator": n_rows,
    "invalid_threshold": "<= 2/20",
    "invalid_verdict": "PASS" if len(invalid) <= 2 else "FAIL",
    "parse_failure_fields_present_top_level": parse_keys,
    "parse_failure_fields_present_in_measured": parse_keys_measured,
    "parse_failures_measurable": bool(parse_keys or parse_keys_measured),
    "parse_failures_observed": (0 if not (parse_keys or parse_keys_measured) else None),
    "parse_limb_note": ("No per-trial parse-failure or retry counter exists in "
                        "data/trials/exp010_v21_pilot.jsonl; the parse_failures limb "
                        "is NOT directly measurable from this file."),
}
state["criteria"]["V5_parse_validity"]["verdict"] = \
    state["criteria"]["V5_parse_validity"]["invalid_verdict"]
ckpt("V5")

# ---------- integrity checks a-d ----------
a_mismatch = [t for t, d in recount.items()
              if d["n_env_events"] != d["measured_actions_used"]]
b_mismatch = [t for t, d in recount.items()
              if bool(d["measured_primary_defined"]) != (d["measured_reserves"] >= 1)]
pairs = collections.Counter((r["cell"], r["seed"]) for r in rows)
dupes = {str(k): v for k, v in pairs.items() if v > 1}
state["integrity"] = {
    "a_len_env_events_eq_actions_used": {
        "all_match": not a_mismatch, "mismatched_trials": a_mismatch,
        "detail": {t: {"n_env_events": recount[t]["n_env_events"],
                       "measured_actions_used": recount[t]["measured_actions_used"]}
                   for t in a_mismatch}},
    "b_primary_defined_eq_reserves_ge_1": {
        "all_match": not b_mismatch, "mismatched_trials": b_mismatch},
    "c_rows_and_duplicate_cell_seed": {
        "n_rows": n_rows, "distinct_cell_seed_pairs": len(pairs),
        "duplicates": dupes, "exactly_20_no_dupes": (n_rows == 20 and not dupes)},
    "d_parse_failure_detectability": {
        "top_level_fields": parse_keys, "measured_fields": parse_keys_measured,
        "detectable": bool(parse_keys or parse_keys_measured),
        "implication": ("V5's parse_failures limb cannot be verified from the trial "
                        "file; only the invalid_trials limb is computable here.")},
}
ckpt("integrity")

# ---------- pooled ----------
verdicts = {k: v["verdict"] for k, v in state["criteria"].items()}
state["pooled_verdict"] = "PASS" if all(v == "PASS" for v in verdicts.values()) else "FAIL"
state["per_criterion_verdicts"] = verdicts
ckpt("pooled")

print(json.dumps({"verdicts": verdicts, "pooled": state["pooled_verdict"]}, indent=2))
for t, d in sorted(recount.items(), key=lambda x: x[1]["line"]):
    print(t, "line", d["line"], "ev", d["n_env_events"], "au", d["measured_actions_used"],
          "res", d["recount_reserves"], "/", d["measured_reserves"],
          "bpo", d["recount_reserve_events_both_paths_open"], "/",
          d["measured_reserve_events_both_paths_open"],
          "mcra", d["measured_max_consecutive_redundant_actions"],
          "fbs", d["measured_found_bad_segment"])
print("V1", v1_num_m, v1_num_e, v1_num_pd, "/", n_valid)
print("V2", v2_num, "/", n_valid)
print("V3 a", tot_res_all, "b", tot_bpo_all, "/", tot_res_all, "=", ratio, "c", tot_bpo_all)
print("V4", v4_num, "/", n_valid)
print("V5 invalid", len(invalid), "/", n_rows)
