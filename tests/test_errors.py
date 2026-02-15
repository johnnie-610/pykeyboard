"""Tests for the pykeyboard error hierarchy."""

import pytest

from pykeyboard import (
    ConfigurationError,
    LocaleError,
    PaginationError,
    PaginationUnchangedError,
    PyKeyboardError,
    ValidationError,
)
from pykeyboard.inline_keyboard import InlineKeyboard


# ---------------------------------------------------------------------------
# Base class
# ---------------------------------------------------------------------------


class TestPyKeyboardError:
    """Test cases for PyKeyboardError base class."""

    def test_creation(self):
        error = PyKeyboardError("something went wrong")
        assert error.message == "something went wrong"
        assert error.error_code == "PYKEYBOARD_ERROR"
        assert str(error) == "[PYKEYBOARD_ERROR] something went wrong"

    def test_is_exception(self):
        with pytest.raises(PyKeyboardError):
            raise PyKeyboardError("boom")


# ---------------------------------------------------------------------------
# ValidationError
# ---------------------------------------------------------------------------


class TestValidationError:
    def test_with_expected(self):
        error = ValidationError("field_name", "bad_val", expected="int")
        assert error.error_code == "VALIDATION_ERROR"
        assert error.field == "field_name"
        assert error.value == "bad_val"
        assert error.expected == "int"
        assert "field_name" in str(error)

    def test_with_reason(self):
        error = ValidationError("age", -1, reason="must be positive")
        assert "must be positive" in str(error)
        assert error.reason == "must be positive"

    def test_minimal(self):
        error = ValidationError("x")
        assert error.field == "x"
        assert error.value is None
        assert error.expected is None

    def test_inherits_from_base(self):
        assert issubclass(ValidationError, PyKeyboardError)


# ---------------------------------------------------------------------------
# PaginationError
# ---------------------------------------------------------------------------


class TestPaginationError:
    def test_creation(self):
        error = PaginationError("count_pages", 0, "must be >= 1")
        assert error.error_code == "PAGINATION_ERROR"
        assert error.param == "count_pages"
        assert error.value == 0
        assert error.reason == "must be >= 1"
        assert "count_pages" in str(error)

    def test_inherits_from_base(self):
        assert issubclass(PaginationError, PyKeyboardError)


# ---------------------------------------------------------------------------
# PaginationUnchangedError
# ---------------------------------------------------------------------------


class TestPaginationUnchangedError:
    def test_creation(self):
        error = PaginationUnchangedError(source="test_source")
        assert error.source == "test_source"
        assert "unchanged" in str(error)
        # Inherits PAGINATION_ERROR code from PaginationError
        assert error.error_code == "PAGINATION_ERROR"

    def test_inherits_from_pagination(self):
        assert issubclass(PaginationUnchangedError, PaginationError)

    def test_catchable_as_pagination_error(self):
        with pytest.raises(PaginationError):
            raise PaginationUnchangedError("src")


# ---------------------------------------------------------------------------
# LocaleError
# ---------------------------------------------------------------------------


class TestLocaleError:
    def test_creation(self):
        error = LocaleError("callback_pattern", reason="must contain '{locale}'")
        assert error.error_code == "LOCALE_ERROR"
        assert error.param == "callback_pattern"
        assert "callback_pattern" in str(error)

    def test_inherits_from_base(self):
        assert issubclass(LocaleError, PyKeyboardError)


# ---------------------------------------------------------------------------
# ConfigurationError
# ---------------------------------------------------------------------------


class TestConfigurationError:
    def test_creation(self):
        error = ConfigurationError("row_width", 0, "must be >= 1")
        assert error.error_code == "CONFIG_ERROR"
        assert error.setting == "row_width"
        assert error.value == 0
        assert error.reason == "must be >= 1"
        assert "row_width" in str(error)

    def test_inherits_from_base(self):
        assert issubclass(ConfigurationError, PyKeyboardError)


# ---------------------------------------------------------------------------
# Integration with InlineKeyboard
# ---------------------------------------------------------------------------


class TestIntegrationWithInlineKeyboard:
    def test_pagination_error_on_zero_pages(self):
        kb = InlineKeyboard()
        with pytest.raises(PaginationError) as exc_info:
            kb.paginate(0, 1, "page_{number}")

        err = exc_info.value
        assert err.param == "count_pages"
        assert err.value == 0

    def test_locale_error_bad_pattern(self):
        kb = InlineKeyboard()
        with pytest.raises(LocaleError) as exc_info:
            kb.languages("no_placeholder", ["en_US"])

        assert exc_info.value.param == "callback_pattern"

    def test_locale_error_empty_list(self):
        kb = InlineKeyboard()
        with pytest.raises(LocaleError) as exc_info:
            kb.languages("lang_{locale}", [])

        assert "empty" in exc_info.value.message


class TestErrorHierarchy:
    """Verify the exception class hierarchy is correct."""

    def test_all_are_pykeyboard_errors(self):
        assert issubclass(ValidationError, PyKeyboardError)
        assert issubclass(PaginationError, PyKeyboardError)
        assert issubclass(PaginationUnchangedError, PyKeyboardError)
        assert issubclass(LocaleError, PyKeyboardError)
        assert issubclass(ConfigurationError, PyKeyboardError)

    def test_all_are_exceptions(self):
        assert issubclass(PyKeyboardError, Exception)

    def test_catch_by_base_class(self):
        """Every subclass should be catchable via ``except PyKeyboardError``."""
        for cls, args in [
            (ValidationError, ("f",)),
            (PaginationError, ("p", 0, "r")),
            (PaginationUnchangedError, ("s",)),
            (LocaleError, ("p",)),
            (ConfigurationError, ("s", "v", "r")),
        ]:
            with pytest.raises(PyKeyboardError):
                raise cls(*args)
