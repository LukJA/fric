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

    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    # dut._log.info(f"Output: {dut.regime_len.value}")
    dut._log.info(f"a   : {dut.a.value}")
    dut._log.info(f"a_s : {dut.dc_a_sign.value}")
    dut._log.info(f"a_r : {dut.dc_a_regime.value}")
    dut._log.info(f"a_e : {dut.dc_a_exponent.value}")
    dut._log.info(f"a_m : {dut.dc_a_mantissa.value}")
    dut._log.info("")
    dut._log.info(f"b   : {dut.b.value}")
    dut._log.info(f"b_s : {dut.dc_b_sign.value}")
    dut._log.info(f"b_r : {dut.dc_b_regime.value}")
    dut._log.info(f"b_e : {dut.dc_b_exponent.value}")
    dut._log.info(f"b_m : {dut.dc_b_mantissa.value}")
    dut._log.info("")
    dut._log.info(f"BM  : {dut.mant_add.big_mantissa.value}")
    dut._log.info(f"SM  : {dut.mant_add.small_mantissa.value}")
    dut._log.info(f"a>? : {dut.mant_add.u_comp.a.value}")
    dut._log.info("")
    dut._log.info(f"I_R : {dut.mant_add.interim_regime.value}")
    dut._log.info(f"I_E : {dut.mant_add.interim_exponent.value}")
    dut._log.info(f"SH  : {dut.mant_add.shamt.value}")
    dut._log.info(f"SM  : {dut.mant_add.small_mantissa_sh.value}")

    dut._log.info("")
    dut._log.info(f"big:   0.{dut.mant_add.big_mantissa.value}")
    dut._log.info(f"small: 0.{dut.mant_add.small_mantissa_sh.value}")
    dut._log.info(f"rout:  {dut.mant_add.interim_regime.value}")
    dut._log.info(f"eout:  {dut.mant_add.interim_exponent.value}")

    await FallingEdge(dut.clk)
    # end


