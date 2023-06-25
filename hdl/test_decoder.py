import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue


@cocotb.test()
async def test_decoder(dut):
    dut._log.warning(f"Test {__name__} Starting...")
    await Timer(100, "ns")

    dut._log.info(f"Input: 0001110")
    dut._log.info(f"Input: + 001 1 10")
    vec = BinaryValue("0001110") ## 3/16 + 001 1 10
    dut.posit.value = vec
    await Timer(100, "ns")
    dut._log.info(f"Output: {dut.regime_len.value}")
    dut._log.info(f"Posit: {dut.posit_reduced.value}")
    dut._log.info(f"R Mask: {dut.r_mask.value}")
    dut._log.info(f"N Mask: {dut.nought_mask.value}")
    dut._log.info(f"E Mask: {dut.exp_mask.value}")
    dut._log.info(f"F Mask: {dut.frac_mask.value}")


    dut._log.info(f"Input: 0111000")
    dut._log.info(f"Input: + 1110 0 0")
    vec = BinaryValue("0111000") ## 16 + 1110 0 0
    dut.posit.value = vec
    await Timer(100, "ns")
    dut._log.info(f"Output: {dut.regime_len.value}")
    dut._log.info(f"Posit: {dut.posit_reduced.value}")
    dut._log.info(f"R Mask: {dut.r_mask.value}")
    dut._log.info(f"N Mask: {dut.nought_mask.value}")
    dut._log.info(f"E Mask: {dut.exp_mask.value}")
    dut._log.info(f"F Mask: {dut.frac_mask.value}")






