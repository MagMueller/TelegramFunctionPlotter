from sympy import *
from parsing_functions import *
import pickle
x, y, z = symbols('x y z')

    
def bool_function(message):
    """
    Input : telegram message
    Output: Bool
    This functions is a boolean functions for a telegram bot handler
    It is suppose to check wether one tried to specify a function (doesn't matter wether is is instantiated correclty or is a correct mathematical expression)
    """
    string = message.text
    if string[0]=="'": # If you start your message with an ' we interpret that as having tried to specified a function
        erg = ''
        if  string.find("'",2)!=-1: # If it is specified correctly
            erg= parse_function(string[1:string.find("'",2)]) # run parse_function
        else:
            erg = 'Function not correctly instantiated'
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb")) # save the data for later because then we don't have to run every parse function again
        return True
    else:
        return False
      
def bool_plot(message):
    """
    Input : telegram message
    Output: Bool
    This functions is a boolean functions for a telegram bot handler
    It is suppose to check wether one tried to specify a function for plotting (doesn't matter wether is is instantiated correclty or is a correct mathematical expression)
    """
    string = message.text
    erg = parse_plot(string)
    if type(erg)!= bool: # when parse_plot does not return False we know that atleast someone tried to plot a function
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb"))  # save the data for later because then we don't have to run every parse function again
        return True
    return False 


def bool_integrate(message):
    """
    Input : telegram message
    Output: Bool
    This functions is a boolean functions for a telegram bot handler
    It is suppose to check wether one tried to specify a function for integration (doesn't matter wether is is instantiated correclty or is a correct mathematical expression)
    """
    string = message.text
    erg=parse_integrate(string)
    if erg!= False: # when parse_integrate does not return False we know that atleast someone tried to plot a function
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb")) # save the data for later because then we don't have to run every parse function again
        return True
    else:
        return False


def bool_derivation(message):
    """
    Input : telegram message
    Output: Bool
    This functions is a boolean functions for a telegram bot handler
    It is suppose to check wether one tried to specify a function for derivation (doesn't matter wether is is instantiated correclty or is a correct mathematical expression)
    """
    string = message.text
    erg=parse_derivation(string)
    if erg!= False: # when parse_derivation does not return False we know that atleast someone tried to plot a function
        pickle.dump(str([(type(erg)!=str),str(erg)]),open("temp/buffer.dat","wb")) # save the data for later because then we don't have to run every parse function again
        return True
    else:
        return False


