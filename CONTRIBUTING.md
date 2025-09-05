# Contributing to PyKeyboard

Thank you for your interest in contributing to PyKeyboard! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project follows a code of conduct to ensure a welcoming environment for all contributors. By participating, you agree to:

- Be respectful and inclusive
- Focus on constructive feedback
- Accept responsibility for mistakes
- Show empathy towards other contributors
- Help create a positive community

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Poetry (for dependency management)
- Git

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/pykeyboard.git
   cd pykeyboard
   ```

3. Set up the upstream remote:
   ```bash
   git remote add upstream https://github.com/johnnie-610/pykeyboard.git
   ```

## Development Setup

### Install Dependencies

```bash
# Install all dependencies including dev dependencies
poetry install

# Activate the virtual environment
poetry shell
```

### Pre-commit Hooks

Install pre-commit hooks to ensure code quality:

```bash
pre-commit install
```

This will run automatic checks on every commit including:
- Code formatting (Ruff)
- Type checking (MyPy)
- Linting (Ruff)
- Import sorting (Ruff)

## Development Workflow

### 1. Choose an Issue

- Check the [Issues](https://github.com/johnnie-610/pykeyboard/issues) page
- Look for issues labeled `good first issue` or `help wanted`
- Comment on the issue to indicate you're working on it

### 2. Create a Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes

- Write clear, focused commits
- Follow the code style guidelines
- Add tests for new functionality
- Update documentation as needed

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pykeyboard --cov-report=html

# Run specific test file
pytest tests/test_inline_keyboard.py

# Run tests matching pattern
pytest -k "pagination"
```

### 5. Check Code Quality

```bash
# Run all quality checks
pre-commit run --all-files

# Or run individual tools
ruff check .
mypy pykeyboard/
```

## Code Style

This project uses modern Python practices:

### Type Hints
- Use type hints for all function parameters and return values
- Use `Union` for multiple possible types
- Use `Optional` for nullable types
- Use `List`, `Dict`, etc. from `typing` (or `list`, `dict` for Python 3.9+)

### Imports
- Group imports: standard library, third-party, local
- Use absolute imports
- Sort imports alphabetically within groups

### Naming Conventions
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_CASE`
- Private attributes/methods: `_prefix`

### Documentation
- Use docstrings for all public functions, classes, and methods
- Follow Google/NumPy docstring format
- Include type information in docstrings
- Provide examples for complex functionality

### Example

```python
from typing import List, Optional

class KeyboardBase:
    """Base class for keyboard implementations.

    This class provides the foundation for creating different types
    of keyboards with row-based layouts.

    Attributes:
        row_width: Number of buttons per row
        keyboard: 2D list representing keyboard layout
    """

    def add(self, *args: Any) -> None:
        """Add buttons to keyboard in rows.

        Args:
            *args: Variable number of buttons to add

        Example:
            >>> keyboard = KeyboardBase()
            >>> keyboard.add(btn1, btn2, btn3)
        """
        # Implementation here
```

## Testing

### Test Structure

Tests are organized in the `tests/` directory:

```
tests/
├── conftest.py          # Pytest fixtures and configuration
├── test_keyboard_base.py    # Base keyboard functionality
├── test_inline_keyboard.py  # Inline keyboard features
├── test_reply_keyboard.py   # Reply keyboard features
├── test_buttons.py          # Button validation
└── test_integration.py      # Integration tests
```

### Writing Tests

- Use descriptive test names: `test_should_handle_empty_keyboard`
- Use fixtures for common setup
- Test both positive and negative cases
- Include edge cases
- Mock external dependencies

### Example Test

```python
import pytest
from pykeyboard import InlineKeyboard, InlineButton

class TestInlineKeyboard:
    def test_pagination_with_valid_inputs(self):
        """Test pagination creates correct button layout."""
        keyboard = InlineKeyboard()
        keyboard.paginate(5, 3, "page_{number}")

        assert keyboard.count_pages == 5
        assert keyboard.current_page == 3
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 5  # first, prev, current, next, last

    def test_pagination_with_invalid_page_count(self):
        """Test pagination raises error for invalid page count."""
        keyboard = InlineKeyboard()

        with pytest.raises(ValueError, match="count_pages must be >= 1"):
            keyboard.paginate(0, 1, "page_{number}")
```

## Documentation

### Docstrings

All public APIs must have comprehensive docstrings:

```python
def paginate(
    self,
    count_pages: int,
    current_page: int,
    callback_pattern: str
) -> None:
    """Create pagination keyboard with specified parameters.

    This method generates a pagination interface with navigation
    buttons for browsing through multiple pages of content.

    Args:
        count_pages: Total number of pages available. Must be >= 1.
        current_page: The page currently being viewed. Must be >= 1
            and <= count_pages.
        callback_pattern: Pattern for callback data containing '{number}'
            placeholder for page numbers.

    Raises:
        ValueError: If count_pages < 1, current_page < 1, or
            current_page > count_pages, or callback_pattern is invalid.

    Example:
        >>> keyboard = InlineKeyboard()
        >>> keyboard.paginate(10, 5, 'page_{number}')
        >>> len(keyboard.keyboard[0])  # 5 navigation buttons
        5
    """
```

### README Updates

When adding new features:
- Update the README with usage examples
- Add the new feature to the table of contents
- Include any breaking changes in upgrade notes

## Submitting Changes

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/changes
- `chore`: Maintenance tasks

Examples:
```
feat(pagination): add support for custom pagination symbols
fix(keyboard): resolve issue with empty button text
docs(readme): update installation instructions
```

### Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Run pre-commit checks
4. Create a pull request with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference to any related issues
   - Screenshots/demo for UI changes

### Review Process

- All PRs require review before merging
- Address review feedback promptly
- Keep PRs focused on a single concern
- Squash commits when appropriate

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- **Description**: Clear description of the issue
- **Steps to reproduce**: Step-by-step instructions
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Python version, OS, package versions
- **Code sample**: Minimal code to reproduce the issue

### Feature Requests

For feature requests, please include:

- **Description**: What feature you'd like to see
- **Use case**: Why this feature would be useful
- **Implementation ideas**: If you have thoughts on how to implement it
- **Alternatives**: Other solutions you've considered

## Getting Help

- **Documentation**: Check the README and docstrings first
- **Issues**: Search existing issues before creating new ones
- **Discussions**: Use GitHub Discussions for questions
- **Code**: Read the source code and tests for implementation details

Thank you for contributing to PyKeyboard! 🎉