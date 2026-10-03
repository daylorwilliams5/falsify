# Falsify: submission drafts

*Placeholders in [brackets] are filled in once exp011 is analyzed. Fact-check every number against `timeline.jsonl` / `results/` before submitting.*

---

## 1. Project summary (target 150–300 words; this draft is ~245)

**Falsify: an AI research organization that checks its own work.**

As AI systems become teams of agents, a new question matters: when do AI organizations stop correcting themselves, and what oversight brings them back? Falsify is an autonomous research lab, built on Omnigent, that investigates this question by running controlled experiments on AI teams.

The lab is organized like a real scientific institution with separation of powers:
- a **Principal Investigator agent** makes research decisions;
- four **research pods** (literature, design, analysis, adversarial review) argue independently;
- an **independent methodology reviewer** audits every decision;
- the **human** sets the mandate and approves only high-stakes actions.

These authority levels are enforced in code, not just in prompts.

In one day the lab ran [N] experiments and changed course on the evidence each time. Highlights:
- it overturned its own pilot when an adversarial agent **executed a blind script that passed the preregistered validity bar while committing unsafe actions in 20/20 trials**, a bar every human and agent had approved;
- it **found and reported two loopholes in its own governance code instead of exploiting them**;
- it diagnosed that the small subject model's failures were **comparison errors, not unwillingness**, and switched to a more capable model.

Its current experiment asks whether peer deliberation makes agents less corrigible under ambiguous evidence: [one-line exp011 result, stated cautiously].

Falsify shows that autonomous science needs more than more agents. It needs institutions that make agents falsify each other.

---

## 2. Demo video script (60 s)

| Time | On screen | Narration |
|---|---|---|
| 0–8 s | Tracker overview (live pipeline, decisions, estimated finish) | "This is Falsify: an AI research lab that studies how AI organizations fail, and audits itself while it does." |
| 8–20 s | Omnigent UI: PI dispatching pods, sub-agents running | "A Principal Investigator agent runs the science. Four pods of independent agents propose experiments, analyze data and attack every conclusion." |
| 20–32 s | Decision D002 → reviewer FAIL → D003 correction (tracker decision cards) | "Every decision is audited by an independent methodology reviewer. Here the PI overreached; the reviewer failed it; the PI corrected itself, with no human needed." |
| 32–45 s | Adversarial pod output: blind script passes the bar, unsafe 20/20 | "Its adversarial pod ran a script that never reads the environment, and it passed our preregistered validity check. Everyone had approved that check, including us. The lab caught it and changed course." |
| 45–55 s | Approval card in Omnigent, then exp011 results | "Humans approve only what matters: new models, real spending. [exp011 result in one line.]" |
| 55–60 s | Logo / repo URL | "Falsify. Autonomous science that falsifies itself." |

---

## 3. Tech video script (60 s)

| Time | On screen | Narration |
|---|---|---|
| 0–12 s | Architecture diagram (README) | "Stack: Omnigent orchestrates a PI, seven specialists and four pods on Claude. The AI teams under study run on qwen3:8b locally and Claude Haiku 4.5." |
| 12–27 s | `falsify/cli.py` level check + tests | "Authority is enforced in code: a CLI computes each experiment's required level from its spec. Unknown fields fail closed. Specs are hash-locked. Level 3 actions pause on an Omnigent approval card. 90 tests." |
| 27–42 s | Timeline: exp009 livelock → v2.1 → inverted bar → pivot | "What was hard: our instruments failed, twice. The lab diagnosed a livelock, rebuilt the environment, then proved its own validity bar was inverted, using executable counterexamples instead of reading the spec." |
| 42–55 s | Timing phases, review materiality, spend ledger | "Fixes we added on the way: machine-checked timing claims, review-materiality rules to stop review spirals, and a hard spend cap on real API use." |
| 55–60 s | Repo | "Lesson: oversight works when it can execute, not just read." |

---

## 4. One-page report outline (`TeamName_OnePager.pdf`)
- **Challenge:** Databricks × Omnigent, Agentic Scientific Discovery. User: AI safety and agent-systems researchers.
- **Tools:**
  - Omnigent (orchestration, policies, approval gates);
  - Claude (lab agents);
  - qwen3:8b via Ollama and Claude Haiku 4.5 (experimental subjects);
  - Python (environments, analysis, bootstrap CIs).
- **What worked:**
  - separation of powers;
  - adversarial pods with executable checks;
  - authority enforced in code;
  - an append-only research record.
- **What was hard:**
  - instrument validity (livelock; inverted bar);
  - small-model comparison failures;
  - Omnigent one-shot mode stopping sessions;
  - review spirals.
- **How the time was spent:** [timeline summary from timeline.jsonl].
- **Results:**
  - exp001 null;
  - exp009 instrument failure;
  - exp010 inverted bar;
  - exp011 [result].
- **Speedup claim (measured):** [from baseline/manual_loop.jsonl and the loop-quality rubric; state honestly].
- **If we had 24 more hours:** [main run of exp011; replication on a second model family; auditor experiment].
