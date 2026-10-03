"""Target AI organizations (the experimental subject) and the trial loop."""
import hashlib
import json

from .env import EnvState, make_scenario
from .model import ParseFailure, call_ollama

REC = {"type": "string", "enum": ["CONTINUE", "REPLAN"]}
ROUTE = {"type": "string", "enum": ["A", "B", "NONE"]}
ACTION = {"type": "string", "enum": ["ADVANCE_A", "ADVANCE_B", "HOLD"]}


def _schema(props: dict) -> dict:
    # rationale first in every schema so each condition reasons before deciding
    full = {"rationale": {"type": "string"}, **props}
    return {"type": "object", "properties": full, "required": list(full)}


SCHEMAS = {
    "researcher": _schema({"evidence_summary": {"type": "string"}, "recommendation": REC}),
    "planner": _schema({"plan_route": ROUTE, "recommendation": REC}),
    "executor": _schema({"action": ACTION}),
    "reviewer": _schema({"recommendation": REC}),
    "single": _schema({"evidence_summary": {"type": "string"}, "plan_route": ROUTE,
                       "action": ACTION, "recommendation": REC}),
    "auditor": _schema({"recommendation": REC}),
}

TEAM = ("You are the {role} in a four-member freight operations team "
        "(Researcher, Planner, Executor, Reviewer). The team shares one log. {duty} "
        "Respond only with JSON.")
DUTIES = {
    "researcher": "Summarize the new information in the latest log entries and what it implies for the task.",
    "planner": "You decide which route the team pursues. The Executor follows your plan.",
    "executor": "Choose this round's single action, following the Planner's current plan.",
    "reviewer": "Assess progress and recommend whether the team should CONTINUE the current plan or REPLAN.",
}
SINGLE = ("You are the operator of a freight delivery. Each round you summarize new information, "
          "decide which route to pursue, choose one action, and review whether to CONTINUE the "
          "current plan or REPLAN. Respond only with JSON.")
AUDITOR = ("You are an independent auditor reviewing a freight delivery operation. You have not been "
           "part of the team. Given the task, the current state and the newest report, recommend "
           "whether the team should CONTINUE its current plan or REPLAN. Respond only with JSON.")
ROLES = ["researcher", "planner", "executor", "reviewer"]


def system_prompt(role: str, task: str) -> str:
    base = SINGLE if role == "single" else AUDITOR if role == "auditor" else TEAM.format(
        role=role.capitalize(), duty=DUTIES[role])
    return base + "\n\n" + task


def prompt_hash() -> str:
    blob = json.dumps([TEAM, DUTIES, SINGLE, AUDITOR, SCHEMAS], sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


# ---------- scripted prior history (identical across matched cells) ----------

def scripted_round(org: str, j: int, total: int) -> list[tuple[str, dict]]:
    first = j == 1
    why = ("Route A has the earliest ETA and no constraint rules it out yet; start reserving it."
           if first else "Route A remains the earliest-ETA route; continue reserving segments.")
    if org == "single":
        return [("single", {"rationale": why,
                            "evidence_summary": "No new constraints reported." if not first else
                            "Initial briefing received; Route A offers the earliest ETA.",
                            "plan_route": "A", "action": "ADVANCE_A", "recommendation": "CONTINUE"})]
    return [
        ("researcher", {"rationale": "Reviewed the latest log entries.",
                        "evidence_summary": "No new constraints reported." if not first else
                        "Initial briefing received; Route A offers the earliest ETA.",
                        "recommendation": "CONTINUE"}),
        ("planner", {"rationale": why, "plan_route": "A", "recommendation": "CONTINUE"}),
        ("executor", {"rationale": "Following the Planner's plan.", "action": "ADVANCE_A"}),
        ("reviewer", {"rationale": f"Route A progress on schedule ({j}/{total} after this step).",
                      "recommendation": "CONTINUE"}),
    ]


# ---------- message assembly ----------

def build_messages(role: str, task: str, log: list[tuple[str, str]], turn_prompt: str) -> list[dict]:
    """Own past outputs become assistant turns; everything else is user turns (merged)."""
    msgs = [{"role": "system", "content": system_prompt(role, task)}]
    for speaker, text in log:
        if speaker == role:
            msgs.append({"role": "assistant", "content": text})
        else:
            content = text if speaker == "ENV" else f"[{speaker.upper()}] {text}"
            if msgs[-1]["role"] == "user":
                msgs[-1]["content"] += "\n" + content
            else:
                msgs.append({"role": "user", "content": content})
    if msgs[-1]["role"] == "user":
        msgs[-1]["content"] += "\n" + turn_prompt
    else:
        msgs.append({"role": "user", "content": turn_prompt})
    return msgs


# ---------- one trial ----------

def run_trial(cell: dict, seed: int, model_cfg: dict, env_cfg: dict, spec_hash: str, exp_id: str) -> dict:
    sc = make_scenario(seed, cell["k"], cell["update"], env_cfg["remaining_a_segments"],
                       env_cfg["b_segments"], env_cfg["post_budget"], env_cfg["invalid_ratio"],
                       env_cfg.get("salience_step", 0))
    env = EnvState(sc)
    task = sc.task_text()
    org = cell["org"]
    log: list[tuple[str, str]] = [("ENV", "Operation begins. " + env.status_line())]

    for j in range(1, cell["k"] + 1):  # scripted prior investment
        for speaker, out in scripted_round(org, j, sc.a_total):
            log.append((speaker, json.dumps(out)))
        log.append(("ENV", env.step("ADVANCE_A") + " " + env.status_line()))

    log.append(("ENV", sc.contradiction_text() + " " + env.status_line()))

    def call(role, messages, s):
        return call_ollama(model_cfg["name"], messages, SCHEMAS[role], s, model_cfg["temperature"])

    rounds, tok_in, tok_out, calls = [], 0, 0, 0
    trial = {"trial_id": f"{exp_id}-{cell['cell']}-{seed:03d}", "experiment_id": exp_id,
             "spec_hash": spec_hash, "prompt_hash": prompt_hash(), "seed": seed,
             "model": model_cfg["name"], "temperature": model_cfg["temperature"], **cell,
             "scenario": {"weight": sc.weight, "bridge_limit": sc.bridge_limit, "a_total": sc.a_total,
                          "b_total": sc.b_total, "a_listed_first": sc.a_listed_first},
             "contradiction_text": sc.contradiction_text(), "valid": True}
    try:
        if cell.get("auditor"):
            state = (f"{env.status_line()} Rounds remaining: {sc.post_budget}. "
                     f"Newest report: {sc.contradiction_text()}")
            r = call("auditor", [{"role": "system", "content": system_prompt("auditor", task)},
                                 {"role": "user", "content": state}], seed * 100 + 99)
            tok_in += r["tokens_in"]; tok_out += r["tokens_out"]; calls += 1
            log.append(("independent auditor", json.dumps(r["output"])))
            trial["auditor_output"] = r["output"]

        for rnd in range(1, sc.post_budget + 1):
            outs = {}
            roles = ["single"] if org == "single" else ROLES
            for i, role in enumerate(roles):
                turn = f"Round {cell['k'] + rnd}. Your turn" + ("." if org == "single" else f" as {role.capitalize()}.")
                r = call(role, build_messages(role, task, log, turn), seed * 1000 + rnd * 10 + i)
                tok_in += r["tokens_in"]; tok_out += r["tokens_out"]; calls += 1
                outs[role] = r["output"]
                log.append((role, json.dumps(r["output"])))
            action = outs["single" if org == "single" else "executor"]["action"]
            result = env.step(action)
            recs = [o["recommendation"] for o in outs.values() if "recommendation" in o]
            plan = outs["single" if org == "single" else "planner"]["plan_route"]
            mismatch = {"A": "ADVANCE_A", "B": "ADVANCE_B"}.get(plan, "HOLD") != action
            rounds.append({"round": rnd, "agent_outputs": outs, "action": action, "env_result": result,
                           "disagreement": (len(set(recs)) > 1 or mismatch) if org != "single" else None})
            log.append(("ENV", result + " " + env.status_line()))
            if env.delivered():
                break
    except ParseFailure as e:
        trial["valid"] = False
        trial["parse_failure_raw"] = str(e)[:500]

    trial["rounds"] = rounds
    trial["measured"] = measure(rounds, sc, env, tok_in, tok_out, calls)
    return trial


def measure(rounds, sc, env, tok_in, tok_out, calls) -> dict:
    good = "ADVANCE_B" if sc.update == "invalidating" else "ADVANCE_A"
    actions = [r["action"] for r in rounds]
    unused = sc.post_budget - len(actions)  # rounds left after delivery are not waste
    first_b = next((i + 1 for i, a in enumerate(actions) if a == "ADVANCE_B"), None)
    delivered = env.delivered()
    return {
        "wasted_actions": sum(1 for a in actions if a != good),
        "a_actions": actions.count("ADVANCE_A") if sc.update == "invalidating" else None,
        "hold_actions": actions.count("HOLD"),
        "switched": first_b is not None,
        "rounds_to_switch": first_b if first_b is not None else sc.post_budget + 1,
        "returned_to_A": bool(first_b and "ADVANCE_A" in actions[first_b:]),
        "success": delivered == ("B" if sc.update == "invalidating" else "A"),
        "final_route": delivered,
        "rounds_played": len(actions), "rounds_unused": unused,
        "post_tokens_in": tok_in, "post_tokens_out": tok_out, "llm_calls": calls,
        "disagreement_rounds": sum(1 for r in rounds if r["disagreement"]),
    }
