import os, sys
from cocotb.runner import get_runner

RTL_TOP = os.getenv("RTL_TOP")

# FIXME: these aren't currently included in the sim -- maybe buid_args?
COCOTB_HDL_TIMEUNIT = os.getenv("COCOTB_HDL_TIMEUNIT")
COCOTB_HDL_TIMEPRECISION = os.getenv("COCOTB_HDL_TIMEPREVISION")

TOPLEVEL_LANG = os.getenv("TOPLEVEL_LANG")
VERILOG_SOURCES = os.getenv("VERILOG_SOURCES", "").split(" ")

SIM = os.getenv("SIM")

if SIM is None:
    raise Exception("SIM undefined!")


def cocotb_test_module(src, toplevel, modulepath, modules):
    sys.path.append(modulepath)

    runner = get_runner(SIM)
    runner.build(
        verilog_sources=src,
        hdl_toplevel=toplevel,
        always=True,
    )

    runner.test(hdl_toplevel=toplevel, test_module=modules)

    sys.path.remove(modulepath)
