# Copyright (c) 2025-2026 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/utils.py

import logging
from typing import Any, Dict, List, Union

from .inline_keyboard import InlineKeyboard
from .keyboard_base import InlineButton
from .reply_keyboard import ReplyButton, ReplyKeyboard

logger = logging.getLogger("pykeyboard.utils")


def create_keyboard_from_config(
    config: Dict[str, Any],
) -> Union[InlineKeyboard, ReplyKeyboard]:
    """Create a keyboard from a configuration dictionary.

    Args:
        config: Configuration dictionary with keyboard settings.
            Supported keys:
                - ``type`` (str): ``"inline"`` (default) or ``"reply"``.
                - ``row_width`` (int): Number of buttons per row.
                - ``buttons`` (list): List of button configs (dicts or plain strings).

    Returns:
        Configured keyboard instance.

    Raises:
        ValueError: If ``type`` is not ``"inline"`` or ``"reply"``.

    Example::

        config = {
            "type": "inline",
            "row_width": 2,
            "buttons": [
                {"text": "Yes", "callback_data": "yes"},
                {"text": "No", "callback_data": "no"},
            ],
        }
        keyboard = create_keyboard_from_config(config)
    """
    keyboard_type = config.get("type", "inline").lower()

    if keyboard_type == "inline":
        keyboard = InlineKeyboard()
    elif keyboard_type == "reply":
        keyboard = ReplyKeyboard()
    else:
        raise ValueError(f"Unsupported keyboard type: {keyboard_type}")

    if "row_width" in config:
        keyboard.row_width = config["row_width"]

    buttons = config.get("buttons", [])
    button_objects = []

    for button_config in buttons:
        if isinstance(button_config, dict):
            if keyboard_type == "inline":
                button = InlineButton(**button_config)
            else:
                button = ReplyButton(**button_config)
        else:
            if keyboard_type == "inline":
                button = InlineButton(text=str(button_config))
            else:
                button = ReplyButton(text=str(button_config))

        button_objects.append(button)

    keyboard.add(*button_objects)
    return keyboard


def get_keyboard_info(
    keyboard: Union[InlineKeyboard, ReplyKeyboard],
) -> Dict[str, Any]:
    """Get comprehensive information about a keyboard.

    Args:
        keyboard: The keyboard to analyze.

    Returns:
        Dictionary with keyboard metadata and statistics.
    """
    info: Dict[str, Any] = {
        "type": type(keyboard).__name__,
        "row_width": keyboard.row_width,
        "total_buttons": sum(len(row) for row in keyboard.keyboard),
        "total_rows": len(keyboard.keyboard),
    }

    if isinstance(keyboard, InlineKeyboard):
        info.update(
            {
                "has_pagination": keyboard.count_pages > 0,
                "current_page": keyboard.current_page,
                "total_pages": keyboard.count_pages,
                "callback_pattern": keyboard.callback_pattern,
                "custom_locales_count": len(keyboard.custom_locales),
            }
        )
    elif isinstance(keyboard, ReplyKeyboard):
        info.update(
            {
                "is_persistent": keyboard.is_persistent,
                "resize_keyboard": keyboard.resize_keyboard,
                "one_time_keyboard": keyboard.one_time_keyboard,
                "selective": keyboard.selective,
                "placeholder": keyboard.placeholder,
            }
        )

    return info


def validate_keyboard_config(config: Dict[str, Any]) -> List[str]:
    """Validate a keyboard configuration dictionary.

    Args:
        config: Configuration dictionary to validate.

    Returns:
        List of validation error messages (empty if valid).
    """
    errors: List[str] = []

    if "type" in config and config["type"] not in ("inline", "reply"):
        errors.append(f"Invalid keyboard type: {config['type']}")

    if "row_width" in config:
        width = config["row_width"]
        if not isinstance(width, int) or width < 1:
            errors.append("row_width must be a positive integer")

    if "buttons" in config and not isinstance(config["buttons"], list):
        errors.append("buttons must be a list")

    return errors
