from coco_wrapper import TestWrapper

def test_posit_adder():
    TestWrapper( toplevel='posit_adder' ).test('posit_adder')


def test_posit_7b_add():
    TestWrapper( toplevel='posit_7b_add' ).test('posit_7b_add')

def test_posit_32b_add():
    TestWrapper( toplevel='posit_32b_add' ).test('posit_32b_add')
