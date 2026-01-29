# Quickstart: Windows Build Support

**Feature**: 002-windows-support
**Date**: 2026-01-28

## Prerequisites

### Windows
- Windows 10 or later
- Python 3.10+ (from python.org or Microsoft Store)
- UV package manager: `pip install uv`
- CMake 3.16+: Download from cmake.org or `winget install Kitware.CMake`
- PowerShell 5.1+ (included in Windows 10+)

### Verification
```powershell
python --version    # Should be 3.10+
uv --version        # Should show uv version
cmake --version     # Should be 3.16+
```

## Installation on Windows

### Quick Build (PowerShell)

```powershell
# Clone and enter directory
git clone <repository-url>
cd swhat

# Run build script
.\clean_build.ps1

# Verify
swhat --version
```

### Manual Build (PowerShell)

```powershell
# Configure
cmake -B build

# Clean (optional)
cmake --build build --target pyclean

# Build
cmake --build build --target build

# Install (dev mode)
cmake --build build --target dev

# Verify
swhat --version
```

### From CMD (if PowerShell restricted)

```cmd
powershell -ExecutionPolicy Bypass -File clean_build.ps1
```

## Validation Checklist

- [ ] `.\clean_build.ps1` completes without errors
- [ ] `swhat --version` displays version number
- [ ] `swhat --help` displays usage information
- [ ] `cmake --build build --target lint` runs linter
- [ ] `cmake --build build --target format` formats code

## Troubleshooting

### "running scripts is disabled on this system"

PowerShell execution policy is restricted. Run:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

Or run the script bypassing the policy:
```powershell
powershell -ExecutionPolicy Bypass -File clean_build.ps1
```

### "cmake is not recognized"

CMake not in PATH. Either:
1. Install via winget: `winget install Kitware.CMake`
2. Add CMake bin directory to PATH manually
3. Use full path: `"C:\Program Files\CMake\bin\cmake.exe" -B build`

### "uv is not recognized"

UV not installed or not in PATH:
```powershell
pip install uv
# Or download from https://github.com/astral-sh/uv/releases
```

### "python is not recognized"

Python not in PATH. During Python installation, check "Add Python to PATH".

### "swhat is not recognized" after build

UV tool bin directory not in PATH. Add to PATH:
```powershell
$env:PATH += ";$env:USERPROFILE\.local\bin"
```

Or add permanently via System Properties → Environment Variables.

## Cross-Platform Commands

| Task | Unix | Windows |
|------|------|---------|
| Build script | `./clean_build.sh` | `.\clean_build.ps1` |
| Configure | `cmake -B build` | `cmake -B build` |
| Build | `cmake --build build --target build` | `cmake --build build --target build` |
| Dev install | `cmake --build build --target dev` | `cmake --build build --target dev` |
| Clean | `cmake --build build --target pyclean` | `cmake --build build --target pyclean` |
| Lint | `cmake --build build --target lint` | `cmake --build build --target lint` |
| Format | `cmake --build build --target format` | `cmake --build build --target format` |
