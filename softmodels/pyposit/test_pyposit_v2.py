from pyposit_v2 import posit_model as posit

## Tests for the implementation accuracy of the pyposit base class

## functional tests
def test_from_float_exact_positive_71():
    x = posit(1, "0000000")

    x.from_float(3/16, 7, 1)
    assert x.p_str == "0001110"
    x.from_float(3/128, 7, 1)
    assert x.p_str == "0000101"
    x.from_float(16.0, 7, 1)
    assert x.p_str == "0111000"
    x.from_float(0, 7, 1)
    assert x.p_str == "0000000"

def test_from_float_exact_negative_71():
    x = posit(1, "0000000")

    x.from_float(-3/16, 7, 1)
    assert x.p_str == "1110010"
    x.from_float(-3/128, 7, 1)
    assert x.p_str == "1111011"
    x.from_float(-16.0, 7, 1)
    assert x.p_str == "1001000"
    x.from_float(-0, 7, 1)
    assert x.p_str == "0000000"

def test_fromto_float_exact_positive_71():

    x = posit(1, (3/16, 7))
    assert x.to_float() == 3/16
    x = posit(1, (3/128, 7))
    assert x.to_float() == 3/128
    x = posit(1, (16, 7))
    assert x.to_float() == 16
    x = posit(1, (0, 7))
    assert x.to_float() == 0

def test_fromto_float_exact_negative_71():

    x = posit(1, (-3/16, 7))
    assert x.to_float() == -3/16
    x = posit(1, (-3/128, 7))
    assert x.to_float() == -3/128
    x = posit(1, (-16, 7))
    assert x.to_float() == -16
    x = posit(1, (-0, 7))
    assert x.to_float() == 0


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

def test_addition_exact_positive_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(1.0, 7, 1)
    b.from_float(1.0, 7, 1)
    assert (a+b).to_float() == 2.0
    assert a.to_float() == 1
    assert b.to_float() == 1

    a.from_float(0.5, 7, 1)
    b.from_float(1.0, 7, 1)
    assert (a+b).to_float() == 1.5
    assert a.to_float() == 0.5
    assert b.to_float() == 1

    a.from_float(8.0, 7, 1)
    b.from_float(6.0, 7, 1)
    assert (a+b).to_float() == 14.0
    assert a.to_float() == 8
    assert b.to_float() == 6

    a.from_float(12.0, 7, 1) 
    b.from_float(12.0, 7, 1)
    assert (a+b).to_float() == 24.0
    assert a.to_float() == 12
    assert b.to_float() == 12

    a.from_float(64.0, 7, 1)
    b.from_float(64.0, 7, 1)
    assert (a+b).to_float() == 128
    assert a.to_float() == 64
    assert b.to_float() == 64

    a.from_float(128.0, 7, 1)
    b.from_float(128.0, 7, 1)
    assert (a+b).to_float() == 256
    assert a.to_float() == 128
    assert b.to_float() == 128

def test_addition_rounding_positive_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(8.0, 7, 1)
    b.from_float(1.5, 7, 1)
    assert (a+b).to_float() == 10
    assert a.to_float() == 8
    assert b.to_float() == 1.5

    a.from_float(16, 7, 1)
    b.from_float(5.0, 7, 1)
    assert (a+b).to_float() == 24
    assert a.to_float() == 16
    assert b.to_float() == 5

    a.from_float(32, 7, 1)
    b.from_float(12.0, 7, 1)
    assert (a+b).to_float() == 48
    assert a.to_float() == 32
    assert b.to_float() == 12

def test_addition_exact_posneg_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(1.5, 7, 1)
    b.from_float(-1.0, 7, 1)
    assert (a+b).to_float() == 0.5
    assert a.to_float() == 1.5
    assert b.to_float() == -1.0

    a.from_float(8.0, 7, 1)
    b.from_float(-6.0, 7, 1)
    assert (a+b).to_float() == 2.0
    assert a.to_float() == 8
    assert b.to_float() == -6

    a.from_float(256.0, 7, 1)
    b.from_float(-128.0, 7, 1)
    assert (a+b).to_float() == 128
    assert a.to_float() == 256
    assert b.to_float() == -128

    a.from_float(1.0, 7, 1)
    b.from_float(-1.0, 7, 1)
    assert (a+b).to_float() == 0.0
    assert (a+b).to_float() != 3.0

def test_addition_rounding_posneg_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(10.0, 7, 1)
    b.from_float(-1.5, 7, 1)
    assert (a+b).to_float() == 8

    a.from_float(24, 7, 1)
    b.from_float(-5.0, 7, 1)
    assert (a+b).to_float() == 16

    a.from_float(48, 7, 1)
    b.from_float(-12.0, 7, 1)
    assert (a+b).to_float() == 32


def test_addition_exact_negpos_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(-1.5, 7, 1)
    b.from_float(1.0, 7, 1)
    assert (a+b).to_float() == -0.5

    a.from_float(-8.0, 7, 1)
    b.from_float(6.0, 7, 1)
    assert (a+b).to_float() == -2.0

    a.from_float(-256.0, 7, 1)
    b.from_float(128.0, 7, 1)
    assert (a+b).to_float() == -128

    a.from_float(-1.0, 7, 1)
    b.from_float(1.0, 7, 1)
    assert (a+b).to_float() == 0.0

def test_addition_rounding_negpos_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(-10.0, 7, 1)
    b.from_float(1.5, 7, 1)
    assert (a+b).to_float() == -8

    a.from_float(-24, 7, 1)
    b.from_float(5.0, 7, 1)
    assert (a+b).to_float() == -16

    a.from_float(-48, 7, 1)
    b.from_float(12.0, 7, 1)
    assert (a+b).to_float() == -32

def test_addition_exact_negative_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(-1.0, 7, 1)
    b.from_float(-1.0, 7, 1)
    assert (a+b).to_float() == -2.0
    assert (a+b).to_float() != 3.0

    a.from_float(-0.5, 7, 1)
    b.from_float(-1.0, 7, 1)
    assert (a+b).to_float() == -1.5

    a.from_float(-8.0, 7, 1)
    b.from_float(-6.0, 7, 1)
    assert (a+b).to_float() == -14.0

    a.from_float(-12.0, 7, 1) 
    b.from_float(-12.0, 7, 1)
    assert (a+b).to_float() == -24.0

    a.from_float(-64.0, 7, 1)
    b.from_float(-64.0, 7, 1)
    assert (a+b).to_float() == -128

    a.from_float(-128.0, 7, 1)
    b.from_float(-128.0, 7, 1)
    assert (a+b).to_float() == -256

def test_addition_rounding_negative_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(-8.0, 7, 1)
    b.from_float(-1.5, 7, 1)
    assert (a+b).to_float() == -10

    a.from_float(-16, 7, 1)
    b.from_float(-5.0, 7, 1)
    assert (a+b).to_float() == -24

    a.from_float(-32, 7, 1)
    b.from_float(-12.0, 7, 1)
    assert (a+b).to_float() == -48

def test_subtraction_exact_positive_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(1.0, 7, 1)
    b.from_float(1.0, 7, 1)
    assert (a-b).to_float() == 0

    a.from_float(1.5, 7, 1)
    b.from_float(1.0, 7, 1)
    assert (a-b).to_float() == 0.5

    a.from_float(8.0, 7, 1)
    b.from_float(6.0, 7, 1)
    assert (a-b).to_float() == 2.0

    a.from_float(12.0, 7, 1) 
    b.from_float(10.0, 7, 1)
    assert (a-b).to_float() == 2.0

    a.from_float(64.0, 7, 1)
    b.from_float(16.0, 7, 1)
    assert (a-b).to_float() == 48

    a.from_float(256.0, 7, 1)
    b.from_float(128.0, 7, 1)
    assert (a-b).to_float() == 128

def test_subtraction_rounding_positive_71():
    a = posit(1, "0000000")
    b = posit(1, "0000000")

    a.from_float(10.0, 7, 1)
    b.from_float(1.5, 7, 1)
    assert (a-b).to_float() == 8

    a.from_float(24, 7, 1)
    b.from_float(5.0, 7, 1)
    assert (a-b).to_float() == 16

    a.from_float(32, 7, 1)
    b.from_float(10.0, 7, 1)
    assert (a-b).to_float() == 24






