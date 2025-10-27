from hypothesis import given, strategies as st, settings
from math import pow

@given(st.integers())
def test_pow_method(x):
    square = pow(x, 2)
    assert square >= 0

def test_pow2_on_negative_input():
    square = pow(-3, 2)
    assert square == 9