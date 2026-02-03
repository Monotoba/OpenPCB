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

# Check if any arguments were passed
if [ $# -gt 0 ]; then
    # Run with arguments (e.g., CLI mode)
    echo "Running OpenPCB with arguments: $@"
    python -m openpcb "$@"
else
    # Run GUI mode (default)
    echo "Starting OpenPCB GUI..."
    python -m openpcb
fi
