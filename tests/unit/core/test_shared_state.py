import pytest
import asyncio
from arkhon_rheo.core.shared_state import SharedAgentState


@pytest.mark.asyncio
async def test_shared_state_locking():
    shared_state = SharedAgentState()
    key = "counter"
    await shared_state.set(key, 0)

    async def increment():
        async with shared_state.lock(key):
            value = await shared_state.get(key)
            await asyncio.sleep(0.01)  # Simulate work
            await shared_state.set(key, value + 1)

    # Run 10 increments concurrently
    tasks = [increment() for _ in range(10)]
    await asyncio.gather(*tasks)

    final_value = await shared_state.get(key)
    assert final_value == 10


@pytest.mark.asyncio
async def test_shared_state_basic_ops():
    state = SharedAgentState()
    await state.set("a", 1)
    val = await state.get("a")
    assert val == 1

    await state.update("a", 2)
    val = await state.get("a")
    assert val == 2
