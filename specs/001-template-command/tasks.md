# Tasks: Template Command

**Input**: Design documents from `/specs/001-template-command/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: No tests requested in feature specification. Manual CLI validation per constitution.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/swhat/` at repository root
- Paths based on plan.md structure

---

## Phase 1: Setup

**Purpose**: Create the templates module structure

- [x] T001 Create templates module file at src/swhat/templates.py with module docstring and type alias

---

## Phase 2: Foundational (Template Registry)

**Purpose**: Core template storage that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T002 [P] Add SPEC_TEMPLATE_CONTENT string constant in src/swhat/templates.py (copy from .specify/templates/spec-template.md)
- [x] T003 [P] Add CHECKLIST_CONTENT string constant in src/swhat/templates.py (specification-checklist content from data-model.md)
- [x] T004 Define TEMPLATES registry dict mapping names to (content, description) tuples in src/swhat/templates.py

**Checkpoint**: Template registry complete - CLI implementation can begin

---

## Phase 3: User Story 1 - View Specification Template (Priority: P1) 🎯 MVP

**Goal**: User can run `swhat template specification` and see the complete template content

**Independent Test**: Run `swhat template specification` and verify output matches spec-template.md content

### Implementation for User Story 1

- [x] T005 [US1] Add `template` subcommand to CLI with optional name argument in src/swhat/cli.py
- [x] T006 [US1] Implement template content lookup (case-insensitive) and stdout output in src/swhat/cli.py
- [x] T007 [US1] Add `--help` documentation for template subcommand in src/swhat/cli.py

**Checkpoint**: `swhat template specification` outputs full template content to stdout

---

## Phase 4: User Story 2 - List Available Templates (Priority: P2)

**Goal**: User can run `swhat template` or `swhat template --list` to see available templates

**Independent Test**: Run `swhat template --list` and verify list of templates with descriptions is displayed

### Implementation for User Story 2

- [x] T008 [US2] Add `--list` flag to template subcommand in src/swhat/cli.py
- [x] T009 [US2] Implement list display showing template names and descriptions in src/swhat/cli.py
- [x] T010 [US2] Make no-argument invocation display same list as --list in src/swhat/cli.py

**Checkpoint**: `swhat template` and `swhat template --list` both show available templates

---

## Phase 5: User Story 3 - Request Unknown Template (Priority: P3)

**Goal**: User gets helpful error message when requesting non-existent template

**Independent Test**: Run `swhat template xyz` and verify error message shows available templates

### Implementation for User Story 3

- [x] T011 [US3] Implement error handling for invalid template names in src/swhat/cli.py
- [x] T012 [US3] Output error to stderr with exit code 1 and include available template names in src/swhat/cli.py

**Checkpoint**: Invalid template requests show helpful error with available options

---

## Phase 6: Polish & Validation

**Purpose**: Final validation and quality gates

- [x] T013 Validate installation with `uv pip install .` in clean environment
- [x] T014 Run quickstart.md validation (all example commands work as documented)
- [x] T015 Verify `swhat template --help` shows usage information

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses same CLI command, extends it
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Adds error handling to same command

### Within Each User Story

- All user stories modify the same file (cli.py), so they should be done sequentially
- US1 → US2 → US3 is the recommended order (matches priority)

### Parallel Opportunities

- T002 and T003 can run in parallel (different string constants, same file but independent)
- Once Foundational is complete, US1 implementation can begin immediately

---

## Parallel Example: Phase 2 (Foundational)

```bash
# Launch template content tasks in parallel:
Task: "Add SPEC_TEMPLATE_CONTENT string constant in src/swhat/templates.py"
Task: "Add CHECKLIST_CONTENT string constant in src/swhat/templates.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational (T002-T004)
3. Complete Phase 3: User Story 1 (T005-T007)
4. **STOP and VALIDATE**: Test `swhat template specification`
5. Deploy/demo if ready - users can view templates!

### Incremental Delivery

1. Complete Setup + Foundational → Template registry ready
2. Add User Story 1 → Test: `swhat template specification` → MVP!
3. Add User Story 2 → Test: `swhat template --list` → Discovery feature
4. Add User Story 3 → Test: `swhat template xyz` → Error handling
5. Each story adds value without breaking previous stories

---

## Notes

- All user stories modify src/swhat/cli.py - recommend sequential execution
- Template content strings are large (~4KB each) - use triple-quoted strings
- Case-insensitive lookup: `name.lower()` before registry access
- Errors to stderr: `click.echo(..., err=True)`
- Exit code 1 for errors: `sys.exit(1)` or `raise SystemExit(1)`
