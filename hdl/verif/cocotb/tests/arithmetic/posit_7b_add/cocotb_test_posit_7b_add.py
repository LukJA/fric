import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.types import LogicArray
from cocotb.clock import Timer
from cocotb.binary import BinaryValue

import pyposit_v2 as pyposit

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
    a = pyposit.posit_model(1, (i, 7))
    b = pyposit.posit_model(1, (j, 7))
    c = a + b
    dut._log.warning(f"Select a:{i} b:{j}")
    dut._log.info(f"A:          {a}  :  {a.to_float()}")
    dut._log.info(f"B:          {b}  :  {b.to_float()}")

    one = BinaryValue(a.p_str) ## 1
    dut.a.value = one
    two = BinaryValue(b.p_str) ## 1
    dut.b.value = two

    await propagate(dut)

    r = pyposit.posit_model(1, str(dut.q.value))
    dut._log.info(f"EXPECT:     {c}  :  {c.to_float()}")
    if (dut.q.value == BinaryValue(c.p_str)):
        dut._log.info(f"RESULT:     {dut.q.value}  :  {r.to_float()}")
    else:
        dut._log.error(f"RESULT:     {dut.q.value}  :  {r.to_float()}")
    assert dut.q.value == BinaryValue(c.p_str) ## 2

@cocotb.test()
async def test_posit_7b_add_exact_moderate(dut):

    dut._log.warning(f"Test {__name__} Starting...")
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
    for i in range(1, 5):
        for j in range(1, 5):
            await test_ab(dut, i, j)


