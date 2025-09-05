# PyKeyboard Edge Cases and Error Handling Guide

This document covers edge cases, error scenarios, and defensive programming practices for PyKeyboard. Understanding these edge cases will help you write robust code that handles unexpected situations gracefully.

## Table of Contents

1. [Keyboard Creation Edge Cases](#keyboard-creation-edge-cases)
2. [Button Validation Edge Cases](#button-validation-edge-cases)
3. [Pagination Edge Cases](#pagination-edge-cases)
4. [Language Selection Edge Cases](#language-selection-edge-cases)
5. [Serialization Edge Cases](#serialization-edge-cases)
6. [Performance Edge Cases](#performance-edge-cases)
7. [Error Handling Patterns](#error-handling-patterns)
8. [Best Practices](#best-practices)

## Keyboard Creation Edge Cases

### Empty Keyboards

```python
from pykeyboard import InlineKeyboard

# This is valid - empty keyboards are allowed
keyboard = InlineKeyboard()
print(len(keyboard.keyboard))  # Output: 0

# Adding to empty keyboard
keyboard.add()  # Valid but does nothing
print(len(keyboard.keyboard))  # Output: 0
```

### Single Button Keyboards

```python
keyboard = InlineKeyboard()
keyboard.add(InlineButton("Only Button", "action:single"))

# This creates a keyboard with one row and one button
print(keyboard.keyboard)  # Output: [[InlineButton(...)]]
```

### Maximum Button Limits

```python
# Telegram has limits on keyboard size
# PyKeyboard handles this gracefully but logs warnings

# Very large keyboard (approaching Telegram limits)
large_keyboard = InlineKeyboard()
buttons = []
for i in range(100):  # This might exceed Telegram's limits
    buttons.append(InlineButton(f"Btn{i}", f"action:{i}"))

large_keyboard.add(*buttons)
# PyKeyboard will create the keyboard but Telegram may reject it
```

## Button Validation Edge Cases

### Text Validation

```python
from pykeyboard import InlineButton

# Valid cases
valid_buttons = [
    InlineButton("OK", "ok"),
    InlineButton("A", "a"),
    InlineButton("Button with spaces", "spaces"),
    InlineButton("123", "numbers"),
    InlineButton("Mixed 123 Text", "mixed"),
]

# Invalid cases that raise ValueError
try:
    InlineButton("", "empty")  # Empty text
except ValueError as e:
    print(f"Error: {e}")  # "Button text cannot be empty"

try:
    InlineButton(None, "none")  # None text
except ValueError as e:
    print(f"Error: {e}")  # "Button text must be a string"
```

### Callback Data Limits

```python
# Telegram limits callback data to 64 bytes
long_callback = "a" * 65  # 65 characters

try:
    button = InlineButton("Test", long_callback)
except ValueError as e:
    print(f"Error: {e}")  # Callback data too long

# Valid: exactly 64 characters
max_callback = "a" * 64
button = InlineButton("Test", max_callback)  # This works
```

### URL Validation

```python
# Valid URLs
valid_urls = [
    "https://example.com",
    "http://example.com",
    "tg://resolve?domain=username",
]

# Invalid URLs
invalid_urls = [
    "ftp://example.com",      # Wrong protocol
    "example.com",            # Missing protocol
    "javascript:alert(1)",    # Dangerous protocol
]
```

## Pagination Edge Cases

### Boundary Conditions

```python
keyboard = InlineKeyboard()

# Edge case 1: Minimum pages
keyboard.paginate(1, 1, "page_{number}")  # Valid: 1 page

# Edge case 2: Current page equals total pages
keyboard.paginate(10, 10, "page_{number}")  # Valid: last page

# Edge case 3: Large page numbers
keyboard.paginate(1000, 500, "page_{number}")  # Valid: middle of large set

# Invalid cases
try:
    keyboard.paginate(0, 1, "page_{number}")  # 0 pages
except ValueError as e:
    print(f"Error: {e}")

try:
    keyboard.paginate(5, 6, "page_{number}")  # Current > total
except ValueError as e:
    print(f"Error: {e}")

try:
    keyboard.paginate(5, 0, "page_{number}")  # Current = 0
except ValueError as e:
    print(f"Error: {e}")
```

### Callback Pattern Edge Cases

```python
# Valid patterns
valid_patterns = [
    "page_{number}",
    "nav_{number}",
    "goto_{number}",
    "p{number}",
]

# Invalid patterns
invalid_patterns = [
    "page_number",      # Missing {number}
    "page_{num}",       # Wrong placeholder
    "{number}page",     # Placeholder not in callback
    "",                 # Empty pattern
]
```

### Large Pagination Sets

```python
# Very large pagination (edge case)
keyboard = InlineKeyboard()
keyboard.paginate(10000, 5000, "page_{number}")

# This creates a large keyboard - consider performance implications
print(f"Rows: {len(keyboard.keyboard)}")
print(f"Total buttons: {sum(len(row) for row in keyboard.keyboard)}")
```

## Language Selection Edge Cases

### Invalid Locales

```python
keyboard = InlineKeyboard()

# Valid locales
keyboard.languages("lang_{locale}", ["en_US", "fr_FR"])

# Invalid locales are silently ignored
keyboard.languages("lang_{locale}", ["invalid_locale", "en_US"])
# Only en_US button will be created

# Empty locale list
keyboard.languages("lang_{locale}", [])  # Creates empty keyboard

# Single locale
keyboard.languages("lang_{locale}", "en_US")  # String instead of list
```

### Custom Locales

```python
# Adding custom locales
keyboard.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")
keyboard.add_custom_locale("es_MEX", "🇲🇽 Mexican Spanish")

# Custom locales override built-in ones
keyboard.add_custom_locale("en_US", "🇺🇸 American English")  # Overrides built-in

# Invalid custom locale names
try:
    keyboard.add_custom_locale("", "Empty")  # Empty name
except ValueError as e:
    print(f"Error: {e}")

try:
    keyboard.add_custom_locale("valid", "")  # Empty display name
except ValueError as e:
    print(f"Error: {e}")
```

### Row Width Edge Cases

```python
# Extreme row widths
keyboard.languages("lang_{locale}", ["en_US", "fr_FR"], row_width=1)  # 1 column
keyboard.languages("lang_{locale}", ["en_US", "fr_FR"], row_width=10)  # Wide layout

# Invalid row width
try:
    keyboard.languages("lang_{locale}", ["en_US"], row_width=0)
except ValueError as e:
    print(f"Error: {e}")  # row_width must be at least 1
```

## Serialization Edge Cases

### JSON Serialization

```python
keyboard = InlineKeyboard()
keyboard.add(InlineButton("Test", "test"))

# Normal serialization
json_str = keyboard.to_json()

# Large keyboard serialization
large_keyboard = InlineKeyboard()
for i in range(1000):
    large_keyboard.add(InlineButton(f"Btn{i}", f"action:{i}"))

large_json = large_keyboard.to_json()
print(f"JSON size: {len(large_json)} characters")
```

### File Operations

```python
# File operation edge cases
keyboard = InlineKeyboard()
keyboard.add(InlineButton("Test", "test"))

# Non-existent directory
try:
    export_keyboard_to_file(keyboard, "/nonexistent/path/keyboard.json")
except FileNotFoundError as e:
    print(f"Error: {e}")

# Permission denied
try:
    export_keyboard_to_file(keyboard, "/root/keyboard.json")
except PermissionError as e:
    print(f"Error: {e}")

# Invalid file format
try:
    export_keyboard_to_file(keyboard, "keyboard.invalid")
except ValueError as e:
    print(f"Error: {e}")
```

### Corrupted Data

```python
# Handling corrupted JSON
corrupted_json = '{"invalid": json}'

try:
    InlineKeyboard.from_json(corrupted_json)
except Exception as e:
    print(f"Error: {e}")

# Missing required fields
incomplete_json = '{"keyboard": []}'

try:
    InlineKeyboard.from_json(incomplete_json)
except Exception as e:
    print(f"Error: {e}")
```

## Performance Edge Cases

### Memory Usage

```python
# High memory usage scenarios
large_keyboard = InlineKeyboard()

# Creating many similar buttons (good candidate for caching)
buttons = []
for i in range(10000):
    buttons.append(InlineButton(f"Button {i}", f"action:{i}"))

large_keyboard.add(*buttons)

# Check memory usage
import sys
print(f"Keyboard size in memory: {sys.getsizeof(large_keyboard)} bytes")
```

### LRU Cache Behavior

```python
from pykeyboard.inline_keyboard import InlineKeyboard

# Cache hit scenario
button1 = InlineKeyboard._create_button("Test", "test")
button2 = InlineKeyboard._create_button("Test", "test")  # Cache hit

print(f"Same object: {button1 is button2}")  # True (cached)

# Cache size limits
# Creating more than 512 different buttons will evict old ones
for i in range(600):
    InlineKeyboard._create_button(f"Btn{i}", f"action:{i}")
```

### Computation Complexity

```python
# O(n) operations
keyboard = InlineKeyboard()

# Adding buttons: O(1) per button
for i in range(1000):
    keyboard.add(InlineButton(f"Btn{i}", f"action:{i}"))

# Pagination: O(1) for small sets, O(log n) for large sets
keyboard.paginate(1000, 500, "page_{number}")

# Serialization: O(n) where n is total buttons
json_data = keyboard.to_json()
```

## Error Handling Patterns

### Defensive Programming

```python
def safe_keyboard_creation(button_data_list):
    """Safely create keyboard with error handling."""
    keyboard = InlineKeyboard()
    valid_buttons = []

    for data in button_data_list:
        try:
            if isinstance(data, dict):
                button = InlineButton(**data)
            elif isinstance(data, str):
                button = InlineButton(data, data.lower())
            else:
                continue  # Skip invalid data

            valid_buttons.append(button)

        except (ValueError, TypeError) as e:
            print(f"Skipping invalid button data: {data} - {e}")
            continue

    if valid_buttons:
        keyboard.add(*valid_buttons)
    else:
        # Fallback for completely invalid data
        keyboard.add(InlineButton("Error", "error:no_buttons"))

    return keyboard
```

### Graceful Degradation

```python
def create_resilient_keyboard(config):
    """Create keyboard with graceful degradation."""
    keyboard = InlineKeyboard()

    try:
        # Try advanced features first
        if 'pagination' in config:
            keyboard.paginate(**config['pagination'])

        if 'languages' in config:
            keyboard.languages(**config['languages'])

        if 'buttons' in config:
            buttons = []
            for btn_config in config['buttons']:
                try:
                    buttons.append(InlineButton(**btn_config))
                except Exception:
                    continue  # Skip invalid buttons
            keyboard.add(*buttons)

    except Exception as e:
        # Fallback to basic keyboard
        print(f"Advanced features failed: {e}")
        keyboard.add(InlineButton("Basic Action", "fallback:action"))

    return keyboard
```

### Validation Integration

```python
from pykeyboard import ButtonValidator

def create_validated_keyboard(button_configs):
    """Create keyboard with comprehensive validation."""
    validator = ButtonValidator()
    keyboard = InlineKeyboard()
    valid_buttons = []

    for config in button_configs:
        try:
            button = InlineButton(**config)
            validation_result = validator.validate_button(button)

            if validation_result['is_valid']:
                valid_buttons.append(button)
            else:
                print(f"Button validation failed: {config}")
                for error in validation_result['errors']:
                    print(f"  - {error}")
                for suggestion in validation_result['suggestions']:
                    print(f"  💡 {suggestion}")

        except Exception as e:
            print(f"Button creation failed: {config} - {e}")

    if valid_buttons:
        keyboard.add(*valid_buttons)
    else:
        keyboard.add(InlineButton("No valid buttons", "error:no_valid_buttons"))

    return keyboard
```

## Best Practices

### 1. Input Validation

```python
def validate_keyboard_input(data):
    """Comprehensive input validation."""
    if not isinstance(data, dict):
        raise TypeError("Keyboard data must be a dictionary")

    required_fields = ['type']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    if data['type'] not in ['inline', 'reply']:
        raise ValueError(f"Invalid keyboard type: {data['type']}")

    if 'buttons' in data:
        if not isinstance(data['buttons'], list):
            raise TypeError("Buttons must be a list")
        for i, btn in enumerate(data['buttons']):
            if not isinstance(btn, dict):
                raise TypeError(f"Button {i} must be a dictionary")
            if 'text' not in btn:
                raise ValueError(f"Button {i} missing 'text' field")
```

### 2. Error Recovery

```python
def create_keyboard_with_fallback(primary_config, fallback_config=None):
    """Create keyboard with automatic fallback."""
    try:
        return create_keyboard_from_config(primary_config)
    except Exception as e:
        print(f"Primary keyboard creation failed: {e}")

        if fallback_config:
            try:
                return create_keyboard_from_config(fallback_config)
            except Exception as e2:
                print(f"Fallback keyboard creation also failed: {e2}")

        # Ultimate fallback
        keyboard = InlineKeyboard()
        keyboard.add(InlineButton("Retry", "action:retry"))
        return keyboard
```

### 3. Resource Management

```python
import contextlib

@contextlib.contextmanager
def keyboard_operation():
    """Context manager for keyboard operations."""
    keyboard = None
    try:
        keyboard = InlineKeyboard()
        yield keyboard
    except Exception as e:
        print(f"Keyboard operation failed: {e}")
        raise
    finally:
        # Cleanup if needed
        if keyboard and hasattr(keyboard, '_cleanup'):
            keyboard._cleanup()

# Usage
with keyboard_operation() as kb:
    kb.add(InlineButton("Test", "test"))
    # Perform operations
```

### 4. Performance Monitoring

```python
import time
import functools

def monitor_performance(func):
    """Decorator to monitor function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            print(f"{func.__name__} took {execution_time:.4f} seconds")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"{func.__name__} failed after {execution_time:.4f} seconds: {e}")
            raise
    return wrapper

@monitor_performance
def create_large_keyboard():
    """Create large keyboard with performance monitoring."""
    keyboard = InlineKeyboard()
    buttons = [InlineButton(f"Btn{i}", f"action:{i}") for i in range(1000)]
    keyboard.add(*buttons)
    return keyboard
```

### 5. Testing Edge Cases

```python
def test_edge_cases():
    """Comprehensive edge case testing."""
    test_cases = [
        # Empty inputs
        {"type": "inline", "buttons": []},
        {"type": "inline", "buttons": None},

        # Invalid data types
        {"type": "inline", "buttons": "not_a_list"},
        {"type": "inline", "buttons": [123, 456]},

        # Missing required fields
        {"buttons": []},  # Missing type
        {"type": "inline", "buttons": [{"callback_data": "test"}]},  # Missing text

        # Extreme values
        {"type": "inline", "buttons": [{"text": "", "callback_data": "empty"}]},
        {"type": "inline", "buttons": [{"text": "A" * 1000, "callback_data": "long"}]},
    ]

    for i, test_case in enumerate(test_cases):
        try:
            keyboard = create_keyboard_from_config(test_case)
            print(f"Test case {i}: ✅ Passed")
        except Exception as e:
            print(f"Test case {i}: ❌ Failed - {e}")
```

This guide covers the most common edge cases and error scenarios you'll encounter when using PyKeyboard. By understanding these edge cases and implementing proper error handling, you can create robust applications that gracefully handle unexpected situations.