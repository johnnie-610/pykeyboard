"""Tests for keyboard base functionality."""

import pytest

from pykeyboard import InlineButton, ReplyButton
from pykeyboard.keyboard_base import KeyboardBase


class TestKeyboardBase:
    """Test cases for KeyboardBase class."""

    def test_keyboard_initialization(self):
        """Test keyboard initializes with correct defaults."""
        keyboard = KeyboardBase()
        assert keyboard.row_width == 3
        assert keyboard.keyboard == []

    def test_add_buttons_single_row(self):
        """Test adding buttons that fit in a single row."""
        keyboard = KeyboardBase(row_width=3)
        buttons = [
            InlineButton(text="Btn1", callback_data="1"),
            InlineButton(text="Btn2", callback_data="2"),
            InlineButton(text="Btn3", callback_data="3"),
        ]

        keyboard.add(*buttons)

        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 3
        assert keyboard.keyboard[0] == buttons

    def test_add_buttons_multiple_rows(self):
        """Test adding buttons that span multiple rows."""
        keyboard = KeyboardBase(row_width=2)
        buttons = [
            InlineButton(text="Btn1", callback_data="1"),
            InlineButton(text="Btn2", callback_data="2"),
            InlineButton(text="Btn3", callback_data="3"),
            InlineButton(text="Btn4", callback_data="4"),
            InlineButton(text="Btn5", callback_data="5"),
        ]

        keyboard.add(*buttons)

        assert len(keyboard.keyboard) == 3
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 2
        assert len(keyboard.keyboard[2]) == 1

    def test_row_method(self):
        """Test adding buttons row by row."""
        keyboard = KeyboardBase()
        button1 = InlineButton(text="Btn1", callback_data="1")
        button2 = InlineButton(text="Btn2", callback_data="2")
        button3 = InlineButton(text="Btn3", callback_data="3")

        keyboard.row(button1)
        keyboard.row(button2, button3)

        assert len(keyboard.keyboard) == 2
        assert keyboard.keyboard[0] == [button1]
        assert keyboard.keyboard[1] == [button2, button3]

    def test_custom_row_width(self):
        """Test keyboard with custom row width."""
        keyboard = KeyboardBase(row_width=4)
        buttons = [
            InlineButton(text=f"Btn{i}", callback_data=str(i))
            for i in range(1, 6)
        ]

        keyboard.add(*buttons)

        assert len(keyboard.keyboard) == 2
        assert len(keyboard.keyboard[0]) == 4
        assert len(keyboard.keyboard[1]) == 1

    def test_empty_add(self):
        """Test adding no buttons."""
        keyboard = KeyboardBase()
        keyboard.add()
        assert keyboard.keyboard == []

    def test_empty_row(self):
        """Test adding empty row."""
        keyboard = KeyboardBase()
        keyboard.row()
        assert keyboard.keyboard == [[]]

    def test_add_method_chaining(self):
        """Test that add() method returns self for chaining."""
        keyboard = KeyboardBase(row_width=2)
        buttons = [
            InlineButton(text="Btn1", callback_data="1"),
            InlineButton(text="Btn2", callback_data="2"),
            InlineButton(text="Btn3", callback_data="3"),
        ]

        # Test chaining
        result = keyboard.add(*buttons)
        assert result is keyboard

        # Verify buttons were added correctly
        assert len(keyboard.keyboard) == 2
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 1

    def test_row_method_chaining(self):
        """Test that row() method returns self for chaining."""
        keyboard = KeyboardBase()
        button1 = InlineButton(text="Btn1", callback_data="1")
        button2 = InlineButton(text="Btn2", callback_data="2")
        button3 = InlineButton(text="Btn3", callback_data="3")

        # Test chaining
        result = keyboard.row(button1).row(button2, button3)
        assert result is keyboard

        # Verify rows were added correctly
        assert len(keyboard.keyboard) == 2
        assert keyboard.keyboard[0] == [button1]
        assert keyboard.keyboard[1] == [button2, button3]

    def test_method_chaining_combined(self):
        """Test combining add() and row() method chaining."""
        keyboard = KeyboardBase(row_width=2)
        buttons = [
            InlineButton(text="A", callback_data="a"),
            InlineButton(text="B", callback_data="b"),
        ]

        # Test combined chaining: add() replaces, row() appends
        result = (
            keyboard.add(*buttons)  # Adds A, B in rows
            .row(InlineButton(text="C", callback_data="c"))  # Adds C in new row
            .row(InlineButton(text="D", callback_data="d"))
        )  # Adds D in new row

        assert result is keyboard

        # Verify final state
        assert len(keyboard.keyboard) == 3
        assert keyboard.keyboard[0] == buttons  # A, B
        assert len(keyboard.keyboard[1]) == 1  # C
        assert len(keyboard.keyboard[2]) == 1  # D
