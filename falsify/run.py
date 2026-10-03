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
            except Exception as e:  # infrastructure error: log it, keep going
                print(f"ERROR {c['cell']} seed {s}: {e!r}", flush=True)
                continue
            with lock:
                with out.open("a") as fh:
                    fh.write(json.dumps(trial) + "\n")
                n += 1
                m = trial["measured"]
                brief = (f"wasted={m['wasted_actions']} switch={m['switched']} success={m['success']}"
                         if "wasted_actions" in m else
                         f"breach={m['integrity_breach']} true={m['true_success']} reported={m['reported_success']}")
                print(f"[{n}/{len(jobs)} {time.time() - t0:.0f}s] {trial['trial_id']} valid={trial['valid']} {brief}",
                      flush=True)
    print(f"DONE {exp} in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main(sys.argv[1])
