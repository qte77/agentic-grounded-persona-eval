# examples/

A real, worked run of the full three-phase pipeline against a live product — not a template, not
illustrative fiction. Every quote, persona, and verdict in here was produced by actually running
`.claude/agents/research-analyst.md` → `persona-synthesizer.md` → `live-evaluator.md` per their own
specs, against a real product's real live site, on the date below. Nothing was invented to make the
example look tidier than a real run actually is — including the parts where tooling stalled, a
source was blocked, or a verdict came back "unconfirmed."

This exists so a new user of the method can see the expected output shape (`§Research` →
`§Personas` → `§Verdicts` + `§Cross-persona synthesis`) end-to-end before running their own, without
this repo abandoning its own product/method split for every other findings doc — see
`findings/README.md`.

## `groundwork/`

- **Product:** [Groundwork](https://github.com/qte77/ldnmxx-hack), live at
  [sortmy.london](https://sortmy.london) — a free, no-sign-up civic assistant for London (NHS
  wayfinding, free heritage/green-space finder, food-hygiene lookup, firm/scam check).
- **`target.md`** — the filled-in config used for this run (the live equivalent, `config/target.md`,
  is gitignored scratch space regenerated per run — this is a permanent record of what was
  configured).
- **`findings.md`** — the full output: 4 sourced Hacker News/Mumsnet/MoneySavingExpert/FCA patterns,
  4 grounded personas, and 4 live-browser verdicts against the real product, run 2026-08-31.
- **Headline finding:** all four independently-run personas converged on the same gap from four
  different angles — the product's "ask in your own words" framing extracts only a location and a
  coarse category from free text, discarding everything else the user actually said. See
  `findings.md`'s closing §Cross-persona synthesis.
- **Honestly flagged, not hidden:** Reddit was network-blocked for Phase 1 research on this runner
  (documented in `findings.md`'s Source coverage note, with UK forum substitutes used instead); an
  initial parallel Phase 3 attempt stalled on a tooling install issue and had to be retried with a
  different install strategy (documented in §Verdicts' tooling note); one live-check against the
  FCA's own register was itself blocked by a bot challenge, leaving one specific data-provenance
  question genuinely unresolved rather than guessed at.

## A note on staleness

This is a snapshot of a live product on a specific date, not a maintained, continuously-re-verified
evaluation. The product will change; this example won't be re-run to keep pace with it. Treat it as
a demonstration of the method's output shape and honesty discipline, not as a current review of
Groundwork.
