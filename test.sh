#!/usr/bin/env bash
set -e

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Error: Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment if not already activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
fi

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo "Installing pytest..."
    uv pip install pytest
fi

echo "=== Running OpenPCB Tests ==="
echo ""

# Run pytest with any passed arguments
# If no arguments, run all tests with quiet mode
if [ $# -gt 0 ]; then
    pytest "$@"
else
    pytest -q
fi

echo ""
echo "=== Tests Complete ==="
