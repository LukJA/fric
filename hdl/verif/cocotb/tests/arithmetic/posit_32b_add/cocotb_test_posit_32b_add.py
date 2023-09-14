import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.types import LogicArray
from cocotb.clock import Timer
from cocotb.binary import BinaryValue

import pyposit_v2 as pyposit
import random
## test seed
random.seed("fric")

async def propagate(dut):
    # get results into dc reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    # get results into cn reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    # get results into nd reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

async def test_ab(dut, i, j):
    a = pyposit.posit_model(2, (i, 32))
    b = pyposit.posit_model(2, (j, 32))
    c = a + b

    dut._log.warning(f"Select a:{i} b:{j}")
    dut._log.info(f"A:          {a}  :  {a.to_float()}")
    dut._log.info(f"B:          {b}  :  {b.to_float()}")

    one = BinaryValue(a.p_str) ## 1
    dut.a.value = one
    two = BinaryValue(b.p_str) ## 1
    dut.b.value = two

    await propagate(dut)
    r = pyposit.posit_model(2, str(dut.q.value))

    dut._log.info(f"EXPECT:     {c}  :  {c.to_float()}")
    if (dut.q.value == BinaryValue(c.p_str)):
        dut._log.info(f"RESULT:     {dut.q.value}  :  {r.to_float()}")
    else:
        dut._log.error(f"RESULT:     {dut.q.value}  :  {r.to_float()}")
    assert dut.q.value == BinaryValue(c.p_str) ## 2



@cocotb.test()
async def test_posit_adder_top(dut):

    dut._log.warning(f"Test {__name__} Starting...")

    i = 12
    j = 12

    dut._log.info(f"{i} + {j} = {i+j}")
    a = pyposit.posit_model(2, (i, 32))
    b = pyposit.posit_model(2, (j, 32))
    c = a + b
    dut._log.info(f"A:          {a}  :  {a.to_float()}")
    dut._log.info(f"B:          {b}  :  {b.to_float()}")
    dut._log.info(f"C:          {c}  :  {c.to_float()}")


    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    one = BinaryValue(a.p_str) ## 1
    dut.a.value = one
    two = BinaryValue(b.p_str) ## 1
    dut.b.value = two

    # get results into dc reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)

    dut._log.info(f"First Pulse:")

    dut._log.info(f"a decode:")
    dut._log.info(f"Posit : {dut.m_p32b_adder.a_decode.posit_reduced.value}")
    dut._log.info(f"LO    : {dut.m_p32b_adder.a_decode.leading_ones.value}")
    dut._log.info(f"LZ    : {dut.m_p32b_adder.a_decode.leading_zeroes.value}")
    dut._log.info(f"Rlen  : {dut.m_p32b_adder.a_decode.regime_len.value}")
    dut._log.info(f"nreg  : {dut.m_p32b_adder.a_decode.negative_regime.value}")
    dut._log.info(f"subreg: {dut.m_p32b_adder.a_decode.subbed_regime.value}")
    dut._log.info(f"R     : {dut.m_p32b_adder.a_decode.regime.value}")

    dut._log.info(f"Zmask : {dut.m_p32b_adder.a_decode.zero_mask.value}")
    dut._log.info(f"Omask : {dut.m_p32b_adder.a_decode.one_mask.value}")
    dut._log.info(f"Rmask : {dut.m_p32b_adder.a_decode.r_mask.value}")
    dut._log.info(f"~Rmask: {dut.m_p32b_adder.a_decode.r_unmask.value}")
    
    dut._log.info(f"N Mask: {dut.m_p32b_adder.a_decode.nought_mask.value}")
    dut._log.info(f"N 'ed : {dut.m_p32b_adder.a_decode.nought_masked.value}")
    dut._log.info("")
    dut._log.info(f"E Mask: {dut.m_p32b_adder.a_decode.exp_mask.value}")
    dut._log.info(f"E 'ed': {dut.m_p32b_adder.a_decode.exp_masked.value}")
    dut._log.info(f"E LSB : {dut.m_p32b_adder.a_decode.exp_LSB_bit.value}")
    dut._log.info(f"E     : {dut.m_p32b_adder.a_decode.exponent.value}")
    dut._log.info("")
    dut._log.info(f"F Mask: {dut.m_p32b_adder.a_decode.frac_mask.value}")#
    dut._log.info(f"F 'ed': {dut.m_p32b_adder.a_decode.frac_masked.value}")
    dut._log.info(f"F MSB : {dut.m_p32b_adder.a_decode.frac_MSB_bit.value}")
    dut._log.info(f"F     : {dut.m_p32b_adder.a_decode.mantissa.value}")

    dut._log.info(f"")
    dut._log.info(f"b decode:")
    dut._log.info(f"Posit : {dut.m_p32b_adder.b_decode.posit_reduced.value}")
    dut._log.info(f"R Mask: {dut.m_p32b_adder.b_decode.r_mask.value}")
    dut._log.info(f"LO    : {dut.m_p32b_adder.b_decode.leading_ones.value}")
    dut._log.info(f"LZ    : {dut.m_p32b_adder.b_decode.leading_zeroes.value}")
    dut._log.info(f"Rlen  : {dut.m_p32b_adder.b_decode.regime_len.value}")
    dut._log.info(f"nreg  : {dut.m_p32b_adder.b_decode.negative_regime.value}")
    dut._log.info(f"subreg: {dut.m_p32b_adder.b_decode.subbed_regime.value}")
    dut._log.info(f"R     : {dut.m_p32b_adder.b_decode.regime.value}")
    dut._log.info(f"N Mask: {dut.m_p32b_adder.b_decode.nought_mask.value}")
    dut._log.info(f"N 'ed : {dut.m_p32b_adder.b_decode.nought_masked.value}")
    dut._log.info("")
    dut._log.info(f"E Mask: {dut.m_p32b_adder.b_decode.exp_mask.value}")
    dut._log.info(f"E 'ed': {dut.m_p32b_adder.b_decode.exp_masked.value}")
    dut._log.info(f"E LSB : {dut.m_p32b_adder.b_decode.exp_LSB_bit.value}")
    dut._log.info(f"E     : {dut.m_p32b_adder.b_decode.exponent.value}")
    dut._log.info("")
    dut._log.info(f"F Mask: {dut.m_p32b_adder.b_decode.frac_mask.value}")#
    dut._log.info(f"F 'ed': {dut.m_p32b_adder.b_decode.frac_masked.value}")
    dut._log.info(f"F MSB : {dut.m_p32b_adder.b_decode.frac_MSB_bit.value}")
    dut._log.info(f"F     : {dut.m_p32b_adder.b_decode.mantissa.value}")


    dut._log.info(f"a   : {dut.m_p32b_adder.a.value}")
    dut._log.info(f"a_s : {dut.m_p32b_adder.dc_a_sign.value}")
    dut._log.info(f"a_r : {dut.m_p32b_adder.dc_a_regime.value}")
    dut._log.info(f"a_e : {dut.m_p32b_adder.dc_a_exponent.value}")
    dut._log.info(f"a_m : {dut.m_p32b_adder.dc_a_mantissa.value}")
    dut._log.info("")
    dut._log.info(f"b   : {dut.m_p32b_adder.b.value}")
    dut._log.info(f"b_s : {dut.m_p32b_adder.dc_b_sign.value}")
    dut._log.info(f"b_r : {dut.m_p32b_adder.dc_b_regime.value}")
    dut._log.info(f"b_e : {dut.m_p32b_adder.dc_b_exponent.value}")
    dut._log.info(f"b_m : {dut.m_p32b_adder.dc_b_mantissa.value}")
    dut._log.info("")
    dut._log.info(f"BM  : {dut.m_p32b_adder.mant_add.big_mantissa.value}")
    dut._log.info(f"SM  : {dut.m_p32b_adder.mant_add.small_mantissa.value}")
    dut._log.info(f"a>? : {dut.m_p32b_adder.mant_add.m_comp.a.value}")
    dut._log.info("")
    dut._log.info(f"dlt_r:{dut.m_p32b_adder.mant_add.delta_regime.value}")
    dut._log.info(f"dlt_e:{dut.m_p32b_adder.mant_add.delta_exponent.value}")
    dut._log.info(f"I_R : {dut.m_p32b_adder.mant_add.interim_regime.value}")
    dut._log.info(f"I_E : {dut.m_p32b_adder.mant_add.interim_exponent.value}")
    dut._log.info(f"shamt:{dut.m_p32b_adder.mant_add.shamt.value}")
    dut._log.info(f"SMsh : {dut.m_p32b_adder.mant_add.small_mantissa_sh.value}")
    dut._log.info("")
    dut._log.info(f"signs:     {dut.m_p32b_adder.mant_add.big_sign.value} {dut.m_p32b_adder.mant_add.small_sign.value}")
    dut._log.info(f"big:   (0.) {dut.m_p32b_adder.mant_add.big_mantissa.value}")
    dut._log.info(f"small: (0.) {dut.m_p32b_adder.mant_add.small_mantissa_sh_alt.value}")
    dut._log.info(f"sum:   (0.){dut.m_p32b_adder.mant_add.s_mantissa_sum.value}")
    dut._log.info(f"ovf:   {dut.m_p32b_adder.mant_add.ovf.value}")
    dut._log.info(f"sumout (0.){dut.m_p32b_adder.mant_add.mantissa_sum.value}")
    dut._log.info(f"rout:  {dut.m_p32b_adder.mant_add.interim_regime.value}")
    dut._log.info(f"eout:  {dut.m_p32b_adder.mant_add.interim_exponent.value}")
    dut._log.info(f"mout:   (0.){dut.m_p32b_adder.mant_add.mantissa_sum.value}")

    dut._log.info("")

    # get results into cn reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut._log.info("")

    dut._log.info(f"Second Pulse:")

    dut._log.info("")
    dut._log.info(f"r:   {dut.m_p32b_adder.cn_interim_regime.value}")
    dut._log.info(f"e:   {dut.m_p32b_adder.cn_interim_exponent.value}")
    dut._log.info(f"sum: (0.){dut.m_p32b_adder.cn_mantissa_sum.value}")


    dut._log.info("")
    dut._log.info("Normalise Block")
    dut._log.info(f"msum_in:   {dut.m_p32b_adder.p_norm.mantissa_sum.value}")
    dut._log.info(f"regi_in:   {dut.m_p32b_adder.p_norm.interim_regime.value}")
    dut._log.info(f"expo_in:   {dut.m_p32b_adder.p_norm.interim_exponent.value}")
    dut._log.info(f"Normed_mantissa:   {dut.m_p32b_adder.p_norm.mantissa_lo.value}")
    dut._log.info(f"adj_exp:           {dut.m_p32b_adder.p_norm.a_exponent.value}")
    dut._log.info(f"- adj_exp:         {dut.m_p32b_adder.p_norm.b_exp_tc.value}")
    dut._log.info(f"toobig/toosmall:   {dut.m_p32b_adder.p_norm.dbg_exp_big.value}/{dut.m_p32b_adder.p_norm.dbg_exp_small.value}")


    dut._log.info("~")
    dut._log.info(f"shamt:     {dut.m_p32b_adder.p_norm.exp_adj_a.value}")
    dut._log.info(f"_shamt:    {dut.m_p32b_adder.p_norm.exp_adj_b.value}")

    dut._log.info(f"man_out:   {dut.m_p32b_adder.p_norm.mantissa.value}")
    dut._log.info(f"exp_out:   {dut.m_p32b_adder.p_norm.exponent.value}")
    dut._log.info(f"reg_out:   {dut.m_p32b_adder.p_norm.regime.value}")

    # get results into nd reg
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut._log.info("")

    dut._log.info(f"Third Pulse:")

    dut._log.info("")
    dut._log.info(f"r:     {dut.m_p32b_adder.p_encode.regime.value}")
    dut._log.info(f"e:     {dut.m_p32b_adder.p_encode.exponent.value}")
    dut._log.info(f"m: (0.){dut.m_p32b_adder.p_encode.mantissa.value}")
    dut._log.info("")
    dut._log.info(f"abs(r)      {dut.m_p32b_adder.p_encode.abs_regime.value}")
    dut._log.info(f"m_exp       {dut.m_p32b_adder.p_encode.expanded_mantissa.value}")
    dut._log.info("")
    dut._log.info(f"r_pair      {dut.m_p32b_adder.p_encode.rounding_pair.value}")
    dut._log.info(f"mantissa    {dut.m_p32b_adder.p_encode.interim_posit.value}")
    dut._log.info(f"exponent    {dut.m_p32b_adder.p_encode.shifted_exponent.value}")
    dut._log.info(f"rno_bit     {dut.m_p32b_adder.p_encode.regime_rno.value}")
    dut._log.info(f"regime_rej  {dut.m_p32b_adder.p_encode.regime_mask.value}")
    dut._log.info(f"posit_s     {dut.m_p32b_adder.p_encode.posit_signed.value}")
    
    dut._log.info("")
    dut._log.info("complete")


    await FallingEdge(dut.clk)

    r = pyposit.posit_model(2, str(dut.q.value))

    dut._log.info(f"EXPECT:     {c}  :  {c.to_float()}")
    if (dut.q.value == BinaryValue(c.p_str)):
        dut._log.info(f"RESULT:     {dut.q.value}  :  {r.to_float()}")
    else:
        dut._log.error(f"RESULT:     {dut.q.value}  :  {r.to_float()}")
    assert dut.q.value == BinaryValue(c.p_str) ## 2

    # end

@cocotb.test()
async def test_posit_32b_add_constrained_rand_int(dut):

    dut._log.warning(f"Test {__name__}.constrained_rand_int Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    # Test:
    for i in range(10):
        a =  random.randint(0, 1e9)
        b =  random.randint(0, 1e9)
        await test_ab(dut, a, b)

@cocotb.test()
async def test_posit_32b_add_constrained_rand(dut):

    dut._log.warning(f"Test {__name__}.constrained_rand_int Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    # Test:
    for i in range(10):
        a =  random.randint(0, 1e9)
        a = a/1e5
        b =  random.randint(0, 1e9)
        b = b/1e5
        await test_ab(dut, a, b)


@cocotb.test()
async def test_posit_32b_add_exact_positive(dut):

    dut._log.warning(f"Test {__name__}.add_exact_positive Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    await test_ab(dut, 1.0, 1.0)
    await test_ab(dut, 0.5, 1.0)
    await test_ab(dut, 8.0, 6.0)
    await test_ab(dut, 12.0, 12.0)
    await test_ab(dut, 64.0, 64.0)
    await test_ab(dut, 128.0, 128.0)

@cocotb.test()
async def test_posit_32b_add_rounded_positive(dut):

    dut._log.warning(f"Test {__name__}.rounded_positive Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    await test_ab(dut, 8.0, 1.5)
    await test_ab(dut, 16.0, 5.0)
    await test_ab(dut, 32.0, 12.0)


@cocotb.test()
async def test_posit_32b_add_exact_posneg(dut):

    dut._log.warning(f"Test {__name__}.exact_posneg Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    await test_ab(dut, 1.5, -1.0)
    await test_ab(dut, 8.0, -6.0)
    await test_ab(dut, 256.0, -128.0)
    await test_ab(dut, 1.0, -1.0)


@cocotb.test()
async def test_posit_32b_add_rounded_posneg(dut):

    dut._log.warning(f"Test {__name__}.rounded_posneg Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    await test_ab(dut, 10.0, -1.5)
    await test_ab(dut, 24.0, -5.0)
    await test_ab(dut, 48.0, -12.0)


@cocotb.test()
async def test_posit_32b_add_exact_negpos(dut):

    dut._log.warning(f"Test {__name__}.exact_negpos Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    await test_ab(dut, -1.5, 1.0)
    await test_ab(dut, -8.0, 6.0)
    await test_ab(dut, -256.0, 128.0)
    await test_ab(dut, -1.0, 1.0)


@cocotb.test()
async def test_posit_32b_add_rounded_negpos(dut):

    dut._log.warning(f"Test {__name__}.rounded_negpos Starting...")
    dut.a.value = 0
    dut.b.value = 0
    dut.rst.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))
    await RisingEdge(dut.clk)
    await FallingEdge(dut.clk)
    dut.rst.value = 1

    await test_ab(dut, -10.0, 1.5)
    await test_ab(dut, -24.0, 5.0)
    await test_ab(dut, -48.0, 12.0)












