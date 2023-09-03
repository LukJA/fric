import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

from pyposit.decode import count_regime

async def test_value(dut, bin_str):

    valid = (
        (bin_str[1] == '0' and '1' in bin_str) or
        (bin_str[1] == '1' and '0' in bin_str)
    )
        
    expected = count_regime(bin_str)
    dut.i.value = BinaryValue(bin_str)

    await Timer(1, "ns")
    
    dut._log.info(f"Input: {bin_str}")

    dut._log.info(f"Valid: {dut.valid.value}")
    assert dut.valid.value == valid

    if valid:
        dut._log.info(f"Output: {dut.c.value} (should be {expected})")
        assert dut.c.value == expected

    dut._log.info("\n")
    

@cocotb.test()
async def test_count_regime(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    await test_value(dut, "10001000100010001000100010001000")
    await test_value(dut, "00001000100010001000100010001000")
    await test_value(dut, "00000000100010001000100010001000")
    await test_value(dut, "00000000000000000000000000000000")
    await test_value(dut, "11001000100010001000100010001000")
    await test_value(dut, "11111111111111111111111111111111")
