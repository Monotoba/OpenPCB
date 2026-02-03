#!/usr/bin/env bash
set -e

echo "=== OpenPCB Development Environment Setup ==="

# Initialize git repository if it doesn't exist
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    echo "Git repository initialized"
else
    echo "Git repository already exists"
fi

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
echo "Detected Python version: $PYTHON_VERSION"

# Verify Python version is 3.11 or 3.12
if [[ ! "$PYTHON_VERSION" =~ ^3\.(11|12)$ ]]; then
    echo "Warning: Python $PYTHON_VERSION detected. OpenPCB requires Python 3.11-3.12"
fi

# Install UV if not already installed
if ! command -v uv &> /dev/null; then
    echo "Installing UV package manager..."
    pip install uv
else
    echo "UV is already installed: $(uv --version)"
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    uv venv
else
    echo "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies with UV..."
uv sync

# Install development dependencies
echo "Installing development tools..."
uv pip install \
    black>=24.1 \
    flake8>=7.0 \
    pylint>=3.0 \
    mypy>=1.8 \
    isort>=5.13 \
    pre-commit>=3.6 \
    pytest>=8.0 \
    pytest-qt>=4.3 \
    pytest-cov>=4.1

# Setup pre-commit hooks
if [ -f ".pre-commit-config.yaml" ]; then
    echo "Setting up pre-commit hooks..."
    pre-commit install
    echo "Pre-commit hooks installed"
else
    echo "Note: .pre-commit-config.yaml not found, skipping pre-commit setup"
fi

# Create git commit message template if it doesn't exist
if [ ! -f ".gitmessage" ]; then
    echo "Creating git commit message template..."
    cat > .gitmessage <<'EOF'
# <type>: <subject> (max 50 chars)
# |<----  Using a Maximum Of 50 Characters  ---->|

# Explain why this change is being made
# |<----   Try To Limit Each Line to a Maximum Of 72 Characters   ---->|

# Provide links to related issues, tickets, or documentation
# --- COMMIT END ---
# Type can be:
#    feat     (new feature)
#    fix      (bug fix)
#    refactor (refactoring code)
#    style    (formatting, missing semicolons, etc; no code change)
#    doc      (changes to documentation)
#    test     (adding or refactoring tests; no production code change)
#    chore    (updating build tasks, package manager configs, etc)
EOF
    git config commit.template .gitmessage
    echo "Git commit template created and configured"
fi

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "Development tools installed:"
echo "  ✓ black (code formatter)"
echo "  ✓ flake8 (linter)"
echo "  ✓ pylint (static analyzer)"
echo "  ✓ mypy (type checker)"
echo "  ✓ isort (import sorter)"
echo "  ✓ pre-commit (git hooks)"
echo "  ✓ pytest + pytest-qt + pytest-cov (testing)"
echo ""
if [ -f ".git/hooks/pre-commit" ]; then
    echo "Pre-commit hooks enabled:"
    echo "  ✓ black (auto-format on commit)"
    echo "  ✓ isort (sort imports)"
    echo "  ✓ flake8 (style check)"
    echo "  ✓ mypy (type check)"
    echo "  ✓ trailing whitespace removal"
    echo "  ✓ end-of-file fixer"
    echo ""
fi
echo "To activate the virtual environment manually, run:"
echo "  source .venv/bin/activate"
echo ""
echo "To run the application:"
echo "  ./run.sh"
echo ""
echo "To run tests:"
echo "  ./test.sh"
echo ""
echo "To run code quality checks:"
echo "  black --check openpcb/"
echo "  flake8 openpcb/"
echo "  mypy openpcb/ --strict"
echo "  isort --check openpcb/"
echo ""
