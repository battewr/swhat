# clean_build.ps1 - Windows PowerShell build script for swhat
# Equivalent to clean_build.sh for Unix systems

$ErrorActionPreference = "Stop"

# T013: Check prerequisites
Write-Host "==> Checking prerequisites..."
$missing = @()

if (-not (Get-Command cmake -ErrorAction SilentlyContinue)) {
    $missing += "cmake"
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    $missing += "uv"
}
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    if (-not (Get-Command python3 -ErrorAction SilentlyContinue)) {
        $missing += "python"
    }
}

if ($missing.Count -gt 0) {
    Write-Host "ERROR: Missing required tools: $($missing -join ', ')" -ForegroundColor Red
    Write-Host "Please install the missing tools and try again."
    exit 1
}
Write-Host "All prerequisites found."

# T004: Configure CMake
Write-Host ""
Write-Host "==> Configuring CMake..."
cmake -B build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# T009: Clean Python artifacts via CMake
Write-Host ""
Write-Host "==> Cleaning..."
cmake --build build --target pyclean
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# T010: Clean __pycache__ directories using PowerShell
Write-Host "==> Cleaning __pycache__ directories..."
Get-ChildItem -Path . -Directory -Recurse -Filter "__pycache__" -ErrorAction SilentlyContinue | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue

# T005: Build
Write-Host ""
Write-Host "==> Building..."
cmake --build build --target build
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# T006: Dev install
Write-Host ""
Write-Host "==> Installing (dev mode)..."
cmake --build build --target dev
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

# T007: Verify
Write-Host ""
Write-Host "==> Verifying..."
swhat --version
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARNING: 'swhat' command not found in PATH." -ForegroundColor Yellow
    Write-Host "You may need to add UV's bin directory to your PATH:"
    Write-Host '  $env:PATH += ";$env:USERPROFILE\.local\bin"'
    exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Build complete!" -ForegroundColor Green
