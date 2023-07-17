import cocotb
from test_value import test_value

async def test_32b(dut, bin_str):
    await test_value(dut, bin_str[1] + bin_str[1:])

@cocotb.test()
async def test_count_regime(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    # NOTE: these have an offset of 1 for the sign bit,
    #       so values computed aren't correct...

    await test_32b(dut, "10001000100010001000100010001000")
    await test_32b(dut, "00001000100010001000100010001000")
    await test_32b(dut, "00000000100010001000100010001000")
    await test_32b(dut, "00000000000000000000000000000000")
