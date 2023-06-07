import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue


@cocotb.test()
async def test_count_leading_ones(dut):
    dut._log.warning(f"Test {__name__} Starting...")
    await Timer(100, "ns")

    dut._log.info(f"Input: 0001110")
    vec = BinaryValue("0001110") ## 3/16
    dut.posit.value = vec
    await Timer(100, "ns")
    dut._log.info(f"Output: {dut.regime_len.value}")


    dut._log.info(f"Input: 0111000")
    vec = BinaryValue("0111000") ## 16
    dut.posit.value = vec
    await Timer(100, "ns")
    dut._log.info(f"Output: {dut.regime_len.value}")




