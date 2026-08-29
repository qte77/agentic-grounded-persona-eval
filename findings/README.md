# findings/

Per-product findings land here as `<slug>-findings.md`, one file per product evaluated. This repo
ships no example findings — they're product-specific and often belong with the product being
evaluated instead of here; use this directory when you'd rather keep the corpus centralized across
products.

## Expected structure

A findings file has three sections, written in order by the three phases:

- **§Research** — sourced quotes grouped by pattern, with a "Source coverage" note (Phase 1)
- **§Personas** — 3-4 persona cards, each traceable to specific §Research quotes (Phase 2)
- **§Verdicts** — one subsection per persona from a real live-product run, plus a closing
  §Cross-persona synthesis (Phase 3)

`scripts/verify_sourcing.py` checks §Research mechanically — every quote block needs a source URL.
