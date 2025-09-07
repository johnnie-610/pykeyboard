# Contributing to PyKeyboard

We welcome contributions to PyKeyboard! This document provides guidelines and information for contributors.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)
- [Documentation](#documentation)

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Poetry for dependency management
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/johnnie-610/pykeyboard.git
   cd pykeyboard
   ```

3. Set up the upstream remote:
   ```bash
   git remote add upstream https://github.com/johnnie-610/pykeyboard.git
   ```

## Development Setup

### Install Dependencies

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Development Workflow

1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run tests to ensure everything works:
   ```bash
   poetry run pytest
   ```

4. Format your code:
   ```bash
   poetry run black .
   poetry run isort .
   ```

5. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

## Code Style

We follow these coding standards:

### Python Style

- **Black**: Code formatting
- **isort**: Import sorting

### Commit Messages

We use conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New features
- `fix`: Bug fixes
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `chore`: Maintenance

### Naming Conventions

- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes: `_single_leading_underscore`

## Testing

### Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=pykeyboard

# Run specific test file
poetry run pytest tests/test_inline_keyboard.py

# Run tests in verbose mode
poetry run pytest -v
```

### Writing Tests

- Use `pytest` framework
- Place tests in `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test function names
- Include docstrings for complex tests

Example:
```python
def test_inline_keyboard_creation():
    """Test that InlineKeyboard can be created successfully."""
    keyboard = InlineKeyboard()
    assert keyboard is not None
    assert len(keyboard.keyboard) == 0
```

## Submitting Changes

### Pull Request Process

1. Ensure your branch is up to date:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Create a Pull Request on GitHub

4. Wait for review and address any feedback

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure all tests pass
- Update documentation if needed

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to reproduce**: Step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Python version, OS, PyKeyboard version, kurigram version
- **Code sample**: Minimal code to reproduce the issue

### Feature Requests

For feature requests, please include:

- **Description**: Clear description of the proposed feature
- **Use case**: Why this feature would be useful
- **Implementation ideas**: Any thoughts on how to implement it
- **Alternatives**: Any alternative solutions considered

## Documentation

### Building Documentation

```bash
# Install documentation dependencies
poetry install --with docs

# Build documentation
poetry run mkdocs build

# Serve documentation locally
poetry run mkdocs serve
```

### Documentation Guidelines

- Use clear, concise language
- Include code examples where appropriate
- Keep API documentation up to date
- Use proper Markdown formatting
- Include type hints in examples

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## License

By contributing to PyKeyboard, you agree that your contributions will be licensed under the MIT License.

## Getting Help

If you need help or have questions:

- Check the [documentation](https://pykeyboard.readthedocs.io/)
- Search existing [issues](https://github.com/johnnie-610/pykeyboard/issues)
- Ask questions in [discussions](https://github.com/johnnie-610/pykeyboard/discussions)

Thank you for contributing to PyKeyboard! 🎉