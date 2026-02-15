# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/keyboard_base.py
import logging
from typing import TYPE_CHECKING, Any, List, Optional, Union

from pydantic import BaseModel, Field, field_validator
from pyrogram.types import (CallbackGame, InlineKeyboardButton, KeyboardButton,
                            LoginUrl, WebAppInfo)

from pykeyboard.errors import ValidationError

if TYPE_CHECKING:
    pass

logger = logging.getLogger("pykeyboard.keyboard_base")

class KeyboardBase(BaseModel):
    """Base class for keyboard implementations with row-based layout.

    This class provides the foundation for creating different types of keyboards
    with row-based layouts. It handles the core functionality of organizing buttons
    into rows and provides a consistent interface for keyboard construction.

    Attributes:
        row_width: Number of buttons per row. Must be >= 1.
        keyboard: 2D list representing the keyboard layout structure.

    Example:
        >>> keyboard = KeyboardBase(row_width=2)
        >>> keyboard.add("Button 1", "Button 2", "Button 3")
        >>> keyboard.keyboard
        [['Button 1', 'Button 2'], ['Button 3']]
    """

    model_config = {"arbitrary_types_allowed": True}

    row_width: int = Field(
        default=3, ge=1, description="Number of buttons per row"
    )
    keyboard: List[List[Union[InlineKeyboardButton, KeyboardButton, Any]]] = (
        Field(
            default_factory=list,
            description="2D list representing keyboard layout",
        )
    )

    def add(self, *args: Any) -> "KeyboardBase":
        """Add buttons to keyboard in rows based on row_width.

        This method automatically organizes the provided buttons into rows
        based on the row_width setting. Each row will contain up to row_width
        buttons, with the last row potentially having fewer buttons.

        Note: This method replaces the entire keyboard content. For chaining
        operations that preserve existing content, use row() method or call
        add() once with all buttons.

        Args:
            *args: Variable number of buttons or button-like objects to add.

        Time complexity: O(n) where n is the number of buttons.

        Example:
            >>> keyboard = KeyboardBase(row_width=2)
            >>> keyboard.add("A", "B", "C", "D", "E")
            >>> keyboard.keyboard
            [['A', 'B'], ['C', 'D'], ['E']]
        """
        self.keyboard.clear()
        for i in range(0, len(args), self.row_width):
            row_slice = args[i : i + self.row_width]
            self.keyboard.append(
                list(row_slice)
            )  # Only convert slice to list once
        self._update_keyboard()
        return self

    def row(self, *args: Any) -> "KeyboardBase":
        """Add a new row of buttons to the keyboard.

        This method adds all provided buttons as a single row, regardless
        of the row_width setting. This is useful for creating rows with
        different numbers of buttons or for precise layout control.

        Args:
            *args: Variable number of buttons to add as a single row.

        Time complexity: O(k) where k is the number of buttons in the row.

        Example:
            >>> keyboard = KeyboardBase()
            >>> keyboard.row("Yes", "No")
            >>> keyboard.row("Maybe", "Cancel")
            >>> keyboard.keyboard
            [['Yes', 'No'], ['Maybe', 'Cancel']]
        """
        self.keyboard.append(list(args))
        self._update_keyboard()
        return self

    def _update_keyboard(self) -> None:
        """Update the underlying Pyrogram structure.

        This method is called after any keyboard modification to ensure
        the Pyrogram-compatible markup stays in sync with the internal
        keyboard representation. Subclasses should override this method
        to implement their specific update logic.

        This is an internal method and should not be called directly.
        """
        pass


class Button(BaseModel):
    """Base button model with text validation.

    This is the foundation class for all button types in PyKeyboard.
    It provides essential text validation and serves as the base
    for more specialized button implementations.

    Attributes:
        text: The display text for the button. Must be a non-empty string.

    Raises:
        ValueError: If text is not a string or is empty/whitespace-only.

    Example:
        >>> button = Button(text="Click me!")
        >>> button.text
        'Click me!'
    """

    text: str = Field(..., min_length=1, description="Button display text")

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate that button text is a non-empty string.

        Args:
            v: The text value to validate.

        Returns:
            The validated text string.

        Raises:
            ValueError: If text is not a string or is empty/whitespace-only.
        """
        if not v.strip():
            raise ValidationError(
                "text", v, expected="non-empty string", reason="text cannot be empty"
            )
        return v


class InlineButton(Button):
    """Inline keyboard button with comprehensive Pyrogram integration.

    This class represents an inline keyboard button with all possible
    Pyrogram InlineKeyboardButton features. It provides full type safety
    and validation while maintaining compatibility with Pyrogram.

    Attributes:
        text: Button display text (inherited from Button).
        callback_data: Callback data sent when button is pressed.
        url: URL to open when button is pressed.
        web_app: Web app to open.
        login_url: Login URL for authorization.
        user_id: User ID for the button.
        switch_inline_query: Switch to inline query.
        switch_inline_query_current_chat: Switch to inline query in current chat.
        callback_game: Callback game.
        requires_password: Whether password is required.
        pay: Whether this is a pay button.
        copy_text: Text to copy to clipboard.

    Note:
        Only one of the optional fields should be used per button.

    Example:
        >>> button = InlineButton(
        ...     text="Visit Website",
        ...     url="https://example.com"
        ... )
        >>> button2 = InlineButton(
        ...     text="Pay",
        ...     pay=True
        ... )

    Positional Constructor (Deprecated):
        For backward compatibility, positional arguments are supported but deprecated:

        >>> button = InlineButton("Click me", "callback_data")  # Deprecated
        >>> button = InlineButton(text="Click me", callback_data="callback_data")  # Preferred
    """

    # Configure Pydantic to allow arbitrary types from Pyrogram
    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, *args, **kwargs):
        """Initialize InlineButton with positional or keyword arguments.

        Supports both positional and keyword arguments for backward compatibility,
        but positional arguments are deprecated in favor of keyword arguments.

        Args:
            *args: Positional arguments (deprecated)
                - args[0]: text (str)
                - args[1]: callback_data (optional, str)
            **kwargs: Keyword arguments (preferred)
                - text: Button display text
                - callback_data: Callback data
                - url: URL to open
                - And other InlineKeyboardButton fields

        Raises:
            DeprecationWarning: When using positional arguments
            ValueError: If positional arguments are invalid
        """
        import warnings

        if args:
            # Handle positional arguments (deprecated)
            warnings.warn(
                "Positional arguments for InlineButton are deprecated. "
                "Use keyword arguments instead: InlineButton(text='...', callback_data='...')",
                DeprecationWarning,
                stacklevel=2,
            )

            if len(args) == 1:
                kwargs.setdefault("text", args[0])
            elif len(args) == 2:
                kwargs.setdefault("text", args[0])
                kwargs.setdefault("callback_data", args[1])
            else:
                raise ValueError(
                    f"InlineButton expects 1-2 positional arguments, got {len(args)}. "
                    "Use keyword arguments: InlineButton(text='...', callback_data='...')"
                )

        super().__init__(**kwargs)

    callback_data: Optional[Union[str, bytes]] = Field(
        default=None, description="Callback data for the button"
    )
    url: Optional[str] = Field(
        default=None, description="URL to open when button is pressed"
    )
    web_app: Optional[WebAppInfo] = Field(
        default=None, description="Web app to open"
    )
    login_url: Optional[LoginUrl] = Field(
        default=None, description="Login URL for authorization"
    )
    user_id: Optional[int] = Field(
        default=None, description="User ID for the button"
    )
    switch_inline_query: Optional[str] = Field(
        default=None, description="Switch to inline query"
    )
    switch_inline_query_current_chat: Optional[str] = Field(
        default=None, description="Switch to inline query in current chat"
    )
    callback_game: Optional[CallbackGame] = Field(
        default=None, description="Callback game"
    )
    requires_password: Optional[bool] = Field(
        default=None, description="Whether password is required"
    )
    pay: Optional[bool] = Field(
        default=None, description="Whether this is a pay button"
    )
    copy_text: Optional[str] = Field(
        default=None, description="Text to copy to clipboard"
    )

    def to_pyrogram(self) -> InlineKeyboardButton:
        """Convert to Pyrogram InlineKeyboardButton.

        Creates a Pyrogram-compatible InlineKeyboardButton instance
        with all the current button's properties.

        Returns:
            InlineKeyboardButton: Pyrogram-compatible button instance.

        Example:
            >>> button = InlineButton(text="Test", callback_data="test")
            >>> pyrogram_btn = button.to_pyrogram()
            >>> isinstance(pyrogram_btn, InlineKeyboardButton)
            True
        """
        return InlineKeyboardButton(
            text=self.text,
            callback_data=self.callback_data,
            url=self.url,
            web_app=self.web_app,
            login_url=self.login_url,
            user_id=self.user_id,
            switch_inline_query=self.switch_inline_query,
            switch_inline_query_current_chat=self.switch_inline_query_current_chat,
            callback_game=self.callback_game,
            requires_password=self.requires_password,
            pay=self.pay,
            copy_text=self.copy_text,
        )

    async def write(self, client: Any) -> Any:
        """Pyrogram serialization method.

        This method is called by Pyrogram to serialize the button for sending
        to Telegram. It delegates to the Pyrogram button's write method.

        Args:
            client: The Pyrogram client instance.

        Returns:
            Serialized button data for Telegram API.
        """
        pyrogram_button = self.to_pyrogram()
        return await pyrogram_button.write(client)
