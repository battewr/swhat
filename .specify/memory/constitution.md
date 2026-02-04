<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 → 1.0.0 (Initial ratification)
Modified principles: N/A (initial creation)
Added sections:
  - Principle I: CLI-First Design
  - Principle II: UV Package Standards
  - Principle III: AI Context Engineering
  - Principle IV: Simplicity & YAGNI
  - Section: Development Standards
  - Section: Quality Gates
  - Governance rules
Removed sections: N/A
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ (no updates needed - compatible)
  - .specify/templates/spec-template.md ✅ (no updates needed - compatible)
  - .specify/templates/tasks-template.md ✅ (no updates needed - test tasks optional)
Follow-up TODOs: None
-->

# swhat Constitution

## Core Principles

### I. CLI-First Design

All functionality MUST be exposed through a command-line interface.

- Every command MUST accept text input via stdin, arguments, or file paths
- Every command MUST produce structured output to stdout (JSON preferred, human-readable optional)
- Errors MUST be written to stderr with clear, actionable messages
- Commands MUST be composable—output of one command serves as input to another
- Exit codes MUST follow Unix conventions: 0 for success, non-zero for errors

**Rationale**: CLI-first design enables integration with AI agents, shell pipelines,
and automation workflows. It ensures the tool remains flexible and scriptable.

### II. UV Package Standards

The project MUST be installable via `uv` and follow modern Python packaging conventions.

- Project MUST use `pyproject.toml` as the single source of package metadata
- Dependencies MUST be declared with version constraints (minimum bounds required)
- The package MUST be installable in an isolated environment without system-level changes
- Entry points MUST be declared in `pyproject.toml` under `[project.scripts]`
- Python version MUST be 3.10 or higher

**Rationale**: UV provides fast, reliable dependency resolution. Following packaging
standards ensures the tool is distributable and reproducible across environments.

### III. AI Context Engineering

Commands that generate specifications, plans, or task lists MUST produce AI-consumable output.

- Output MUST be structured and parseable (Markdown with consistent heading hierarchy or JSON)
- Specifications MUST include explicit acceptance criteria that an AI can verify
- Plans MUST decompose work into discrete, independently implementable tasks
- Context documents MUST avoid ambiguity—use MUST/SHOULD/MAY language per RFC 2119
- Research artifacts MUST cite sources and distinguish facts from inferences

**Rationale**: The tool's primary purpose is to bridge human intent and AI execution.
Output quality directly determines AI implementation success.

### IV. Simplicity & YAGNI

Implement only what is needed for the current use case.

- Do NOT add features, abstractions, or configuration options "for future use"
- Prefer flat module structures over deep hierarchies
- Avoid premature optimization—measure before optimizing
- Three lines of similar code is acceptable; abstract only upon third repetition
- Configuration MUST have sensible defaults; require minimal setup for basic usage

**Rationale**: Complexity is the enemy of maintainability. Simple code is easier to
understand, debug, and extend when actual requirements emerge.

## Development Standards

- **Language**: Python 3.10+
- **Package Manager**: UV (for installation and dependency management)
- **Linting**: Ruff (for linting and formatting)
- **Type Hints**: Required for public APIs; optional for internal implementation
- **Testing**: No unit tests required at this time; integration tests via manual CLI
  validation are acceptable
- **Documentation**: Docstrings for public functions; inline comments only where logic
  is non-obvious

## Quality Gates

Before merging any feature:

1. **Installation Gate**: `uv pip install .` MUST succeed in a clean virtual environment
2. **CLI Gate**: All commands MUST execute without unhandled exceptions
3. **Output Gate**: Commands MUST produce valid JSON (when JSON mode enabled) or
   well-formed Markdown
4. **Help Gate**: `--help` MUST be implemented for all commands with usage examples

## Governance

This constitution defines the non-negotiable standards for the swhat project.

- **Precedence**: Constitution principles supersede ad-hoc decisions. When in doubt,
  consult this document.
- **Amendments**: Changes to this constitution require:
  1. A written proposal describing the change and rationale
  2. Review of impact on existing code and workflows
  3. Version increment following semantic versioning (see below)
- **Versioning Policy**:
  - MAJOR: Removal or redefinition of principles
  - MINOR: Addition of new principles or sections
  - PATCH: Clarifications, typos, non-semantic refinements
- **Compliance**: All pull requests SHOULD reference relevant constitution principles
  when applicable

**Version**: 1.0.0 | **Ratified**: 2026-01-28 | **Last Amended**: 2026-01-28
