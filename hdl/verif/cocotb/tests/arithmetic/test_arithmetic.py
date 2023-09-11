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
        f"{RTL_TOP}/alu/two_comp.sv",
        f"{RTL_TOP}/alu/posit_32b_add.sv",
        f"{RTL_TOP}/alu/posit_32b_sub.sv",
        f"{RTL_TOP}/alu/posit_7b_add.sv",
        f"{RTL_TOP}/alu/posit_7b_sub.sv"
    ]
    + glob.glob(f"{RTL_TOP}/decode/luke_decoder/*.sv")
    + glob.glob(f"{RTL_TOP}/encode/*.sv")
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


def test_posit_7b_add():
    cocotb_test_module(
        src=SRC,

        toplevel="posit_7b_add",

        modulepath=f"{CWD}/posit_7b_add",
        modules=[
            "cocotb_test_posit_7b_add"
        ]
    )
