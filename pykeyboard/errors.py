# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/erros.py


import hashlib
import inspect
import json
import traceback
from typing import Any, Dict, Optional, Union

from loguru import logger


def capture_traceback_info(skip_frames: int = 0) -> Dict[str, Any]:
    """Capture detailed traceback information for error reporting.

    Args:
        skip_frames: Number of frames to skip from the top of the traceback.

    Returns:
        Dictionary containing traceback information including file, line, function, and code context.
    """
    try:
        frame = inspect.currentframe()
        if frame is None:
            return {}

        for _ in range(skip_frames + 1):
            frame = frame.f_back
            if frame is None:
                return {}

        filename = frame.f_code.co_filename
        line_number = frame.f_lineno
        function_name = frame.f_code.co_name

        try:
            import linecache

            line_content = linecache.getline(filename, line_number).strip()
        except:
            line_content = "Could not retrieve source line"

        return {
            "file": filename,
            "line": line_number,
            "function": function_name,
            "code": line_content,
            "traceback": traceback.format_exc(),
        }
    except Exception:
        return {}


class PyKeyboardError(Exception):
    """Base exception class for PyKeyboard library errors.

    This class provides comprehensive error reporting with automatic logging,
    detailed context information, and developer-friendly help messages.

    Attributes:
        message: The error message describing what went wrong.
        error_code: A unique code identifying the error type.
        context: Additional context information about the error.
        traceback_info: Detailed traceback information captured at error creation.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "PYKEYBOARD_ERROR",
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[Dict[str, Any]] = None,
    ):
        """Initialize PyKeyboardError with comprehensive error information.

        Args:
            message: Descriptive error message.
            error_code: Unique error code for categorization.
            context: Additional context information.
            traceback_info: Pre-captured traceback information.
        """
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        self.traceback_info = traceback_info or capture_traceback_info(
            skip_frames=1
        )

        self._log_error()

        super().__init__(f"[{self.error_code}] {self.message}")

    def _log_error(self) -> None:
        """Log the error to the terminal with full context."""
        logger.error(f"PyKeyboard Error [{self.error_code}]: {self.message}")

        if self.context:
            logger.error(f"Context: {self.context}")

        if self.traceback_info:
            location = self.traceback_info.get("function", "unknown")
            file_info = f"{self.traceback_info.get('file', 'unknown')}:{self.traceback_info.get('line', 0)}"
            logger.error(f"Location: {file_info} in {location}()")

    def get_help_message(self) -> str:
        """Generate a comprehensive help message for developers.

        Returns:
            Formatted help message with explanation, solution, and example.
        """
        help_parts = [
            f"🚨 PyKeyboard Error: {self.error_code}",
            "",
            f"❓ What happened: {self.message}",
            "",
            "🔧 How to fix: Override this method in subclasses to provide specific guidance.",
            "",
            "📝 Example:",
            "```python",
            "try:",
            "    # Your code that might raise this error",
            "    pass",
            "except PyKeyboardError as e:",
            "    print(e.get_help_message())",
            "```",
        ]

        if self.traceback_info:
            help_parts.extend(
                [
                    "",
                    f"📍 Location: {self.traceback_info.get('file', 'unknown')}:{self.traceback_info.get('line', 0)}",
                    f"Function: {self.traceback_info.get('function', 'unknown')}",
                ]
            )

        return "\n".join(help_parts)

    def get_full_report(self) -> str:
        """Generate a complete error report for debugging.

        Returns:
            Comprehensive error report including all available information.
        """
        report_parts = [
            "=" * 60,
            f"PYKEYBOARD ERROR REPORT - {self.error_code}",
            "=" * 60,
            "",
            f"Message: {self.message}",
            "",
            f"Error Code: {self.error_code}",
        ]

        if self.context:
            report_parts.extend(["", "Context Information:", "-" * 20])
            for key, value in self.context.items():
                report_parts.append(f"{key}: {value}")

        if self.traceback_info:
            report_parts.extend(
                [
                    "",
                    "Traceback Information:",
                    "-" * 20,
                    f"File: {self.traceback_info.get('file', 'unknown')}",
                    f"Line: {self.traceback_info.get('line', 0)}",
                    f"Function: {self.traceback_info.get('function', 'unknown')}",
                    f"Code: {self.traceback_info.get('code', 'N/A')}",
                    "",
                    "Full Traceback:",
                    "-" * 15,
                    self.traceback_info.get(
                        "traceback", "No traceback available"
                    ),
                ]
            )

        report_parts.extend(
            [
                "",
                "Help & Solutions:",
                "-" * 15,
                self.get_help_message(),
                "",
                "=" * 60,
            ]
        )

        return "\n".join(report_parts)


class ValidationError(PyKeyboardError):
    """Error raised when input validation fails.

    This error occurs when user-provided data doesn't meet the required
    validation criteria for PyKeyboard components.
    """

    def __init__(
        self,
        field_name: str,
        invalid_value: Optional[Any] = None,
        expected_type: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[Dict[str, Any]] = None,
    ):
        """Initialize ValidationError with field-specific information.

        Args:
            field_name: Name of the field that failed validation.
            invalid_value: The invalid value that was provided.
            expected_type: Description of the expected type/format.
            context: Additional context information.
            traceback_info: Pre-captured traceback information.
        """
        self.field_name = field_name
        self.invalid_value = invalid_value
        self.expected_type = expected_type

        message = f"Validation failed for field '{field_name}': expected {expected_type}, got {type(invalid_value).__name__}"

        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            context=context
            or {
                "field": field_name,
                "value": str(invalid_value),
                "expected": expected_type,
            },
            traceback_info=traceback_info,
        )

    def get_help_message(self) -> str:
        """Generate validation-specific help message."""
        help_parts = [
            f"🚨 Validation Error: {self.error_code}",
            "",
            f"❓ What happened: The field '{self.field_name}' received an invalid value.",
            f"   - Provided: {self.invalid_value} (type: {type(self.invalid_value).__name__})",
            f"   - Expected: {self.expected_type}",
            "",
            "🔧 How to fix:",
            f"   1. Check the value you're passing to '{self.field_name}'",
            f"   2. Ensure it matches the expected {self.expected_type} format",
            "   3. Refer to the PyKeyboard documentation for valid formats",
            "",
            "📝 Example:",
            "```python",
            "# ❌ Wrong",
            f"keyboard.{self.field_name} = {repr(self.invalid_value)}",
            "",
            "# ✅ Correct",
            f"keyboard.{self.field_name} = # Provide a valid {self.expected_type}",
            "```",
        ]

        if self.traceback_info:
            help_parts.extend(
                [
                    "",
                    f"📍 Error occurred in: {self.traceback_info.get('function', 'unknown')}()",
                    f"   at {self.traceback_info.get('file', 'unknown')}:{self.traceback_info.get('line', 0)}",
                ]
            )

        return "\n".join(help_parts)


class PaginationError(PyKeyboardError):
    """Error raised when pagination parameters are invalid.

    This error occurs when pagination setup fails due to invalid page counts,
    current page values, or callback patterns.
    """

    def __init__(
        self,
        parameter_name: str,
        invalid_value: Any,
        reason: str,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[Dict[str, Any]] = None,
    ):
        """Initialize PaginationError with parameter-specific information.

        Args:
            parameter_name: Name of the invalid parameter (count_pages, current_page, etc.).
            invalid_value: The invalid value that was provided.
            reason: Detailed explanation of why the value is invalid.
            context: Additional context information.
            traceback_info: Pre-captured traceback information.
        """
        self.parameter_name = parameter_name
        self.invalid_value = invalid_value
        self.reason = reason

        message = (
            f"Pagination parameter '{parameter_name}' is invalid: {reason}"
        )

        super().__init__(
            message=message,
            error_code="PAGINATION_ERROR",
            context=context
            or {
                "parameter": parameter_name,
                "value": str(invalid_value),
                "reason": reason,
            },
            traceback_info=traceback_info,
        )

    def get_help_message(self) -> str:
        """Generate pagination-specific help message."""
        help_parts = [
            f"🚨 Pagination Error: {self.error_code}",
            "",
            f"❓ What happened: Invalid pagination parameter '{self.parameter_name}'.",
            f"   - Provided: {self.invalid_value}",
            f"   - Issue: {self.reason}",
            "",
            "🔧 How to fix:",
        ]

        # Specific guidance based on parameter
        if self.parameter_name == "count_pages":
            help_parts.extend(
                [
                    "   1. count_pages must be >= 1",
                    "   2. For single-page content, consider not using pagination",
                    "   3. Maximum supported is 10000 pages",
                ]
            )
        elif self.parameter_name == "current_page":
            help_parts.extend(
                [
                    "   1. current_page must be >= 1",
                    "   2. current_page cannot exceed count_pages",
                    "   3. Use 1-based indexing (first page is 1, not 0)",
                ]
            )
        elif self.parameter_name == "callback_pattern":
            help_parts.extend(
                [
                    "   1. callback_pattern must contain '{number}' placeholder",
                    "   2. The placeholder will be replaced with page numbers",
                    "   3. Example: 'page_{number}' becomes 'page_1', 'page_2', etc.",
                ]
            )

        help_parts.extend(
            [
                "",
                "📝 Example:",
                "```python",
                "# ❌ Wrong",
                f"keyboard.paginate({self.invalid_value if self.parameter_name == 'count_pages' else '5'}, {self.invalid_value if self.parameter_name == 'current_page' else '1'}, '{self.invalid_value if self.parameter_name == 'callback_pattern' else 'invalid_pattern'}')",
                "",
                "# ✅ Correct",
                "keyboard.paginate(5, 1, 'page_{number}')  # 5 pages, start at page 1",
                "```",
            ]
        )

        if self.traceback_info:
            help_parts.extend(
                [
                    "",
                    f"📍 Error occurred in: {self.traceback_info.get('function', 'unknown')}()",
                    f"   at {self.traceback_info.get('file', 'unknown')}:{self.traceback_info.get('line', 0)}",
                ]
            )

        return "\n".join(help_parts)


class PaginationUnchangedError(PaginationError):
    """Error raised when pagination keyboard hasn't changed from previous call.

    This error occurs when the automatic duplicate prevention system detects
    that the same pagination keyboard is being created again, preventing
    unnecessary MessageNotModifiedError from Telegram.
    """

    def __init__(
        self,
        source: str,
        keyboard_hash: str,
        previous_hash: str,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[Dict[str, Any]] = None,
    ):
        """Initialize PaginationUnchangedError with duplicate detection information.

        Args:
            source: The source identifier used for isolation (from contextvar or parameter).
            keyboard_hash: The SHA256 hash of the current keyboard state.
            previous_hash: The SHA256 hash of the previous keyboard state.
            context: Additional context information.
            traceback_info: Pre-captured traceback information.
        """
        self.source = source
        self.keyboard_hash = keyboard_hash
        self.previous_hash = previous_hash

        message = f"Pagination keyboard unchanged for source '{source}': duplicate detected"

        super().__init__(
            parameter_name="keyboard_state",
            invalid_value=keyboard_hash,
            reason=f"Keyboard hash matches previous hash ({previous_hash[:16]}...) for source '{source}'",
            context=context
            or {
                "source": source,
                "current_hash": keyboard_hash,
                "previous_hash": previous_hash,
                "hash_match": keyboard_hash == previous_hash,
            },
            traceback_info=traceback_info,
        )

    @staticmethod
    def get_keyboard_hash(keyboard_data: Union[Dict[str, Any], str]) -> str:
        """Generate SHA256 hash for keyboard state.

        Args:
            keyboard_data: Dictionary or string representation of keyboard state.

        Returns:
            SHA256 hash string of the keyboard data.
        """
        if isinstance(keyboard_data, dict):
            # Sort keys for consistent hashing
            json_str = json.dumps(
                keyboard_data, sort_keys=True, separators=(",", ":")
            )
        else:
            # Use string directly for better performance
            json_str = str(keyboard_data)

        return hashlib.sha256(json_str.encode("utf-8")).hexdigest()

    def get_help_message(self) -> str:
        """Generate duplicate prevention specific help message."""
        help_parts = [
            f"🚨 Pagination Unchanged Error: {self.error_code}",
            "",
            f"❓ What happened: The pagination keyboard for source '{self.source}' hasn't changed.",
            f"   - This prevents Telegram's MessageNotModifiedError",
            f"   - Source: {self.source}",
            f"   - Hash: {self.keyboard_hash[:16]}...",
            "",
            "🔧 How to fix:",
            "   1. Through answering callback query, encourage your users to navigate to a different page",
            "   2. This error is usually handled automatically - no action needed",
            "   3. If you need to force keyboard update, change pagination parameters",
            "   4. Use different source parameter for different clients",
            "   5. Check if contextvar is set correctly for multi-client scenarios",
            "",
            "📝 Example:",
            "```python",
            "# Automatic handling (recommended)",
            "try:",
            "    keyboard.paginate(5, 1, 'page:{number}')",
            "except PaginationUnchangedError:",
            "    # Skip message edit - keyboard hasn't changed",
            "    pass",
            "",
            "# Force update with different parameters",
            "keyboard.paginate(5, 2, 'page:{number}')  # Different page",
            "",
            "# Multi-client with explicit source",
            "keyboard.paginate(5, 1, 'page:{number}', source='client_123')",
            "```",
        ]

        if self.traceback_info:
            help_parts.extend(
                [
                    "",
                    f"📍 Error occurred in: {self.traceback_info.get('function', 'unknown')}()",
                    f"   at {self.traceback_info.get('file', 'unknown')}:{self.traceback_info.get('line', 0)}",
                ]
            )

        return "\n".join(help_parts)


class LocaleError(PyKeyboardError):
    """Error raised when locale/language parameters are invalid.

    This error occurs when language selection fails due to invalid locale codes,
    unsupported languages, or malformed callback patterns.
    """

    def __init__(
        self,
        parameter_name: str,
        invalid_value: Optional[Any] = None,
        reason: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[Dict[str, Any]] = None,
    ):
        """Initialize LocaleError with locale-specific information.

        Args:
            parameter_name: Name of the invalid parameter (locales, callback_pattern, etc.).
            invalid_value: The invalid value that was provided.
            reason: Detailed explanation of why the value is invalid.
            context: Additional context information.
            traceback_info: Pre-captured traceback information.
        """
        self.parameter_name = parameter_name
        self.invalid_value = invalid_value
        self.reason = reason

        message = f"Locale parameter '{parameter_name}' is invalid: {reason}"

        super().__init__(
            message=message,
            error_code="LOCALE_ERROR",
            context=context
            or {
                "parameter": parameter_name,
                "value": str(invalid_value),
                "reason": reason,
            },
            traceback_info=traceback_info,
        )

    def get_help_message(self) -> str:
        """Generate locale-specific help message."""
        help_parts = [
            f"🚨 Locale Error: {self.error_code}",
            "",
            f"❓ What happened: Invalid locale parameter '{self.parameter_name}'.",
            f"   - Provided: {self.invalid_value}",
            f"   - Issue: {self.reason}",
            "",
            "🔧 How to fix:",
        ]

        # Specific guidance based on parameter
        if self.parameter_name == "callback_pattern":
            help_parts.extend(
                [
                    "   1. callback_pattern must contain '{locale}' placeholder",
                    "   2. The placeholder will be replaced with locale codes",
                    "   3. Example: 'lang_{locale}' becomes 'lang_en_US', 'lang_fr_FR', etc.",
                ]
            )
        elif self.parameter_name == "locales":
            help_parts.extend(
                [
                    "   1. locales must be a non-empty list or string",
                    "   2. Each locale code must be supported by PyKeyboard",
                    "   3. Use get_all_locales() to see available options",
                    "   4. Common formats: 'en_US', 'fr_FR', 'de_DE', 'es_ES'",
                ]
            )
        elif self.parameter_name == "row_width":
            help_parts.extend(
                [
                    "   1. row_width must be >= 1",
                    "   2. Controls how many language buttons appear per row",
                    "   3. Recommended: 2-3 for mobile, 3-5 for desktop",
                ]
            )

        help_parts.extend(
            [
                "",
                "📝 Example:",
                "```python",
                "# ❌ Wrong",
                f"keyboard.languages('{self.invalid_value if self.parameter_name == 'callback_pattern' else 'lang_{locale}'}', {repr(self.invalid_value) if self.parameter_name == 'locales' else ['en_US', 'fr_FR']})",
                "",
                "# ✅ Correct",
                "keyboard.languages('lang_{locale}', ['en_US', 'fr_FR', 'de_DE'])",
                "",
                "# Get available locales:",
                "locales = keyboard.get_all_locales()",
                "print(list(locales.keys())[:5])  # First 5 available locales",
                "```",
            ]
        )

        if self.traceback_info:
            help_parts.extend(
                [
                    "",
                    f"📍 Error occurred in: {self.traceback_info.get('function', 'unknown')}()",
                    f"   at {self.traceback_info.get('file', 'unknown')}:{self.traceback_info.get('line', 0)}",
                ]
            )

        return "\n".join(help_parts)


class ConfigurationError(PyKeyboardError):
    """Error raised when configuration parameters are invalid.

    This error occurs when PyKeyboard is configured incorrectly or when
    required settings are missing or malformed.
    """

    def __init__(
        self,
        setting_name: str,
        invalid_value: Any,
        reason: str,
        context: Optional[Dict[str, Any]] = None,
        traceback_info: Optional[Dict[str, Any]] = None,
    ):
        """Initialize ConfigurationError with setting-specific information.

        Args:
            setting_name: Name of the invalid configuration setting.
            invalid_value: The invalid value that was provided.
            reason: Detailed explanation of why the value is invalid.
            context: Additional context information.
            traceback_info: Pre-captured traceback information.
        """
        self.setting_name = setting_name
        self.invalid_value = invalid_value
        self.reason = reason

        message = f"Configuration setting '{setting_name}' is invalid: {reason}"

        super().__init__(
            message=message,
            error_code="CONFIG_ERROR",
            context=context
            or {
                "setting": setting_name,
                "value": str(invalid_value),
                "reason": reason,
            },
            traceback_info=traceback_info,
        )

    def get_help_message(self) -> str:
        """Generate configuration-specific help message."""
        help_parts = [
            f"🚨 Configuration Error: {self.error_code}",
            "",
            f"❓ What happened: Invalid configuration for '{self.setting_name}'.",
            f"   - Provided: {self.invalid_value}",
            f"   - Issue: {self.reason}",
            "",
            "🔧 How to fix:",
            "   1. Check your PyKeyboard configuration",
            "   2. Verify the setting name and value format",
            "   3. Refer to the configuration documentation",
            "   4. Ensure all required settings are provided",
            "",
            "📝 Example:",
            "```python",
            "# ❌ Wrong configuration",
            f"pykeyboard.{self.setting_name} = {repr(self.invalid_value)}",
            "",
            "# ✅ Correct configuration",
            f"pykeyboard.{self.setting_name} = # Provide a valid value",
            "",
            "# Check current configuration:",
            "from pykeyboard import get_keyboard_info",
            "info = get_keyboard_info(keyboard)",
            "print(info)",
            "```",
            "",
            "Common configuration issues:",
            "• row_width must be >= 1",
            "• callback_pattern must contain required placeholders",
            "• locale codes must be supported",
            "• pagination parameters must be within valid ranges",
        ]

        if self.traceback_info:
            help_parts.extend(
                [
                    "",
                    f"📍 Error occurred in: {self.traceback_info.get('function', 'unknown')}()",
                    f"   at {self.traceback_info.get('file', 'unknown')}:{self.traceback_info.get('line', 0)}",
                ]
            )

        return "\n".join(help_parts)
