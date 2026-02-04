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
swhat init                    # Initialize project for swhat workflow
swhat template --list         # List available templates
swhat template specification  # Output specification template
swhat template plan           # Output plan template
```

## Architecture

This project uses the **Specify** workflow template. The development flow is:

1. `/swhat.specify <description>` - Create feature spec from natural language
2. `/swhat.plan` - Generate technical implementation plan
3. Implementation - Execute the plan (manual or via Option 3 in Next Steps)

### Key Directories

- `src/swhat/` - Main package source code
  - `__init__.py` - Package version
  - `cli.py` - CLI entry point (Click-based)
  - `init.py` - Project initialization
  - `templates.py` - Embedded templates
  - `commands/` - Agent command/skill content files
- `.specify/memory/constitution.md` - Project principles and quality gates (read this first)
- `.specify/templates/` - Templates for specs, plans, tasks
- `.claude/commands/` - Slash command definitions (swhat.specify.md, swhat.plan.md)
- `.swhat/<feature>/` - Feature-specific artifacts (spec.md, plan.md, etc.)

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
├── __init__.py    # Package version (__version__ = "0.3.0")
├── cli.py         # CLI entry point with Click group
├── init.py        # Project initialization logic
├── templates.py   # Embedded template content
└── commands/      # Agent command/skill content
    ├── claude_specify_command.py
    ├── claude_plan_command.py
    ├── claude_feature_skill.py
    ├── roo_specify_command.py
    ├── roo_plan_command.py
    └── roo_feature_skill.py
```

## Active Technologies
- Python 3.10+ + Click 8.0+ (existing CLI framework) (001-template-command)
- N/A (templates embedded in Python source as string constants) (001-template-command)

- Python 3.10+ with Click 8.0+ for CLI framework

## Recent Changes
- 002-windows-support: Added PowerShell 5.1+ (Windows default), CMake 3.16+ + UV (cross-platform), CMake (cross-platform)
