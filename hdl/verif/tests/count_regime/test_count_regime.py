import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

async def test_value(dut, bin_str):
    dut.i.value = BinaryValue(bin_str)

    await Timer(100, "ns")
    
    dut._log.info(f"Input: {bin_str}")
    dut._log.info(f"Output: {dut.c.value}")
    dut._log.info(f" Valid: {dut.valid.value}")

    # assert dut.c.value == bin_str[1:].index('1')

@cocotb.test()
async def test_count_regime(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    await test_value(dut, "10001000100010001000100010001000")
    await test_value(dut, "00001000100010001000100010001000")
    await test_value(dut, "00000000100010001000100010001000")
    await test_value(dut, "00000000000000000000000000000000")

    assert False
    

