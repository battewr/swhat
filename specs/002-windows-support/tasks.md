# Tasks: Windows Build Support

**Input**: Design documents from `/specs/002-windows-support/`
**Prerequisites**: plan.md ✓, spec.md ✓, research.md ✓, contracts/ ✓, quickstart.md ✓

**Tests**: No automated tests per project standards. Manual CLI validation on Windows.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Build scripts at repository root
- CMakeLists.txt at repository root
- Documentation at repository root (README.md, CLAUDE.md)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare CMakeLists.txt for cross-platform compatibility

- [ ] T001 Update CMakeLists.txt to find python3 or python executable (cross-platform)
- [ ] T002 Remove Unix-specific find command from pyclean target in CMakeLists.txt

**Checkpoint**: CMakeLists.txt is cross-platform ready

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core Windows script that MUST be complete before testing user stories

**⚠️ CRITICAL**: No Windows testing can begin until this phase is complete

- [ ] T003 Create clean_build.ps1 PowerShell script at repository root

**Checkpoint**: Foundation ready - Windows build script exists

---

## Phase 3: User Story 1 - Build and Install on Windows (Priority: P1) 🎯 MVP

**Goal**: Windows developer can build and install swhat CLI

**Independent Test**: Run `.\clean_build.ps1` on Windows and verify `swhat --version` responds

### Implementation for User Story 1

- [ ] T004 [US1] Implement cmake configuration step in clean_build.ps1 (cmake -B build)
- [ ] T005 [US1] Implement build step in clean_build.ps1 (cmake --build build --target build)
- [ ] T006 [US1] Implement dev install step in clean_build.ps1 (cmake --build build --target dev)
- [ ] T007 [US1] Implement verification step in clean_build.ps1 (swhat --version)
- [ ] T008 [US1] Add error handling with $ErrorActionPreference = "Stop" in clean_build.ps1

**Checkpoint**: Windows build and install works (MVP complete)

---

## Phase 4: User Story 2 - Clean Build on Windows (Priority: P2)

**Goal**: Windows developer can perform clean builds

**Independent Test**: Run pyclean target and verify artifacts are removed

### Implementation for User Story 2

- [ ] T009 [US2] Implement pyclean step in clean_build.ps1 (cmake --build build --target pyclean)
- [ ] T010 [US2] Add __pycache__ cleanup to clean_build.ps1 using PowerShell Remove-Item

**Checkpoint**: Clean builds work on Windows

---

## Phase 5: User Story 3 - Consistent Developer Experience (Priority: P3)

**Goal**: Documentation reflects cross-platform support

**Independent Test**: Read docs and verify Windows and Unix instructions are present

### Implementation for User Story 3

- [ ] T011 [P] [US3] Update README.md with Windows installation instructions
- [ ] T012 [P] [US3] Update CLAUDE.md with Windows build commands

**Checkpoint**: Documentation complete for both platforms

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final verification and edge cases

- [ ] T013 Add prerequisite check to clean_build.ps1 (verify cmake, uv, python are available)
- [ ] T014 Run quickstart.md validation checklist on Windows

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - US1 (P1) must complete before US2 (P2) - need working build before clean
  - US3 (P3) can run in parallel with US1/US2 (documentation only)
- **Polish (Phase 6)**: Depends on US1 and US2 being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2)
- **User Story 2 (P2)**: Depends on US1 (need working build script structure)
- **User Story 3 (P3)**: Can start after Phase 1 - No code dependencies

### Parallel Opportunities

- T001 and T002 can run in parallel (different parts of CMakeLists.txt)
- T011 and T012 can run in parallel (different documentation files)

---

## Parallel Example: Setup Phase

```bash
# T001 and T002 can run in parallel:
Task T001: "Update CMakeLists.txt python detection"
Task T002: "Remove Unix-specific find from CMakeLists.txt"
```

## Parallel Example: Documentation (US3)

```bash
# T011 and T012 can run in parallel:
Task T011: "Update README.md"
Task T012: "Update CLAUDE.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T002)
2. Complete Phase 2: Foundational (T003)
3. Complete Phase 3: User Story 1 (T004-T008)
4. **STOP and VALIDATE**: `.\clean_build.ps1` works on Windows
5. MVP achieved - Windows developers can build and install

### Incremental Delivery

1. Complete Setup + Foundational → CMake ready, script created
2. Add User Story 1 → Windows build works → MVP!
3. Add User Story 2 → Clean builds work
4. Add User Story 3 → Documentation complete
5. Polish → Prerequisite checks → Production ready

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- This feature requires Windows machine for full testing
- Unix build (clean_build.sh) should continue to work unchanged
- No automated tests - manual validation per project standards
