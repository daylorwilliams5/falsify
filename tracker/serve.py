"""Falsify research tracker: a read-only live view of the lab's state.

Usage: uv run python tracker/serve.py  (http://127.0.0.1:5210)
Reads only the lab's own files; never writes.
"""
import json
import pathlib
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
                     "phase": t.get("phase"), "phase_label": t.get("phase_label"), "last_log": last})
    reqs = [e for e in events if e.get("stage") == "engineering_request"]
    builds = [e for e in events if e.get("stage") in ("build_complete", "build_rejected")]
    pending = [r for r in reqs if not any(b["ts"] >= r["ts"] for b in builds)]
    loop_starts = [e for e in events if e.get("stage") in ("directive",) and "Loop 3" in e.get("text", "")]
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
