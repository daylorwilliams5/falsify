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

from .org import run_trial, run_trial_v2


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
    trial_fn = run_trial_v2 if spec["environment"].get("name") == "freightroute_v2" else run_trial
    lock, t0, n = threading.Lock(), time.time(), 0
    with ThreadPoolExecutor(spec.get("concurrency", 1)) as pool:
        futs = {pool.submit(trial_fn, c, s, spec["model"], spec["environment"], spec_hash, exp): (c, s)
                for c, s in jobs}
        for f in as_completed(futs):
            c, s = futs[f]
            try:
                trial = f.result()
            except Exception as e:  # infrastructure error -> recorded INVALID trial (policy A)
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
                brief = (f"wasted={m['wasted_actions']} switch={m['switched']} success={m['success']}"
                         if "wasted_actions" in m else
                         f"breach={m['integrity_breach']} true={m['true_success']} reported={m['reported_success']}")
                print(f"[{n}/{len(jobs)} {time.time() - t0:.0f}s] {trial['trial_id']} valid={trial['valid']} {brief}",
                      flush=True)
    replacement_pass(spec, spec_hash, out, trial_fn)
    print(f"DONE {exp} in {time.time() - t0:.0f}s", flush=True)


REPLACEMENT_OFFSET = 10000  # preregistered: replacement seed = original seed + 10000 * attempt


def replacement_pass(spec, spec_hash, out, trial_fn) -> None:
    """Policy A: rerun invalid trials once with a preregistered replacement seed; pause if >10% invalid."""
    exp = spec["experiment_id"]
    trials = [json.loads(l) for l in out.read_text().splitlines() if l.strip()]
    by_cell = {}
    for t in trials:
        by_cell.setdefault(t["cell"], []).append(t)
    rates = {c: sum(not t["valid"] for t in ts) / len(ts) for c, ts in by_cell.items()}
    flagged = {c: round(r, 3) for c, r in rates.items() if r > 0.10}
    if flagged:
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


if __name__ == "__main__":
    main(sys.argv[1])
