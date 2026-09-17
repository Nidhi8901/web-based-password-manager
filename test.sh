#!/bin/bash

set -e

echo "======================================"
echo "Running Password Manager Tests"
echo "======================================"

echo "[1/3] Checking Python syntax..."
python -m py_compile app.py web_app.py
echo "✓ Python syntax check passed"

echo "[2/3] Checking required Python packages..."
python -c "import flask, passlib, cryptography, bcrypt"
echo "✓ Required packages check passed"

echo "[3/3] Checking application configuration..."
if [ -z "$ENCRYPTION_KEY" ]; then
    echo "✗ ENCRYPTION_KEY is not set"
    exit 1
fi

python -c "from app import fernet; print('✓ Encryption configuration loaded')"

echo "======================================"
echo "All tests passed successfully!"
echo "======================================"
