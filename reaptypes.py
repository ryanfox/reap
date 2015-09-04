globalscope = {}


class Evaluator(object):
    """Evaluates things."""
    def eval(self, arg, scope=globalscope):
        if isinstance(arg, list):
            for argument in arg[:-1]:
                self.eval(argument, scope)
            return self.eval(arg[-1], scope)
        elif isinstance(arg, int):
            return arg
        elif arg in scope:
            return self.eval(scope[arg], scope)
        elif isinstance(arg, FunctionCallExpr):
            return scope[arg.function](*arg.args)
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

evaluator = Evaluator()


class Procedure(object):
    """A function that can have side effects"""
    def __init__(self, name, params, body, scope=globalscope):
        self.name = name
        self.params = params
        self.body = body
        self.scope = scope

    def __call__(self, *args):
        if len(args) != len(self.params):
            raise TypeError('{} takes {} args, received {}'.format(self.name, len(self.params), len(args)))
        localscope = self.scope.copy()
        params = {key: val for key, val in zip(self.params, args)}
        localscope.update(params)
        return evaluator.eval(self.body, localscope)


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

