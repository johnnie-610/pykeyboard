# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/visualization.py
import logging
import json
from typing import Any, Dict, List, Optional

from .inline_keyboard import InlineKeyboard
from .keyboard_base import KeyboardBase
from .reply_keyboard import ReplyKeyboard

logger = logging.getLogger("pykeyboard.visualization")

class KeyboardVisualizer:
    """Advanced keyboard visualization and debugging utilities.

    This class provides comprehensive visualization tools for debugging and
    inspecting keyboard layouts, button structures, and keyboard state.
    Useful for development, testing, and troubleshooting keyboard issues.

    Features:
        - ASCII art keyboard visualization
        - JSON structure inspection
        - Button layout analysis
        - Performance metrics
        - Validation reports
    """

    @staticmethod
    def visualize_keyboard(keyboard: InlineKeyboard | ReplyKeyboard) -> str:
        """Create an ASCII art visualization of the keyboard layout.

        Args:
            keyboard: The keyboard to visualize

        Returns:
            str: ASCII art representation of the keyboard

        Example:
            >>> keyboard = InlineKeyboard()
            >>> keyboard.add("Yes", "No", "Maybe")
            >>> print(KeyboardVisualizer.visualize_keyboard(keyboard))
            ┌─────┬─────┬─────┐
            │ Yes │ No  │Maybe│
            └─────┴─────┴─────┘
        """
        if not keyboard.keyboard:
            return "┌─── Empty Keyboard ───┐\n│   No buttons added   │\n└──────────────────────┘"

        max_widths = []
        for row in keyboard.keyboard:
            for i, button in enumerate(row):
                if i >= len(max_widths):
                    max_widths.append(0)
                text = button.text if hasattr(button, "text") else str(button)
                max_widths[i] = max(max_widths[i], len(text))

        max_widths = [max(w, 3) for w in max_widths]

        lines = []

        top_border = "┌" + "┬".join("─" * (w + 2) for w in max_widths) + "┐"
        lines.append(top_border)

        for row_idx, row in enumerate(keyboard.keyboard):
            row_parts = []
            for i, button in enumerate(row):
                text = button.text if hasattr(button, "text") else str(button)
                width = max_widths[i]
                row_parts.append(f" {text.center(width)} ")

            row_line = "│" + "│".join(row_parts) + "│"
            lines.append(row_line)

            if row_idx < len(keyboard.keyboard) - 1:
                separator = (
                    "├" + "┼".join("─" * (w + 2) for w in max_widths) + "┤"
                )
                lines.append(separator)

        bottom_border = "└" + "┴".join("─" * (w + 2) for w in max_widths) + "┘"
        lines.append(bottom_border)

        return "\n".join(lines)

    @staticmethod
    def analyze_keyboard(
        keyboard: InlineKeyboard | ReplyKeyboard,
    ) -> Dict[str, Any]:
        """Analyze keyboard structure and provide detailed statistics.

        Args:
            keyboard: The keyboard to analyze

        Returns:
            Dict containing analysis results

        Example:
            >>> keyboard = InlineKeyboard()
            >>> keyboard.add("A", "B", "C", "D")
            >>> analysis = KeyboardVisualizer.analyze_keyboard(keyboard)
            >>> print(f"Total buttons: {analysis['total_buttons']}")
            Total buttons: 4
        """
        analysis = {
            "keyboard_type": type(keyboard).__name__,
            "total_buttons": 0,
            "total_rows": len(keyboard.keyboard),
            "row_lengths": [],
            "button_types": {},
            "max_row_length": 0,
            "min_row_length": float("inf"),
            "average_row_length": 0,
            "empty_rows": 0,
            "button_texts": [],
            "structure_valid": True,
            "issues": [],
        }

        for row_idx, row in enumerate(keyboard.keyboard):
            row_len = len(row)
            analysis["row_lengths"].append(row_len)
            analysis["total_buttons"] += row_len
            analysis["max_row_length"] = max(
                analysis["max_row_length"], row_len
            )
            analysis["min_row_length"] = min(
                analysis["min_row_length"], row_len
            )

            if row_len == 0:
                analysis["empty_rows"] += 1
                analysis["issues"].append(f"Row {row_idx} is empty")

            for button in row:
                btn_type = type(button).__name__
                analysis["button_types"][btn_type] = (
                    analysis["button_types"].get(btn_type, 0) + 1
                )

                if hasattr(button, "text"):
                    analysis["button_texts"].append(button.text)
                else:
                    analysis["button_texts"].append(str(button))

        if analysis["total_buttons"] > 0:
            analysis["average_row_length"] = (
                analysis["total_buttons"] / analysis["total_rows"]
            )

        if analysis["total_buttons"] == 0:
            analysis["issues"].append("Keyboard has no buttons")
            analysis["structure_valid"] = False

        if analysis["empty_rows"] > 0:
            analysis["structure_valid"] = False

        return analysis

    @staticmethod
    def generate_debug_report(keyboard: InlineKeyboard | ReplyKeyboard) -> str:
        """Generate a comprehensive debug report for the keyboard.

        Args:
            keyboard: The keyboard to debug

        Returns:
            str: Detailed debug report

        Example:
            >>> keyboard = InlineKeyboard()
            >>> keyboard.paginate(5, 3, "page_{number}")
            >>> report = KeyboardVisualizer.generate_debug_report(keyboard)
            >>> print(report)
            === Keyboard Debug Report ===
            Type: InlineKeyboard
            Total Buttons: 5
            ...
        """
        analysis = KeyboardVisualizer.analyze_keyboard(keyboard)
        visualization = KeyboardVisualizer.visualize_keyboard(keyboard)

        report_lines = [
            "=" * 50,
            "KEYBOARD DEBUG REPORT",
            "=" * 50,
            f"Keyboard Type: {analysis['keyboard_type']}",
            f"Total Buttons: {analysis['total_buttons']}",
            f"Total Rows: {analysis['total_rows']}",
            f"Row Lengths: {analysis['row_lengths']}",
            f"Max Row Length: {analysis['max_row_length']}",
            f"Min Row Length: {analysis['min_row_length']}",
            f"Average Row Length: {analysis['average_row_length']:.1f}",
            f"Empty Rows: {analysis['empty_rows']}",
            f"Button Types: {analysis['button_types']}",
            f"Structure Valid: {analysis['structure_valid']}",
            "",
            "BUTTON TEXTS:",
        ]

        for i, text in enumerate(analysis["button_texts"][:20]):
            report_lines.append(f"  {i+1:2d}. {text}")
        if len(analysis["button_texts"]) > 20:
            report_lines.append(
                f"  ... and {len(analysis['button_texts']) - 20} more"
            )

        if analysis["issues"]:
            report_lines.extend(
                [
                    "",
                    "ISSUES FOUND:",
                    *[f"  • {issue}" for issue in analysis["issues"]],
                ]
            )

        report_lines.extend(["", "VISUALIZATION:", visualization, "", "=" * 50])

        return "\n".join(report_lines)

    @staticmethod
    def compare_keyboards(
        keyboard1: InlineKeyboard | ReplyKeyboard,
        keyboard2: InlineKeyboard | ReplyKeyboard,
    ) -> Dict[str, Any]:
        """Compare two keyboards and highlight differences.

        Args:
            keyboard1: First keyboard to compare
            keyboard2: Second keyboard to compare

        Returns:
            Dict containing comparison results

        Example:
            >>> kb1 = InlineKeyboard()
            >>> kb1.add("A", "B")
            >>> kb2 = InlineKeyboard()
            >>> kb2.add("A", "C")
            >>> diff = KeyboardVisualizer.compare_keyboards(kb1, kb2)
            >>> print(f"Differences: {diff['differences']}")
        """
        analysis1 = KeyboardVisualizer.analyze_keyboard(keyboard1)
        analysis2 = KeyboardVisualizer.analyze_keyboard(keyboard2)

        comparison = {
            "keyboard1_type": analysis1["keyboard_type"],
            "keyboard2_type": analysis2["keyboard_type"],
            "differences": [],
            "similarities": [],
            "structure_match": True,
        }

        metrics_to_compare = [
            "total_buttons",
            "total_rows",
            "max_row_length",
            "min_row_length",
            "empty_rows",
        ]

        for metric in metrics_to_compare:
            if analysis1[metric] != analysis2[metric]:
                comparison["differences"].append(
                    f"{metric}: {analysis1[metric]} vs {analysis2[metric]}"
                )
            else:
                comparison["similarities"].append(
                    f"{metric}: {analysis1[metric]}"
                )

        if analysis1["row_lengths"] != analysis2["row_lengths"]:
            comparison["differences"].append(
                f"row_lengths: {analysis1['row_lengths']} vs {analysis2['row_lengths']}"
            )
            comparison["structure_match"] = False
        else:
            comparison["similarities"].append("row_lengths: identical")

        if analysis1["button_texts"] != analysis2["button_texts"]:
            comparison["differences"].append("button_texts: different")
            comparison["structure_match"] = False
        else:
            comparison["similarities"].append("button_texts: identical")

        return comparison

    @staticmethod
    def export_keyboard_data(
        keyboard: InlineKeyboard | ReplyKeyboard, format: str = "json"
    ) -> str:
        """Export keyboard data in various formats for debugging.

        Args:
            keyboard: The keyboard to export
            format: Export format ("json", "yaml", "text")

        Returns:
            str: Exported keyboard data

        Example:
            >>> keyboard = InlineKeyboard()
            >>> keyboard.add("Test", "Button")
            >>> json_data = KeyboardVisualizer.export_keyboard_data(keyboard, "json")
            >>> print(json_data)
            {"keyboard": [["Test", "Button"]], ...}
        """
        if format.lower() == "json":
            return keyboard.to_json()
        elif format.lower() == "text":
            return KeyboardVisualizer.generate_debug_report(keyboard)
        elif format.lower() == "yaml":
            try:
                import yaml

                data = keyboard.to_dict()
                return yaml.dump(
                    data, default_flow_style=False, allow_unicode=True
                )
            except ImportError:
                return "YAML export requires PyYAML: pip install PyYAML"
        else:
            return (
                f"Unsupported format: {format}. Use 'json', 'yaml', or 'text'."
            )


def visualize(keyboard: InlineKeyboard | ReplyKeyboard) -> str:
    """Quick visualization of a keyboard."""
    return KeyboardVisualizer.visualize_keyboard(keyboard)


def debug(keyboard: InlineKeyboard | ReplyKeyboard) -> str:
    """Quick debug report for a keyboard."""
    return KeyboardVisualizer.generate_debug_report(keyboard)


def analyze(keyboard: InlineKeyboard | ReplyKeyboard) -> Dict[str, Any]:
    """Quick analysis of a keyboard."""
    return KeyboardVisualizer.analyze_keyboard(keyboard)
