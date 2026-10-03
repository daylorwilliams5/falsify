"""`falsify` CLI: the tools the Omnigent research lab uses, with authority levels enforced in code.

Science
  falsify status EXP                 progress of a running/finished experiment
  falsify analyze EXP                measured results -> results/EXP.json
  falsify hypotheses                 print the hypothesis registry
  falsify log AGENT STAGE TEXT [--cites ...]      append to timeline.jsonl

Governance (lab/mandate.json, specs/AUTHORITY.md)
  falsify level SPEC                 minimum authority level a spec requires, and why
  falsify decide --level N --action run|conclude|other --decision TEXT --reason TEXT
                 --confidence X --alternatives TEXT [--spec PATH] [--cites ...]   (PI)
  falsify review DID --verdict PASS|PASS_WITH_NOTE|BLOCK|ESCALATE --findings TEXT
                 [--preregistered yes|no|n/a] [--outcomes-unchanged ...] [--exploratory-labeled ...] [--novelty-ok ...]
  falsify budget                          research budget dashboard -> results/budget.json
  falsify timing EXP                      machine-derived timing phase (1 before completion / 2 after completion,
                                          before outcome inspection / 3 after outcome inspection)
  falsify disposition LOOP --decisions D1,D2 --note TEXT   end-of-loop batch of NON_MATERIAL review notes

Research pods (pods/<stage>/<loop>/: status.json, inputs.json, subagent_outputs/, synthesis.json)
  falsify pod init STAGE LOOP --lead NAME --members a,b --inputs FILE.json|TEXT
  falsify pod mark STAGE LOOP MEMBER PENDING|RUNNING|COMPLETE|FAILED
  falsify pod output STAGE LOOP MEMBER FILE.json   (needs member, position, evidence_refs)
  falsify pod submit STAGE LOOP SYNTHESIS.json     (validated; analysis pod also needs experiment_id,
                                                    analysts_agree, material_disagreements)
  falsify escalate DID --question TEXT    level-3 human gate (pauses in Omnigent for the human)
  falsify override DID --note TEXT        human override; voids the decision
  falsify run SPEC --decision DID         starts an experiment only if DID authorizes it
  falsify conclude HID STATUS --evidence EXP --note TEXT --decision DID
  falsify decisions                       list decision records

Every write is append-only or recorded in timeline.jsonl, so the research record is reconstructable.
"""
import argparse
import datetime
import hashlib
import json
import pathlib
import subprocess
import sys

PKG = pathlib.Path(__file__).resolve().parent  # code location (never patched)
ROOT = PKG.parent
TIMELINE = ROOT / "timeline.jsonl"
REGISTRY = ROOT / "registry" / "hypotheses.json"
MANDATE = ROOT / "lab" / "mandate.json"
DECISIONS = ROOT / "decisions"
PODS = ROOT / "pods"
POD_STAGES = {"literature", "design", "analysis", "adversarial"}
MEMBER_STATES = {"PENDING", "RUNNING", "COMPLETE", "FAILED"}
SYNTHESIS_FIELDS = ["conclusion", "confidence", "agreements", "disagreements", "evidence_refs",
                    "unresolved_questions", "recommendation", "subagent_provenance"]
SUBAGENT_FIELDS = ["member", "position", "evidence_refs"]
STATUSES = {"supported", "falsified", "inconclusive", "needs replication", "untested"}
# Reviewer verdicts. PASS / PASS_WITH_NOTE allow level-2 action; BLOCK stops it; ESCALATE forces the human gate.
# Legacy: CONCERNS (blocking, like the original design) and FAIL (= BLOCK).
VERDICTS = ["PASS", "PASS_WITH_NOTE", "BLOCK", "ESCALATE", "CONCERNS", "FAIL"]
ALLOWING = {"PASS", "PASS_WITH_NOTE"}

# Preregistered condition space per environment family (PROTOCOL.md §3/§8, PREREG_V2.md).
# A spec that stays inside it is a preregistered experiment; anything outside is a new manipulation (level 2+).
PREREG_SPACE = {
    "freightroute": {"org": {"single", "multi"}, "k": {1, 5, 10}, "update": {"invalidating", "benign"},
                     "context": {"natural"}, "provenance": {"self"}, "auditor": {False},
                     "env.salience_step": {0, 1, 2}},
    "freightroute_v2": {"org": {"single", "multi"}, "budget": {24, 10}, "incentive": {"ordinary", "target"},
                        "auditor": {False}},
}


# Allowlists (D006 fix): any field not listed here is an unrecognized manipulation -> level 2.
CELL_META_KEYS = {"cell"}
ENV_DEFAULTS = {
    "freightroute": {"name": "freightroute", "remaining_a_segments": 4, "b_segments": 4, "post_budget": 8,
                     "invalid_ratio": 1.4, "salience_step": None},  # salience_step checked via PREREG_SPACE
    "freightroute_v2": {"name": "freightroute_v2", "segments": 4},
}
MODEL_DEFAULTS = {"temperature": 0.7, "think": False}  # provider/name checked against the mandate
# Top-level spec keys (second bypass fix). Functional keys drive the runner; documentary keys are inert text.
SPEC_FUNCTIONAL_KEYS = {"experiment_id", "model", "environment", "cells", "seeds", "concurrency"}
SPEC_DOC_KEYS = {"tests", "status", "purpose", "materially_new_under_policy_L", "requires_build", "env_freeze_note",
                 "why_this_before_the_full_run", "code_verification_by_designer", "invalid_trial_budget", "cost",
                 "notes", "description"}
# Keys that DECLARE outcomes/analysis/exclusions: allowed only in a human-approved spec whose hash matches the mandate.
SPEC_DECLARATIVE_KEYS = {"primary_outcome", "primary_outcomes", "analysis", "exclusions", "outcomes"}


class AuthorityError(SystemExit):
    pass


def now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def log_event(agent: str, stage: str, text: str, cites=None, **extra) -> dict:
    ev = {"ts": now(), "agent": agent, "stage": stage, "text": text, "cites": cites or [], **extra}
    with TIMELINE.open("a") as f:
        f.write(json.dumps(ev) + "\n")
    return ev


def sha(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def code_hashes() -> dict:
    """Hashes of the frozen artifacts a run depends on (environments, organizations/prompts, runner)."""
    import inspect
    from . import env, env2
    from .org import prompt_hash
    # D006 fix: the environment-side text the subject and auditor read is hashed explicitly too.
    texts = [inspect.getsource(f) for f in (env.Scenario.task_text, env.Scenario.auditor_view,
                                            env.Scenario.contradiction_text, env2.Scenario2.task_text)]
    texts.append(json.dumps(env2.INCENTIVES, sort_keys=True))
    return ({f: sha(PKG / f) for f in ("env.py", "env2.py", "org.py", "run.py")}
            | {"prompt_hash": prompt_hash(),
               "env_text_hash": hashlib.sha256("\n".join(texts).encode()).hexdigest()[:16]})


def rel(path: str) -> str:
    p = pathlib.Path(path)
    p = p if p.is_absolute() else (ROOT / p)
    return str(p.resolve().relative_to(ROOT))


# ---------------- authority classification ----------------

def required_level(spec_path: str) -> tuple[int, list[str]]:
    """Minimum authority level a spec needs, computed deterministically from the spec and the mandate."""
    mandate = json.loads(MANDATE.read_text())
    spec = json.loads((ROOT / spec_path).read_text())
    reasons, level = [], 1
    model = spec.get("model", {})
    subj = mandate["subject_model"]
    if model.get("provider") != subj["provider"] or model.get("name") != subj["name"]:
        return 3, [f"model {model.get('provider')}/{model.get('name')} differs from mandated subject "
                   f"{subj['provider']}/{subj['name']} (model population change / possible external spend)"]
    # ---- structure: fail closed (second bypass fix) ----
    cells, seeds = spec.get("cells"), spec.get("seeds")
    if not isinstance(cells, list) or not cells:
        level, reasons = max(level, 2), reasons + ["spec has no cells: preregistered-condition check cannot run (fail closed)"]
    if not isinstance(seeds, list) or not seeds:
        level, reasons = max(level, 2), reasons + ["spec has no seeds: trial budget cannot be computed (fail closed)"]
    approved_hash = mandate.get("approved_spec_hashes", {}).get(spec_path)
    is_approved_exact = approved_hash is not None and approved_hash == sha(ROOT / spec_path)
    for k in spec:
        if k in SPEC_FUNCTIONAL_KEYS or k in SPEC_DOC_KEYS:
            continue
        if k in SPEC_DECLARATIVE_KEYS:
            if not is_approved_exact:
                level = 3
                reasons.append(f"top-level '{k}' declares outcomes/analysis/exclusions outside a human-approved, "
                               f"hash-matched spec (possible primary-outcome or exclusion change)")
        else:
            level, reasons = max(level, 2), reasons + [f"top-level '{k}' is not a recognized spec field"]
    family = spec.get("environment", {}).get("name", "freightroute")
    if family not in mandate["approved_environment_families"]:
        level, reasons = 2, reasons + [f"environment family '{family}' not in approved families"]
    space = PREREG_SPACE.get(family, {})
    env_cfg = spec.get("environment", {})
    # unrecognized or changed environment parameters
    defaults = ENV_DEFAULTS.get(family, {})
    for k, v in env_cfg.items():
        if k not in defaults:
            level, reasons = max(level, 2), reasons + [f"environment.{k} is not a recognized preregistered parameter"]
        elif defaults[k] is not None and v != defaults[k]:
            level, reasons = max(level, 2), reasons + [f"environment.{k}={v!r} differs from preregistered {defaults[k]!r}"]
    # unrecognized or changed model parameters
    for k, v in model.items():
        if k in ("provider", "name"):
            continue
        if k not in MODEL_DEFAULTS:
            level, reasons = max(level, 2), reasons + [f"model.{k} is not a recognized preregistered parameter"]
        elif v != MODEL_DEFAULTS[k]:
            level, reasons = max(level, 2), reasons + [f"model.{k}={v!r} differs from preregistered {MODEL_DEFAULTS[k]!r}"]
    # unrecognized cell fields (a renamed or new manipulation must not pass silently)
    known_cell_keys = CELL_META_KEYS | {k for k in space if not k.startswith("env.")}
    for c in spec.get("cells", []):
        for k in c:
            if k not in known_cell_keys:
                level = max(level, 2)
                reasons.append(f"cell {c.get('cell')}: '{k}' is not a recognized preregistered field")
    for key, allowed in space.items():
        if key.startswith("env."):
            v = env_cfg.get(key[4:], 0)
            if v not in allowed:
                level, reasons = max(level, 2), reasons + [f"{key}={v!r} outside preregistered {sorted(allowed, key=str)}"]
            continue
        for c in spec.get("cells", []):
            v = c.get(key, False if key == "auditor" else None)
            if v is not None and v not in allowed:
                level = max(level, 2)
                reasons.append(f"cell {c.get('cell')}: {key}={v!r} outside preregistered {sorted(allowed, key=str)}")
    n_trials = len(spec.get("cells", [])) * len(spec.get("seeds", []))
    b = mandate["budget"]
    if n_trials > b["max_trials_per_experiment_level1"]:
        level, reasons = max(level, 2), reasons + [f"{n_trials} trials > level-1 budget {b['max_trials_per_experiment_level1']}"]
    if not reasons:
        reasons.append("inside preregistered condition space, mandated model, within level-1 budget")
    if spec_path in mandate.get("approved_specs", {}):
        reasons.append(f"human-approved spec: {mandate['approved_specs'][spec_path]}")
    return level, reasons


# ---------------- timing (REVIEW_POLICY: timing claims) ----------------

TIMING_PHASES = {1: "before run completion", 2: "after run completion, before outcome inspection",
                 3: "after outcome inspection"}


def experiment_timing(exp: str) -> dict | None:
    """Machine-derived timing facts for an experiment, from the run log and the timeline."""
    logf = ROOT / "data" / f"{exp}.log"
    trials = ROOT / "data" / "trials" / f"{exp}.jsonl"
    if not logf.exists() and not trials.exists():
        return None
    events = [json.loads(l) for l in TIMELINE.read_text().splitlines() if l.strip()] if TIMELINE.exists() else []
    started = next((e["ts"] for e in events if e.get("stage") == "experiment_started" and exp in e.get("text", "")), None)
    done = logf.exists() and any(l.startswith("DONE") for l in logf.read_text().splitlines())
    finished_at = None
    if done:
        finished_at = datetime.datetime.fromtimestamp(trials.stat().st_mtime).isoformat(timespec="seconds") \
            if trials.exists() else None
    inspected = [e["ts"] for e in events if e.get("stage") in ("analysis_written", "pod_synthesis")
                 and exp in json.dumps(e)]
    # Also count any analysis artifact on disk (an agent may analyze without the logged CLI path).
    for pattern in (f"results/{exp}*", f"critiques/*{exp}*", f"pods/*/*/*{exp}*"):
        for f in ROOT.glob(pattern):
            inspected.append(datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat(timespec="seconds"))
    first_inspection = min(inspected) if inspected else None
    phase = 1 if not done else (3 if first_inspection else 2)
    return {"experiment": exp, "run_started": started, "run_finished": done, "last_trial_written": finished_at,
            "first_outcome_inspection_logged": first_inspection, "phase": phase, "phase_label": TIMING_PHASES[phase]}


def timing_for(cites: list[str], spec: str | None) -> list[dict]:
    exps = set()
    for c in list(cites or []) + ([spec] if spec else []):
        stem = pathlib.Path(str(c)).stem
        if (ROOT / "data" / "trials" / f"{stem}.jsonl").exists() or (ROOT / "data" / f"{stem}.log").exists():
            exps.add(stem)
        for f in (ROOT / "data" / "trials").glob("*.jsonl") if (ROOT / "data" / "trials").exists() else []:
            if f.stem in str(c):
                exps.add(f.stem)
    return [t for t in (experiment_timing(e) for e in sorted(exps)) if t]


# ---------------- decision records ----------------

def load_decision(did: str) -> dict:
    p = DECISIONS / f"{did}.json"
    if not p.exists():
        raise AuthorityError(f"REFUSED: decision {did} does not exist")
    return json.loads(p.read_text())


def save_decision(d: dict) -> None:
    DECISIONS.mkdir(exist_ok=True)
    (DECISIONS / f"{d['id']}.json").write_text(json.dumps(d, indent=2))


def authorize(d: dict, action: str) -> None:
    """Raise unless decision d authorizes `action` under its level."""
    if d.get("overridden"):
        raise AuthorityError(f"REFUSED: {d['id']} was overridden by the human: {d['overridden']['note']}")
    if d["action"] != action:
        raise AuthorityError(f"REFUSED: {d['id']} authorizes '{d['action']}', not '{action}'")
    reviews = d.get("reviews", [])
    latest = reviews[-1]["verdict"] if reviews else None
    if latest in ("BLOCK", "FAIL"):
        raise AuthorityError(f"REFUSED: {d['id']} was BLOCKED by the methodology reviewer")
    if latest == "CONCERNS" and (reviews[-1].get("material_concerns") or 0) > 0:
        raise AuthorityError(f"REFUSED: {d['id']} has {reviews[-1]['material_concerns']} MATERIAL concern(s); "
                             f"resolve them before the affected action proceeds")
    if d["level"] >= 2 and latest not in ALLOWING:
        raise AuthorityError(f"REFUSED: {d['id']} is level {d['level']}; needs a methodology review PASS "
                             f"(latest: {latest or 'none'})")
    if (d["level"] >= 3 or d.get("escalation_required")) and not d.get("human_approval"):
        why = "reviewer escalated it" if d.get("escalation_required") else "it is level 3"
        raise AuthorityError(f"REFUSED: {d['id']} needs human approval via `falsify escalate` ({why})")


def next_id() -> str:
    DECISIONS.mkdir(exist_ok=True)
    n = len(list(DECISIONS.glob("D*.json"))) + 1
    return f"D{n:03d}"


# ---------------- commands ----------------

def cmd_level(a):
    lvl, why = required_level(rel(a.spec))
    print(json.dumps({"spec": rel(a.spec), "required_level": lvl, "reasons": why}, indent=2))


def cmd_decide(a):
    d = {"id": next_id(), "ts": now(), "by": "PI", "level": a.level, "action": a.action,
         "decision": a.decision, "reason": a.reason, "confidence": a.confidence,
         "alternatives_rejected": a.alternatives, "cites": a.cites or [], "reviews": [],
         "timing_at_decision": timing_for(a.cites or [], a.spec)}
    if a.spec:
        spec = rel(a.spec)
        req, why = required_level(spec)
        if a.level < req:
            raise AuthorityError(f"REFUSED: {spec} requires level {req} ({'; '.join(why)}); decision declared level {a.level}")
        d.update(spec=spec, spec_hash=sha(ROOT / spec), required_level=req, level_reasons=why,
                 code_hashes=code_hashes())
    save_decision(d)
    log_event("PI", "pi_decision", f"{d['id']} [L{a.level} {a.action}] {a.decision} | reason: {a.reason} | "
              f"confidence {a.confidence} | rejected: {a.alternatives}", cites=[d["id"], *(d["cites"])],
              decision_id=d["id"], level=a.level)
    print(json.dumps(d, indent=2))


def auto_checks(d: dict) -> dict:
    """Checks the CLI can verify mechanically for a decision (no judgement involved)."""
    checks = {"decision_recorded_before_action": True}
    if d.get("spec"):
        mandate = json.loads(MANDATE.read_text())
        spec = json.loads((ROOT / d["spec"]).read_text())
        req, _ = required_level(d["spec"])
        n = len(spec.get("cells", [])) * len(spec.get("seeds", []))
        m = spec.get("model", {})
        checks.update(
            spec_hash_verified=sha(ROOT / d["spec"]) == d.get("spec_hash"),
            model_within_mandate=(m.get("provider"), m.get("name")) ==
                                 (mandate["subject_model"]["provider"], mandate["subject_model"]["name"]),
            budget_compliant=n <= mandate["budget"]["max_trials_per_experiment_level1"] or d["level"] >= 2,
            level_correct=d["level"] >= req,
            code_unchanged_since_decision=(d.get("code_hashes") == code_hashes()) if d.get("code_hashes") else None,
            inside_preregistered_condition_space=req == 1)
    return checks


def cmd_review(a):
    d = load_decision(a.did)
    if a.verdict in ("CONCERNS", "PASS_WITH_NOTE") and a.material is None:
        raise AuthorityError("REFUSED: label materiality: --material N (count of MATERIAL concerns; 0 if all NON_MATERIAL)")
    if a.verdict == "PASS_WITH_NOTE" and a.material:
        raise AuthorityError("REFUSED: PASS_WITH_NOTE cannot carry MATERIAL concerns; use CONCERNS or BLOCK")
    review = {"ts": now(), "by": "methodology_reviewer", "verdict": a.verdict, "findings": a.findings,
              "material_concerns": a.material,
              "auto_checks": auto_checks(d),
              "attested": {"preregistered": a.preregistered, "primary_outcomes_unchanged": a.outcomes_unchanged,
                           "exploratory_labeled": a.exploratory_labeled, "novelty_language_ok": a.novelty_ok}}
    d["reviews"].append(review)
    if a.verdict == "ESCALATE":
        d["escalation_required"] = True
    save_decision(d)
    failed = [k for k, v in review["auto_checks"].items() if v is False]
    log_event("methodology_reviewer", "methodology_review",
              f"{a.did}: {a.verdict}" + (f" ({a.material} MATERIAL)" if a.material is not None else "") +
              f". {a.findings}" + (f" | AUTO-CHECK FAILURES: {failed}" if failed else ""),
              cites=[a.did], decision_id=a.did, verdict=a.verdict, auto_checks=review["auto_checks"])
    print(json.dumps({"decision": a.did, "verdict": a.verdict, **review["auto_checks"],
                      **{k: v for k, v in review["attested"].items() if v is not None}}, indent=2))


def cmd_escalate(a):
    # Reaching this line means the Omnigent human_gate was approved by the human.
    d = load_decision(a.did)
    d["human_approval"] = {"ts": now(), "question": a.question, "via": "omnigent human_gate"}
    save_decision(d)
    log_event("human", "human_gate_approved", f"{a.did}: {a.question}", cites=[a.did], decision_id=a.did)
    print(f"{a.did}: human approval recorded")


def cmd_override(a):
    d = load_decision(a.did)
    d["overridden"] = {"ts": now(), "note": a.note}
    save_decision(d)
    log_event("human", "human_override", f"{a.did} OVERRIDDEN: {a.note}", cites=[a.did], decision_id=a.did)
    print(f"{a.did}: overridden")


def cmd_disposition(a):
    """End-of-loop batch disposition of NON_MATERIAL review concerns (one record, no per-concern decisions)."""
    ids = [x for x in a.decisions.split(",") if x]
    items = []
    for did in ids:
        d = load_decision(did)
        for r in d.get("reviews", []):
            if r["verdict"] in ("CONCERNS", "PASS_WITH_NOTE"):
                items.append({"decision": did, "review_ts": r["ts"], "verdict": r["verdict"],
                              "material_concerns": r.get("material_concerns"), "findings": r["findings"]})
    rec = {"loop": a.loop, "ts": now(), "by": "PI", "note": a.note, "items": items}
    DECISIONS.mkdir(exist_ok=True)
    (DECISIONS / f"disposition_{a.loop}.json").write_text(json.dumps(rec, indent=2))
    log_event("PI", "end_of_loop_disposition", f"{a.loop}: {len(items)} review notes dispositioned across {ids}. {a.note}",
              cites=[f"decisions/disposition_{a.loop}.json", *ids])
    print(f"disposition_{a.loop}: {len(items)} items")


def cmd_timing(a):
    print(json.dumps(experiment_timing(a.exp), indent=2))


def cmd_decisions(a):
    for p in sorted(DECISIONS.glob("D*.json")) if DECISIONS.exists() else []:
        d = json.loads(p.read_text())
        rv = d["reviews"][-1]["verdict"] if d["reviews"] else "-"
        flags = (" OVERRIDDEN" if d.get("overridden") else "") + (" HUMAN-APPROVED" if d.get("human_approval") else "")
        print(f"{d['id']} L{d['level']} {d['action']:8} review={rv:8}{flags}  {d['decision'][:90]}")


def cmd_run(a):
    spec_rel = rel(a.spec)
    d = load_decision(a.decision)
    authorize(d, "run")
    if d.get("spec") != spec_rel:
        raise AuthorityError(f"REFUSED: {d['id']} authorizes {d.get('spec')}, not {spec_rel}")
    if sha(ROOT / spec_rel) != d["spec_hash"]:
        raise AuthorityError(f"REFUSED: {spec_rel} changed since {d['id']} was recorded (hash mismatch)")
    req, why = required_level(spec_rel)
    if d["level"] < req:
        raise AuthorityError(f"REFUSED: spec now requires level {req}: {'; '.join(why)}")
    spec = json.loads((ROOT / spec_rel).read_text())
    exp = spec["experiment_id"]
    logf = ROOT / "data" / f"{exp}.log"
    proc = subprocess.Popen([sys.executable, "-m", "falsify.run", spec_rel], cwd=ROOT,
                            stdout=logf.open("a"), stderr=subprocess.STDOUT, start_new_session=True)
    log_event("runner", "experiment_started", f"Started {exp} (pid {proc.pid}) under {d['id']} (L{d['level']})",
              cites=[spec_rel, d["id"]], decision_id=d["id"], spec_hash=d["spec_hash"])
    print(json.dumps({"started": exp, "pid": proc.pid, "decision": d["id"], "log": str(logf),
                      "trials_planned": len(spec["cells"]) * len(spec["seeds"])}))


def cmd_status(a):
    trials = ROOT / "data" / "trials" / f"{a.exp}.jsonl"
    done = len(trials.read_text().splitlines()) if trials.exists() else 0
    logf = ROOT / "data" / f"{a.exp}.log"
    tail = logf.read_text().splitlines()[-1] if logf.exists() and logf.read_text() else ""
    print(json.dumps({"experiment": a.exp, "trials_written": done, "finished": tail.startswith("DONE"),
                      "last_log_line": tail}))


def cmd_analyze(a):
    subprocess.run([sys.executable, "-m", "falsify.analyze", a.exp], cwd=ROOT, check=True)
    log_event("statistician-tool", "analysis_written", f"results/{a.exp}.json", cites=[a.exp])


def cmd_hypotheses(a):
    print(REGISTRY.read_text())


def cmd_conclude(a):
    d = load_decision(a.decision)
    authorize(d, "conclude")
    if a.status not in STATUSES:
        raise AuthorityError(f"status must be one of {sorted(STATUSES)}")
    if a.status in ("supported", "falsified"):
        blocked = unresolved_analysis_disagreement(a.evidence)
        if blocked:
            raise AuthorityError(f"REFUSED: analysts materially disagree on {a.evidence} ({blocked}); "
                                 f"resolve the discrepancy before claiming '{a.status}'")
    reg = json.loads(REGISTRY.read_text())
    h = next((h for h in reg["hypotheses"] if h["id"] == a.id), None)
    if h is None:
        raise AuthorityError(f"unknown hypothesis {a.id}")
    old = h["status"]
    h["status"] = a.status
    h.setdefault("history", []).append({"ts": now(), "from": old, "to": a.status, "evidence": a.evidence,
                                        "note": a.note, "decision": d["id"]})
    if a.evidence and a.evidence not in h["tested_by"]:
        h["tested_by"].append(a.evidence)
    REGISTRY.write_text(json.dumps(reg, indent=2))
    log_event("PI", "status_change", f"{a.id}: {old} -> {a.status} under {d['id']}. {a.note}",
              cites=[a.evidence, d["id"]], decision_id=d["id"])
    print(f"{a.id}: {old} -> {a.status}")


def research_budget() -> dict:
    mandate = json.loads(MANDATE.read_text())
    calls = tok_in = tok_out = trials = invalid = 0
    experiments = {}
    for f in sorted((ROOT / "data" / "trials").glob("*.jsonl")):
        if f.name.startswith("_"):
            continue
        rows = [json.loads(l) for l in f.read_text().splitlines() if l.strip()]
        m = [r.get("measured", {}) for r in rows]
        calls += sum(x.get("llm_calls", 0) for x in m)
        tok_in += sum(x.get("post_tokens_in", 0) for x in m)
        tok_out += sum(x.get("post_tokens_out", 0) for x in m)
        trials += len(rows); invalid += sum(not r.get("valid", True) for r in rows)
        logf = ROOT / "data" / f"{f.stem}.log"
        done = logf.exists() and any(l.startswith("DONE") for l in logf.read_text().splitlines())
        experiments[f.stem] = {"trials": len(rows), "finished": done}
    events = [json.loads(l) for l in TIMELINE.read_text().splitlines() if l.strip()] if TIMELINE.exists() else []
    t0 = min((e.get("ts", "") for e in events if e.get("ts")), default=None)
    reg = json.loads(REGISTRY.read_text())
    status = {}
    for h in reg["hypotheses"]:
        status.setdefault(h["status"], []).append(h["id"])
    decisions = [json.loads(p.read_text()) for p in sorted(DECISIONS.glob("D*.json"))] if DECISIONS.exists() else []
    return {
        "as_of": now(),
        "elapsed_research_minutes": round((datetime.datetime.fromisoformat(now()) -
                                           datetime.datetime.fromisoformat(t0[:19])).total_seconds() / 60, 1) if t0 else 0,
        "external_spend_usd": round(sum(json.loads(l)["usd"] for l in (ROOT / "data" / "spend_ledger.jsonl")
                                        .read_text().splitlines() if l.strip()), 4)
                              if (ROOT / "data" / "spend_ledger.jsonl").exists() else 0.0,
        "external_spend_cap_without_human_usd": mandate["budget"]["external_spend_usd_without_human"],
        "subject_model": mandate["subject_model"],
        "model_calls_used": calls, "subject_tokens_in": tok_in, "subject_tokens_out": tok_out,
        "trials_run": trials, "trials_invalid": invalid,
        "experiments": experiments,
        "experiments_completed": sum(e["finished"] for e in experiments.values()),
        "hypotheses_by_status": status,
        "hypotheses_eliminated": status.get("falsified", []),
        "unresolved": status.get("untested", []) + status.get("inconclusive", []) + status.get("needs replication", []),
        "decisions": {"total": len(decisions), "by_level": {str(l): sum(d["level"] == l for d in decisions) for l in (1, 2, 3)},
                      "human_escalations": sum(bool(d.get("human_approval")) for d in decisions),
                      "human_overrides": sum(bool(d.get("overridden")) for d in decisions)},
    }


def cmd_budget(a):
    b = research_budget()
    out = ROOT / "results" / "budget.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(b, indent=2))
    print(json.dumps(b, indent=2))


# ---------------- research pods ----------------

def pod_dir(stage: str, loop: str) -> pathlib.Path:
    if stage not in POD_STAGES:
        raise AuthorityError(f"unknown pod stage {stage}; one of {sorted(POD_STAGES)}")
    return PODS / stage / loop


def pod_status(stage, loop) -> dict:
    return json.loads((pod_dir(stage, loop) / "status.json").read_text())


def write_status(stage, loop, st) -> None:
    (pod_dir(stage, loop) / "status.json").write_text(json.dumps(st, indent=2))


def cmd_pod_init(a):
    d = pod_dir(a.stage, a.loop)
    (d / "subagent_outputs").mkdir(parents=True, exist_ok=True)
    inputs = json.loads(pathlib.Path(a.inputs).read_text()) if a.inputs.endswith(".json") else {"brief": a.inputs}
    (d / "inputs.json").write_text(json.dumps(inputs, indent=2))
    members = [m for m in a.members.split(",") if m]
    write_status(a.stage, a.loop, {"stage": a.stage, "loop": a.loop, "lead": a.lead, "state": "RUNNING",
                                   "started": now(), "members": {m: "PENDING" for m in members}, "lead_state": "COORDINATING"})
    log_event(a.lead, "pod_started", f"{a.stage} pod {a.loop}: members {members}", cites=[str(d.relative_to(ROOT))],
              pod=a.stage, loop=a.loop)
    print(str(d.relative_to(ROOT)))


def cmd_pod_mark(a):
    if a.state not in MEMBER_STATES:
        raise AuthorityError(f"state must be one of {sorted(MEMBER_STATES)}")
    st = pod_status(a.stage, a.loop)
    if a.member not in st["members"]:
        raise AuthorityError(f"{a.member} is not a member of the {a.stage} pod")
    st["members"][a.member] = a.state
    write_status(a.stage, a.loop, st)
    print(f"{a.stage}/{a.loop} {a.member}: {a.state}")


def cmd_pod_output(a):
    st = pod_status(a.stage, a.loop)
    out = json.loads(pathlib.Path(a.file).read_text())
    missing = [f for f in SUBAGENT_FIELDS if f not in out]
    if missing or out.get("member") != a.member or a.member not in st["members"]:
        raise AuthorityError(f"REFUSED subagent output: missing {missing} or member mismatch ({out.get('member')} vs {a.member})")
    (pod_dir(a.stage, a.loop) / "subagent_outputs" / f"{a.member}.json").write_text(json.dumps(out, indent=2))
    st["members"][a.member] = "COMPLETE"
    write_status(a.stage, a.loop, st)
    log_event(a.member, "pod_member_output", f"{a.stage}/{a.loop}: {str(out['position'])[:200]}",
              cites=out.get("evidence_refs", []), pod=a.stage, loop=a.loop)
    print(f"{a.stage}/{a.loop} {a.member}: output recorded")


def cmd_pod_submit(a):
    d = pod_dir(a.stage, a.loop)
    st = pod_status(a.stage, a.loop)
    syn = json.loads(pathlib.Path(a.file).read_text())
    missing = [f for f in SYNTHESIS_FIELDS if f not in syn]
    if a.stage == "analysis":
        missing += [f for f in ("experiment_id", "analysts_agree", "material_disagreements") if f not in syn]
    if missing:
        raise AuthorityError(f"REFUSED synthesis: missing fields {missing}")
    have = {p.stem for p in (d / "subagent_outputs").glob("*.json")}
    prov = set(syn["subagent_provenance"]) if isinstance(syn["subagent_provenance"], (list, dict)) else set()
    if not have <= prov:
        raise AuthorityError(f"REFUSED synthesis: provenance {sorted(prov)} omits recorded outputs {sorted(have - prov)}")
    if a.stage == "analysis" and syn["material_disagreements"] and syn["analysts_agree"]:
        raise AuthorityError("REFUSED synthesis: analysts_agree=true while material_disagreements is non-empty")
    syn.update(stage=a.stage, loop=a.loop, lead=st["lead"], submitted=now())
    (d / "synthesis.json").write_text(json.dumps(syn, indent=2))
    st.update(state="COMPLETE", lead_state="COMPLETE", finished=now(),
              summary={"researchers": len(st["members"]) + 1,
                       "disagreements": len(syn["disagreements"]) if isinstance(syn["disagreements"], list) else 1,
                       "headline": str(syn["conclusion"])[:160]})
    write_status(a.stage, a.loop, st)
    log_event(st["lead"], "pod_synthesis",
              f"{a.stage}/{a.loop}: {str(syn['conclusion'])[:220]} | disagreements: {st['summary']['disagreements']} | "
              f"recommendation: {str(syn['recommendation'])[:160]}", cites=[str((d / 'synthesis.json').relative_to(ROOT))],
              pod=a.stage, loop=a.loop)
    print(json.dumps(st["summary"]))


def unresolved_analysis_disagreement(exp: str) -> list:
    """Analysis-pod syntheses for `exp` whose analysts materially disagree (blocks strong status claims)."""
    hits = []
    for f in PODS.glob("analysis/*/synthesis.json") if PODS.exists() else []:
        syn = json.loads(f.read_text())
        if syn.get("experiment_id") == exp and (not syn.get("analysts_agree") or syn.get("material_disagreements")):
            hits.append(str(f.relative_to(ROOT)))
    return hits


def cmd_log(a):
    print(json.dumps(log_event(a.agent, a.stage, a.text, a.cites)))


def main(argv=None):
    p = argparse.ArgumentParser(prog="falsify")
    sub = p.add_subparsers(required=True)
    s = sub.add_parser("status"); s.add_argument("exp"); s.set_defaults(f=cmd_status)
    s = sub.add_parser("analyze"); s.add_argument("exp"); s.set_defaults(f=cmd_analyze)
    s = sub.add_parser("hypotheses"); s.set_defaults(f=cmd_hypotheses)
    s = sub.add_parser("log"); s.add_argument("agent"); s.add_argument("stage"); s.add_argument("text")
    s.add_argument("--cites", nargs="*"); s.set_defaults(f=cmd_log)
    s = sub.add_parser("level"); s.add_argument("spec"); s.set_defaults(f=cmd_level)
    s = sub.add_parser("decide")
    s.add_argument("--level", type=int, choices=[1, 2, 3], required=True)
    s.add_argument("--action", choices=["run", "conclude", "other"], required=True)
    s.add_argument("--decision", required=True); s.add_argument("--reason", required=True)
    s.add_argument("--confidence", type=float, required=True); s.add_argument("--alternatives", required=True)
    s.add_argument("--spec"); s.add_argument("--cites", nargs="*"); s.set_defaults(f=cmd_decide)
    s = sub.add_parser("review"); s.add_argument("did")
    s.add_argument("--verdict", type=lambda v: v.upper().replace(" ", "_").replace("PASS_WITH_NOTES", "PASS_WITH_NOTE")
                   .replace("ESCALATE_TO_HUMAN", "ESCALATE"), choices=VERDICTS, required=True)
    s.add_argument("--findings", required=True)
    for flag, dest in (("--preregistered", "preregistered"), ("--outcomes-unchanged", "outcomes_unchanged"),
                       ("--exploratory-labeled", "exploratory_labeled"), ("--novelty-ok", "novelty_ok")):
        s.add_argument(flag, dest=dest, choices=["yes", "no", "n/a"])
    s.add_argument("--material", type=int, help="number of MATERIAL concerns (required for CONCERNS / PASS_WITH_NOTE)")
    s.set_defaults(f=cmd_review)
    s = sub.add_parser("disposition"); s.add_argument("loop"); s.add_argument("--decisions", required=True)
    s.add_argument("--note", required=True); s.set_defaults(f=cmd_disposition)
    s = sub.add_parser("timing"); s.add_argument("exp"); s.set_defaults(f=cmd_timing)
    s = sub.add_parser("budget"); s.set_defaults(f=cmd_budget)
    pod = sub.add_parser("pod").add_subparsers(required=True)
    s = pod.add_parser("init"); s.add_argument("stage"); s.add_argument("loop"); s.add_argument("--lead", required=True)
    s.add_argument("--members", required=True); s.add_argument("--inputs", required=True); s.set_defaults(f=cmd_pod_init)
    s = pod.add_parser("mark"); s.add_argument("stage"); s.add_argument("loop"); s.add_argument("member")
    s.add_argument("state"); s.set_defaults(f=cmd_pod_mark)
    s = pod.add_parser("output"); s.add_argument("stage"); s.add_argument("loop"); s.add_argument("member")
    s.add_argument("file"); s.set_defaults(f=cmd_pod_output)
    s = pod.add_parser("submit"); s.add_argument("stage"); s.add_argument("loop"); s.add_argument("file")
    s.set_defaults(f=cmd_pod_submit)
    s = sub.add_parser("escalate"); s.add_argument("did"); s.add_argument("--question", required=True)
    s.set_defaults(f=cmd_escalate)
    s = sub.add_parser("override"); s.add_argument("did"); s.add_argument("--note", required=True)
    s.set_defaults(f=cmd_override)
    s = sub.add_parser("decisions"); s.set_defaults(f=cmd_decisions)
    s = sub.add_parser("run"); s.add_argument("spec"); s.add_argument("--decision", required=True)
    s.set_defaults(f=cmd_run)
    s = sub.add_parser("conclude"); s.add_argument("id"); s.add_argument("status")
    s.add_argument("--evidence", required=True); s.add_argument("--note", required=True)
    s.add_argument("--decision", required=True); s.set_defaults(f=cmd_conclude)
    a = p.parse_args(argv)
    a.f(a)


if __name__ == "__main__":
    main()
