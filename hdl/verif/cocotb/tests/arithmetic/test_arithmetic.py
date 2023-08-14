import sys, os
import glob

try:
    from cocotb_setup import *
except ModuleNotFoundError:
    sys.exit("Error: incorrect configuration! "
             "Please run `source setup.sh` from verif/cocotb.")
    

CWD = os.path.dirname(os.path.realpath(__file__))

###############################################################################

SRC = (
    [
        f"{RTL_TOP}/typedef/common.sv",
        f"{RTL_TOP}/alu/comparator.sv",
        f"{RTL_TOP}/alu/two_comp.sv"
    ]
    + glob.glob(f"{RTL_TOP}/decode/luke_decoder/*.sv")
    + glob.glob(f"{RTL_TOP}/alu/adder/*.sv")
)

def test_posit_adder():
    cocotb_test_module(
        src=SRC,

        toplevel="posit_adder",

        modulepath=f"{CWD}/posit_adder",
        modules=[
            "cocotb_test_posit_adder"
        ]
    )
