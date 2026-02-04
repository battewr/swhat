# Research: Init Command

**Feature**: 002-init-command
**Date**: 2026-01-28

## Summary

This feature requires minimal research. The technical decisions are straightforward given the existing codebase patterns and the user's explicit guidance to use `tmp/speckit.specify.md` as the command template source.

## Decision Log

### D1: Command Template Storage

**Decision**: Add a new template "specify-command" to the existing `templates.py` registry, containing the content from `tmp/speckit.specify.md`.

**Rationale**:
- Follows the established pattern from 001-template-command
- Templates are embedded in source code (no external file dependencies)
- Allows `swhat init` to retrieve content via existing infrastructure

**Alternatives Considered**:
| Alternative | Rejected Because |
|-------------|-----------------|
| Read from `tmp/` at runtime | Violates embedded storage principle; file may not exist |
| Hardcode in `init.py` | Duplicates template storage pattern; harder to maintain |
| Use importlib.resources | More complex; existing pattern works |

### D2: Directory Creation Approach

**Decision**: Use `pathlib.Path.mkdir(parents=True, exist_ok=True)` for all directory creation.

**Rationale**:
- Cross-platform compatible
- Handles nested directories (`.claude/commands/`)
- Idempotent - safe for re-initialization
- Standard Python library, no new dependencies

### D3: File Writing Behavior

**Decision**: Always overwrite command files; never touch other files in `.swhat/`.

**Rationale**:
- FR-008 requires overwrite for re-initialization (update behavior)
- FR-009 requires preserving user files in `.swhat/`
- Only writing to specific known paths (command files) achieves both

### D4: Command File Locations

**Decision**: Write identical content to both:
- `.claude/commands/swhat.specify.md`
- `.roo/commands/swhat.specify.md`

**Rationale**:
- Both AI agents use the same markdown command format
- Single source of truth (template) with multiple outputs
- Users may use either or both agents

### D5: Output Messaging

**Decision**: Print human-readable progress messages to stdout, errors to stderr.

**Rationale**:
- Constitution Principle I requires stdout/stderr separation
- Users expect feedback during init
- Simple `click.echo()` for progress, `click.echo(..., err=True)` for errors

## Open Questions

None. All technical decisions are resolved.

## Dependencies

No new dependencies required. Uses existing:
- Click 8.0+ (CLI framework)
- pathlib (standard library)
