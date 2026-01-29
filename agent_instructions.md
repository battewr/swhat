# Agent Instructions for swhat

This document describes how to use the **swhat** CLI tool for specification-driven development.

## Installation

```bash
# Clone and install
git clone <repository-url>
cd swhat
./clean_build.sh        # Unix/Linux/macOS
# OR
.\clean_build.ps1       # Windows PowerShell
```

Alternatively, install directly with UV:

```bash
uv pip install -e .
```

Verify installation:

```bash
swhat --version
swhat --help
```

## Setup

Initialize swhat in your project directory:

```bash
cd /path/to/your/project
swhat init
```

This creates the necessary `.specify/` directory structure and automatically installs the swhat commands and skills for both **Claude CLI** and **Roo**.

## Usage

The following commands and skills are executed within **Claude CLI** or **Roo** during an agentic coding session.

### Automatic Specification Detection

The swhat skills automatically detect complex feature requests during conversation. When you ask Claude to implement, build, create, or add a new feature, the `swhat-feature-workflow` skill activates and guides you through requirements clarification before generating code.

Example prompts that trigger automatic specification:
- "Add user authentication to the app"
- "Build a REST API for managing orders"
- "Create a notification system"

### Manual Specification Access

Use the `/swhat.specify` command for direct access to the specification engine:

```
/swhat.specify <feature-description>
```

This creates or updates a feature specification from your natural language description.

## Best Practices

1. **Start with a clear description** - The more context you provide, the better the specification
2. **Answer clarification questions** - This improves spec quality and reduces implementation issues
3. **Review specs before implementation** - Catch requirement gaps early
