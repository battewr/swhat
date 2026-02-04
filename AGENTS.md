# AGENTS.md

Instructions for AI agents working on the swhat codebase.

## Project Overview

**swhat** is a Python CLI tool for specification-driven development. It transforms natural language feature descriptions into AI-implementable execution plans through a structured workflow.

**Purpose**: Bridge human intent and AI execution by producing structured, unambiguous specifications that AI agents can implement without guesswork.

## Core Principles (Non-Negotiable)

These principles are defined in `.specify/memory/constitution.md` and supersede ad-hoc decisions.

### I. CLI-First Design

- All functionality MUST be exposed via command-line interface
- Commands accept input via stdin, arguments, or file paths
- Output goes to stdout (JSON preferred); errors to stderr
- Commands MUST be composable (output of one feeds another)
- Exit codes: 0 = success, non-zero = error

### II. UV Package Standards

- Use `pyproject.toml` as the single source of package metadata
- Dependencies declared with version constraints
- Package installable via `uv pip install .` in isolated environment
- Entry points declared under `[project.scripts]`
- Python 3.10+ required

### III. AI Context Engineering

- Output MUST be structured and parseable (Markdown with consistent headings or JSON)
- Specifications include explicit, verifiable acceptance criteria
- Plans decompose work into discrete, independently implementable tasks
- Use MUST/SHOULD/MAY language per RFC 2119

### IV. Simplicity & YAGNI

- Implement only what is needed NOW
- No features "for future use"
- Prefer flat module structures over deep hierarchies
- Abstract only upon third repetition
- Sensible defaults; minimal setup for basic usage

## Development Workflow

The project uses a **Specify** workflow with these phases:

```
Feature Description → Specification → Plan → Tasks → Implementation
```

### Slash Commands (for AI agents)

**swhat commands** (installed via `swhat init`):

| Platform | Command | Purpose |
|----------|---------|---------|
| Claude Code | `/swhat.specify <desc>` | Create feature spec from natural language |
| Claude Code | `/swhat.plan` | Generate technical implementation plan |
| Roo Code | `/swhat-specify <desc>` | Create feature spec from natural language |
| Roo Code | `/swhat-plan` | Generate technical implementation plan |

**Legacy speckit commands** (if using speckit templates):

| Command | Purpose |
|---------|---------|
| `/speckit.specify <desc>` | Create feature spec from natural language |
| `/speckit.plan` | Generate technical implementation plan |
| `/speckit.tasks` | Break plan into executable task list |
| `/speckit.implement` | Execute tasks phase by phase |

### Workflow Artifacts

Artifacts are stored in `specs/<feature-id>/` or `.swhat/<feature-id>/`:

- `spec.md` - Feature specification (WHAT and WHY)
- `plan.md` - Technical implementation plan (HOW)
- `tasks.md` - Ordered task list with dependencies
- `requirements.md` - Quality validation checklist

## Quality Gates

Before merging any feature:

1. **Installation Gate**: `uv pip install .` succeeds in clean venv
2. **CLI Gate**: All commands execute without unhandled exceptions
3. **Output Gate**: Commands produce valid JSON or well-formed Markdown
4. **Help Gate**: `--help` implemented for all commands with examples

## Code Standards

- **Language**: Python 3.10+
- **Package Manager**: UV
- **Linting**: Ruff (`ruff check src/` and `ruff format src/`)
- **Type Hints**: Required for public APIs; optional for internals
- **Testing**: Manual CLI validation (no unit tests required currently)
- **Docstrings**: Public functions only; inline comments where non-obvious

## Project Structure

```
swhat/
├── src/swhat/
│   ├── __init__.py      # Package version
│   ├── cli.py           # CLI entry point (Click-based)
│   ├── templates.py     # Embedded template content
│   ├── init.py          # Project initialization logic
│   └── commands/        # Agent command/skill content
│       ├── claude_specify_command.py
│       ├── claude_plan_command.py
│       ├── claude_feature_skill.py
│       ├── roo_specify_command.py
│       ├── roo_plan_command.py
│       └── roo_feature_skill.py
├── .specify/
│   ├── memory/
│   │   └── constitution.md  # Project principles (READ FIRST)
│   └── templates/           # Workflow templates
├── .claude/
│   ├── commands/            # Claude Code slash commands
│   └── skills/              # Auto-triggering skills
├── specs/                   # Feature artifacts
├── pyproject.toml           # Package metadata
└── CMakeLists.txt           # Cross-platform build system
```

## CLI Commands

```bash
swhat --help              # Show available commands
swhat --version           # Show version
swhat template --list     # List available templates
swhat template <name>     # Output template content to stdout
swhat init                # Initialize project for swhat workflow
```

### Available Templates

- `specification` - Feature specification template
- `specification-checklist` - Spec quality validation checklist
- `plan` - Implementation plan template

## Build Commands

### Quick Build (Recommended)

```bash
# Unix
./clean_build.sh

# Windows PowerShell
.\clean_build.ps1
```

### CMake Targets

```bash
cmake -B build                        # Configure
cmake --build build --target build    # Build package
cmake --build build --target dev      # Dev install (editable)
cmake --build build --target lint     # Run Ruff linter
cmake --build build --target format   # Format code
cmake --build build --target pyclean  # Clean artifacts
```

## Key Implementation Details

### Templates Are Embedded

Templates are stored as string constants in `src/swhat/templates.py`, not external files. This avoids file system dependencies and simplifies distribution.

### Initialization Creates Agent Files

`swhat init` creates:
- `.swhat/` - User workspace directory
- `.claude/commands/swhat.specify.md` - Claude Code specify command
- `.claude/commands/swhat.plan.md` - Claude Code plan command
- `.claude/skills/swhat-feature-workflow/SKILL.md` - Auto-trigger skill
- `.roo/commands/swhat-specify.md` - Roo Code specify command
- `.roo/commands/swhat-plan.md` - Roo Code plan command
- `.roo/skills/swhat-feature-workflow/SKILL.md` - Auto-trigger skill

### Specification Guidelines

When creating specifications:

1. Focus on **WHAT** users need and **WHY**
2. Avoid implementation details (no tech stack, APIs, code structure)
3. Write for business stakeholders, not developers
4. Maximum 3 `[NEEDS CLARIFICATION]` markers per spec
5. Make informed guesses using industry standards for unspecified details
6. Success criteria must be measurable and technology-agnostic

### Success Criteria Examples

**Good** (user-focused, measurable):
- "Users can complete checkout in under 3 minutes"
- "System supports 10,000 concurrent users"
- "95% of searches return results in under 1 second"

**Bad** (implementation-focused):
- "API response time under 200ms"
- "Database handles 1000 TPS"
- "Redis cache hit rate above 80%"

## Common Tasks

### Adding a New Template

1. Add template content as a string constant in `src/swhat/templates.py`
2. Register in the `TEMPLATES` dict with name and description
3. Template is immediately available via `swhat template <name>`

### Adding a New CLI Command

1. Add command function in `src/swhat/cli.py` using `@main.command()` decorator
2. Include `--help` with usage examples
3. Follow Click conventions for options and arguments
4. Ensure composable stdin/stdout behavior

### Modifying the Constitution

Changes to `.specify/memory/constitution.md` require:
1. Written proposal with rationale
2. Impact review on existing code
3. Version increment (MAJOR for removals, MINOR for additions, PATCH for clarifications)

## Error Handling

- Write errors to stderr with clear, actionable messages
- Use non-zero exit codes for failures
- Never swallow exceptions silently
- Provide context in error messages (what failed, what to do)

## What NOT to Do

- Don't add features without explicit requirements
- Don't create abstractions for one-time operations
- Don't add configuration options "for future use"
- Don't include implementation details in specifications
- Don't skip the specification phase for new features
- Don't break CLI composability (always support stdin/stdout/pipes)
