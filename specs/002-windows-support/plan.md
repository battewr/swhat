# Implementation Plan: Windows Build Support

**Branch**: `002-windows-support` | **Date**: 2026-01-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-windows-support/spec.md`

## Summary

Add Windows support to the existing CMake build system by creating a PowerShell equivalent of clean_build.sh and updating CMakeLists.txt to handle cross-platform differences. The core CMake commands remain the same; only the wrapper script and platform-specific commands need adaptation.

## Technical Context

**Language/Version**: PowerShell 5.1+ (Windows default), CMake 3.16+
**Primary Dependencies**: UV (cross-platform), CMake (cross-platform)
**Storage**: N/A
**Testing**: Manual CLI validation on Windows
**Target Platform**: Windows 10+, alongside existing Unix support
**Project Type**: Single project (build system extension)
**Performance Goals**: Build completes in under 2 minutes
**Constraints**: Must work in PowerShell; paths with spaces must be handled
**Scale/Scope**: Single build script addition, CMakeLists.txt updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| **I. CLI-First Design** | Build commands via CLI | ✅ PASS - PowerShell script invokes cmake CLI |
| **II. UV Package Standards** | UV-based installation | ✅ PASS - UV is cross-platform, works on Windows |
| **III. AI Context Engineering** | N/A for build system | ✅ PASS - Not applicable |
| **IV. Simplicity & YAGNI** | Minimal additions | ✅ PASS - Single script, minimal CMake changes |

**Quality Gates**:
- Installation Gate: Same cmake commands work on Windows → Will verify
- CLI Gate: `swhat --version` works after build → Will verify
- Help Gate: N/A for build scripts

## Project Structure

### Documentation (this feature)

```text
specs/002-windows-support/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── quickstart.md        # Phase 1 output
└── contracts/           # Phase 1 output (build interface spec)
```

### Source Code (repository root)

```text
clean_build.sh           # Existing Unix build script
clean_build.ps1          # NEW: Windows PowerShell build script
CMakeLists.txt           # Updated for cross-platform compatibility
README.md                # Updated with Windows instructions
CLAUDE.md                # Updated with Windows commands
```

**Structure Decision**: Minimal changes - add one PowerShell script and update CMakeLists.txt for cross-platform path handling. No new directories needed.

## Complexity Tracking

> No violations. Single script addition follows Simplicity & YAGNI principle.
