#!/bin/bash

# Setup script for Strand SDK development

set -e

echo "🔧 Setting up Strand SDK development environment..."

# Check Python version
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✓ Python $python_version"

# Create virtual environment
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "🚀 Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install in editable mode
echo "🔗 Installing strand-sdk in editable mode..."
pip install -e ".[dev,models,docs]"

# Setup pre-commit hooks
echo "🪝 Setting up pre-commit hooks..."
pre-commit install

echo ""
echo "✅ Development environment setup complete!"
echo ""
echo "Next steps:"
echo "  1. Activate: source .venv/bin/activate"
echo "  2. Run tests: pytest tests/"
echo "  3. Run linter: ruff check strand tests"
echo "  4. Check types: mypy strand"

