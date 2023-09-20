from coco_wrapper import cocotb_test_wrapper

def test_posit_adder():
    cocotb_test_wrapper(
        toplevel='posit_adder',
        test_search_path='posit_adder'
    )


def test_posit_7b_add():
    cocotb_test_wrapper(
        toplevel='posit_7b_add',
        test_search_path='posit_7b_add'
    )

def test_posit_32b_add():
    cocotb_test_wrapper(
        toplevel='posit_32b_add',
        test_search_path='posit_32b_add'
    )
