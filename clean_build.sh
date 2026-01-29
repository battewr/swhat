#!/bin/bash
set -e

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
