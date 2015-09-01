import ply.lex as lex
import ply.yacc as yacc

from functions import Function, Procedure


reserved = {'function': 'FUNCTION'}
tokens = ['NAME', 'NUMBER', 'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY', 'EQUALS'] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_EQUALS = r'='

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

names = {}


def p_function_definition(t):
    """statement : FUNCTION NAME paramlist fnbody"""
    names[t[2]] = Function(t[2], t[3], t[4])


def p_function_call(t):
    """expression : NAME paramlist"""
    try:
        names[t[1]](t[2])
    except KeyError:
        print('function not defined: {}'.format(t[1]))


def p_params(t):
    """paramlist : LPAREN params RPAREN"""
    t[0] = t[2]


def p_paramlist(t):
    """params : params param"""
    t[0] = t[1] + [t[2]]


def p_paramlist_empty(t):
    """params : empty"""
    t[0] = []


def p_param(t):
    """param : expression"""
    t[0] = t[1]


def p_fnbody(t):
    """fnbody : LCURLY statements RCURLY"""
    t[0] = t[2]


def p_statements(t):
    """statements : statements statement"""
    t[0] = t[1] + [t[2]]


def p_statement(t):
    """statements : statement"""
    t[0] = t[1]


def p_assignment(t):
    """statement : NAME EQUALS expression"""
    names[t[1]] = t[3]


def p_statement_expression(t):
    """statement : expression"""
    t[0] = t[1]


def p_number_expression(t):
    """expression : NUMBER"""
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
    parser.parse(s)
