"""Tests for utility functions and modern Python features."""

import pytest
from pykeyboard import (
    get_python_version, supports_match_case, supports_typing_self,
    supports_literal_types, create_keyboard_from_config,
    get_keyboard_info, validate_keyboard_config,
    export_keyboard_to_file, import_keyboard_from_file,
    InlineKeyboard, ReplyKeyboard
)
import json
import tempfile
import os


class TestPythonVersionUtilities:
    """Test cases for Python version utility functions."""

    def test_get_python_version(self):
        """Test getting Python version as tuple."""
        version = get_python_version()

        assert isinstance(version, tuple)
        assert len(version) == 3
        assert all(isinstance(v, int) for v in version)
        assert version[0] >= 3  # Major version should be 3 or higher

    def test_supports_match_case(self):
        """Test match/case support detection."""
        result = supports_match_case()

        # Should return True for Python 3.10+, False for older versions
        assert isinstance(result, bool)

    def test_supports_typing_self(self):
        """Test typing.Self support detection."""
        result = supports_typing_self()

        # Should return True for Python 3.11+, False for older versions
        assert isinstance(result, bool)

    def test_supports_literal_types(self):
        """Test Literal types support detection."""
        result = supports_literal_types()

        # Should return True for Python 3.8+, False for older versions
        assert isinstance(result, bool)


class TestKeyboardCreation:
    """Test cases for keyboard creation from configuration."""

    def test_create_inline_keyboard_from_config(self):
        """Test creating inline keyboard from configuration."""
        config = {
            "type": "inline",
            "row_width": 2,
            "buttons": [
                {"text": "Button 1", "callback_data": "btn1"},
                {"text": "Button 2", "callback_data": "btn2"},
                "Button 3"  # Simple text button
            ]
        }

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)
        assert keyboard.row_width == 2
        assert len(keyboard.keyboard) == 2  # 3 buttons with row_width=2 = 2 rows
        assert len(keyboard.keyboard[0]) == 2
        assert len(keyboard.keyboard[1]) == 1

    def test_create_reply_keyboard_from_config(self):
        """Test creating reply keyboard from configuration."""
        config = {
            "type": "reply",
            "buttons": [
                {"text": "Reply 1", "request_contact": True},
                "Reply 2"
            ]
        }

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, ReplyKeyboard)
        assert len(keyboard.keyboard) == 1
        assert len(keyboard.keyboard[0]) == 2

    def test_create_keyboard_invalid_type(self):
        """Test creating keyboard with invalid type."""
        config = {
            "type": "invalid",
            "buttons": ["Button 1"]
        }

        with pytest.raises(ValueError, match="Unsupported keyboard type"):
            create_keyboard_from_config(config)

    def test_create_keyboard_missing_type(self):
        """Test creating keyboard with missing type defaults to inline."""
        config = {
            "buttons": ["Button 1"]
        }

        keyboard = create_keyboard_from_config(config)

        assert isinstance(keyboard, InlineKeyboard)


class TestKeyboardInfo:
    """Test cases for keyboard information retrieval."""

    def test_get_inline_keyboard_info(self):
        """Test getting information about inline keyboard."""
        keyboard = InlineKeyboard()
        keyboard.add("Button 1", "Button 2")
        keyboard.paginate(5, 3, "page_{number}")

        info = get_keyboard_info(keyboard)

        assert info["type"] == "InlineKeyboard"
        assert info["total_buttons"] == 2
        assert info["total_rows"] == 2  # 1 row of buttons + 1 row of pagination
        assert info["has_pagination"] is True
        assert info["current_page"] == 3
        assert info["total_pages"] == 5

    def test_get_reply_keyboard_info(self):
        """Test getting information about reply keyboard."""
        keyboard = ReplyKeyboard()
        keyboard.add("Reply 1", "Reply 2")
        keyboard.is_persistent = True
        keyboard.resize_keyboard = True

        info = get_keyboard_info(keyboard)

        assert info["type"] == "ReplyKeyboard"
        assert info["total_buttons"] == 2
        assert info["is_persistent"] is True
        assert info["resize_keyboard"] is True

    def test_get_keyboard_info_features(self):
        """Test that keyboard info includes Python feature support."""
        info = get_keyboard_info(InlineKeyboard())

        assert "features" in info
        assert "match_case" in info["features"]
        assert "typing_self" in info["features"]
        assert "literal_types" in info["features"]
        assert isinstance(info["features"]["match_case"], bool)

    def test_get_keyboard_info_custom_locales_count(self):
        """Test that get_keyboard_info correctly counts custom locales."""
        keyboard = InlineKeyboard()

        # Initially no custom locales
        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 0

        # Add some custom locales
        keyboard.add_custom_locale("custom1", "Custom 1")
        keyboard.add_custom_locale("custom2", "Custom 2")

        # Check count is updated
        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 2

        # Clear custom locales
        keyboard.clear_custom_locales()
        info = get_keyboard_info(keyboard)
        assert info["custom_locales_count"] == 0


class TestConfigValidation:
    """Test cases for keyboard configuration validation."""

    def test_validate_valid_config(self):
        """Test validation of valid configuration."""
        config = {
            "type": "inline",
            "row_width": 3,
            "buttons": ["Button 1", "Button 2"]
        }

        errors = validate_keyboard_config(config)

        assert errors == []

    def test_validate_invalid_keyboard_type(self):
        """Test validation of invalid keyboard type."""
        config = {
            "type": "invalid_type",
            "buttons": ["Button 1"]
        }

        errors = validate_keyboard_config(config)

        assert len(errors) > 0
        assert any("Invalid keyboard type" in error for error in errors)

    def test_validate_invalid_row_width(self):
        """Test validation of invalid row width."""
        config = {
            "type": "inline",
            "row_width": 0,  # Invalid: must be >= 1
            "buttons": ["Button 1"]
        }

        errors = validate_keyboard_config(config)

        assert len(errors) > 0
        assert any("row_width must be a positive integer" in error for error in errors)

    def test_validate_invalid_buttons_type(self):
        """Test validation of invalid buttons type."""
        config = {
            "type": "inline",
            "buttons": "not_a_list"  # Invalid: must be a list
        }

        errors = validate_keyboard_config(config)

        assert len(errors) > 0
        assert any("buttons must be a list" in error for error in errors)


class TestFileOperations:
    """Test cases for keyboard file import/export operations."""

    def test_export_import_json(self):
        """Test JSON export and import roundtrip."""
        # Create a keyboard
        keyboard = InlineKeyboard()
        keyboard.add("Button 1", "Button 2")
        keyboard.paginate(5, 3, "page_{number}")

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            # Export to JSON
            export_keyboard_to_file(keyboard, temp_file, "json")

            # Import from JSON
            imported_keyboard = import_keyboard_from_file(temp_file, "json")

            # Verify the imported keyboard
            assert isinstance(imported_keyboard, InlineKeyboard)
            assert len(imported_keyboard.keyboard) == len(keyboard.keyboard)
            assert imported_keyboard.count_pages == keyboard.count_pages
            assert imported_keyboard.current_page == keyboard.current_page

        finally:
            os.unlink(temp_file)

    def test_export_import_yaml(self):
        """Test YAML export and import roundtrip."""
        pytest.importorskip("yaml")  # Skip if PyYAML not available

        # Create a keyboard
        keyboard = ReplyKeyboard()
        keyboard.add("Reply 1", "Reply 2")

        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml', delete=False) as f:
            temp_file = f.name

        try:
            # Export to YAML
            export_keyboard_to_file(keyboard, temp_file, "yaml")

            # Import from YAML
            imported_keyboard = import_keyboard_from_file(temp_file, "yaml")

            # Verify the imported keyboard
            assert isinstance(imported_keyboard, ReplyKeyboard)
            assert len(imported_keyboard.keyboard) == len(keyboard.keyboard)

        finally:
            os.unlink(temp_file)

    def test_export_import_pickle(self):
        """Test pickle export and import roundtrip."""
        import pickle

        # Create a keyboard
        keyboard = InlineKeyboard()
        keyboard.add("Button 1", "Button 2")

        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.pkl', delete=False) as f:
            temp_file = f.name

        try:
            # Export to pickle
            export_keyboard_to_file(keyboard, temp_file, "pickle")

            # Import from pickle
            imported_keyboard = import_keyboard_from_file(temp_file, "pickle")

            # Verify the imported keyboard
            assert isinstance(imported_keyboard, InlineKeyboard)
            assert len(imported_keyboard.keyboard) == len(keyboard.keyboard)

        finally:
            os.unlink(temp_file)

    def test_export_invalid_format(self):
        """Test export with invalid format."""
        keyboard = InlineKeyboard()
        keyboard.add("Button 1")

        with pytest.raises(ValueError, match="Unsupported export format"):
            export_keyboard_to_file(keyboard, "dummy.json", "invalid_format")

    def test_import_invalid_format(self):
        """Test import with invalid format."""
        with pytest.raises(ValueError, match="Unsupported import format"):
            import_keyboard_from_file("dummy.json", "invalid_format")

    def test_import_yaml_without_yaml(self):
        """Test YAML import when PyYAML is not available."""
        # Mock the yaml import to fail
        import sys
        original_import = __builtins__.__import__

        def mock_import(name, *args, **kwargs):
            if name == 'yaml':
                raise ImportError("No module named 'yaml'")
            return original_import(name, *args, **kwargs)

        __builtins__.__import__ = mock_import

        try:
            with pytest.raises(ImportError, match="PyYAML is required"):
                export_keyboard_to_file(InlineKeyboard(), "dummy.yaml", "yaml")
        finally:
            __builtins__.__import__ = original_import


class TestModernPythonFeatures:
    """Test cases for modern Python features usage."""

    def test_match_case_fallback(self):
        """Test that match/case fallback works correctly."""
        # This test ensures the fallback logic works when match/case is not available
        config = {"type": "inline", "buttons": ["Test"]}

        # The function should work regardless of Python version
        keyboard = create_keyboard_from_config(config)
        assert isinstance(keyboard, InlineKeyboard)

    def test_literal_types_fallback(self):
        """Test that Literal type fallbacks work correctly."""
        # Import the module to ensure type aliases are created correctly
        from pykeyboard.utils import KeyboardType, ExportFormat

        # These should be either Literal types or fallback str types
        assert KeyboardType is not None
        assert ExportFormat is not None

    def test_conditional_feature_usage(self):
        """Test that features are used conditionally based on Python version."""
        # Test the demonstrate_modern_features function
        from pykeyboard.utils import demonstrate_modern_features

        features = demonstrate_modern_features()

        assert isinstance(features, dict)
        assert "python_version" in features
        assert "match_case" in features
        assert "typing_self" in features
        assert "literal_types" in features

        # All values should be either tuples or booleans
        for key, value in features.items():
            if key == "python_version":
                assert isinstance(value, tuple)
            else:
                assert isinstance(value, bool)


class TestIntegration:
    """Integration tests for utility functions."""

    def test_full_config_workflow(self):
        """Test full configuration workflow."""
        # Create config
        config = {
            "type": "inline",
            "row_width": 2,
            "buttons": [
                {"text": "Start", "callback_data": "start"},
                {"text": "Help", "callback_data": "help"},
                {"text": "Settings", "callback_data": "settings"}
            ]
        }

        # Validate config
        errors = validate_keyboard_config(config)
        assert errors == []

        # Create keyboard
        keyboard = create_keyboard_from_config(config)

        # Get info
        info = get_keyboard_info(keyboard)
        assert info["total_buttons"] == 3
        assert info["row_width"] == 2

        # Export and import
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            temp_file = f.name

        try:
            export_keyboard_to_file(keyboard, temp_file, "json")
            imported = import_keyboard_from_file(temp_file, "json")

            assert len(imported.keyboard) == len(keyboard.keyboard)
        finally:
            os.unlink(temp_file)