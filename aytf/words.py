from enum import Enum

##### Collecting ops


def word_comment_start(machine, _stack):
    """ Tells the machine that until told otherwise all words
    should be sent to `comment_collector` """
    machine.set_collector(comment_collector)


def word_comment_end(machine, _stack):
    """ Disable the machine's collector """
    machine.set_collector(None)


def comment_collector(word):
    """
    Returns false when it encounters the end of comment character.
    This will trigger the normal processing of this word, which is
    to disable the collector.
    """
    return word != ")"


def word_compile_start(machine, _stack):
    Compiler.compiled_words = []
    machine.set_collector(compiler_collector)


def word_compile_end(machine, _stack):
    name, *cmds = Compiler.compiled_words
    machine.env[name.upper()] = CompiledFunc(" ".join(cmds))
    machine.set_collector(None)


def compiler_collector(word):
    if word != ";":
        Compiler.compiled_words.append(word)
    return word != ";"


class Compiler:
    class __Compiler:
        def __init__(self):
            self.compiled_words = []

        def __str__(self):
            return repr(self)

    instance = None

    def __init__(self):
        if not Compiler.instance:
            Compiler.instance = Compiler.__Compiler()

    def __getattr__(self, name):
        return getattr(self.instance, name)


##### Stack ops


def word_dup(_machine, stack):
    stack.push(stack.peek()[0])


##### Maths ops


def word_minus(_machine, stack):
    _invert_two_items_op(stack, lambda x, y: x - y)


def word_divide(_machine, stack):
    try:
        _invert_two_items_op(stack, lambda x, y: int(x / y))
    except ZeroDivisionError:
        # I have no idea which forth I saw div-by-zero pushing 0
        # onto the stack.  Seems wrong...
        stack.push(0)


def word_multiply(_machine, stack):
    _invert_two_items_op(stack, lambda x, y: x * y)


##### Private helpers functions


def _invert_two_items_op(stack, op):
    # For some ops we want the deeper item to be the leftmost
    # and the shallower to be the right. For instance
    # ( 2 3 - ) is 2-3, but popping from the stack [2 3]
    # will return 3 and the next pop will return 2. So we
    # swap them
    rt, lt = stack.pop(), stack.pop()
    stack.push(op(lt, rt))


class PyFunc:
    def __init__(self, f):
        self.f = f

    def call(self, machine, stack):
        self.f(machine, stack)


class CompiledFunc:
    def __init__(self, words):
        self.words = words

    def call(self, machine, stack):
        from io import StringIO

        machine.run(StringIO(self.words))


WORDS = {
    ".": PyFunc((lambda _, s: print(s.peek()[0]))),
    ".S": PyFunc((lambda _, s: print([i for i in s]))),
    "DUP": PyFunc(word_dup),
    # Math ops
    "+": PyFunc((lambda _, s: s.append(s.pop() + s.pop()))),
    "-": PyFunc(word_minus),
    "*": PyFunc(word_multiply),
    "/": PyFunc(word_divide),
    # Comments
    "(": PyFunc(word_comment_start),
    ")": PyFunc(word_comment_end),
    # Compiler
    ":": PyFunc(word_compile_start),
    ";": PyFunc(word_compile_end),
}
