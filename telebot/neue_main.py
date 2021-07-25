import os
import telebot
import matplotlib.pyplot as plt
import numpy as np
from boolean_functions import *
from plot import plot_func
from math_part import *

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
    plot_func(parse_plot(text))
    img = open('temp/test.png','rb')
    bot.send_photo(message.chat.id, img)



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
    
    
def check_function(message):
  print(message)
  try:
    print(message.text)
    ans = eval(message.text)
    print("eval ans: ", ans)
    return True
  except:
    print("noo")
    return False


#this works with eval
@bot.message_handler(func=check_function)
def taschenrechner(message):
  if message.text != None:
    print("my ans: ", message.text)
    bot.send_message(message.chat.id, message.text)
  else:
    bot.send_message(message.chat.id, "not valid")




bot.polling()