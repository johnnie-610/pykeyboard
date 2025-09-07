"""Tests for inline keyboard functionality."""

import pytest

from pykeyboard import (InlineButton, InlineKeyboard, LocaleError,
                        PaginationError, PaginationUnchangedError,
                        pagination_client_context)


class TestInlineKeyboard:
    """Test cases for InlineKeyboard class."""

    def test_inline_keyboard_initialization(self):
        """Test inline keyboard initializes correctly."""
        keyboard = InlineKeyboard()
        assert keyboard.row_width == 3
        assert keyboard.keyboard == []
        assert keyboard.callback_pattern == ""
        assert keyboard.count_pages == 0
        assert keyboard.current_page == 0

    def test_pagination_small_keyboard(self):
        """Test pagination with small number of pages."""
        keyboard = InlineKeyboard()
        keyboard.paginate(3, 2, "page_{number}")

        assert keyboard.count_pages == 3
        assert keyboard.current_page == 2
        assert keyboard.callback_pattern == "page_{number}"
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3

    def test_pagination_large_keyboard(self):
        """Test pagination with large number of pages."""
        keyboard = InlineKeyboard()
        keyboard.paginate(10, 5, "page_{number}")

        assert keyboard.count_pages == 10
        assert keyboard.current_page == 5
        assert len(keyboard.keyboard) == 1
        assert (
            len(keyboard.keyboard[0]) == 5
        )  # first, prev, current, next, last

    def test_pagination_edge_cases(self):
        """Test pagination edge cases."""
        # Test with 0 pages (should raise error)
        keyboard = InlineKeyboard()
        with pytest.raises(PaginationError, match="count_pages must be >= 1"):
            keyboard.paginate(0, 1, "page_{number}")

        # Test with negative current_page (should raise error)
        keyboard = InlineKeyboard()
        with pytest.raises(PaginationError, match="current_page must be >= 1"):
            keyboard.paginate(5, -1, "page_{number}")

        # Test with current_page > count_pages (should raise error)
        keyboard = InlineKeyboard()
        with pytest.raises(
            PaginationError, match="current_page.*cannot exceed count_pages"
        ):
            keyboard.paginate(5, 10, "page_{number}")

    def test_language_selection_valid_locale(self):
        """Test language selection with valid locale."""
        keyboard = InlineKeyboard()
        keyboard.languages("lang_{locale}", ["en_US", "ru_RU"], 2)

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 2
        assert keyboard.keyboard[0][0].text == "🇺🇸 English"
        assert keyboard.keyboard[0][1].text == "🇷🇺 Русский"

    def test_language_selection_invalid_locale(self):
        """Test language selection with invalid locale."""
        keyboard = InlineKeyboard()

        with pytest.raises(LocaleError, match="No valid locales found"):
            keyboard.languages("lang_{locale}", ["invalid_locale"], 1)

    def test_language_selection_empty_list(self):
        """Test language selection with empty locale list."""
        keyboard = InlineKeyboard()

        with pytest.raises(LocaleError, match="locales list cannot be empty"):
            keyboard.languages("lang_{locale}", [], 1)

    def test_language_selection_string_input(self):
        """Test language selection with string input instead of list."""
        keyboard = InlineKeyboard()
        keyboard.languages("lang_{locale}", "en_US", 1)

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 1
        assert keyboard.keyboard[0][0].text == "🇺🇸 English"

    def test_language_selection_invalid_row_width(self):
        """Test language selection with invalid row width."""
        keyboard = InlineKeyboard()

        with pytest.raises(LocaleError, match="row_width must be >= 1"):
            keyboard.languages("lang_{locale}", ["en_US"], 0)

    def test_language_selection_invalid_callback_pattern(self):
        """Test language selection with invalid callback pattern."""
        keyboard = InlineKeyboard()

        with pytest.raises(
            LocaleError,
            match="callback_pattern must contain '\\{locale\\}' placeholder",
        ):
            keyboard.languages("invalid_pattern", ["en_US"], 1)

    def test_language_selection_empty_callback_pattern(self):
        """Test language selection with empty callback pattern."""
        keyboard = InlineKeyboard()

        with pytest.raises(
            LocaleError,
            match="callback_pattern must contain '\\{locale\\}' placeholder",
        ):
            keyboard.languages("", ["en_US"], 1)

    def test_language_selection_mixed_valid_invalid_locales(self):
        """Test language selection with mix of valid and invalid locales."""
        keyboard = InlineKeyboard()
        keyboard.languages(
            "lang_{locale}", ["en_US", "invalid", "ru_RU", "also_invalid"], 2
        )

        # Should only include valid locales
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 2
        assert keyboard.keyboard[0][0].text == "🇺🇸 English"
        assert keyboard.keyboard[0][1].text == "🇷🇺 Русский"

    def test_language_selection_large_number_of_locales(self):
        """Test language selection with many locales."""
        locales = [
            "en_US",
            "ru_RU",
            "de_DE",
            "fr_FR",
            "es_ES",
            "it_IT",
            "pt_BR",
            "zh_CN",
            "ja_JP",
            "ko_KR",
        ]
        keyboard = InlineKeyboard()
        keyboard.languages("lang_{locale}", locales, 3)

        # Should create multiple rows
        assert (
            len(keyboard.keyboard) == 4
        )  # 10 locales with 3 per row = 4 rows (3 + 3 + 3 + 1)
        assert len(keyboard.keyboard[0]) == 3
        assert len(keyboard.keyboard[1]) == 3
        assert len(keyboard.keyboard[2]) == 3
        assert len(keyboard.keyboard[3]) == 1

    def test_language_selection_single_row_layout(self):
        """Test language selection with single row layout."""
        keyboard = InlineKeyboard()
        keyboard.languages("lang_{locale}", ["en_US", "ru_RU", "de_DE"], 3)

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3

    def test_language_selection_callback_data_format(self):
        """Test that callback data is formatted correctly."""
        keyboard = InlineKeyboard()
        keyboard.languages("language:{locale}:select", ["en_US", "ru_RU"], 1)

        assert keyboard.keyboard[0][0].callback_data == "language:en_US:select"
        assert keyboard.keyboard[1][0].callback_data == "language:ru_RU:select"

    def test_language_selection_duplicate_locales(self):
        """Test language selection with duplicate locales."""
        keyboard = InlineKeyboard()
        keyboard.languages(
            "lang_{locale}", ["en_US", "ru_RU", "en_US", "ru_RU"], 2
        )

        # Should handle duplicates gracefully - 4 locales with row_width=2 = 2 rows
        assert len(keyboard.keyboard) == 2
        assert len(keyboard.keyboard[0]) == 2

    def test_language_selection_non_string_locale_in_list(self):
        """Test language selection with non-string locale in list."""
        keyboard = InlineKeyboard()

        # Non-string locales are filtered out, so only valid ones are included
        keyboard.languages("lang_{locale}", ["en_US", 123, "ru_RU"], 1)
        assert len(keyboard.keyboard) == 2  # Only en_US and ru_RU are valid
        assert keyboard.keyboard[0][0].callback_data == "lang_en_US"
        assert keyboard.keyboard[1][0].callback_data == "lang_ru_RU"

    def test_language_selection_non_string_non_list_locales(self):
        """Test language selection with invalid locales type."""
        keyboard = InlineKeyboard()

        with pytest.raises(
            LocaleError, match="locales must be a string or list"
        ):
            keyboard.languages("lang_{locale}", 123, 1)

    def test_button_creation_caching(self):
        """Test that button creation uses caching."""
        keyboard = InlineKeyboard()

        # Create same button multiple times
        button1 = keyboard._create_button("Test", "test")
        button2 = keyboard._create_button("Test", "test")

        # Should be the same object due to lru_cache
        assert button1 is button2

    def test_pyrogram_markup_property(self):
        """Test pyrogram markup property."""
        keyboard = InlineKeyboard()
        keyboard.add(InlineButton(text="Test", callback_data="test"))

        markup = keyboard.pyrogram_markup
        assert markup is not None
        assert len(markup.inline_keyboard) == 1

    def test_serialization(self):
        """Test keyboard serialization and deserialization."""
        keyboard = InlineKeyboard()
        keyboard.paginate(5, 3, "page_{number}")

        # Serialize to dict
        data = keyboard.to_dict()
        assert isinstance(data, dict)
        assert "count_pages" in data
        assert "current_page" in data

        # Deserialize from dict
        restored = InlineKeyboard.from_dict(data)
        assert restored.count_pages == keyboard.count_pages
        assert restored.current_page == keyboard.current_page
        assert restored.callback_pattern == keyboard.callback_pattern

    def test_pagination_extreme_edge_cases(self):
        """Test pagination with extreme edge cases."""
        # Test with very large page count
        keyboard = InlineKeyboard()
        keyboard.paginate(1000, 500, "page_{number}")
        assert keyboard.count_pages == 1000
        assert keyboard.current_page == 500

        # Test with page 1 of 1
        keyboard = InlineKeyboard()
        keyboard.paginate(1, 1, "page_{number}")
        assert len(keyboard.keyboard[0]) == 1
        assert keyboard.keyboard[0][0].text == "· 1 ·"

    def test_pagination_invalid_callback_pattern(self):
        """Test pagination with invalid callback pattern."""
        keyboard = InlineKeyboard()

        with pytest.raises(
            PaginationError,
            match="callback_pattern must contain '\\{number\\}' placeholder",
        ):
            keyboard.paginate(5, 1, "invalid_pattern")

    def test_pagination_empty_callback_pattern(self):
        """Test pagination with empty callback pattern."""
        keyboard = InlineKeyboard()

        with pytest.raises(
            PaginationError,
            match="callback_pattern must contain '\\{number\\}' placeholder",
        ):
            keyboard.paginate(5, 1, "")

    def test_keyboard_large_button_count(self):
        """Test keyboard with large number of buttons."""
        keyboard = InlineKeyboard(row_width=5)

        # Add 50 buttons
        buttons = [
            InlineButton(f"Button {i}", f"callback_{i}") for i in range(50)
        ]
        keyboard.add(*buttons)

        # Should create 10 rows of 5 buttons each
        assert len(keyboard.keyboard) == 10
        for row in keyboard.keyboard:
            assert len(row) == 5

    def test_keyboard_mixed_button_types(self):
        """Test keyboard with mixed button types and properties."""
        keyboard = InlineKeyboard()

        # Add buttons with different properties
        button1 = InlineButton("URL Button", url="https://example.com")
        button2 = InlineButton("Callback Button", callback_data="test")
        button3 = InlineButton(
            "Complex Button",
            callback_data="complex",
            url="https://example.com",
            web_app=None,
        )

        keyboard.add(button1, button2, button3)

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3

    def test_keyboard_empty_operations(self):
        """Test keyboard operations with empty inputs."""
        keyboard = InlineKeyboard()

        # Empty add should work
        keyboard.add()
        assert keyboard.keyboard == []

        # Empty row should work
        keyboard.row()
        assert len(keyboard.keyboard) == 1
        assert keyboard.keyboard[0] == []

    def test_keyboard_row_width_edge_cases(self):
        """Test keyboard with extreme row width values."""
        # Very small row width
        keyboard = InlineKeyboard(row_width=1)
        keyboard.add("A", "B", "C")

        assert len(keyboard.keyboard) == 3
        for row in keyboard.keyboard:
            assert len(row) == 1

        # Very large row width
        keyboard = InlineKeyboard(row_width=100)
        keyboard.add("A", "B", "C")

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3

    def test_keyboard_chaining_operations(self):
        """Test chaining multiple keyboard operations."""
        keyboard = InlineKeyboard(row_width=2)

        # Chain add and row operations (add replaces, row appends)
        keyboard.add("A", "B", "C").row("D", "E").row("F")

        assert (
            len(keyboard.keyboard) == 4
        )  # 2 rows from add, 1 from first row, 1 from second row
        assert keyboard.keyboard[0] == ["A", "B"]
        assert keyboard.keyboard[1] == ["C"]
        assert keyboard.keyboard[2] == ["D", "E"]
        # Note: "F" is not included because row() appends but doesn't replace like add()

    def test_custom_locale_operations(self):
        """Test custom locale operations."""
        keyboard = InlineKeyboard()

        # Add custom locales
        keyboard.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")
        keyboard.add_custom_locale("es_LATINO", "🇲🇽 Español Latino")

        # Verify custom locales are stored
        custom_locales = keyboard.get_custom_locales()
        assert "en_PIRATE" in custom_locales
        assert "es_LATINO" in custom_locales
        assert custom_locales["en_PIRATE"] == "🏴‍☠️ Pirate English"

        # Test language selection with custom locales
        keyboard.languages("lang_{locale}", ["en_PIRATE", "es_LATINO"], 1)
        assert len(keyboard.keyboard) == 2
        assert keyboard.keyboard[0][0].text == "🏴‍☠️ Pirate English"
        assert keyboard.keyboard[1][0].text == "🇲🇽 Español Latino"

    def test_custom_locale_removal(self):
        """Test custom locale removal."""
        keyboard = InlineKeyboard()
        keyboard.add_custom_locale("test_locale", "Test Display")

        # Remove existing locale
        assert keyboard.remove_custom_locale("test_locale") is True
        assert "test_locale" not in keyboard.get_custom_locales()

        # Try to remove non-existent locale
        assert keyboard.remove_custom_locale("non_existent") is False

    def test_custom_locale_clear(self):
        """Test clearing all custom locales."""
        keyboard = InlineKeyboard()
        keyboard.add_custom_locale("locale1", "Display1")
        keyboard.add_custom_locale("locale2", "Display2")

        assert len(keyboard.get_custom_locales()) == 2

        keyboard.clear_custom_locales()
        assert len(keyboard.get_custom_locales()) == 0

    def test_get_all_locales_with_custom(self):
        """Test get_all_locales includes both built-in and custom locales."""
        keyboard = InlineKeyboard()
        keyboard.add_custom_locale("custom_test", "Custom Test")

        all_locales = keyboard.get_all_locales()
        assert "en_US" in all_locales  # Built-in
        assert "custom_test" in all_locales  # Custom
        assert all_locales["custom_test"] == "Custom Test"

    def test_custom_locale_validation(self):
        """Test custom locale validation."""
        keyboard = InlineKeyboard()

        # Valid custom locale
        keyboard.add_custom_locale("valid_code", "Valid Display")
        assert "valid_code" in keyboard.get_custom_locales()

        # Invalid empty code
        with pytest.raises(
            ValueError, match="locale_code must be a non-empty string"
        ):
            keyboard.add_custom_locale("", "Display")

        # Invalid empty display
        with pytest.raises(
            ValueError, match="display_name must be a non-empty string"
        ):
            keyboard.add_custom_locale("code", "")

    def test_custom_locale_override_builtin(self):
        """Test that custom locales override built-in ones."""
        keyboard = InlineKeyboard()

        # Override built-in en_US
        keyboard.add_custom_locale("en_US", "Custom English")

        all_locales = keyboard.get_all_locales()
        assert (
            all_locales["en_US"] == "Custom English"
        )  # Should be custom, not built-in

    def test_pagination_duplicate_prevention_default_source(self):
        """Test duplicate prevention with default source."""
        keyboard = InlineKeyboard()

        # First call should work
        keyboard.paginate(5, 3, "page_{number}")
        assert keyboard.count_pages == 5
        assert keyboard.current_page == 3

        # Second call with same parameters should raise PaginationUnchangedError
        with pytest.raises(PaginationUnchangedError) as exc_info:
            keyboard.paginate(5, 3, "page_{number}")

        error = exc_info.value
        assert error.source == "default"
        assert error.keyboard_hash == error.previous_hash

    def test_pagination_duplicate_prevention_explicit_source(self):
        """Test duplicate prevention with explicit source."""
        keyboard = InlineKeyboard()

        # First call should work
        keyboard.paginate(5, 3, "page_{number}", source="client_1")
        assert keyboard.count_pages == 5

        # Second call with same parameters and source should raise error
        with pytest.raises(PaginationUnchangedError) as exc_info:
            keyboard.paginate(5, 3, "page_{number}", source="client_1")

        error = exc_info.value
        assert error.source == "client_1"

        # Different source should work
        keyboard2 = InlineKeyboard()
        keyboard2.paginate(5, 3, "page_{number}", source="client_2")
        assert keyboard2.count_pages == 5

    def test_pagination_duplicate_prevention_different_parameters(self):
        """Test that different parameters don't trigger duplicate prevention."""
        keyboard = InlineKeyboard()

        # Clear any existing hashes
        InlineKeyboard.clear_pagination_hashes()

        # First call
        keyboard.paginate(5, 3, "page_{number}")
        assert keyboard.count_pages == 5

        # Different page should work
        keyboard.paginate(5, 4, "page_{number}")
        assert keyboard.current_page == 4

        # Different count should work
        keyboard.paginate(6, 4, "page_{number}")
        assert keyboard.count_pages == 6

        # Different pattern should work
        keyboard.paginate(6, 4, "nav_{number}")
        assert keyboard.callback_pattern == "nav_{number}"

    def test_pagination_duplicate_prevention_contextvar(self):
        """Test duplicate prevention with contextvar."""
        # Set contextvar
        pagination_client_context.set("test_client")

        keyboard = InlineKeyboard()

        # First call should work
        keyboard.paginate(5, 3, "page_{number}")
        assert keyboard.count_pages == 5

        # Second call should raise error due to contextvar
        with pytest.raises(PaginationUnchangedError) as exc_info:
            keyboard.paginate(5, 3, "page_{number}")

        error = exc_info.value
        assert error.source == "test_client"

        # Reset contextvar
        pagination_client_context.set(None)

    def test_pagination_duplicate_prevention_explicit_overrides_contextvar(
        self,
    ):
        """Test that explicit source parameter overrides contextvar."""
        # Set contextvar
        pagination_client_context.set("context_client")

        keyboard = InlineKeyboard()

        # First call with explicit source
        keyboard.paginate(5, 3, "page_{number}", source="explicit_client")
        assert keyboard.count_pages == 5

        # Second call with same explicit source should raise error
        with pytest.raises(PaginationUnchangedError) as exc_info:
            keyboard.paginate(5, 3, "page_{number}", source="explicit_client")

        error = exc_info.value
        assert error.source == "explicit_client"

        # Reset contextvar
        pagination_client_context.set(None)

    def test_pagination_duplicate_prevention_isolation_between_sources(self):
        """Test that different sources have isolated duplicate prevention."""
        keyboard1 = InlineKeyboard()
        keyboard2 = InlineKeyboard()

        # Both keyboards can have same pagination without conflict
        keyboard1.paginate(5, 3, "page_{number}", source="client_a")
        keyboard2.paginate(5, 3, "page_{number}", source="client_b")

        # Each should raise error only for their own source
        with pytest.raises(PaginationUnchangedError) as exc_info:
            keyboard1.paginate(5, 3, "page_{number}", source="client_a")
        assert exc_info.value.source == "client_a"

        with pytest.raises(PaginationUnchangedError) as exc_info:
            keyboard2.paginate(5, 3, "page_{number}", source="client_b")
        assert exc_info.value.source == "client_b"
