import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge


async def reset(dut):
    """Start the clock, hold reset for a couple of cycles, then release it."""
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    dut.rst.value = 1
    dut.en.value = 0

    for _ in range(3):
        await RisingEdge(dut.clk)

    dut.rst.value = 0
    await RisingEdge(dut.clk)


@cocotb.test()
async def test_reset_clears_count(dut):
    await reset(dut)
    assert int(dut.count.value) == 0, f"Reset failed: count is {int(dut.count.value)}"
    dut._log.info("Reset test passed")
