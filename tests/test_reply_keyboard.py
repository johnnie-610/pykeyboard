"""Tests for reply keyboard functionality."""

import pytest
from pykeyboard import ReplyKeyboard, ReplyButton


class TestReplyKeyboard:
    """Test cases for ReplyKeyboard class."""

    def test_reply_keyboard_initialization(self):
        """Test reply keyboard initializes correctly."""
        keyboard = ReplyKeyboard()
        assert keyboard.row_width == 3
        assert keyboard.keyboard == []
        assert keyboard.is_persistent is None
        assert keyboard.resize_keyboard is None
        assert keyboard.one_time_keyboard is None
        assert keyboard.selective is None
        assert keyboard.placeholder is None

    def test_reply_keyboard_with_options(self):
        """Test reply keyboard with custom options."""
        keyboard = ReplyKeyboard(
            is_persistent=True,
            resize_keyboard=True,
            one_time_keyboard=True,
            selective=True,
            placeholder="Choose an option"
        )
        assert keyboard.is_persistent is True
        assert keyboard.resize_keyboard is True
        assert keyboard.one_time_keyboard is True
        assert keyboard.selective is True
        assert keyboard.placeholder == "Choose an option"

    def test_pyrogram_markup_property(self):
        """Test pyrogram markup property."""
        keyboard = ReplyKeyboard()
        keyboard.add(ReplyButton(text="Test"))

        markup = keyboard.pyrogram_markup
        assert markup is not None
        assert len(markup.keyboard) == 1


class TestReplyButton:
    """Test cases for ReplyButton class."""

    def test_reply_button_initialization(self):
        """Test reply button initializes correctly."""
        button = ReplyButton(text="Test Button")
        assert button.text == "Test Button"
        assert button.request_contact is None
        assert button.request_location is None
        assert button.request_poll is None
        assert button.request_users is None
        assert button.request_chat is None
        assert button.web_app is None

    def test_reply_button_with_options(self):
        """Test reply button with various options."""
        button = ReplyButton(
            text="Contact",
            request_contact=True,
            request_location=False
        )
        assert button.text == "Contact"
        assert button.request_contact is True
        assert button.request_location is False

    def test_reply_button_to_pyrogram(self):
        """Test conversion to Pyrogram KeyboardButton."""
        button = ReplyButton(text="Test", request_contact=True)
        pyrogram_button = button.to_pyrogram()

        assert pyrogram_button.text == "Test"
        assert pyrogram_button.request_contact is True

    def test_reply_button_validation(self):
        """Test reply button text validation."""
        # Valid text
        button = ReplyButton(text="Valid text")
        assert button.text == "Valid text"

        # Empty text should raise error
        with pytest.raises(ValueError, match="Button text cannot be empty"):
            ReplyButton(text="")

        # Non-string text should raise error
        with pytest.raises(ValueError, match="Button text must be a string"):
            ReplyButton(text=123)  # type: ignore