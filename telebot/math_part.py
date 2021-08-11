from sympy import *

x, y, z = symbols('x y z')

def get_derivative(f, var=x):
    """This is basically just a wrapper function
    Input: sympy function
    Output: sympy function"""
    return f.diff(var)

def get_integral(f,var=x, borders=()):
    """This is also a wrapper function
    Input: sympy function
    Output: sympy function"""
    if f == parse_expr('0'): # Integration of the '0' funtion strangely did not work, so we just implemented it manually
        if len(borders)==2: # -> borders have been specified
            return borders[1]-borders[0]
        else:
            return 'x'
    if len(borders)==2:
        return integrate(f,(var,borders[0],borders[1]))
    else:
        return integrate(f,var)
