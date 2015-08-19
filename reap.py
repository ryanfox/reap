import shlex

def tokenize(statement):
    return shlex.split(statement)

def reap_print(statement):
    print(statement)

def reap_eval(statement):
    tokens = tokenize(statement)

    if tokens[0].isdigit():
        return int(tokens[0])
    elif tokens[0] == '+':
        return int(reap_eval(tokens[1])) + int(reap_eval(tokens[2]))
    elif tokens[0] == '-':
        return int(tokens[1]) - int(tokens[2])
    elif tokens[0] == '*':
        return int(tokens[1]) * int(tokens[2])
    elif tokens[0] == '/':
        return int(tokens[1]) / int(tokens[2])
    else:
        return 'invalid syntax'

def reap_read():
    return raw_input('reap> ')

while True:
    reap_print(reap_eval(reap_read()))
