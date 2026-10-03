"""Anthropic backend: spend ledger, hard cap, schema strictness, provider dispatch (fake client; no API calls)."""
import json
import types

import pytest

from falsify import model, org


class FakeClient:
    def __init__(self, text='{"rationale": "r", "action": "ADVANCE_B"}', stop="end_turn"):
        self.calls, self.text, self.stop = [], text, stop
        self.messages = types.SimpleNamespace(create=self.create)

    def create(self, **kw):
        self.calls.append(kw)
        usage = types.SimpleNamespace(input_tokens=1000, output_tokens=100, cache_creation_input_tokens=0,
                                      cache_read_input_tokens=0)
        return types.SimpleNamespace(content=[types.SimpleNamespace(type="text", text=self.text)], usage=usage,
                                     stop_reason=self.stop)


@pytest.fixture
def fake(tmp_path, monkeypatch):
    monkeypatch.setattr(model, "SPEND_LEDGER", tmp_path / "ledger.jsonl")
    c = FakeClient()
    monkeypatch.setattr(model, "_client", c)
    return c


SCHEMA = {"type": "object", "properties": {"rationale": {"type": "string"}, "action": {"type": "string"}},
          "required": ["rationale", "action"]}


def test_cost_is_logged_and_schema_is_strict(fake):
    r = model.call_anthropic("claude-haiku-4-5", [{"role": "system", "content": "S"},
                                                  {"role": "user", "content": "U"}], SCHEMA, 7, 0.7)
    assert r["output"]["action"] == "ADVANCE_B"
    assert abs(model.spent_usd() - (1000 * 1 + 100 * 5) / 1e6) < 1e-9
    kw = fake.calls[0]
    assert kw["system"] == "S" and kw["messages"] == [{"role": "user", "content": "U"}]
    assert kw["output_config"]["format"]["schema"]["additionalProperties"] is False
    assert kw["model"] == "claude-haiku-4-5" and kw["temperature"] == 0.7


def test_hard_cap_refuses_calls(fake, monkeypatch):
    monkeypatch.setenv("FALSIFY_SPEND_CAP_USD", "0.002")
    model.call_anthropic("claude-haiku-4-5", [{"role": "user", "content": "U"}], SCHEMA, 1, 0.7)  # $0.0015
    model.call_anthropic("claude-haiku-4-5", [{"role": "user", "content": "U"}], SCHEMA, 2, 0.7)  # -> $0.003
    with pytest.raises(model.BudgetExceeded):
        model.call_anthropic("claude-haiku-4-5", [{"role": "user", "content": "U"}], SCHEMA, 3, 0.7)
    assert len(fake.calls) == 2


def test_unparseable_reply_retries_then_fails(fake):
    fake.text = "not json"
    with pytest.raises(model.ParseFailure):
        model.call_anthropic("claude-haiku-4-5", [{"role": "user", "content": "U"}], SCHEMA, 1, 0.7)
    assert len(fake.calls) == 2


def test_provider_dispatch(monkeypatch):
    seen = []
    monkeypatch.setattr(org, "call_anthropic", lambda *a: seen.append("anthropic") or {"output": {}})
    monkeypatch.setattr(org, "call_ollama", lambda *a: seen.append("ollama") or {"output": {}})
    org.call_llm({"provider": "anthropic", "name": "claude-haiku-4-5", "temperature": 0.7}, [], SCHEMA, 1)
    org.call_llm({"provider": "ollama", "name": "qwen3:8b", "temperature": 0.7}, [], SCHEMA, 1)
    assert seen == ["anthropic", "ollama"]


# ---- lesson from loop 3: fixed baseline scripts must not be able to fake the effect ----
def scripted(action_for_round):
    def policy(props, messages):
        a = action_for_round(messages)
        if "recommendation" in props:
            return {"rationale": "r", "evidence_assessment": "e", "recommendation": a}
        if "vote" in props:
            return {"rationale": "r", "vote": a}
        return {"rationale": "r", "evidence_assessment": "e", "action": a}
    return lambda m, msgs, schema, seed, t: {"output": policy(schema["properties"], msgs), "tokens_in": 0,
                                             "tokens_out": 0, "retried": False}


@pytest.mark.parametrize("const", ["ADVANCE_A", "ADVANCE_B", "INSPECT", "HOLD"])
def test_evidence_blind_scripts_show_no_ambiguity_or_org_effect(monkeypatch, const):
    """A policy that ignores the evidence must produce IDENTICAL outcomes in every cell, so any measured
    org x evidence difference cannot be manufactured by a non-reading script."""
    monkeypatch.setattr(org, "call_ollama", scripted(lambda msgs: const))
    outs = set()
    for o in ("single", "peer"):
        for e in ("clear", "probabilistic", "conflicting"):
            t = org.run_trial_e({"cell": "x", "org": o, "evidence": e}, 1, {"name": "q", "temperature": 0.7},
                                {"post_budget": 3}, "h", "x")
            m = t["measured"]
            outs.add((m["first_response"], m["switched"], m["persist_actions"], m["seek_actions"]))
    assert len(outs) == 1


def test_measures_distinguish_persist_from_switch_scripts(monkeypatch):
    res = {}
    for const in ("ADVANCE_A", "ADVANCE_B"):
        monkeypatch.setattr(org, "call_ollama", scripted(lambda msgs, c=const: c))
        t = org.run_trial_e({"cell": "x", "org": "single", "evidence": "probabilistic"}, 1,
                            {"name": "q", "temperature": 0.7}, {"post_budget": 3}, "h", "x")
        res[const] = t["measured"]["first_response"]
    assert res == {"ADVANCE_A": "persist", "ADVANCE_B": "switch"}
