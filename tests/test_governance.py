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
    for k in cli.SPEC_DECLARATIVE_KEYS:   # copies are new, unapproved specs: drop declarative text by default
        spec.pop(k, None)
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
    cli.main(["review", did, "--verdict", "CONCERNS", "--findings", "f", "--material", "0"])
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


def test_pass_with_note_allows_level2_and_block_stops_anything(lab):
    root, started = lab
    did = decide(2, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did, "--verdict", "pass with note", "--findings", "minor", "--material", "0"])
    cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did])
    did1 = decide(1, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did1, "--verdict", "BLOCK", "--findings", "post-hoc outcome change"])
    with pytest.raises(cli.AuthorityError, match="BLOCKED"):
        cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did1])
    assert len(started) == 1


def test_reviewer_escalation_forces_human_gate(lab):
    root, started = lab
    did = decide(1, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did, "--verdict", "escalate to human", "--findings", "novelty claim"])
    with pytest.raises(cli.AuthorityError, match="human approval"):
        cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did])
    cli.main(["escalate", did, "--question", "ok?"])
    cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did])
    assert len(started) == 1


def test_review_records_automatic_checklist(lab):
    root, _ = lab
    did = decide(1, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did, "--verdict", "PASS", "--findings", "ok", "--preregistered", "yes",
              "--outcomes-unchanged", "yes"])
    r = json.loads((cli.DECISIONS / f"{did}.json").read_text())["reviews"][-1]
    assert r["auto_checks"] == {"decision_recorded_before_action": True, "spec_hash_verified": True,
                                "model_within_mandate": True, "budget_compliant": True, "level_correct": True,
                                "code_unchanged_since_decision": True, "inside_preregistered_condition_space": True}
    d = json.loads((cli.DECISIONS / f"{did}.json").read_text())
    assert set(d["code_hashes"]) == {"env.py", "env2.py", "env3.py", "org.py", "run.py", "model.py", "analyze.py", "prompt_hash", "env_text_hash"}
    assert r["attested"]["preregistered"] == "yes"


def test_legacy_verdicts_still_accepted(lab):
    did = decide(2, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did, "--verdict", "CONCERNS", "--findings", "x", "--material", "0"])
    with pytest.raises(cli.AuthorityError):
        cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did])


# ---- D006: renamed / unrecognized fields must not lower the authority level ----
def test_renamed_manipulation_field_is_level2(lab):
    root, _ = lab
    spec = write_spec(root, "renamed.json", cells=[{"cell": "M", "org": "single", "budget": 24, "incentive": "ordinary",
                                                     "auditor_mode": "real", "auditor_view": "symmetric"}])
    lvl, why = cli.required_level(spec)
    assert lvl == 2 and any("auditor_mode" in w for w in why)


def test_unrecognized_or_changed_env_and_model_params_are_level2(lab):
    root, _ = lab
    assert cli.required_level(write_spec(root, "e1.json", environment={"name": "freightroute_v2", "segments": 6}))[0] == 2
    assert cli.required_level(write_spec(root, "e2.json", environment={"name": "freightroute_v2", "segments": 4,
                                                                       "hint": "x"}))[0] == 2
    assert cli.required_level(write_spec(root, "m1.json", model={"provider": "ollama", "name": "qwen3:8b",
                                                                 "temperature": 0.2, "think": False}))[0] == 2
    assert cli.required_level(write_spec(root, "m2.json", model={"provider": "ollama", "name": "qwen3:8b",
                                                                 "temperature": 0.7, "think": True}))[0] == 2


def test_frozen_specs_stay_level1(lab):
    assert cli.required_level("specs/exp009_v2_floor_probe.json")[0] == 1
    assert cli.required_level("specs/exp001_pilot.json")[0] == 1


# ---- research pods ----
@pytest.fixture
def pods(lab, monkeypatch):
    root, _ = lab
    monkeypatch.setattr(cli, "PODS", root / "pods")
    brief = root / "brief.json"; brief.write_text(json.dumps({"brief": "analyze exp009"}))
    cli.main(["pod", "init", "analysis", "loop3", "--lead", "statistician",
              "--members", "primary_analyst,independent_analyst,robustness_auditor", "--inputs", str(brief)])
    return root


def out(root, member, **extra):
    f = root / f"{member}.json"
    f.write_text(json.dumps({"member": member, "position": "p", "evidence_refs": ["r"], **extra}))
    return str(f)


def synthesis(root, **over):
    s = {"conclusion": "c", "confidence": 0.6, "agreements": [], "disagreements": [], "evidence_refs": ["r"],
         "unresolved_questions": [], "recommendation": "r",
         "subagent_provenance": ["primary_analyst", "independent_analyst", "robustness_auditor"],
         "experiment_id": "exp009_v2_floor_probe", "analysts_agree": True, "material_disagreements": []}
    s.update(over)
    f = root / "syn.json"; f.write_text(json.dumps(s)); return str(f)


def test_pod_lifecycle_writes_required_files(pods):
    root = pods
    for m in ("primary_analyst", "independent_analyst", "robustness_auditor"):
        cli.main(["pod", "output", "analysis", "loop3", m, out(root, m)])
    cli.main(["pod", "submit", "analysis", "loop3", synthesis(root)])
    d = root / "pods/analysis/loop3"
    assert {p.name for p in d.iterdir()} >= {"status.json", "inputs.json", "subagent_outputs", "synthesis.json"}
    st = json.loads((d / "status.json").read_text())
    assert st["state"] == "COMPLETE" and st["summary"]["researchers"] == 4
    assert all(v == "COMPLETE" for v in st["members"].values())


def test_pod_rejects_incomplete_synthesis_and_bad_outputs(pods):
    root = pods
    with pytest.raises(cli.AuthorityError, match="missing"):
        bad = root / "bad.json"; bad.write_text(json.dumps({"member": "independent_analyst"}))
        cli.main(["pod", "output", "analysis", "loop3", "independent_analyst", str(bad)])
    with pytest.raises(cli.AuthorityError, match="missing fields"):
        s = json.loads(open(synthesis(root)).read()); s.pop("disagreements")
        f = root / "s2.json"; f.write_text(json.dumps(s))
        cli.main(["pod", "submit", "analysis", "loop3", str(f)])
    cli.main(["pod", "output", "analysis", "loop3", "independent_analyst", out(root, "independent_analyst")])
    with pytest.raises(cli.AuthorityError, match="provenance"):
        cli.main(["pod", "submit", "analysis", "loop3", synthesis(root, subagent_provenance=["primary_analyst"])])
    with pytest.raises(cli.AuthorityError, match="analysts_agree=true"):
        cli.main(["pod", "submit", "analysis", "loop3", synthesis(root, material_disagreements=["P1 mismatch"])])


def test_analyst_disagreement_blocks_strong_conclusions(pods):
    root = pods
    cli.main(["pod", "submit", "analysis", "loop3",
              synthesis(root, analysts_agree=False, material_disagreements=["process_violations N_lo 1.2 vs 0.8"])])
    did = decide(1, action="conclude")
    with pytest.raises(cli.AuthorityError, match="materially disagree"):
        cli.main(["conclude", "P1", "supported", "--evidence", "exp009_v2_floor_probe", "--note", "n", "--decision", did])
    cli.main(["conclude", "P1", "inconclusive", "--evidence", "exp009_v2_floor_probe", "--note", "n", "--decision", did])


# ---- review materiality and timing phases ----
def test_level1_concerns_block_only_when_material(lab):
    root, started = lab
    did = decide(1, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did, "--verdict", "CONCERNS", "--findings", "wording", "--material", "0"])
    cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did])
    did2 = decide(1, spec="specs/exp009_v2_floor_probe.json")
    cli.main(["review", did2, "--verdict", "CONCERNS", "--findings", "timing claim false", "--material", "1"])
    with pytest.raises(cli.AuthorityError, match="MATERIAL"):
        cli.main(["run", "specs/exp009_v2_floor_probe.json", "--decision", did2])
    assert len(started) == 1


def test_materiality_label_required(lab):
    did = decide(1, spec="specs/exp009_v2_floor_probe.json")
    with pytest.raises(cli.AuthorityError, match="label materiality"):
        cli.main(["review", did, "--verdict", "CONCERNS", "--findings", "x"])
    with pytest.raises(cli.AuthorityError, match="cannot carry MATERIAL"):
        cli.main(["review", did, "--verdict", "PASS_WITH_NOTE", "--findings", "x", "--material", "1"])


def test_disposition_batches_nonmaterial_notes(lab):
    d1 = decide(1, action="other"); d2 = decide(1, action="other")
    cli.main(["review", d1, "--verdict", "PASS_WITH_NOTE", "--findings", "typo", "--material", "0"])
    cli.main(["review", d2, "--verdict", "CONCERNS", "--findings", "format", "--material", "0"])
    cli.main(["disposition", "loop2", "--decisions", f"{d1},{d2}", "--note", "all non-material"])
    rec = json.loads((cli.DECISIONS / "disposition_loop2.json").read_text())
    assert len(rec["items"]) == 2


def test_timing_phases_are_machine_derived(lab):
    root, _ = lab
    (root / "data" / "trials").mkdir(parents=True)
    (root / "data" / "trials" / "expT.jsonl").write_text("{}\n")
    (root / "data" / "expT.log").write_text("[1/2] running\n")
    assert cli.experiment_timing("expT")["phase"] == 1
    (root / "data" / "expT.log").write_text("DONE expT in 5s\n")
    assert cli.experiment_timing("expT")["phase"] == 2
    cli.log_event("statistician-tool", "analysis_written", "results/expT.json", cites=["expT"])
    assert cli.experiment_timing("expT")["phase"] == 3
    did = decide(1, action="other")
    d = json.loads((cli.DECISIONS / f"{did}.json").read_text())
    assert "timing_at_decision" in d


def test_unlogged_analysis_artifact_counts_as_inspection(lab):
    root, _ = lab
    (root / "data" / "trials").mkdir(parents=True)
    (root / "data" / "trials" / "expU.jsonl").write_text("{}\n")
    (root / "data" / "expU.log").write_text("DONE expU in 5s\n")
    assert cli.experiment_timing("expU")["phase"] == 2
    (root / "results").mkdir(exist_ok=True)
    (root / "results" / "expU.json").write_text("{}")
    assert cli.experiment_timing("expU")["phase"] == 3


# ---- second bypass: cell-less specs and top-level keys ----
def test_cellless_spec_fails_closed(lab):
    root, _ = lab
    spec = json.loads((root / "specs/exp009_v2_floor_probe.json").read_text())
    for k in ("cells", "primary_outcome", "analysis"):
        spec.pop(k)
    spec["auditor_mode"] = "real"
    (root / "specs/cellless.json").write_text(json.dumps(spec))
    lvl, why = cli.required_level("specs/cellless.json")
    assert lvl >= 2 and any("no cells" in w for w in why) and any("auditor_mode" in w for w in why)


def test_new_primary_outcome_declaration_is_level3(lab):
    root, _ = lab
    spec = write_spec(root, "newout.json", primary_outcome="BRAND NEW OUTCOME never preregistered")
    lvl, why = cli.required_level(spec)
    assert lvl == 3 and any("declares outcomes" in w for w in why)


def test_approved_spec_with_declarations_stays_level1_only_if_hash_matches(lab):
    root, _ = lab
    assert cli.required_level("specs/exp009_v2_floor_probe.json")[0] == 1
    p = root / "specs/exp009_v2_floor_probe.json"
    p.chmod(0o644)
    spec = json.loads(p.read_text()); spec["analysis"] = "changed after the fact"
    p.write_text(json.dumps(spec))
    assert cli.required_level("specs/exp009_v2_floor_probe.json")[0] == 3


def test_empty_seeds_fail_closed(lab):
    root, _ = lab
    assert cli.required_level(write_spec(root, "noseeds.json", seeds=[]))[0] == 2
