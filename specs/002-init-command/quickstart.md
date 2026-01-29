# Quickstart: Init Command

**Feature**: 002-init-command
**Date**: 2026-01-28

## Overview

The `swhat init` command sets up a project for specification-driven development by creating necessary directories and installing AI agent commands.

## Usage

### Initialize a Project

```bash
# Navigate to your project root
cd /path/to/your/project

# Run init
swhat init
```

### Expected Output

```
Initializing swhat in current directory...
  Created .swhat/
  Created .claude/commands/swhat.specify.md
  Created .roo/commands/swhat.specify.md
Initialization complete! You can now use /swhat.specify in Claude Code or Roo.
```

### Re-initialize (Update)

```bash
# Run init again to update command files
swhat init
```

```
Initializing swhat in current directory...
  .swhat/ already exists
  Updated .claude/commands/swhat.specify.md
  Updated .roo/commands/swhat.specify.md
Initialization complete! You can now use /swhat.specify in Claude Code or Roo.
```

### Get Help

```bash
swhat init --help
```

## After Initialization

### In Claude Code

```
/swhat.specify Add user authentication with OAuth2
```

### In Roo

```
/swhat.specify Add user authentication with OAuth2
```

## Directory Structure Created

```
your-project/
├── .swhat/                          # User workspace (empty initially)
├── .claude/
│   └── commands/
│       └── swhat.specify.md         # Claude Code command
└── .roo/
    └── commands/
        └── swhat.specify.md         # Roo command
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - initialization complete |
| 1 | Error - could not create directories or write files |

## Troubleshooting

**Error: Permission denied**
- Ensure you have write permissions in the current directory
- Try running from a different location

**Error: Template not found**
- This indicates a bug in swhat installation
- Try reinstalling: `uv pip install --force-reinstall swhat`
