# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-08-29

### Added

- Initial extraction of the grounded-persona-eval method from a real internal application: the
  three-phase method (`research-analyst`, `persona-synthesizer`, `live-evaluator` subagent
  definitions), `AGENTS.md` orchestration, `config/target.example.md`, and
  `scripts/verify_sourcing.py` (with tests) — the one mechanically-checkable rule, that every quote
  in a findings doc carries a source URL.
