class Evaluator(object):
    """Evaluates things."""
    def eval(self, arg):
        if isinstance(arg, int):
            return arg
        elif isinstance(arg, Variable):
            return arg.value
        elif isinstance(arg, Procedure):
            return arg()
        elif isinstance(arg, AddExpr):
            return self.eval(arg.left) + self.eval(arg.right)
        elif isinstance(arg, SubtractExpr):
            return self.eval(arg.left) - self.eval(arg.right)
        elif isinstance(arg, MultiplyExpr):
            return self.eval(arg.left) * self.eval(arg.right)
        elif isinstance(arg, DivideExpr):
            return self.eval(arg.left) / self.eval(arg.right)
        else:
            raise TypeError('unrecognized type: ' + type(arg))

evaluator = Evaluator()


class Procedure(object):
    """A function that can have side effects"""
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body

    def __call__(self, *args):
        return evaluator.eval(self.body)


class Function(Procedure):
    """A 'pure' function.  That is, one without any side effects.  Not implemented yet"""
    pass


class BinaryExpr(object):
    """A binary expression.  Has a left and right side."""
    def __init__(self, left, right):
        self.left = left
        self.right = right


class AddExpr(BinaryExpr):
    """An add expression.  Adds two things together."""
    pass


class SubtractExpr(BinaryExpr):
    """A subtract expression.  Returns the difference between two things."""
    pass


class MultiplyExpr(BinaryExpr):
    """A multiply expression.  Returns the product of two things."""
    pass


class DivideExpr(BinaryExpr):
    """A division expression.  Returns the quotient between two things."""
    pass


class Variable(object):
    """A variable.  Has a name.  Stores a value"""
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __repr__(self):
        return self.value

    def __str__(self):
        return str(self.value)
