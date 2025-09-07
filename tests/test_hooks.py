"""Tests for validation hooks and keyboard hook manager functionality."""

import pytest

from pykeyboard import (ButtonValidator, InlineButton, InlineKeyboard,
                        KeyboardHookManager, ReplyButton, ReplyKeyboard,
                        add_keyboard_hook, add_validation_rule, validate_button,
                        validate_keyboard)


class TestButtonValidator:
    """Test cases for ButtonValidator class."""

    def test_button_validator_initialization(self):
        """Test button validator initializes with default rules."""
        validator = ButtonValidator()

        assert len(validator._rules) > 0  # Should have default rules
        assert "text_not_empty" in validator._rules
        assert "text_length" in validator._rules
        assert "callback_data_format" in validator._rules

    def test_add_custom_rule(self):
        """Test adding custom validation rules."""
        validator = ButtonValidator()

        def custom_rule(button, context=None):
            return button.text.startswith("Test")

        validator.add_rule(
            "starts_with_test",
            custom_rule,
            "Must start with 'Test'",
            "Prefix with 'Test'",
        )

        assert "starts_with_test" in validator._rules
        assert (
            validator._error_messages["starts_with_test"]
            == "Must start with 'Test'"
        )
        assert (
            validator._suggestions["starts_with_test"] == "Prefix with 'Test'"
        )

    def test_validate_button_success(self):
        """Test successful button validation."""
        validator = ButtonValidator()
        button = InlineButton(text="Valid Button", callback_data="valid")

        result = validator.validate_button(button)

        assert result["is_valid"] is True
        assert len(result["errors"]) == 0
        assert result["checked_rules"] > 0

    def test_validate_button_failure(self):
        """Test button validation failure."""
        validator = ButtonValidator()
        # Pydantic validation now happens at creation time, so we need a valid button
        # that fails custom validation rules
        button = InlineButton(
            text="a" * 100, callback_data="invalid"
        )  # Too long text

        result = validator.validate_button(button)

        assert result["is_valid"] is False
        assert len(result["errors"]) > 0
        assert "Button text is too long" in result["errors"][0]

    def test_validate_button_with_context(self):
        """Test button validation with context."""
        validator = ButtonValidator()

        def context_aware_rule(button, context=None):
            if context and context.get("max_length"):
                return len(button.text) <= context["max_length"]
            return True

        validator.add_rule("context_max_length", context_aware_rule)

        button = InlineButton(
            text="Very Long Button Text", callback_data="test"
        )
        context = {"max_length": 10}

        result = validator.validate_button(button, context)

        assert result["is_valid"] is False
        assert any("context_max_length" in error for error in result["errors"])

    def test_skip_rules(self):
        """Test skipping specific validation rules."""
        validator = ButtonValidator()
        button = InlineButton(
            text="a" * 100, callback_data="test"
        )  # Would fail text_length

        # Skip the text_length rule
        result = validator.validate_button(button, skip_rules=["text_length"])

        assert (
            result["is_valid"] is True
        )  # Should pass when skipping the failing rule

    def test_validate_keyboard(self):
        """Test keyboard validation."""
        validator = ButtonValidator()

        keyboard = InlineKeyboard()
        keyboard.add(
            InlineButton(text="Valid", callback_data="valid"),
            InlineButton(
                text="a" * 100, callback_data="invalid"
            ),  # Invalid: too long
        )

        result = validator.validate_keyboard(keyboard)

        assert result["is_valid"] is False
        assert result["total_buttons"] == 2
        assert result["valid_buttons"] == 1
        assert result["invalid_buttons"] == 1
        assert len(result["button_results"]) == 2

    def test_validate_empty_keyboard(self):
        """Test validation of empty keyboard."""
        validator = ButtonValidator()
        keyboard = InlineKeyboard()

        result = validator.validate_keyboard(keyboard)

        # Empty keyboards may be considered valid depending on use case
        # The test should check the actual behavior
        assert result["total_buttons"] == 0
        assert "total_buttons" in result

    def test_remove_rule(self):
        """Test removing validation rules."""
        validator = ButtonValidator()

        # Add a rule
        validator.add_rule("test_rule", lambda btn, ctx: True)

        # Remove it
        removed = validator.remove_rule("test_rule")
        assert removed is True
        assert "test_rule" not in validator._rules

        # Try to remove non-existent rule
        removed = validator.remove_rule("non_existent")
        assert removed is False

    def test_context_validator(self):
        """Test context validator functionality."""
        validator = ButtonValidator()

        def max_buttons_check(context):
            return context.get("total_buttons", 0) <= 2

        validator.add_context_validator(max_buttons_check)

        keyboard = InlineKeyboard()
        keyboard.add("Btn1", "Btn2", "Btn3")  # 3 buttons, exceeds limit

        result = validator.validate_keyboard(keyboard)

        assert result["is_valid"] is False
        assert "Context validation failed" in result["context_errors"]


class TestKeyboardHookManager:
    """Test cases for KeyboardHookManager class."""

    def test_hook_manager_initialization(self):
        """Test hook manager initializes correctly."""
        manager = KeyboardHookManager()

        assert manager._pre_hooks == []
        assert manager._post_hooks == []
        assert manager._button_hooks == []
        assert manager._error_hooks == []

    def test_add_pre_hook(self):
        """Test adding pre-construction hooks."""
        manager = KeyboardHookManager()

        def pre_hook(keyboard):
            keyboard.row_width = 5

        manager.add_pre_hook(pre_hook)

        assert len(manager._pre_hooks) == 1

    def test_add_post_hook(self):
        """Test adding post-construction hooks."""
        manager = KeyboardHookManager()

        def post_hook(keyboard):
            keyboard.add("Added by hook")

        manager.add_post_hook(post_hook)

        assert len(manager._post_hooks) == 1

    def test_add_button_hook(self):
        """Test adding button transformation hooks."""
        manager = KeyboardHookManager()

        def button_hook(button):
            button.text = f"Modified: {button.text}"
            return button

        manager.add_button_hook(button_hook)

        assert len(manager._button_hooks) == 1

    def test_add_error_hook(self):
        """Test adding error handling hooks."""
        manager = KeyboardHookManager()

        def error_hook(error, keyboard):
            print(f"Error: {error}")

        manager.add_error_hook(error_hook)

        assert len(manager._error_hooks) == 1

    def test_process_button(self):
        """Test button processing through hooks."""
        manager = KeyboardHookManager()

        def uppercase_hook(button):
            button.text = button.text.upper()
            return button

        def add_prefix_hook(button):
            button.text = f"[{button.text}]"
            return button

        manager.add_button_hook(uppercase_hook)
        manager.add_button_hook(add_prefix_hook)

        button = InlineButton(text="test", callback_data="test")
        processed = manager.process_button(button)

        assert processed.text == "[TEST]"

    def test_execute_pre_hooks(self):
        """Test executing pre-construction hooks."""
        manager = KeyboardHookManager()
        keyboard = InlineKeyboard()

        call_count = 0

        def counting_hook(kb):
            nonlocal call_count
            call_count += 1
            kb.row_width = 10

        manager.add_pre_hook(counting_hook)
        manager.execute_pre_hooks(keyboard)

        assert call_count == 1
        assert keyboard.row_width == 10

    def test_execute_post_hooks(self):
        """Test executing post-construction hooks."""
        manager = KeyboardHookManager()
        keyboard = InlineKeyboard()

        call_count = 0

        def counting_hook(kb):
            nonlocal call_count
            call_count += 1

        manager.add_post_hook(counting_hook)
        manager.execute_post_hooks(keyboard)

        assert call_count == 1

    def test_error_hook_execution(self):
        """Test error hook execution when hooks fail."""
        manager = KeyboardHookManager()

        def failing_hook(button):
            raise ValueError("Hook failed")

        def error_handler(error, keyboard):
            assert isinstance(error, ValueError)
            assert str(error) == "Hook failed"

        manager.add_button_hook(failing_hook)
        manager.add_error_hook(error_handler)

        button = InlineButton(text="test", callback_data="test")
        # This should not raise an exception due to error handling
        result = manager.process_button(button)
        assert result is button


class TestConvenienceFunctions:
    """Test cases for convenience functions."""

    def test_validate_button_function(self):
        """Test the validate_button convenience function."""
        button = InlineButton(text="Valid", callback_data="valid")
        assert validate_button(button) is True

        invalid_button = InlineButton(
            text="a" * 100, callback_data="invalid"
        )  # Too long
        assert validate_button(invalid_button) is False

    def test_validate_keyboard_function(self):
        """Test the validate_keyboard convenience function."""
        keyboard = InlineKeyboard()
        keyboard.add("Valid Button")

        result = validate_keyboard(keyboard)
        assert result["is_valid"] is True
        assert result["total_buttons"] == 1

    def test_add_validation_rule_function(self):
        """Test the add_validation_rule convenience function."""

        def custom_rule(button, context=None):
            return "custom" in button.text.lower()

        add_validation_rule("has_custom", custom_rule, "Must contain 'custom'")

        # Test with default validator
        from pykeyboard.hooks import default_validator

        assert "has_custom" in default_validator._rules

    def test_add_keyboard_hook_function(self):
        """Test the add_keyboard_hook convenience function."""

        def test_hook(keyboard):
            pass

        # Test different hook types
        add_keyboard_hook("pre", test_hook)
        add_keyboard_hook("post", test_hook)
        add_keyboard_hook("button", lambda btn: btn)
        add_keyboard_hook("error", lambda err, kb: None)

        from pykeyboard.hooks import default_hook_manager

        assert len(default_hook_manager._pre_hooks) > 0
        assert len(default_hook_manager._post_hooks) > 0
        assert len(default_hook_manager._button_hooks) > 0
        assert len(default_hook_manager._error_hooks) > 0

    def test_invalid_hook_type(self):
        """Test invalid hook type raises error."""
        with pytest.raises(ValueError, match="Invalid hook type"):
            add_keyboard_hook("invalid_type", lambda: None)


class TestHookIntegration:
    """Integration tests for hooks functionality."""

    def test_complete_validation_workflow(self):
        """Test complete validation workflow with multiple rules."""
        validator = ButtonValidator()

        # Add multiple custom rules
        validator.add_rule(
            "no_numbers",
            lambda btn, ctx: not any(char.isdigit() for char in btn.text),
            "Button text cannot contain numbers",
            "Remove numbers from button text",
        )

        validator.add_rule(
            "min_length",
            lambda btn, ctx: len(btn.text) >= 3,
            "Button text must be at least 3 characters",
            "Make button text longer",
        )

        # Test valid button
        valid_button = InlineButton(text="Valid Text", callback_data="valid")
        result = validator.validate_button(valid_button)
        assert result["is_valid"] is True

        # Test invalid button (multiple failures)
        invalid_button = InlineButton(
            text="1", callback_data="invalid"
        )  # Too short and has number
        result = validator.validate_button(invalid_button)
        assert result["is_valid"] is False
        assert len(result["errors"]) >= 2  # Should have multiple errors
        assert (
            len(result["suggestions"]) >= 2
        )  # Should have multiple suggestions

    def test_hook_manager_integration(self):
        """Test hook manager integration with keyboard construction."""
        manager = KeyboardHookManager()

        # Track hook execution
        execution_order = []

        def pre_hook(kb):
            execution_order.append("pre")
            kb.row_width = 4

        def button_hook(btn):
            execution_order.append("button")
            btn.text = f"Processed: {btn.text}"
            return btn

        def post_hook(kb):
            execution_order.append("post")

        manager.add_pre_hook(pre_hook)
        manager.add_button_hook(button_hook)
        manager.add_post_hook(post_hook)

        # Simulate keyboard construction
        keyboard = InlineKeyboard()
        manager.execute_pre_hooks(keyboard)

        button = InlineButton(text="Test", callback_data="test")
        processed_button = manager.process_button(button)
        keyboard.add(processed_button)

        manager.execute_post_hooks(keyboard)

        # Verify execution order
        assert execution_order == ["pre", "button", "post"]
        assert keyboard.row_width == 4
        assert processed_button.text == "Processed: Test"
