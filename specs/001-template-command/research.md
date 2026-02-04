# Research: Template Command

**Feature**: 001-template-command
**Date**: 2026-01-28

## Summary

This feature requires minimal research. All technical decisions are straightforward given the existing codebase patterns and constitution requirements.

## Decision Log

### D1: Template Storage Mechanism

**Decision**: Store templates as multi-line string constants in a dedicated Python module (`templates.py`)

**Rationale**:
- Meets FR-004 requirement: templates embedded in source code
- No external file I/O at runtime
- Templates are version-controlled with the code
- Simple to add new templates: add another constant + registry entry

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| Read from `importlib.resources` | Still requires bundling files; more complex |
| Load from `.specify/templates/` at runtime | Violates FR-004; depends on working directory |
| Store in `__init__.py` | Clutters package metadata |

### D2: Template Registry Structure

**Decision**: Use a simple `dict[str, tuple[str, str]]` mapping name → (content, description)

**Rationale**:
- YAGNI: No need for classes or abstractions with only 2 templates
- Easy iteration for `--list` output
- O(1) lookup by name
- Trivially extensible

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| `@dataclass Template` | Over-engineering for 2 fields |
| JSON/YAML config | Adds parsing complexity; violates embedded storage requirement |
| Plugin system | Massive over-engineering; no current need |

### D3: Case-Insensitivity Implementation

**Decision**: Normalize input to lowercase before registry lookup

**Rationale**:
- Simple one-line implementation: `name.lower()`
- Matches spec assumption
- User-friendly (no exact-case errors)

### D4: Error Output Handling

**Decision**: Use `click.echo(..., err=True)` for errors, exit with code 1

**Rationale**:
- Constitution Principle I requires errors to stderr
- Click provides built-in support
- Consistent with Unix conventions

## Open Questions

None. All technical decisions are resolved.

## Dependencies

No new dependencies required. Uses existing Click 8.0+ from `pyproject.toml`.
