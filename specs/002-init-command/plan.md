# Implementation Plan: Init Command

**Branch**: `002-init-command` | **Date**: 2026-01-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-init-command/spec.md`

## Summary

Add a `swhat init` subcommand that initializes a project for specification-driven development. The command creates the `.swhat/` directory, installs AI agent command files to `.claude/commands/` and `.roo/commands/`, embedding the specification workflow from stored templates.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Click 8.0+ (existing CLI framework)
**Storage**: File system (creates directories and writes markdown files)
**Testing**: Manual CLI validation (per constitution)
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Single CLI package
**Performance Goals**: Initialization in <5 seconds
**Constraints**: Must work in any writable directory
**Scale/Scope**: Creates 3 directories, writes 2 command files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Evidence |
|-----------|--------|----------|
| I. CLI-First Design | PASS | Command uses arguments, outputs to stdout/stderr, Unix exit codes |
| II. UV Package Standards | PASS | No new dependencies; uses existing Click |
| III. AI Context Engineering | PASS | Generated command files are structured Markdown for AI agents |
| IV. Simplicity & YAGNI | PASS | Simple directory creation and file writing; no abstractions |

### Quality Gates Checklist

- [x] Installation Gate: `uv pip install .` succeeds
- [x] CLI Gate: `swhat init` runs without exceptions
- [x] Output Gate: Generated command files are well-formed Markdown
- [x] Help Gate: `swhat init --help` shows usage

## Project Structure

### Documentation (this feature)

```text
specs/002-init-command/
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
├── cli.py               # CLI entry point - add init subcommand (existing)
├── templates.py         # Template registry (existing) - add specify command template
└── init.py              # NEW: Init command implementation
```

**Structure Decision**: Single module structure. Init logic in dedicated `init.py` module to keep `cli.py` focused on command routing. The specify command template will be added to `templates.py` alongside existing templates.

## Complexity Tracking

> No violations. Design follows all constitution principles.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| (none) | - | - |
