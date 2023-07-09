import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, ReadOnly
from cocotb.triggers import Timer
from cocotb.binary import BinaryValue

def first_ones(s: str, n: int = 2):
    i = 0
    p = ""
    for q in range(0, len(s)):
        if s[q] == "1":
            i += 1
        if i <= n:
            p += s[q]
        else:
            p += "0"
    return p


@cocotb.test()
async def test_count_leading_ones(dut):
    dut._log.warning(f"Test {__name__} Starting...")

    for i in range(0, 9):
        v = "0"*i + "1"*(8-i)
        x = first_ones(v)
        dut._log.info(f"{i}: Input : {v}")
        dut._log.info(f"{i}: Target: {x}")
        vec = BinaryValue(v)
        dut.a.value = vec

        await Timer(100, "ns")
        dut._log.info(f"{i}:    Output: {dut.q.value}")
        assert dut.q.value == BinaryValue(x)





