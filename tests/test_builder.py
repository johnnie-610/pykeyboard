"""Tests for keyboard builder and factory functionality."""

import pytest

from pykeyboard import (InlineButton, InlineKeyboard, KeyboardBuilder,
                        KeyboardFactory, ReplyButton, ReplyKeyboard,
                        ValidationError)


class TestKeyboardBuilder:
    """Test cases for KeyboardBuilder class."""

    def test_keyboard_builder_initialization(self):
        """Test keyboard builder initializes correctly."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        assert builder.keyboard is keyboard
        assert builder._validation_hooks == []
        assert builder._button_transforms == []

    def test_add_button_inline_keyboard(self):
        """Test adding buttons to inline keyboard."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_button("Test Button", "test_callback")
        builder.add_button(
            "Another Button", "another_callback", url="https://example.com"
        )

        # Each add_button clears the keyboard and adds one button
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 1
        assert (
            keyboard.keyboard[0][0].text == "Another Button"
        )  # Last added button
        assert keyboard.keyboard[0][0].callback_data == "another_callback"
        assert keyboard.keyboard[0][0].url == "https://example.com"

    def test_add_button_reply_keyboard(self):
        """Test adding buttons to reply keyboard."""
        keyboard = ReplyKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_button("Reply Button", request_contact=True)

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 1
        assert keyboard.keyboard[0][0].text == "Reply Button"
        assert keyboard.keyboard[0][0].request_contact is True

    def test_add_buttons_bulk(self):
        """Test adding multiple buttons at once."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_buttons(
            "Button 1",
            {"text": "Button 2", "callback_data": "btn2"},
            InlineButton("Button 3", "btn3"),
        )

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3
        assert keyboard.keyboard[0][0].text == "Button 1"
        assert keyboard.keyboard[0][1].text == "Button 2"
        assert keyboard.keyboard[0][2].text == "Button 3"

    def test_add_row(self):
        """Test adding complete rows."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_row("Row1 Col1", "Row1 Col2")
        builder.add_row("Row2 Col1", "Row2 Col2", "Row2 Col3")

        assert len(keyboard.keyboard) == 2
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 3
        assert keyboard.keyboard[0][0].text == "Row1 Col1"
        assert keyboard.keyboard[1][2].text == "Row2 Col3"

    def test_add_conditional_button(self):
        """Test conditional button addition."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        # Condition is True
        builder.add_conditional_button(True, "Visible Button", "visible")
        # Condition is False
        builder.add_conditional_button(False, "Hidden Button", "hidden")

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 1
        assert keyboard.keyboard[0][0].text == "Visible Button"

    def test_add_paginated_buttons(self):
        """Test paginated button addition."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
        builder.add_paginated_buttons(items, "select_{item}_page_{page}", 3, 1)

        # First page: items 1-3, added as a single row
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3
        assert keyboard.keyboard[0][0].text == "Item 1"
        assert keyboard.keyboard[0][1].text == "Item 2"
        assert keyboard.keyboard[0][2].text == "Item 3"
        assert keyboard.keyboard[0][0].callback_data == "select_Item 1_page_1"
        assert keyboard.keyboard[0][2].callback_data == "select_Item 3_page_1"

    def test_add_navigation_buttons(self):
        """Test navigation button addition."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_navigation_buttons(5, 3, "nav_{number}")

        assert keyboard.count_pages == 5
        assert keyboard.current_page == 3
        assert keyboard.callback_pattern == "nav_{number}"

    def test_add_language_buttons(self):
        """Test language button addition."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_language_buttons(["en_US", "ru_RU"], "lang_{locale}", 2)

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 2
        assert keyboard.keyboard[0][0].text == "🇺🇸 English"
        assert keyboard.keyboard[0][1].text == "🇷🇺 Русский"

    def test_validation_hooks(self):
        """Test validation hook functionality."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        def text_not_empty(button):
            return len(button.text.strip()) > 0

        builder.add_validation_hook(text_not_empty)

        # Valid button
        builder.add_button("Valid Button", "valid")

        # Invalid button should raise a pydantic ValidationError due to empty text
        with pytest.raises(
            Exception
        ):  # Could be ValidationError or pydantic error
            builder.add_button("", "invalid")

    def test_button_transforms(self):
        """Test button transformation functionality."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        def add_prefix(button):
            button.text = f"▶️ {button.text}"
            return button

        builder.add_button_transform(add_prefix)
        builder.add_button("Test Button", "test")

        assert keyboard.keyboard[0][0].text == "▶️ Test Button"

    def test_build_method(self):
        """Test build method returns correct keyboard."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_button("Test", "test")
        result = builder.build()

        assert result is keyboard
        assert len(result.keyboard) == 1

    def test_method_chaining(self):
        """Test method chaining functionality."""
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        # Chain multiple operations
        result = (
            builder.add_button("Button 1", "btn1")
            .add_button("Button 2", "btn2")  # Overwrites previous
            .add_row("Row Button 1", "Row Button 2")
            .build()
        )

        assert (
            len(result.keyboard) == 2
        )  # 1 single button + 1 row with 2 buttons
        assert len(result.keyboard[0]) == 1  # Button 2
        assert len(result.keyboard[1]) == 2  # Row buttons


class TestKeyboardFactory:
    """Test cases for KeyboardFactory class."""

    def test_create_confirmation_keyboard(self):
        """Test confirmation keyboard creation."""
        keyboard = KeyboardFactory.create_confirmation_keyboard()

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 2
        assert keyboard.keyboard[0][0].text == "✅ Yes"
        assert keyboard.keyboard[0][1].text == "❌ No"

    def test_create_confirmation_keyboard_with_cancel(self):
        """Test confirmation keyboard with cancel button."""
        keyboard = KeyboardFactory.create_confirmation_keyboard(
            cancel_text="🚫 Cancel", callback_pattern="confirm_{action}"
        )

        assert len(keyboard.keyboard) == 2
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 1
        assert keyboard.keyboard[1][0].text == "🚫 Cancel"
        assert keyboard.keyboard[0][0].callback_data == "confirm_yes"

    def test_create_menu_keyboard(self):
        """Test menu keyboard creation."""
        menu_items = {"Home": "home", "Settings": "settings", "Help": "help"}
        keyboard = KeyboardFactory.create_menu_keyboard(menu_items)

        assert (
            len(keyboard.keyboard) == 2
        )  # 3 buttons with row_width=2 = 2 rows
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 1
        assert keyboard.keyboard[0][0].text == "Home"
        assert keyboard.keyboard[0][0].callback_data == "menu_home"

    def test_create_rating_keyboard(self):
        """Test rating keyboard creation."""
        keyboard = KeyboardFactory.create_rating_keyboard(5)

        assert (
            len(keyboard.keyboard) == 2
        )  # 5 buttons with row_width=3 = 2 rows
        assert len(keyboard.keyboard[0]) == 3
        assert len(keyboard.keyboard[1]) == 2
        assert keyboard.keyboard[0][0].text == "⭐ (1)"
        assert keyboard.keyboard[1][1].text == "⭐⭐⭐⭐⭐ (5)"

    def test_create_rating_keyboard_without_labels(self):
        """Test rating keyboard without labels."""
        keyboard = KeyboardFactory.create_rating_keyboard(
            3, include_labels=False
        )

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3
        assert keyboard.keyboard[0][0].text == "⭐"
        assert keyboard.keyboard[0][2].text == "⭐⭐⭐"

    def test_create_pagination_keyboard(self):
        """Test pagination keyboard creation."""
        keyboard = KeyboardFactory.create_pagination_keyboard(10, 5)

        assert keyboard.count_pages == 10
        assert keyboard.current_page == 5
        assert len(keyboard.keyboard) == 1
        assert (
            len(keyboard.keyboard[0]) == 5
        )  # first, prev, current, next, last

    def test_create_pagination_keyboard_with_buttons(self):
        """Test pagination keyboard with additional buttons."""
        include_buttons = [
            {"text": "Save", "callback_data": "save"},
            {"text": "Delete", "callback_data": "delete"},
        ]
        keyboard = KeyboardFactory.create_pagination_keyboard(
            5, 3, include_buttons=include_buttons
        )

        assert len(keyboard.keyboard) == 2
        assert len(keyboard.keyboard[0]) == 5  # pagination buttons
        assert len(keyboard.keyboard[1]) == 2  # additional buttons

    def test_create_language_keyboard(self):
        """Test language keyboard creation."""
        keyboard = KeyboardFactory.create_language_keyboard(
            ["en_US", "es_ES", "fr_FR"]
        )

        assert (
            len(keyboard.keyboard) == 2
        )  # 3 buttons with row_width=2 = 2 rows
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 1
        assert keyboard.keyboard[0][0].text == "🇺🇸 English"
        assert keyboard.keyboard[0][1].text == "🇪🇸 Español"
        assert keyboard.keyboard[1][0].text == "🇫🇷 Français"


class TestKeyboardBuilderIntegration:
    """Integration tests for keyboard builder functionality."""

    def test_complex_keyboard_construction(self):
        """Test building a complex keyboard with multiple features."""
        builder = KeyboardBuilder(InlineKeyboard())

        # Build a complex keyboard
        keyboard = (
            builder.add_button("🚀 Start", "start")
            .add_button("⚙️ Settings", "settings")  # Overwrites previous
            .add_row("📊 Stats", "🆘 Help", "❓ FAQ")
            .add_navigation_buttons(10, 5)
            .build()
        )

        assert (
            len(keyboard.keyboard) == 3
        )  # 1 single button + 1 row + 1 pagination
        assert len(keyboard.keyboard[0]) == 1  # settings button
        assert len(keyboard.keyboard[1]) == 3  # row with 3 buttons
        assert len(keyboard.keyboard[2]) == 5  # pagination row

    def test_builder_with_validation_and_transforms(self):
        """Test builder with validation hooks and transforms."""
        builder = KeyboardBuilder(InlineKeyboard())

        # Add validation
        def no_empty_text(button):
            return len(button.text.strip()) > 0

        def add_emoji(button):
            if not button.text.startswith(("🚀", "⚙️", "📊")):
                button.text = f"📝 {button.text}"
            return button

        builder.add_validation_hook(no_empty_text)
        builder.add_button_transform(add_emoji)

        # Build keyboard
        keyboard = (
            builder.add_button("Start", "start")
            .add_button("⚙️ Settings", "settings")  # Overwrites previous
            .build()
        )

        assert len(keyboard.keyboard) == 1
        assert (
            keyboard.keyboard[0][0].text == "⚙️ Settings"
        )  # Last added, not transformed
