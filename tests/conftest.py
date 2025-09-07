"""Pytest configuration and fixtures for pykeyboard tests."""

from typing import List

import pytest

from pykeyboard import InlineButton, InlineKeyboard, ReplyButton, ReplyKeyboard


@pytest.fixture
def sample_inline_buttons() -> List[InlineButton]:
    """Sample inline buttons for testing."""
    return [
        InlineButton(text="Button 1", callback_data="btn1"),
        InlineButton(text="Button 2", callback_data="btn2"),
        InlineButton(text="Button 3", callback_data="btn3"),
    ]


@pytest.fixture
def sample_reply_buttons() -> List[ReplyButton]:
    """Sample reply buttons for testing."""
    return [
        ReplyButton(text="Reply 1"),
        ReplyButton(text="Reply 2"),
        ReplyButton(text="Reply 3"),
    ]


@pytest.fixture
def inline_keyboard() -> InlineKeyboard:
    """Empty inline keyboard for testing."""
    return InlineKeyboard()


@pytest.fixture
def reply_keyboard() -> ReplyKeyboard:
    """Empty reply keyboard for testing."""
    return ReplyKeyboard()


@pytest.fixture
def populated_inline_keyboard(
    sample_inline_buttons: List[InlineButton],
) -> InlineKeyboard:
    """Inline keyboard with sample buttons."""
    keyboard = InlineKeyboard()
    keyboard.add(*sample_inline_buttons)
    return keyboard


@pytest.fixture
def populated_reply_keyboard(
    sample_reply_buttons: List[ReplyButton],
) -> ReplyKeyboard:
    """Reply keyboard with sample buttons."""
    keyboard = ReplyKeyboard()
    keyboard.add(*sample_reply_buttons)
    return keyboard
