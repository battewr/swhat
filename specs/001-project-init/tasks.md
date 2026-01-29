# Tasks: Project Initialization

**Input**: Design documents from `/specs/001-project-init/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, contracts/ ✓, quickstart.md ✓

**Tests**: No automated tests per spec requirement ("no testing atm"). Manual CLI validation only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/swhat/` at repository root
- Paths follow plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create source directory structure at src/swhat/
- [x] T002 [P] Create package init file at src/swhat/__init__.py with version "0.1.0"
- [x] T003 [P] Create pyproject.toml with project metadata, click dependency, and entry point

**Checkpoint**: Project structure exists, ready for CLI implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Create CLI entry point at src/swhat/cli.py with Click group, --help, and --version
- [x] T005 Configure pyproject.toml entry point: swhat = "swhat.cli:main"

**Checkpoint**: Foundation ready - CLI framework wired, entry point callable

---

## Phase 3: User Story 1 - Install Package Locally (Priority: P1) 🎯 MVP

**Goal**: Developer can install the package and invoke the CLI entry point

**Independent Test**: Run `uv pip install -e .` and verify `swhat --version` responds

### Implementation for User Story 1

- [x] T006 [US1] Verify pyproject.toml has correct [build-system] for UV compatibility
- [x] T007 [US1] Add Python version constraint (>=3.10) to pyproject.toml
- [x] T008 [US1] Add click>=8.0 dependency to pyproject.toml [project.dependencies]
- [x] T009 [US1] Validate installation with `uv pip install -e .` in clean environment

**Checkpoint**: Package installs successfully, `swhat` command is available

---

## Phase 4: User Story 2 - Run CLI Command (Priority: P2)

**Goal**: User can execute CLI with --help, --version, and get proper error handling

**Independent Test**: Run `swhat --help`, `swhat --version`, `swhat invalid` and verify outputs

### Implementation for User Story 2

- [x] T010 [US2] Implement main() Click group in src/swhat/cli.py with docstring for help text
- [x] T011 [US2] Add @click.version_option() decorator to main() for --version support
- [x] T012 [US2] Configure Click to show help when invoked with no arguments (invoke_without_command=True)
- [x] T013 [US2] Verify error messages go to stderr and exit codes follow contract (0 success, 2 usage error)

**Checkpoint**: CLI responds correctly to --help, --version, invalid commands

---

## Phase 5: User Story 3 - Understand Project Purpose (Priority: P3)

**Goal**: New user can understand and get started with the project via documentation

**Independent Test**: Read README, follow quickstart, achieve working installation

### Implementation for User Story 3

- [x] T014 [P] [US3] Create README.md with project description, installation, and usage sections
- [x] T015 [P] [US3] Update CLAUDE.md with final project structure and commands
- [x] T016 [US3] Add development section to README.md referencing UV and Ruff

**Checkpoint**: Documentation complete, new user can onboard in under 5 minutes

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T017 [P] Add .gitignore with Python patterns (__pycache__, *.pyc, .venv/, dist/, *.egg-info/)
- [x] T018 [P] Add ruff configuration to pyproject.toml [tool.ruff] section
- [x] T019 Run ruff check and ruff format on all Python files
- [x] T020 Run quickstart.md validation checklist to verify all acceptance criteria

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 (P1) → US2 (P2) → US3 (P3) in sequence
  - US2 depends on US1 (need working install to test CLI)
  - US3 can run in parallel with US2 (documentation vs code)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 (need installable package to test CLI behavior)
- **User Story 3 (P3)**: Can start after Foundational - No code dependencies (documentation only)

### Within Each User Story

- Configuration before implementation
- Implementation before validation
- Story complete before moving to next priority

### Parallel Opportunities

- T002 and T003 can run in parallel (different files)
- T014 and T015 can run in parallel (different documentation files)
- T017 and T018 can run in parallel (different concerns)

---

## Parallel Example: Setup Phase

```bash
# After T001 completes, launch T002 and T003 in parallel:
Task T002: "Create package init file at src/swhat/__init__.py"
Task T003: "Create pyproject.toml with project metadata"
```

## Parallel Example: Documentation (US3)

```bash
# T014 and T015 can run in parallel:
Task T014: "Create README.md"
Task T015: "Update CLAUDE.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T005)
3. Complete Phase 3: User Story 1 (T006-T009)
4. **STOP and VALIDATE**: `uv pip install -e . && swhat --version`
5. MVP achieved - package is installable

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test installation → MVP!
3. Add User Story 2 → Test CLI behavior → Full CLI working
4. Add User Story 3 → Verify documentation → Ready for users
5. Polish → Linting, gitignore → Production ready

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- No automated tests per spec - use manual validation from quickstart.md
