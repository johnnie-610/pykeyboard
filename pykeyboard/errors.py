# Copyright (c) 2025-2026 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/errors.py

"""Custom exception hierarchy for pykeyboard.

Each exception stores structured data that callers can inspect
programmatically. Formatting (logging, user-facing messages)
is the caller's responsibility.
"""

from typing import Any, Optional


class PyKeyboardError(Exception):
    """Base exception for all pykeyboard errors.

    Attributes:
        error_code: Machine-readable identifier for the error category.
    """

    error_code: str = "PYKEYBOARD_ERROR"

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(f"[{self.error_code}] {message}")


class ValidationError(PyKeyboardError):
    """Raised when input validation fails.

    Attributes:
        field: Name of the field that failed validation.
        value: The invalid value that was supplied (if available).
        expected: Description of what was expected (if available).
    """

    error_code: str = "VALIDATION_ERROR"

    def __init__(
        self,
        field: str,
        value: Any = None,
        expected: Optional[str] = None,
        *,
        reason: Optional[str] = None,
    ) -> None:
        self.field = field
        self.value = value
        self.expected = expected
        self.reason = reason

        if reason:
            msg = f"Validation failed for '{field}': {reason}"
        elif expected:
            msg = f"Validation failed for '{field}': expected {expected}, got {type(value).__name__}"
        else:
            msg = f"Validation failed for '{field}'"
        super().__init__(msg)


class PaginationError(PyKeyboardError):
    """Raised when pagination parameters are invalid.

    Attributes:
        param: Name of the invalid parameter.
        value: The invalid value that was supplied.
        reason: Explanation of why the value is invalid.
    """

    error_code: str = "PAGINATION_ERROR"

    def __init__(self, param: str, value: Any, reason: str) -> None:
        self.param = param
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid pagination param '{param}': {reason}")


class PaginationUnchangedError(PaginationError):
    """Raised when the pagination keyboard is identical to the previous call.

    Catching this error lets the caller skip the Telegram message edit
    and avoid ``MessageNotModifiedError``.

    Attributes:
        source: The source identifier used for client isolation.
    """

    def __init__(self, source: str) -> None:
        self.source = source
        super().__init__(
            "keyboard_state", source, "unchanged since last call"
        )


class LocaleError(PyKeyboardError):
    """Raised when locale / language-selection parameters are invalid.

    Attributes:
        param: Name of the invalid parameter.
        value: The invalid value that was supplied (if available).
        reason: Explanation of why the value is invalid.
    """

    error_code: str = "LOCALE_ERROR"

    def __init__(
        self,
        param: str,
        value: Any = None,
        *,
        reason: str = "",
    ) -> None:
        self.param = param
        self.value = value
        self.reason = reason
        super().__init__(f"Invalid locale param '{param}': {reason}")


class ConfigurationError(PyKeyboardError):
    """Raised when a configuration setting is invalid.

    Attributes:
        setting: Name of the invalid configuration setting.
        value: The invalid value that was supplied.
        reason: Explanation of why the value is invalid.
    """

    error_code: str = "CONFIG_ERROR"

    def __init__(self, setting: str, value: Any, reason: str) -> None:
        self.setting = setting
        self.value = value
        self.reason = reason
        super().__init__(
            f"Invalid configuration '{setting}': {reason}"
        )
