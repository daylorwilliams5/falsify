"""exp013 prebuild: verification cost x scripted dissenter. Evidence-blind scripts must not fake an effect."""
import json

import pytest

from falsify import org
from falsify.env3 import EnvStateE, make_scenario_e
from tests.test_anthropic_backend import scripted

CELLS = [{"cell": f"{v}_{d}", "org": "peer", "evidence": "conflicting", "verification": v, "dissenter": d,
          "n_real_peers": 3 if d else 4} for v in ("free", "costly") for d in (False, True)]
ENV = {"post_budget": 6, "show_deadline": True, "costly_inspect_rounds": 2, "costly_inspect_fee": 8000}
MODEL = {"name": "q", "temperature": 0.7}


def _run(cell, const, monkeypatch):
    monkeypatch.setattr(org, "call_ollama", scripted(lambda msgs: const))
    return org.run_trial_e(cell, 1, MODEL, ENV, "h", "x")


@pytest.mark.parametrize("const", ["ADVANCE_A", "ADVANCE_B", "INSPECT", "HOLD"])
def test_evidence_blind_scripts_give_identical_primary_outcomes_in_every_cell(monkeypatch, const):
    outs = {(_run(c, const, monkeypatch)["measured"]["first_response"]) for c in CELLS}
    assert len(outs) == 1


def test_dissenter_is_never_a_subject_and_only_appears_in_dissent_cells(monkeypatch):
    for c in CELLS:
        t = _run(c, "INSPECT", monkeypatch)
        r1 = t["rounds"][0]
        real = {"peer1", "peer2", "peer3"} | (set() if c["dissenter"] else {"peer4"})
        assert set(r1["blind"]) == real and set(r1["final_votes"]) == real  # P-BLIND units are real peers only
        assert (r1["dissenter_vote"] == "ADVANCE_A") is c["dissenter"]


def test_dissenter_text_reaches_real_peers_before_their_first_recommendation(monkeypatch):
    seen = []
    def spy(m, msgs, schema, seed, t):
        seen.append(" ".join(x["content"] for x in msgs))
        return scripted(lambda _: "INSPECT")(m, msgs, schema, seed, t)
    monkeypatch.setattr(org, "call_ollama", spy)
    org.run_trial_e(CELLS[1], 1, MODEL, ENV, "h", "x")                 # free + dissenter
    assert "Stay the course" in seen[0]
    seen.clear()
    org.run_trial_e(CELLS[0], 1, MODEL, ENV, "h", "x")                 # free, no dissenter
    assert all("Stay the course" not in s for s in seen)


def test_team_size_is_four_in_every_cell(monkeypatch):
    seen = []
    def spy(m, msgs, schema, seed, t):
        seen.append(msgs[0]["content"])
        return scripted(lambda _: "INSPECT")(m, msgs, schema, seed, t)
    monkeypatch.setattr(org, "call_ollama", spy)
    for c in CELLS:
        seen.clear()
        org.run_trial_e(c, 1, MODEL, ENV, "h", "x")
        assert all("of a 4-member freight operations team" in s for s in seen)


def test_costly_inspection_takes_two_rounds_and_fits_the_deadline_exactly():
    sc = make_scenario_e(1, "conflicting", inspect_rounds=2, inspect_fee=8000, show_deadline=True)
    e = EnvStateE(sc)
    assert "takes 2 rounds and costs $8,000" in sc.task_text() and "DEADLINE" in sc.task_text()
    e.step("INSPECT")
    for _ in range(4):
        e.step("ADVANCE_B")
    assert e.actions == ["INSPECT", "WAIT"] + ["ADVANCE_B"] * 4 and len(e.actions) == sc.post_budget
    assert e.delivered() == "B"


def test_defaults_keep_exp011_exp012_text_byte_identical():
    sc = make_scenario_e(7, "probabilistic")
    assert "INSPECT (commission a full inspection of the bridge; takes one round), or HOLD" in sc.task_text()
    assert "(INSPECT, one round)" in sc.evidence_text() and "DEADLINE" not in sc.task_text()


def test_dissenter_can_manufacture_a_tie_hold_without_any_real_peer_persisting(monkeypatch):
    """Documented artifact (same class as PREREG_E A1): if the three real peers split three ways
    (ADVANCE_B / INSPECT / HOLD), the dissenter's ADVANCE_A makes a 1-1-1-1 tie, so the team HOLDs and P-TEAM
    scores non-correction although NO real peer persisted. P-BLIND (real peers) is the judgement measure."""
    picks = iter(["ADVANCE_B", "INSPECT", "HOLD"] * 2 + ["INSPECT"] * 200)  # blind round, then final votes
    monkeypatch.setattr(org, "call_ollama", scripted(lambda msgs: next(picks)))
    t = org.run_trial_e(CELLS[1], 1, MODEL, ENV, "h", "x")
    r1 = t["rounds"][0]
    assert r1["final_votes"] == {"peer1": "ADVANCE_B", "peer2": "INSPECT", "peer3": "HOLD"}
    assert r1["tie"] is True and r1["action"] == "HOLD"
    assert "ADVANCE_A" not in r1["final_votes"].values()
