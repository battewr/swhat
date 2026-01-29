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

## Usage

Open **Claude CLI** or **Roo** at the root of your initialized project directory (where you ran `swhat init`). The agent must be launched from this location to access the swhat commands and skills.

### Automatic Specification Detection

The swhat skills automatically detect complex feature requests during conversation. When you ask Claude to implement, build, create, or add a new feature, the `swhat-feature-workflow` skill activates and guides you through requirements clarification before generating code.

Example prompts that trigger automatic specification:
- "Add user authentication to the app"
- "Build a REST API for managing orders"
- "Create a notification system"

### Manual Commands

#### `/swhat.specify`

Use for direct access to the specification engine:

```
/swhat.specify <feature-description>
```

This creates or updates a feature specification from your natural language description in `.swhat/<feature>/spec.md`.

#### `/swhat.plan`

Use after specification to generate an implementation plan:

```
/swhat.plan
```

This reads the current spec and generates a technical implementation plan in `.swhat/<feature>/plan.md`, including:
- Architecture decisions
- File changes required
- Implementation sequence
- Risk considerations

### Agent Skills (Automatic Detection)

The `swhat-feature-workflow` skill monitors your conversation and automatically activates when it detects complex feature requests. This happens transparently - you don't need to invoke any command.

**What triggers automatic detection:**
- Requests to "implement", "build", "create", or "add" new functionality
- Multi-step features requiring architectural decisions
- Features that benefit from upfront planning

**What the skill does:**
1. Pauses before writing code
2. Asks clarifying questions about requirements
3. Generates a specification for your approval
4. Optionally generates an implementation plan
5. Proceeds with implementation only after confirmation

**When it does NOT activate:**
- Bug fixes
- Small tweaks or configuration changes
- Documentation updates
- Simple refactoring

You can always bypass automatic detection by starting your request with "just" or "quickly" (e.g., "just add a console.log").

## Best Practices

1. **Start with a clear description** - The more context you provide, the better the specification
2. **Answer clarification questions** - This improves spec quality and reduces implementation issues
3. **Review specs before implementation** - Catch requirement gaps early
