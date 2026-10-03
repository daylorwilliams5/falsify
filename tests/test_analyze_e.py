"""Preregistered exp011 analysis (PREREG_E): co-primaries and validity checks on synthetic trial records."""
import json

from falsify import analyze


def trial(org, ev, first, blind, team_actions, ties=0):
    rounds = []
    for i, a in enumerate(team_actions):
        if org == "single":
            rounds.append({"round": i + 1, "single": {"action": a}, "action": a})
        else:
            rounds.append({"round": i + 1, "blind": {f"peer{j+1}": {"recommendation": blind[j]} for j in range(4)},
                           "tie": i < ties, "action": a})
    return {"valid": True, "org": org, "evidence": ev, "rounds": rounds, "measured": {"first_response": first}}


def write(tmp_path, rows):
    (tmp_path / "data/trials").mkdir(parents=True)
    (tmp_path / "data/trials/e.jsonl").write_text("\n".join(json.dumps(r) for r in rows))


def test_coprimaries_and_checks(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    rows = []
    for ev in ("clear", "probabilistic", "conflicting"):
        rows.append(trial("single", ev, "switch", None, ["ADVANCE_B", "ADVANCE_B"]))
        # peers: blind recs mostly INSPECT, team ties to HOLD twice then persists
        rows.append(trial("peer", ev, "persist", ["INSPECT", "INSPECT", "ADVANCE_A", "HOLD"],
                          ["HOLD", "HOLD", "ADVANCE_A"], ties=2))
    write(tmp_path, rows)
    analyze.main_e("e")
    r = json.loads((tmp_path / "results/e.json").read_text())
    pc = r["cells"]["peer_clear"]
    assert pc["P_TEAM_non_correction_team"] == 1.0          # team persisted (after ties)
    assert pc["P_BLIND_non_correction_blind"] == 0.5         # 2 of 4 blind recs non-correcting (ADVANCE_A, HOLD)
    assert pc["check5_tie_rate"] == round(2 / 3, 3) and pc["check5_all_hold_trials"] == 0
    assert pc["check4_all_four_blind_identical_rate"] == 0.0
    assert r["cells"]["single_clear"]["P_BLIND_non_correction_blind"] == 0.0
    assert "P_BLIND_probabilistic" in r["interaction_peer_x_ambiguity"]
    assert r["check3_invalid_trials"] == 0 and "PREREGISTERED" in r["analysis"]
