# Research: Project Initialization

**Feature**: 001-project-init
**Date**: 2026-01-28

## CLI Framework Selection

**Decision**: Click

**Rationale**:
- Click is the de facto standard for Python CLI applications
- Provides automatic `--help` generation from docstrings
- Handles `--version` with a simple decorator
- Proper exit code handling built-in
- Errors automatically written to stderr
- Widely used, well-documented, stable API
- Single dependency with minimal footprint

**Alternatives Considered**:

| Framework | Pros | Cons | Why Rejected |
|-----------|------|------|--------------|
| argparse | Standard library, no deps | Verbose, manual help formatting | More boilerplate for same result |
| Typer | Type hints as CLI args | Built on Click, extra abstraction | Unnecessary layer for simple CLI |
| Fire | Auto-generates CLI from functions | Magic behavior, less control | Unpredictable output formatting |

## Package Structure

**Decision**: src-layout with `src/swhat/` package

**Rationale**:
- PEP 621 compliant (pyproject.toml as single source)
- src-layout prevents accidental imports of uninstalled package
- UV fully supports src-layout with editable installs
- Clean separation between package code and project files

**Alternatives Considered**:

| Layout | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Flat (swhat/ at root) | Simpler paths | Import confusion during dev | Can import uninstalled code |
| Namespace package | Multi-repo sharing | Complexity | Single project, not needed |

## Version Management

**Decision**: Single source of truth in `src/swhat/__init__.py`

**Rationale**:
- pyproject.toml uses `dynamic = ["version"]` with setuptools-scm or direct import
- Avoids version duplication
- Click's `@click.version_option()` reads from package metadata

**Implementation**:
```python
# src/swhat/__init__.py
__version__ = "0.1.0"

# pyproject.toml
[project]
version = "0.1.0"  # Or use dynamic versioning

# cli.py
@click.version_option(package_name="swhat")
```

## Dependencies

**Decision**: Minimal dependency set

| Dependency | Version | Purpose |
|------------|---------|---------|
| click | >=8.0 | CLI framework |

**Dev Dependencies** (optional, for development):

| Dependency | Version | Purpose |
|------------|---------|---------|
| ruff | >=0.1 | Linting and formatting |

## Python Version

**Decision**: Python 3.10+

**Rationale**:
- Constitution requirement
- Match patterns (3.10+) useful for future CLI parsing
- Union types without `Union` (3.10+)
- Broad platform support

## Entry Point

**Decision**: `swhat` command via `[project.scripts]`

**Implementation**:
```toml
[project.scripts]
swhat = "swhat.cli:main"
```

This allows:
- `swhat --help` - Show usage
- `swhat --version` - Show version
- Future subcommands: `swhat specify`, `swhat plan`, etc.
