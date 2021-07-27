import os
import telebot
import matplotlib.pyplot as plt
import numpy as np
from boolean_functions import *
from plot import plot_func
from math_part import *


toggle_switch_negative()

#API_KEY = os.getenv('API_KEY')
API_KEY = "1913464534:AAGjZ9gC5KQmRiAjd-YWCAjhkKYGIpU6SBM"
bot = telebot.TeleBot(API_KEY)

#test for /Greet in telegram
@bot.message_handler(commands=['Greet'])
def greet(message):
    bot.reply_to(message, "Hey! Hows it going?")

#just hello
@bot.message_handler(commands=['hello'])
def hello(message):
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['bild'])
def hello(message):
    img = open('temp/test.png','rb')
    bot.send_photo(message.chat.id, img)

@bot.message_handler(func=bool_plot)
def plot(message):
    text=str(message.text)
    try:
        plot_func(parse_plot(text))
        img = open('temp/test.png','rb')
        bot.send_photo(message.chat.id, img)
    except:
        bot.send_message(message.chat.id,'There was an Error while plotting')



@bot.message_handler(func=bool_integrate)
def integrate(message):
    text=str(message.text)
    erg=parse_integrate(text)
    rückgabe=''
    if len(erg)==2:
        rückgabe= str((get_integral(erg[0],borders=erg[1])))
    elif len(erg)==1:
        rückgabe= str(get_integral(erg[0]))
    bot.send_message(message.chat.id, rückgabe.replace('**','^'))

@bot.message_handler(func=bool_derivation)
def derivate(message):
    text=str(message.text)
    erg=parse_derivation(text)
    rückgabe=''
    if len(erg)==2:
        rückgabe= str(get_derivative(erg[0],var=erg[1]))
    elif len(erg)==1:
        rückgabe= str(get_derivative(erg[0]))
    bot.send_message(message.chat.id, rückgabe.replace('**','^'))
    
    
@bot.message_handler(func=false_plot)
def false_plot_awnser(message):
    bot.send_message(message.chat.id, parse_plot(message.text))
    
    
@bot.message_handler(func=false_integration)
def false_intgration_awnser(message):
    bot.send_message(message.chat.id, parse_integrate(message.text))
    
@bot.message_handler(func=false_derivation)
def false_derivate_awnser(message):
    bot.send_message(message.chat.id, parse_derivation(message.text))
    

@bot.message_handler(commands=['help','dir','start'])
def help_message(message):
    with open('dir_of_commands.txt','r') as f:
        bot.send_message(message.chat.id, f.read())
        
        
@bot.message_handler(commands=['help','dir','start'])
def help_message(message):
    with open('dir_of_commands.txt','r') as f:
        bot.send_message(message.chat.id, f.read())

@bot.message_handler(commands=['toggle'])
def mach_was(message):
    if get_switch()==True:
        toggle_switch_negative()
    else:
        toggle_switch_positve()
    bot.send_message(message.chat.id, 'der switch ist jetzt'+str(get_switch()))


@bot.message_handler(func=bool_function)
def set_function(message):
    toggle_switch_positve()
    function = str(parse_function(message.text))
    with open('temp/current_function.txt','w') as f:
        f.write(function)
        f.close()
    bot.send_message(message.chat.id, 'The current function is now '+function.replace("**","^") +'\nYou can now plot, derivate or integrate it')
    
@bot.message_handler(func=function_command)
def use_saved_function(message):
    with open('temp/current_function.txt','r') as f:
        function = parse_function(f.read())
        f.close()
    if message.text == 'plot':
        plot_func(function)
        img = open('temp/test.png','rb')
        bot.send_photo(message.chat.id, img)
    elif message.text == 'derivate':
        awnser = str(get_derivative(function))
        with open('temp/last_function.txt','w') as f:
            f.write(awnser)
            f.close()
        bot.send_message(message.chat.id,awnser.replace("**","^"))
    else:
        awnser = str(get_integral(function))
        with open('temp/last_function.txt','w') as f:
            f.write(awnser)
            f.close()
        bot.send_message(message.chat.id,awnser.replace("**","^") )
     

@bot.message_handler(commands=['set'])
def set_function(message):
    with open('temp/last_function.txt','r') as f:
        function = f.read()
        f.close()
    with open('temp/current_function.txt','w') as f:
        f.write(function)
        f.close()
    bot.send_message(message.chat.id,"You have set the function to "+function)
 
@bot.message_handler(commands=['delete'])
def set_function(message):
    if get_switch():
        with open('temp/last_function.txt','w') as f:
            f.write('')
            f.close()
        with open('temp/current_function.txt','w') as f:
            f.write('')
            f.close()
        toggle_switch_negative()
        bot.send_message(message.chat.id,"You have deletet the function")
    else:
        bot.send_message(message.chat.id,"There is no function to delete")
        
        
@bot.message_handler(func=missing)
def set_function(message):
    bot.send_message(message.chat.id,"There is no function saved")



@bot.message_handler(func=rest)
def default_awnser(message):
    print(message.text)
    bot.send_message(message.chat.id, "Sorry, I can't understand what you send. Have a look at the /dir command")


bot.polling()

