"""Tests for button functionality and validation."""

import pytest
import warnings
from pykeyboard import InlineButton, ReplyButton


class TestInlineButton:
    """Test cases for InlineButton class."""

    def test_inline_button_initialization(self):
        """Test inline button initializes correctly."""
        button = InlineButton(text="Test Button", callback_data="test_callback")
        assert button.text == "Test Button"
        assert button.callback_data == "test_callback"
        assert button.url is None
        assert button.web_app is None

    def test_inline_button_with_all_options(self):
        """Test inline button with all optional parameters."""
        button = InlineButton(
            text="Full Button",
            callback_data="callback",
            url="https://example.com",
            user_id=12345
        )
        assert button.text == "Full Button"
        assert button.callback_data == "callback"
        assert button.url == "https://example.com"
        assert button.user_id == 12345

    def test_inline_button_to_pyrogram(self):
        """Test conversion to Pyrogram InlineKeyboardButton."""
        button = InlineButton(text="Test", callback_data="test", url="https://test.com")
        pyrogram_button = button.to_pyrogram()

        assert pyrogram_button.text == "Test"
        assert pyrogram_button.callback_data == "test"
        assert pyrogram_button.url == "https://test.com"

    def test_inline_button_validation(self):
        """Test inline button text validation."""
        # Valid text
        button = InlineButton(text="Valid text", callback_data="test")
        assert button.text == "Valid text"

        # Empty text should raise error
        from pydantic import ValidationError
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            InlineButton(text="", callback_data="test")

        # Non-string text should raise error
        with pytest.raises(ValidationError, match="Input should be a valid string"):
            InlineButton(text=123, callback_data="test")  # type: ignore

    def test_inline_button_serialization(self):
        """Test button serialization."""
        button = InlineButton(text="Test", callback_data="test", url="https://test.com")
        data = button.model_dump()

        assert data["text"] == "Test"
        assert data["callback_data"] == "test"
        assert data["url"] == "https://test.com"

        # Test deserialization
        restored = InlineButton.model_validate(data)
        assert restored.text == button.text
        assert restored.callback_data == button.callback_data
        assert restored.url == button.url

    def test_inline_button_positional_constructor_deprecated(self):
        """Test positional constructor with deprecation warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Test single positional argument
            button = InlineButton("Test Button", "test_callback")
            assert button.text == "Test Button"
            assert button.callback_data == "test_callback"

            # Check that deprecation warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "Positional arguments for InlineButton are deprecated" in str(w[0].message)

    def test_inline_button_positional_constructor_invalid(self):
        """Test positional constructor with invalid arguments."""
        with pytest.raises(ValueError, match="InlineButton expects 1-2 positional arguments"):
            InlineButton("text", "callback", "extra")  # Too many args

    def test_inline_button_positional_with_kwargs(self):
        """Test positional constructor mixed with keyword arguments."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            button = InlineButton("Test", url="https://example.com")
            assert button.text == "Test"
            assert button.url == "https://example.com"
            assert button.callback_data is None

            # Check deprecation warning
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)


class TestReplyButton:
    """Test cases for ReplyButton class."""

    def test_reply_button_initialization(self):
        """Test reply button initializes correctly."""
        button = ReplyButton(text="Test Button")
        assert button.text == "Test Button"
        assert button.request_contact is None
        assert button.request_location is None

    def test_reply_button_with_requests(self):
        """Test reply button with request options."""
        button = ReplyButton(
            text="Contact",
            request_contact=True,
            request_location=True
        )
        assert button.text == "Contact"
        assert button.request_contact is True
        assert button.request_location is True

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
        from pydantic import ValidationError
        with pytest.raises(ValidationError, match="String should have at least 1 character"):
            ReplyButton(text="")

        # Non-string text should raise error
        with pytest.raises(ValidationError, match="Input should be a valid string"):
            ReplyButton(text=123)  # type: ignore

    def test_reply_button_positional_constructor_deprecated(self):
        """Test positional constructor with deprecation warning."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Test single positional argument
            button = ReplyButton("Test Button")
            assert button.text == "Test Button"

            # Check that deprecation warning was issued
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)
            assert "Positional arguments for ReplyButton are deprecated" in str(w[0].message)

    def test_reply_button_positional_constructor_invalid(self):
        """Test positional constructor with invalid arguments."""
        with pytest.raises(ValueError, match="ReplyButton expects 1 positional argument"):
            ReplyButton("text", "extra")  # Too many args

    def test_reply_button_positional_with_kwargs(self):
        """Test positional constructor mixed with keyword arguments."""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            button = ReplyButton("Test", request_contact=True)
            assert button.text == "Test"
            assert button.request_contact is True

            # Check deprecation warning
            assert len(w) == 1
            assert issubclass(w[0].category, DeprecationWarning)