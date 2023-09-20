from coco_wrapper import cocotb_test_wrapper

def test_dff():
    cocotb_test_wrapper(
        src='dff',
        toplevel='dff'
    )
