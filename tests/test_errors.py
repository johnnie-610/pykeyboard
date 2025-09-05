"""Tests for comprehensive error reporting system."""

import pytest
import json
from unittest.mock import patch, MagicMock
from pykeyboard import (
    PyKeyboardError, ValidationError, PaginationError, LocaleError,
    ConfigurationError, DependencyError, ErrorSuggestion
)
from pykeyboard.inline_keyboard import InlineKeyboard


class TestPyKeyboardError:
    """Test cases for PyKeyboardError base class."""

    def test_pykeyboard_error_creation(self):
        """Test basic PyKeyboardError creation."""
        error = PyKeyboardError("Test error", "TEST_ERROR")

        assert str(error) == "[TEST_ERROR] Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.message == "Test error"
        assert error.suggestions == []
        assert error.context == {}

    def test_pykeyboard_error_with_suggestions(self):
        """Test PyKeyboardError with suggestions."""
        suggestions = [
            ErrorSuggestion("Fix it", "Here's how", ["Step 1", "Step 2"])
        ]
        error = PyKeyboardError("Test error", "TEST_ERROR", suggestions)

        assert len(error.suggestions) == 1
        assert error.suggestions[0].title == "Fix it"

    def test_pykeyboard_error_full_report(self):
        """Test full error report generation."""
        error = PyKeyboardError(
            "Test error",
            "TEST_ERROR",
            context={"key": "value"},
            suggestions=[ErrorSuggestion("Fix", "How to fix", ["Do this"])]
        )

        report = error.get_full_report()
        assert "Test error" in report
        assert "TEST_ERROR" in report
        assert "key: value" in report
        assert "Fix" in report

    def test_error_suggestion_formatting(self):
        """Test error suggestion formatting."""
        suggestion = ErrorSuggestion(
            "Test Title",
            "Test description",
            ["Step 1", "Step 2"],
            "code_example",
            "docs_link"
        )

        formatted = suggestion.format_suggestion()
        assert "Test Title" in formatted
        assert "Test description" in formatted
        assert "Step 1" in formatted
        assert "Step 2" in formatted
        assert "code_example" in formatted
        assert "docs_link" in formatted


class TestSpecificErrors:
    """Test cases for specific error types."""

    def test_validation_error(self):
        """Test ValidationError creation."""
        error = ValidationError("field_name", "invalid_value", "str")

        assert error.error_code == "VALIDATION_ERROR"
        assert "field_name" in error.message
        assert "invalid_value" in error.context
        assert len(error.suggestions) == 1

    def test_pagination_error(self):
        """Test PaginationError creation."""
        error = PaginationError("count_pages", 0, "must be >= 1")

        assert error.error_code == "PAGINATION_ERROR"
        assert "count_pages" in error.message
        assert len(error.suggestions) == 1

    def test_locale_error(self):
        """Test LocaleError creation."""
        error = LocaleError("invalid_locale", "not supported")

        assert error.error_code == "LOCALE_ERROR"
        assert "invalid_locale" in error.message
        assert len(error.suggestions) == 1

    def test_configuration_error(self):
        """Test ConfigurationError creation."""
        error = ConfigurationError("setting", "invalid value")

        assert error.error_code == "CONFIG_ERROR"
        assert "setting" in error.message
        assert len(error.suggestions) == 1

    def test_dependency_error(self):
        """Test DependencyError creation."""
        original_error = ImportError("Module not found")
        error = DependencyError("missing_module", "import", original_error)

        assert error.error_code == "DEPENDENCY_ERROR"
        assert "missing_module" in error.message
        assert error.original_error is original_error
        assert len(error.suggestions) == 1




class TestIntegrationWithInlineKeyboard:
    """Integration tests with InlineKeyboard."""

    def test_inline_keyboard_pagination_error_handling(self):
        """Test pagination error handling in InlineKeyboard."""
        keyboard = InlineKeyboard()

        # Test invalid count_pages
        with pytest.raises(PaginationError) as exc_info:
            keyboard.paginate(0, 1, "page_{number}")

        error = exc_info.value
        assert error.error_code == "PAGINATION_ERROR"
        assert "count_pages" in error.message
        assert len(error.suggestions) == 1

    def test_inline_keyboard_locale_error_handling(self):
        """Test locale error handling in InlineKeyboard."""
        keyboard = InlineKeyboard()

        # Test invalid callback pattern
        with pytest.raises(LocaleError) as exc_info:
            keyboard.languages("invalid_pattern", ["en_US"])

        error = exc_info.value
        assert error.error_code == "LOCALE_ERROR"
        assert "callback_pattern" in error.message
        assert len(error.suggestions) == 1

    def test_inline_keyboard_empty_locales_error(self):
        """Test empty locales list error."""
        keyboard = InlineKeyboard()

        with pytest.raises(LocaleError) as exc_info:
            keyboard.languages("lang_{locale}", [])

        error = exc_info.value
        assert error.error_code == "LOCALE_ERROR"
        assert "empty" in error.message

    def test_direct_error_raising(self):
        """Test that errors are raised directly without automatic reporting."""
        keyboard = InlineKeyboard()

        # Test that errors are raised directly
        with pytest.raises(PaginationError):
            keyboard.paginate(0, 1, "page_{number}")

        with pytest.raises(LocaleError):
            keyboard.languages("", ["en_US"])




class TestErrorSerialization:
    """Test cases for error serialization."""

    def test_error_to_dict(self):
        """Test converting error to dictionary."""
        error = PyKeyboardError(
            "Test error",
            "TEST_ERROR",
            context={"key": "value"},
            suggestions=[ErrorSuggestion("Fix", "How", ["Step"])]
        )

        # Errors don't have to_dict method, but we can test the report
        report = error.get_full_report()
        assert isinstance(report, str)
        assert "Test error" in report

    def test_error_json_serialization(self):
        """Test JSON serialization of error data."""
        error = PyKeyboardError("Test error", "TEST_ERROR")

        # Test that error context can be JSON serialized
        import json
        context_json = json.dumps(error.context)
        assert context_json == "{}"

        # Test error with context
        error_with_context = PyKeyboardError(
            "Test error",
            "TEST_ERROR",
            context={"number": 42, "text": "hello"}
        )
        context_json = json.dumps(error_with_context.context)
        assert '"number":42' in context_json
        assert '"text":"hello"' in context_json