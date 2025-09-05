"""Performance profiling and benchmarking tests for pykeyboard."""

import time
import pytest
from typing import List
from pykeyboard import InlineKeyboard, InlineButton, ReplyKeyboard, ReplyButton


class TestPerformance:
    """Performance tests for keyboard operations."""

    def test_inline_keyboard_construction_performance(self):
        """Test performance of inline keyboard construction with various sizes."""
        sizes = [10, 50, 100, 500, 1000]

        for size in sizes:
            start_time = time.perf_counter()

            # Create keyboard with many buttons
            keyboard = InlineKeyboard(row_width=min(8, size // 10 + 1))
            buttons = [InlineButton(f"Button {i}", f"callback_{i}") for i in range(size)]
            keyboard.add(*buttons)

            end_time = time.perf_counter()
            duration = end_time - start_time

            # Performance assertion: should complete within reasonable time
            assert duration < 1.0, f"Keyboard construction took too long: {duration:.4f}s for {size} buttons"
            print(".4f")

    def test_pagination_performance(self):
        """Test performance of pagination with large page counts."""
        large_page_counts = [100, 500, 1000, 5000]

        for page_count in large_page_counts:
            start_time = time.perf_counter()

            keyboard = InlineKeyboard()
            keyboard.paginate(page_count, page_count // 2, "page_{number}")

            end_time = time.perf_counter()
            duration = end_time - start_time

            # Performance assertion
            assert duration < 0.5, f"Pagination took too long: {duration:.4f}s for {page_count} pages"
            print(".4f")

    def test_language_selection_performance(self):
        """Test performance of language selection with many locales."""
        # Test with all available locales
        all_locales = list(InlineKeyboard._get_locales().keys())

        start_time = time.perf_counter()

        keyboard = InlineKeyboard()
        keyboard.languages("lang_{locale}", all_locales, 5)

        end_time = time.perf_counter()
        duration = end_time - start_time

        # Performance assertion
        assert duration < 1.0, f"Language selection took too long: {duration:.4f}s for {len(all_locales)} locales"
        print(".4f")

    def test_button_creation_caching_performance(self):
        """Test performance improvement from button creation caching."""
        # Create the same button multiple times
        iterations = 1000

        start_time = time.perf_counter()

        keyboard = InlineKeyboard()
        for i in range(iterations):
            # Same button parameters to test cache hit
            button = keyboard._create_button("Test Button", "test_callback")

        end_time = time.perf_counter()
        duration = end_time - start_time

        # Performance assertion: should be very fast due to caching
        assert duration < 0.1, f"Button creation took too long: {duration:.4f}s for {iterations} iterations"
        print(".4f")

    def test_reply_keyboard_performance(self):
        """Test performance of reply keyboard operations."""
        sizes = [20, 100, 500]

        for size in sizes:
            start_time = time.perf_counter()

            keyboard = ReplyKeyboard(row_width=min(6, size // 10 + 1))
            buttons = [ReplyButton(f"Button {i}") for i in range(size)]
            keyboard.add(*buttons)

            end_time = time.perf_counter()
            duration = end_time - start_time

            # Performance assertion
            assert duration < 1.0, f"Reply keyboard construction took too long: {duration:.4f}s for {size} buttons"
            print(".4f")

    def test_memory_usage_growth(self):
        """Test that memory usage doesn't grow excessively with repeated operations."""
        import psutil
        import os

        if not hasattr(psutil, 'Process'):
            pytest.skip("psutil not available for memory testing")

        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Perform many keyboard operations
        for i in range(100):
            keyboard = InlineKeyboard()
            keyboard.paginate(50, 25, f"page_{i}_{{number}}")
            keyboard.languages("lang_{locale}", ["en_US", "ru_RU", "de_DE"], 2)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_growth = final_memory - initial_memory

        # Memory growth should be reasonable (less than 50MB for 100 operations)
        assert memory_growth < 50, f"Excessive memory growth: {memory_growth:.2f}MB"
        print(".2f")

    def test_json_serialization_performance(self):
        """Test performance of JSON serialization/deserialization."""
        # Create a complex keyboard
        keyboard = InlineKeyboard()
        keyboard.paginate(100, 50, "page_{number}")
        keyboard.languages("lang_{locale}", ["en_US", "ru_RU", "de_DE", "fr_FR", "es_ES"], 3)

        # Test serialization performance
        start_time = time.perf_counter()
        json_str = keyboard.to_json()
        end_time = time.perf_counter()
        serialize_duration = end_time - start_time

        # Test deserialization performance
        start_time = time.perf_counter()
        restored = InlineKeyboard.from_json(json_str)
        end_time = time.perf_counter()
        deserialize_duration = end_time - start_time

        # Performance assertions
        assert serialize_duration < 0.1, f"JSON serialization took too long: {serialize_duration:.4f}s"
        assert deserialize_duration < 0.1, f"JSON deserialization took too long: {deserialize_duration:.4f}s"

        # Verify correctness
        assert restored.count_pages == keyboard.count_pages
        assert len(restored.keyboard) == len(keyboard.keyboard)

        print(".4f")
        print(".4f")

    @pytest.mark.parametrize("button_count", [10, 50, 100])
    def test_scaling_performance(self, button_count):
        """Test performance scaling with increasing button counts."""
        start_time = time.perf_counter()

        keyboard = InlineKeyboard(row_width=5)
        buttons = [InlineButton(f"Btn {i}", f"cb_{i}") for i in range(button_count)]
        keyboard.add(*buttons)

        end_time = time.perf_counter()
        duration = end_time - start_time

        # Performance should scale roughly linearly
        expected_max_duration = button_count * 0.001  # 1ms per button
        assert duration < expected_max_duration, (
            f"Performance scaling issue: {duration:.4f}s for {button_count} buttons "
            f"(expected < {expected_max_duration:.4f}s)"
        )

        print(".4f")