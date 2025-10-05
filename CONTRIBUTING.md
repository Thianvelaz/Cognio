# Contributing to Cognio

Thank you for your interest in contributing to Cognio! This document provides guidelines and instructions for contributing.

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/0xReLogic/Cognio/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)

### Suggesting Features

1. Check existing [Discussions](https://github.com/0xReLogic/Cognio/discussions)
2. Create a new discussion describing:
   - The problem it solves
   - Proposed solution
   - Alternative approaches considered

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our code standards
4. **Write tests** for new functionality
5. **Run tests** to ensure everything passes:
   ```bash
   poetry run pytest
   ```
6. **Format code**:
   ```bash
   poetry run black src/ tests/
   poetry run ruff check src/ tests/
   ```
7. **Commit** with clear messages:
   ```bash
   git commit -m "Add feature: brief description"
   ```
8. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Create a Pull Request** with:
   - Clear description of changes
   - Reference to related issues
   - Screenshots (if applicable)

## Code Standards

### Python Style

- Follow [PEP 8](https://pep8.org/)
- Use [Black](https://black.readthedocs.io/) for formatting (line length: 100)
- Use [Ruff](https://docs.astral.sh/ruff/) for linting
- Use type hints for all functions

### Example

```python
def calculate_similarity(embedding1: list[float], embedding2: list[float]) -> float:
    """
    Calculate cosine similarity between two embeddings.

    Args:
        embedding1: First embedding vector
        embedding2: Second embedding vector

    Returns:
        Similarity score between 0.0 and 1.0
    """
    # Implementation here
    pass
```

### Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings
- Update README.md if adding user-facing features

### Testing

- Write tests for new features
- Maintain or improve test coverage (target: 80%+)
- Include both unit and integration tests

```python
def test_save_memory() -> None:
    """Test saving a memory."""
    # Test implementation
    pass
```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/Cognio.git
cd Cognio

# Install dependencies
poetry install

# Run tests
poetry run pytest

# Run linter
poetry run ruff check src/

# Format code
poetry run black src/
```

## Pull Request Checklist

Before submitting your PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Commit messages are clear
- [ ] No breaking changes (or clearly documented)
- [ ] Branch is up to date with main

## Review Process

1. Maintainers will review your PR
2. Address any feedback or requested changes
3. Once approved, your PR will be merged

## Questions?

Feel free to ask questions in:
- [GitHub Discussions](https://github.com/0xReLogic/Cognio/discussions)
- Pull request comments
- Issue comments

Thank you for contributing!
