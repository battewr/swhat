#!/bin/bash
set -e

# Remove stale build directory (prevents cross-platform cache conflicts)
if [ -d build ]; then
    echo "==> Removing stale build directory..."
    rm -rf build
fi

echo "==> Configuring CMake..."
cmake -B build

echo "==> Cleaning..."
cmake --build build --target pyclean
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

echo "==> Building..."
cmake --build build --target build

echo "==> Installing (dev mode)..."
cmake --build build --target dev

echo ""
echo "==> Verifying..."
swhat --version
