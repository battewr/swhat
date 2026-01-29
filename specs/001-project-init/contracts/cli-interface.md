# CLI Interface Contract: swhat

**Version**: 0.1.0
**Date**: 2026-01-28

## Entry Point

**Command**: `swhat`

## Global Options

| Option | Short | Type | Required | Description |
|--------|-------|------|----------|-------------|
| `--help` | `-h` | flag | No | Display usage information and exit |
| `--version` | `-V` | flag | No | Display version number and exit |

## Behaviors

### Default (no arguments)

**Input**: `swhat`
**Output**: Same as `--help`
**Exit Code**: 0

### Help

**Input**: `swhat --help`
**Output** (stdout):
```
Usage: swhat [OPTIONS] COMMAND [ARGS]...

  swhat - Specification-driven development CLI

  Transform natural language feature descriptions into AI-implementable
  execution plans.

Options:
  -V, --version  Show the version and exit.
  -h, --help     Show this message and exit.
```
**Exit Code**: 0

### Version

**Input**: `swhat --version`
**Output** (stdout):
```
swhat, version 0.1.0
```
**Exit Code**: 0

### Invalid Command

**Input**: `swhat invalid-command`
**Output** (stderr):
```
Error: No such command 'invalid-command'.
```
**Exit Code**: 2 (Click's default for usage errors)

## Future Subcommands (placeholder)

These will be implemented in subsequent features:

| Command | Description |
|---------|-------------|
| `swhat specify` | Create feature specification |
| `swhat plan` | Generate implementation plan |
| `swhat tasks` | Generate task list |
| `swhat implement` | Execute implementation |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Usage/argument error |

## Output Streams

- **stdout**: Normal output (help text, version, command results)
- **stderr**: Error messages only
