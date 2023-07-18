import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

async def test_value(dut, bin_str):
    dut.i.value = BinaryValue(bin_str)

    await Timer(1, "ns")
    
    dut._log.info(f"Input: {bin_str}")

    if '1' in bin_str:
        dut._log.info(f"Output: {dut.c.value} (should be {bin_str.index('1')})")
    dut._log.info(f" Valid: {dut.valid.value}\n")

    if '1' in bin_str:
        assert dut.valid.value == 1
        assert dut.c.value == bin_str.index('1')
    else:
        assert dut.valid.value == 0

@cocotb.test()
async def test_16b_count(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    dut.leading_bit.value = 0

    # await test_value(dut, "1000100010001000")
    await test_value(dut, "0000100010001000")
    await test_value(dut, "0000000010001000")
    await test_value(dut, "0000000000000000")
    await test_value(dut, "0100000000000000")
    await test_value(dut, "1000000000000000")
    await test_value(dut, "0000000001000000")
    await test_value(dut, "0000000111100000")
    await test_value(dut, "0000111010100000")
    await test_value(dut, "0111100000000100")

    # assert False
