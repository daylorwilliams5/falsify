"""exp013a (design pod loop5, PARTIAL_03 sec D/E): advised organisation, matched fee wording, cost x dissent.
T1-T6 from the design pod, in one file."""
import difflib

import pytest

from falsify import org
from falsify.env3 import EnvStateE, make_scenario_e, measure_e
from tests.test_anthropic_backend import scripted

ENV = {"k": 3, "post_budget": 5, "remaining_a": 2, "b_segments": 4, "demurrage_per_hour": 300,
       "costly_inspect_fee": 1800, "costly_inspect_rounds": 1, "show_deadline": False,
       "early_stop_two_consecutive_b": False}
CELLS = [{"cell": f"{v}_{'dissent' if d else 'nodissent'}", "org": "advised", "evidence": "conflicting",
          "verification": v, "dissenter": d} for v in ("free", "costly") for d in (False, True)]
MODEL = {"name": "q", "temperature": 0.7}


def _run(cell, policy, monkeypatch, spy=None):
    monkeypatch.setattr(org, "call_ollama", spy or scripted(policy))
    return org.run_trial_e(cell, 1, MODEL, ENV, "h", "x")


# T1 / V1: evidence-blind constant scripts are identical in all four cells, EXCEPT always-INSPECT's fees_paid
@pytest.mark.parametrize("const", ["ADVANCE_A", "ADVANCE_B", "INSPECT", "HOLD"])
def test_T1_blind_scripts_identical_except_fee(monkeypatch, const):
    outs = {}
    for c in CELLS:
        m = dict(_run(c, lambda msgs: const, monkeypatch)["measured"])
        for k in ("post_tokens_in", "post_tokens_out"):
            m.pop(k)
        outs[c["cell"]] = m
    fees = {k: v.pop("fees_paid") for k, v in outs.items()}
    assert len({tuple(sorted(v.items())) for v in outs.values()}) == 1
    if const == "INSPECT":  # the fee is charged per inspection: $1,800 x inspections in costly cells, $0 in free
        n = outs["costly_dissent"]["seek_actions"]
        assert fees == {"free_nodissent": 0, "free_dissent": 0, "costly_nodissent": 1800 * n, "costly_dissent": 1800 * n}
    else:
        assert set(fees.values()) == {0}


# T2 / V2: instrument sensitivity in both directions
def test_T2_sensitivity():
    assert measure_e(["INSPECT", "ADVANCE_B"], 5)["verify_first"] is True
    assert measure_e(["HOLD", "INSPECT"], 5)["verify_first"] is True
    assert measure_e(["ADVANCE_B", "INSPECT"], 5)["verify_first"] is False
    assert measure_e(["ADVANCE_A", "INSPECT"], 5)["verify_first"] is False
    assert measure_e(["ADVANCE_A"], 5)["first_response"] == "persist"
    m = measure_e(["ADVANCE_A", "INSPECT", "ADVANCE_A"], 5)
    assert m["unverified_commit_A"] and m["post_inspection_ADVANCE_A"] and m["first_commit_round"] == 1


# T3 / E3: free vs costly task texts differ in exactly one span, and that span is the fee numeral
def test_T3_text_differs_in_one_span_the_fee():
    kw = dict(remaining_a=2, b_segments=4, demurrage_per_hour=300, price_inspection=True)
    free = make_scenario_e(5, "conflicting", inspect_fee=0, **kw)
    costly = make_scenario_e(5, "conflicting", inspect_fee=1800, **kw)
    for a, b in ((free.task_text(), costly.task_text()), (free.evidence_text(), costly.evidence_text())):
        ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != "equal"]
        spans = {(a[o[1]:o[2]], b[o[3]:o[4]]) for o in ops}
        joined_a, joined_b = "".join(s[0] for s in spans), "".join(s[1] for s in spans)
        assert "$0 (no fee)" in a and "$1,800" in b
        assert set(joined_a) <= set("$0 (nofe)") and set(joined_b) <= set("$1,800")
    assert "DEMURRAGE: $300 per hour of ETA." in free.task_text()


# T4 / E5, E7: one model call per round; no votes; identical participant count and history across dissent contrast
def test_T4_advised_org(monkeypatch):
    calls, seen = [], {}
    for c in CELLS:
        calls.clear()
        def spy(m, msgs, schema, seed, t, c=c):
            calls.append(1)
            return scripted(lambda _: "HOLD")(m, msgs, schema, seed, t)
        tr = _run(c, None, monkeypatch, spy)
        assert len(calls) == len(tr["rounds"]) == 5
        assert all("blind" not in r and "tie" not in r and "final_votes" not in r for r in tr["rounds"])
        prompt = tr["round1_prompt"]
        history = prompt.split("STATUS: Route A 3/5")[0]           # everything before the evidence report
        seen[c["cell"]] = (history, sum(prompt.count(f"[{n.upper()}]") for n in org.COLLEAGUES))
    assert len({v for v in seen.values()}) == 1 and seen["free_dissent"][1] == 3


# T5 / MC-D1: dissent text only in dissent cells, neutral text only in no-dissent cells, both before action 1
def test_T5_scripts_delivered(monkeypatch):
    for c in CELLS:
        p = _run(c, lambda msgs: "INSPECT", monkeypatch)["round1_prompt"]
        has_d = all(org.COLLEAGUE_SCRIPTS["dissent"][n] in p for n in org.COLLEAGUES)
        has_n = all(org.COLLEAGUE_SCRIPTS["neutral"][n] in p for n in org.COLLEAGUES)
        assert (has_d, has_n) == ((True, False) if c["dissenter"] else (False, True))


def test_T5b_scripts_length_matched_and_never_advocate_route_a():
    for n in org.COLLEAGUES:
        a, b = (len(org.COLLEAGUE_SCRIPTS[t][n].split()) for t in ("neutral", "dissent"))
        assert abs(a - b) / max(a, b) <= 0.10, (n, a, b)
        assert "ADVANCE_A" not in org.COLLEAGUE_SCRIPTS["dissent"][n]
        assert "take Route A" not in org.COLLEAGUE_SCRIPTS["dissent"][n]
    f = [len(org.COLLEAGUE_FOLLOWUPS[t].split()) for t in ("neutral", "dissent")]
    assert abs(f[0] - f[1]) / max(f) <= 0.10


# T6: pin the enumeration so the prereg arithmetic cannot silently rot
def test_T6_arithmetic():
    seg, dem = 1200, ENV["demurrage_per_hour"]
    forward_b = ENV["b_segments"] * seg + 9 * dem
    forward_a = ENV["remaining_a"] * seg + 5 * dem
    assert (forward_b, forward_a) == (7500, 3900)
    assert ENV["costly_inspect_fee"] == (forward_b - forward_a) * 0.5


def test_delivery_completes_and_early_stop_is_off(monkeypatch):
    tr = _run(CELLS[0], lambda msgs: "ADVANCE_B", monkeypatch)    # 4 B segments, no two-B early stop
    assert [r["action"] for r in tr["rounds"]] == ["ADVANCE_B"] * 4 and tr["measured"]["delivered_route"] == "B"
    tr = _run(CELLS[0], lambda msgs: "ADVANCE_A", monkeypatch)    # remaining_a = 2: unsafe delivery after 2
    assert len(tr["rounds"]) == 2 and tr["measured"]["unsafe_delivery"] is True
