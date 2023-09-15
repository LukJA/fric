"""Tests for the implementation accuracy of pyposit addition."""

from util import pyposit_71_from_float


#######################
## Utility Functions ##
#######################

def _test_addition(test_cases):
    for a_val, b_val, res, inv_cases in test_cases:
        a = pyposit_71_from_float(a_val)
        b = pyposit_71_from_float(b_val)
        c = a + b
        
        assert a.float_approximation == a_val
        assert b.float_approximation == b_val
        assert c.float_approximation == res

        for inv_res in inv_cases:
            assert c.float_approximation != inv_res


###########
## Tests ##
###########

def test_addition_exact_positive_71():
    _test_addition([
        #     a,     b,   a+b, any != cases
        (   1.0,   1.0,   2.0,        [3.0] ),
        (   0.5,   1.0,   1.5,           [] ),
        (   8.0,   6.0,  14.0,           [] ),
        (  12.0,  12.0,  24.0,           [] ),
        (  64.0,  64.0, 128.0,           [] ),
        ( 128.0, 128.0, 256.0,           [] )
    ])

def test_addition_rounding_positive_71():
    _test_addition([
        #     a,     b,    a+b, any != cases
        (   8.0,   1.5,   10.0,           [] ),
        (  16.0,   5.0,   24.0,           [] ),
        (  32.0,  12.0,   48.0,           [] ),
        (  48.0,  64.0,  128.0,           [] ),
        ( 256.0, 256.0, 1024.0,           [] ),
        (  32.0,   8.0,   48.0,           [] )
    ])

def test_addition_exact_posneg_71():
    _test_addition([
        #     a,      b,    a+b, any != cases
        (   1.5,   -1.0,    0.5,           [] ),
        (   8.0,   -6.0,    2.0,           [] ),
        ( 256.0, -128.0,  128.0,           [] ),
        (   1.0,   -1.0,    0.0,        [3.0] )
    ])

def test_addition_rounding_posneg_71():
    _test_addition([
        #     a,      b,    a+b, any != cases
        (  10.0,   -1.5,    8.0,           [] ),
        (  24.0,   -5.0,   16.0,           [] ),
        (  48.0,  -12.0,   32.0,           [] )
    ])


def test_addition_exact_negpos_71():
    _test_addition([
        #      a,      b,    a+b, any != cases
        (   -1.5,    1.0,   -0.5,           [] ),
        (   -8.0,    6.0,   -2.0,           [] ),
        ( -256.0,  128.0, -128.0,           [] ),
        (   -1.0,    1.0,    0.0,           [] )
    ])

def test_addition_rounding_negpos_71():
    _test_addition([
        #      a,      b,    a+b, any != cases
        (  -10.0,    1.5,   -8.0,           [] ),
        (  -24.0,    5.0,  -16.0,           [] ),
        (  -48.0,   12.0,  -32.0,           [] )
    ])

def test_addition_exact_negative_71():
    _test_addition([
        #      a,      b,    a+b, any != cases
        (   -1.0,   -1.0,   -2.0,        [3.0] ),
        (   -0.5,   -1.0,   -1.5,           [] ),
        (   -8.0,   -6.0,  -14.0,           [] ),
        (  -12.0,  -12.0,  -24.0,           [] ),
        (  -64.0,  -64.0, -128.0,           [] ),
        ( -128.0, -128.0, -256.0,           [] ),
    ])

def test_addition_rounding_negative_71():
    _test_addition([
        #      a,      b,    a+b, any != cases
        (   -8.0,   -1.5,  -10.0,           [] ),
        (  -16.0,   -5.0,  -24.0,           [] ),
        (  -32.0,  -12.0,  -48.0,           [] )
    ])


