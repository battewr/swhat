# Quickstart: Template Command

**Feature**: 001-template-command
**Date**: 2026-01-28

## Overview

The `swhat template` command outputs specification templates for reference. Templates are embedded in the package and available offline.

## Usage

### View a Template

```bash
# Output the specification template
swhat template specification

# Output the specification checklist
swhat template specification-checklist
```

### List Available Templates

```bash
# Show all available templates (both commands produce identical output)
swhat template
swhat template --list
```

### Save Template to File

```bash
# Pipe to a file
swhat template specification > my-spec.md

# Use with other commands
swhat template specification | grep "##"
```

### Get Help

```bash
swhat template --help
```

## Available Templates

| Name | Description |
|------|-------------|
| specification | Feature specification template with user stories, requirements, and success criteria |
| specification-checklist | Quality validation checklist for reviewing specifications |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - template output or list displayed |
| 1 | Error - invalid template name |

## Examples

**Example 1: Start a new spec**
```bash
swhat template specification > specs/my-feature/spec.md
```

**Example 2: Review spec quality**
```bash
swhat template specification-checklist > specs/my-feature/checklist.md
```

**Example 3: Check what templates exist**
```bash
$ swhat template --list
Available templates:
  specification             Feature specification template
  specification-checklist   Spec quality validation checklist
```
