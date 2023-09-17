from coco_wrapper import cocotb_test_wrapper

def test_priority_encoder():
    cocotb_test_wrapper(
        src='decode/henry_decoder',
        toplevel='count_regime_16'
    ).test('priority_encoder')

def test_count_regime():
    cocotb_test_wrapper(
        src='decode/henry_decoder',
        toplevel='posit32_count_regime'
    ).test('count_regime')
