from coco_wrapper import cocotb_test_wrapper

def test_priority_encoder():
    cocotb_test_wrapper(
        src='decode/henry_decoder',
        toplevel='count_regime_16',
        test_search_path='priority_encoder'
    )

def test_count_regime():
    cocotb_test_wrapper(
        src='decode/henry_decoder',
        toplevel='posit32_count_regime',
        test_search_path='count_regime'
    )
