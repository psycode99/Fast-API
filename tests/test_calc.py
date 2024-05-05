from app.calc import add
import pytest

@pytest.mark.parametrize("x, y, result", [(1,2,3), (2,2,4), (3,3,6)])
def test_add(x, y, result):
    sum = add(x, y)
    assert sum == result
