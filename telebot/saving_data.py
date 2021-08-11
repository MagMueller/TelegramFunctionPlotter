import pickle
from sympy import parse_expr

def saving_last_function(function,message_id_as_str):
    dir_of_last_functions = eval(pickle.load(open("temp/last_functions.dat","rb")))
    dir_of_last_functions[message_id_as_str]=function
    pickle.dump(str(dir_of_last_functions),open("temp/last_functions.dat","wb"))

    
def getting_buffer():
    try:
        erg= eval(pickle.load(open("temp/buffer.dat","rb")))
        return [erg[0],parse_expr(erg[1])]
    except:
        return [False, "Not a mathematical function"]