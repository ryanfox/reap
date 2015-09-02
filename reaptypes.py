class Procedure(object):
    """A function that can have side effects"""
    def __init__(self, name, statement):
        self.name = name
        self.statement = statement

    def __call__(self, *args):
        return self.statement.eval()


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
    def eval(self):
        return self.left.eval() + self.right.eval()


class SubtractExpr(BinaryExpr):
    """A subtract expression.  Returns the difference between two things."""
    def eval(self):
        return self.left.eval() - self.right.eval()


class MultiplyExpr(BinaryExpr):
    """A multiply expression.  Returns the product of two things."""
    def eval(self):
        return self.left.eval() * self.right.eval()


class DivideExpr(BinaryExpr):
    """A division expression.  Returns the quotient between two things."""
    def eval(self):
        return self.left.eval() / self.right.eval()


class Variable(object):
    """A variable.  Has a name.  Stores a value"""
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Int(object):
    """An integer.  What do you want from me"""
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value