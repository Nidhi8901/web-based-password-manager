#!/bin/bash

set -e

echo "======================================"
echo "Running Password Manager Tests"
echo "======================================"

echo "[1/3] Checking Python syntax..."
python3 -m py_compile app.py web_app.py
echo "✓ Python syntax check passed"

echo "[2/3] Checking required Python packages..."
python3 -c "import flask, passlib, cryptography, bcrypt"
echo "✓ Required packages check passed"

echo "[3/3] Checking project files..."
test -f app.py
test -f web_app.py
test -f requirements.txt
test -f Dockerfile
echo "✓ Required project files found"

echo "======================================"
echo "All tests passed successfully!"
echo "======================================"
