# agentic-grounded-persona-eval — orchestration

Execute the grounded-persona-eval pipeline: real ICP research → personas grounded in that
research → live evaluation of the product by those personas.

## Pipeline

```
Phase 1: research-analyst        → findings/<slug>-findings.md §Research
Phase 2: persona-synthesizer     → same file §Personas   (needs §Research)
Phase 3: live-evaluator × N      → reports back to you   (needs §Personas; one instance per persona, parallel)
                                     you write §Verdicts + §Cross-persona synthesis, once, after all N report
```

Strict order between phases — a phase never starts before the one before it has real output, per
each subagent's own precondition check. **Within Phase 3, run all persona instances in parallel**
(single message, multiple Task/Agent calls) — they're independent once §Personas exists, and
running them serially wastes wall-clock for no benefit.

**Single writer for §Verdicts.** `live-evaluator` instances do not write to
`findings/<slug>-findings.md` themselves — concurrent appends from parallel instances risk
clobbering each other, and there's no reliable way for an instance to know it's "the last one." Each
instance reports its structured verdict back to you (the orchestrator); once all N have reported,
you write the entire §Verdicts section — one subsection per persona, plus a closing §Cross-persona
synthesis — in a single pass. If one instance stalls or only produces partial data, don't block
indefinitely: record its partial result honestly (see `live-evaluator.md`'s own guidance on this)
rather than waiting forever or fabricating a completion.

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

- `scripts/verify_sourcing.py findings/<slug>-findings.md` — mechanically checks that every
  blockquote in the *entire file* carries a source URL (it's not scoped to §Research alone — a
  persona-voice quote in §Verdicts needs one too). Run this before trusting Phase 1's output; a CI
  workflow can run it on every push that touches `findings/`.
- Read `findings/<slug>-findings.md`'s §Cross-persona synthesis (written by you, per the single-writer
  rule above) for the single highest-leverage output: what do independently-motivated personas
  converge on, from different angles?
