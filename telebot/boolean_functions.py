from sympy import *

x, y, z = symbols('x y z')

def parse_function(eingabe):
    try: 
        kopie=eingabe
        if kopie.find("^")!=-1:
            kopie=kopie.replace('^','**')
        stop = True
        while(stop):
            for pos,letter in enumerate(kopie):
                if letter.isnumeric():
                    if pos!=0:
                        if kopie[pos-1]=='x' or kopie[pos-1]=='y' or kopie[pos-1]=='z':
                            kopie=kopie[:pos]+'*'+kopie[pos:]
                            break
                    if pos!=len(kopie)-1:
                        if kopie[pos+1]=='x' or kopie[pos+1]=='y' or kopie[pos+1]=='z':
                            kopie=kopie[:pos+1]+'*'+kopie[pos+1:]
                            break
            stop=False
        return parse_expr(kopie)
    except: 
        return 'Function not corretly formated'
    

def bool_plot(message):
    string = message.text
    return type(parse_plot(string))!= bool and type(parse_plot(string))!=str

def parse_plot(string):
    if string[0:5]=='plot ':
        first = string.find("'")
        second = string.find("'",first+1)
        if first!= -1 and second !=-1:
            return parse_function(string[first+1:second])
        else:
            return 'Function not correctly instantiated'
    return False


def false_plot(message):
    string = message.text
    return type(parse_plot(string))==str

def parse_integrate(string):
    if string[0:10]=='integrate ':
        if string.find('borders')==-1:
            first = 10
            second = string.find("'",first+1)
            if first!= -1 and second !=-1:
                return [parse_function(string[first+1:second])]
        else: 
            first = 10
            second = string.find("'",first+1)
            third = string.find("'",second+1)
            fourth = string.find("'",third+1)
            if first!= -1 and second !=-1 and third!=-1 and fourth!=1:
                border1=0
                border2=0
                try: 
                    border1=float(string[third+1:string.find(',')])
                    border2=float(string[string.find(',')+1:fourth])
                except:
                    return 'Borders are not in the correct format'
                if border2<border1:
                    return "Upper Burder can't have smaller value then lower"
                print(string[first+1:second])
                return [parse_function(string[first+1:second]),(border1,border2)]
    return False
            
def bool_integrate(message):
    string = message.text
    erg=parse_integrate(string)
    return type(erg)==list and erg[0]!='Error'

def false_integration(message):
    string = message.text
    erg=parse_integrate(string)
    return type(erg)!= bool and not(bool_integrate(message))

def parse_derivation(string):
    if string[0:9]=='derivate ':
            pos_var=string.find('var')
            if pos_var!=-1:
                first = 9
                second = string.find("'",first+1)
                if pos_var+2 < len(string):
                    if (string[pos_var+4]=='x' and string[first+1:second].find('x')!=-1) or (string[pos_var+4]=='y' and string[first+1:second].find('y')!=-1) or (string[pos_var+4]=='z' and string[first+1:second].find('z')!=-1): 
                        return [parse_function(string[first+1:second]),string[pos_var+4]]
                    else:
                        return "Wrong variable given"
                else:
                    return "No Variable given"
            else:
                first = 9
                second = string.find("'",first+1)
                return [parse_function(string[first+1:second])]
    return False


def bool_derivation(message):
    string = message.text
    erg=parse_derivation(string)
    return type(erg)==list and erg[0]!= 'Error'

def false_derivation(message):
    string = message.text
    erg=parse_derivation(string)
    return not(bool_derivation(message)) and type(erg)!=bool

def rest(message):
    return True