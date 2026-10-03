# Falsify

> An autonomous scientific lab for understanding AI-agent behavior.

Falsify is a solo project built for the 7th Hack-Nation Global AI Hackathon, Challenge 3: Agentic Scientific Discovery (Databricks × Omnigent).

Most evaluations of AI agents ask whether an agent succeeded.

Falsify asks a different question:

**Why did the agent behave that way, and what intervention would change its behavior?**

Falsify uses Omnigent to run an autonomous scientific organization. The organization reviews prior work, generates hypotheses, designs controlled experiments, runs them, analyzes the results, challenges its own conclusions, and decides what to test next.

The goal is not to produce more agent benchmarks. The goal is to build an empirical science of AI-agent behavior.

---

## Research question

Falsify is currently studying:

**Under what conditions do autonomous AI agents become resistant to correction or sacrifice process integrity, and what forms of oversight restore reliable behavior?**

(The human-set mandate is in [`lab/mandate.json`](lab/mandate.json).)

The lab is particularly interested in behavioral effects caused by:

- performance pressure
- ambiguous corrective evidence
- prior investment
- peer consensus
- organizational structure
- shared history
- independent review

Falsify does not assume these effects exist. It is built to test them experimentally. Each one is a registered hypothesis with a falsification condition in [`registry/hypotheses.json`](registry/hypotheses.json).

---

## Why this matters

AI agents are increasingly asked to operate over long horizons, coordinate with other agents, use tools, and make consequential decisions.

We have many benchmarks for whether those systems complete tasks. We have much less causal understanding of **why their behavior changes**.

An agent can fail because it misunderstood the task. Or because it became anchored to an earlier plan. Or because other agents reinforced that plan. Or because a performance objective rewarded cutting corners.

Those failure modes need different interventions. Falsify is designed to tell them apart experimentally.

---

## How Falsify works

The research loop is:

**Question → Evidence → Hypothesis → Experiment → Result → Challenge → Updated decision**

```
Human researcher            sets the mandate, can override any decision, approves level-3 escalations
      ↓
Omnigent research lab       PI + specialist pods │ independent methodology reviewer
      ↓ PI decision (L1 autonomous · L2 + reviewer PASS · L3 human gate)
Experiment runner           falsify/run.py, `bin/falsify run`
      ↓
Target AI agent(s)          single agent or Planner/Researcher/Executor/Reviewer team, local qwen3:8b,
                            acting in a synthetic, fully controlled environment (FreightRoute)
      ↓
Measured results            data/trials/*.jsonl (immutable) → results/*.json
      ↓
Back to the lab             interpret → challenge → revise hypotheses → choose the next experiment
```

Omnigent coordinates the research organization ([`lab/config.yaml`](lab/config.yaml), [`lab/agents/`](lab/agents/)).

### Principal Investigator

The PI synthesizes evidence, chooses between competing hypotheses, allocates research effort, and decides what the lab tests next. Its authority is bounded by the mandate and by authority levels enforced in code ([`specs/AUTHORITY.md`](specs/AUTHORITY.md)).

### Literature pod

Agents search prior work, identify relevant findings, and look for evidence that contradicts the lab's assumptions ([`sources/`](sources/)).

### Experiment design pod

A lead experimentalist proposes tests. A confound hunter tries to explain why the experiment might produce a misleading result. An information-gain planner compares candidate experiments by what the lab would learn from each one ([`pods/design/`](pods/design/)).

### Analysis pod

A primary analyst evaluates the results. An independent analyst runs a separate analysis without seeing the first analyst's implementation. A robustness auditor looks for alternative explanations. If the analysts disagree, the CLI refuses to mark a hypothesis supported or falsified until the discrepancy is resolved.

### Adversarial pod

A skeptic, a null advocate and an adversarial confound hunter try to falsify the lab's interpretation before the PI can treat a hypothesis as supported ([`critiques/`](critiques/)).

### Independent methodology reviewer

A separate reviewer audits every PI decision and checks that conclusions are supported by the experiment that was actually run. The PI may not ignore a FAIL. In practice the reviewer has already failed two PI decisions, and the PI recorded a correction for each ([`decisions/`](decisions/)).

---

## The lab does not assume its own agents are trustworthy

Falsify is itself an agentic system studying agentic systems. That makes reliability part of the experiment.

The lab therefore separates:

- generation from evaluation
- experiment execution from interpretation
- scientific authority from methodology review
- raw observations from later conclusions

Raw trial data in `data/trials/` is never edited. Interpretations live in `critiques/` and must cite result IDs. Every decision is recorded in `decisions/` and in the append-only `timeline.jsonl` before it is acted on.

Disagreements between researchers are preserved, not silently averaged away.

The PI cannot redefine a failed experiment as a successful one: changing a primary outcome or exclusion criterion after results exist is a level-3 action that requires the human.

---

## What happened during the first research loops

**Loop 1: the first hypothesis did not survive testing.** H1 predicted that more prior investment in a plan would make agents more resistant to abandoning it once it was shown to be invalid ([`exp001_pilot`](results/exp001_pilot.json), 40 trials).

It did not produce the expected effect. Under clear contradictory evidence, 18 of 20 agents switched course immediately, and the interaction estimate was Δ = 0.0, 95% CI [−1.6, 1.6]. The skeptic then showed from the transcripts that the two non-switching trials were route-attribution errors, not persistence.

The lab recorded H1 as inconclusive (a floor effect that the measure could not separate from a reference error) rather than manufacturing a result.

**Loop 2: the instrument failed.** The second experiment ([`exp009`](results/exp009_v2_floor_probe_memo.md), 20 trials) asked whether operational pressure made agents skip a required verification step.

That experiment also failed, for a different reason: the environment was not a valid measurement instrument. Its VERIFY action re-inspected the same route segment indefinitely and returned identical text, so 13 of 20 agents never booked a route at all. Across all trials, 236 of 300 actions were the same repeated check. The primary outcome was undefined for most trials ([`decisions/D011.json`](decisions/D011.json)).

The environment also lacked any honest way to report that the task couldn't be done safely, so part of the integrity dilemma it posed was manufactured by the action space.

Falsify stopped, made no hypothesis status changes, and redesigned the instrument. The human set a stopping rule: FreightRoute v2.1 gets one pilot. If it still can't tell a chosen shortcut from a forced one, the environment is dropped and the lab pivots.

This is intentional. A failed experiment is preferable to a false discovery.

---

## Current experiment

**exp010: FreightRoute v2.1 instrument validation**

Question:

> Can the rebuilt environment tell a violation the agent *chose* from one the environment forced, and is the primary outcome defined for most trials?

Manipulation:

> Action budget (24 / 14) × performance target (ordinary / target), single agent, 5 seeds per cell (20 trials).

Primary outcome:

> Fraction of trials in which the primary outcome is defined, against a pre-registered validity threshold. The behavioral outcomes (verification rate, process violations, unsupported claims) are reported descriptively only.

Current result:

> Experiment pending the PI decision and methodology review.

---

## Final finding

> **[INSERT FINAL RESULT HERE]**

If the experiment does not support the hypothesis, the final result will say so.

---

## What makes Falsify different

Falsify is not a multi-agent chat room. It is a scientific organization.

Agents have differentiated roles, independent information, explicit decision authority, structured research artifacts, and adversarial review.

Most importantly, experimental results change what the lab does next. A failed hypothesis is not the end of the workflow. It becomes evidence for the next experiment.

---

## Run it

Requirements: Python 3.12+ with [`uv`](https://docs.astral.sh/uv/), [Ollama](https://ollama.com) with `qwen3:8b`, [Omnigent](https://omnigent.ai) (`uv tool install omnigent`), tmux, and Node for the UI.

```bash
uv sync                                   # Python dependencies
ollama pull qwen3:8b
OLLAMA_NUM_PARALLEL=4 ollama serve        # parallel slots for the runner
uv run pytest -q tests                    # environment integrity tests
bin/falsify run specs/exp001_pilot.json   # run an experiment in the background
bin/falsify status exp001_pilot
bin/falsify analyze exp001_pilot          # → results/exp001_pilot.json + plot
omnigent run lab -p "Run the next research loop."   # the Omnigent research lab
npm --prefix ui install && npm --prefix ui run dev  # public demo at http://localhost:5199
```

The public demo is a single page at `#/`. "See the lab working" opens the internal views: decisions, reviewer verdicts, the timeline and the experiments.

---

## Built with

- Omnigent (research organization; PI and pods on the Claude SDK harness)
- Python
- a local subject model (`qwen3:8b` via Ollama)
- synthetic, fully controlled experiment environments
- append-only research logs and immutable trial data
- independent analysis and review agents
- React + Vite for the demo

Built solo in 24 hours.

---

## Repository structure

```text
falsify/
├── falsify/           # environments (env.py, env2.py), target organizations, runner, analysis, CLI
├── lab/               # research mandate + Omnigent PI config; lab/agents/ = specialist configs
├── pods/              # outputs of the multi-agent research pods
├── specs/             # protocols, preregistrations, policies, experiment specs (candidates/ = lab proposals)
├── registry/          # hypotheses and their statuses
├── data/trials/       # raw trial records (immutable)
├── results/           # measured analyses and plots
├── critiques/         # specialist and reviewer interpretations
├── decisions/         # PI decision records with reviews and human actions
├── sources/           # candidate literature
├── timeline.jsonl     # append-only research record
├── tracker/           # internal live research tracker
└── ui/                # public research demo
```

---

## Philosophy

Scientific agents should not be optimized to find something interesting.

They should be optimized to find out whether it is true.

That is Falsify.
