# agentic-grounded-persona-eval — orchestration

Execute the grounded-persona-eval pipeline: real ICP research → personas grounded in that
research → live evaluation of the product by those personas.

## Pipeline

```
Phase 1: research-analyst        → findings/<slug>-findings.md §Research
Phase 2: persona-synthesizer     → same file §Personas   (needs §Research)
Phase 3: live-evaluator × N      → same file §Verdicts   (needs §Personas; one instance per persona, parallel)
```

Strict order between phases — a phase never starts before the one before it has real output, per
each subagent's own precondition check. **Within Phase 3, run all persona instances in parallel**
(single message, multiple Task/Agent calls) — they're independent once §Personas exists, and
running them serially wastes wall-clock for no benefit.

## Before running

1. Copy `config/target.example.md` to `config/target.md` and fill it in for the product under test.
2. Confirm `<slug>` (used in `findings/<slug>-findings.md`) — a short kebab-case name for the
   product, e.g. the product's own repo name.

## Running it

With Claude Code:

```sh
claude -p "Read AGENTS.md and execute the grounded-persona-eval pipeline for config/target.md, phase by phase, per each subagent's own precondition checks."
```

Or drive each phase manually — the subagent `.md` files in `.claude/agents/` are the spec, not a
required runtime; any agent capable of following instructions and using
[`polyfetch-scrape`](https://github.com/qte77/polyfetch-scrape) can run this method.

## After running

- `scripts/verify_sourcing.py findings/<slug>-findings.md` — mechanically checks every quote block
  in §Research carries a source URL. Run this before trusting Phase 1's output; a CI workflow can
  run it on every push that touches `findings/`.
- Read `findings/<slug>-findings.md`'s §Cross-persona synthesis (written by the last Phase 3
  instance to complete) for the single highest-leverage output: what do independently-motivated
  personas converge on, from different angles?
