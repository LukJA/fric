import cocotb
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

@cocotb.test()
async def count_trailing_ones(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    for i in range(0, 9):
        v = "0"*(8-i) + "1"*i
        dut._log.info(f"Input: {v}")
        vec = BinaryValue(v)
        dut.a.value = vec

        await Timer(100, "ns")
        dut._log.info(f"Output: {dut.q.value}")
        assert dut.q.value == i

    for i in range(0, 9):
        v = "1"*(7-i) + "0"*(i<8) + "1"*i
        dut._log.info(f"Input: {v}")
        vec = BinaryValue(v)
        dut.a.value = vec

        await Timer(100, "ns")
        dut._log.info(f"Output: {dut.q.value}")
        assert dut.q.value == i
