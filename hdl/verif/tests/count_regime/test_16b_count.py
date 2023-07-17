import cocotb
from test_value import test_value

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
