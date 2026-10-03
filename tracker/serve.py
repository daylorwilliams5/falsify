"""Falsify research tracker: a read-only live view of the lab's state.

Usage: uv run python tracker/serve.py  (http://127.0.0.1:5210)
Reads only the lab's own files; never writes.
"""
import datetime as dt
import json
import pathlib
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from falsify import cli  # noqa: E402


def read_json(p):
    try:
        return json.loads(p.read_text())
    except Exception:
        return None


PROGRESS = re.compile(r"^\[(\d+)/(\d+)\s+(\d+)s\]")

# Default stage durations (minutes), from durations measured earlier today; replaced by Loop-3 measurements when available.
# exp009 (20 single-agent trials) took 15.4 min; loop-1/2 specialist turnarounds were ~3-6 min each.
STAGE_DEFAULTS = [
    ("design_pod", "Design pod (v2.1 proposal + confound hunter + info-gain)", 15, "pod: lead + 2 sub-agents, sequential"),
    ("design_decision", "PI decision + methodology review", 6, "loop-2 decision->review turnaround"),
    ("build", "Engineering build + tests (engineer)", 30, "estimate for v2.1 env changes + tests"),
    ("pilot", "20-trial v2.1 pilot (qwen3:8b)", 16, "exp009: 20 trials in 15.4 min"),
    ("analysis_pod", "Analysis pod (primary + independent + robustness)", 15, "pod estimate"),
    ("adversarial_pod", "Adversarial pod (skeptic + null advocate + confound hunter)", 15, "pod estimate"),
    ("final_decision", "PI keep-or-kill decision + review", 6, "decision->review turnaround"),
]


def ts(x):
    return dt.datetime.fromisoformat(str(x)[:19]) if x else None


def experiment_eta(exp: str) -> dict:
    logf = ROOT / "data" / f"{exp}.log"
    if not logf.exists():
        return {}
    lines = logf.read_text().splitlines()
    done = next((l for l in reversed(lines) if l.startswith("DONE")), None)
    if done:
        m = re.search(r"in (\d+)s", done)
        return {"finished": True, "duration_min": round(int(m.group(1)) / 60, 1) if m else None}
    prog = [PROGRESS.match(l) for l in lines]
    prog = [m for m in prog if m]
    if not prog:
        return {"finished": False, "eta_min": None, "basis": "no trials finished yet"}
    n, total, secs = map(int, prog[-1].groups())
    rate = secs / n
    remaining = max(total - n, 0) * rate
    started = dt.datetime.fromtimestamp(logf.stat().st_mtime) - dt.timedelta(seconds=0)
    return {"finished": False, "done": n, "total": total, "sec_per_trial": round(rate, 1),
            "eta_min": round(remaining / 60, 1),
            "eta_clock": (dt.datetime.now() + dt.timedelta(seconds=remaining)).strftime("%H:%M"),
            "basis": f"{n}/{total} trials in {secs}s"}


def loop_plan(events: list, loop_start: str | None) -> dict:
    if not loop_start:
        return {}
    t0 = ts(loop_start)
    ev = [e for e in events if e.get("ts") and ts(e["ts"]) >= t0]
    pods = {}
    for st in (ROOT / "pods").glob("*/loop3/status.json") if (ROOT / "pods").exists() else []:
        s = read_json(st) or {}
        pods[s.get("stage")] = s
    measured_pod = [ (ts(p["finished"]) - ts(p["started"])).total_seconds() / 60
                     for p in pods.values() if p.get("finished") and p.get("started")]
    pod_est = round(sum(measured_pod) / len(measured_pod), 1) if measured_pod else None

    def first(pred, after=None):
        for e in ev:
            if (after is None or ts(e["ts"]) >= after) and pred(e):
                return ts(e["ts"])
        return None

    stages, cursor = [], t0
    design = pods.get("design")
    spans = {}
    spans["design_pod"] = (ts(design["started"]) if design else None, ts(design.get("finished")) if design else None)
    d_end = spans["design_pod"][1]
    dec = first(lambda e: e.get("stage") == "pi_decision", d_end) if d_end else None
    rev = first(lambda e: e.get("stage") == "methodology_review", dec) if dec else None
    spans["design_decision"] = (dec, rev)
    req = first(lambda e: e.get("stage") == "engineering_request")
    built = first(lambda e: e.get("stage") == "build_complete", req) if req else None
    spans["build"] = (req, built)
    run = first(lambda e: e.get("stage") == "experiment_started", built) if built else None
    run_end = None
    if run:
        exp_ev = next(e for e in ev if e.get("stage") == "experiment_started" and ts(e["ts"]) == run)
        exp_id = (exp_ev.get("text", "").split("Started ")[-1].split(" ")[0])
        eta = experiment_eta(exp_id)
        if eta.get("finished"):
            run_end = ts(exp_ev["ts"]) + dt.timedelta(minutes=eta.get("duration_min") or 0)
    spans["pilot"] = (run, run_end)
    for key in ("analysis", "adversarial"):
        p = pods.get(key)
        spans[f"{key}_pod"] = (ts(p["started"]) if p else None, ts(p.get("finished")) if p else None)
    adv_end = spans["adversarial_pod"][1]
    fdec = first(lambda e: e.get("stage") == "pi_decision", adv_end) if adv_end else None
    frev = first(lambda e: e.get("stage") == "methodology_review", fdec) if fdec else None
    spans["final_decision"] = (fdec, frev)

    now = dt.datetime.now()
    projected = None
    for key, label, default, basis in STAGE_DEFAULTS:
        est = default
        b = basis
        if key.endswith("_pod") and pod_est:
            est, b = pod_est, f"measured mean of {len(measured_pod)} loop-3 pod(s)"
        start, end = spans.get(key, (None, None))
        if end:
            status, mins = "done", round((end - start).total_seconds() / 60, 1) if start else None
            projected = end
        elif start:
            status = "running"
            elapsed = (now - start).total_seconds() / 60
            mins = round(elapsed, 1)
            projected = start + dt.timedelta(minutes=max(est, elapsed + 1))
        else:
            status, mins = "pending", None
            base = projected or now
            projected = max(base, now) + dt.timedelta(minutes=est)
        stages.append({"key": key, "label": label, "status": status, "est_min": est, "basis": b,
                       "actual_or_elapsed_min": mins, "start": start.strftime("%H:%M") if start else None,
                       "end": end.strftime("%H:%M") if end else None,
                       "projected_end": projected.strftime("%H:%M") if projected else None})
    return {"started": t0.strftime("%H:%M"), "stages": stages,
            "projected_finish": projected.strftime("%H:%M") if projected else None,
            "remaining_min": round(max((projected - now).total_seconds(), 0) / 60) if projected else None,
            "note": "estimates; pod times switch to measured loop-3 durations once a pod completes"}


def state() -> dict:
    events = [json.loads(l) for l in (ROOT / "timeline.jsonl").read_text().splitlines() if l.strip()]
    decisions = [read_json(p) for p in sorted((ROOT / "decisions").glob("D*.json"))]
    decisions = [d for d in decisions if d]
    pods = []
    for st in sorted((ROOT / "pods").glob("*/*/status.json")) if (ROOT / "pods").exists() else []:
        s = read_json(st) or {}
        syn = read_json(st.parent / "synthesis.json")
        s["synthesis"] = {k: syn.get(k) for k in ("conclusion", "confidence", "recommendation", "analysts_agree")} if syn else None
        pods.append(s)
    exps = []
    for f in sorted((ROOT / "data" / "trials").glob("*.jsonl")):
        if f.name.startswith("_"):
            continue
        t = cli.experiment_timing(f.stem) or {}
        logf = ROOT / "data" / f"{f.stem}.log"
        last = logf.read_text().splitlines()[-1] if logf.exists() and logf.read_text().strip() else ""
        spec = next((read_json(p) for p in ROOT.glob(f"specs/{f.stem}.json")), None)
        planned = len(spec["cells"]) * len(spec["seeds"]) if spec and spec.get("cells") else None
        exps.append({"id": f.stem, "trials": len(f.read_text().splitlines()), "planned": planned,
                     "phase": t.get("phase"), "phase_label": t.get("phase_label"), "last_log": last,
                     "eta": experiment_eta(f.stem)})
    reqs = [e for e in events if e.get("stage") == "engineering_request"]
    builds = [e for e in events if e.get("stage") in ("build_complete", "build_rejected")]
    pending = [r for r in reqs if not any(b["ts"] >= r["ts"] for b in builds)]
    loop_starts = [e for e in events if e.get("stage") == "loop_open" and "LOOP3" in e.get("text", "")]
    return {
        "budget": cli.research_budget(),
        "registry": read_json(ROOT / "registry" / "hypotheses.json"),
        "mandate": read_json(ROOT / "lab" / "mandate.json"),
        "decisions": [{"id": d["id"], "ts": d["ts"], "level": d["level"], "action": d["action"],
                       "confidence": d.get("confidence"), "decision": d["decision"][:400],
                       "alternatives": str(d.get("alternatives_rejected", ""))[:300],
                       "reviews": [{"verdict": r["verdict"], "material": r.get("material_concerns"), "ts": r["ts"]}
                                   for r in d.get("reviews", [])],
                       "human_approval": bool(d.get("human_approval")), "overridden": bool(d.get("overridden"))}
                      for d in decisions],
        "pods": pods, "experiments": exps,
        "pending_engineering": pending,
        "timeline": events[-60:][::-1],
        "loop3_started": loop_starts[-1]["ts"] if loop_starts else None,
        "plan": loop_plan(events, loop_starts[-1]["ts"] if loop_starts else None),
    }


class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        if self.path.startswith("/api/state"):
            body = json.dumps(state(), default=str).encode()
            ctype = "application/json"
        else:
            body = (ROOT / "tracker" / "index.html").read_bytes()
            ctype = "text/html; charset=utf-8"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5210
    print(f"Falsify tracker on http://127.0.0.1:{port}", flush=True)
    ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
