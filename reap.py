import ply.lex as lex
import ply.yacc as yacc

from reaptypes import Function, AddExpr, SubtractExpr, MultiplyExpr, DivideExpr, AssignStmt

reserved = {'function': 'FUNCTION'}
tokens = ['NAME', 'INT', 'FLOAT', 'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'COMMA', 'EQUALS',
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE'] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_COMMA = r','
t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'

# Ignored characters
t_ignore = ' \t'


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'NAME')  # Check for reserved words
    return t


def t_FLOAT(t):
    r'(\d+\.\d*)|(\.\d+)'
    try:
        t.value = float(t.value)
    except ValueError:
        print('Unable to parse float value: {}'.format(t.value))
    return t


def t_INT(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print('Integer value too large {}'.format(t.value))
        t.value = 0
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    print('Illegal character {}'.format(t.value[0]))
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE')
)

globalscope = {}


def p_statement_expression(t):
    """statement : expression"""
    t[0] = t[1]


def p_function_definition(t):
    """statement : FUNCTION NAME LPAREN params RPAREN fnbody"""
    globalscope[t[2]] = Function(t[2], t[4], t[6], globalscope)


def p_params(t):
    """params : bareparam endparams"""
    t[0] = [t[1]] + t[2]


def p_params_empty(t):
    """params : empty"""
    t[0] = []


def p_bare_param(t):
    """bareparam : NAME"""
    t[0] = t[1]


def p_end_params(t):
    """endparams : endparams endparam"""
    t[0] = t[1] + [t[2]]


def p_end_params_empty(t):
    """endparams : empty"""
    t[0] = []


def p_end_param(t):
    """endparam : COMMA bareparam"""
    t[0] = t[2]


def p_function_call(t):
    """expression : NAME LPAREN args RPAREN"""
    try:
        t[0] = globalscope[t[1]](*t[3])
    except KeyError:
        print('function not defined: {}'.format(t[1]))


def p_args(t):
    """args : barearg endargs"""
    t[0] = [t[1]] + t[2]


def p_args_empty(t):
    """args : empty"""
    t[0] = []


def p_bare_arg(t):
    """barearg : expression"""
    t[0] = t[1]


def p_end_args(t):
    """endargs : endargs endarg"""
    t[0] = t[1] + [t[2]]


def p_end_args_empty(t):
    """endargs : empty"""
    t[0] = []


def p_end_arg(t):
    """endarg : COMMA barearg"""
    t[0] = t[2]


def p_fnbody(t):
    """fnbody : LCURLY statements RCURLY"""
    t[0] = t[2]


def p_statements(t):
    """statements : statements statement"""
    t[0] = t[1] + [t[2]]


def p_statements_statement(t):
    """statements : statement"""
    t[0] = [t[1]]


def p_assignment(t):
    """statement : NAME EQUALS expression"""
    t[0] = AssignStmt(t[1], t[3])


def p_add(t):
    """expression : expression PLUS expression"""
    t[0] = AddExpr(left=t[1], right=t[3])


def p_subtract(t):
    """expression : expression MINUS expression"""
    t[0] = SubtractExpr(left=t[1], right=t[3])


def p_multiply(t):
    """expression : expression TIMES expression"""
    t[0] = MultiplyExpr(left=t[1], right=t[3])


def p_divide(t):
    """expression : expression DIVIDE expression"""
    t[0] = DivideExpr(left=t[1], right=t[3])


def p_number_expression(t):
    """expression : number"""
    t[0] = t[1]


def p_int(t):
    """number : INT"""
    t[0] = t[1]


def p_float(t):
    """number : FLOAT"""
    t[0] = t[1]


def p_name_expression(t):
    """expression : NAME"""
    t[0] = t[1]


def p_empty(p):
    """empty :"""
    pass


def p_error(t):
    print('Syntax error at \'{}\''.format(t.value))

parser = yacc.yacc()

while True:
    try:
        s = input('reap> ')
    except EOFError:
        break
    out = parser.parse(s)
    if out:
        print(out)
