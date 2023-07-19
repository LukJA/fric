import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue


async def test_pe_0(dut, n):
    bin_str = f"{n:02b}"
    dut.slice.value = BinaryValue(bin_str)

    await Timer(100, "ns")
    
    dut._log.info(f"Input: {bin_str}")
    dut._log.info(f"Output: {dut.count.value}")

    assert dut.valid.value == (1 if n > 0 else 0)
    assert dut.count.value == [2, 1, 0, 0][n]

async def test_pe_1(dut, n):
    bin_str = f"{n:02b}"
    dut.slice.value = BinaryValue(bin_str)

    await Timer(100, "ns")
    
    dut._log.info(f"Input: {bin_str}")
    dut._log.info(f"Output: {dut.count.value}")

    assert dut.valid.value == (1 if n != 3 else 0)
    assert dut.count.value == [0, 0, 1, 2][n]

@cocotb.test()
async def test_pe_2(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    dut.leading_bit.value = 0

    for i in range(0, 4):
        await test_pe_0(dut, i)

    dut.leading_bit.value = 1

    for i in range(0, 4):
        await test_pe_1(dut, i)

