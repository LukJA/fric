from coco_wrapper import cocotb_test_wrapper

def test_posit_adder():
    cocotb_test_wrapper( toplevel='posit_adder' ).test('posit_adder')


def test_posit_7b_add():
    cocotb_test_wrapper( toplevel='posit_7b_add' ).test('posit_7b_add')

def test_posit_32b_add():
    cocotb_test_wrapper( toplevel='posit_32b_add' ).test('posit_32b_add')
