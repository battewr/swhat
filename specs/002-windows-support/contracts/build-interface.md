# Build Interface Contract

**Version**: 1.0.0
**Date**: 2026-01-28

## Build Scripts

### Unix (clean_build.sh)

**Invocation**: `./clean_build.sh`

**Behavior**:
1. Configure CMake: `cmake -B build`
2. Clean artifacts: `cmake --build build --target pyclean`
3. Build package: `cmake --build build --target build`
4. Install dev: `cmake --build build --target dev`
5. Verify: `swhat --version`

**Exit Codes**:
- 0: Success
- Non-zero: Failure (stops at first error)

### Windows (clean_build.ps1)

**Invocation**: `.\clean_build.ps1`

**Alternative (from CMD)**: `powershell -ExecutionPolicy Bypass -File clean_build.ps1`

**Behavior**: Identical to Unix script

**Exit Codes**: Same as Unix

## CMake Targets

All targets work identically on both platforms:

| Target | Command | Description |
|--------|---------|-------------|
| (default) | `cmake --build build` | No-op (no default target) |
| build | `cmake --build build --target build` | Build package to dist/ |
| dev | `cmake --build build --target dev` | Install editable via uv tool |
| lint | `cmake --build build --target lint` | Run ruff linter |
| format | `cmake --build build --target format` | Format code with ruff |
| pyclean | `cmake --build build --target pyclean` | Remove build artifacts |

## Prerequisites

### Unix
- Python 3.10+
- UV package manager
- CMake 3.16+

### Windows
- Python 3.10+
- UV package manager
- CMake 3.16+
- PowerShell 5.1+ (included in Windows 10+)

## Environment After Build

After successful build on either platform:
- `swhat` command available globally
- `swhat --version` returns version string
- `swhat --help` shows usage
