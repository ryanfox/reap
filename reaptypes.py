class Scope(dict):
    """Contain the variables in a scope"""

    def __init__(self, parent=None):
        super().__init__()
        self.scope = {}
        self.parent = parent

    def get(self, key, default=None):
        if key in self.scope:
            return self.scope[key]
        elif self.parent:
            return self.parent.get(key, default)
        else:
            return default


class Evaluator(object):
    """Evaluates things."""
    def __init__(self, scope):
        self.globalscope = scope

    def eval(self, arg, scope=None):
        if scope is None:
            scope = self.globalscope

        if isinstance(arg, list):
            for argument in arg[:-1]:
                self.eval(argument, scope)
            return self.eval(arg[-1], scope)

        elif isinstance(arg, int):
            return arg

        elif arg in scope:
            return self.eval(scope[arg], scope)

        elif isinstance(arg, FunctionCallExpr):
            function = scope[arg.function]
            function.scope.parent = scope

            if len(arg.args) != len(function.params):
                raise TypeError('{} takes {} args, received {}'.format(function.name, len(function.params), len(arg.args)))
            params = {key: self.eval(val) for key, val in zip(function.params, arg.args)}
            function.scope.update(params)
            return self.eval(function.body, function.scope)

        elif isinstance(arg, Procedure):
            scope[arg.name] = arg
            return arg

        elif isinstance(arg, AddExpr):
            return self.eval(arg.left, scope) + self.eval(arg.right, scope)

        elif isinstance(arg, SubtractExpr):
            return self.eval(arg.left, scope) - self.eval(arg.right, scope)

        elif isinstance(arg, MultiplyExpr):
            return self.eval(arg.left, scope) * self.eval(arg.right, scope)

        elif isinstance(arg, DivideExpr):
            return self.eval(arg.left, scope) / self.eval(arg.right, scope)

        elif isinstance(arg, AssignStmt):
            scope[arg.left] = self.eval(arg.right, scope)
            return scope[arg.left]

        else:
            raise TypeError('unrecognized type: ' + type(arg))


class Procedure(object):
    """A function that can have side effects"""
    def __init__(self, name, params, body):
        self.name = name
        self.params = params
        self.body = body
        self.scope = Scope()


class Function(Procedure):
    """A 'pure' function.  That is, one without any side effects.  Not implemented yet"""
    pass


class FunctionCallExpr(object):
    """An expression containing a function call.  E.g. foo()"""
    def __init__(self, function, *args):
        self.function = function
        self.args = args


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


class AssignStmt(BinaryExpr):
    """An assignment expression.  E.g. x = 10"""
    pass

