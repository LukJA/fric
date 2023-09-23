from coco_wrapper import cocotb_test_wrapper

def test_decoder():
    cocotb_test_wrapper(
        src='decode/unified_decoder',
        toplevel='count_lead_bit',
        test_search_path='priority_encoder'
    )
