#!/usr/bin/env python3
"""
PyKeyboard Usage Examples and Edge Cases
========================================

This file contains comprehensive examples demonstrating all features of PyKeyboard,
including edge cases, error handling, and best practices.

Run this file to see examples in action:
    python examples.py

For more information, visit: https://github.com/johnnie-610/pykeyboard
"""

import sys
import traceback
from typing import List, Dict, Any
from pathlib import Path

# Import PyKeyboard components
from pykeyboard import (
    # Core classes
    InlineKeyboard, ReplyKeyboard, InlineButton, ReplyButton,

    # Advanced features
    KeyboardBuilder, KeyboardFactory, KeyboardVisualizer,

    # Validation system
    ButtonValidator, add_validation_rule,

    # Modern utilities
    create_keyboard_from_config, export_keyboard_to_file, import_keyboard_from_file,
    get_keyboard_info, supports_match_case,

)


def print_separator(title: str = "", char: str = "=", length: int = 60):
    """Print a visual separator for examples."""
    if title:
        total_length = length
        title_length = len(title) + 2  # Add spaces
        side_length = (total_length - title_length) // 2
        separator = char * side_length + f" {title} " + char * (total_length - title_length - side_length)
        print(f"\n{separator}")
    else:
        print(f"\n{char * length}")


def example_basic_usage():
    """Example 1: Basic keyboard creation and usage."""
    print_separator("Example 1: Basic Usage")

    # Create a simple inline keyboard
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("👍 Like", "action:like"),
        InlineButton("👎 Dislike", "action:dislike"),
        InlineButton("🔄 Share", "action:share")
    )

    print("Basic Inline Keyboard:")
    print(KeyboardVisualizer.visualize_keyboard(keyboard))

    # Create a reply keyboard
    reply_kb = ReplyKeyboard()
    reply_kb.row(
        ReplyButton("Option A"),
        ReplyButton("Option B")
    )
    reply_kb.row(ReplyButton("Cancel"))

    print("\nBasic Reply Keyboard:")
    print(KeyboardVisualizer.visualize_keyboard(reply_kb))


def example_pagination():
    """Example 2: Advanced pagination with custom navigation."""
    print_separator("Example 2: Advanced Pagination")

    # Create paginated keyboard
    keyboard = InlineKeyboard()
    keyboard.paginate(25, 5, "page_{number}")

    print("Pagination Keyboard (Page 5 of 25):")
    print(KeyboardVisualizer.visualize_keyboard(keyboard))

    # Add custom navigation buttons
    keyboard.row(
        InlineButton("🔍 Search", "action:search"),
        InlineButton("🏠 Home", "action:home"),
        InlineButton("❌ Close", "action:close")
    )

    print("\nWith Custom Navigation:")
    print(KeyboardVisualizer.visualize_keyboard(keyboard))


def example_languages():
    """Example 3: Multi-language support with custom locales."""
    print_separator("Example 3: Multi-Language Support")

    # Create language selection keyboard
    keyboard = InlineKeyboard()
    keyboard.languages("lang_{locale}", ["en_US", "es_ES", "fr_FR", "de_DE"], 2)

    print("Language Selection Keyboard:")
    print(KeyboardVisualizer.visualize_keyboard(keyboard))

    # Add custom locale
    keyboard.add_custom_locale("en_PIRATE", "🏴‍☠️ Pirate English")
    keyboard.add_custom_locale("es_LATINO", "🇲🇽 Español Latino")

    # Create keyboard with custom locales
    custom_kb = InlineKeyboard()
    custom_kb.languages("set_lang_{locale}", ["en_PIRATE", "es_LATINO"])

    print("\nCustom Locales Keyboard:")
    print(KeyboardVisualizer.visualize_keyboard(custom_kb))


def example_builder_pattern():
    """Example 4: Fluent builder pattern for complex keyboards."""
    print_separator("Example 4: Builder Pattern")

    # Using the fluent builder API
    keyboard = (KeyboardBuilder(InlineKeyboard())
        .add_button("📧 Email", "contact:email")
        .add_button("📱 Phone", "contact:phone")
        .add_row("💬 Message", "contact:message")
        .add_conditional_button(True, "🚨 Emergency", "contact:emergency")
        .add_conditional_button(False, "🔒 Private", "contact:private")  # Won't be added
        .build())

    print("Built with Fluent API:")
    print(KeyboardVisualizer.visualize_keyboard(keyboard))

    # Using factory methods
    confirmation_kb = KeyboardFactory.create_confirmation_keyboard(
        yes_text="✅ Confirm",
        no_text="❌ Cancel",
        cancel_text="⏪ Back"
    )

    print("\nFactory Method - Confirmation:")
    print(KeyboardVisualizer.visualize_keyboard(confirmation_kb))


def example_validation():
    """Example 5: Custom validation and error handling."""
    print_separator("Example 5: Validation System")

    # Add custom validation rules
    add_validation_rule(
        "no_emojis",
        lambda btn, ctx: not any(ord(c) > 127 for c in btn.text),
        "Button text contains emojis or special characters",
        "Remove emojis and use plain text"
    )

    add_validation_rule(
        "reasonable_length",
        lambda btn, ctx: 1 <= len(btn.text) <= 30,
        "Button text must be 1-30 characters",
        "Shorten the button text"
    )

    # Create validator instance
    validator = ButtonValidator()

    # Test validation
    test_buttons = [
        InlineButton("Valid Button", "test:valid"),
        InlineButton("🚀 Too Long Button Text Here", "test:invalid"),
        InlineButton("", "test:empty"),  # Invalid
    ]

    print("Validation Results:")
    for i, button in enumerate(test_buttons, 1):
        result = validator.validate_button(button)
        status = "✅ Valid" if result['is_valid'] else "❌ Invalid"
        print(f"Button {i}: {status}")
        if not result['is_valid']:
            for error in result['errors']:
                print(f"  • {error}")
            for suggestion in result['suggestions']:
                print(f"  💡 {suggestion}")


def example_serialization():
    """Example 6: JSON serialization and file operations."""
    print_separator("Example 6: Serialization")

    # Create complex keyboard
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("Save", "action:save"),
        InlineButton("Load", "action:load"),
        InlineButton("Delete", "action:delete")
    )
    keyboard.paginate(10, 1, "nav_{number}")

    # Serialize to JSON
    json_str = keyboard.to_json()
    print(f"JSON Length: {len(json_str)} characters")
    print(f"JSON Preview: {json_str[:100]}...")

    # Deserialize from JSON
    restored_keyboard = InlineKeyboard.from_json(json_str)
    print(f"\nRestored Keyboard - {len(restored_keyboard.keyboard)} rows")

    # Export to file
    export_keyboard_to_file(keyboard, "example_keyboard.json")
    export_keyboard_to_file(keyboard, "example_keyboard.yaml")

    # Import from file
    imported_kb = import_keyboard_from_file("example_keyboard.json")
    print(f"Imported Keyboard - {len(imported_kb.keyboard)} rows")

    # Clean up
    Path("example_keyboard.json").unlink(missing_ok=True)
    Path("example_keyboard.yaml").unlink(missing_ok=True)


def example_visualization():
    """Example 7: Advanced debugging and visualization."""
    print_separator("Example 7: Visualization & Debugging")

    # Create complex keyboard for analysis
    keyboard = InlineKeyboard()
    keyboard.add(
        InlineButton("A", "a"), InlineButton("B", "b"), InlineButton("C", "c"),
        InlineButton("D", "d"), InlineButton("E", "e"), InlineButton("F", "f")
    )
    keyboard.row(InlineButton("Single", "single"))

    # ASCII visualization
    print("ASCII Visualization:")
    print(KeyboardVisualizer.visualize_keyboard(keyboard))

    # Detailed analysis
    analysis = KeyboardVisualizer.analyze_keyboard(keyboard)
    print("Analysis Results:")
    print(f"  • Total Buttons: {analysis['total_buttons']}")
    print(f"  • Total Rows: {analysis['total_rows']}")
    print(f"  • Max Row Length: {analysis['max_row_length']}")
    print(f"  • Structure Valid: {analysis['structure_valid']}")

    # Debug report
    print("Debug Report:")
    debug_lines = KeyboardVisualizer.generate_debug_report(keyboard).split('\n')[:15]
    for line in debug_lines:
        print(f"  {line}")


def example_modern_python():
    """Example 8: Modern Python features and utilities."""
    print_separator("Example 8: Modern Python Features")

    # Check Python version support
    print("Python Version Support:")
    print(f"  • Python Version: {sys.version}")
    print(f"  • Match/Case Support: {supports_match_case()}")
    print(f"  • Literal Types Support: {supports_literal_types()}")

    # Configuration-based keyboard creation
    config = {
        "type": "inline",
        "row_width": 2,
        "buttons": [
            {"text": "Start", "callback_data": "cmd:start"},
            {"text": "Help", "callback_data": "cmd:help"},
            {"text": "Settings", "callback_data": "cmd:settings"},
            {"text": "About", "callback_data": "cmd:about"}
        ]
    }

    keyboard = create_keyboard_from_config(config)
    print("Configuration-based Keyboard:")
    print(KeyboardVisualizer.visualize_keyboard(keyboard))

    # Keyboard information
    info = get_keyboard_info(keyboard)
    print("Keyboard Information:")
    print(f"  • Type: {info['type']}")
    print(f"  • Total Buttons: {info['total_buttons']}")
    print(f"  • Python Features: {info['features']}")


def example_edge_cases():
    """Example 9: Edge cases and error handling."""
    print_separator("Example 9: Edge Cases & Error Handling")

    print("Testing Edge Cases:")

    # Test 1: Empty keyboard
    try:
        empty_kb = InlineKeyboard()
        print("  ✅ Empty keyboard created successfully")
    except Exception as e:
        print(f"  ❌ Empty keyboard failed: {e}")

    # Test 2: Invalid pagination
    try:
        kb = InlineKeyboard()
        kb.paginate(0, 1, "page_{number}")  # Invalid: 0 pages
        print("  ❌ Should have failed with 0 pages")
    except ValueError as e:
        print(f"  ✅ Correctly caught invalid pagination: {e}")

    # Test 3: Invalid current page
    try:
        kb = InlineKeyboard()
        kb.paginate(5, 10, "page_{number}")  # Invalid: current > total
        print("  ❌ Should have failed with invalid current page")
    except ValueError as e:
        print(f"  ✅ Correctly caught invalid current page: {e}")

    # Test 4: Large keyboard
    try:
        kb = InlineKeyboard()
        # Create keyboard with many buttons
        buttons = [InlineButton(f"Btn{i}", f"action:{i}") for i in range(50)]
        kb.add(*buttons)
        print(f"  ✅ Large keyboard created: {len(kb.keyboard)} rows")
    except Exception as e:
        print(f"  ❌ Large keyboard failed: {e}")

    # Test 5: Invalid locale
    try:
        kb = InlineKeyboard()
        kb.languages("lang_{locale}", ["invalid_locale"])
        print("  ❌ Should have handled invalid locale gracefully")
    except Exception as e:
        print(f"  ✅ Correctly handled invalid locale: {e}")




def example_performance():
    """Example 11: Performance considerations and optimization."""
    print_separator("Example 11: Performance & Optimization")

    import time

    # Test keyboard creation performance
    print("Performance Testing:")

    # Small keyboard
    start_time = time.time()
    small_kb = InlineKeyboard()
    for i in range(10):
        small_kb.add(InlineButton(f"Button {i}", f"action:{i}"))
    small_time = time.time() - start_time
    print(".4f")

    # Large keyboard
    start_time = time.time()
    large_kb = InlineKeyboard()
    for i in range(100):
        large_kb.add(InlineButton(f"Button {i}", f"action:{i}"))
    large_time = time.time() - start_time
    print(".4f")

    # Pagination performance
    start_time = time.time()
    paginated_kb = InlineKeyboard()
    paginated_kb.paginate(1000, 500, "page_{number}")
    pagination_time = time.time() - start_time
    print(".4f")

    # Serialization performance
    start_time = time.time()
    json_data = large_kb.to_json()
    serialize_time = time.time() - start_time
    print(".4f")

    # Deserialization performance
    start_time = time.time()
    restored_kb = InlineKeyboard.from_json(json_data)
    deserialize_time = time.time() - start_time
    print(".4f")

    print("Optimization Tips:")
    print("  • Use LRU cache for repeated button creation")
    print("  • Minimize list copying in large keyboards")
    print("  • Use pagination for large datasets")
    print("  • Cache serialized keyboards when possible")


def main():
    """Run all examples."""
    print("🚀 PyKeyboard Comprehensive Examples")
    print("=" * 60)
    print("This script demonstrates all major features of PyKeyboard.")
    print("Each example shows different aspects of the library.\n")

    examples = [
        example_basic_usage,
        example_pagination,
        example_languages,
        example_builder_pattern,
        example_validation,
        example_serialization,
        example_visualization,
        example_modern_python,
        example_edge_cases,
        example_performance,
    ]

    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
            print(f"\n✅ Example {i}/{len(examples)} completed successfully")
        except Exception as e:
            print(f"\n❌ Example {i}/{len(examples)} failed: {e}")
            print("Traceback:")
            traceback.print_exc()

    print_separator("All Examples Complete", "=")
    print("🎉 Thank you for exploring PyKeyboard!")
    print("\n📚 For more information:")
    print("   • Documentation: https://pykeyboard.readthedocs.io/")
    print("   • GitHub: https://github.com/johnnie-610/pykeyboard")
    print("   • Issues: https://github.com/johnnie-610/pykeyboard/issues")
    print("   • Community: https://github.com/johnnie-610/pykeyboard/discussions")


if __name__ == "__main__":
    main()