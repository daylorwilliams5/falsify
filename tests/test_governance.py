"""Authority levels are enforced by the CLI, not by prompts. Runs against a temp copy of the lab state."""
import json
import shutil

import pytest

from falsify import cli


@pytest.fixture
def lab(tmp_path, monkeypatch):
    for d in ("lab", "specs", "registry"):
        shutil.copytree(cli.ROOT / d, tmp_path / d, ignore=shutil.ignore_patterns("node_modules"))
    (tmp_path / "data").mkdir()
    monkeypatch.setattr(cli, "ROOT", tmp_path)
    monkeypatch.setattr(cli, "MANDATE", tmp_path / "lab" / "mandate.json")
    monkeypatch.setattr(cli, "DECISIONS", tmp_path / "decisions")
    monkeypatch.setattr(cli, "TIMELINE", tmp_path / "timeline.jsonl")
    monkeypatch.setattr(cli, "REGISTRY", tmp_path / "registry" / "hypotheses.json")
    started = []
    monkeypatch.setattr(cli.subprocess, "Popen", lambda *a, **k: started.append(a) or type("P", (), {"pid": 1})())
    return tmp_path, started


def write_spec(root, name, **over):
    spec = json.loads((root / "specs/exp009_v2_floor_probe.json").read_text())
    spec.update(over)
    p = root / "specs" / name
    p.write_text(json.dumps(spec))
    return f"specs/{name}"


def decide(level, action="run", spec=None):
    args = ["decide", "--level", str(level), "--action", action, "--decision", "x", "--reason", "y",
            "--confidence", "0.8", "--alternatives", "z"] + (["--spec", spec] if spec else [])
    cli.main(args)
    return sorted((cli.DECISIONS).glob("D*.json"))[-1].stem


def test_level1_preregistered_run_is_autonomous(lab):
    root, started = lab
    did = decide(1, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did])
    assert len(started) == 1


def test_run_without_decision_is_refused(lab):
    with pytest.raises(cli.AuthorityError):
        cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", "D999"])


def test_new_manipulation_needs_level2_and_review(lab):
    root, started = lab
    spec = write_spec(root, "new_ctrl.json", cells=[{"cell": "X", "org": "single", "budget": 14,
                                                       "incentive": "ordinary", "auditor": False}])
    with pytest.raises(cli.AuthorityError, match="requires level 2"):
        decide(1, spec=spec)
    did = decide(2, spec=spec)
    with pytest.raises(cli.AuthorityError, match="review PASS"):
        cli.main(["run", spec, "--decision", did])
    cli.main(["review", did, "--verdict", "CONCERNS", "--findings", "f"])
    with pytest.raises(cli.AuthorityError):
        cli.main(["run", spec, "--decision", did])
    cli.main(["review", did, "--verdict", "PASS", "--findings", "ok"])
    cli.main(["run", spec, "--decision", did])
    assert len(started) == 1


def test_model_change_is_level3_and_needs_human(lab):
    root, started = lab
    spec = write_spec(root, "haiku.json", model={"provider": "anthropic", "name": "claude-haiku-4-5", "temperature": 0.7})
    with pytest.raises(cli.AuthorityError, match="requires level 3"):
        decide(2, spec=spec)
    did = decide(3, spec=spec)
    cli.main(["review", did, "--verdict", "PASS", "--findings", "ok"])
    with pytest.raises(cli.AuthorityError, match="human approval"):
        cli.main(["run", spec, "--decision", did])
    cli.main(["escalate", did, "--question", "spend ~$5 on Haiku replication?"])
    cli.main(["run", spec, "--decision", did])
    assert len(started) == 1


def test_spec_edited_after_decision_is_refused(lab):
    root, _ = lab
    spec = write_spec(root, "probe_copy.json")
    did = decide(1, spec=spec)
    write_spec(root, "probe_copy.json", seeds=[1, 2, 3, 4, 5, 6])
    with pytest.raises(cli.AuthorityError, match="hash mismatch"):
        cli.main(["run", spec, "--decision", did])


def test_human_override_voids_decision(lab):
    did = decide(1, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["override", did, "--note", "stop"])
    with pytest.raises(cli.AuthorityError, match="overridden"):
        cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did])


def test_conclude_requires_conclude_decision(lab):
    run_did = decide(1, spec="specs/exp009_v2_floor_probe.json")
    with pytest.raises(cli.AuthorityError, match="authorizes 'run'"):
        cli.main(["conclude", "H2", "inconclusive", "--evidence", "e", "--note", "n", "--decision", run_did])
    did = decide(1, action="conclude")
    cli.main(["conclude", "H2", "inconclusive", "--evidence", "e", "--note", "n", "--decision", did])
    reg = json.loads(cli.REGISTRY.read_text())
    assert next(h for h in reg["hypotheses"] if h["id"] == "H2")["status"] == "inconclusive"


def test_every_decision_and_review_is_on_the_timeline(lab):
    did = decide(2, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did, "--verdict", "PASS", "--findings", "ok"])
    stages = [json.loads(l)["stage"] for l in cli.TIMELINE.read_text().splitlines()]
    assert stages == ["pi_decision", "methodology_review"]
