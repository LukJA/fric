from coco_wrapper import TestWrapper

def test_priority_encoder():
    TestWrapper(
        src='decode/henry_decoder',
        toplevel='count_regime_16'
    ).test('priority_encoder')

def test_count_regime():
    TestWrapper(
        src='decode/henry_decoder',
        toplevel='posit32_count_regime'
    ).test('count_regime')
