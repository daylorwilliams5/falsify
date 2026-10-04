FALSIFY DATASET
Generated during the Hack-Nation 7th Global AI Hackathon (Oct 3, 2026) by the Falsify lab.
All trials are simulated: synthetic freight-routing tasks given to AI agents. No personal data.

STRUCTURE
  raw/        -> data/trials/<experiment_id>.jsonl   one JSON object per trial, append-only, never edited
  processed/  -> results/<experiment_id>.json        the scripted, preregistered analysis of those trials
  provenance  -> timeline.jsonl, decisions/D*.json, specs/<experiment_id>.json, specs/PREREG_*.md
  cost        -> data/spend_ledger.jsonl             per-call API tokens and USD (no keys, no prompts)

EXPERIMENTS (subject model, trials)
  exp001_pilot                                   qwen3:8b,         40   route switching after invalidating evidence
  exp009_v2_floor_probe                          qwen3:8b,         20   process integrity (instrument failed: livelock)
  exp010_v21_pilot                               qwen3:8b,         20   rebuilt instrument (validity bar later shown inverted)
  exp011_ambiguity_x_peer_haiku_pilot            claude-haiku-4-5, 30 valid (+30 harness errors kept)
  exp012_ambiguity_x_peer_haiku_main             claude-haiku-4-5, 90   single vs 4 peers x clear/probabilistic/conflicting evidence
  exp013t_time_cost_x_advisory_majority_haiku    claude-haiku-4-5, 60 valid (+60 harness errors kept)
                                                 time cost x scripted advisory majority, one live decider

TRIAL RECORD FIELDS (data/trials/*.jsonl; experiment-specific fields vary)
  trial_id, experiment_id, spec_hash, seed, model, temperature   identity and reproducibility
  cell + cell factors (org, evidence, verification, dissenter)    experimental condition
  valid, invalid_reason                                           invalid trials are kept; "exception:" = harness error, not model behaviour
  evidence_text, round1_system, round1_prompt                     what the subject actually saw (exp013t)
  rounds[]                                                        per round: the subject's JSON output (rationale, evidence_assessment,
                                                                  p_route_a_legal [exp013t], action) or peers' blind recommendations and votes,
                                                                  team action, environment response
  measured{}                                                      outcomes computed by code from the action sequence, never by a model:
                                                                  first_response (switch/persist/seek/hold), verify_first, switched,
                                                                  persist_actions, seek_actions, unsafe_delivery, delivered_route,
                                                                  fees_paid, tokens, llm_calls
NOTES
  Haiku results are never pooled with qwen3 results. Anthropic's API has no sampling seed, so Haiku runs are reproducible
  distributionally, not trial by trial; scenarios are reproducible from seed via falsify/env3.py make_scenario_e().
