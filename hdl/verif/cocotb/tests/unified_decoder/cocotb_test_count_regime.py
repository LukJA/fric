import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

async def test_value(dut, bin_str):

    if bin_str[1] == '0' and '1' in bin_str:
        valid = 1
        expected = bin_str[0:].index('1')
    elif bin_str[1] == '1' and '0' in bin_str:
        valid = 1
        expected = bin_str[1:].index('0')
    else:
        valid = 0
        expected = 32
    dut.vec.value = BinaryValue(bin_str)

    await Timer(1, "ns")
    
    dut._log.info(f"Input: {bin_str}")

    dut._log.info(f"Valid: {dut.valid.value}")
    assert dut.valid.value == valid

    if valid:
        dut._log.info(f"Output: {dut.cnt.value} (should be {expected})")
        assert dut.cnt.value == expected

    dut._log.info("\n")
    

@cocotb.test()
async def test_count_regime(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    await test_value(dut, "00101000")
    await test_value(dut, "00001000")
    await test_value(dut, "00000000")
