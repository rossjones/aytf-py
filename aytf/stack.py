class Stack(list):
    def push(self, item):
        self.append(item)

    def peek(self, n=1):
        return self[-1:]
