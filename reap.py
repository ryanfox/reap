import ply.lex as lex
import ply.yacc as yacc

from reaptypes import Function, Variable, Int, AddExpr, SubtractExpr, MultiplyExpr, DivideExpr

reserved = {'function': 'FUNCTION'}
tokens = ['NAME', 'NUMBER', 'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'EQUALS',
          'PLUS', 'MINUS', 'TIMES', 'DIVIDE'] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
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


def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
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

names = {}


def p_statement_expression(t):
    """statement : expression"""
    print(t[1])
    t[0] = t[1]


def p_function_definition(t):
    """statement : FUNCTION NAME LPAREN RPAREN fnbody"""
    names[t[2]] = Function(t[2], t[5])


def p_function_call(t):
    """expression : NAME LPAREN RPAREN"""
    try:
        t[0] = names[t[1]]()
    except KeyError:
        print('function not defined: {}'.format(t[1]))


def p_fnbody(t):
    """fnbody : LCURLY statement RCURLY"""
    t[0] = t[2]


def p_assignment(t):
    """statement : NAME EQUALS expression"""
    t[0] = Variable(name=t[1], value=t[3])


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
    """expression : NUMBER"""
    t[0] = Int(t[1])


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
    parser.parse(s)
