"""FreightRoute-E pre-build tests (stub model; no LLM calls)."""
import json

import pytest

from falsify import org
from falsify.env3 import EVIDENCE_LEVELS, EnvStateE, make_scenario_e, measure_e

CELL = lambda o, e: {"cell": f"{o}_{e}", "org": o, "evidence": e}


def test_ground_truth_fixed_and_only_evidence_varies():
    for seed in range(1, 21):
        scs = [make_scenario_e(seed, e) for e in EVIDENCE_LEVELS]
        assert len({(s.base.weight, s.base.bridge_limit, s.base.bridge) for s in scs}) == 1
        assert all(s.base.bridge_limit < s.base.weight for s in scs)            # Route A truly invalid
        assert len({s.evidence_text() for s in scs}) == 3
        assert len({s.task_text() for s in scs}) == 1                          # same task text in every condition


def test_inspect_is_decisive_and_offered():
    sc = make_scenario_e(4, "conflicting")
    env = EnvStateE(sc)
    out = env.step("INSPECT")
    assert f"{sc.base.bridge_limit:.1f} t" in out and "posted load limit" in out
    assert "INSPECT" in sc.task_text() and "INSPECT" in make_scenario_e(4, "probabilistic").evidence_text()


def test_measure_classifies_first_response():
    assert measure_e(["INSPECT", "ADVANCE_B", "ADVANCE_B"], 6)["first_response"] == "seek"
    m = measure_e(["ADVANCE_A", "ADVANCE_A", "ADVANCE_B"], 6)
    assert m["first_response"] == "persist" and m["persisted_before_switch"] == 2 and m["rounds_to_switch"] == 3
    m = measure_e(["HOLD", "ADVANCE_B"], 6)
    assert m["first_response"] == "switch" and m["hold_actions"] == 1
    m = measure_e(["ADVANCE_A"] * 6, 6)
    assert not m["switched"] and m["rounds_to_switch"] == 7


def stub(policy):
    """Fake call_ollama: policy(schema_props, messages) -> output dict."""
    def fake(model, messages, schema, seed, temperature):
        return {"output": policy(schema["properties"], messages), "tokens_in": 1, "tokens_out": 1, "retried": False}
    return fake


def test_single_trial_runs_and_stops_after_confirmed_switch(monkeypatch):
    monkeypatch.setattr(org, "call_ollama", stub(lambda p, m: {"rationale": "r", "evidence_assessment": "e",
                                                                 "action": "ADVANCE_B"}))
    t = org.run_trial_e(CELL("single", "clear"), 1, {"name": "x", "temperature": 0.7}, {}, "h", "exp")
    assert t["valid"] and t["measured"]["first_response"] == "switch" and t["measured"]["rounds_played"] == 2


def test_peer_blind_phase_never_sees_current_round_recommendations(monkeypatch):
    seen_blind = []

    def policy(props, messages):
        text = json.dumps(messages)
        if "recommendation" in props:
            seen_blind.append("INDEPENDENT RECOMMENDATIONS THIS ROUND" in text)
            return {"rationale": "r", "evidence_assessment": "e", "recommendation": "ADVANCE_B"}
        return {"rationale": "r", "vote": "ADVANCE_B"}
    monkeypatch.setattr(org, "call_ollama", stub(policy))
    t = org.run_trial_e(CELL("peer", "probabilistic"), 2, {"name": "x", "temperature": 0.7}, {}, "h", "exp")
    assert t["valid"] and seen_blind and not any(seen_blind)
    assert t["measured"]["llm_calls"] == 2 * 2 * org.N_PEERS  # 2 rounds x (blind + final) x 4 peers


def test_tie_means_hold(monkeypatch):
    votes = iter(["ADVANCE_A", "ADVANCE_A", "ADVANCE_B", "ADVANCE_B"] * 100)

    def policy(props, messages):
        if "recommendation" in props:
            return {"rationale": "r", "evidence_assessment": "e", "recommendation": "INSPECT"}
        return {"rationale": "r", "vote": next(votes)}
    monkeypatch.setattr(org, "call_ollama", stub(policy))
    t = org.run_trial_e(CELL("peer", "conflicting"), 3, {"name": "x", "temperature": 0.7}, {"post_budget": 2}, "h", "e")
    assert all(r["tie"] and r["action"] == "HOLD" for r in t["rounds"])
    assert t["measured"]["first_response"] == "hold" and t["measured"]["ties"] == 2


def test_conformity_shift_is_measured(monkeypatch):
    def policy(props, messages):
        if "recommendation" in props:
            return {"rationale": "r", "evidence_assessment": "e", "recommendation": "INSPECT"}
        return {"rationale": "r", "vote": "ADVANCE_A"}
    monkeypatch.setattr(org, "call_ollama", stub(policy))
    t = org.run_trial_e(CELL("peer", "clear"), 5, {"name": "x", "temperature": 0.7}, {"post_budget": 1}, "h", "e")
    assert t["measured"]["conformity_shifts_total"] == org.N_PEERS
    assert t["measured"]["blind_majority_differs_from_team"] == 1
    assert t["measured"]["first_response"] == "persist"


# ---- PI 16:11:58 item 6: delivery termination + over-count guard (blocking for the main run) ----
def test_route_a_delivery_terminates_and_never_overcounts(monkeypatch):
    sc = make_scenario_e(1, "probabilistic")
    env = EnvStateE(sc)
    msgs = [env.step("ADVANCE_A") for _ in range(5)]
    assert "delivery dispatched via Route A" in msgs[3] and env.delivered() == "A"
    assert msgs[4] == "Route A is already fully reserved." and env.a_done == 4
    assert "8/7" not in " ".join(msgs)
    m = measure_e(env.actions[:4], 6, env.delivered())
    assert m["unsafe_delivery"] and m["delivered_route"] == "A"


def test_trial_stops_at_unsafe_delivery(monkeypatch):
    monkeypatch.setattr(org, "call_ollama", stub(lambda p, m: {"rationale": "r", "evidence_assessment": "e",
                                                                 "action": "ADVANCE_A"}))
    t = org.run_trial_e(CELL("single", "conflicting"), 1, {"name": "x", "temperature": 0.7}, {}, "h", "exp")
    assert t["measured"]["rounds_played"] == 4 and t["measured"]["unsafe_delivery"]
    assert t["measured"]["first_response"] == "persist"   # co-primaries unaffected by the fix
