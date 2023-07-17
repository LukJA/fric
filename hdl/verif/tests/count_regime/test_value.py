from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

async def test_value(dut, bin_str):
    dut.i.value = BinaryValue(bin_str)

    await Timer(100, "ns")
    
    dut._log.info(f"Input: {bin_str}")

    if '1' in bin_str:
        dut._log.info(f"Output: {dut.c.value} (should be {bin_str.index('1')})")
    dut._log.info(f" Valid: {dut.valid.value}\n")

    if '1' in bin_str:
        assert dut.valid.value == 1
        assert dut.c.value == bin_str.index('1')
    else:
        assert dut.valid.value == 0
