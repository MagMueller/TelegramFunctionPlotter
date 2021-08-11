from sympy import *
import pickle
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
    
def bool_function(message):
    string = message.text
    if string[0]=="'":
        erg = ''
        if  string.find("'",2)!=-1:
            erg= parse_function(string[1:string.find("'",2)])
        else:
            erg = 'Function not correctly instantiated'
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb"))
        return True
    else:
        return False
      
def function_command(message):
    string = message.text
    return string in ['derivate','plot','integrate']

def bool_plot(message):
    string = message.text
    erg = parse_plot(string)
    if type(erg)!= bool:
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb"))
        return True
    return False 

def parse_plot(string):
    if string[0:5]=='plot ':
        first = string.find("'")
        second = string.find("'",first+1)
        if first!= -1 and second !=-1:
            return parse_function(string[first+1:second])
        else:
            return 'Function not correctly instantiated'
    return False

def bool_integrate(message):
    string = message.text
    erg=parse_integrate(string)
    if erg!= False:
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb"))
        return True
    else:
        return False


def parse_integrate(string):
    if string[0:10]=='integrate ':
        if string.find('borders')==-1:
            first = string.find("'")
            second = string.find("'",first+1)
            if first!= -1 and second !=-1:
                return [parse_function(string[first+1:second])]
            else:
                return 'Function not correctly instantiated'
        else: 
            first = string.find("'")
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
                return [parse_function(string[first+1:second]),(border1,border2)]
            else: 
                return 'Function or borders are not correctly instantiated'      
    return False
            

def bool_derivation(message):
    string = message.text
    erg=parse_derivation(string)
    if erg!= False:
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb"))
        return True
    else:
        return False

def parse_derivation(string):
    if string[0:9]=='derivate ':
        first = string.find("'")
        second = string.find("'",first+1)
        if first!= -1 and second !=-1:
            pos_var=string.find('var')
            if pos_var!=-1:
                if pos_var+4 < len(string) and (string[pos_var+4]=='x' or string[pos_var+4]=='y' or string[pos_var+4]=='z'):
                    return [parse_function(string[first+1:second]),string[pos_var+4]]
                else:
                    return "No or wrong Variable given"
            else:
                return [parse_function(string[first+1:second])]
        else:
            return 'Function not correctly instantiated'
    return False


