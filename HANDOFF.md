# Falsify: handoff

*Last updated: 2026-10-03, ~15:55 PDT. If you're a new Claude Code session: read this whole file first, then `timeline.jsonl` (last ~30 lines) and `decisions/` (newest first).*

## What this is
Hackathon project for **Hack-Nation 7th Global AI Hackathon, Challenge 3 (Databricks × Omnigent, Agentic Scientific Discovery)**. The event runs Oct 3–4, 2026; check the official deadline.
- **Repo:** https://github.com/daylorwilliams5/falsify (public). Local: `~/Documents/falsify`.
- **What it does:** an Omnigent-orchestrated AI research lab that studies when AI organizations resist correction or sacrifice process integrity, and decides from evidence what to test next.
- **Mandate (research question):** `lab/mandate.json`.

## Architecture (see README.md, specs/AUTHORITY.md)
- **Human:** sets the mandate, can override any decision, approves Level 3 escalations (an Omnigent approval card).
- **PI agent** (`lab/config.yaml`): makes the scientific decisions and records them in `decisions/D*.json`.
- **Methodology reviewer** (`lab/agents/reviewer`): audits every decision. Verdicts are PASS / PASS_WITH_NOTE / CONCERNS(+material count) / BLOCK / ESCALATE.
- **Four pods:** literature, design (designer), analysis (statistician), adversarial (skeptic). Each has 2 sub-agents and produces `pods/<stage>/<loop>/synthesis.json`.
- **Authority levels are enforced in `falsify/cli.py`** (`bin/falsify level/decide/review/escalate/run/conclude`), with 87 tests.
  - L1: PI acts alone.
  - L2: needs a reviewer PASS.
  - L3: needs the human gate.
  - Non-mandated models, unknown fields, outcome declarations and spec edits after a decision all fail closed.
- **Subject (the AI organization being studied):** `falsify/org.py`, with environments `env.py` (v1 route switching), `env2.py` (v2.1 process integrity) and `env3.py` (FreightRoute-E: ambiguous evidence × peers).

## Results so far (all in timeline.jsonl / results/)
1. **exp001** (v1, qwen3:8b, 40 trials): floor effect. Prior investment didn't cause persistence. **H1 = inconclusive.** The two failures were route-attribution errors.
2. **exp009** (v2 probe): **the instrument failed** (VERIFY livelock; 13/20 trials made zero reservations).
3. **exp010** (v2.1 pilot, 20 trials): mechanically passed V1–V5, but **the lab then showed the bar was inverted.** A blind fixed script passes it while committing unsafe claims 20/20, and fully compliant scripts fail it. Also, **qwen3:8b makes numeric comparison errors in both directions**, so integrity metrics mix up unwillingness with incapacity. Conclusion: FreightRoute v2.1 + qwen can't answer the willingness question.
4. **System-level findings (strong demo material):**
   - the agents found 2 governance loopholes in the CLI and reported them instead of exploiting them;
   - the reviewer caught a false "pre-data" timing claim against the raw logs;
   - the pods corrected the PI 4+ times on code-level facts;
   - the adversarial pod caught an inverted validity bar that everyone (including the human and the engineer) had approved.

## Where Loop 3 is right now
- **Loop 3** (first pod-based loop) is finishing: the adversarial pod synthesis, then the PI's **keep-or-kill decision for FreightRoute.** The human directive is to pivot unless a non-obvious signal survives; it didn't (it was a comparison failure).
- **Mandate exception recorded** (lab/mandate.json approved_exceptions): Haiku 4.5 approved for the ambiguity × peer family only, $20 cap.
- **Next experiment, READY and merged:** `specs/candidates/exp011_ambiguity_x_peer_haiku_pilot.json`.
  - **Question:** does social reinforcement make agents less corrigible under ambiguous evidence?
  - **Design:** single vs 4 peers (blind → see others → vote, tie = HOLD) × clear / probabilistic / conflicting evidence.
  - **Subject:** **Claude Haiku 4.5** (human approved in chat, about $3, hard cap $20).
  - **Level 3**, so it needs: PI decision → reviewer → `bin/falsify escalate` → **the human approves the card in the Omnigent UI** → `bin/falsify run`.
  - Draft prereg: `specs/PREREG_E_DRAFT.md`.
- **Human directives in force:** see `timeline.jsonl` entries with `agent: human` (pivot plan, incentive validity, review materiality, timing claims, edge-case policy, architecture).

## How to run / operate
| What | Command / location |
|---|---|
| Lab (PI + pods), live | `tmux attach -t falsify` (detach: Ctrl-B, D; **don't Ctrl-C**). It runs `bin/lab-supervisor 370ac29f0ec845bcafc42d041bc82502` |
| Omnigent web UI | http://127.0.0.1:6767/c/370ac29f0ec845bcafc42d041bc82502 (approval cards appear here) |
| Research tracker | http://127.0.0.1:5210. Restart with `uv run python tracker/serve.py 5210` |
| Send the PI a message | type into the tmux REPL, or the web UI message box |
| Keep the Mac awake | `caffeinate -dims` (stop with Ctrl-C) |
| Tests | `uv run pytest -q tests` (87 should pass) |
| Validate the lab spec before launch | `bin/check-lab` |
| Budget / spend | `bin/falsify budget` (Haiku spend comes from `data/spend_ledger.jsonl`) |
| Experiment status | `bin/falsify status <exp>`; logs in `data/<exp>.log` |
| Local model server | `OLLAMA_NUM_PARALLEL=4 ollama serve` (qwen3:8b) |

**API key:** in `~/Documents/falsify/.env` as `ANTHROPIC_API_KEY=...`. **It's git-ignored; never commit or print it.** The spend cap is set with env `FALSIFY_SPEND_CAP_USD` (default 20).

## Gotchas learned the hard way
- **Never launch the lab with `omnigent run ... -p`.** `-p` is one-shot mode and **stops the session when the PI goes idle** (this caused 4 "disconnections"). Use interactive mode (`bin/lab-supervisor`).
- **Validate with Omnigent's real validator** (`bin/check-lab`). Sub-agent names must be unique across the whole tree.
- **When changing code while the lab runs,** use a **git worktree** (`git worktree add ../falsify-x -b branch`). **Never commit a `.venv` symlink** (that broke the environment once).
- **Run tests with `set -o pipefail`** (a piped `tail` once hid failures).
- **Validity bars must be tested against fixed baseline scripts before approval** (the loop 3 lesson).
- **The engineer (Claude Code) builds code; lab agents must not edit `falsify/`, `tests/` or `lab/`.** The PI requests builds with `bin/falsify log PI engineering_request ...`; the engineer replies with `engineer build_complete`.

## Hackathon deliverables still to do
- **150–300 word summary,** 60 s demo video, 60 s tech video, **1-page PDF** (`TeamName_OnePager.pdf`), the public repo (done), a zip of the code, and the dataset link (`data/trials`, or "N/A").
- **Demo moments to show:**
  1. a PI decision → reviewer FAIL → PI correction (D002 → D003);
  2. the PI reporting a governance loophole and refusing to patch it (D006);
  3. the adversarial pod's executable proof that the validity bar was inverted;
  4. a result changing the next experiment (exp009 → v2.1 → pivot);
  5. the tracker with live time estimates.
- **Speedup comparison:** manual loop 1 timing is in `baseline/manual_loop.jsonl` (23.8 min, done with AI help, so a conservative baseline). Loop-quality rubric: `baseline/LOOP_QUALITY_RUBRIC.md` (not yet scored).

## Open issues
- The `ui/` folder: a control-room app built by another session; it reads fixtures, not live data.
- Pod `status.json` files can be edited directly by agents (the CLI validates only through its own commands).
- The loop-quality rubric Q1–Q8 for Loops 1–3 hasn't been computed yet.

## DEADLINE: 6:00 AM (Oct 4), with videos, demo, etc.
Plan:
- ~21:00: science freeze; no new experiments after this.
- 21:00–00:00: record narration.
- 00:00–02:00: package and SUBMIT EARLY.
- 02:00–06:00: buffer.

Drafts live in `submission/`.

## LATEST (16:13): read this first
- Loop 3 is CLOSED. The D015 gate was approved by the human (recorded as: FreightRoute v2.1 parked, not killed; no extra v2.1 trials; exp011 approved).
- **exp011 (Haiku 4.5, ambiguity × peer pilot, 30 trials, about $3) is APPROVED at Level 3.**
  - Decision D016, review PASS_WITH_NOTE; the human gate was approved at 16:12:45 from a browser.
  - The PI should now run `bin/falsify run specs/exp011_ambiguity_x_peer_haiku_pilot.json --decision D016`. **Check `data/exp011_ambiguity_x_peer_haiku_pilot.log`.** If it hasn't started, type into the PI's REPL (`tmux attach -t falsify`) asking it to run D016.
- **Known gap flagged by the PI before any data:** `falsify/analyze.py` `main_e` computes only `non_correction`, which the PI's prereg amendment demotes. It does not compute P-BLIND, tie rate, all-HOLD count, or blind-recommendation measures. An engineering build is needed before the analysis pod reads exp011. See the timeline entries `exp011_predata_corrections` (16:11:58) and D016.
- Spend so far: about $0.0002 (key test). Watch `bin/falsify budget` and `data/spend_ledger.jsonl`. The cap is $20.
- After exp011: analysis pod → adversarial pod → PI decision. Then the hackathon deliverables (see above).
