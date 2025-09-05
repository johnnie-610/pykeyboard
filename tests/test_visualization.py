"""Tests for keyboard visualization and debugging utilities."""

import pytest
from pykeyboard import (
    KeyboardVisualizer, InlineKeyboard, ReplyKeyboard,
    InlineButton, ReplyButton, visualize, debug, analyze
)


class TestKeyboardVisualization:
    """Test cases for keyboard visualization functionality."""

    def test_visualize_empty_keyboard(self):
        """Test visualization of empty keyboard."""
        keyboard = InlineKeyboard()

        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)

        assert "Empty Keyboard" in visualization
        assert "No buttons added" in visualization

    def test_visualize_simple_keyboard(self):
        """Test visualization of simple keyboard."""
        keyboard = InlineKeyboard()
        keyboard.add("Button 1", "Button 2", "Button 3")

        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)

        # Should contain table borders and button text
        assert "┌" in visualization
        assert "┬" in visualization
        assert "┐" in visualization
        assert "Button 1" in visualization
        assert "Button 2" in visualization
        assert "Button 3" in visualization
        assert "└" in visualization
        assert "┴" in visualization
        assert "┘" in visualization

    def test_visualize_multi_row_keyboard(self):
        """Test visualization of multi-row keyboard."""
        keyboard = InlineKeyboard(row_width=2)
        keyboard.add("A", "B", "C", "D", "E")  # 3 rows: 2, 2, 1

        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)

        lines = visualization.split('\n')
        # Should have top border, 3 data rows, 2 separators, bottom border
        assert len(lines) >= 6  # Minimum lines for this layout

        # Check that we have the right number of columns in each row
        data_lines = [line for line in lines if '│' in line and not any(char in line for char in '┌┬┐├┼┤└┴┘')]
        assert len(data_lines) == 3  # 3 rows of data

    def test_visualize_with_different_lengths(self):
        """Test visualization with buttons of different lengths."""
        keyboard = InlineKeyboard()
        keyboard.add("Short", "Medium Length", "Very Long Button Text")

        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)

        # Should handle different button lengths properly
        assert "Short" in visualization
        assert "Medium Length" in visualization
        assert "Very Long Button Text" in visualization

    def test_visualize_reply_keyboard(self):
        """Test visualization of reply keyboard."""
        keyboard = ReplyKeyboard()
        keyboard.add("Reply 1", "Reply 2")

        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)

        assert "Reply 1" in visualization
        assert "Reply 2" in visualization


class TestKeyboardAnalysis:
    """Test cases for keyboard analysis functionality."""

    def test_analyze_empty_keyboard(self):
        """Test analysis of empty keyboard."""
        keyboard = InlineKeyboard()

        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)

        assert analysis["total_buttons"] == 0
        assert analysis["total_rows"] == 0
        assert analysis["structure_valid"] is False
        assert "Keyboard has no buttons" in analysis["issues"]

    def test_analyze_simple_keyboard(self):
        """Test analysis of simple keyboard."""
        keyboard = InlineKeyboard()
        keyboard.add("Btn1", "Btn2", "Btn3", "Btn4")

        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)

        assert analysis["total_buttons"] == 4
        assert analysis["total_rows"] == 1
        assert analysis["max_row_length"] == 4
        assert analysis["min_row_length"] == 4
        assert analysis["average_row_length"] == 4.0
        assert analysis["structure_valid"] is True
        assert len(analysis["button_texts"]) == 4

    def test_analyze_multi_row_keyboard(self):
        """Test analysis of multi-row keyboard."""
        keyboard = InlineKeyboard(row_width=2)
        keyboard.add("A", "B", "C", "D", "E")  # 3 rows: 2, 2, 1

        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)

        assert analysis["total_buttons"] == 5
        assert analysis["total_rows"] == 3
        assert analysis["max_row_length"] == 2
        assert analysis["min_row_length"] == 1
        assert analysis["average_row_length"] == 5/3
        assert analysis["empty_rows"] == 0

    def test_analyze_keyboard_with_empty_row(self):
        """Test analysis of keyboard with empty row."""
        keyboard = InlineKeyboard()
        keyboard.add("Btn1", "Btn2")
        keyboard.row()  # Add empty row
        keyboard.add("Btn3")

        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)

        assert analysis["total_buttons"] == 3
        assert analysis["total_rows"] == 3
        assert analysis["empty_rows"] == 1
        assert analysis["structure_valid"] is False
        assert any("empty" in issue.lower() for issue in analysis["issues"])

    def test_analyze_button_types(self):
        """Test analysis of different button types."""
        keyboard = InlineKeyboard()
        keyboard.add(
            InlineButton("Inline", "callback"),
            ReplyButton("Reply")
        )

        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)

        assert "InlineButton" in analysis["button_types"]
        assert "ReplyButton" in analysis["button_types"]
        assert analysis["button_types"]["InlineButton"] == 1
        assert analysis["button_types"]["ReplyButton"] == 1


class TestDebugReport:
    """Test cases for debug report generation."""

    def test_generate_debug_report_empty(self):
        """Test debug report for empty keyboard."""
        keyboard = InlineKeyboard()

        report = KeyboardVisualizer.generate_debug_report(keyboard)

        assert "KEYBOARD DEBUG REPORT" in report
        assert "Empty Keyboard" in report
        assert "No buttons added" in report

    def test_generate_debug_report_simple(self):
        """Test debug report for simple keyboard."""
        keyboard = InlineKeyboard()
        keyboard.add("Test Button")

        report = KeyboardVisualizer.generate_debug_report(keyboard)

        assert "KEYBOARD DEBUG REPORT" in report
        assert "InlineKeyboard" in report
        assert "Total Buttons: 1" in report
        assert "Total Rows: 1" in report
        assert "Test Button" in report

    def test_generate_debug_report_with_pagination(self):
        """Test debug report for keyboard with pagination."""
        keyboard = InlineKeyboard()
        keyboard.paginate(10, 5, "page_{number}")

        report = KeyboardVisualizer.generate_debug_report(keyboard)

        assert "Total Buttons: 5" in report  # pagination buttons
        assert "Total Rows: 1" in report
        assert "· 5 ·" in report  # current page indicator

    def test_generate_debug_report_with_issues(self):
        """Test debug report for keyboard with issues."""
        keyboard = InlineKeyboard()
        keyboard.add("Btn1", "Btn2")
        keyboard.row()  # Empty row

        report = KeyboardVisualizer.generate_debug_report(keyboard)

        assert "ISSUES FOUND:" in report
        assert "empty" in report.lower()


class TestKeyboardComparison:
    """Test cases for keyboard comparison functionality."""

    def test_compare_identical_keyboards(self):
        """Test comparison of identical keyboards."""
        kb1 = InlineKeyboard()
        kb1.add("A", "B", "C")

        kb2 = InlineKeyboard()
        kb2.add("A", "B", "C")

        comparison = KeyboardVisualizer.compare_keyboards(kb1, kb2)

        assert comparison["structure_match"] is True
        assert len(comparison["differences"]) == 0
        assert len(comparison["similarities"]) > 0

    def test_compare_different_keyboards(self):
        """Test comparison of different keyboards."""
        kb1 = InlineKeyboard()
        kb1.add("A", "B", "C")  # 3 buttons

        kb2 = InlineKeyboard()
        kb2.add("X", "Y")  # 2 buttons

        comparison = KeyboardVisualizer.compare_keyboards(kb1, kb2)

        assert comparison["structure_match"] is False
        assert len(comparison["differences"]) > 0
        assert any("total_buttons" in diff for diff in comparison["differences"])

    def test_compare_different_types(self):
        """Test comparison of different keyboard types."""
        kb1 = InlineKeyboard()
        kb1.add("Test")

        kb2 = ReplyKeyboard()
        kb2.add("Test")

        comparison = KeyboardVisualizer.compare_keyboards(kb1, kb2)

        assert comparison["keyboard1_type"] == "InlineKeyboard"
        assert comparison["keyboard2_type"] == "ReplyKeyboard"
        assert comparison["structure_match"] is False


class TestDataExport:
    """Test cases for keyboard data export functionality."""

    def test_export_json(self):
        """Test JSON export of keyboard data."""
        keyboard = InlineKeyboard()
        keyboard.add("Test Button")

        json_data = KeyboardVisualizer.export_keyboard_data(keyboard, "json")

        assert isinstance(json_data, str)
        assert '"text": "Test Button"' in json_data

    def test_export_text_report(self):
        """Test text export (debug report) of keyboard data."""
        keyboard = InlineKeyboard()
        keyboard.add("Test Button")

        text_data = KeyboardVisualizer.export_keyboard_data(keyboard, "text")

        assert isinstance(text_data, str)
        assert "KEYBOARD DEBUG REPORT" in text_data
        assert "Test Button" in text_data

    def test_export_yaml(self):
        """Test YAML export of keyboard data."""
        pytest.importorskip("yaml")  # Skip if PyYAML not available

        keyboard = InlineKeyboard()
        keyboard.add("Test Button")

        yaml_data = KeyboardVisualizer.export_keyboard_data(keyboard, "yaml")

        assert isinstance(yaml_data, str)
        assert "Test Button" in yaml_data

    def test_export_yaml_without_yaml(self):
        """Test YAML export when PyYAML is not available."""
        # Mock yaml import to fail
        import sys
        original_import = __builtins__.__import__

        def mock_import(name, *args, **kwargs):
            if name == 'yaml':
                raise ImportError("No module named 'yaml'")
            return original_import(name, *args, **kwargs)

        __builtins__.__import__ = mock_import

        try:
            keyboard = InlineKeyboard()
            result = KeyboardVisualizer.export_keyboard_data(keyboard, "yaml")

            assert "PyYAML" in result
            assert "pip install" in result
        finally:
            __builtins__.__import__ = original_import

    def test_export_invalid_format(self):
        """Test export with invalid format."""
        keyboard = InlineKeyboard()

        result = KeyboardVisualizer.export_keyboard_data(keyboard, "invalid")

        assert "Unsupported format" in result
        assert "json" in result
        assert "yaml" in result
        assert "text" in result


class TestConvenienceFunctions:
    """Test cases for convenience functions."""

    def test_visualize_function(self):
        """Test the visualize convenience function."""
        keyboard = InlineKeyboard()
        keyboard.add("Test")

        result = visualize(keyboard)

        assert isinstance(result, str)
        assert "Test" in result

    def test_debug_function(self):
        """Test the debug convenience function."""
        keyboard = InlineKeyboard()
        keyboard.add("Test")

        result = debug(keyboard)

        assert isinstance(result, str)
        assert "KEYBOARD DEBUG REPORT" in result
        assert "Test" in result

    def test_analyze_function(self):
        """Test the analyze convenience function."""
        keyboard = InlineKeyboard()
        keyboard.add("Test")

        result = analyze(keyboard)

        assert isinstance(result, dict)
        assert result["total_buttons"] == 1
        assert result["total_rows"] == 1


class TestVisualizationIntegration:
    """Integration tests for visualization functionality."""

    def test_complete_visualization_workflow(self):
        """Test complete visualization workflow."""
        # Create a complex keyboard
        keyboard = InlineKeyboard()
        keyboard.add("🚀 Start", "⚙️ Settings", "📊 Stats")
        keyboard.row("🆘 Help", "❓ FAQ")
        keyboard.paginate(5, 3, "page_{number}")

        # Test all visualization functions
        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)
        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)
        debug_report = KeyboardVisualizer.generate_debug_report(keyboard)

        # Verify visualization contains expected elements
        assert "🚀 Start" in visualization
        assert "⚙️ Settings" in visualization
        assert "📊 Stats" in visualization
        assert "🆘 Help" in visualization
        assert "❓ FAQ" in visualization
        assert "· 3 ·" in visualization  # Current page

        # Verify analysis is correct
        assert analysis["total_buttons"] == 8  # 5 buttons + 3 pagination
        assert analysis["total_rows"] == 3
        assert analysis["structure_valid"] is True

        # Verify debug report contains all information
        assert "KEYBOARD DEBUG REPORT" in debug_report
        assert "Total Buttons: 8" in debug_report
        assert "Total Rows: 3" in debug_report
        assert "🚀 Start" in debug_report

    def test_visualization_with_special_characters(self):
        """Test visualization with special characters and emojis."""
        keyboard = InlineKeyboard()
        keyboard.add("🚀", "⚙️", "📊", "🆘", "❓")

        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)

        # Should handle emojis and special characters correctly
        assert "🚀" in visualization
        assert "⚙️" in visualization
        assert "📊" in visualization
        assert "🆘" in visualization
        assert "❓" in visualization

    def test_large_keyboard_visualization(self):
        """Test visualization of large keyboard."""
        keyboard = InlineKeyboard(row_width=5)

        # Create 50 buttons
        buttons = [f"Btn{i:02d}" for i in range(1, 51)]
        keyboard.add(*buttons)

        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)
        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)

        # Should handle large keyboards efficiently
        assert analysis["total_buttons"] == 50
        assert analysis["total_rows"] == 10  # 50 buttons / 5 per row
        assert "Btn01" in visualization
        assert "Btn50" in visualization

        # Visualization should not be excessively long
        lines = visualization.split('\n')
        assert len(lines) < 50  # Reasonable limit for visualization size