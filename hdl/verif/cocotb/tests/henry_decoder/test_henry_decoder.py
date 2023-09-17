import pytest
from coco_wrapper import cocotb_test_wrapper

src_dirs = [
    'decode/henry_decoder'
]

def test_priority_encoder():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_regime_16',
        test_search_path='priority_encoder'
    )

def test_count_regime():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='posit32_count_regime',
        test_search_path='count_regime'
    )
