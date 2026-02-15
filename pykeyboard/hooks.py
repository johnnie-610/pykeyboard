# Copyright (c) 2025-2026 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/hooks.py

import logging
from typing import Any, Callable, Dict, List, Optional, Union

from .inline_keyboard import InlineKeyboard
from .keyboard_base import KeyboardBase
from .reply_keyboard import ReplyKeyboard

logger = logging.getLogger(__name__)




class ButtonValidator:
    """Advanced button validation system with customizable hooks.

    This class provides a comprehensive validation system for keyboard buttons,
    allowing developers to define custom validation rules, constraints, and
    business logic checks.

    Features:
        - Built-in validation rules
        - Custom validation hooks
        - Context-aware validation
        - Validation chaining
        - Error reporting and suggestions

    Example:
        >>> validator = ButtonValidator()
        >>> validator.add_rule("text_length", lambda btn: len(btn.text) <= 20)
        >>> is_valid = validator.validate_button(my_button)
    """

    def __init__(self):
        """Initialize the validator with default rules."""
        self._rules: Dict[
            str, Callable[[Any, Optional[Dict[str, Any]]], bool]
        ] = {}
        self._error_messages: Dict[str, str] = {}
        self._suggestions: Dict[str, str] = {}
        self._context_validators: List[Callable[[Dict[str, Any]], bool]] = []

        self._setup_default_rules()

    def _setup_default_rules(self):
        """Set up default validation rules."""

        self.add_rule(
            "text_not_empty",
            lambda btn, ctx: bool(btn.text and btn.text.strip()),
            "Button text cannot be empty",
            "Add meaningful text to the button",
        )

        self.add_rule(
            "text_length",
            lambda btn, ctx: len(btn.text) <= 50,
            "Button text is too long (max 50 characters)",
            "Shorten the button text or use abbreviations",
        )

        self.add_rule(
            "callback_data_format",
            lambda btn, ctx: (
                not hasattr(btn, "callback_data")
                or btn.callback_data is None
                or (
                    isinstance(btn.callback_data, str)
                    and len(btn.callback_data) <= 64
                )
            ),
            "Callback data is too long (max 64 characters)",
            "Use shorter callback data or implement a mapping system",
        )

        self.add_rule(
            "url_format",
            lambda btn, ctx: (
                not hasattr(btn, "url")
                or btn.url is None
                or (
                    isinstance(btn.url, str)
                    and btn.url.startswith(("http://", "https://", "tg://"))
                )
            ),
            "URL must start with http://, https://, or tg://",
            "Use a valid URL format",
        )

    def add_rule(
        self,
        name: str,
        validator: Callable[[Any, Optional[Dict[str, Any]]], bool],
        error_message: str = "",
        suggestion: str = "",
    ) -> "ButtonValidator":
        r"""Add a custom validation rule.

        Args:
            name: Unique name for the rule
            validator: Function that takes (button, context) and returns bool
            error_message: Error message when validation fails
            suggestion: Suggestion for fixing the issue

        Returns:
            Self for method chaining

        Example:
            >>> validator.add_rule(
            ...     "no_special_chars",
            ...     lambda btn, ctx: not re.search(r'[^\w\s]', btn.text),
            ...     "Button text contains special characters",
            ...     "Remove special characters from button text"
            ... )
        """
        self._rules[name] = validator
        if error_message:
            self._error_messages[name] = error_message
        if suggestion:
            self._suggestions[name] = suggestion
        return self

    def remove_rule(self, name: str) -> bool:
        """Remove a validation rule.

        Args:
            name: Name of the rule to remove

        Returns:
            True if rule was removed, False if not found
        """
        if name in self._rules:
            del self._rules[name]
            self._error_messages.pop(name, None)
            self._suggestions.pop(name, None)
            return True
        return False

    def add_context_validator(
        self, validator: Callable[[Dict[str, Any]], bool]
    ) -> "ButtonValidator":
        """Add a context validator that runs on the entire keyboard context.

        Args:
            validator: Function that validates the entire context

        Returns:
            Self for method chaining

        Example:
            >>> def max_buttons_check(context):
            ...     return context.get('total_buttons', 0) <= 10
            >>> validator.add_context_validator(max_buttons_check)
        """
        self._context_validators.append(validator)
        return self

    def validate_button(
        self,
        button: Any,
        context: Optional[Dict[str, Any]] = None,
        skip_rules: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Validate a single button against all rules.

        Args:
            button: The button to validate
            context: Optional context information
            skip_rules: List of rule names to skip

        Returns:
            Dict with validation results

        Example:
            >>> result = validator.validate_button(my_button)
            >>> if not result['is_valid']:
            ...     print(f"Errors: {result['errors']}")
        """
        skip_rules = skip_rules or []
        errors = []
        warnings = []
        suggestions = []

        for rule_name, validator_func in self._rules.items():
            if rule_name in skip_rules:
                continue

            try:
                if not validator_func(button, context):
                    error_msg = self._error_messages.get(
                        rule_name, f"Failed rule: {rule_name}"
                    )
                    errors.append(error_msg)

                    suggestion = self._suggestions.get(rule_name)
                    if suggestion:
                        suggestions.append(suggestion)
            except Exception as e:
                warnings.append(f"Rule '{rule_name}' raised exception: {e}")

        return {
            "is_valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "suggestions": suggestions,
            "checked_rules": len(self._rules) - len(skip_rules),
        }

    def validate_keyboard(
        self,
        keyboard: Union[InlineKeyboard, ReplyKeyboard],
        context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Validate an entire keyboard.

        Args:
            keyboard: The keyboard to validate
            context: Optional context information

        Returns:
            Dict with comprehensive validation results

        Example:
            >>> result = validator.validate_keyboard(my_keyboard)
            >>> print(f"Valid buttons: {result['valid_buttons']}/{result['total_buttons']}")
        """
        ctx = {
            **(context or {}),
            "keyboard_type": type(keyboard).__name__,
            "total_rows": len(keyboard.keyboard),
            "total_buttons": sum(len(row) for row in keyboard.keyboard),
        }

        context_errors = []
        for ctx_validator in self._context_validators:
            try:
                if not ctx_validator(ctx):
                    context_errors.append("Context validation failed")
            except Exception as e:
                context_errors.append(f"Context validator error: {e}")

        button_results = []
        valid_buttons = 0
        total_buttons = 0

        for row_idx, row in enumerate(keyboard.keyboard):
            for btn_idx, button in enumerate(row):
                total_buttons += 1
                result = self.validate_button(
                    button, {**ctx, "row": row_idx, "col": btn_idx}
                )
                button_results.append(
                    {
                        "row": row_idx,
                        "col": btn_idx,
                        "button": button,
                        "result": result,
                    }
                )
                if result["is_valid"]:
                    valid_buttons += 1

        all_errors = []
        all_warnings = []
        all_suggestions = []

        for result in button_results:
            all_errors.extend(result["result"]["errors"])
            all_warnings.extend(result["result"]["warnings"])
            all_suggestions.extend(result["result"]["suggestions"])

        all_errors.extend(context_errors)

        return {
            "is_valid": len(all_errors) == 0 and valid_buttons == total_buttons,
            "total_buttons": total_buttons,
            "valid_buttons": valid_buttons,
            "invalid_buttons": total_buttons - valid_buttons,
            "errors": all_errors,
            "warnings": all_warnings,
            "suggestions": all_suggestions,
            "button_results": button_results,
            "context_errors": context_errors,
        }


class KeyboardHookManager:
    """Manager for keyboard construction hooks and middleware.

    This class provides a way to add middleware and hooks to the keyboard
    construction process, allowing for custom processing, validation, and
    transformation of keyboards during creation.

    Features:
        - Pre-construction hooks
        - Post-construction hooks
        - Button transformation hooks
        - Validation middleware
        - Error handling hooks

    Example:
        >>> manager = KeyboardHookManager()
        >>> manager.add_pre_hook(lambda kb: print(f"Building {type(kb).__name__}"))
        >>> manager.add_post_hook(lambda kb: validate_keyboard(kb))
    """

    def __init__(self):
        """Initialize the hook manager."""
        self._pre_hooks: List[Callable[[KeyboardBase], None]] = []
        self._post_hooks: List[Callable[[KeyboardBase], None]] = []
        self._button_hooks: List[Callable[[Any], Any]] = []
        self._error_hooks: List[Callable[[Exception, KeyboardBase], None]] = []

    def add_pre_hook(
        self, hook: Callable[[KeyboardBase], None]
    ) -> "KeyboardHookManager":
        """Add a hook that runs before keyboard construction.

        Args:
            hook: Function that takes the keyboard and performs preprocessing

        Returns:
            Self for method chaining
        """
        self._pre_hooks.append(hook)
        return self

    def add_post_hook(
        self, hook: Callable[[KeyboardBase], None]
    ) -> "KeyboardHookManager":
        """Add a hook that runs after keyboard construction.

        Args:
            hook: Function that takes the keyboard and performs postprocessing

        Returns:
            Self for method chaining
        """
        self._post_hooks.append(hook)
        return self

    def add_button_hook(
        self, hook: Callable[[Any], Any]
    ) -> "KeyboardHookManager":
        """Add a hook that transforms buttons during construction.

        Args:
            hook: Function that takes a button and returns transformed button

        Returns:
            Self for method chaining
        """
        self._button_hooks.append(hook)
        return self

    def add_error_hook(
        self, hook: Callable[[Exception, KeyboardBase], None]
    ) -> "KeyboardHookManager":
        """Add a hook that handles errors during construction.

        Args:
            hook: Function that takes (exception, keyboard) and handles the error

        Returns:
            Self for method chaining
        """
        self._error_hooks.append(hook)
        return self

    def process_button(self, button: Any) -> Any:
        """Process a button through all button hooks.

        Args:
            button: The button to process

        Returns:
            The processed button
        """
        for hook in self._button_hooks:
            try:
                button = hook(button)
            except Exception as e:
                for error_hook in self._error_hooks:
                    try:
                        error_hook(e, None)
                    except Exception:
                        logger.warning("Error hook failed while handling button hook error", exc_info=True)
        return button

    def execute_pre_hooks(self, keyboard: KeyboardBase) -> None:
        """Execute all pre-construction hooks.

        Args:
            keyboard: The keyboard being constructed
        """
        for hook in self._pre_hooks:
            try:
                hook(keyboard)
            except Exception as e:
                for error_hook in self._error_hooks:
                    try:
                        error_hook(e, keyboard)
                    except Exception:
                        logger.warning("Error hook failed while handling pre-hook error", exc_info=True)

    def execute_post_hooks(self, keyboard: KeyboardBase) -> None:
        """Execute all post-construction hooks.

        Args:
            keyboard: The constructed keyboard
        """
        for hook in self._post_hooks:
            try:
                hook(keyboard)
            except Exception as e:
                for error_hook in self._error_hooks:
                    try:
                        error_hook(e, keyboard)
                    except Exception:
                        logger.warning("Error hook failed while handling post-hook error", exc_info=True)


default_validator = ButtonValidator()
default_hook_manager = KeyboardHookManager()


def validate_button(
    button: Any, context: Optional[Dict[str, Any]] = None
) -> bool:
    """Convenience function to validate a button with default validator.

    Args:
        button: The button to validate
        context: Optional context information

    Returns:
        True if valid, False otherwise
    """
    result = default_validator.validate_button(button, context)
    return result["is_valid"]


def validate_keyboard(
    keyboard: Union[InlineKeyboard, ReplyKeyboard],
) -> Dict[str, Any]:
    """Convenience function to validate a keyboard with default validator.

    Args:
        keyboard: The keyboard to validate

    Returns:
        Dict with validation results
    """
    return default_validator.validate_keyboard(keyboard)


def add_validation_rule(
    name: str,
    validator: Callable[[Any, Optional[Dict[str, Any]]], bool],
    error_message: str = "",
    suggestion: str = "",
) -> None:
    """Convenience function to add a validation rule to the default validator.

    Args:
        name: Rule name
        validator: Validation function
        error_message: Error message for failures
        suggestion: Suggestion for fixing issues
    """
    default_validator.add_rule(name, validator, error_message, suggestion)


def add_keyboard_hook(hook_type: str, hook: Callable) -> None:
    """Convenience function to add hooks to the default hook manager.

    Args:
        hook_type: Type of hook ('pre', 'post', 'button', 'error')
        hook: The hook function

    Raises:
        ValueError: If hook_type is invalid
    """
    if hook_type == "pre":
        default_hook_manager.add_pre_hook(hook)
    elif hook_type == "post":
        default_hook_manager.add_post_hook(hook)
    elif hook_type == "button":
        default_hook_manager.add_button_hook(hook)
    elif hook_type == "error":
        default_hook_manager.add_error_hook(hook)
    else:
        raise ValueError(
            f"Invalid hook type: {hook_type}. Use 'pre', 'post', 'button', or 'error'"
        )
