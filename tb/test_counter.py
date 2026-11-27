import random

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def reset(dut):
    """Start the clock, hold reset for a couple of cycles, then release it."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst.value = 1
    dut.en.value = 0

    for _ in range(3):
        await RisingEdge(dut.clk)

    dut.rst.value = 0
    await RisingEdge(dut.clk)

async def tick(dut):
    """Advance one clock cycle and return the counter value AFTER that edge."""
    await RisingEdge(dut.clk)
    await Timer(1, unit="ns")  # let the flip-flop outputs settle
    return int(dut.count.value)

@cocotb.test()
async def test_reset_clears_count(dut):
    await reset(dut)
    assert int(dut.count.value) == 0, f"Reset failed: count is {int(dut.count.value)}"
    dut._log.info("Reset test passed")

@cocotb.test()
async def test_counts_when_enabled(dut):
    await reset(dut)
    dut.en.value = 1
    for expected in range(1, 6):
        assert await tick(dut) == expected

@cocotb.test()
async def test_holds_when_disabled(dut):
    await reset(dut)
    dut.en.value = 1
    await tick(dut)
    assert await tick(dut) == 2
    dut.en.value = 0
    for _ in range(5):
        assert await tick(dut) == 2
