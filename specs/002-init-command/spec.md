# Feature Specification: Init Command

**Feature Branch**: `002-init-command`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "swhat init command to install Roo/Claude commands, create .swhat directory, and write agent skill"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Initialize Project for Specification Workflow (Priority: P1)

A developer has installed swhat and wants to set up their project to use the specification-driven development workflow. They run `swhat init` in their project root, and the command creates the necessary directory structure and installs AI agent commands so they can immediately start using `/swhat.specify` in their preferred AI coding assistant.

**Why this priority**: This is the core functionality - without initialization, users cannot use swhat's specification workflow in their projects.

**Independent Test**: Can be fully tested by running `swhat init` in an empty directory and verifying the `.swhat/` directory and command files are created.

**Acceptance Scenarios**:

1. **Given** a project directory without swhat initialization, **When** the user runs `swhat init`, **Then** a `.swhat/` directory is created in the project root
2. **Given** a project directory without swhat initialization, **When** the user runs `swhat init`, **Then** Claude Code command files are written to `.claude/commands/`
3. **Given** a project directory without swhat initialization, **When** the user runs `swhat init`, **Then** Roo command files are written to `.roo/commands/`

---

### User Story 2 - Use Specification Command After Init (Priority: P2)

After running `swhat init`, a developer opens their AI coding assistant (Claude Code or Roo) and wants to create a feature specification. They type `/swhat.specify <feature description>` and the AI agent uses the installed command to generate a structured specification.

**Why this priority**: This validates that the installed commands actually work with the AI agents - the primary purpose of init.

**Independent Test**: Can be fully tested by running `swhat init`, then using the `/swhat.specify` command in Claude Code or Roo.

**Acceptance Scenarios**:

1. **Given** a project where `swhat init` has been run, **When** the user invokes `/swhat.specify` in Claude Code, **Then** the specification workflow executes using the embedded templates
2. **Given** a project where `swhat init` has been run, **When** the user invokes `/swhat.specify` in Roo, **Then** the specification workflow executes using the embedded templates

---

### User Story 3 - Re-initialize Existing Project (Priority: P3)

A developer has previously run `swhat init` but wants to update to the latest command definitions (perhaps after upgrading swhat). They run `swhat init` again and the command updates the files without losing any user data.

**Why this priority**: Important for maintenance but not required for initial usage.

**Independent Test**: Can be fully tested by running `swhat init` twice and verifying files are updated without errors.

**Acceptance Scenarios**:

1. **Given** a project where `swhat init` has already been run, **When** the user runs `swhat init` again, **Then** the command files are updated to the latest version
2. **Given** a project with existing `.swhat/` directory, **When** the user runs `swhat init`, **Then** any user-created files in `.swhat/` are preserved

---

### Edge Cases

- What happens when the user runs `swhat init` in a directory without write permissions?
- What happens if `.claude/commands/` or `.roo/commands/` directories already exist with conflicting files?
- What happens if the user runs `swhat init` outside of a project directory (e.g., in `/` or home)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create a `.swhat/` directory in the current working directory when it doesn't exist
- **FR-002**: System MUST create `.claude/commands/` directory structure if it doesn't exist
- **FR-003**: System MUST create `.roo/commands/` directory structure if it doesn't exist
- **FR-004**: System MUST write the `swhat.specify.md` command file to `.claude/commands/`
- **FR-005**: System MUST write the `swhat.specify.md` command file to `.roo/commands/`
- **FR-006**: System MUST embed the specification workflow content from `tmp/speckit.specify.md` into the command files
- **FR-007**: System MUST use the `swhat template` command internally to retrieve template content for embedding
- **FR-008**: System MUST overwrite existing command files when re-initializing (update behavior)
- **FR-009**: System MUST preserve user-created files in `.swhat/` directory during re-initialization
- **FR-010**: System MUST return exit code 0 on successful initialization
- **FR-011**: System MUST return non-zero exit code and display error message if initialization fails
- **FR-012**: System MUST provide `--help` documentation for the init subcommand

### Key Entities

- **Command File**: A markdown file containing AI agent instructions, placed in the appropriate commands directory for each supported AI agent (Claude Code, Roo).
- **Project Directory**: The working directory where `swhat init` is executed, which becomes the root for all swhat-related files.
- **Agent Skill**: The embedded workflow instructions that enable AI agents to execute the specification process.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can complete project initialization in under 5 seconds
- **SC-002**: After initialization, the `/swhat.specify` command is immediately available in supported AI agents
- **SC-003**: Re-initialization preserves 100% of user-created files in `.swhat/` directory
- **SC-004**: The `--help` flag displays clear usage information for the init command

## Assumptions

- Users have already installed swhat via `uv pip install swhat` or equivalent
- Users are running the command from their project root directory
- The command file format for Claude Code (`.claude/commands/*.md`) and Roo (`.roo/commands/*.md`) follows standard conventions
- The specification workflow content in `tmp/speckit.specify.md` represents the canonical version to embed
- Both Claude Code and Roo support the same markdown command file format
