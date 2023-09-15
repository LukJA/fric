import sys, os

try:
    import coco_wrapper.coco_wrapper
except ModuleNotFoundError:
    sys.exit("Error: incorrect configuration! "
             "Please run `source setup.sh` from verif/cocotb.")


CWD = os.path.dirname(os.path.realpath(__file__))

###############################################################################

def test_priority_encoder():
    coco_wrapper.cocotb_test_module(
        src=[
            f"{coco_wrapper.RTL_TOP}/typedef/posit_types.sv",
            f"{coco_wrapper.RTL_TOP}/decode/henry_decoder/util/mux.sv",
            f"{coco_wrapper.RTL_TOP}/decode/henry_decoder/util/priority_encoders.sv",
            f"{coco_wrapper.RTL_TOP}/decode/henry_decoder/posit32_count_regime.sv",
            f"{CWD}/priority_encoder/priority_encoder_16_tb.sv",
        ],

        toplevel="priority_encoder_16_tb",

        modulepath=f"{CWD}/priority_encoder",
        modules=[
            "cocotb_test_pe_16b"
        ]
    )

def test_count_regime():
    coco_wrapper.cocotb_test_module(
        src=[
            f"{coco_wrapper.RTL_TOP}/typedef/posit_types.sv",
            f"{coco_wrapper.RTL_TOP}/decode/henry_decoder/util/mux.sv",
            f"{coco_wrapper.RTL_TOP}/decode/henry_decoder/util/priority_encoders.sv",
            f"{coco_wrapper.RTL_TOP}/decode/henry_decoder/posit32_count_regime.sv",
            f"{CWD}/count_regime/posit32_count_regime_tb.sv",
        ],

        toplevel="posit32_count_regime_tb",

        modulepath=f"{CWD}/count_regime",
        modules=[
            "cocotb_test_count_regime"
        ]
    )
