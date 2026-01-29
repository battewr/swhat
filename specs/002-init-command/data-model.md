# Data Model: Init Command

**Feature**: 002-init-command
**Date**: 2026-01-28

## Entities

### Command File

A markdown file installed by `swhat init` that enables AI agents to execute the specification workflow.

| Attribute | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| path | Path | File system location | Relative to project root |
| content | string | Markdown command content | From specify-command template |
| agent | string | Target AI agent | "claude" or "roo" |

**Locations**:
- Claude Code: `.claude/commands/swhat.specify.md`
- Roo: `.roo/commands/swhat.specify.md`

### Project Directory Structure

Directories created by `swhat init`.

| Directory | Purpose | Created If |
|-----------|---------|------------|
| `.swhat/` | User workspace for specifications | Always |
| `.claude/commands/` | Claude Code custom commands | Always |
| `.roo/commands/` | Roo custom commands | Always |

## New Template

### specify-command

A new template to be added to `templates.py` registry.

**Name**: `specify-command`
**Description**: "AI agent command for specification workflow"
**Content**: From `tmp/speckit.specify.md` (the edited version)

```python
# Add to TEMPLATES dict in templates.py
"specify-command": (SPECIFY_COMMAND_CONTENT, "AI agent command for specification workflow"),
```

## Data Flow

```
swhat init
    │
    ├── Create .swhat/ directory
    │
    ├── Get specify-command template from registry
    │
    ├── Create .claude/commands/ directory
    │   └── Write swhat.specify.md
    │
    └── Create .roo/commands/ directory
        └── Write swhat.specify.md
```

## Validation Rules

| Rule | Enforcement |
|------|-------------|
| Directory must be writable | Check before creating, error with clear message |
| Template must exist in registry | Use existing get_template(); error if None |
| Files are always overwritten | No existence check before write |

## State Transitions

N/A - Init is a one-shot operation that creates/updates files.
