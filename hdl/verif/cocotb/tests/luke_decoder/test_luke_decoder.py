from coco_wrapper import TestWrapper

src_dirs = [
    'decode/luke_decoder',
    'alu'
]

def test_clo():
    TestWrapper(
        src=src_dirs,
        toplevel='count_lead_one'
    ).test('clo')

def test_clo_24():
    TestWrapper(
        src=src_dirs,
        toplevel='count_lead_one_24'
    ).test('count_lead_one_24')

def test_clz():
    TestWrapper(
        src=src_dirs,
        toplevel='count_lead_zero'
    ).test('clz')

def test_cto():
    TestWrapper(
        src=src_dirs,
        toplevel='count_tail_one'
    ).test('cto')

def test_ctz():
    TestWrapper(
        src=src_dirs,
        toplevel='count_tail_zero'
    ).test('ctz')

def test_decoder():
    TestWrapper(
        src=src_dirs,
        toplevel='format_decoder'
    ).test('decoder')

def test_ffo():
    TestWrapper(
        src=src_dirs,
        toplevel='find_first_one'
    ).test('ffo')
    
def test_ffno():
    TestWrapper(
        src=src_dirs,
        toplevel='find_first_n_ones'
    ).test('ffno')
