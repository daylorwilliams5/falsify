"""Run every cell × seed in a spec and append trials to data/trials/<experiment_id>.jsonl.

Usage: uv run python -m falsify.run specs/exp001_pilot.json
Resumable: trials already in the output file are skipped.
"""
import hashlib
import json
import pathlib
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from .org import run_trial, run_trial_e, run_trial_v2


def main(spec_path: str) -> None:
    raw = pathlib.Path(spec_path).read_bytes()
    spec = json.loads(raw)
    spec_hash = hashlib.sha256(raw).hexdigest()[:16]
    exp = spec["experiment_id"]
    out = pathlib.Path("data/trials") / f"{exp}.jsonl"
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set()
    if out.exists():
        done = {json.loads(l)["trial_id"] for l in out.read_text().splitlines() if l.strip()}

    jobs = [(c, s) for s in spec["seeds"] for c in spec["cells"]
            if f"{exp}-{c['cell']}-{s:03d}" not in done]
    print(f"{exp}: {len(jobs)} trials to run ({len(done)} already done), spec {spec_hash}", flush=True)
    trial_fn = {"freightroute_v2": run_trial_v2, "freightroute_evidence": run_trial_e}.get(
        spec["environment"].get("name"), run_trial)
    lock, t0, n = threading.Lock(), time.time(), 0
    budget_stop = False
    with ThreadPoolExecutor(spec.get("concurrency", 1)) as pool:
        futs = {pool.submit(trial_fn, c, s, spec["model"], spec["environment"], spec_hash, exp): (c, s)
                for c, s in jobs}
        for f in as_completed(futs):
            c, s = futs[f]
            try:
                trial = f.result()
            except Exception as e:  # infrastructure error -> recorded INVALID trial (policy A)
                if type(e).__name__ == "BudgetExceeded":
                    print(f"STOP {exp}: {e}. Cancelling remaining trials (spend cap).", flush=True)
                    for other in futs:
                        other.cancel()
                    budget_stop = True
                trial = {"trial_id": f"{exp}-{c['cell']}-{s:03d}", "experiment_id": exp, "spec_hash": spec_hash,
                         "seed": s, **c, "valid": False, "invalid_reason": f"exception: {e!r}"[:300],
                         "measured": {}}
                print(f"ERROR {c['cell']} seed {s}: {e!r}", flush=True)
            with lock:
                with out.open("a") as fh:
                    fh.write(json.dumps(trial) + "\n")
                n += 1
                m = trial["measured"]
                if not trial["valid"]:
                    trial.setdefault("invalid_reason", "parse_failure_after_retry")
                    print(f"[{n}/{len(jobs)}] {trial['trial_id']} INVALID ({trial['invalid_reason'][:80]})", flush=True)
                    continue
                brief = (f"first={m['first_response']} switch={m['switched']} persist={m['persist_actions']}"
                         if "first_response" in m else
                         f"wasted={m['wasted_actions']} switch={m['switched']} success={m['success']}"
                         if "wasted_actions" in m else
                         f"breach={m['integrity_breach']} true={m['true_success']} reported={m['reported_success']}")
                print(f"[{n}/{len(jobs)} {time.time() - t0:.0f}s] {trial['trial_id']} valid={trial['valid']} {brief}",
                      flush=True)
    if budget_stop:
        print(f"STOPPED {exp}: spend cap reached; no replacement trials run", flush=True)
        return
    replacement_pass(spec, spec_hash, out, trial_fn)
    print(f"DONE {exp} in {time.time() - t0:.0f}s", flush=True)


REPLACEMENT_OFFSET = 10000  # preregistered: replacement seed = original seed + 10000 * attempt


def replacement_pass(spec, spec_hash, out, trial_fn, human_override: bool = False) -> None:
    """Policy A: rerun invalid trials once with a preregistered replacement seed; pause if >10% invalid,
    unless the human has approved resuming after a pause (human_override, set only via `falsify resume`)."""
    exp = spec["experiment_id"]
    trials = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
    by_cell = {}
    for t in trials:
        by_cell.setdefault(t["cell"], []).append(t)
    rates = {c: sum(not t["valid"] for t in ts) / len(ts) for c, ts in by_cell.items()}
    flagged = {c: round(r, 3) for c, r in rates.items() if r > 0.10}
    if flagged and not human_override:
        flag = pathlib.Path("results") / f"{exp}_PAUSE.json"
        flag.parent.mkdir(exist_ok=True)
        flag.write_text(json.dumps({"reason": "invalid-trial rate > 10% in cell(s); human decision required",
                                    "cells": flagged}, indent=2))
        print(f"PAUSE {exp}: invalid rate >10% in {flagged}. No replacements run; awaiting human decision.", flush=True)
        return
    have = {t["trial_id"] for t in trials}
    cells = {c["cell"]: c for c in spec["cells"]}
    for t in trials:
        if t["valid"]:
            continue
        new_seed = t["seed"] + REPLACEMENT_OFFSET
        new_id = f"{exp}-{t['cell']}-{new_seed:03d}"
        if new_id in have:
            continue
        try:
            rep = trial_fn(cells[t["cell"]], new_seed, spec["model"], spec["environment"], spec_hash, exp)
        except Exception as e:
            rep = {"trial_id": new_id, "experiment_id": exp, "seed": new_seed, **cells[t["cell"]],
                   "valid": False, "invalid_reason": f"exception: {e!r}"[:300], "measured": {}}
        rep["replaces"] = t["trial_id"]
        with out.open("a") as fh:
            fh.write(json.dumps(rep) + "\n")
        print(f"REPLACEMENT {new_id} for {t['trial_id']} valid={rep['valid']}", flush=True)


def resume_after_pause(spec_path: str) -> None:
    """Human-approved resume: run preregistered replacement trials for every invalid trial (seed + 10000)."""
    raw = pathlib.Path(spec_path).read_bytes()
    spec = json.loads(raw)
    exp = spec["experiment_id"]
    out = pathlib.Path("data/trials") / f"{exp}.jsonl"
    trial_fn = {"freightroute_v2": run_trial_v2, "freightroute_evidence": run_trial_e}.get(
        spec["environment"].get("name"), run_trial)
    t0 = time.time()
    print(f"RESUME {exp}: replacement trials for invalid records (human-approved)", flush=True)
    replacement_pass(spec, hashlib.sha256(raw).hexdigest()[:16], out, trial_fn, human_override=True)
    print(f"DONE {exp} (replacements) in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "--resume-after-pause":
        resume_after_pause(sys.argv[1])
    else:
        main(sys.argv[1])
