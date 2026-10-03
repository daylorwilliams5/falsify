"""`falsify` CLI: the tools the Omnigent research lab uses.

  falsify run SPEC            start an experiment in the background (approval-gated in Omnigent)
  falsify status EXP          progress of a running/finished experiment
  falsify analyze EXP         compute measured results -> results/EXP.json
  falsify hypotheses          print the hypothesis registry
  falsify conclude ID STATUS --evidence RESULT_ID --note TEXT   (approval-gated)
  falsify log AGENT STAGE TEXT [--cites ID ...]                 append to timeline.jsonl

Every write is append-only or recorded in timeline.jsonl, so the research record is reconstructable.
"""
import argparse
import datetime
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TIMELINE = ROOT / "timeline.jsonl"
REGISTRY = ROOT / "registry" / "hypotheses.json"
STATUSES = {"supported", "falsified", "inconclusive", "needs replication", "untested"}


def now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def log_event(agent: str, stage: str, text: str, cites=None, **extra) -> dict:
    ev = {"ts": now(), "agent": agent, "stage": stage, "text": text, "cites": cites or [], **extra}
    with TIMELINE.open("a") as f:
        f.write(json.dumps(ev) + "\n")
    return ev


def cmd_run(a):
    spec_path = pathlib.Path(a.spec)
    spec = json.loads(spec_path.read_text())
    exp = spec["experiment_id"]
    logf = ROOT / "data" / f"{exp}.log"
    proc = subprocess.Popen([sys.executable, "-m", "falsify.run", str(spec_path)], cwd=ROOT,
                            stdout=logf.open("a"), stderr=subprocess.STDOUT, start_new_session=True)
    log_event("runner", "experiment_started", f"Started {exp} (pid {proc.pid})", cites=[str(spec_path)])
    print(json.dumps({"started": exp, "pid": proc.pid, "log": str(logf),
                      "trials_planned": len(spec["cells"]) * len(spec["seeds"])}))


def cmd_status(a):
    trials = ROOT / "data" / "trials" / f"{a.exp}.jsonl"
    done = len(trials.read_text().splitlines()) if trials.exists() else 0
    logf = ROOT / "data" / f"{a.exp}.log"
    tail = logf.read_text().splitlines()[-1] if logf.exists() else ""
    print(json.dumps({"experiment": a.exp, "trials_written": done, "finished": tail.startswith("DONE"),
                      "last_log_line": tail}))


def cmd_analyze(a):
    subprocess.run([sys.executable, "-m", "falsify.analyze", a.exp], cwd=ROOT, check=True)
    log_event("statistician-tool", "analysis_written", f"results/{a.exp}.json", cites=[a.exp])


def cmd_hypotheses(a):
    print(REGISTRY.read_text())


def cmd_conclude(a):
    if a.status not in STATUSES:
        sys.exit(f"status must be one of {sorted(STATUSES)}")
    reg = json.loads(REGISTRY.read_text())
    h = next((h for h in reg["hypotheses"] if h["id"] == a.id), None)
    if h is None:
        sys.exit(f"unknown hypothesis {a.id}")
    old = h["status"]
    h["status"] = a.status
    h.setdefault("history", []).append({"ts": now(), "from": old, "to": a.status,
                                        "evidence": a.evidence, "note": a.note})
    if a.evidence and a.evidence not in h["tested_by"]:
        h["tested_by"].append(a.evidence)
    REGISTRY.write_text(json.dumps(reg, indent=2))
    log_event("director", "status_change", f"{a.id}: {old} -> {a.status}. {a.note}", cites=[a.evidence])
    print(f"{a.id}: {old} -> {a.status}")


def cmd_log(a):
    print(json.dumps(log_event(a.agent, a.stage, a.text, a.cites)))


def main():
    p = argparse.ArgumentParser(prog="falsify")
    sub = p.add_subparsers(required=True)
    s = sub.add_parser("run"); s.add_argument("spec"); s.set_defaults(f=cmd_run)
    s = sub.add_parser("status"); s.add_argument("exp"); s.set_defaults(f=cmd_status)
    s = sub.add_parser("analyze"); s.add_argument("exp"); s.set_defaults(f=cmd_analyze)
    s = sub.add_parser("hypotheses"); s.set_defaults(f=cmd_hypotheses)
    s = sub.add_parser("conclude"); s.add_argument("id"); s.add_argument("status")
    s.add_argument("--evidence", required=True); s.add_argument("--note", required=True)
    s.set_defaults(f=cmd_conclude)
    s = sub.add_parser("log"); s.add_argument("agent"); s.add_argument("stage"); s.add_argument("text")
    s.add_argument("--cites", nargs="*"); s.set_defaults(f=cmd_log)
    a = p.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
