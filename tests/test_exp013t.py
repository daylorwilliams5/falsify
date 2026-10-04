"""exp013t (human 18:4x): TIME cost channel x unanimous advisory majority, advised organisation, with F1/F3/F4/F5/C2."""
import difflib
import re

import pytest

from falsify import org
from falsify.env3 import EnvStateE, make_scenario_e
from tests.test_anthropic_backend import scripted

ENV = {"name": "freightroute_evidence", "k": 3, "post_budget": 6, "show_deadline": True, "costly_inspect_rounds": 2,
       "early_stop_two_consecutive_b": False, "signpost": False, "position_only_colleagues": True, "elicit_p": True}
CELLS = [{"cell": f"{v}_{'majority' if d else 'silent'}", "org": "advised", "evidence": "conflicting",
          "verification": v, "dissenter": d} for v in ("free", "costly") for d in (False, True)]
MODEL = {"name": "q", "temperature": 0.7}


def advised_script(action):
    def f(m, msgs, schema, seed, t):
        props = schema["properties"]
        out = {"rationale": "r", "evidence_assessment": "e", "action": action}
        if "p_route_a_legal" in props:
            out["p_route_a_legal"] = 0.5
        if "recommendation" in props:
            out = {"rationale": "r", "evidence_assessment": "e", "recommendation": action}
        return {"output": out, "tokens_in": 0, "tokens_out": 0, "retried": False}
    return f


def _run(cell, action, monkeypatch, env=ENV):
    monkeypatch.setattr(org, "call_ollama", advised_script(action))
    return org.run_trial_e(cell, 1, MODEL, env, "h", "x")


@pytest.mark.parametrize("const", ["ADVANCE_A", "ADVANCE_B", "INSPECT", "HOLD"])
def test_blind_scripts_identical_primary_in_every_cell(monkeypatch, const):
    outs = {c["cell"]: _run(c, const, monkeypatch)["measured"]["verify_first"] for c in CELLS}
    assert len(set(outs.values())) == 1


def test_F1_unknown_keys_raise(monkeypatch):
    with pytest.raises(ValueError, match="unknown"):
        _run(CELLS[0], "HOLD", monkeypatch, {**ENV, "n_scripted_colleagues": 3})
    with pytest.raises(ValueError, match="unknown"):
        _run({**CELLS[0], "dissenter_strength": 2}, "HOLD", monkeypatch)


def test_F3_p_is_elicited_before_the_action():
    props = list(org.SCHEMAS_E["advised"]["properties"])
    assert props.index("p_route_a_legal") < props.index("action")


def test_F4_position_only_scripts_matched_and_no_reasons():
    n, d = (org.POSITION_SCRIPTS[k] for k in ("neutral", "dissent"))
    assert len(n.split()) == len(d.split())
    assert "inspect" not in n.lower() and "route" not in n.lower()       # silent neutral: says nothing about it
    assert "because" not in d.lower() and "12 t" not in d and "Route A" not in d


def test_F4_F5_rendered_prompt(monkeypatch):
    hist = set()
    for c in CELLS:
        p = _run(c, "INSPECT", monkeypatch)["round1_prompt"]
        script = org.POSITION_SCRIPTS["dissent" if c["dissenter"] else "neutral"]
        other = org.POSITION_SCRIPTS["neutral" if c["dissenter"] else "dissent"]
        assert p.count(script) == 3 and other not in p
        assert "agreed, Route A" not in p and "earliest ETA" not in p.split("REPORT 1")[0].split("acknowledged")[-1]
        hist.add(p.split("REPORT 1")[0])
    assert len(hist) == 1                                                 # identical, route-neutral history


def test_C2_signpost_deleted_in_both_arms_and_texts_differ_only_in_round_count():
    f = make_scenario_e(2, "conflicting", inspect_rounds=1, show_deadline=True, signpost=False)
    c = make_scenario_e(2, "conflicting", inspect_rounds=2, show_deadline=True, signpost=False)
    assert "INSPECT" not in f.evidence_text() and f.evidence_text() == c.evidence_text()
    ops = [o for o in difflib.SequenceMatcher(None, f.task_text(), c.task_text(), autojunk=False).get_opcodes()
           if o[0] != "equal"]
    assert "".join(f.task_text()[o[1]:o[2]] for o in ops) in ("one round", "one", "on")
    assert "2 rounds" in c.task_text() and "DEADLINE" in f.task_text() and "DEADLINE" in c.task_text()


def test_time_price_is_binding_but_feasible():
    for rounds, slack in ((1, 1), (2, 0)):
        sc = make_scenario_e(1, "conflicting", inspect_rounds=rounds, show_deadline=True)
        e = EnvStateE(sc)
        e.step("INSPECT")
        for _ in range(4):
            e.step("ADVANCE_B")
        assert e.delivered() == "B" and sc.post_budget - len(e.actions) == slack


def test_exp011_exp012_specs_still_pass_the_whitelist():
    import json, pathlib
    for f in ("exp011_ambiguity_x_peer_haiku_pilot", "exp012_ambiguity_x_peer_haiku_main"):
        s = json.loads(pathlib.Path(f"specs/{f}.json").read_text())
        assert set(s["environment"]) <= org.ENV_E_KEYS and all(set(c) <= org.CELL_E_KEYS for c in s["cells"])


def test_MC_C1_cost_marker_is_in_what_the_subject_sees(monkeypatch):
    for c in CELLS:
        t = _run(c, "HOLD", monkeypatch)
        seen = t["round1_system"] + t["round1_prompt"]
        assert ("takes 2 rounds" in seen) is (c["verification"] == "costly")
        assert ("takes one round" in seen) is (c["verification"] == "free")
