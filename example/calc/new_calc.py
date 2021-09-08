"""
-----------------------------------------------------------------------------
Name: Lim Yan Peng, Gary
Student Number: A0189806M

To run, execute the following command:
python IE1_LIM_YAN_PENG_GARY.py

Description:
A simple calculator with variables that accepts prefix expressions.   

Examples of prefix notations:
= A 1           --> Assign value 1 to A
= A * 2 2       --> Assign value 2 * 2 = 4 to A
* - 5 2 3       --> (5-2)*3

To avoid ambiguity between subtraction and negative numbers,
any '-' joined to a number will be interpreted as a 
negative integer:
/ + -2 4 -4     --> (-2 + 4) / (-4)

-----------------------------------------------------------------------------
"""
import sys
sys.path.insert(0, "../..")

# Define reserve keywords (e.g. sqrt operator)
reserved = {
    'sqrt' : 'SQRT'
}

tokens = ['NAME', 'NUMBER'] + list(reserved.values())

literals = ['=', '+', '-', '*', '/']

# Tokens

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Check for reserve keywords 
    # (this is where sqrt gets registered as a SQRT token)
    if t.value in reserved:
        t.type = reserved.get(t.value)
    return t


def t_NUMBER(t):
    r'\-?\d+'

    # Numbers now contain an option - sign to denote negative numbers
    t.value = int(t.value)
    return t

t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing rules

# Ordered from lowest to highest precedence
# Omitted UMINUS to avoid ambiguity with subtract expressions:
# - expr expr
# - expr
precedence = (
    # ('right', 'UMINUS'),
    ('left', '+', '-'),
    ('left', '*', '/'),
)

# dictionary of names
names = {}

def p_statement_assign(p):
    'statement : "=" NAME expression'
    names[p[2]] = p[3]


def p_statement_expr(p):
    'statement : expression'
    print(p[1])

# For prefix expressions, the operator comes before the expressions
def p_expression_binop(p):
    '''expression : '+' expression expression
                  | '-' expression expression
                  | '*' expression expression
                  | '/' expression expression'''
    if p[1] == '+':
        p[0] = p[2] + p[3]
    elif p[1] == '-':
        p[0] = p[2] - p[3]
    elif p[1] == '*':
        p[0] = p[2] * p[3]
    elif p[1] == '/':
        p[0] = p[2] / p[3]


# Omitted UMINUS to avoid ambiguity with subtract expressions
# def p_expression_uminus(p):
#     "expression :  '-' expression %prec UMINUS"
#     p[0] = -p[2]


# Parenthesis not needed
# def p_expression_group(p):
#     "expression : '(' expression ')'"
#     p[0] = p[2]

def p_expression_sqrt(p):
    "expression : SQRT expression"
    # Print an error message if operand is negative
    if p[2] < 0:
        print("Cannot perform sqrt on negative number")
        return
    p[0] = (p[2])**0.5


def p_expression_number(p):
    "expression : NUMBER"
    p[0] = p[1]


def p_expression_name(p):
    "expression : NAME"
    try:
        p[0] = names[p[1]]
    except LookupError:
        print("Undefined name '%s'" % p[1])
        p[0] = 0


def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
    else:
        print("Syntax error at EOF")

import ply.yacc as yacc
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s:
        continue
    yacc.parse(s)
