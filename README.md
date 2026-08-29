# agentic-grounded-persona-eval

A reusable, product-agnostic method for testing whether a product actually works for its ICP —
grounded in real evidence, not invented personas.

> Stop guessing what your users think. Ground it, then ask them.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Ready-FF6B35?logo=anthropic&logoColor=white)](https://claude.ai/code)

## The problem this solves

Simulated-user testing is usually either skipped, or run with invented personas that reflect the
builder's own assumptions about their users, not real ones. Real ICP behavior is public and
gatherable — this method grounds every persona in sourced evidence before it's allowed to evaluate
anything.

## The method — three phases, strictly in order

A phase never starts before the one before it has real output.

1. **Research** (`.claude/agents/research-analyst.md`) — gather real posts/threads/reviews from
   where the product's ICP actually talks (Reddit, Hacker News, ProductHunt, Trustpilot, or
   industry-appropriate equivalents). Extract **sourced quotes**, not paraphrases — every claim
   about "what users say" carries a URL. No inventing a pain point that wasn't actually observed.
2. **Grounded personas** (`.claude/agents/persona-synthesizer.md`) — synthesize 3-4 personas
   **from** the Phase 1 evidence. Every persona's voice, skepticism, and vocabulary traces back to
   specific quotes gathered in Phase 1. A persona with no grounding quotes is not a persona, it's a
   guess wearing a persona's clothes.
3. **Live evaluation** (`.claude/agents/live-evaluator.md`) — each persona actually uses the live
   product (not a description of it) and reports a candid, in-character verdict: first impression,
   what's confusing, would-they-use-it, a one-line "review" in their voice. The verdict is tagged
   against which Phase 1 evidence it does or doesn't confirm.

## Honesty discipline — non-negotiable

- A quote that can't be sourced doesn't go in the findings doc. `scripts/verify_sourcing.py` checks
  this mechanically — see below.
- A persona verdict must say what it's *not* sure about. A simulated user's confident-sounding
  opinion is not evidence of a real one's.
- A headless capture reflects only that runner's network — treat an empty error capture as "no
  error on this network," not "no error, period." If a source is blocked (bot-fingerprinting, rate
  limits), record that honestly rather than reporting it as evidence of absence.
- Partial data is not the same as no data. If Phase 3 stalls partway through a run, record what was
  actually captured — scoped honestly (e.g. "framing only, never reached the computed output") —
  rather than discarding it or waiting indefinitely for a complete run.

## Tooling

Research and live evaluation both lean on real APIs over HTML scraping wherever one exists — a
source with a real API sidesteps bot-fingerprinting entirely, and general UGC scraping (Reddit,
ProductHunt's own pages, Trustpilot, Medium, Indie Hackers) is fragile against it. Known-good
starting points:

- **Hacker News search** — `https://hn.algolia.com/api/v1/search?query=…`. No auth.
- **Hacker News full comment trees** — `https://hacker-news.firebaseio.com/v0/item/<id>.json`
  (official Firebase API, no auth) — walk `kids` recursively after Algolia search finds a story.
- **ProductHunt** — GraphQL API v2, `https://api.producthunt.com/v2/api/graphql`. Self-serve
  `developer_token` from a PH account's API dashboard, no app review needed.

Any source beyond these still needs its own probe before it's trusted — a name appearing here is
not evidence it will work on a given runner's network.

**Browser interaction** (Phase 1's structured-API fallback, and all of Phase 3):
[`polyfetch-scrape`](https://github.com/qte77/polyfetch-scrape) — `USING.md` is the stable
agent-facing contract. `polyfetch fetch`/`discover --json` for static pages; `render_session()` for
real multi-step browser interaction (click, fill, screenshot) against a live product.

## Using this on a new product

1. Fork or clone this repo (or copy it into the target product's own repo as a subdirectory —
   either works, since the method has no dependency on where its output lives).
2. Copy `config/target.example.md` to `config/target.md` and fill in: the product being tested, its
   known/assumed ICPs, and any product-specific research constraints.
3. Run Phase 1 → Phase 2 → Phase 3, in order, per each subagent's own `.md` (or drive them manually
   with Claude Code / another agent runtime — the subagent files are the spec, not a required
   runtime).
4. Findings land in `findings/<product-slug>-findings.md` — see `findings/README.md` for the
   expected structure. This repo intentionally does not ship example findings; they're
   product-specific and belong with the product being evaluated, or in a `findings/` subdirectory
   here if you'd rather keep the corpus centralized.

## Origin

Extracted from a real internal application of this method — 7 sourced Hacker News patterns, 4
grounded personas, live-evaluated against the product itself. That application's product-specific
findings stayed with the product being evaluated, per this method's own product/method split; only
the method (this repo) is meant to be public and reusable.

## License

Licensed under the [Apache License 2.0](LICENSE).
