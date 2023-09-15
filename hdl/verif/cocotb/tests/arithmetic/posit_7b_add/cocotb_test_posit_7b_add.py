import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.types import LogicArray
from cocotb.clock import Timer
from cocotb.binary import BinaryValue

from pyposit.pyposit import PyPosit, PyPositConfig
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
    cfg_71 = PyPositConfig(n_bits=7, es=1)
    a = PyPosit.from_float(cfg_71, i)
    b = PyPosit.from_float(cfg_71, j)
    c = a + b

    dut._log.warning(f"Select a:{i} b:{j}")
    dut._log.info(f"A:          {a}  :  {a.float_approximation}")
    dut._log.info(f"B:          {b}  :  {b.float_approximation}")

    one = BinaryValue(a.value) ## 1
    dut.a.value = one
    two = BinaryValue(b.value) ## 1
    dut.b.value = two

    await propagate(dut)
    r = PyPosit(cfg_71, str(dut.q.value))

    dut._log.info(f"EXPECT:     {c}  :  {c.float_approximation}")
    if (dut.q.value == BinaryValue(c.value)):
        dut._log.info(f"RESULT:     {dut.q.value}  :  {r.float_approximation}")
    else:
        dut._log.error(f"RESULT:     {dut.q.value}  :  {r.float_approximation}")
    assert dut.q.value == BinaryValue(c.value) ## 2

# @cocotb.test()
# async def test_posit_7b_add_constrained_rand_int(dut):

#     dut._log.warning(f"Test {__name__}.constrained_rand_int Starting...")
#     dut.a.value = 0
#     dut.b.value = 0
#     dut.rst.value = 0

#     # 10ns system clock, start it low
#     clock = Clock(dut.clk, 10, units="ns")
#     cocotb.start_soon(clock.start(start_high=False))
#     await RisingEdge(dut.clk)
#     await FallingEdge(dut.clk)
#     dut.rst.value = 1

#     # Test:
#     for i in range(10):
#         a =  random.randint(0, 128)
#         b =  random.randint(0, 128)
#         await test_ab(dut, a, b)


@cocotb.test()
async def test_posit_7b_add_exact_positive(dut):

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
async def test_posit_7b_add_rounded_positive(dut):

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
async def test_posit_7b_add_exact_posneg(dut):

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
async def test_posit_7b_add_rounded_posneg(dut):

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
async def test_posit_7b_add_exact_negpos(dut):

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
async def test_posit_7b_add_rounded_negpos(dut):

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












