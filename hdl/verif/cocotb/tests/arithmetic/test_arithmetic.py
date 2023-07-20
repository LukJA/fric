import sys, os
import glob

try:
    from cocotb_setup import *
except ModuleNotFoundError:
    sys.exit("Error: incorrect configuration! "
             "Please run `source setup.sh` from verif/cocotb.")
    

CWD = os.path.dirname(os.path.realpath(__file__))

###############################################################################

SRC = glob.glob(f"{RTL_TOP}/*.sv")

# move common.sv to start because importing is a pain
SRC.insert(0, SRC.pop(SRC.index(f"{RTL_TOP}/common.sv")))

def test_posit_adder():
    cocotb_test_module(
        src=SRC,

        toplevel="posit_adder",

        modulepath=f"{CWD}/posit_adder",
        modules=[
            "cocotb_test_posit_adder"
        ]
    )
