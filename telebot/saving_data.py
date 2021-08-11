import pickle
from sympy import parse_expr

def saving_last_function(function,message_id_as_str):
    """
    Input : telegram message, message_id_as_str
    Output: Nothing
    This function simply saves the function in a directory via pickle"""
    dir_of_last_functions = eval(pickle.load(open("temp/last_functions.dat","rb"))) # get the dir_of_last_functions
    dir_of_last_functions[message_id_as_str]=function # put in the value
    pickle.dump(str(dir_of_last_functions),open("temp/last_functions.dat","wb")) # save the changed diretory

    
def getting_buffer():
    """
    Input : Nothing
    Output: list of saved function from the buffer"""
    try:
        erg= eval(pickle.load(open("temp/buffer.dat","rb"))) # get the list
        return [erg[0],parse_expr(erg[1])] # return with parsed function
    except:
        return [False, "Not a correct mathematical function"] # if it Failed return failure Message