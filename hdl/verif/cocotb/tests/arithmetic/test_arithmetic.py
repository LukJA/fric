import sys, os
import glob

try:
    import coco_wrapper.coco_wrapper
except ModuleNotFoundError:
    sys.exit("Error: incorrect configuration!")
    

CWD = os.path.dirname(os.path.realpath(__file__))

###############################################################################

SRC = (
    [
        f"{coco_wrapper.RTL_TOP}/typedef/common.sv",
        f"{coco_wrapper.RTL_TOP}/alu/comparator.sv",
        f"{coco_wrapper.RTL_TOP}/alu/two_comp.sv",
        f"{coco_wrapper.RTL_TOP}/alu/posit_32b_add.sv",
        f"{coco_wrapper.RTL_TOP}/alu/posit_32b_sub.sv",
        f"{coco_wrapper.RTL_TOP}/alu/posit_7b_add.sv",
        f"{coco_wrapper.RTL_TOP}/alu/posit_7b_sub.sv"
    ]
    + glob.glob(f"{coco_wrapper.RTL_TOP}/decode/luke_decoder/*.sv")
    + glob.glob(f"{coco_wrapper.RTL_TOP}/encode/*.sv")
    + glob.glob(f"{coco_wrapper.RTL_TOP}/alu/adder/*.sv")
)

def test_posit_adder():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="posit_adder",

        modulepath=f"{CWD}/posit_adder",
        modules=[
            "cocotb_test_posit_adder"
        ]
    )


def test_posit_7b_add():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="posit_7b_add",

        modulepath=f"{CWD}/posit_7b_add",
        modules=[
            "cocotb_test_posit_7b_add"
        ]
    )

def test_posit_32b_add():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="posit_32b_add",

        modulepath=f"{CWD}/posit_32b_add",
        modules=[
            "cocotb_test_posit_32b_add"
        ]
    )
