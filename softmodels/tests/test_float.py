"""Test accuracy when converting between posit and floating point."""

from pyposit import PyPosit
from util import cfg_71, pyposit_71_from_float

float_pos_test_vals = {
     3/16 : "0001110",
    3/128 : "0000101",
     16.0 : "0111000",
      0.0 : "0000000"
}

float_neg_test_vals = {
     -3/16 : "1110010",
    -3/128 : "1111011",
     -16.0 : "1001000",
      -0.0 : "0000000"
}

def test_from_float_exact_positive_71():
    for val, string in float_pos_test_vals.items():
        assert pyposit_71_from_float(val).value == string

def test_from_float_exact_negative_71():
    for val, string in float_pos_test_vals.items():
        assert pyposit_71_from_float(val).value == string

def test_to_float_exact_positive_71():
    x = PyPosit(cfg_71, '0'*7)

    for val, string in float_pos_test_vals.items():
        x.value = string
        assert x.float_approximation    == val
        assert x.float_approximation_2c == val
        assert pyposit_71_from_float(val).value == string

def test_to_float_exact_negative_71():
    x = PyPosit(cfg_71, '0'*7)

    for val, string in float_neg_test_vals.items():
        x.value = string
        assert x.float_approximation    == val
        assert x.float_approximation_2c == val
        assert pyposit_71_from_float(val).value == string

def test_fromto_float_exact_positive_71():
    for val in float_pos_test_vals:
        assert pyposit_71_from_float(val).float_approximation == val

def test_fromto_float_exact_negative_71():
    for val in float_neg_test_vals:
        assert pyposit_71_from_float(val).float_approximation == val