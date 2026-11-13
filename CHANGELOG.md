# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- CodeQL workflow (`.github/workflows/codeql.yaml`) scanning `python`, `actions` on every
  push, weekly and on demand; actions pinned to full commit SHAs.
- `examples/groundwork/`: a worked run of the full method against a public product.

### Changed

- CI pins its actions by commit SHA with a read-only token (#3), and runs the sourcing check on
  `examples/**/findings.md` too (#5).
- `.gitignore` keeps every product-specific file local: `config/target*.md` (except
  `config/target.example.md`), `findings/*-findings.md`, `vendor/` and the agent `MEMORY.md`.

## [0.1.0] - 2026-08-29

### Added

- Initial extraction of the grounded-persona-eval method from a real internal application: the
  three-phase method (`research-analyst`, `persona-synthesizer`, `live-evaluator` subagent
  definitions), `AGENTS.md` orchestration, `config/target.example.md`, and
  `scripts/verify_sourcing.py` (with tests) — the one mechanically-checkable rule, that every quote
  in a findings doc carries a source URL.
