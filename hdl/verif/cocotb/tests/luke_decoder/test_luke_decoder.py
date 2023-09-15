import sys, os
import glob

try:
    import coco_wrapper.coco_wrapper
except ModuleNotFoundError:
    sys.exit("Error: incorrect configuration! "
             "Please run `source setup.sh` from verif/cocotb.")


CWD = os.path.dirname(os.path.realpath(__file__))

###############################################################################

SRC = (
    [
        f"{coco_wrapper.RTL_TOP}/typedef/common.sv",
        f"{coco_wrapper.RTL_TOP}/alu/comparator.sv",
        f"{coco_wrapper.RTL_TOP}/alu/two_comp.sv"
    ]
    + glob.glob(f"{coco_wrapper.RTL_TOP}/decode/luke_decoder/*.sv")
)

def test_dff():
    coco_wrapper.cocotb_test_module(
        src=[f"{coco_wrapper.RTL_TOP}/dff.sv"],

        toplevel="dff",

        modulepath=f"{CWD}/dff",
        modules=[
            "cocotb_test_dff"
        ]
    )

def test_clo():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="count_lead_one",

        modulepath=f"{CWD}/clo",
        modules=[
            "cocotb_test_clo"
        ]
    )

def test_clo_24():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="count_lead_one_24",

        modulepath=f"{CWD}/count_lead_one_24",
        modules=[
            "cocotb_test_count_lead_one_24"
        ]
    )

def test_clz():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="count_lead_zero",

        modulepath=f"{CWD}/clz",
        modules=[
            "cocotb_test_clz"
        ]
    )

def test_cto():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="count_tail_one",

        modulepath=f"{CWD}/cto",
        modules=[
            "cocotb_test_cto"
        ]
    )

def test_ctz():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="count_tail_zero",

        modulepath=f"{CWD}/ctz",
        modules=[
            "cocotb_test_ctz"
        ]
    )

def test_decoder():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="format_decoder",

        modulepath=f"{CWD}/decoder",
        modules=[
            "cocotb_test_decoder"
        ]
    )

def test_ffo():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="find_first_one",

        modulepath=f"{CWD}/ffo",
        modules=[
            "cocotb_test_ffo"
        ]
    )
    
def test_ffno():
    coco_wrapper.cocotb_test_module(
        src=SRC,

        toplevel="find_first_n_ones",

        modulepath=f"{CWD}/ffno",
        modules=[
            "cocotb_test_ffno"
        ]
    )
