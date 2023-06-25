import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue


@cocotb.test()
async def test_decoder_a(dut):
    dut._log.warning(f"Test {__name__} Starting...")
    await Timer(100, "ns")

    dut._log.info(f"Input: 0001110")
    dut._log.info(f"Input: + 001 1 10")
    vec = BinaryValue("0001110") ## 3/16 + 001 1 10
    dut.posit.value = vec
    await Timer(100, "ns")
    # dut._log.info(f"Output: {dut.regime_len.value}")
    dut._log.info(f"Posit : {dut.posit_reduced.value}")
    dut._log.info(f"R Mask: {dut.r_mask.value}")
    dut._log.info("")
    dut._log.info(f"N Mask: {dut.nought_mask.value}")
    dut._log.info(f"N 'ed : {dut.nought_masked.value}")
    dut._log.info("")
    dut._log.info(f"E Mask: {dut.exp_mask.value}")
    dut._log.info(f"E 'ed': {dut.exp_masked.value}")
    dut._log.info(f"E LSB : {dut.exp_LSB_bit.value}")
    dut._log.info(f"E     : {dut.exponent.value}")
    dut._log.info("")
    dut._log.info(f"F Mask: {dut.frac_mask.value}")#
    dut._log.info(f"F 'ed': {dut.frac_masked.value}")
    dut._log.info(f"F MSB : {dut.frac_MSB_bit.value}")
    dut._log.info(f"F     : {dut.mantissa.value}")


@cocotb.test()
async def test_decoder_b(dut):
    dut._log.warning(f"Test {__name__} Starting...")
    await Timer(100, "ns")

    dut._log.info(f"Input: 0111000")
    dut._log.info(f"Input: + 1110 0 0")
    vec = BinaryValue("0111000") ## 16 + 1110 0 0
    dut.posit.value = vec
    await Timer(100, "ns")
    # dut._log.info(f"Output: {dut.regime_len.value}")
    dut._log.info(f"Posit : {dut.posit_reduced.value}")
    dut._log.info(f"R Mask: {dut.r_mask.value}")
    dut._log.info("")
    dut._log.info(f"N Mask: {dut.nought_mask.value}")
    dut._log.info(f"N 'ed : {dut.nought_masked.value}")
    dut._log.info("")
    dut._log.info(f"E Mask: {dut.exp_mask.value}")
    dut._log.info(f"E 'ed': {dut.exp_masked.value}")
    dut._log.info(f"E LSB : {dut.exp_LSB_bit.value}")
    dut._log.info(f"E     : {dut.exponent.value}")
    dut._log.info("")
    dut._log.info(f"F Mask: {dut.frac_mask.value}")#
    dut._log.info(f"F 'ed': {dut.frac_masked.value}")
    dut._log.info(f"F MSB : {dut.frac_MSB_bit.value}")
    dut._log.info(f"F     : {dut.mantissa.value}")







