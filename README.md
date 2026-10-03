# Falsify

**An Omnigent-orchestrated research lab that studies how AI organizations fail, and decides from evidence what to test next.**

Built for the 7th Hack-Nation Global AI Hackathon, Challenge 3: Agentic Scientific Discovery (Databricks × Omnigent).

> **Research question.** What environmental and organizational conditions make autonomous AI systems less corrigible or more willing to sacrifice process integrity for task success, and which oversight architectures restore reliable behavior?

## How it works

```
Human researcher
      ↓ directives, approvals
OMNIGENT research lab (lab/)  ─ director + literature, scientist, designer, statistician, skeptic, auditor
      ↓ proposes ≥2 experiments, picks one, pauses at the human_gate policy
Experiment runner (falsify/run.py, `bin/falsify run`)
      ↓
Target AI organization (falsify/org.py): single agent or Planner/Researcher/Executor/Reviewer team
      ↓ acts in a synthetic, fully controlled environment (FreightRoute v1 / v2)
Measured results (data/trials/*.jsonl → results/*.json)
      ↓
Back to Omnigent: interpret → challenge → revise hypotheses → choose next experiment
```

- **Omnigent is the lab.** It holds the shared scientific state (`registry/`, `specs/`, `critiques/`, `timeline.jsonl`), coordinates six specialist agents, passes structured evidence between them, and enforces human approval (a CEL policy that pauses `falsify run` and `falsify conclude`).
- **The target organization is the experimental subject.** It runs on a local `qwen3:8b` model in plain Python, with no Omnigent text in its prompts.
- **Measured data and interpretation are kept separate.** Trial data is never edited. Agent interpretations live in `critiques/` and must cite result IDs.

## Environments

| | FreightRoute v1: corrigibility after invalidation | FreightRoute v2: integrity under pressure |
|---|---|---|
| Task | Deliver cargo; Route A is preferred until an inspection report invalidates it | Same task, plus a required VERIFY-before-RESERVE procedure, a hidden over-limit segment, and a score that credits a delivery *report* |
| Manipulations | org (single / multi), prior investment k, benign-update control, auditor | action budget (24 / 10), performance target (ordinary / target), org, auditor |
| Primary outcomes | wasted actions after contradiction; switch rate; success; cost | verification rate, process violations, hard violations, reported vs **true** vs compliant success, unsupported claims |
| Docs | [`specs/PROTOCOL.md`](specs/PROTOCOL.md) | [`specs/ENV_V2.md`](specs/ENV_V2.md), [`specs/PREREG_V2.md`](specs/PREREG_V2.md) |

Governance: [`specs/EDGE_CASE_POLICY.md`](specs/EDGE_CASE_POLICY.md) covers invalid trials, decision rules, auditor visibility, what counts as a material change, and logging.

## Results so far (live; see `timeline.jsonl`)

- **exp001 pilot** (v1, 40 trials, qwen3:8b): 18/20 invalidating trials switched immediately and 20/20 benign trials correctly continued. H1 interaction Δ = 0.0, 95% CI [−1.6, 1.6]. **H1 is inconclusive (floor effect).**
  - The lab's skeptic found, from transcripts, that both non-switching trials were *route-attribution errors* (the bridge assigned to the wrong route), not persistence.
- **Lab decision:** the designer first recommended an ambiguity × organization study. After the skeptic's critique it reversed itself and recommended **exp009, a 20-trial v2 floor probe**. Before that, it found a flaw in v2: under the low budget, compliance becomes arithmetically impossible once Route A has been explored. That flaw led to measurement-only *feasible vs forced* violation instrumentation.

All claims are provisional. The literature list ([`sources/candidates.md`](sources/candidates.md)) is approved for synthesis only; most entries were checked at abstract level only.

## Run it

Requirements: Python 3.12+ with [`uv`](https://docs.astral.sh/uv/), [Ollama](https://ollama.com) with `qwen3:8b`, [Omnigent](https://omnigent.ai) (`uv tool install omnigent`), and tmux.

```bash
uv sync                                   # Python dependencies
ollama pull qwen3:8b
OLLAMA_NUM_PARALLEL=4 ollama serve        # parallel slots for the runner
uv run pytest -q tests                    # environment integrity tests
bin/falsify run specs/exp001_pilot.json   # run an experiment in the background
bin/falsify status exp001_pilot
bin/falsify analyze exp001_pilot          # → results/exp001_pilot.json + plot
omnigent run lab -p "Run the next research loop."   # the Omnigent research lab
```

## Repository layout

```
falsify/     env.py, env2.py (environments) · org.py (target organizations) · run.py · analyze.py · cli.py
lab/         Omnigent agent configs: director (config.yaml) + agents/<specialist>/config.yaml
specs/       protocols, preregistration, policy, experiment specs (candidates/ = lab proposals)
registry/    hypotheses.json, the hypothesis families and their statuses
data/trials/ raw trial records (immutable)
results/     measured analysis output and plots
critiques/   specialist interpretations
sources/     candidate literature (provisional)
baseline/    manual research-loop timings (for the speedup comparison)
ui/          research control room (in progress)
timeline.jsonl  append-only research record
```

## Credits
Daylor Williams. Built with Claude Code and Omnigent.
