import sys, os

try:
    from cocotb_setup import *
except ModuleNotFoundError:
    sys.exit("Error: incorrect configuration! "
             "Please run `source setup.sh` from verif/cocotb.")


CWD = os.path.dirname(os.path.realpath(__file__))

###############################################################################

def test_priority_encoder():
    cocotb_test_module(
        src=[
            f"{RTL_TOP}/posit/posit_types.sv",
            f"{RTL_TOP}/decode/util/mux.sv",
            f"{RTL_TOP}/decode/util/priority_encoders.sv",
            f"{RTL_TOP}/decode/posit32_count_regime.sv"
        ],

        toplevel="count_regime_16",

        modulepath=f"{CWD}/priority_encoder",
        modules=[
            "cocotb_test_pe_16b"
        ]
    )

def test_count_regime():
    cocotb_test_module(
        src=[
            f"{RTL_TOP}/posit/posit_types.sv",
            f"{RTL_TOP}/decode/util/mux.sv",
            f"{RTL_TOP}/decode/util/priority_encoders.sv",
            f"{RTL_TOP}/decode/posit32_count_regime.sv"
        ],

        toplevel="posit32_regime_tb",

        modulepath=f"{CWD}/count_regime",
        modules=[
            "cocotb_test_count_regime"
        ]
    )
