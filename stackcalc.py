import sys
import readline
from ast import literal_eval
import math
class StackCalculator:
    class StackEmptyError(Exception):
        def __str__(self):
            return "StackEmptyError"

    class VariablePtr:
        def __init__(self, name, parent):
            self.parent = parent
            self.name = name
        def __repr__(self):
            return "$" + self.name
        @property
        def value(self):
            if self.name not in self.parent._vars.keys():
                raise ValueError("Attempt to dereference variable without assignment")
            return self.parent._vars[self.name]
        def set(self, value):
            self.parent._vars[self.name] = value

    class Block:
        def __init__(self, block_str, parent):
            self.block_str = block_str
            self.parent = parent

        def __repr__(self):
            return "(" + self.block_str + ")"

        def call(self):
            self.parent.evaluate(self.block_str)

    def __init__(self):
        self._stack = []
        self._vars = dict()

    def push(self, item):
        try:
            if type(item) == type(''):
                if item[0] == '$':
                    self._stack.append(StackCalculator.VariablePtr(item[1:],self))
                else:
                    self._stack.append(literal_eval(item))
            else:
                self._stack.append(item)
        except ValueError:
            if callable(getattr(self, "_operator_" + str(item))):
                getattr(self, "_operator_" + str(item))()

    def pop(self):
        if len(self._stack) > 0:
            if isinstance(self._stack[-1], StackCalculator.VariablePtr):
                return self._stack.pop().value
            return self._stack.pop()
        raise StackCalculator.StackEmptyError

    def peek(self):
        if len(self._stack) > 0:
            if isinstance(self._stack[-1], StackCalculator.VariablePtr):
                return self._stack[-1].value
            return self._stack[-1]
        raise StackCalculator.StackEmptyError

    def ptrpop(self):
        if len(self._stack) > 0:
            if isinstance(self._stack[-1], StackCalculator.VariablePtr):
                return self._stack.pop()
            raise TypeError("Item on top not a VariablePtr")
        raise StackCalculator.StackEmptyError

    def evaluate(self, str_in):
        self._restore = self._stack[:]
        for item in str_in.split():
            try:
                self.push(item)
            except Exception as e:
                sys.stderr.write("Error: {}\n".format(str(e)))
                self._stack = self._restore

    def interact(self):
        while 1:
            try:
                self.evaluate(input("> "))
            except EOFError:
                sys.stderr.write("bye\n")
                sys.exit(0)

    def _operator_bye(self):
        """exit"""
        sys.exit(0)

    def _operator_examine(self):
        """print the stack for examination"""
        print(self._stack)

    def _operator_peek(self):
        """print the top item on the stack"""
        print(self.peek())

    def _operator_pop(self):
        """delete the top item from the stack"""
        print(self.pop())

    def _operator_add(self):
        """add the top two items on the stack and push the result"""
        self.push(self.pop() + self.pop())

    def _operator_mul(self):
        """multiply the top two items on the stack and push the result"""
        self.push(self.pop() * self.pop())

    def _operator_neg(self):
        """negate the top item on the stack"""
        self.push(-self.pop())

    def _operator_flip(self):
        """flip the position of the top two items on the stack"""
        top = self.pop()
        self.push(self.pop())
        self.push(top)

    def _operator_abs(self):
        """push abs of top of stack"""
        self.push(abs(self.pop()))

    def _operator_invert(self):
        """push inverse (1/n) of top of stack"""
        self.push(1/self.pop())

    def _operator_inv(self):
        """alias for invert"""
        self._operator_invert()

    def _operator_pow(self):
        """raise the 2nd to top item on the stack to the power of the
           top item on the stack and push the result"""
        to = self.pop()
        self.push(self.pop()**to)

    def _operator_avg(self):
        """compute the average of the top two items on the stack and
           push the result"""
        self.push((self.pop()+self.pop())/2)

    def _operator_peeksum(self):
        """sum everything on the stack without popping and push the result"""
        self.push(sum(self._stack))

    def _operator_empty(self):
        """empty the stack"""
        self._stack = []

    def _operator_pi(self):
        """pushes pi to the stack"""
        self.push(math.pi)

    def _operator_e(self):
        """pushes e to the stack"""
        self.push(math.e)

    def _operator_sin(self):
        """calculate the sin of the top item in radians and push it to the stack"""
        self.push(math.sin(self.peek()))

    def _operator_cos(self):
        """calculate the cos of the top item in radians and push it to the stack"""
        self.push(math.cos(self.peek()))

    def _operator_tan(self):
        """calculate the tan of the top item in radians and push it to the stack"""
        self.push(math.tan(self.peek()))

    def _operator_torad(self):
        """convert the item on the top of the stack from a degrees value to radians"""
        self.push(math.radians(self.pop()))

    def _operator_todeg(self):
        """convert the item on the top of the stack from a radians value to degrees"""
        self.push(math.degrees(self.pop()))

    def _operator_set(self):
        """pop the var pointer on the second to top of the stack and set it to the
           value on the top of the stack"""
        value = self.pop()
        self.ptrpop().set(value)

    def _operator_equal(self):
        """pop the top two items from the stack, and push True to the stack if they are
           equal, False otherwise"""
        self.push(self.pop() == self.pop())

if __name__ == "__main__":
    calc = StackCalculator()
    calc.interact()
