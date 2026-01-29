# Quickstart: Project Initialization

**Feature**: 001-project-init
**Date**: 2026-01-28

## Prerequisites

- Python 3.10 or higher
- UV package manager installed (`pip install uv` or via pipx)

## Installation

### From Source (Development)

```bash
# Clone the repository
git clone <repository-url>
cd swhat

# Install in editable mode
uv pip install -e .

# Verify installation
swhat --version
```

### From Source (Standard)

```bash
# Install without editable mode
uv pip install .

# Verify installation
swhat --version
```

## Verification Steps

### 1. Check Installation

```bash
swhat --version
# Expected: swhat, version 0.1.0
```

### 2. View Help

```bash
swhat --help
# Expected: Usage information with available options
```

### 3. Test Default Behavior

```bash
swhat
# Expected: Same output as --help
```

### 4. Test Error Handling

```bash
swhat nonexistent-command
# Expected: Error message to stderr, exit code 2
echo $?
# Expected: 2
```

## Validation Checklist

- [ ] `uv pip install -e .` completes without errors
- [ ] `swhat --version` displays version number
- [ ] `swhat --help` displays usage information
- [ ] `swhat` (no args) shows help
- [ ] Invalid command produces error to stderr
- [ ] Exit codes are correct (0 for success, non-zero for errors)

## Troubleshooting

### "command not found: swhat"

The package isn't installed or the Python bin directory isn't in PATH.

```bash
# Check if installed
uv pip show swhat

# If using virtual environment, ensure it's activated
source .venv/bin/activate
```

### Python version mismatch

```bash
python --version
# Must be 3.10 or higher
```

### UV not found

```bash
# Install UV
pip install uv
# Or via pipx
pipx install uv
```
