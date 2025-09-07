"""Tests for utility functions and modern Python features."""

import json
import os
import tempfile

import pytest

from pykeyboard import (InlineKeyboard, ReplyKeyboard,
                        create_keyboard_from_config, export_keyboard_to_file,
                        get_keyboard_info, import_keyboard_from_file,
                        validate_keyboard_config)
from pykeyboard.utils import (get_python_version, supports_literal_types,
                              supports_match_case, supports_typing_self)


class TestPythonVersionUtilities:
    """Test cases for Python version utility functions."""

    def test_get_python_version(self):
        """Test getting Python version as tuple."""
        version = get_python_version()

        assert isinstance(version, tuple)
        assert len(version) == 3
        assert all(isinstance(v, int) for v in version)
        assert version[0] >= 3  # Major version should be 3 or higher

    def test_supports_match_case(self):
        """Test match/case support detection."""
        result = supports_match_case()

        # Should return True for Python 3.10+, False for older versions
        assert isinstance(result, bool)

    def test_supports_typing_self(self):
        """Test typing.Self support detection."""
        result = supports_typing_self()

        # Should return True for Python 3.11+, False for older versions
        assert isinstance(result, bool)

    def test_supports_literal_types(self):
        """Test Literal types support detection."""
        result = supports_literal_types()

        # Should return True for Python 3.8+, False for older versions
        assert isinstance(result, bool)


class TestKeyboardCreation:
    """Test cases for keyboard creation from configuration."""

    def test_create_inline_keyboard_from_config(self):
        """Test creating inline keyboard from configuration."""
        config = {
            "type": "inline",
            "row_width": 2,
            "buttons": [
                {"text": "Button 1", "callback_data": "btn1"},
                {"text": "Button 2", "callback_data": "btn2"},
                "Button 3",  # Simple text button
            ],
        }

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)
        assert keyboard.row_width == 2
        assert (
            len(keyboard.keyboard) == 2
        )  # 3 buttons with row_width=2 = 2 rows
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 1

    def test_create_reply_keyboard_from_config(self):
        """Test creating reply keyboard from configuration."""
        config = {
            "type": "reply",
            "buttons": [
                {"text": "Reply 1", "request_contact": True},
                "Reply 2",
            ],
        }

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, ReplyKeyboard)
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 2

    def test_create_keyboard_invalid_type(self):
        """Test creating keyboard with invalid type."""
        config = {"type": "invalid", "buttons": ["Button 1"]}

        with pytest.raises(ValueError, match="Unsupported keyboard type"):
            create_keyboard_from_config(config)

    def test_create_keyboard_missing_type(self):
        """Test creating keyboard with missing type defaults to inline."""
        config = {"buttons": ["Button 1"]}

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)


class TestKeyboardInfo:
    """Test cases for keyboard information retrieval."""

    def test_get_reply_keyboard_info(self):
        """Test getting information about reply keyboard."""
        keyboard = ReplyKeyboard()
        keyboard.add("Reply 1", "Reply 2")
        keyboard.is_persistent = True
        keyboard.resize_keyboard = True

        info = get_keyboard_info(keyboard)

        assert info["type"] == "ReplyKeyboard"
        assert (
            info["total_buttons"] == 2
        )  # Reply keyboards don't support pagination
        assert info["is_persistent"] is True
        assert info["resize_keyboard"] is True

    def test_get_keyboard_info_features(self):
        """Test that keyboard info includes Python feature support."""
        info = get_keyboard_info(InlineKeyboard())

        assert "features" in info
        assert "match_case" in info["features"]
        assert "typing_self" in info["features"]
        assert "literal_types" in info["features"]
        assert isinstance(info["features"]["match_case"], bool)

    def test_get_keyboard_info_custom_locales_count(self):
        """Test that get_keyboard_info correctly counts custom locales."""
        keyboard = InlineKeyboard()

        # Initially no custom locales
        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 0

        # Add some custom locales
        keyboard.add_custom_locale("custom1", "Custom 1")
        keyboard.add_custom_locale("custom2", "Custom 2")

        # Check count is updated
        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 2

        # Clear custom locales
        keyboard.clear_custom_locales()
        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 0


class TestConfigValidation:
    """Test cases for keyboard configuration validation."""

    def test_validate_valid_config(self):
        """Test validation of valid configuration."""
        config = {
            "type": "inline",
            "row_width": 3,
            "buttons": ["Button 1", "Button 2"],
        }

        errors = validate_keyboard_config(config)

        assert errors == []

    def test_validate_invalid_keyboard_type(self):
        """Test validation of invalid keyboard type."""
        config = {"type": "invalid_type", "buttons": ["Button 1"]}

        errors = validate_keyboard_config(config)

        assert len(errors) > 0
        assert any("Invalid keyboard type" in error for error in errors)

    def test_validate_invalid_row_width(self):
        """Test validation of invalid row width."""
        config = {
            "type": "inline",
            "row_width": 0,  # Invalid: must be >= 1
            "buttons": ["Button 1"],
        }

        errors = validate_keyboard_config(config)

        assert len(errors) > 0
        assert any(
            "row_width must be a positive integer" in error for error in errors
        )

    def test_validate_invalid_buttons_type(self):
        """Test validation of invalid buttons type."""
        config = {
            "type": "inline",
            "buttons": "not_a_list",  # Invalid: must be a list
        }

        errors = validate_keyboard_config(config)

        assert len(errors) > 0
        assert any("buttons must be a list" in error for error in errors)
