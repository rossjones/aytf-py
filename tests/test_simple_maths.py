from aytf.machine import Machine
from io import StringIO


class TestSimpleMaths:
    def setup_class(self):
        self.tests = {
            "2 3 +": [5],
            "2 3 -": [-1],
            "10 2 /": [5],
            "10 1 /": [10],
            "10 0 /": [0],
            "10 2 *": [20],
            "10 0 *": [0],
        }

    def test_each(self):
        self.machine = Machine()
        for script, expected in self.tests.items():
            self.machine.reset()
            with StringIO(script) as s:
                assert self.machine.run(s) == expected
