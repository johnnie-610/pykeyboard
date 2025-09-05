# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/reply_keyboard.py

from typing import Optional, Any
from pydantic import BaseModel, Field, model_validator, PrivateAttr
from pyrogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
    ForceReply,
    KeyboardButtonPollType,
    KeyboardButtonRequestUsers,
    KeyboardButtonRequestChat,
    WebAppInfo,
)
from .keyboard_base import KeyboardBase, Button


class ReplyKeyboard(KeyboardBase):
    """Reply keyboard with comprehensive Pyrogram integration and customization options.

    This class provides a feature-rich reply keyboard implementation with all
    Pyrogram ReplyKeyboardMarkup options. It supports persistent keyboards,
    resizing, one-time usage, selective display, and custom placeholders.

    Attributes:
        row_width: Number of buttons per row (inherited from KeyboardBase).
        keyboard: 2D list representing keyboard layout (inherited from KeyboardBase).
        is_persistent: Whether the keyboard persists after sending a message.
        resize_keyboard: Whether the keyboard should be resized to fit content.
        one_time_keyboard: Whether the keyboard disappears after one use.
        selective: Whether the keyboard is shown only to specific users.
        placeholder: Placeholder text shown in the input field.

    Example:
        >>> keyboard = ReplyKeyboard(
        ...     resize_keyboard=True,
        ...     one_time_keyboard=True,
        ...     placeholder="Choose an option..."
        ... )
        >>> keyboard.add("Yes", "No", "Maybe")
        >>> # Use with Kurigram
        >>> await message.reply_text("What do you think?", reply_markup=keyboard.pyrogram_markup)
    """

    is_persistent: Optional[bool] = Field(None, description="Whether the keyboard is persistent")
    resize_keyboard: Optional[bool] = Field(None, description="Whether to resize the keyboard")
    one_time_keyboard: Optional[bool] = Field(None, description="Whether it's a one-time keyboard")
    selective: Optional[bool] = Field(None, description="Whether the keyboard is selective")
    placeholder: Optional[str] = Field(None, description="Placeholder text for the input field")

    pyrogram_markup: Optional[ReplyKeyboardMarkup] = PrivateAttr(default=None)

    @model_validator(mode='after')
    def initialize_pyrogram_markup(self) -> 'ReplyKeyboard':
        """Initialize the Pyrogram ReplyKeyboardMarkup after model creation."""
        self.pyrogram_markup = ReplyKeyboardMarkup(
            keyboard=self.keyboard,
            is_persistent=self.is_persistent,
            resize_keyboard=self.resize_keyboard,
            one_time_keyboard=self.one_time_keyboard,
            selective=self.selective,
            placeholder=self.placeholder,
        )
        return self

    def _update_keyboard(self) -> None:
        """Update the underlying Pyrogram ReplyKeyboardMarkup."""
        super()._update_keyboard()
        if self.pyrogram_markup:
            self.pyrogram_markup.keyboard = self.keyboard

    @property
    def pyrogram_markup(self) -> ReplyKeyboardMarkup:
        """Get the Pyrogram ReplyKeyboardMarkup for this keyboard."""
        if self.pyrogram_markup is None:
            self.pyrogram_markup = ReplyKeyboardMarkup(
                keyboard=self.keyboard,
                is_persistent=self.is_persistent,
                resize_keyboard=self.resize_keyboard,
                one_time_keyboard=self.one_time_keyboard,
                selective=self.selective,
                placeholder=self.placeholder,
            )
        return self.pyrogram_markup

    def write(self, client: Any = None) -> Any:
        """Pyrogram serialization hook to allow passing this object directly as reply_markup."""
        return self.pyrogram_markup.write(client)


class ReplyButton(Button):
    """Reply keyboard button with comprehensive Pyrogram integration and advanced features.

    This class extends the base Button class with all Pyrogram KeyboardButton
    capabilities, including contact/location requests, poll creation, user/chat
    selection, and web app integration.

    Attributes:
        text: Button display text (inherited from Button).
        request_contact: Request user's contact information when pressed.
        request_location: Request user's location when pressed.
        request_poll: Request poll creation with specified type.
        request_users: Request user selection with specified criteria.
        request_chat: Request chat selection with specified criteria.
        web_app: Web app to open when button is pressed.

    Note:
        Only one request_* field should be set per button for optimal UX.

    Example:
        >>> # Contact request button
        >>> contact_btn = ReplyButton(
        ...     text="📱 Share Contact",
        ...     request_contact=True
        ... )
        >>>
        >>> # Location request button
        >>> location_btn = ReplyButton(
        ...     text="📍 Share Location",
        ...     request_location=True
        ... )
        >>>
        >>> # Web app button
        >>> web_btn = ReplyButton(
        ...     text="Open App",
        ...     web_app=WebAppInfo(url="https://example.com")
        ... )

    Positional Constructor (Deprecated):
        For backward compatibility, positional arguments are supported but deprecated:

        >>> button = ReplyButton("Click me")  # Deprecated
        >>> button = ReplyButton(text="Click me")  # Preferred
    """

    model_config = {"arbitrary_types_allowed": True}

    def __init__(self, *args, **kwargs):
        """Initialize ReplyButton with positional or keyword arguments.

        Supports both positional and keyword arguments for backward compatibility,
        but positional arguments are deprecated in favor of keyword arguments.

        Args:
            *args: Positional arguments (deprecated)
                - args[0]: text (str)
            **kwargs: Keyword arguments (preferred)
                - text: Button display text
                - request_contact: Request contact
                - request_location: Request location
                - And other KeyboardButton fields

        Raises:
            DeprecationWarning: When using positional arguments
            ValueError: If positional arguments are invalid
        """
        import warnings

        if args:
            warnings.warn(
                "Positional arguments for ReplyButton are deprecated. "
                "Use keyword arguments instead: ReplyButton(text='...')",
                DeprecationWarning,
                stacklevel=2
            )

            if len(args) == 1:
                kwargs.setdefault('text', args[0])
            else:
                raise ValueError(
                    f"ReplyButton expects 1 positional argument, got {len(args)}. "
                    "Use keyword arguments: ReplyButton(text='...')"
                )

        super().__init__(**kwargs)

    request_contact: Optional[bool] = Field(None, description="Request contact information")
    request_location: Optional[bool] = Field(None, description="Request location information")
    request_poll: Optional[KeyboardButtonPollType] = Field(None, description="Request poll")
    request_users: Optional[KeyboardButtonRequestUsers] = Field(None, description="Request users")
    request_chat: Optional[KeyboardButtonRequestChat] = Field(None, description="Request chat")
    web_app: Optional[WebAppInfo] = Field(None, description="Web app to open")

    def to_pyrogram(self) -> KeyboardButton:
        """Convert to Pyrogram KeyboardButton.

        Creates a Pyrogram-compatible KeyboardButton instance with all
        the current button's properties and request capabilities.

        Returns:
            KeyboardButton: Pyrogram-compatible button instance.

        Example:
            >>> button = ReplyButton(text="Contact", request_contact=True)
            >>> pyrogram_btn = button.to_pyrogram()
            >>> isinstance(pyrogram_btn, KeyboardButton)
            True
        """
        return KeyboardButton(
            text=self.text,
            request_contact=self.request_contact,
            request_location=self.request_location,
            request_poll=self.request_poll,
            request_users=self.request_users,
            request_chat=self.request_chat,
            web_app=self.web_app,
        )

    def write(self, client: Any = None) -> Any:
        """Pyrogram serialization method.

        This method is called by Pyrogram to serialize the button for sending
        to Telegram. It delegates to the Pyrogram button's write method.

        Args:
            client: The Pyrogram client instance (optional).

        Returns:
            Serialized button data for Telegram API.
        """
        pyrogram_button = self.to_pyrogram()

        return pyrogram_button.write()


class PyReplyKeyboardRemove(BaseModel):
    """Remove reply keyboard markup with selective option.

    This class provides a convenient way to remove reply keyboards from chat.
    It wraps Pyrogram's ReplyKeyboardRemove with additional type safety and
    validation.

    Attributes:
        selective: Whether the removal should be selective (only for specific users).

    Example:
        >>> # Remove keyboard for all users
        >>> remove_all = PyReplyKeyboardRemove()
        >>>
        >>> # Remove keyboard selectively
        >>> remove_selective = PyReplyKeyboardRemove(selective=True)
        >>>
        >>> # Use with Kurigram
        >>> await message.reply_text("Keyboard removed", reply_markup=remove_all.to_pyrogram())
    """

    selective: Optional[bool] = Field(None, description="Whether the action is selective")

    def to_pyrogram(self) -> ReplyKeyboardRemove:
        """Convert to Pyrogram ReplyKeyboardRemove.

        Creates a Pyrogram-compatible ReplyKeyboardRemove instance.

        Returns:
            ReplyKeyboardRemove: Pyrogram-compatible remove markup.

        Example:
            >>> remover = PyReplyKeyboardRemove(selective=True)
            >>> pyrogram_remove = remover.to_pyrogram()
        """
        return ReplyKeyboardRemove(selective=self.selective)

    def write(self, client: Any = None) -> Any:
        """Pyrogram serialization hook to allow passing this object directly as reply_markup."""
        return self.to_pyrogram().write(client)


class PyForceReply(BaseModel):
    """Force user to send a reply with selective and placeholder options.

    This class provides a convenient way to force users to send a reply message.
    It wraps Pyrogram's ForceReply with additional type safety and validation.

    Attributes:
        selective: Whether the force reply should be selective (only for specific users).
        placeholder: Placeholder text shown in the input field when forcing reply.

    Example:
        >>> # Force reply for all users
        >>> force_all = PyForceReply(placeholder="Please reply...")
        >>>
        >>> # Force reply selectively
        >>> force_selective = PyForceReply(
        ...     selective=True,
        ...     placeholder="Reply to this message"
        ... )
        >>>
        >>> # Use with Kurigram
        >>> await message.reply_text("Please reply", reply_markup=force_all.to_pyrogram())
    """

    selective: Optional[bool] = Field(None, description="Whether the action is selective")
    placeholder: Optional[str] = Field(None, description="Placeholder text for the input field")

    def to_pyrogram(self) -> ForceReply:
        """Convert to Pyrogram ForceReply.

        Creates a Pyrogram-compatible ForceReply instance.

        Returns:
            ForceReply: Pyrogram-compatible force reply markup.

        Example:
            >>> force_reply = PyForceReply(placeholder="Type your response...")
            >>> pyrogram_force = force_reply.to_pyrogram()
        """
        return ForceReply(selective=self.selective, placeholder=self.placeholder)

    def write(self, client: Any = None) -> Any:
        """Pyrogram serialization hook to allow passing this object directly as reply_markup."""
        return self.to_pyrogram().write(client)


def _add_serialization_methods(cls):
    """Add JSON serialization methods to keyboard classes."""
    def to_json(self) -> str:
        """Convert keyboard to JSON string.

        Serializes the keyboard to a JSON string that can be stored in files,
        databases, or sent over network connections.

        Returns:
            str: JSON representation of the keyboard.

        Example:
            >>> keyboard = ReplyKeyboard()
            >>> keyboard.add("Yes", "No")
            >>> json_str = keyboard.to_json()
        """
        return self.model_dump_json()

    @classmethod
    def from_json(cls, json_str: str):
        """Create keyboard instance from JSON string.

        Deserializes a keyboard from a JSON string created by to_json().
        This method validates the JSON data and reconstructs the keyboard.

        Args:
            json_str: JSON string representation of a keyboard.

        Returns:
            Reconstructed keyboard instance.

        Raises:
            ValidationError: If the JSON data is invalid or malformed.

        Example:
            >>> json_str = '{"keyboard":[["Yes","No"]]}'
            >>> keyboard = ReplyKeyboard.from_json(json_str)
        """
        return cls.model_validate_json(json_str)

    cls.to_json = to_json
    cls.from_json = classmethod(from_json)
    return cls


# Apply serialization methods to keyboard classes
ReplyKeyboard = _add_serialization_methods(ReplyKeyboard)
ReplyButton = _add_serialization_methods(ReplyButton)
PyReplyKeyboardRemove = _add_serialization_methods(PyReplyKeyboardRemove)
PyForceReply = _add_serialization_methods(PyForceReply)
