# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/builder.py

from functools import wraps
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

from .errors import (ConfigurationError, LocaleError, PaginationError,
                     ValidationError)
from .inline_keyboard import InlineKeyboard
from .keyboard_base import Button, InlineButton, KeyboardBase
from .reply_keyboard import ReplyButton, ReplyKeyboard

T = TypeVar("T", bound=KeyboardBase)


class KeyboardBuilder:
    """Fluent API builder for type-safe keyboard construction.

    This builder provides a fluent interface for constructing keyboards
    with method chaining, making keyboard creation more readable and
    less error-prone.

    Features:
        - Method chaining for fluent API
        - Type-safe button addition
        - Validation hooks
        - Conditional button addition
        - Bulk operations

    Example:
        >>> builder = KeyboardBuilder(InlineKeyboard())
        >>> keyboard = (builder
        ...     .add_button("Yes", "yes")
        ...     .add_button("No", "no")
        ...     .add_row("Maybe", "maybe")
        ...     .build())
    """

    def __init__(self, keyboard: Union[InlineKeyboard, ReplyKeyboard]):
        """Initialize the builder with a keyboard instance.

        Args:
            keyboard: The keyboard to build upon
        """
        self.keyboard = keyboard
        self._validation_hooks: List[Callable[[Any], bool]] = []
        self._button_transforms: List[Callable[[Any], Any]] = []

    def add_validation_hook(
        self, hook: Callable[[Any], bool]
    ) -> "KeyboardBuilder":
        """Add a validation hook that runs before adding buttons.

        Args:
            hook: Function that takes a button and returns True if valid

        Returns:
            Self for method chaining

        Example:
            >>> def validate_text(btn): return len(btn.text) > 0
            >>> builder.add_validation_hook(validate_text)
        """
        self._validation_hooks.append(hook)
        return self

    def add_button_transform(
        self, transform: Callable[[Any], Any]
    ) -> "KeyboardBuilder":
        """Add a button transformation function.

        Args:
            transform: Function that takes a button and returns transformed button

        Returns:
            Self for method chaining

        Example:
            >>> def add_prefix(btn):
            ...     btn.text = f"▶️ {btn.text}"
            ...     return btn
            >>> builder.add_button_transform(add_prefix)
        """
        self._button_transforms.append(transform)
        return self

    def _create_button_from_spec(
        self, btn_spec: Union[str, Dict[str, Any], Any]
    ) -> Any:
        """Create a button from various specification formats."""
        if isinstance(btn_spec, str):
            # Simple text button
            if isinstance(self.keyboard, InlineKeyboard):
                return InlineButton(text=btn_spec)
            else:
                return ReplyButton(text=btn_spec)
        elif isinstance(btn_spec, dict):
            # Dict specification
            if isinstance(self.keyboard, InlineKeyboard):
                return InlineButton(**btn_spec)
            else:
                return ReplyButton(**btn_spec)
        else:
            # Already a button object
            return btn_spec

    def _process_button(self, button: Any) -> Any:
        """Process a button through validation hooks and transforms."""
        # Run validation hooks
        for hook in self._validation_hooks:
            if not hook(button):
                raise ValidationError("button", button, "valid")

        # Apply transforms
        for transform in self._button_transforms:
            button = transform(button)

        return button

    def add_button(
        self, text: str, callback_data: Optional[str] = None, **kwargs
    ) -> "KeyboardBuilder":
        """Add a single button to the keyboard.

        Args:
            text: Button text
            callback_data: Callback data (for inline keyboards)
            **kwargs: Additional button parameters

        Returns:
            Self for method chaining

        Example:
            >>> builder.add_button("Click me", "action:click")
        """
        if isinstance(self.keyboard, InlineKeyboard):
            button = InlineButton(
                text=text, callback_data=callback_data, **kwargs
            )
        else:
            button = ReplyButton(text=text, **kwargs)

        button = self._process_button(button)
        self.keyboard.add(button)
        return self

    def add_buttons(
        self, *buttons: Union[str, Dict[str, Any], Any]
    ) -> "KeyboardBuilder":
        """Add multiple buttons at once.

        Args:
            *buttons: Button specifications (strings, dicts, or button objects)

        Returns:
            Self for method chaining

        Example:
            >>> builder.add_buttons(
            ...     "Yes",
            ...     {"text": "No", "callback_data": "no"},
            ...     InlineButton("Maybe", "maybe")
            ... )
        """
        processed_buttons = []

        for btn_spec in buttons:
            button = self._create_button_from_spec(btn_spec)
            button = self._process_button(button)
            processed_buttons.append(button)

        self.keyboard.add(*processed_buttons)
        return self

    def add_row(
        self, *buttons: Union[str, Dict[str, Any], Any]
    ) -> "KeyboardBuilder":
        """Add a complete row of buttons.

        Args:
            *buttons: Button specifications for the row

        Returns:
            Self for method chaining

        Example:
            >>> builder.add_row("Left", "Right")
        """
        try:
            processed_buttons = []

            for btn_spec in buttons:
                button = self._create_button_from_spec(btn_spec)
                button = self._process_button(button)
                processed_buttons.append(button)

            self.keyboard.row(*processed_buttons)
            return self
        except (
            PaginationError,
            ValidationError,
            LocaleError,
            ConfigurationError,
        ) as e:
            raise e

    def add_conditional_button(
        self,
        condition: bool,
        text: str,
        callback_data: Optional[str] = None,
        **kwargs,
    ) -> "KeyboardBuilder":
        """Add a button only if condition is True.

        Args:
            condition: Whether to add the button
            text: Button text
            callback_data: Callback data
            **kwargs: Additional button parameters

        Returns:
            Self for method chaining

        Example:
            >>> builder.add_conditional_button(
            ...     user.is_admin, "Admin Panel", "admin"
            ... )
        """
        if condition:
            self.add_button(text, callback_data, **kwargs)
        return self

    def add_paginated_buttons(
        self,
        items: List[str],
        callback_pattern: str,
        items_per_page: int = 5,
        current_page: int = 1,
    ) -> "KeyboardBuilder":
        """Add paginated buttons from a list of items.

        Args:
            items: List of item texts
            callback_pattern: Pattern for callback data with {item} and {page} placeholders
            items_per_page: Number of items per page
            current_page: Current page number

        Returns:
            Self for method chaining

        Example:
            >>> items = ["Item 1", "Item 2", "Item 3", "Item 4", "Item 5"]
            >>> builder.add_paginated_buttons(
            ...     items, "select_{item}_page_{page}", 3, 1
            ... )
        """
        start_idx = (current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_items = items[start_idx:end_idx]

        for item in page_items:
            callback_data = callback_pattern.format(
                item=item, page=current_page
            )
            self.add_button(item, callback_data)

        return self

    def add_navigation_buttons(
        self,
        total_pages: int,
        current_page: int,
        callback_pattern: str = "page_{number}",
    ) -> "KeyboardBuilder":
        """Add navigation buttons for pagination.

        Args:
            total_pages: Total number of pages
            current_page: Current page number
            callback_pattern: Pattern for callback data

        Returns:
            Self for method chaining

        Example:
            >>> builder.add_navigation_buttons(5, 3, "nav_{number}")
        """
        if isinstance(self.keyboard, InlineKeyboard):
            self.keyboard.paginate(total_pages, current_page, callback_pattern)
        return self

    def add_language_buttons(
        self,
        locales: List[str],
        callback_pattern: str = "lang_{locale}",
        row_width: int = 2,
    ) -> "KeyboardBuilder":
        """Add language selection buttons.

        Args:
            locales: List of locale codes
            callback_pattern: Pattern for callback data
            row_width: Number of buttons per row

        Returns:
            Self for method chaining

        Example:
            >>> builder.add_language_buttons(
            ...     ["en_US", "ru_RU", "de_DE"], "set_lang_{locale}"
            ... )
        """
        if isinstance(self.keyboard, InlineKeyboard):
            self.keyboard.languages(callback_pattern, locales, row_width)
        return self

    def build(self) -> Union[InlineKeyboard, ReplyKeyboard]:
        """Build and return the final keyboard.

        Returns:
            The constructed keyboard

        Example:
            >>> keyboard = builder.build()
        """
        return self.keyboard


class KeyboardFactory:
    """Factory class for creating keyboards with predefined configurations.

    This factory provides methods for creating common keyboard patterns
    and configurations, making keyboard creation even more convenient.

    Features:
        - Predefined keyboard templates
        - Bulk keyboard creation
        - Configuration presets
        - Keyboard cloning and modification
    """

    @staticmethod
    def create_confirmation_keyboard(
        yes_text: str = "✅ Yes",
        no_text: str = "❌ No",
        cancel_text: Optional[str] = None,
        callback_pattern: str = "confirm_{action}",
        columns: int = 2,
    ) -> InlineKeyboard:
        """Create a confirmation dialog keyboard.

        Args:
            yes_text: Text for yes button
            no_text: Text for no button
            cancel_text: Text for cancel button (optional)
            callback_pattern: Pattern for callback data
            columns: int: Row width of the keyboard

        Returns:
            Configured InlineKeyboard

        Example:
            >>> keyboard = KeyboardFactory.create_confirmation_keyboard()
        """
        keyboard = InlineKeyboard(row_width=columns)
        builder = KeyboardBuilder(keyboard)

        buttons = [
            {
                "text": yes_text,
                "callback_data": callback_pattern.format(action="yes"),
            },
            {
                "text": no_text,
                "callback_data": callback_pattern.format(action="no"),
            },
        ]
        if cancel_text:
            # Ensure cancel button has proper callback_data; pass as dict spec to avoid creating a text-only button
            buttons.append(
                {
                    "text": cancel_text,
                    "callback_data": callback_pattern.format(action="cancel"),
                }
            )

        builder.add_buttons(*buttons)

        return builder.build()

    @staticmethod
    def create_menu_keyboard(
        menu_items: Dict[str, str],
        callback_pattern: str = "menu_{action}",
        columns: int = 2,
    ) -> InlineKeyboard:
        """Create a menu keyboard from a dictionary of items.

        Args:
            menu_items: Dict mapping button text to action
            callback_pattern: Pattern for callback data
            columns: Number of columns

        Returns:
            Configured InlineKeyboard

        Example:
            >>> menu = {"Home": "home", "Settings": "settings", "Help": "help"}
            >>> keyboard = KeyboardFactory.create_menu_keyboard(menu)
        """
        keyboard = InlineKeyboard(row_width=columns)
        builder = KeyboardBuilder(keyboard)

        buttons = []
        for text, action in menu_items.items():
            buttons.append(
                {
                    "text": text,
                    "callback_data": callback_pattern.format(action=action),
                }
            )

        builder.add_buttons(*buttons)
        return builder.build()

    @staticmethod
    def create_rating_keyboard(
        max_rating: int = 5,
        callback_pattern: str = "rate_{stars}",
        include_labels: bool = True,
    ) -> InlineKeyboard:
        """Create a star rating keyboard.

        Args:
            max_rating: Maximum rating value
            callback_pattern: Pattern for callback data
            include_labels: Whether to include rating labels

        Returns:
            Configured InlineKeyboard

        Example:
            >>> keyboard = KeyboardFactory.create_rating_keyboard(5)
        """
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)
        texts = []
        buttons = []

        for i in range(1, max_rating + 1):
            stars = "⭐" * i
            text = f"{stars} ({i})" if include_labels else stars
            texts.append(text)
            buttons.append(
                {
                    "text": text,
                    "callback_data": callback_pattern.format(stars=i),
                }
            )

        builder.add_buttons(*buttons)

        return builder.build()

    @staticmethod
    def create_pagination_keyboard(
        total_pages: int,
        current_page: int,
        callback_pattern: str = "page_{number}",
        include_buttons: Optional[List[Dict[str, str]]] = None,
    ) -> InlineKeyboard:
        """Create a pagination keyboard with optional additional buttons.

        Args:
            total_pages: Total number of pages
            current_page: Current page number
            callback_pattern: Pattern for pagination callbacks
            include_buttons: Additional buttons to include

        Returns:
            Configured InlineKeyboard

        Example:
            >>> keyboard = KeyboardFactory.create_pagination_keyboard(10, 5)
        """
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)

        builder.add_navigation_buttons(
            total_pages, current_page, callback_pattern
        )

        if include_buttons:
            button_specs = []
            for btn in include_buttons:
                button_specs.append(
                    {
                        "text": btn["text"],
                        "callback_data": btn.get(
                            "callback_data", btn["text"].lower()
                        ),
                    }
                )
            builder.add_row(*button_specs)

        return builder.build()

    @staticmethod
    def create_language_keyboard(
        locales: List[str],
        callback_pattern: str = "lang_{locale}",
        row_width: int = 2,
    ) -> InlineKeyboard:
        """Create a language selection keyboard.

        Args:
            locales: List of locale codes
            callback_pattern: Pattern for callback data
            row_width: Number of buttons per row

        Returns:
            Configured InlineKeyboard

        Example:
            >>> keyboard = KeyboardFactory.create_language_keyboard(
            ...     ["en_US", "es_ES", "fr_FR"]
            ... )
        """
        keyboard = InlineKeyboard()
        builder = KeyboardBuilder(keyboard)
        builder.add_language_buttons(locales, callback_pattern, row_width)
        return builder.build()

    @staticmethod
    def clone_keyboard(
        source_keyboard: Union[InlineKeyboard, ReplyKeyboard],
        deep_copy: bool = True,
    ) -> Union[InlineKeyboard, ReplyKeyboard]:
        """Clone an existing keyboard.

        Args:
            source_keyboard: Keyboard to clone
            deep_copy: Whether to perform deep copy

        Returns:
            Cloned keyboard instance

        Example:
            >>> cloned = KeyboardFactory.clone_keyboard(original_keyboard)
        """
        if deep_copy:
            json_data = source_keyboard.to_json()
            if isinstance(source_keyboard, InlineKeyboard):
                return InlineKeyboard.from_json(json_data)
            else:
                return ReplyKeyboard.from_json(json_data)
        else:
            # Shallow copy
            if isinstance(source_keyboard, InlineKeyboard):
                new_keyboard = InlineKeyboard()
            else:
                new_keyboard = ReplyKeyboard()

            new_keyboard.keyboard = source_keyboard.keyboard.copy()
            return new_keyboard


# Convenience functions
def build_inline_keyboard() -> KeyboardBuilder:
    """Create a builder for inline keyboards."""
    return KeyboardBuilder(InlineKeyboard())


def build_reply_keyboard() -> KeyboardBuilder:
    """Create a builder for reply keyboards."""
    return KeyboardBuilder(ReplyKeyboard())


# Decorator for custom keyboard factories
def keyboard_factory(
    func: Callable[..., Union[InlineKeyboard, ReplyKeyboard]],
) -> Callable[..., Union[InlineKeyboard, ReplyKeyboard]]:
    """Decorator to mark functions as keyboard factories.

    This decorator can be used to create custom factory functions
    with additional validation and error handling.

    Example:
        >>> @keyboard_factory
        ... def create_custom_keyboard():
        ...     return InlineKeyboard()
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create keyboard: {e}") from e

    return wrapper
