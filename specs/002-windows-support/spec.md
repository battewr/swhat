# Feature Specification: Windows Build Support

**Feature Branch**: `002-windows-support`
**Created**: 2026-01-28
**Status**: Draft
**Input**: User description: "lets add Windows support now to our cmake system so this tool can be installed locally to windows for development"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Build and Install on Windows (Priority: P1)

A Windows developer clones the repository and wants to build and install the swhat CLI tool on their local Windows machine for development purposes.

**Why this priority**: Without a working Windows build, Windows developers cannot use or contribute to the project. This is the core functionality being requested.

**Independent Test**: Can be fully tested by running the build script on a Windows machine and verifying `swhat --version` responds.

**Acceptance Scenarios**:

1. **Given** a Windows machine with the required tools installed, **When** the developer runs the build script, **Then** the build completes without errors.
2. **Given** a successful build on Windows, **When** the developer runs the CLI entry point, **Then** the tool responds with version information.
3. **Given** a Windows machine without the package installed, **When** the developer runs the build script for the first time, **Then** all dependencies are installed automatically.

---

### User Story 2 - Clean Build on Windows (Priority: P2)

A Windows developer wants to perform a clean build to ensure no stale artifacts affect their development workflow.

**Why this priority**: Clean builds are essential for troubleshooting and ensuring reproducible builds during development.

**Independent Test**: Can be tested by running the clean target followed by build and verifying fresh artifacts are created.

**Acceptance Scenarios**:

1. **Given** a previous build exists on Windows, **When** the developer runs the clean command, **Then** all build artifacts are removed.
2. **Given** a clean state, **When** the developer runs the build command, **Then** fresh artifacts are generated from scratch.

---

### User Story 3 - Consistent Developer Experience (Priority: P3)

A developer switching between Windows and Unix-based systems expects the same build commands and workflow to work on both platforms.

**Why this priority**: Cross-platform consistency reduces cognitive load and documentation complexity.

**Independent Test**: Can be tested by comparing the build workflow on Windows vs Unix and verifying command parity.

**Acceptance Scenarios**:

1. **Given** the same source code, **When** a developer uses the build system on Windows, **Then** the commands and workflow mirror the Unix experience.
2. **Given** documentation for the build process, **When** a developer reads it, **Then** they can follow the same steps on either platform.

---

### Edge Cases

- What happens when required tools are missing on Windows? The build should fail with a clear message indicating which tools need to be installed.
- How does the system handle Windows paths with spaces? Paths should be properly quoted to handle spaces in directory names.
- What happens when the developer runs the build from a non-standard shell (e.g., Git Bash vs PowerShell vs CMD)? The build should work in common Windows development environments.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Build system MUST support Windows as a target platform alongside existing Unix support.
- **FR-002**: Build system MUST provide a Windows-compatible build script that performs the same operations as the Unix script.
- **FR-003**: Build system MUST properly handle Windows-style paths including those with spaces.
- **FR-004**: Build system MUST detect and report missing prerequisites on Windows with actionable error messages.
- **FR-005**: Build system MUST install the CLI tool so it is accessible from the command line after build.
- **FR-006**: Clean target MUST remove all build artifacts on Windows.
- **FR-007**: Build commands MUST work in PowerShell, the primary Windows development environment.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A Windows developer can complete a full build and install in under 2 minutes on a standard development machine.
- **SC-002**: The same build commands work identically on Windows and Unix platforms.
- **SC-003**: 100% of existing build targets (build, dev, clean, lint, format) function correctly on Windows.
- **SC-004**: A new Windows developer can go from clone to running `swhat --version` in under 5 minutes following the documentation.

## Assumptions

- Windows 10 or later is the target Windows version.
- PowerShell is the primary shell for Windows development.
- UV package manager is available on Windows (cross-platform tool).
- CMake is available on Windows (cross-platform tool).
- The existing CMake-based build system will be extended rather than replaced.
- Git Bash compatibility is a nice-to-have but not required.
