## tes_dff.py

import random
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.types import LogicArray
from cocotb.clock import Timer


@cocotb.test()
async def dff_test(dut):

    dut._log.info("Start")
    # set a, b val
    dut.a.value = 0
    dut.b.value = 0

    # 10ns system clock, start it low
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start(start_high=False))

    await RisingEdge(dut.clk)
    await ReadOnly() # wait for signals
    assert dut.q.value == 0

    await FallingEdge(dut.clk)
    dut.a.value = 1
    dut.b.value = 2

    await RisingEdge(dut.clk)
    await ReadOnly() # wait for signals
    assert dut.q.value == 3

    await FallingEdge(dut.clk)
    dut.a.value = 3
    dut.b.value = 4

    await RisingEdge(dut.clk)
    await ReadOnly() # wait for signals
    assert dut.q.value == 7

    await FallingEdge(dut.clk)
    dut.a.value = 5
    dut.b.value = 6

    await RisingEdge(dut.clk)
    await ReadOnly() # wait for signals
    assert dut.q.value == 11

    # end

