# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**swhat** is a Python CLI tool for specification-driven development. It transforms natural language feature descriptions into AI-implementable execution plans through a structured workflow: specification → planning → task generation → implementation.

## Build & Development Commands

### Unix (Linux/macOS)

```bash
# Quick build (recommended)
./clean_build.sh

# CMake build workflow
cmake -B build                        # Configure
cmake --build build --target build    # Build package (dist/)
cmake --build build --target dev      # Dev install (editable)
cmake --build build --target lint     # Run linter
cmake --build build --target format   # Format code
cmake --build build --target pyclean  # Clean artifacts
cmake --install build                 # Install to system
```

### Windows (PowerShell)

```powershell
# Quick build (recommended)
.\clean_build.ps1

# CMake build workflow (same commands as Unix)
cmake -B build                        # Configure
cmake --build build --target build    # Build package (dist/)
cmake --build build --target dev      # Dev install (editable)
cmake --build build --target lint     # Run linter
cmake --build build --target format   # Format code
cmake --build build --target pyclean  # Clean artifacts

# If PowerShell execution is restricted
powershell -ExecutionPolicy Bypass -File clean_build.ps1
```

### Manual Commands

```bash
# Unix
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
ruff check src/
ruff format src/
```

### CLI Commands

```bash
swhat --help
swhat --version
```

## Architecture

This project uses the **Specify** workflow template. The development flow is:

1. `/speckit.specify <description>` - Create feature spec from natural language
2. `/speckit.plan` - Generate technical plan with research, data models, contracts
3. `/speckit.tasks` - Break plan into executable task list
4. `/speckit.implement` - Execute tasks phase by phase

### Key Directories

- `src/swhat/` - Main package source code
  - `__init__.py` - Package version
  - `cli.py` - CLI entry point (Click-based)
- `.specify/memory/constitution.md` - Project principles and quality gates (read this first)
- `.specify/templates/` - Templates for specs, plans, tasks
- `.claude/commands/` - Slash command definitions for the workflow
- `specs/<###-feature>/` - Feature-specific artifacts (spec.md, plan.md, tasks.md, etc.)

### Constitution Principles

The constitution at `.specify/memory/constitution.md` defines non-negotiable standards:

1. **CLI-First**: All functionality via CLI, composable stdin/stdout, Unix exit codes
2. **UV Package Standards**: pyproject.toml, Python 3.10+, declared dependencies
3. **AI Context Engineering**: Structured output (JSON/Markdown), explicit acceptance criteria
4. **Simplicity & YAGNI**: No premature abstraction, sensible defaults

### Quality Gates

Before merging: installation must work (`uv pip install .`), CLI commands must not throw unhandled exceptions, `--help` must be implemented for all commands.

## Development Standards

- Python 3.10+
- Package manager: UV
- Linting: Ruff
- Type hints required for public APIs
- No unit tests required currently; manual CLI validation acceptable

## Source Structure

```
src/swhat/
├── __init__.py    # Package version (__version__ = "0.1.0")
└── cli.py         # CLI entry point with Click group
```

## Active Technologies

- Python 3.10+ with Click 8.0+ for CLI framework

## Recent Changes
- 002-windows-support: Added PowerShell 5.1+ (Windows default), CMake 3.16+ + UV (cross-platform), CMake (cross-platform)
