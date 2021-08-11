import telebot
import matplotlib.pyplot as plt
import numpy as np
from boolean_functions import *
from plot import plot_func
from math_part import *
from saving_data import *
import pickle


API_KEY = "1913464534:AAGjZ9gC5KQmRiAjd-YWCAjhkKYGIpU6SBM"
bot = telebot.TeleBot(API_KEY)

def saving_last_function(function,message_id_as_str):
    dir_of_last_functions = eval(pickle.load(open("temp/last_functions.dat","rb")))
    dir_of_last_functions[message_id_as_str]=function
    pickle.dump(str(dir_of_last_functions),open("temp/last_functions.dat","wb"))


@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['bild'])
def bild(message):
    img = open('temp/test.png','rb')
    bot.send_photo(message.chat.id, img)

@bot.message_handler(func=bool_plot)
def plot(message):
    text=str(message.text)
    gespeichertes_erg = getting_buffer()
    if gespeichertes_erg[0]==False:
        bot.send_message(message.chat.id,gespeichertes_erg[1])
    else:
        Plot = plot_func(gespeichertes_erg[1])
        if Plot==True:
            img = open('temp/test.png','rb')
            bot.send_photo(message.chat.id, img)
        elif Plot == False:
            bot.send_message(message.chat.id,'There was an Error while plotting')
        else:
            bot.send_message(message.chat.id,Plot)




@bot.message_handler(func=bool_integrate)
def integrate(message):
    text=str(message.text)
    gespeichertes_erg = getting_buffer()
    if gespeichertes_erg[0]==False:
        bot.send_message(message.chat.id,gespeichertes_erg[1])
    else:
        erg = gespeichertes_erg[1]
        rückgabe=''
        if len(erg)==2:
            rückgabe= str((get_integral(erg[0],borders=erg[1])))
        elif len(erg)==1:
            if len(erg[0].atoms(Symbol))==0:
                rückgabe = str(erg[0])+'*x'
            else:
                rückgabe= str(get_integral(erg[0]))
        saving_last_function(rückgabe,str(message.chat.id))
        bot.send_message(message.chat.id, rückgabe.replace('**','^'))
      

@bot.message_handler(func=bool_derivation)
def derivate(message):
    text=str(message.text)
    gespeichertes_erg = getting_buffer()    
    if gespeichertes_erg[0]==False:
        bot.send_message(message.chat.id,gespeichertes_erg[1])
    else:
        erg = gespeichertes_erg[1]
        rückgabe=''
        if len(erg)==2:
            rückgabe= str(get_derivative(erg[0],var=erg[1]))
        elif len(erg)==1:
            rückgabe= str(get_derivative(erg[0]))
        saving_last_function(rückgabe,str(message.chat.id))
        bot.send_message(message.chat.id, rückgabe.replace('**','^'))
    
    

@bot.message_handler(commands=['help','dir','start'])
def help_message(message):
    with open('dir_of_commands.txt','r') as f:
        bot.send_message(message.chat.id, f.read())


@bot.message_handler(func=bool_function)
def set_function(message):
    gespeichertes_erg = getting_buffer()  
    if gespeichertes_erg[0]==False:
        bot.send_message(message.chat.id,gespeichertes_erg[1])
    else:
        function = str(gespeichertes_erg[1])
        dir_of_set_functions = eval(pickle.load(open("temp/set_functions.dat","rb")))
        dir_of_set_functions[str(message.chat.id)]= function
        pickle.dump(str(dir_of_set_functions),open("temp/set_functions.dat","wb"))
        bot.send_message(message.chat.id, 'The current function is now '+function.replace("**","^") +'\nYou can now plot, derivate or integrate it')
    
@bot.message_handler(func=function_command)
def use_saved_function(message):
    dir_of_set_functions = eval(pickle.load(open("temp/set_functions.dat","rb")))
    if str(message.chat.id) in dir_of_set_functions.keys():
        function=parse_expr(dir_of_set_functions[str(message.chat.id)])
        if message.text == 'plot':
            
            Plot = plot_func(function)
            if Plot==True:
                img = open('temp/test.png','rb')
                bot.send_photo(message.chat.id, img)
            elif Plot == False:
                bot.send_message(message.chat.id,'There was an Error while plotting')
            else:
                bot.send_message(message.chat.id,Plot)    
            
        elif message.text == 'derivate':
            awnser = str(get_derivative(function))
            saving_last_function(awnser,str(message.chat.id))
            bot.send_message(message.chat.id,awnser.replace("**","^"))
        else:
            awnser = str(get_integral(function))
            saving_last_function(awnser,str(message.chat.id))
            bot.send_message(message.chat.id,awnser.replace("**","^") )
    else:
        bot.send_message(message.chat.id,"You have not already saved a function")
     

@bot.message_handler(commands=['set'])
def set_function(message):
    dir_of_last_functions = eval(pickle.load(open("temp/last_functions.dat","rb")))
    if str(message.chat.id) in dir_of_last_functions.keys():
        function=dir_of_last_functions[str(message.chat.id)]
        dir_of_set_functions = eval(pickle.load(open("temp/set_functions.dat","rb")))
        dir_of_set_functions[str(message.chat.id)]= function
        pickle.dump(str(dir_of_set_functions),open("temp/set_functions.dat","wb"))  
        bot.send_message(message.chat.id,"You have set the function to "+function)
    else:
        bot.send_message(message.chat.id,"There is no last function you have used")


@bot.message_handler(func= lambda message:True)
def default_awnser(message):
    bot.send_message(message.chat.id, "Sorry, I can't understand what you send. Have a look at the /dir command")


bot.polling(none_stop=True)
