# Copyright (c) 2025 Johnnie
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# This file is part of the pykeyboard-kurigram library
#
# pykeyboard/performance.py

import statistics
import time
import logging
from typing import Any, Callable, Dict, List, Optional, Union

from .inline_keyboard import InlineKeyboard
from .reply_keyboard import ReplyKeyboard

logger = logging.getLogger("pykeyboard.performance")

class KeyboardProfiler:
    """Performance profiler for keyboard operations.

    This class provides comprehensive performance monitoring for keyboard
    operations, including creation time, serialization, and common operations.

    Features:
        - Operation timing and benchmarking
        - Memory usage tracking
        - Statistical analysis of performance
        - Performance regression detection
        - Detailed performance reports
    """

    def __init__(self):
        """Initialize the profiler."""
        self._measurements: Dict[str, List[float]] = {}
        self._memory_measurements: Dict[str, List[int]] = {}
        self._operation_counts: Dict[str, int] = {}

    def start_operation(self, operation_name: str) -> "OperationTimer":
        """Start timing an operation.

        Args:
            operation_name: Name of the operation to time

        Returns:
            OperationTimer context manager
        """
        return OperationTimer(self, operation_name)

    def record_measurement(
        self,
        operation_name: str,
        duration: float,
        memory_usage: Optional[int] = None,
    ):
        """Record a performance measurement.

        Args:
            operation_name: Name of the operation
            duration: Duration in seconds
            memory_usage: Memory usage in bytes (optional)
        """
        if operation_name not in self._measurements:
            self._measurements[operation_name] = []
        self._measurements[operation_name].append(duration)

        if memory_usage is not None:
            if operation_name not in self._memory_measurements:
                self._memory_measurements[operation_name] = []
            self._memory_measurements[operation_name].append(memory_usage)

        self._operation_counts[operation_name] = (
            self._operation_counts.get(operation_name, 0) + 1
        )

    def get_operation_stats(self, operation_name: str) -> Dict[str, Any]:
        """Get statistical information for an operation.

        Args:
            operation_name: Name of the operation

        Returns:
            Dict with statistical information
        """
        if operation_name not in self._measurements:
            return {}

        measurements = self._measurements[operation_name]
        stats = {
            "count": len(measurements),
            "total_time": sum(measurements),
            "mean": statistics.mean(measurements),
            "median": statistics.median(measurements),
            "min": min(measurements),
            "max": max(measurements),
            "stdev": (
                statistics.stdev(measurements) if len(measurements) > 1 else 0
            ),
        }

        if operation_name in self._memory_measurements:
            memory_measurements = self._memory_measurements[operation_name]
            stats.update(
                {
                    "memory_mean": statistics.mean(memory_measurements),
                    "memory_median": statistics.median(memory_measurements),
                    "memory_min": min(memory_measurements),
                    "memory_max": max(memory_measurements),
                }
            )

        return stats

    def get_all_stats(self) -> Dict[str, Dict[str, Any]]:
        """Get statistics for all operations.

        Returns:
            Dict mapping operation names to their statistics
        """
        return {
            op: self.get_operation_stats(op) for op in self._measurements.keys()
        }

    def generate_report(self, format: str = "text") -> str:
        """Generate a performance report.

        Args:
            format: Report format ('text', 'json', 'markdown')

        Returns:
            Formatted performance report
        """
        stats = self.get_all_stats()

        if format == "json":
            import json

            return json.dumps(stats, indent=2, default=str)

        elif format == "markdown":
            return self._format_markdown_report(stats)

        else:  # text format
            return self._format_text_report(stats)

    def _format_text_report(self, stats: Dict[str, Dict[str, Any]]) -> str:
        """Format statistics as text report."""
        lines = []
        lines.append("Keyboard Performance Report")
        lines.append("=" * 50)

        for operation, op_stats in stats.items():
            lines.append(f"\nOperation: {operation}")
            lines.append(f"  Count: {op_stats['count']}")
            lines.append(f"  Total Time: {op_stats['total_time']:.4f}s")
            lines.append(f"  Mean: {op_stats['mean']:.4f}s")
            lines.append(f"  Median: {op_stats['median']:.4f}s")
            lines.append(f"  Min: {op_stats['min']:.4f}s")
            lines.append(f"  Max: {op_stats['max']:.4f}s")
            if "stdev" in op_stats:
                lines.append(f"  Std Dev: {op_stats['stdev']:.4f}s")

            if "memory_mean" in op_stats:
                lines.append(
                    f"  Memory Mean: {op_stats['memory_mean']:.0f} bytes"
                )
                lines.append(
                    f"  Memory Median: {op_stats['memory_median']:.0f} bytes"
                )

        return "\n".join(lines)

    def _format_markdown_report(self, stats: Dict[str, Dict[str, Any]]) -> str:
        """Format statistics as markdown report."""
        lines = []
        lines.append("# Keyboard Performance Report")
        lines.append("")

        for operation, op_stats in stats.items():
            lines.append(f"## {operation}")
            lines.append("")
            lines.append(f"- **Count:** {op_stats['count']}")
            lines.append(f"- **Total Time:** {op_stats['total_time']:.4f}s")
            lines.append(f"- **Mean:** {op_stats['mean']:.4f}s")
            lines.append(f"- **Median:** {op_stats['median']:.4f}s")
            lines.append(f"- **Min:** {op_stats['min']:.4f}s")
            lines.append(f"- **Max:** {op_stats['max']:.4f}s")
            if "stdev" in op_stats:
                lines.append(f"- **Std Dev:** {op_stats['stdev']:.4f}s")

            if "memory_mean" in op_stats:
                lines.append(
                    f"- **Memory Mean:** {op_stats['memory_mean']:.0f} bytes"
                )
                lines.append(
                    f"- **Memory Median:** {op_stats['memory_median']:.0f} bytes"
                )
            lines.append("")

        return "\n".join(lines)

    def benchmark_keyboard_creation(
        self,
        keyboard_factory: Callable[[], Union[InlineKeyboard, ReplyKeyboard]],
        iterations: int = 100,
    ) -> Dict[str, Any]:
        """Benchmark keyboard creation performance.

        Args:
            keyboard_factory: Function that creates a keyboard
            iterations: Number of iterations to run

        Returns:
            Dict with benchmark results
        """

        times = []

        for _ in range(iterations):
            with self.start_operation("keyboard_creation"):
                keyboard = keyboard_factory()

        creation_stats = self.get_operation_stats("keyboard_creation")

        # Additional metrics
        keyboard = keyboard_factory()
        creation_stats.update(
            {
                "keyboard_type": type(keyboard).__name__,
                "total_buttons": sum(len(row) for row in keyboard.keyboard),
                "total_rows": len(keyboard.keyboard),
                "buttons_per_second": (
                    creation_stats["count"] / creation_stats["total_time"]
                    if creation_stats["total_time"] > 0
                    else 0
                ),
            }
        )

        return creation_stats

    def benchmark_keyboard_operations(
        self,
        keyboard: Union[InlineKeyboard, ReplyKeyboard],
        operations: List[str],
        iterations: int = 50,
    ) -> Dict[str, Dict[str, Any]]:
        """Benchmark various keyboard operations.

        Args:
            keyboard: Keyboard to benchmark
            operations: List of operations to benchmark
            iterations: Number of iterations per operation

        Returns:
            Dict mapping operation names to their benchmark results
        """

        results = {}

        for operation in operations:
            if operation == "serialization":
                self._benchmark_serialization(keyboard, iterations)
                results[operation] = self.get_operation_stats("serialization")
            elif operation == "deserialization":
                self._benchmark_deserialization(keyboard, iterations)
                results[operation] = self.get_operation_stats("deserialization")
            elif operation == "pyrogram_conversion":
                self._benchmark_pyrogram_conversion(keyboard, iterations)
                results[operation] = self.get_operation_stats(
                    "pyrogram_conversion"
                )

        return results

    def _benchmark_serialization(
        self, keyboard: Union[InlineKeyboard, ReplyKeyboard], iterations: int
    ):
        """Benchmark keyboard serialization."""
        for _ in range(iterations):
            with self.start_operation("serialization"):
                json_str = keyboard.to_json()

    def _benchmark_deserialization(
        self, keyboard: Union[InlineKeyboard, ReplyKeyboard], iterations: int
    ):
        """Benchmark keyboard deserialization."""
        json_str = keyboard.to_json()
        for _ in range(iterations):
            with self.start_operation("deserialization"):
                if isinstance(keyboard, InlineKeyboard):
                    InlineKeyboard.from_json(json_str)
                else:
                    ReplyKeyboard.from_json(json_str)

    def _benchmark_pyrogram_conversion(
        self, keyboard: Union[InlineKeyboard, ReplyKeyboard], iterations: int
    ):
        """Benchmark Pyrogram markup conversion."""
        for _ in range(iterations):
            with self.start_operation("pyrogram_conversion"):
                _ = keyboard.pyrogram_markup


class OperationTimer:
    """Context manager for timing operations."""

    def __init__(self, profiler: KeyboardProfiler, operation_name: str):
        """Initialize the timer.

        Args:
            profiler: Profiler instance
            operation_name: Name of the operation
        """
        self.profiler = profiler
        self.operation_name = operation_name
        self.start_time = None
        self.memory_start = None

    def __enter__(self):
        """Start timing."""
        self.start_time = time.perf_counter()

        # Try to get memory usage (optional)
        try:
            import os

            import psutil

            process = psutil.Process(os.getpid())
            self.memory_start = process.memory_info().rss
        except ImportError:
            self.memory_start = None

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and record measurement."""
        if self.start_time is not None:
            duration = time.perf_counter() - self.start_time

            memory_usage = None
            if self.memory_start is not None:
                try:
                    import os

                    import psutil

                    process = psutil.Process(os.getpid())
                    memory_end = process.memory_info().rss
                    memory_usage = memory_end - self.memory_start
                except ImportError:
                    pass

            self.profiler.record_measurement(
                self.operation_name, duration, memory_usage
            )


# Global profiler instance
default_profiler = KeyboardProfiler()


# Convenience functions
def profile_operation(operation_name: str):
    """Decorator to profile a function.

    Args:
        operation_name: Name of the operation

    Returns:
        Decorated function
    """

    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            with default_profiler.start_operation(operation_name):
                return func(*args, **kwargs)

        return wrapper

    return decorator


def get_performance_stats(
    operation_name: Optional[str] = None,
) -> Union[Dict[str, Any], Dict[str, Dict[str, Any]]]:
    """Get performance statistics.

    Args:
        operation_name: Specific operation name, or None for all operations

    Returns:
        Performance statistics
    """
    if operation_name:
        return default_profiler.get_operation_stats(operation_name)
    else:
        return default_profiler.get_all_stats()


def generate_performance_report(format: str = "text") -> str:
    """Generate a performance report.

    Args:
        format: Report format ('text', 'json', 'markdown')

    Returns:
        Formatted performance report
    """
    return default_profiler.generate_report(format)


def benchmark_keyboard_creation(
    keyboard_factory: Callable[[], Union[InlineKeyboard, ReplyKeyboard]],
    iterations: int = 100,
) -> Dict[str, Any]:
    """Benchmark keyboard creation performance.

    Args:
        keyboard_factory: Function that creates a keyboard
        iterations: Number of iterations to run

    Returns:
        Dict with benchmark results
    """
    return default_profiler.benchmark_keyboard_creation(
        keyboard_factory, iterations
    )


def benchmark_keyboard_operations(
    keyboard: Union[InlineKeyboard, ReplyKeyboard],
    operations: List[str],
    iterations: int = 50,
) -> Dict[str, Dict[str, Any]]:
    """Benchmark various keyboard operations.

    Args:
        keyboard: Keyboard to benchmark
        operations: List of operations to benchmark
        iterations: Number of iterations per operation

    Returns:
        Dict mapping operation names to their benchmark results
    """
    return default_profiler.benchmark_keyboard_operations(
        keyboard, operations, iterations
    )
