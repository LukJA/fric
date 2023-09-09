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
    two = BinaryValue("0101100") ## 3
    dut.b.value = two

    # get results into dc reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut._log.info(f"First Pulse:")

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
    dut._log.info(f"big:   (0.){dut.mant_add.big_mantissa.value}")
    dut._log.info(f"small: (0.){dut.mant_add.small_mantissa_sh.value}")
    dut._log.info(f"sum:   (0.){dut.mant_add.s_mantissa_sum.value}")
    dut._log.info(f"ovf:   {dut.mant_add.ovf.value}")
    dut._log.info(f"rout:  {dut.mant_add.interim_regime.value}")
    dut._log.info(f"eout:  {dut.mant_add.interim_exponent.value}")
    dut._log.info(f"mout:   (0.){dut.mant_add.mantissa_sum.value}")

    dut._log.info("")

    # get results into cn reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut._log.info("")

    dut._log.info(f"Second Pulse:")

    dut._log.info("")
    dut._log.info(f"r:   {dut.cn_interim_regime.value}")
    dut._log.info(f"e:   {dut.cn_interim_exponent.value}")
    dut._log.info(f"sum: (0.){dut.cn_mantissa_sum.value}")


    dut._log.info("")
    dut._log.info("Normalise Block")
    dut._log.info(f"msum_in:   {dut.p_norm.mantissa_sum.value}")
    dut._log.info(f"regi_in:   {dut.p_norm.interim_regime.value}")
    dut._log.info(f"expo_in:   {dut.p_norm.interim_exponent.value}")
    dut._log.info(f"Normed_mantissa:   {dut.p_norm.mantissa_lo.value}")
    dut._log.info(f"adj_exp:           {dut.p_norm.a_exponent.value}")
    dut._log.info("~")
    dut._log.info(f"shamt:     {dut.p_norm.exp_adj_a.value}")
    dut._log.info(f"_shamt:    {dut.p_norm.exp_adj_b.value}")

    dut._log.info(f"man_out:   {dut.p_norm.mantissa.value}")
    dut._log.info(f"exp_out:   {dut.p_norm.exponent.value}")
    dut._log.info(f"reg_out:   {dut.p_norm.regime.value}")

    # get results into nd reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut._log.info("")

    dut._log.info(f"Third Pulse:")

    dut._log.info("")
    dut._log.info(f"r:     {dut.nd_regime.value}")
    dut._log.info(f"e:     {dut.nd_exponent.value}")
    dut._log.info(f"m: (0.){dut.nd_mantissa.value}")
    dut._log.info(f"r:     {dut.p_encode.regime.value}")
    dut._log.info(f"e:     {dut.p_encode.exponent.value}")
    dut._log.info(f"m: (0.){dut.p_encode.mantissa.value}")
    dut._log.info("")
    dut._log.info(f"abs(r)      {dut.p_encode.abs_regime.value}")
    dut._log.info(f"m_exp       {dut.p_encode.expanded_mantissa.value}")
    dut._log.info("")
    dut._log.info(f"mantissa    {dut.p_encode.interim_posit.value}")
    dut._log.info(f"exponent    {dut.p_encode.shifted_exponent.value}")
    dut._log.info(f"rno_bit     {dut.p_encode.regime_rno.value}")
    dut._log.info(f"regime_rej  {dut.p_encode.regime_mask.value}")
    dut._log.info(f"posit       {dut.p_encode.posit_rounded.value}")
    dut._log.info(f"posit_s     {dut.p_encode.posit_signed.value}")
    
    dut._log.info("")
    dut._log.info("complete")
    dut._log.info(f"RESULT:     {dut.q.value}")

    await FallingEdge(dut.clk)
    # end


