from pyposit import posit

## Tests for the implementation accuracy of the pyposit base class

## functional tests
def test_from_float_exact_positive_71():
    x = posit(1, "0000000")

    x.from_float(3/16, 7, 1)
    assert x.get_p_str() == "0001110"
    x.from_float(3/128, 7, 1)
    assert x.get_p_str() == "0000101"
    x.from_float(16.0, 7, 1)
    assert x.get_p_str() == "0111000"
    x.from_float(0, 7, 1)
    assert x.get_p_str() == "0000000"

## functional tests
def test_from_float_exact_negative_71():
    x = posit(1, "0000000")

    x.from_float(-3/16, 7, 1)
    assert x.get_p_str() == "1110010"
    x.from_float(-3/128, 7, 1)
    assert x.get_p_str() == "1111011"
    x.from_float(-16.0, 7, 1)
    assert x.get_p_str() == "1001000"
    x.from_float(-0, 7, 1)
    assert x.get_p_str() == "0000000"


def test_to_float_exact_positive_71():
    x = posit(1, "0000000")

    x.p_set(1, "0001110")
    assert x.to_float() == 3/16
    assert x.to_float_2c() == 3/16
    x.p_set(1, "0000101")
    assert x.to_float() == 3/128
    assert x.to_float_2c() == 3/128
    x.p_set(1, "0111000")
    assert x.to_float() == 16.0
    assert x.to_float_2c() == 16.0
    x.p_set(1, "0000000")
    assert x.to_float() == 0
    assert x.to_float_2c() == 0

def test_to_float_exact_negative_71():
    x = posit(1, "0000000")

    x.p_set(1, "1110010")
    assert x.to_float() == -3/16
    assert x.to_float_2c() == -3/16
    x.p_set(1, "1111011")
    assert x.to_float() == -3/128
    assert x.to_float_2c() == -3/128
    x.p_set(1, "1001000")
    assert x.to_float() == -16.0
    assert x.to_float_2c() == -16.0
    x.p_set(1, "0000000")
    assert x.to_float() == 0
    assert x.to_float_2c() == 0




