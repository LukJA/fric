from coco_wrapper import TestWrapper

def test_dff():
    TestWrapper(
        src='dff',
        toplevel='dff'
    ).test('.')
