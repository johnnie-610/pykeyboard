"""Utility functions and modern Python features for PyKeyboard."""

import sys
from typing import Union, Any, Dict, List, Literal
from pathlib import Path
from .keyboard_base import InlineButton
from .inline_keyboard import InlineKeyboard
from .reply_keyboard import ReplyKeyboard, ReplyButton


# Import optional dependencies at module level for better performance
try:
    import json
except ImportError:
    json = None

try:
    import pickle
except ImportError:
    pickle = None


def get_python_version() -> tuple[int, int, int]:
    """Get the current Python version as a tuple.

    Returns:
        Tuple of (major, minor, micro) version numbers
    """
    return (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)


def supports_match_case() -> bool:
    """Check if the current Python version supports match/case statements.

    Returns:
        True if Python 3.10+ is available, False otherwise
    """
    return sys.version_info >= (3, 10)


def supports_typing_self() -> bool:
    """Check if the current Python version supports typing.Self.

    Returns:
        True if Python 3.11+ is available, False otherwise
    """
    return sys.version_info >= (3, 11)


def supports_literal_types() -> bool:
    """Check if the current Python version supports Literal types.

    Returns:
        True if Python 3.8+ is available, False otherwise
    """
    return sys.version_info >= (3, 8)


def create_keyboard_from_config(config: Dict[str, Any]) -> Union[InlineKeyboard, ReplyKeyboard]:
    """Create a keyboard from a configuration dictionary using modern Python features.

    This function demonstrates the use of match/case (Python 3.10+) and other
    modern Python features for keyboard creation.

    Args:
        config: Configuration dictionary with keyboard settings

    Returns:
        Configured keyboard instance

    Raises:
        ValueError: If configuration is invalid
    """
    keyboard_type = config.get('type', 'inline')

    if supports_match_case():
        match keyboard_type.lower():
            case 'inline':
                keyboard = InlineKeyboard()
            case 'reply':
                keyboard = ReplyKeyboard()
            case _:
                raise ValueError(f"Unsupported keyboard type: {keyboard_type}")
    else:
        if keyboard_type.lower() == 'inline':
            keyboard = InlineKeyboard()
        elif keyboard_type.lower() == 'reply':
            keyboard = ReplyKeyboard()
        else:
            raise ValueError(f"Unsupported keyboard type: {keyboard_type}")

    if 'row_width' in config:
        keyboard.row_width = config['row_width']

    buttons = config.get('buttons', [])

    for button_config in buttons:
        if isinstance(button_config, dict):
            if keyboard_type == 'inline':
                button = InlineButton(**button_config)
            else:
                button = ReplyButton(**button_config)
        else:
            if keyboard_type == 'inline':
                button = InlineButton(text=str(button_config))
            else:
                button = ReplyButton(text=str(button_config))

        keyboard.add(button)

    return keyboard


def get_keyboard_info(keyboard: Union[InlineKeyboard, ReplyKeyboard]) -> Dict[str, Any]:
    """Get comprehensive information about a keyboard using modern typing features.

    Args:
        keyboard: The keyboard to analyze

    Returns:
        Dictionary with keyboard information
    """
    info = {
        'type': type(keyboard).__name__,
        'row_width': keyboard.row_width,
        'total_buttons': sum(len(row) for row in keyboard.keyboard),
        'total_rows': len(keyboard.keyboard),
        'python_version': get_python_version(),
        'features': {
            'match_case': supports_match_case(),
            'typing_self': supports_typing_self(),
            'literal_types': supports_literal_types(),
        }
    }

    if isinstance(keyboard, InlineKeyboard):
        info.update({
            'has_pagination': bool(keyboard.count_pages > 0),
            'current_page': keyboard.current_page,
            'total_pages': keyboard.count_pages,
            'callback_pattern': keyboard.callback_pattern,
            'custom_locales_count': len(keyboard.custom_locales),
        })
    elif isinstance(keyboard, ReplyKeyboard):
        info.update({
            'is_persistent': keyboard.is_persistent,
            'resize_keyboard': keyboard.resize_keyboard,
            'one_time_keyboard': keyboard.one_time_keyboard,
            'selective': keyboard.selective,
            'placeholder': keyboard.placeholder,
        })

    return info


def validate_keyboard_config(config: Dict[str, Any]) -> List[str]:
    """Validate a keyboard configuration using modern Python features.

    Args:
        config: Configuration dictionary to validate

    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []

    if supports_match_case():
        match config:
            case {'type': keyboard_type} if keyboard_type not in ['inline', 'reply']:
                errors.append(f"Invalid keyboard type: {keyboard_type}")
            case {'row_width': width} if not isinstance(width, int) or width < 1:
                errors.append("row_width must be a positive integer")
            case {'buttons': buttons} if not isinstance(buttons, list):
                errors.append("buttons must be a list")
            case _:
                pass
    else:
        if 'type' in config and config['type'] not in ['inline', 'reply']:
            errors.append(f"Invalid keyboard type: {config['type']}")

        if 'row_width' in config:
            width = config['row_width']
            if not isinstance(width, int) or width < 1:
                errors.append("row_width must be a positive integer")

        if 'buttons' in config and not isinstance(config['buttons'], list):
            errors.append("buttons must be a list")

    return errors


def export_keyboard_to_file(
    keyboard: Union[InlineKeyboard, ReplyKeyboard],
    file_path: Union[str, Path],
    format: Literal['json', 'yaml', 'pickle'] = 'json'
) -> None:
    """Export a keyboard to a file using modern Python features.

    Args:
        keyboard: The keyboard to export
        file_path: Path to save the file
        format: Export format ('json', 'yaml', or 'pickle')

    Raises:
        ValueError: If format is unsupported
        ImportError: If required library is not available
    """
    file_path = Path(file_path)

    if format == 'json':
        if json is None:
            raise ImportError("json module not available")
        data = keyboard.to_dict()
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    elif format == 'yaml':
        try:
            import yaml
            data = keyboard.to_dict()
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(data, f, default_flow_style=False, allow_unicode=True)
        except ImportError:
            raise ImportError("PyYAML is required for YAML export. Install with: pip install PyYAML")

    elif format == 'pickle':
        if pickle is None:
            raise ImportError("pickle module not available")
        with open(file_path, 'wb') as f:
            pickle.dump(keyboard, f)



def import_keyboard_from_file(
    file_path: Union[str, Path],
    format: Literal['json', 'yaml', 'pickle'] = 'json'
) -> Union[InlineKeyboard, ReplyKeyboard]:
    """Import a keyboard from a file using modern Python features.

    Args:
        file_path: Path to the file to load
        format: Import format ('json', 'yaml', or 'pickle')

    Returns:
        Loaded keyboard instance

    Raises:
        ValueError: If format is unsupported
        ImportError: If required library is not available
    """
    file_path = Path(file_path)

    if format == 'json':
        if json is None:
            raise ImportError("json module not available")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if 'callback_pattern' in data:
            return InlineKeyboard.from_dict(data)
        else:
            pass

    elif format == 'yaml':
        try:
            import yaml
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            if 'callback_pattern' in data:
                return InlineKeyboard.from_dict(data)
            else:
                pass
        except ImportError:
            raise ImportError("PyYAML is required for YAML import. Install with: pip install PyYAML")

    elif format == 'pickle':
        if pickle is None:
            raise ImportError("pickle module not available")
        with open(file_path, 'rb') as f:
            return pickle.load(f)


if supports_literal_types():
    KeyboardType = Literal['inline', 'reply']
    ExportFormat = Literal['json', 'yaml', 'pickle']
else:
    KeyboardType = str
    ExportFormat = str

