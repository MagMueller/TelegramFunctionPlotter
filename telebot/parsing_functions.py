from sympy import *
x, y, z = symbols('x y z')


def parse_function(eingabe):
    """
    Input: string
    Output: sympy function or string if parsing failed
    
    This function tries to parse an incomming string to an sympy expr
    First we replace inputs like "x2" to "x*2" because sympy would interpret "x2" as an x with the specifier 2
    """
    try: 
        kopie=eingabe.replace('^','**') 
        stop = True
        while(stop): # This loop replaces  "x2" to "x*2" 
            for pos,letter in enumerate(kopie):
                if letter.isnumeric():
                    if pos!=0:
                        if kopie[pos-1] in ['x','y','z']: # if we find eg. an x next to a number we insert an *
                            kopie=kopie[:pos]+'*'+kopie[pos:]
                            break
                    if pos!=len(kopie)-1:
                        if kopie[pos+1] in ['x','y','z']:
                            kopie=kopie[:pos+1]+'*'+kopie[pos+1:]
                            break
            stop=False
        return parse_expr(kopie) # Then we use the sympy function parse_expr to transform the input to a sympy expr
    except: 
        return 'Function not corretly formated' # If it failed we return a failure message
    
def parse_plot(string):
    """
    Input: string
    Output: sympy function or string if parsing failed or False if we the string does'nt start with 'plot '
    """
    if string[0:5]=='plot ':
        first = string.find("'")
        second = string.find("'",first+1)
        if first!= -1 and second !=-1:
            return parse_function(string[first+1:second])
        else:
            return 'Function not correctly instantiated' # Error message when we miss a '
    return False


def parse_integrate(string):
    """
    Input: string
    Output: sympy function or string if parsing failed or False if we the string does'nt start with 'integrate '
    """
    if string[0:10]=='integrate ':
        if string.find('borders')==-1: # if borders weren't specified
            first = string.find("'")
            second = string.find("'",first+1)
            if first!= -1 and second !=-1: 
                erg = parse_function(string[first+1:second])
                if type(erg)==str:
                    return erg
                else:
                    return [erg] # if function correctly instantiated return parse_function
            else:
                return 'Function not correctly instantiated' # else return failure message
        else: # if borders are specified
            first = string.find("'")
            second = string.find("'",first+1)
            third = string.find("'",second+1)
            fourth = string.find("'",third+1)
            if first!= -1 and second !=-1 and third!=-1 and fourth!=1: # if function and borders are correctly instantiated
                border1=0
                border2=0
                try: 
                    border1=float(string[third+1:string.find(',')])
                    border2=float(string[string.find(',')+1:fourth])
                except:
                    return 'Borders are not in the correct format'
                if border2<border1: # If upper borders smaller the lower
                    return "Upper Burder can't have smaller value then lower" #return failure
                erg = parse_function(string[first+1:second])
                if type(erg)==str:
                    return erg
                else:
                    return [erg,(border1,border2)] #return the function and the borders as a list
            else: 
                return 'Function or borders are not correctly instantiated'  # Failure message
    return False


def parse_derivation(string):
    """
    Input: string
    Output: sympy function or string if parsing failed or False if we the string does'nt start with 'derivate '
    """
    if string[0:9]=='derivate ':
        first = string.find("'")
        second = string.find("'",first+1)
        if first!= -1 and second !=-1: # if function correctly instantiated 
            pos_var=string.find('var')
            if pos_var!=-1: # if variable is specified
                if pos_var+4 < len(string) and string[pos_var+4] in ['x','y','z']: # if variable is corectly specified
                    erg = parse_function(string[first+1:second])
                    if type(erg)==str:
                        return erg
                    else:
                        return [erg,string[pos_var+4]] # return functionm variabke as list
                else:
                    return "No or wrong Variable given" # return failure message
            else:
                erg = parse_function(string[first+1:second])
                if type(erg)==str:
                    return erg
                else:
                    return [erg] # return function as list
        else:
            return 'Function not correctly instantiated'# return failure message
    return False
