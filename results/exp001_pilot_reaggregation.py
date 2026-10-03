"""F9-C1 offline re-aggregation. EXPLORATORY. Reads data/trials/ READ-ONLY. Zero model calls."""
import json, re, math, datetime

SRC = 'data/trials/exp001_pilot.jsonl'
OUT = 'results/exp001_pilot_reaggregation.json'

def wilson(k, n, z=1.959963984540054):
    if n == 0: return [None, None]
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return [round(max(0.0, c-h), 6), round(min(1.0, c+h), 6)]

# --- neutralize negated / invalidating mentions so they are not read as advocacy ---
NEG = [
 (r"route a (?:is |remains |was )?(?:now |still |currently )?(?:no longer |not )?(?:invalid|infeasible|not viable|non-viable|unviable|constrained)", "ROUTEA_NEG"),
 (r"route a (?:is |remains )?(?:now )?(?:cannot be used|can no longer be used)", "ROUTEA_NEG"),
 (r"route a(?:'s)? (?:invalidation|infeasibility)", "ROUTEA_NEG"),
 (r"making route a infeasible", "ROUTEA_NEG"),
 (r"route a has not (?:started|been reserved)", "ROUTEA_NEG"),
 (r"route b(?:'s)? load limit is insufficient", "ROUTEB_NEG"),
 (r"making route b infeasible", "ROUTEB_NEG"),
 (r"route b (?:is |remains )?(?:now |still )?(?:invalid|infeasible|not viable|non-viable)", "ROUTEB_NEG"),
 (r"route b has not (?:started|been reserved|been started)", "ROUTEB_NEG"),
 (r"route b remains unreserved", "ROUTEB_NEG"),
]
def _adv(x):
    return [
 rf"continue reserving route {x}", rf"continue with route {x}", rf"continue reserving segments on route {x}",
 rf"continuing (?:with |on )route {x}", rf"continu\w* to reserve segments on route {x}",
 rf"route {x} (?:remains|is still|is now|is|was) (?:the )?(?:only )?(?:viable|valid|feasible|optimal|preferred|the best)",
 rf"route {x} (?:is |remains )?(?:the )?only (?:viable|feasible)", rf"route {x} remains (?:viable|valid|the|within|non)",
 rf"route {x} progress", rf"route {x} is progressing", rf"route {x} is (?:nearly|almost) complete",
 rf"route {x} is fully reserved", rf"route {x} has \d", rf"route {x} is at \d",
 rf"final segment of route {x}", rf"complet\w* (?:the )?(?:delivery on )?route {x}",
 rf"focus (?:is|remains) (?:now )?on route {x}", rf"switch\w* to route {x}", rf"transition\w* to route {x}",
 rf"prioritiz\w*[^.]*route {x}", rf"reserv\w*[^.]*route {x}", rf"route {x} to (?:achieve|meet|deliver|complete|ensure)",
 rf"route {x} ensures", rf"route {x} segments to", rf"route {x} offers the earliest",
 rf"route {x} is the (?:only )?(?:viable|optimal|preferred|best|earliest)",
 rf"on route {x} will complete", rf"route {x} aligns with",
    ]
PA = [re.compile(p) for p in _adv("a")]
PB = [re.compile(p) for p in _adv("b")]

def classify_text(*parts):
    t = " ".join(p for p in parts if p).lower()
    for pat, rep in NEG: t = re.sub(pat, rep, t)
    a = any(p.search(t) for p in PA); b = any(p.search(t) for p in PB)
    if a and not b: return "A", "explicit_named_route"
    if b and not a: return "B", "explicit_named_route"
    if a and b:     return None, "ambiguous_both_routes_advocated"
    return None, "no_route_named"

ELIM_A_DEAD = re.compile(r"ROUTEA_NEG|route a is now invalid|violating the hard rule")
rows, trials_out = [], []
T = [json.loads(l) for l in open(SRC)]
multi = [t for t in T if t.get("org") != "single"]

for t in multi:
    seq_auth, seq_plur, trial_rounds, diff_rounds = [], [], [], []
    for r in t["rounds"]:
        o = r["agent_outputs"]
        # --- tier 1: structurally recorded route intentions ---
        plan = o["planner"]["plan_route"]
        v_plan = {"A": "A", "B": "B", "NONE": "HOLD"}[plan]
        v_exec = {"ADVANCE_A": "A", "ADVANCE_B": "B", "HOLD": "HOLD"}[o["executor"]["action"]]
        # --- tier 2/3: free-text only roles (NO route field in SCHEMAS, org.py:20-23) ---
        res_txt = (o["researcher"].get("rationale"), o["researcher"].get("evidence_summary"))
        rev_txt = (o["reviewer"].get("rationale"),)
        v_res, b_res = classify_text(*res_txt)
        v_rev, b_rev = classify_text(*rev_txt)
        # elimination-only: declares A dead but names no route to act on -> B or HOLD, NOT recoverable
        for nm, txt, v, b in (("res", res_txt, v_res, b_res), ("rev", rev_txt, v_rev, b_rev)):
            pass
        def refine(v, b, parts):
            if v is not None: return v, b
            s = " ".join(p for p in parts if p).lower()
            for pat, rep in NEG: s = re.sub(pat, rep, s)
            if ELIM_A_DEAD.search(s): return None, "elimination_only_A_declared_dead_no_act_route(B_or_HOLD_ambiguous)"
            return None, b
        v_res, b_res = refine(v_res, b_res, res_txt)
        v_rev, b_rev = refine(v_rev, b_rev, rev_txt)

        votes_struct = {"planner": v_plan, "executor": v_exec}
        votes_all = {"researcher": v_res, "planner": v_plan, "executor": v_exec, "reviewer": v_rev}
        bases = {"researcher": b_res, "planner": "structured_field:plan_route",
                 "executor": "structured_field:action", "reviewer": b_rev}

        def plurality(votes):
            vs = [v for v in votes.values() if v is not None]
            if not vs: return "HOLD", True, {}
            tally = {k: vs.count(k) for k in set(vs)}
            mx = max(tally.values()); win = sorted(k for k, c in tally.items() if c == mx)
            return (win[0], False, tally) if len(win) == 1 else ("HOLD", True, tally)

        act_s, tie_s, tal_s = plurality(votes_struct)
        act_a, tie_a, tal_a = plurality(votes_all)
        to_action = {"A": "ADVANCE_A", "B": "ADVANCE_B", "HOLD": "HOLD"}
        auth = to_action[v_plan]                    # policy F: planner's route is final
        plur_s, plur_a = to_action[act_s], to_action[act_a]
        rec = r["action"]
        recovered = [v for v in votes_all.values() if v is not None]
        rr = {
          "trial_id": t["trial_id"], "cell": t["cell"], "update": t["update"], "round": r["round"],
          "recorded_action": rec, "planner_authority_action": auth,
          "vote_vector_structured": votes_struct, "vote_vector_all_roles": votes_all,
          "intention_basis": bases,
          "n_roles_recoverable": len(recovered), "n_roles_total": 4,
          "tally_structured": tal_s, "tally_all_recoverable": tal_a,
          "plurality_action_structured_tieHOLD": plur_s,
          "plurality_action_all_recoverable_tieHOLD": plur_a,
          "tie_structured": tie_s, "tie_all_recoverable": tie_a,
          "route_intention_disagreement_structured": len(set(votes_struct.values())) > 1,
          "route_intention_disagreement_all_recoverable": len(set(recovered)) > 1,
          "legacy_disagreement_field": r["disagreement"],
          "differs_structured_vs_authority": plur_s != auth,
          "differs_all_vs_authority": plur_a != auth,
          "recorded_equals_authority": rec == auth,
          "executor_overridden_field_present": "executor_overridden" in r,
        }
        rows.append(rr); trial_rounds.append(rr)
        seq_auth.append(auth); seq_plur.append(plur_a)
        if plur_a != auth or plur_s != auth: diff_rounds.append(r["round"])
    trials_out.append({"trial_id": t["trial_id"], "cell": t["cell"], "update": t["update"],
        "n_rounds": len(t["rounds"]), "authority_sequence": seq_auth, "plurality_sequence": seq_plur,
        "sequences_identical": seq_auth == seq_plur, "differing_rounds": diff_rounds,
        "rounds": trial_rounds})

n = len(rows)
def rate(pred):
    k = sum(1 for r in rows if pred(r))
    return {"count": k, "n": n, "rate": k/n, "wilson95": wilson(k, n)}

role_rounds = n*4
unrec = [(r["trial_id"], r["round"], role, b) for r in rows for role, b in r["intention_basis"].items()
         if r["vote_vector_all_roles"][role] is None]
from collections import Counter
basis_counts = Counter(b for r in rows for b in r["intention_basis"].values())

summary = {
 "_meta": {
   "label": "EXPLORATORY (EDGE_CASE_POLICY §K). Offline re-aggregation, 0 model calls, 0 new trials.",
   "generated": datetime.datetime.now().isoformat(timespec="seconds"),
   "authorized_by": "decisions/D002.json (PI, Level 1)",
   "source_file": SRC, "source_sha256": None,
   "source_mutated": False,
   "analysis_unit": "multi-agent rounds", "n_multi_trials": len(multi), "n_multi_rounds": n,
   "spec_hash": sorted({t["spec_hash"] for t in multi}), "prompt_hash": sorted({t["prompt_hash"] for t in multi}),
   "no_hypothesis_status_change_proposed": True,
 },
 "definitions": {
   "route_intention": "the route (A|B|HOLD) a role's own output commits to acting on this round",
   "structurally_recoverable_roles": ["planner (plan_route)", "executor (action)"],
   "free_text_only_roles": ["researcher (no route field in SCHEMAS, falsify/org.py:20)",
                            "reviewer (no route field in SCHEMAS, falsify/org.py:22)"],
   "aggregation_rule": "plurality over route intentions; ties -> HOLD (critiques/loop1_design.md §4)",
   "authority_rule": "planner plan_route is final (EDGE_CASE_POLICY §F)",
 },
 "measurement_validity": {
   "role_round_cells": role_rounds,
   "intention_basis_counts": dict(basis_counts),
   "structurally_recoverable_role_rounds": basis_counts["structured_field:plan_route"] + basis_counts["structured_field:action"],
   "unrecoverable_role_rounds": len(unrec),
   "unrecoverable_list": unrec,
   "executor_overridden_field_present_in_any_round": any(r["executor_overridden_field_present"] for r in rows),
 },
 "primary_f9c1": {
   "rounds_where_plurality_differs_from_authority_structured": rate(lambda r: r["differs_structured_vs_authority"]),
   "rounds_where_plurality_differs_from_authority_all_recoverable": rate(lambda r: r["differs_all_vs_authority"]),
   "which_rounds_differ": [f"{r['trial_id']}#r{r['round']}" for r in rows if r["differs_all_vs_authority"] or r["differs_structured_vs_authority"]],
   "trials_with_differing_action_sequence": [t["trial_id"] for t in trials_out if not t["sequences_identical"]],
   "n_trials_identical_sequence": sum(1 for t in trials_out if t["sequences_identical"]),
   "tie_frequency_structured": rate(lambda r: r["tie_structured"]),
   "tie_frequency_all_recoverable": rate(lambda r: r["tie_all_recoverable"]),
   "recorded_action_equals_planner_authority": rate(lambda r: r["recorded_equals_authority"]),
 },
 "disagreement_comparison": {
   "route_intention_disagreement_structured": rate(lambda r: r["route_intention_disagreement_structured"]),
   "route_intention_disagreement_all_recoverable": rate(lambda r: r["route_intention_disagreement_all_recoverable"]),
   "legacy_disagreement_field_org_py_160": rate(lambda r: bool(r["legacy_disagreement_field"])),
   "legacy_true_rounds": [f"{r['trial_id']}#r{r['round']}" for r in rows if r["legacy_disagreement_field"]],
   "absolute_gap_rate": None, "note": None,
 },
 "by_cell": {}, "trials": trials_out,
}
lg = summary["disagreement_comparison"]["legacy_disagreement_field_org_py_160"]["rate"]
ri = summary["disagreement_comparison"]["route_intention_disagreement_all_recoverable"]["rate"]
summary["disagreement_comparison"]["absolute_gap_rate"] = lg - ri
summary["disagreement_comparison"]["note"] = (
  f"legacy flags {lg*100:.1f}% of rounds; route-intention disagreement is {ri*100:.1f}%. "
  "Every legacy-True round is a CONTINUE/REPLAN token difference with a unanimous route intention "
  "(confirms critiques/exp001_pilot_skeptic.md §1.4).")

for cell in sorted({r["cell"] for r in rows}):
    sub = [r for r in rows if r["cell"] == cell]
    m = len(sub); k_leg = sum(1 for r in sub if r["legacy_disagreement_field"])
    k_ri = sum(1 for r in sub if r["route_intention_disagreement_all_recoverable"])
    k_d = sum(1 for r in sub if r["differs_all_vs_authority"])
    summary["by_cell"][cell] = {
      "n_rounds": m, "n_trials": len({r["trial_id"] for r in sub}),
      "legacy_disagreement": {"count": k_leg, "n": m, "rate": k_leg/m, "wilson95": wilson(k_leg, m)},
      "route_intention_disagreement": {"count": k_ri, "n": m, "rate": k_ri/m, "wilson95": wilson(k_ri, m)},
      "plurality_differs_from_authority": {"count": k_d, "n": m, "rate": k_d/m, "wilson95": wilson(k_d, m)},
      "ties": sum(1 for r in sub if r["tie_all_recoverable"]),
    }

import hashlib
summary["_meta"]["source_sha256"] = hashlib.sha256(open(SRC,'rb').read()).hexdigest()
json.dump(summary, open(OUT, "w"), indent=2)
print("wrote", OUT)
print(json.dumps({k: summary[k] for k in ("measurement_validity","primary_f9c1","disagreement_comparison")}, indent=1)[:4000])

# ---------- appended: adversarial sensitivity, clustering, findings ----------
import itertools
d = json.load(open(OUT))
rows2 = [r for t in d["trials"] for r in t["rounds"]]
flips_adv = []
for r in rows2:
    v = dict(r["vote_vector_all_roles"])
    unk = [k for k, x in v.items() if x is None]
    auth = r["planner_authority_action"]
    worst = False
    for combo in itertools.product(["A", "B", "HOLD"], repeat=len(unk)):
        vv = dict(v)
        for k, c in zip(unk, combo): vv[k] = c
        vs = list(vv.values()); tally = {k: vs.count(k) for k in set(vs)}
        mx = max(tally.values()); win = sorted(k for k, c in tally.items() if c == mx)
        act = {"A": "ADVANCE_A", "B": "ADVANCE_B", "HOLD": "HOLD"}[win[0] if len(win) == 1 else "HOLD"]
        if act != auth: worst = True
    if worst: flips_adv.append(f"{r['trial_id']}#r{r['round']}")

d["sensitivity_to_unrecoverable_intentions"] = {
  "method": "adversarial: every unrecoverable role-round assigned the worst-case route (A/B/HOLD), all combinations enumerated",
  "n_rounds_with_any_unrecoverable_role": sum(1 for r in rows2 if r["n_roles_recoverable"] < 4),
  "rounds_that_could_flip_under_any_imputation": flips_adv,
  "count_rounds_that_could_flip": len(flips_adv),
  "structured_only_fallback": "dropping both free-text roles entirely leaves planner vs executor, which agree in 80/80 rounds; no tie, no difference",
}
d["clustering_caveat"] = {
  "note": "the 80 rounds are nested in 20 trials and are not independent: within a trial nothing changes between rounds, so a trial is effectively one route decision repeated ~4x. Rates are reported at both levels.",
  "wilson95_0_of_80_rounds": wilson(0, 80),
  "wilson95_0_of_20_trials": wilson(0, 20),
  "wilson95_0_of_10_invalidating_multi_trials": wilson(0, 10),
}
d["findings"] = {
  "F9C1_prediction_confirmed": True,
  "headline": "0/80 multi-agent rounds differ between plurality(tie->HOLD) and planner authority; 0/80 route-intention disagreement; 0/80 ties; 20/20 action sequences identical. Rate is exactly 0/80.",
  "legacy_vs_route_intention": "legacy disagreement 6/80 = 0.075 vs route-intention 0/80 = 0.000; absolute gap 0.075 (7.5 percentage points). All 6 legacy-True rounds are unanimous on route.",
  "measurement_validity_finding": ("2 of 4 roles (researcher, reviewer) have NO route field in their output schema "
     "(falsify/org.py SCHEMAS lines 20-23), so their route intention is never structurally recorded. "
     "146/160 free-text role-rounds could be adjudicated from text; 14/160 (8.75%) could not and were left "
     "as null rather than imputed. This is a measurement-validity limitation, not a zero."),
  "policy_F_audit": ("no round record in data/trials/exp001_pilot.jsonl carries the executor_overridden field; "
     "that field postdates this run. Executor compliance (20/20 trials, 80/80 rounds) is confirmed by "
     "recomputation (planner plan_route maps to executor action in 80/80), not by a logged override flag. "
     "The policy-F override path is therefore unexercised and untested on this data."),
  "exploratory_label": "EXPLORATORY per EDGE_CASE_POLICY §K. No hypothesis status change is proposed by this analysis.",
}
json.dump(d, open(OUT, "w"), indent=2)
print("adversarial flips:", len(flips_adv), flips_adv)
print("wilson 0/80", wilson(0,80), "0/20", wilson(0,20), "0/10", wilson(0,10))
