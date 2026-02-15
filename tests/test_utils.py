"""Tests for utility functions."""

import pytest

from pykeyboard import (
    InlineKeyboard,
    ReplyKeyboard,
    create_keyboard_from_config,
    get_keyboard_info,
    validate_keyboard_config,
)


class TestCreateKeyboardFromConfig:
    """Test cases for keyboard creation from configuration."""

    def test_create_inline_keyboard_from_config(self):
        """Test creating inline keyboard from configuration."""
        config = {
            "type": "inline",
            "row_width": 2,
            "buttons": [
                {"text": "Button 1", "callback_data": "btn1"},
                {"text": "Button 2", "callback_data": "btn2"},
                "Button 3",
            ],
        }

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)
        assert keyboard.row_width == 2
        assert len(keyboard.keyboard) == 2  # 3 buttons, row_width=2 → 2 rows
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

    def test_create_keyboard_missing_type_defaults_to_inline(self):
        """Test creating keyboard with missing type defaults to inline."""
        config = {"buttons": ["Button 1"]}

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)

    def test_create_keyboard_case_insensitive_type(self):
        """Test that keyboard type is case-insensitive."""
        config = {"type": "INLINE", "buttons": ["Button 1"]}

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)

    def test_create_keyboard_empty_buttons(self):
        """Test creating keyboard with no buttons."""
        config = {"type": "inline", "buttons": []}

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)
        assert len(keyboard.keyboard) == 0


class TestGetKeyboardInfo:
    """Test cases for keyboard information retrieval."""

    def test_get_inline_keyboard_info(self):
        """Test getting information about an inline keyboard."""
        keyboard = InlineKeyboard()
        info = get_keyboard_info(keyboard)

        assert info["type"] == "InlineKeyboard"
        assert info["total_buttons"] == 0
        assert info["total_rows"] == 0
        assert "has_pagination" in info
        assert "custom_locales_count" in info

    def test_get_reply_keyboard_info(self):
        """Test getting information about a reply keyboard."""
        keyboard = ReplyKeyboard()
        keyboard.add("Reply 1", "Reply 2")
        keyboard.is_persistent = True
        keyboard.resize_keyboard = True

        info = get_keyboard_info(keyboard)

        assert info["type"] == "ReplyKeyboard"
        assert info["total_buttons"] == 2
        assert info["is_persistent"] is True
        assert info["resize_keyboard"] is True

    def test_get_keyboard_info_custom_locales_count(self):
        """Test that get_keyboard_info correctly counts custom locales."""
        keyboard = InlineKeyboard()

        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 0

        keyboard.add_custom_locale("custom1", "Custom 1")
        keyboard.add_custom_locale("custom2", "Custom 2")

        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 2

        keyboard.clear_custom_locales()
        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 0


class TestValidateKeyboardConfig:
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
            "row_width": 0,
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
            "buttons": "not_a_list",
        }

        errors = validate_keyboard_config(config)

        assert len(errors) > 0
        assert any("buttons must be a list" in error for error in errors)

    def test_validate_empty_config(self):
        """Test validation of an empty config passes."""
        errors = validate_keyboard_config({})

        assert errors == []
