"""Async integration tests for pagination duplicate prevention."""

import asyncio

import pytest

from pykeyboard import (InlineKeyboard, PaginationUnchangedError,
                        pagination_client_context)


class TestAsyncPaginationPrevention:
    """Async integration tests for pagination duplicate prevention."""

    @pytest.mark.asyncio
    async def test_async_multi_client_scenario(self):
        """Test multi-client scenario with different contexts."""
        results = []

        async def client_task(client_id):
            pagination_client_context.set(f"client_{client_id}")
            keyboard = InlineKeyboard()

            # Each client can create the same pagination
            keyboard.paginate(5, 3, "page_{number}")
            results.append((client_id, "created"))

            # But duplicate should be prevented per client
            try:
                keyboard.paginate(5, 3, "page_{number}")
                results.append((client_id, "error"))
            except PaginationUnchangedError:
                results.append((client_id, "duplicate"))

        # Simulate multiple clients
        tasks = [client_task(i) for i in range(1, 4)]
        await asyncio.gather(*tasks)

        # Verify each client worked independently
        assert len(results) == 6
        for i in range(1, 4):
            assert (i, "created") in results
            assert (i, "duplicate") in results

    @pytest.mark.asyncio
    async def test_async_performance_under_load(self):
        """Test performance with concurrent async operations."""
        pagination_client_context.set("perf_test")

        async def create_pagination(task_id):
            keyboard = InlineKeyboard()
            keyboard.paginate(10, 5, f"page_{task_id}_{{number}}")
            return task_id

        # Create many concurrent tasks
        tasks = [create_pagination(i) for i in range(50)]
        results = await asyncio.gather(*tasks)

        # All tasks should complete successfully
        assert len(results) == 50
        assert set(results) == set(range(50))

    @pytest.mark.asyncio
    async def test_async_error_handling_in_callback_flow(self):
        """Test error handling in typical async callback flow."""
        pagination_client_context.set("callback_test")

        # Simulate callback handler
        async def handle_callback():
            keyboard = InlineKeyboard()

            # First pagination call (simulating initial message)
            keyboard.paginate(5, 1, "page_{number}")

            # Simulate user clicking next page
            keyboard.paginate(5, 2, "page_{number}")

            # Simulate user clicking same page again (should be prevented)
            try:
                keyboard.paginate(5, 2, "page_{number}")
                return "error_not_prevented"
            except PaginationUnchangedError:
                return "duplicate_prevented"

        result = await handle_callback()
        assert result == "duplicate_prevented"

    @pytest.mark.asyncio
    async def test_async_contextvar_reset(self):
        """Test contextvar reset between operations."""
        results = []

        async def operation_with_context():
            pagination_client_context.set("temp_client")
            keyboard = InlineKeyboard()
            keyboard.paginate(5, 3, "page_{number}")
            results.append("created")

            # Reset context
            pagination_client_context.set(None)

            # New operation should use default source
            keyboard2 = InlineKeyboard()
            keyboard2.paginate(5, 3, "page_{number}")
            results.append("default_used")

        await operation_with_context()

        assert len(results) == 2
        assert "created" in results
        assert "default_used" in results

    @pytest.mark.asyncio
    async def test_async_memory_usage(self):
        """Test memory usage with prolonged async operations."""
        pagination_client_context.set("memory_test")

        # Create multiple keyboards with different sources
        keyboards = []
        for i in range(10):
            keyboard = InlineKeyboard()
            keyboard.paginate(
                5, 3, f"page_{i}_{{number}}", source=f"source_{i}"
            )
            keyboards.append(keyboard)

        # Verify all keyboards were created
        assert len(keyboards) == 10
        for kb in keyboards:
            assert kb.count_pages == 5

        # Each source should have its own hash tracking
        for i in range(10):
            with pytest.raises(PaginationUnchangedError):
                keyboards[i].paginate(
                    5, 3, f"page_{i}_{{number}}", source=f"source_{i}"
                )
