# Implementation Plan: Template Command

**Branch**: `001-template-command` | **Date**: 2026-01-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-template-command/spec.md`

## Summary

Add a `swhat template` subcommand that outputs specification templates stored as Python strings. Initial release includes two templates: "specification" (the feature spec template) and "specification-checklist" (quality validation checklist). Templates are embedded in source code to ensure portability without external file dependencies.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Click 8.0+ (existing CLI framework)
**Storage**: N/A (templates embedded in Python source as string constants)
**Testing**: Manual CLI validation (per constitution)
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Single CLI package
**Performance Goals**: Template output in <1 second
**Constraints**: Templates must be embedded in source (no external file reads at runtime)
**Scale/Scope**: 2 templates initially; architecture supports future additions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. CLI-First Design | PASS | Command outputs to stdout, errors to stderr, exit codes follow Unix conventions |
| II. UV Package Standards | PASS | No new dependencies; uses existing Click; entry point already in pyproject.toml |
| III. AI Context Engineering | PASS | Templates are structured Markdown; output is parseable |
| IV. Simplicity & YAGNI | PASS | Simple dict-based registry; no abstraction until third template type |

### Quality Gates Checklist

- [x] Installation Gate: `uv pip install .` succeeds
- [x] CLI Gate: `swhat template specification` runs without exceptions
- [x] Output Gate: Template content is well-formed Markdown
- [x] Help Gate: `swhat template --help` shows usage

## Project Structure

### Documentation (this feature)

```text
specs/001-template-command/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (N/A - no API)
└── tasks.md             # Phase 2 output (/speckit.tasks command)
```

### Source Code (repository root)

```text
src/swhat/
├── __init__.py          # Package version (existing)
├── cli.py               # CLI entry point - add template subcommand (existing)
└── templates.py         # NEW: Template registry and content strings
```

**Structure Decision**: Single module structure. Templates live in a dedicated `templates.py` module to keep `cli.py` focused on command definitions. The registry is a simple dict mapping names to (content, description) tuples.

## Complexity Tracking

> No violations. Design follows all constitution principles.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | - | - |
