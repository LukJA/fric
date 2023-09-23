import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

async def test_value(dut, bin_str):

    valid = '1' in bin_str
    expected = bin_str.index('1') if valid else None

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
async def test_count_leading_ones(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    for i in range(9):
        v = "1"*i + "0"*(8-i)
        await test_value(dut, v)
