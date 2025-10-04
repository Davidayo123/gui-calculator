
# tests/test_calc.py
import pytest
from calc import add, sub, mul, div, power, mod

def test_basic_ops():
    assert add(2, 3) == 5
    assert sub(5, 2) == 3
    assert mul(3, 4) == 12
    assert power(2, 3) == 8
    assert mod(10, 3) == 1

def test_division():
    assert div(8, 2) == 4
    with pytest.raises(ZeroDivisionError):
        div(1, 0)

def test_mod_zero():
    with pytest.raises(ZeroDivisionError):
        mod(5, 0)
