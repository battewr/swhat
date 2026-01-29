# Tasks: Init Command

**Input**: Design documents from `/specs/002-init-command/`
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

**Purpose**: Add the specify-command template to the registry

- [x] T001 Add SPECIFY_COMMAND_CONTENT string constant in src/swhat/templates.py (content from tmp/speckit.specify.md)
- [x] T002 Add "specify-command" entry to TEMPLATES registry dict in src/swhat/templates.py

---

## Phase 2: Foundational (Init Module)

**Purpose**: Create the init module that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create src/swhat/init.py module with docstring and imports (pathlib, click)
- [x] T004 Implement initialize_project() function in src/swhat/init.py that creates directories and writes files
- [x] T005 Add init subcommand to CLI in src/swhat/cli.py that calls initialize_project()

**Checkpoint**: Init module exists and is wired to CLI

---

## Phase 3: User Story 1 - Initialize Project (Priority: P1) 🎯 MVP

**Goal**: User can run `swhat init` and have .swhat/, .claude/commands/, .roo/commands/ created with command files

**Independent Test**: Run `swhat init` in empty directory, verify all directories and files are created

### Implementation for User Story 1

- [x] T006 [US1] Implement .swhat/ directory creation in src/swhat/init.py
- [x] T007 [US1] Implement .claude/commands/ directory creation in src/swhat/init.py
- [x] T008 [US1] Implement .roo/commands/ directory creation in src/swhat/init.py
- [x] T009 [US1] Implement writing swhat.specify.md to .claude/commands/ in src/swhat/init.py
- [x] T010 [US1] Implement writing swhat.specify.md to .roo/commands/ in src/swhat/init.py
- [x] T011 [US1] Add progress output messages (Created/Updated) in src/swhat/init.py
- [x] T012 [US1] Add --help documentation for init subcommand in src/swhat/cli.py

**Checkpoint**: `swhat init` creates all directories and files, shows progress

---

## Phase 4: User Story 2 - Use Specification Command (Priority: P2)

**Goal**: The installed command files work correctly with Claude Code and Roo

**Independent Test**: After `swhat init`, invoke `/swhat.specify` in Claude Code or Roo

### Implementation for User Story 2

- [x] T013 [US2] Verify command file content includes all required sections (frontmatter, outline, guidelines) in src/swhat/templates.py
- [x] T014 [US2] Ensure template references `swhat template` commands correctly in src/swhat/templates.py

**Checkpoint**: Command files are properly formatted for AI agents

---

## Phase 5: User Story 3 - Re-initialize Project (Priority: P3)

**Goal**: Running `swhat init` again updates command files without touching user files in .swhat/

**Independent Test**: Run `swhat init` twice, verify command files updated, .swhat/ contents preserved

### Implementation for User Story 3

- [x] T015 [US3] Ensure directory creation uses exist_ok=True for idempotent behavior in src/swhat/init.py
- [x] T016 [US3] Ensure file writes overwrite existing command files in src/swhat/init.py
- [x] T017 [US3] Add "already exists" vs "Created" messaging logic in src/swhat/init.py

**Checkpoint**: Re-initialization works correctly

---

## Phase 6: Polish & Validation

**Purpose**: Final validation and quality gates

- [x] T018 Validate installation with `uv pip install .` in clean environment
- [x] T019 Run quickstart.md validation (all example commands work as documented)
- [x] T020 Verify `swhat init --help` shows usage information
- [x] T021 Test error handling when directory is not writable

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - Core functionality
- **User Story 2 (P2)**: Depends on US1 - validates command file content
- **User Story 3 (P3)**: Depends on US1 - adds idempotent behavior

### Within Each Phase

- Setup tasks are sequential (T001 before T002)
- Foundational tasks are sequential (T003 → T004 → T005)
- US1 tasks mostly sequential (directory creation before file writing)
- US2 and US3 tasks can be done after US1

### Parallel Opportunities

- T006, T007, T008 could theoretically be parallel but are in same file
- T009 and T010 could be parallel (different output paths) but same file

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003-T005)
3. Complete Phase 3: User Story 1 (T006-T012)
4. **STOP and VALIDATE**: Test `swhat init` creates all files
5. Deploy/demo if ready - users can initialize projects!

### Incremental Delivery

1. Complete Setup + Foundational → Init command exists
2. Add User Story 1 → Test: `swhat init` works → MVP!
3. Add User Story 2 → Test: Command files work in AI agents
4. Add User Story 3 → Test: Re-initialization works
5. Each story adds confidence without breaking previous stories

---

## Notes

- Template content is large (~8KB) - use triple-quoted string
- Use `pathlib.Path` for cross-platform compatibility
- Progress messages: `click.echo()` for stdout
- Error messages: `click.echo(..., err=True)` for stderr
- Exit code 1 for errors: `sys.exit(1)` or `raise SystemExit(1)`
- The specify-command template content comes from tmp/speckit.specify.md
