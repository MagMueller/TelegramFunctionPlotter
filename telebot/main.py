import os
import telebot
from bob_telegram_tools.bot import TelegramBot
import matplotlib.pyplot as plt
import numpy as np

#API_KEY = os.getenv('API_KEY')
API_KEY = "1702660552:AAG1xiHvgK2H5Np3m-6YSAQAB-cKhoL2SSY"
bot = telebot.TeleBot(API_KEY)

user_id = int(1291571328)
bot_plot = TelegramBot(API_KEY, user_id)


#test for /Greet in telegram
@bot.message_handler(commands=['Greet'])
def greet(message):
  bot.reply_to(message, "Hey! Hows it going?")

#just hello
@bot.message_handler(commands=['hello'])
def hello(message):
  bot.send_message(message.chat.id, "Hello!")


#plot all inputs where x occures
def plotable(message):
  #plotFunction = message.text
  if 'x' in message.text:
    return True
  else:
      print("no formal with x")
      return False

@bot.message_handler(func=plotable)
def plotFunction(message):
  # Creating vectors X and Y
  x = np.linspace(-10, 10, 100)

  #input has this style
  #f = "x ** 3"
  try:
    #fig = plt.figure(figsize=(10, 5))
    # Create the plot
    plt.plot(x, eval(message.text))
    # Show the plot
    #plt.show()
    plt.ylabel("Test")
    bot_plot.send_plot(plt)
  except:
    print("error during ploting")



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





"""
idee:
Eingeben ylim = 10
function = x^20
/show 
ableitung

"""


# This method delete the generetad image


bot.polling()