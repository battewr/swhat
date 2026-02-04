# Research: Windows Build Support

**Feature**: 002-windows-support
**Date**: 2026-01-28

## Windows Script Format

**Decision**: PowerShell (.ps1) script

**Rationale**:
- PowerShell is the default shell on Windows 10+
- Native Windows scripting without additional dependencies
- Better error handling than batch files (.bat/.cmd)
- Can be run from CMD via `powershell -ExecutionPolicy Bypass -File clean_build.ps1`

**Alternatives Considered**:

| Format | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| Batch (.bat) | Universal, runs in CMD | Limited error handling, archaic syntax | Poor developer experience |
| Python script | Cross-platform | Extra dependency, defeats purpose of build script | Adds complexity |
| Git Bash | Uses same .sh script | Requires Git Bash installation | Not default on Windows |

## CMake Cross-Platform Considerations

**Decision**: Use CMake cross-platform commands where possible

**Key Changes Needed**:

1. **Python executable name**: `python3` (Unix) vs `python` (Windows)
   - Solution: Use `find_program(PYTHON_EXECUTABLE python3 python)` to find either

2. **find command in pyclean**: Unix-specific
   - Solution: Use CMake's `file(GLOB_RECURSE)` or PowerShell equivalent in script

3. **Path separators**: Forward slash works in CMake on all platforms
   - No changes needed for CMakeLists.txt paths

4. **Shell commands**: The `|| true` pattern is bash-specific
   - Solution: Remove from CMake, handle in platform scripts

## UV on Windows

**Decision**: UV works natively on Windows

**Verification**:
- UV is distributed as a standalone binary for Windows
- Installation: `pip install uv` or download from GitHub releases
- All UV commands (`uv build`, `uv tool install`, etc.) work identically

## PowerShell Error Handling

**Decision**: Use `$ErrorActionPreference = "Stop"` (equivalent to `set -e`)

**Pattern**:
```powershell
$ErrorActionPreference = "Stop"

# Commands will stop on first error
cmake -B build
cmake --build build --target pyclean
# etc.
```

## Clean Target Cross-Platform Fix

**Decision**: Make pyclean target cross-platform by removing Unix-specific `find` command

**Current (Unix-only)**:
```cmake
COMMAND find "${CMAKE_SOURCE_DIR}" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
```

**Cross-platform solution**:
- Remove find from CMakeLists.txt
- Handle __pycache__ cleanup in platform-specific scripts
- CMake's `rm -rf` via `${CMAKE_COMMAND} -E rm -rf` already works cross-platform

## Installation Path on Windows

**Decision**: UV tool install works the same on Windows

**Behavior**:
- `uv tool install` installs to `~/.local/bin` on Unix
- On Windows, installs to `%USERPROFILE%\.local\bin` or similar
- UV automatically adds to PATH or provides instructions

## Summary of Changes

| Component | Change |
|-----------|--------|
| CMakeLists.txt | Fix python3/python detection, remove Unix-specific find |
| clean_build.ps1 | New file - PowerShell equivalent of clean_build.sh |
| README.md | Add Windows installation instructions |
| CLAUDE.md | Add Windows build commands |
