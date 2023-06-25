import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.types import LogicArray
from cocotb.clock import Timer
from cocotb.binary import BinaryValue


@cocotb.test()
async def test_posit_adder_top(dut):

    dut._log.warning(f"Test {__name__} Starting...")
    dut._log.info(f"1 + 2 = 3")

    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    one = BinaryValue("0100000") ## 1
    dut.a.value = one
    two = BinaryValue("0101000") ## 2
    dut.b.value = two

    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    # dut._log.info(f"Output: {dut.regime_len.value}")
    dut._log.info(f"a   : {dut.a.value}")
    dut._log.info(f"a_s : {dut.dc_a_sign.value}")
    dut._log.info(f"a_r : {dut.dc_a_regime.value}")
    dut._log.info(f"a_e : {dut.dc_a_exponent.value}")
    dut._log.info(f"a_m : {dut.dc_a_mantissa.value}")

    dut._log.info(f"b   : {dut.b.value}")
    dut._log.info(f"b_s : {dut.dc_b_sign.value}")
    dut._log.info(f"b_r : {dut.dc_b_regime.value}")
    dut._log.info(f"b_e : {dut.dc_b_exponent.value}")
    dut._log.info(f"b_m : {dut.dc_b_mantissa.value}")

    await FallingEdge(dut.clk)
    # end


