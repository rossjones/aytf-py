import pytest

from aytf.stack import Stack


class TestStack:
    def test_empty_stack_ops(self):
        with pytest.raises(IndexError):
            s = Stack()
            s.pop()
