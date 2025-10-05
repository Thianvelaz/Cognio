#!/bin/bash
# First-time setup script for Cognio

set -e

echo "=== Cognio Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "Found Python $PYTHON_VERSION"

if [[ $(echo "$PYTHON_VERSION < 3.11" | bc) -eq 1 ]]; then
    echo "Warning: Python 3.11+ is recommended"
fi
echo ""

# Check if Poetry is installed
echo "Checking Poetry..."
if ! command -v poetry &> /dev/null; then
    echo "Poetry not found. Installing..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi
echo "Poetry is installed"
echo ""

# Install dependencies
echo "Installing dependencies..."
poetry install
echo ""

# Create data directory
echo "Creating data directory..."
mkdir -p data
echo ""

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "Please edit .env file if needed"
else
    echo ".env file already exists"
fi
echo ""

# Run tests
echo "Running tests..."
poetry run pytest --quiet
echo ""

echo "=== Setup Complete ==="
echo ""
echo "To start the server:"
echo "  poetry run uvicorn src.main:app --reload"
echo ""
echo "Or with Docker:"
echo "  docker-compose up -d"
echo ""
