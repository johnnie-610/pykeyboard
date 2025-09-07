# Utilities API Reference

## Python Version Utilities

### get_python_version()

Get the current Python version as a tuple.

**Returns:**
- `tuple[int, int, int]`: Tuple of (major, minor, micro) version numbers

### supports_match_case()

Check if the current Python version supports match/case statements.

**Returns:**
- `bool`: True if Python 3.10+ is available, False otherwise

### supports_typing_self()

Check if the current Python version supports typing.Self.

**Returns:**
- `bool`: True if Python 3.11+ is available, False otherwise

### supports_literal_types()

Check if the current Python version supports Literal types.

**Returns:**
- `bool`: True if Python 3.8+ is available, False otherwise

---

## Keyboard Creation Utilities

### create_keyboard_from_config(config)

Create a keyboard from a configuration dictionary using modern Python features.

**Parameters:**
- `config` (Dict[str, Any]): Configuration dictionary with keyboard settings

**Returns:**
- `Union[InlineKeyboard, ReplyKeyboard]`: Configured keyboard instance

**Raises:**
- `ValueError`: If configuration is invalid

### get_keyboard_info(keyboard)

Get comprehensive information about a keyboard using modern typing features.

**Parameters:**
- `keyboard` (Union[InlineKeyboard, ReplyKeyboard]): The keyboard to analyze

**Returns:**
- `Dict[str, Any]`: Dictionary with keyboard information

### validate_keyboard_config(config)

Validate a keyboard configuration using modern Python features.

**Parameters:**
- `config` (Dict[str, Any]): Configuration dictionary to validate

**Returns:**
- `List[str]`: List of validation error messages (empty if valid)

---

## File I/O Utilities

### export_keyboard_to_file(keyboard, file_path, format='json')

Export a keyboard to a file using modern Python features.

**Parameters:**
- `keyboard` (Union[InlineKeyboard, ReplyKeyboard]): The keyboard to export
- `file_path` (Union[str, Path]): Path to save the file
- `format` (Literal['json', 'yaml', 'pickle']): Export format

**Raises:**
- `ValueError`: If format is unsupported
- `ImportError`: If required library is not available

### import_keyboard_from_file(file_path, format='json')

Import a keyboard from a file using modern Python features.

**Parameters:**
- `file_path` (Union[str, Path]): Path to the file to load
- `format` (Literal['json', 'yaml', 'pickle']): Import format

**Returns:**
- `Union[InlineKeyboard, ReplyKeyboard]`: Loaded keyboard instance

**Raises:**
- `ValueError`: If format is unsupported
- `ImportError`: If required library is not available

---

## Feature Demonstration

### demonstrate_modern_features()

Demonstrate modern Python features usage in the library.

**Returns:**
- `Dict[str, Any]`: Dictionary with information about Python version and supported features

---

## Type Aliases

### KeyboardType

Type alias for keyboard types.

```python
KeyboardType = Literal['inline', 'reply']  # or str if Literal not supported
```

### ExportFormat

Type alias for export formats.

```python
ExportFormat = Literal['json', 'yaml', 'pickle']  # or str if Literal not supported