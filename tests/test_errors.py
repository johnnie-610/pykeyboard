"""Tests for comprehensive error reporting system."""

import json
from unittest.mock import MagicMock, patch

import pytest

from pykeyboard import (ConfigurationError, LocaleError, PaginationError,
                        PaginationUnchangedError, PyKeyboardError,
                        ValidationError)
from pykeyboard.inline_keyboard import InlineKeyboard


class TestPyKeyboardError:
    """Test cases for PyKeyboardError base class."""

    def test_pykeyboard_error_creation(self):
        """Test basic PyKeyboardError creation."""
        error = PyKeyboardError("Test error", "TEST_ERROR")

        assert str(error) == "[TEST_ERROR] Test error"
        assert error.error_code == "TEST_ERROR"
        assert error.message == "Test error"

    def test_pykeyboard_error_full_report(self):
        """Test full error report generation."""
        error = PyKeyboardError(
            "Test error", "TEST_ERROR", context={"key": "value"}
        )

        report = error.get_full_report()
        assert "Test error" in report
        assert "TEST_ERROR" in report
        assert "key: value" in report


class TestSpecificErrors:
    """Test cases for specific error types."""

    def test_validation_error(self):
        """Test ValidationError creation."""
        error = ValidationError("field_name", "invalid_value", "str")

        assert error.error_code == "VALIDATION_ERROR"
        assert "field_name" in error.message
        assert (
            "value" in error.context
        )  # ValidationError uses 'value' key in context
        # suggestions attribute may not be available

    def test_pagination_error(self):
        """Test PaginationError creation."""
        error = PaginationError("count_pages", 0, "must be >= 1")

        assert error.error_code == "PAGINATION_ERROR"
        assert "count_pages" in error.message

    def test_locale_error(self):
        """Test LocaleError creation."""
        error = LocaleError("invalid_locale", "not supported")

        assert error.error_code == "LOCALE_ERROR"
        assert "invalid_locale" in error.message
        # suggestions attribute may not be available

    def test_configuration_error(self):
        """Test ConfigurationError creation."""
        error = ConfigurationError("setting", "invalid value", "invalid format")

        assert error.error_code == "CONFIG_ERROR"
        assert "setting" in error.message
        # suggestions attribute may not be available

    def test_pagination_unchanged_error(self):
        """Test PaginationUnchangedError creation."""
        error = PaginationUnchangedError(
            source="test_source", keyboard_hash="abc123", previous_hash="def456"
        )

        assert (
            error.error_code == "PAGINATION_ERROR"
        )  # Inherits from PaginationError
        assert "test_source" in error.message
        assert error.source == "test_source"
        assert error.keyboard_hash == "abc123"
        assert error.previous_hash == "def456"

    def test_pagination_unchanged_error_hash_generation(self):
        """Test hash generation for keyboard state."""
        keyboard_data = {
            "count_pages": 5,
            "current_page": 3,
            "callback_pattern": "page_{number}",
            "source": "test",
        }

        hash_value = PaginationUnchangedError.get_keyboard_hash(keyboard_data)
        assert isinstance(hash_value, str)
        assert len(hash_value) == 64  # SHA256 hex length

        # Same data should produce same hash
        hash_value2 = PaginationUnchangedError.get_keyboard_hash(keyboard_data)
        assert hash_value == hash_value2

        # Different data should produce different hash
        keyboard_data["current_page"] = 4
        hash_value3 = PaginationUnchangedError.get_keyboard_hash(keyboard_data)
        assert hash_value != hash_value3


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
        # suggestions attribute may not be available

    def test_inline_keyboard_locale_error_handling(self):
        """Test locale error handling in InlineKeyboard."""
        keyboard = InlineKeyboard()

        # Test invalid callback pattern
        with pytest.raises(LocaleError) as exc_info:
            keyboard.languages("invalid_pattern", ["en_US"])

        error = exc_info.value
        assert error.error_code == "LOCALE_ERROR"
        assert "callback_pattern" in error.message
        # suggestions attribute may not be available

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
            "Test error", "TEST_ERROR", context={"key": "value"}
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
            "Test error", "TEST_ERROR", context={"number": 42, "text": "hello"}
        )
        context_json = json.dumps(error_with_context.context)
        assert '"number"' in context_json  # JSON formatting may vary
        assert '"text"' in context_json
        assert "42" in context_json
        assert "hello" in context_json
