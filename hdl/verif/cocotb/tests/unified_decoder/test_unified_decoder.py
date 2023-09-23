from coco_wrapper import cocotb_test_wrapper


src_dirs = [ 'decode/unified_decoder', 'alu/two_comp.sv' ]


def test_clz():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_lead_zero',
        test_search_path='clz'
    )

def test_clo():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_lead_one',
        test_search_path='clo'
    )

def test_decoder():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='format_decoder',
        test_search_path='decode'
    )

def test_ffo():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='find_first_one',
        test_search_path='ffo'
    )
    
def test_ffno():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='find_first_n_ones',
        test_search_path='ffno'
    )
