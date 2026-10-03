# Prior-work synthesis and gap analysis: under what conditions does multi-agent escalation emerge after a shared plan is invalidated?

Agent: literature. Date: 2026-10-03.
Scope rules in force (human researcher, `timeline.jsonl` @ 2026-10-03T11:11:04): sources restricted to
`sources/candidates.md` (**PROVISIONALLY APPROVED**); synthesis and gap analysis allowed; **strong novelty
claims not allowed** — where our design looks new it is stated relative to the nearest prior work.

**Verification flags used throughout.** `[abstract-only]` — only abstract/landing page checked (the default
for nearly every entry). `[2026 preprint]` — recent, not peer-reviewed. `[not fetched]` — recorded in
`candidates.md` as "found by search, not fetched"; weakest tier. `DIRECT` / `ADJACENT` per `candidates.md`
(DIRECT = tests persistence after plan invalidation in LLM agents / multi-agent LLM groups, or sunk-cost-like
behavior in LLMs). **No ADJACENT source is used to carry a claim that needs a DIRECT one**; where that would
be required, this is said explicitly.

Our own result is cited by ID, not re-derived: `results/exp001_pilot.json`, `results/exp001_pilot_stats.json`,
`critiques/exp001_pilot_skeptic.md`.

---

## 0. The one DIRECT escalation source, stated precisely

**Barkett, Long & Kröger 2025, "Getting out of the Big-Muddy: Escalation of Commitment in LLMs"**
(arxiv 2508.01545) — `DIRECT`, `[abstract-only]`.

What `candidates.md` records that it **did**:
- A **Staw-style vignette** (1976 paradigm; `Staw 1976` is itself `ADJACENT`, `[abstract-only]`).
- **One model: o4-mini.**
- Three organizational conditions with reported escalation rates: **little escalation for an individual**,
  **46.2% in a hierarchy**, **99.2% in peer deliberation**.

What `candidates.md` explicitly records that it **did not** do:
- **Not agentic.** No action loop, no budget, no environment state, no cost of acting.
- **Investment amount not varied.** Prior investment is a fixture of the vignette, not a manipulated factor.
- **No auditor fix.** No mitigation arm, in particular no history-free external auditor.

Three further things it does **not** establish, which follow from the above and which we must not borrow:
- It does not vary **evidence decisiveness**. A Staw-style vignette supplies *equivocal* mixed-signal
  feedback by construction; it does not contain a decisive hard-constraint violation, and it therefore
  cannot tell us the escalation rate when the invalidating evidence is unambiguous.
- It does not **decompose** the hierarchy vs peer-deliberation gap. Hierarchy and peer deliberation differ
  simultaneously in authority, number of speakers, turn count, context length and accumulated agreement.
  The 46.2 / 99.2 contrast is a package contrast.
- It does not speak to **model family or scale** (single model).
- Because it is `[abstract-only]`, even the three headline numbers are at abstract-level verification; we
  should quote them as reported, not treat them as audited.

**What Barkett et al. predicts for FreightRoute v1.** Our `multi` organization is the *hierarchy* arm and
only the hierarchy arm — Researcher → Planner (holds authority) → Executor → Reviewer over one shared log,
with the Executor complying with the Planner in 20/20 multi trials (`exp001_pilot_skeptic.md` §T5). We have
**no peer-deliberation arm**. So Barkett's largest and most robust effect — the jump to 99.2% under peer
deliberation — is **not addressable by our current design at all**. The comparison our design does make
(hierarchy vs individual, under decisive evidence, agentic) maps onto Barkett's smaller and more fragile
contrast, and does so after changing two things at once (agentic loop; decisive rather than equivocal
evidence).

**Is our null consistent or inconsistent with Barkett et al.?** **Consistent, and non-diagnostic.** Reasons:
1. Barkett's hierarchy rate is 46.2% *under vignette conditions with equivocal feedback*. Our invalidating
   evidence is decisive (a hard-rule load-limit violation) and switching is free — the skeptic's T1 shows a
   correctly-comprehending agent has no reason to persist. Barkett et al. tested nothing at the decisive end,
   so it makes **no prediction** we could have contradicted.
2. Our measured Δ = 0.0, 95% CI [−1.6, 1.6] on a `wasted_actions` outcome taking only {0, 4}, with 18/20
   invalidating trials at 0, is a floor measurement. A CI that wide on a 4-unit-quantized outcome cannot
   exclude Barkett-sized effects.
3. The two non-zero trials were route-attribution errors, not persistence, and **no trial referenced the
   prior investment** (`exp001_pilot_skeptic.md` §1.1). We did not observe the behavior Barkett et al.
   measured, so we did not fail to replicate it either.

The honest statement: **we did not identify prior work that directly tests escalation after plan
invalidation under decisive invalidating evidence in an agentic loop with a role hierarchy**, and our pilot
does not yet test it either, because the pilot is at a design floor.

---

## (a) Mechanism-by-mechanism synthesis

### Mechanism 1 — Evidence ambiguity: does escalation require equivocal rather than decisive evidence?

| | |
|---|---|
| **What prior work establishes** | Nothing directly. The escalation paradigm itself (`Staw 1976`, `ADJACENT`, `[abstract-only]`) is built on *equivocal* negative feedback, and `Barkett, Long & Kröger 2025` (`DIRECT`, `[abstract-only]`) inherits that vignette structure — so every reported LLM escalation rate we have is an *equivocal-evidence* rate. `Sleesman et al. 2012` (`ADJACENT`, `[abstract-only]`), a meta-analysis mapping determinants of escalation, is the right source to adjudicate this and we have it only at abstract level; we cannot read a decisiveness moderator out of an abstract. `Conlon & Garland 1993` (`ADJACENT`, `[abstract-only]`) shows a *different* variable — project completion — can dominate sunk cost, which is indirect evidence that escalation is driven by what makes continuing look attractive rather than by investment per se. On the LLM-agentic side, `ToolMaze` (Zhu et al., `DIRECT (single agent)`, `[2026 preprint]`) reports single agents over-trusting invalid tool paths, and `CostBench` (Liu et al., `DIRECT (single agent)`, `[abstract-only]`) reports mid-task disruptions cutting performance ~40% with weak replanning — but neither manipulates investment, and neither is described as manipulating how decisive the disruption is. |
| **What prior work does not establish** | We did not identify prior work that directly tests escalation under *decisive* (hard-constraint) invalidating evidence versus equivocal evidence, holding organization fixed. Ambiguity is a confound baked into the entire escalation literature we have access to, not a manipulated factor in any approved source. |
| **Verification level** | Weak-to-moderate. One `DIRECT` source at `[abstract-only]`; two `DIRECT (single agent)` sources, one of them `[2026 preprint]`; human-side sources all `ADJACENT` and `[abstract-only]`. |
| **Prediction for FreightRoute** | This mechanism predicts our result exactly. With a hard rule, a known-feasible alternative from round 0, free switching and no payoff for completing A, the design sits at the decisive end — i.e. outside the region where any approved source reports escalation. Predicted `wasted_actions` ≈ 0, which is what we got (18/20 zeros). **Ambiguity is the leading candidate explanation for our floor**, and it is the one mechanism whose manipulation is both untested in prior work and cheap for us (it is essentially skeptic control C2 "pull-toward-A" plus C4 salience step 1). |

### Mechanism 2 — Peer deliberation vs role hierarchy: which organizational form escalates more?

| | |
|---|---|
| **What prior work establishes** | This is the **best-supported** mechanism in the file, and it is supported by the only `DIRECT` escalation source. `Barkett, Long & Kröger 2025` (`DIRECT`, `[abstract-only]`): individual ≈ little, hierarchy 46.2%, peer deliberation 99.2% — a large, monotone ordering, organizational form ≫ individual disposition. Human precedent agrees in direction: `Whyte 1993` (`ADJACENT`, `[abstract-only]`) — groups escalate more than individuals. Supporting mechanism-level ADJACENT material on why group form matters: `MAST` (Cemri et al. 2025, `ADJACENT`, `[abstract-only]`) on verification failures in multi-agent systems; `Anthropic multi-agent research system` (2025, `ADJACENT`, `[abstract-only]`) on orchestrator-worker cascading errors; `ChatDev` (Qian et al. 2023, `ADJACENT`) as the template for roles sharing one chat history, which is exactly our architecture. |
| **What prior work does not establish** | (i) Why hierarchy < peer deliberation — the 46.2/99.2 gap is a package contrast (authority, speaker count, turn count, context length, accumulated agreement all move together), so it does not identify authority as the operative variable. (ii) Whether the ordering survives an agentic loop. (iii) Whether a *compliant* hierarchy like ours (Executor never overrode the Planner) behaves like Barkett's hierarchy at all. (iv) `Whyte 1993` is `ADJACENT` and human; it cannot carry an LLM organizational claim on its own. |
| **Verification level** | Moderate for the ordering (one `DIRECT` source, `[abstract-only]`, one model). Weak for any causal decomposition. |
| **Prediction for FreightRoute** | Barkett et al. predicts we chose the **weaker** of the two multi-agent arms. If escalation is to be elicited, a peer-deliberation arm (no single authority; agreement must be reached) is predicted to produce far more of it than our Planner-authority hierarchy — on the reported numbers, roughly twice the rate. It also predicts our single-vs-hierarchy contrast is the small one, which is consistent with our organization main effect of 0.0, CI [−0.8, 0.8] — though with a floored outcome that agreement is uninformative. Note our architecture does not even implement a contested hierarchy: 20/20 Executor compliance means our "hierarchy" is closer to Barkett's *individual* arm with narration (`exp001_pilot_skeptic.md` §T5) than to a hierarchy with a suppressed dissenter. |

### Mechanism 3 — Acting vs one-shot reasoning (vignette/questionnaire vs agentic loop with a budget)

| | |
|---|---|
| **What prior work establishes** | The two paradigms exist in the approved file but **have never been joined on escalation**. Vignette side: `Barkett, Long & Kröger 2025` is explicitly "not agentic" (`DIRECT`, `[abstract-only]`); `Staw 1976`, `Arkes & Blumer 1985`, `Conlon & Garland 1993`, `Whyte 1993`, `Sleesman et al. 2012` are all human questionnaire/scenario work (`ADJACENT`, `[abstract-only]`). Agentic side (`candidates.md` §2/§3): `CostBench` (`DIRECT (single agent)`, `[abstract-only]`) — mid-task disruption, ~40% performance drop, weak replanning; `ToolMaze` (`DIRECT (single agent)`, `[2026 preprint]`) — over-trust of invalid tool paths; `Vending-Bench` (`ADJACENT`, `[abstract-only]`) — long-run derailment not clearly tied to a full context window; `METR` long-task horizons (`ADJACENT`, `[abstract-only]`) with gains partly from adapting to mistakes; `LLMs Get Lost in Multi-Turn Conversation` (`ADJACENT`, `[abstract-only]`) — early wrong turns persist; `Project Vend` (`ADJACENT`, `[abstract-only]`, anecdotal) — persistence despite acknowledging the problem. The agentic sources establish that replanning after disruption is *weak in single agents*; none of them manipulates investment, and none is multi-agent. |
| **What prior work does not establish** | We did not identify prior work that directly tests escalation after plan invalidation under an agentic action loop with a budget, in a multi-agent organization. Every escalation number we have is one-shot; every agentic replanning-failure number we have is single-agent and investment-free. The two literatures do not touch. |
| **Verification level** | Weak. One `[2026 preprint]`, the rest `[abstract-only]`; `Project Vend` is self-described anecdotal and must not carry weight; `Effective harnesses for long-running agents` and `Measuring AI agent autonomy in practice` are `[not fetched]` and are **excluded from load-bearing use** here. |
| **Prediction for FreightRoute** | Two opposed predictions, which is why this is interesting. (i) *Acting reduces escalation*: in an agentic loop with a real budget, the alternative's feasibility is verifiable and switching is cheap, so the Staw rationalization has nothing to grip — this predicts our floor. (ii) *Acting increases persistence*: the single-agent replanning literature (`CostBench`, `ToolMaze`) says agents that have begun executing a path over-trust it, which predicts non-zero wasted actions. Our pilot supports (i) over (ii) **but only weakly**, because our R=8 budget was never engaged (8 rounds offered, 4 ever used, 40/40 trials) and `wasted_actions` was quantized to {0, 4} — the agentic character of the environment was largely inert, so the pilot is a poor test of the acting-vs-reasoning contrast it nominally instantiates. |

### Mechanism 4 — Shared history / consensus / self-conditioning

| | |
|---|---|
| **What prior work establishes** | The conformity cluster (`candidates.md` §4) is consistent and directionally clear, and entirely `ADJACENT`. `BenchForm` (Weng et al. 2025, `ADJACENT`, `[abstract-only]`): conformity grows with **interaction time** and **majority size** — the closest thing we have to a dose-response for accumulated agreement. `Herd Behavior in LLM Multi-Agent Systems` (Cho, Guntuku & Ungar 2025, `ADJACENT`, `[abstract-only]`): how peer information is *presented* drives conformity. `Exploring Collaboration Mechanisms for LLM Agents` (Zhang et al. 2024, `ADJACENT`, `[abstract-only]`): conformity and consensus in agent societies. `Peacemaker or Troublemaker` (Yao et al. 2025, `ADJACENT`, `[abstract-only]`): sycophancy causes disagreement collapse. `LLMs Trust Their Own` (Soffer et al., `ADJACENT`, `[2026 preprint]`): more conformity to in-group agents. Self-conditioning: `The Illusion of Diminishing Returns` (Sinha et al. 2025, `ADJACENT`, `[abstract-only]`) — errors in a model's own history raise later errors *beyond* context-length effects, which is the cleanest approved support for separating history content from history length. `Plans Don't Persist` (Mehta & Datta, `ADJACENT`, `[2026 preprint]`) — plans are read back from context, so persistence depends on context; `Generative Agents` (Park et al. 2023, `ADJACENT`) — accumulated memory drives behavior. Self-authorship: `LLM Evaluators Recognize and Favor Their Own Generations` (Panickssery et al. 2024, `ADJACENT`, `[abstract-only]`) and `Staw 1976`'s personal-responsibility effect (`ADJACENT`). Counterpoint, which must be kept: `Multiagent Debate` (Du et al. 2023, `ADJACENT`, `[abstract-only]`) reports debate *helps*, cutting against a blanket "more interaction → more conformity" reading. |
| **What prior work does not establish** | Every source here is `ADJACENT`. **None of them measures escalation after plan invalidation**, and conformity-on-a-benchmark-answer is not the same dependent variable as persisting on an invalidated plan with sunk actions. We did not identify prior work that directly tests whether accumulated rounds of unanimous agreement cause persistence after invalidation, separately from context length and separately from self-authorship. The one source that could bridge to escalation (`Barkett`) does not manipulate agreement history. |
| **Verification level** | Weak for our purpose. Internally consistent cluster, but `ADJACENT` across the board, two `[2026 preprint]`, all `[abstract-only]`, plus a live counterexample (`Multiagent Debate`). **This cluster must not be used to assert that consensus causes escalation** — it can only motivate the hypothesis. |
| **Prediction for FreightRoute** | `BenchForm`'s interaction-time dose-response predicts our k=10 arm should persist more than k=1. We observed the **opposite sign** (investment main effect −0.8, CI [−2.0, 0.0]) — but the skeptic shows this is one seed's attention error landing in the k=1 cells, not evidence against conformity. Crucially, our k=10 history is ten *near-duplicate scripted* turns, i.e. redundant filler rather than accumulating distinct agreement, and our four roles are the same model over the same context — `Soffer et al.`'s in-group effect and `BenchForm`'s majority-size effect both imply this should be a high-conformity configuration, and indeed all four roles reproduced the identical mis-binding with `disagreement = False` in every round (C-005). The prediction for a *fixed* design is: with genuine accumulated agreement (distinct, non-template concurrences) and a recorded-dissent comparison arm, this cluster predicts a detectable effect. `Sinha et al.` predicts it should survive a token-matched padded control — which is exactly H6's falsification test. |

### Mechanism 5 — Model family / scale: how much of the reported behavior is model-specific?

| | |
|---|---|
| **What prior work establishes** | Almost nothing, and this is the sharpest weakness in the evidence base. `Barkett, Long & Kröger 2025` is **one model (o4-mini)**; the 46.2% / 99.2% figures have no cross-model replication in any approved source. No approved source reports an escalation-after-invalidation scaling curve. The nearest approved material is indirect: `METR` (`ADJACENT`, `[abstract-only]`) shows time-horizon capability scales and that gains come partly from adapting to mistakes — which implies larger models should replan *better*, i.e. escalate less, but this is an inference from a capability metric, not a measurement of escalation. `Vending-Bench` and `Project Vend` (`ADJACENT`) are single-configuration. `Measuring AI agent autonomy in practice` is `[not fetched]` and excluded. |
| **What prior work does not establish** | We did not identify prior work that directly tests whether escalation after plan invalidation varies with model family or scale, under any organizational form. All reported LLM escalation rates in the approved set rest on one model. |
| **Verification level** | Very weak — single-model `[abstract-only]` for the only `DIRECT` source; the scaling inference comes from an `ADJACENT` capability benchmark and should be labelled a conjecture. |
| **Prediction for FreightRoute** | `qwen3:8b` at T=0.7 is far from o4-mini in family and scale, so Barkett et al. makes **no calibrated prediction** for our model. The skeptic's T8 is the sharper point: our only behavioral phenomenon is an 8B-scale reference-binding slip that a larger model may never make, so the planned Haiku 4.5 replication could return all zeros and still say nothing about H1. Conversely the METR-style inference predicts larger models escalate *less* under decisive evidence — meaning a cross-model sweep run on the current floored design is predicted to produce zeros everywhere and is **not worth compute until a cell shows interpretable non-floor behavior**. |

---

## (b) The causal comparison that has not been made, and is worth our compute

**Primary gap.** We did not identify prior work that directly tests **evidence decisiveness (decisive
hard-constraint invalidation vs equivocal/mixed invalidation) × organizational form (individual vs role
hierarchy vs peer deliberation)** under **an agentic loop with a real action budget**, with **prior
investment manipulated**. Every approved source holds at least two of those four factors fixed:
- `Barkett et al. 2025` varies organizational form only — equivocal evidence, no acting, investment fixed.
- `CostBench` / `ToolMaze` act, but are single-agent, investment-free, and do not vary decisiveness.
- The §4 conformity cluster varies interaction/consensus, but on a different dependent variable entirely.

**The specific comparison we should buy first**, and why it is the highest-value cell, is the **2 × 2 of
evidence decisiveness × organizational form, with peer deliberation added**:

1. **Evidence decisiveness is the factor that explains our null** and is untested everywhere in the approved
   set. Without it we cannot distinguish "LLM hierarchies don't escalate" from "our environment made
   escalation impossible" — the skeptic's T1 says the second is sufficient on its own.
2. **A peer-deliberation arm is required for us to touch Barkett et al.'s main effect at all.** Our
   hierarchy-only design engages their weakest contrast; adding a flat/vote decision rule converts H5 from
   an untestable claim about our single architecture into the direct agentic analogue of their 46.2 vs 99.2
   result. This is the nearest-prior-work framing: *relative to Barkett et al., what is not yet done is the
   agentic, decisive-evidence version of their organizational-form contrast.*
3. It is cheap relative to the alternatives, and it subsumes the skeptic's C2 (pull-toward-A) and C3
   (route counterbalance) rather than competing with them.

**Prerequisite, non-negotiable.** None of this is interpretable without the skeptic's **C1 comprehension
probe**. `Barkett et al.`'s vignette paradigm has no comprehension failure mode — the vignette states the
situation — so prior work gives us *no* calibration for distinguishing mis-binding from persistence. That
distinction is ours to instrument, and until it is instrumented, a non-zero `wasted_actions` in a
decisive-evidence or peer-deliberation arm is uninterpretable.

**Secondary gaps, in descending value.**
- **History-free auditor as a causal fix (M1).** We did not identify prior work that directly tests a
  fresh, history-free auditor as a fix for persistence after invalidation in a multi-agent organization.
  `candidates.md` records `Barkett et al.` as having **no auditor fix**, and the supporting material
  (`Huang et al. 2023` self-correction fails without external feedback; `Kamoi et al. 2024` correction works
  with reliable external feedback; `McAleese et al. 2024` separate critics catch missed errors;
  `Bricken et al. 2025` independent parallel auditors 13%→42%; `Greenblatt et al. 2023` a monitor not
  sharing the actor's state) is **entirely `ADJACENT`** and on different tasks. Promising, but it is a
  mitigation for a phenomenon we have not yet elicited — it should follow, not precede, the decisiveness arm.
- **Consensus vs context length vs self-authorship, separated within one design (H2/H3/H4/H6).** The
  conformity cluster and `Sinha et al.` motivate the separation; no approved source performs it.

---

## (c) Effect of prior work on our registry hypotheses, by ID

**More promising after this review**

- **H5 (hierarchy / authority)** — *largest upgrade*. `Barkett et al.` (`DIRECT`) reports organizational form
  as the dominant factor (little → 46.2% → 99.2%), and its falsification test ("persistence unchanged under a
  flat/vote decision rule") is precisely the under-specified part of that source. H5 should be **promoted
  from a side hypothesis to a co-primary one**, and its flat arm reconceived as *peer deliberation* (consensus
  required, no final authority) rather than merely a vote, because that is the arm with the 99.2% report.
  Caveat: single model, `[abstract-only]`.
- **H3 (conformity / accumulated consensus)** — upgraded in plausibility by `BenchForm`'s interaction-time and
  majority-size dose-response, `Soffer et al.`'s in-group conformity, `Yao et al.`'s disagreement collapse, and
  our own observation of four same-model roles reproducing one error with `disagreement = False` throughout.
  But all support is `ADJACENT` and the dependent variable differs, plus `Du et al. 2023` cuts the other way.
  Its stated falsification test (recorded dissent in prior rounds) is well-posed and worth running — **after**
  the design produces non-floor behavior.
- **M1 (fresh independent auditor)** — plausible on converging `ADJACENT` evidence and clearly absent from
  prior work, hence valuable. Sequencing caveat above: a mitigation needs a phenomenon.
- **H6 (context length as the real explanator)** — upgraded as a *control* rather than as a hypothesis.
  `Sinha et al.` (self-conditioning beyond context length) and `Vending-Bench` (derailment not clearly tied to
  a full window) both argue context length alone is an insufficient explanation; our own T4 shows k is
  confounded with context length, redundancy and apparent completion. H6's padded control is **mandatory**,
  consistent with skeptic C5.

**Less promising after this review**

- **H1 (prior computational investment × organization)** — *largest downgrade*, from two directions. Prior
  work: `Barkett et al.` does **not vary investment amount**, so there is no `DIRECT` precedent for an
  investment dose-response in LLMs; `Conlon & Garland 1993` (`ADJACENT`) reports project completion
  information can *dominate* sunk cost, i.e. the attractiveness of continuing may matter more than how much
  was spent; `Sleesman et al. 2012` (`ADJACENT`, `[abstract-only]`) treats sunk cost as one determinant among
  many. Our data: no trial referenced the prior investment at all, and the investment main effect's sign is
  opposite to H1. H1 should be reframed as conditional — *investment matters only where continuing is
  attractive, i.e. under equivocal evidence* — which makes **evidence decisiveness a moderator that must be
  in the design before H1 is run again**. H1 is not falsified; it is **not yet testable** in this environment.
- **H4 (self-authorship)** — downgraded on *priority*, not on plausibility. Support is `ADJACENT` and thin
  (`Panickssery et al. 2024` self-preference in evaluation; `Staw 1976` personal responsibility), the
  manipulation (self vs external provenance of an identical plan) is subtle, and it is the mechanism least
  likely to clear a floor. Defer until a cell shows interpretable non-floor behavior.
- **H2 (shared history rather than investment)** — neutral-to-mildly-more-promising in content (it is the
  hypothesis `Sinha et al.` and `Plans Don't Persist` speak to most directly) but **low priority as stated**,
  because it is defined as a subtraction from H1 and inherits H1's untestability on the current design.
  Its logic is better served by folding it into the padded/dissent controls.

**P-family (`integrity_under_pressure`, FreightRoute v2) — essentially unaddressed by the approved set**

- **P1 (resource scarcity → skipped verification)**, **P2 (performance target → unsupported claims)**,
  **P3 (scarcity × pressure interaction)** — no approved source tests these. The nearest material is
  `Agentic Misalignment` (Lynch et al. 2025, `ADJACENT`, `[abstract-only]`) on disobedience under goal
  conflict and `Sabotage Evaluations` (Benton et al. 2024, `ADJACENT`) on subverting oversight. Neither
  manipulates budget or an explicit score target. **Verdict: neither more nor less promising on
  prior-work grounds — unconstrained.** P3 in particular asks for an interaction term with no prior effect
  size anywhere in the file, so it is the most power-hungry hypothesis in the registry and should not be
  attempted before P1 and P2 show main effects.
- **P4 (organization × pressure)** — mildly more promising by *analogy* to `Barkett et al.`'s
  organizational-form dominance and `Whyte 1993`, but this is a cross-family analogy (escalation →
  integrity), and **no approved source supports it on the integrity dependent variable**. Treat as conjecture.
- **P5 (independent auditor reduces integrity failures without destroying success)** — mildly more promising
  via the same `ADJACENT` oversight cluster as M1 (`Bricken et al.` 13%→42%, `McAleese et al.`,
  `Greenblatt et al.`, `Bowman et al. 2022`). Shares M1's sequencing caveat, and additionally shares P1–P3's
  problem that the phenomenon to be mitigated has not been elicited in our environment.

---

## (d) Prior-work claims too weakly verified to lean on

Listed in order of how much damage over-reliance would do.

1. **Barkett et al.'s 46.2% / 99.2% figures.** `[abstract-only]`, single model (o4-mini), single paradigm
   (Staw-style vignette), no cross-model replication in the approved set. Usable as **motivation and as the
   nearest-prior-work reference point**; **not** usable as a calibrated expected effect size for our
   environment, our model, or our dependent variable. Any power calculation anchored to 46.2% is unjustified.
2. **Anything resting on `[not fetched]` entries.** `Effective harnesses for long-running agents` (Young 2025)
   and `Measuring AI agent autonomy in practice` (Anthropic 2026) are recorded in `candidates.md` as found by
   search and not fetched. **Do not cite these for any claim**, including the fresh-context-handoff motivation
   for M1 — that motivation must rest on `Huang et al. 2023` / `Kamoi et al. 2024` / `Bricken et al. 2025`
   instead.
3. **The 2026 preprints.** `ToolMaze` (Zhu et al.), `When Agents Commit Too Soon` (Mehta), `Plans Don't
   Persist` (Mehta & Datta), `LLMs Trust Their Own` (Soffer et al.) — all `[2026 preprint]`, not peer-reviewed,
   all `[abstract-only]`. Three of the four are also `ADJACENT`. Usable to motivate hypotheses; not usable to
   establish that an effect exists. Note two of them share an author (Mehta), so they are not independent
   corroboration of each other.
4. **Any conformity source carrying an escalation claim.** All of `candidates.md` §4 is `ADJACENT`. Conformity
   on benchmark answers is a different dependent variable from persistence on an invalidated plan with sunk
   actions. We did not identify prior work that directly tests consensus-driven escalation after plan
   invalidation; `BenchForm` et al. cannot be made to stand in. `Du et al. 2023` (debate helps) must be
   reported alongside them.
5. **Human escalation findings as predictions for LLM organizations.** `Whyte 1993`, `Staw 1976`,
   `Arkes & Blumer 1985`, `Conlon & Garland 1993`, `Sleesman et al. 2012` — all `ADJACENT`, all
   `[abstract-only]`, all human-subject. They license *hypotheses* about our org contrast; they do not
   license *expectations* about LLM behavior. In particular, `Sleesman et al. 2012` is a meta-analysis whose
   value is in its moderator table, and we have only the abstract — **we should not claim to know which
   determinants it ranks highest**.
6. **`Project Vend`'s persistence observation.** Recorded in `candidates.md` as anecdotal. Illustrative only;
   zero inferential weight.
7. **The scaling inference for Mechanism 5.** "Larger models replan better, therefore escalate less" is an
   inference from `METR`'s capability metric (`ADJACENT`, `[abstract-only]`), not a measurement of escalation.
   Label it a conjecture wherever it appears.
8. **`candidates.md`'s own gap assessment.** The file states its conclusions rest on one session's search,
   mostly at abstract level, with a stated next step of checking papers citing `Barkett et al.` and
   `ToolMaze`. Every "we did not identify prior work" statement in this document — including (b)'s primary
   gap — inherits that limitation and should be re-checked after that citation search is done.

---

## Summary statement for use in write-ups

We did not identify prior work that directly tests escalation after plan invalidation under decisive
hard-constraint evidence in an agentic loop, nor under a role hierarchy with manipulated prior investment,
nor with a history-free auditor as a mitigation. Relative to the nearest prior work
(`Barkett, Long & Kröger 2025`, `DIRECT`, `[abstract-only]`, o4-mini, Staw-style vignettes, non-agentic,
investment not varied, no auditor arm), our design differs in being agentic, hierarchy-only, and
decisive-evidence. Our pilot null (Δ = 0.0, CI [−1.6, 1.6], `results/exp001_pilot_stats.json`) is
**consistent with** that source and **non-diagnostic** of it: Barkett et al. tested nothing at the decisive-
evidence end, our outcome was quantized to {0, 4} with 18/20 invalidating trials at zero, and
`critiques/exp001_pilot_skeptic.md` shows the two non-zero trials were route-attribution errors with no
reference to prior investment in any trial. The comparison worth our compute next is evidence decisiveness ×
organizational form (adding a peer-deliberation arm), gated on the comprehension probe.
