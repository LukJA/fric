import os, sys
from cocotb.runner import get_runner

COCOTB_TOP = os.getenv("COCOTB_TOP")
RTL_TOP = os.getenv("RTL_TOP")

# FIXME: these aren't currently included in the sim -- maybe buid_args?
COCOTB_HDL_TIMEUNIT = os.getenv("COCOTB_HDL_TIMEUNIT")
COCOTB_HDL_TIMEPRECISION = os.getenv("COCOTB_HDL_TIMEPREVISION")

TOPLEVEL_LANG = os.getenv("TOPLEVEL_LANG")
VERILOG_SOURCES = os.getenv("VERILOG_SOURCES", "").split(" ")

SIM = os.getenv("SIM")

if SIM is None:
    print("Error: SIM undefined!", file=sys.stderr)
    sys.exit(1)

SIM_BUILD_ARGS=os.getenv("SIM_BUILD_ARGS", "").split(" ")

# FIXME: could we share runner per import to improve runtime?
#       i.e. call runner=get_runner(SIM) up here, then
#            just reference it within the function?

def cocotb_test_module(src, toplevel, modulepath, modules):
    sys.path.append(modulepath)

    subpath = modulepath.replace(f"{COCOTB_TOP}/tests/", "")

    runner = get_runner(SIM)
    runner.build(
        verilog_sources=src,
        hdl_toplevel=toplevel,
        always=True,
        build_args=SIM_BUILD_ARGS,
        build_dir=f"{COCOTB_TOP}/sim_build/{subpath}"
    )

    runner.test(hdl_toplevel=toplevel, test_module=modules)

    sys.path.remove(modulepath)
