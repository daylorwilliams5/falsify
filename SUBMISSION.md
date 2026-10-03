# Falsify: submission copy

## Project description

**Falsify is an autonomous scientific lab for studying AI-agent behavior.**

Most agent benchmarks tell us whether an agent succeeds. Falsify asks why its behavior changes and what intervention makes it more reliable.

Using Omnigent, Falsify coordinates a PI, a literature pod, an experiment-design pod, independent analysts, adversarial reviewers, and a methodology reviewer. The lab can move through the entire scientific loop autonomously: review evidence, form competing hypotheses, choose an experiment, run it, analyze the result, challenge its own interpretation, and decide what to test next.

The first research program investigates agent corrigibility and behavioral integrity: when agents persist with bad plans, respond to pressure, follow peer consensus, or ignore corrective evidence.

Crucially, Falsify does not assume its own research agents are trustworthy. Generation, execution, analysis, and review are separated, raw results are immutable, and scientific claims can be rejected by independent reviewers.

During development, the lab's first hypothesis failed to show its predicted effect: 18 of 20 agents abandoned an invalidated plan immediately. The lab recorded that honestly instead of forcing a result. A later experiment was invalidated after the lab found a flaw in its own measurement environment, and the lab treated that as an instrument failure, not a discovery.

**Final result:** [INSERT FINAL EMPIRICAL FINDING]

Built solo in 24 hours.

## One-line version

> Falsify is an Omnigent-powered autonomous scientific lab that experimentally studies why AI agents behave badly and which interventions make them more reliable.

## 30-second pitch

> We have a lot of benchmarks that tell us whether AI agents succeed, but much less understanding of why their behavior changes. I built Falsify, an autonomous scientific lab that uses Omnigent to generate hypotheses about agent behavior, design and run controlled experiments, analyze the results independently, challenge its own conclusions, and decide what to test next. The lab is currently studying when agents become resistant to correction or sacrifice process integrity, and what forms of oversight restore reliable behavior.
