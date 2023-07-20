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

def test_dff():
    cocotb_test_module(
        src=SRC,

        toplevel="dff",

        modulepath=f"{CWD}/dff",
        modules=[
            "cocotb_test_dff"
        ]
    )

def test_clo():
    cocotb_test_module(
        src=SRC,

        toplevel="count_lead_one",

        modulepath=f"{CWD}/clo",
        modules=[
            "cocotb_test_clo"
        ]
    )

def test_clz():
    cocotb_test_module(
        src=SRC,

        toplevel="count_lead_zero",

        modulepath=f"{CWD}/clz",
        modules=[
            "cocotb_test_clz"
        ]
    )

def test_decoder():
    cocotb_test_module(
        src=SRC,

        toplevel="format_decoder",

        modulepath=f"{CWD}/decoder",
        modules=[
            "cocotb_test_decoder"
        ]
    )

def test_ffo():
    cocotb_test_module(
        src=SRC,

        toplevel="find_first_one",

        modulepath=f"{CWD}/ffo",
        modules=[
            "cocotb_test_ffo"
        ]
    )
    
def test_ffno():
    cocotb_test_module(
        src=SRC,

        toplevel="find_first_n_ones",

        modulepath=f"{CWD}/ffno",
        modules=[
            "cocotb_test_ffno"
        ]
    )
