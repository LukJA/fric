from coco_wrapper import cocotb_test_wrapper

src_dirs = [
    'decode/luke_decoder',
    'alu'
]

def test_clo():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_lead_one',
        test_search_path='clo'
    )

def test_clo_24():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_lead_one_24',
        test_search_path='count_lead_one_24'
    )

def test_clz():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_lead_zero',
        test_search_path='clz'
    )

def test_cto():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_tail_one',
        test_search_path='cto'
    )

def test_ctz():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='count_tail_zero',
        test_search_path='ctz'
    )

def test_decoder():
    cocotb_test_wrapper(
        src=src_dirs,
        toplevel='format_decoder',
        test_search_path='decoder'
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
