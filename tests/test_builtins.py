from aytf.machine import Machine
from io import StringIO


class TestBuiltins:
    def setup_method(self):
        self.machine = Machine()

    def test_dup(self):
        with StringIO("2 3 DUP") as s:
            assert self.machine.run(s) == [2, 3, 3]
