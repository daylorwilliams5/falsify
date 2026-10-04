# Falsify: submission drafts

*Numbers are from `results/exp012_*.json` and `results/exp013t_*.json`. Fact-check every number against `timeline.jsonl` / `results/` before submitting.*

---

## 1. Project summary (paste into the form; ~280 words)

**Falsify: an AI research lab that checks its own work.**

AI agents increasingly work in teams, but we mostly measure whether they succeed, not *why* they stop correcting themselves. Falsify is an autonomous research lab, built on Omnigent, that runs controlled experiments to find out.

**It is organized like a scientific institution, with separation of powers enforced in code:**
- a Principal Investigator agent decides what to test next;
- four research pods (literature, design, analysis, adversarial) argue independently;
- an independent methodology reviewer audits every decision;
- the human approves only high-stakes actions, through Omnigent approval cards.

**In one day the lab ran 6 experiments and changed course on evidence each time.** It also caught its own mistakes:
- an adversarial agent executed a blind script that passed the preregistered validity bar while acting unsafely in 20/20 trials;
- agents reported loopholes in their own governance code instead of exploiting them;
- the reviewer blocked a run over a silent $8,000 bug in the engineer's code.

**What it found about Claude Haiku 4.5:**
- Given ambiguous evidence that its plan was wrong, it checked before acting in 60/60 trials, alone or in teams (95% upper bound on persisting: 4.9%).
- When colleagues simply advised "skip the inspection", checking fell from 100% to 70% (−30 points, 95% CI −13 to −47).
- Making the check cost time had no effect.
- Those that skipped deferred to their colleagues. The advice was safe, so whether they would follow unsafe advice is untested.

**Who benefits:** AI-safety researchers and teams deploying multi-agent systems, who get causal, reproducible evidence about when oversight works. Every decision, review and trial is on the record.

Autonomous science needs more than more agents. It needs institutions that make agents falsify each other.

Live: https://falsify-nine.vercel.app · Code: https://github.com/daylorwilliams5/falsify

---

## 2. Demo video: hits the challenge's six beats (question, handoffs, experiment, result, learned, next)

Open these tabs first: **falsify-nine.vercel.app**, the **Omnigent UI** (127.0.0.1:6767), and **falsify-nine.vercel.app/#/timeline**.

| Time | Beat | On screen | Say |
|---|---|---|---|
| 0–8 s | **Question** | Live site front page | "Falsify is an autonomous research lab. Its question: when do AI agents stop correcting themselves, and what brings them back?" |
| 8–22 s | **Agent handoffs** | Omnigent UI: scroll the conversation where the PI sends work to the design pod, the pod reports back, and the reviewer responds | "A lead scientist agent hands the question to a design team. Their critic tears the design apart, and an independent reviewer audits the decision. I only approve the big moves." |
| 22–32 s | **Experiment** | Site: the "What we're testing" box (exp013) | "The experiment: an AI agent gets ambiguous evidence that its route is unsafe. We vary whether checking costs time, and whether colleagues tell it to skip the check." |
| 32–44 s | **Result** | Site: the 2×2 grid, 21/30 | "When colleagues were silent, it checked every time. When they said 'skip it', checking dropped to 70%. Making checking cost time changed nothing." |
| 44–53 s | **What the lab learned** | Timeline: the D020 BLOCK → D021 → D023 correction | "The lab also caught its own mistakes. The reviewer ran my code, found a hidden $8,000 bug and blocked the run. Later it removed a safety claim the data couldn't support." |
| 53–60 s | **Next** | Site: "What the lab is doing next" | "Next: the same colleagues recommending the unsafe route. Do agents still defer?" |

*If the platform accepts a 2-minute demo, slow each beat down and add one Omnigent approval-card click. The form's limit is 60 s.*

---

## 3. Tech video (≤60 s)

| Time | Section | On screen | Say |
|---|---|---|---|
| 0–13 s | **Stack** | README architecture diagram | "Omnigent orchestrates a PI agent, four pods and an independent reviewer, all on Claude. The AI agents under study run on qwen3 locally and Claude Haiku through the API, inside simulated freight-routing environments we built in Python." |
| 13–30 s | **Highlights** | `bin/falsify level` output; `tests/` | "The clever part is that authority lives in code, not prompts. A CLI computes each experiment's authority level from its spec. Specs are hash-locked. Unknown settings fail closed. Level-3 actions wait for an Omnigent approval card. Every validity check is tested against scripts that don't read the environment: 129 tests." |
| 30–52 s | **Challenges** | Timeline: exp009 livelock → inverted bar → $8,000 block | "What broke: our first environment livelocked. Our validity bar turned out to be inverted: a blind script passed it. And a silent default in my own code would have contaminated a run, until the reviewer executed it and blocked it. Each time, the fix was to make oversight execute instead of read." |
| 52–60 s | **Takeaway** | Repo | "Lesson: oversight works when it can run the code, not just review the summary." |

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
- **How the time was spent:** 6 experiments, 21 PI decisions, every one independently reviewed; about $6 of API spend in total (`data/spend_ledger.jsonl`).
- **Results:**
  - exp001 null;
  - exp009 instrument failure;
  - exp010 inverted bar;
  - exp011 pilot: no persistence in any of 30 trials; comprehension gate passed; peers never disagreed (check 4), so peer pressure is untested.
  - exp012 main run (90 trials): 0 persistence. Clear evidence → switch 30/30; ambiguous → inspect first 60/60. Upper bounds: 4.9% ambiguous-only, 18.1% per cell.
  - exp013t (60 trials):
    - **an advisory majority cut verification from 100% to 70%** (−30 pts, CI −13 to −47);
    - time cost had no effect;
    - no safety claim: the design could not produce an unsafe outcome (tripwire, D023);
    - all manipulation checks passed.
- **Speedup claim (measured):** result-to-decision time 60 min (Loop 1) → 6–11 min (Loops 4–5), about 6–10×, with more review per result. Not measured against a conventional lab; the remaining bottleneck is question → valid experiment (56 min for exp013).
- **If we had 24 more hours:** the same advisory majority recommending the UNSAFE route (does deference stay safe?); strong prior commitment; live peers who actually disagree; replication on a second model family.
