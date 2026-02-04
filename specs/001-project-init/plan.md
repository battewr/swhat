# Implementation Plan: Project Initialization

**Branch**: `001-project-init` | **Date**: 2026-01-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-project-init/spec.md`

## Summary

Initialize the swhat CLI project with a complete Python package structure: pyproject.toml for UV-based installation, src/ directory with CLI module, README.md for documentation, and updated CLAUDE.md for AI agent context. The CLI will use Click for argument parsing and provide `--help` and `--version` flags.

## Technical Context

**Language/Version**: Python 3.10+
**Primary Dependencies**: Click (CLI framework)
**Storage**: N/A (no persistence in this feature)
**Testing**: Manual CLI validation (no automated tests per spec)
**Target Platform**: Cross-platform (Linux, macOS, Windows)
**Project Type**: Single project
**Performance Goals**: CLI responds within 1 second
**Constraints**: Minimal dependencies, single-file CLI entry point acceptable
**Scale/Scope**: Single developer tool, local execution

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| **I. CLI-First Design** | All functionality via CLI, stdin/stdout, Unix exit codes | ✅ PASS - CLI entry point with --help, --version, stderr for errors |
| **II. UV Package Standards** | pyproject.toml, Python 3.10+, entry points declared | ✅ PASS - Using pyproject.toml with [project.scripts] |
| **III. AI Context Engineering** | Structured output, explicit criteria | ✅ PASS - CLAUDE.md provides AI context |
| **IV. Simplicity & YAGNI** | Only what's needed, flat structure, sensible defaults | ✅ PASS - Minimal structure, single CLI module |

**Quality Gates**:
- Installation Gate: `uv pip install .` → Will verify
- CLI Gate: `swhat --help` executes without exception → Will verify
- Output Gate: Help text is well-formed → Will verify
- Help Gate: --help implemented → Required by FR-005

## Project Structure

### Documentation (this feature)

```text
specs/001-project-init/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output (CLI interface spec)
```

### Source Code (repository root)

```text
src/
└── swhat/
    ├── __init__.py      # Package version
    └── cli.py           # CLI entry point (Click-based)

pyproject.toml           # Package manifest with [project.scripts]
README.md                # Project documentation
CLAUDE.md                # AI agent instructions (update existing)
```

**Structure Decision**: Single project with flat src/swhat/ layout. No tests/ directory per spec requirement ("no testing atm"). The CLI is simple enough that a single cli.py file is sufficient—no services/ or models/ directories needed for this initialization feature.

## Complexity Tracking

> No violations. Structure follows Simplicity & YAGNI principle.
