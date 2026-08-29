# Contributing

## Applying the method to a new product

See `README.md` §Using this on a new product, and `AGENTS.md` for the orchestration commands.

## Changing the method itself

The three subagent `.md` files in `.claude/agents/` **are** the method — edit them directly rather
than maintaining a separate spec. Keep them product-agnostic: if a change only makes sense for one
specific product, it belongs in that product's `config/target.md`, not here.

`scripts/verify_sourcing.py` encodes the one mechanically-checkable rule (every quote needs a
source). Any change to it needs its test in `tests/test_verify_sourcing.py` updated first — this is
the one part of the repo that's genuinely testable code, not instructions for an agent to follow, so
it follows normal TDD: red, green, refactor.

```sh
uv run pytest
```

## Commit style

Branch per topic, commit by topic, squash-merge. No hard requirement on conventional-commit
prefixes, but a short imperative subject line is appreciated.
