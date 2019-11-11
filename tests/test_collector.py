from aytf.machine import Machine
from io import StringIO


class TestCollector:
    def setup_method(self):
        self.machine = Machine()

    def test_comment(self):
        with StringIO("( 1 2 3 4 ) 1") as s:
            assert self.machine.run(s) == [1]

    def test_compiler(self):
        # Should define a word called adder which adds one
        # to the item at the top of the stack, then puts 5
        # on the stack and calls ADDER to increment
        with StringIO(": adder 1 + ; 5 ADDER") as s:
            assert self.machine.run(s) == [6]
