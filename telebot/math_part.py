from sympy import *

x, y, z = symbols('x y z')

def get_derivative(f, var=x):
    return f.diff(var)

def get_integral(f,var=x, borders=()):
    if f == parse_expr('0'):
        if len(borders)==2:
            return borders[1]-borders[0]
        else:
            return 'x'
    if len(borders)==2:
        return str(integrate(f,(var,borders[0],borders[1])))
    else:
        return integrate(f,var)
