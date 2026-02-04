# Feature Specification: Template Command

**Feature Branch**: `001-template-command`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "swhat template {template_name} command to expose specification templates stored in Python source code"

## Clarifications

### Session 2026-01-28

- Q: Which templates should be included in initial release? → A: "specification" and "specification-checklist"
- Q: Should `swhat template` (no args) and `swhat template --list` display identical or different output? → A: Both display identical output (template names with brief descriptions)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View Specification Template (Priority: P1)

A developer working on a new feature wants to see the specification template to understand what sections and format are expected when writing a feature spec. They run `swhat template specification` and the complete specification template is displayed to their terminal.

**Why this priority**: This is the core functionality - exposing templates for users to reference. Without this, the command has no value.

**Independent Test**: Can be fully tested by running `swhat template specification` and verifying the complete spec-template.md content is output to stdout.

**Acceptance Scenarios**:

1. **Given** swhat is installed and the user is in any directory, **When** the user runs `swhat template specification`, **Then** the complete specification template content is printed to stdout
2. **Given** swhat is installed, **When** the user runs `swhat template specification`, **Then** the output matches the content of the project's spec-template.md template exactly

---

### User Story 2 - List Available Templates (Priority: P2)

A developer wants to discover what templates are available in the system. They run `swhat template` (without arguments) or `swhat template --list` and see a list of all available template names.

**Why this priority**: Discovery is essential for usability - users need to know what templates exist before they can request one.

**Independent Test**: Can be fully tested by running `swhat template --list` and verifying a list of template names is displayed.

**Acceptance Scenarios**:

1. **Given** swhat is installed, **When** the user runs `swhat template` without arguments, **Then** a list of available template names is displayed
2. **Given** swhat is installed, **When** the user runs `swhat template --list`, **Then** a list of available template names is displayed with brief descriptions

---

### User Story 3 - Request Unknown Template (Priority: P3)

A developer mistypes a template name or requests a template that doesn't exist. The system provides helpful feedback about what templates are available.

**Why this priority**: Error handling improves user experience but is not core functionality.

**Independent Test**: Can be fully tested by running `swhat template nonexistent` and verifying an appropriate error message is shown.

**Acceptance Scenarios**:

1. **Given** swhat is installed, **When** the user runs `swhat template xyz` where "xyz" is not a valid template name, **Then** an error message is displayed indicating the template was not found
2. **Given** swhat is installed, **When** the user requests an invalid template, **Then** the error message includes the list of valid template names

---

### Edge Cases

- What happens when the user provides an empty template name (`swhat template ""`)?
- How does the system handle template names with special characters or spaces?
- What happens if the user pipes the output to another command (`swhat template specification | cat`)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a `template` subcommand under the `swhat` CLI
- **FR-002**: System MUST accept a template name as a positional argument to `swhat template`
- **FR-003**: System MUST output the complete template content to stdout when a valid template name is provided
- **FR-004**: System MUST store template content embedded in Python source code (not read from external files at runtime)
- **FR-005**: System MUST initially include the "specification" template (content from spec-template.md) and the "specification-checklist" template (content from requirements checklist structure)
- **FR-006**: System MUST display a list of available templates with brief descriptions when no template name argument is provided
- **FR-007**: System MUST provide a `--list` flag that displays identical output to FR-006 (template names with descriptions)
- **FR-008**: System MUST return exit code 0 on successful template retrieval
- **FR-009**: System MUST return non-zero exit code when an invalid template name is provided
- **FR-010**: System MUST display an error message with available template names when an invalid template is requested
- **FR-011**: System MUST provide `--help` documentation for the template subcommand

### Key Entities

- **Template**: A named text content block representing a workflow artifact structure (e.g., "specification", "plan", "tasks"). Each template has a unique name and associated content string.
- **Template Registry**: The collection of all available templates, allowing lookup by name and enumeration of available templates.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can retrieve any registered template content in under 1 second
- **SC-002**: Template content output is identical to the source template file (byte-for-byte accuracy)
- **SC-003**: The `--help` flag displays usage information for the template command
- **SC-004**: Invalid template requests produce clear error messages that include the list of valid options
- **SC-005**: The command is composable with Unix pipes (stdout contains only template content, errors go to stderr)

## Assumptions

- Templates are relatively small text files (under 100KB) suitable for embedding in Python source
- The initial release includes two templates: "specification" and "specification-checklist"; additional templates (plan, tasks, etc.) will be added in future iterations
- Template names are case-insensitive and use lowercase with hyphens (e.g., "specification", "plan-template")
- The template content is static and does not require runtime variable substitution in this feature
