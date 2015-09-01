class Procedure(object):
    """A function that can have side effects"""
    def __init__(self, name, paramlist, statements, scope):
        self.name = name
        self.paramlist = paramlist
        self.statements = statements
        self.scope = scope

    def __call__(self, *args):
        params = {key: value for key, value in zip(self.paramlist, *args)}
        # figure out how to actually eval method here
        print('called function {}'.format(self.name))


class Function(Procedure):
    """A 'pure' function.  That is, one without any side effects"""
    def __init__(self, name, paramlist, statements):
        super().__init__(name, paramlist, statements, {})
