from .utils import batched
import pytest


def test_batched():
    sample = 'ABCDEFG'
    it = batched(sample, 3)
    assert next(it) == ('A', 'B', 'C')
    assert next(it) == ('D', 'E', 'F')
    assert next(it) == ('G',)

    with pytest.raises(StopIteration):
        next(it)
