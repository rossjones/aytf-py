from .stack import Stack
from .words import WORDS


class Machine:
    def __init__(self):
        self.reset()
        self.collector = None

    def set_collector(self, collector_func):
        """
        Some operations want to run until they encounter a paired
        word, such as comments. For this we hand a function to the
        machine that is able to collect input until
        """
        self.collector = collector_func

    def reset(self):
        self.stack = Stack()
        self.env = WORDS

    def run(self, source):
        # We need a mode that allows for collecting
        # words until a specific word
        for word in self._parse_source(source):
            self.parse_word(word)

        return self.stack

    def parse_word(self, word):
        if self.collector is not None:
            proceed = self.collector(word)
            if not proceed:
                self._call_func(word)
        else:
            self._call_func(word)

    def _call_func(self, word):
        f = self.env.get(word.upper())
        if f is None:
            try:
                value = int(word)
                self.stack.push(value)
            except ValueError:
                self.abort(f"Unknown word and not an integer: {word}")
        else:
            f.call(self, self.stack)

    def abort(self, reason):
        import sys

        print(f"Stopping because: {reason}")
        sys.exit(1)

    def _parse_source(self, source):
        line = source.readline()
        while line:
            yield from line.split(" ")
            line = source.readline()
