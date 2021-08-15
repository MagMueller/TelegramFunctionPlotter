import telebot
from boolean_functions import *
from plot import plot_func
from math_part import *
from saving_data import *
import pickle

print("start")

API_KEY = "1913464534:AAGjZ9gC5KQmRiAjd-YWCAjhkKYGIpU6SBM" # specify our API
bot = telebot.TeleBot(API_KEY) # create a bot


@bot.message_handler(commands=['hello'])
def hello(message):
    """Reply with a nice Hello"""
    bot.send_message(message.chat.id, "Hello!")

@bot.message_handler(commands=['bild'])
def bild(message):
    """send the last saved photo"""
    img = open('temp/plot.png','rb')
    bot.send_photo(message.chat.id, img)
    

@bot.message_handler(func=bool_plot)
def plot(message):
    """This function handels the plotting (working ones and failures)"""
    text=message.text
    gespeichertes_erg = getting_buffer() # get the saved data from the buffer
    if gespeichertes_erg[0]==False: # if the saved data is a failure message
        bot.send_message(message.chat.id,gespeichertes_erg[1]) # just reply with the failure message
    else:
        Plot = plot_func(gespeichertes_erg[1]) # otherwise plot the function
        if Plot==True: # if th plotting suceeded
            img = open('temp/plot.png','rb')
            bot.send_photo(message.chat.id, img) # send the picture
        else:
            bot.send_message(message.chat.id,Plot) # if Plot returned a failure message, reply it




@bot.message_handler(func=bool_integrate)
def integrate(message):
    """This function handels the integration (working ones and failures)"""
    text=str(message.text)
    gespeichertes_erg = getting_buffer() # get the saved data from the buffer
    if gespeichertes_erg[0]==False: # if the saved data is a failure message
        bot.send_message(message.chat.id,gespeichertes_erg[1]) # just reply with the failure message
    else:  # otherwise integrate the function
        erg = gespeichertes_erg[1]
        rückgabe=''
        if len(erg)==2: # if borders were specified
            try:
                rückgabe= str((get_integral(erg[0],borders=erg[1]))) # try to integrate function with borders
            except:
                rückgabe = 'Integration failed' # give failure message if integration fauled
        elif len(erg)==1: # if borders weren't specified
            try:
                rückgabe= str(get_integral(erg[0])) # try to integrate function
                saving_last_function(rückgabe,str(message.chat.id)) # save the result as last function 
            except:
                rückgabe = 'Integration failed' # give failure message if integration failed
        
        bot.send_message(message.chat.id, rückgabe.replace('**','^')) # reply the function
      

@bot.message_handler(func=bool_derivation)
def derivate(message):
    """This function handels the derivation (working ones and failures)"""
    text=str(message.text)
    gespeichertes_erg = getting_buffer() # get the saved data from the buffer
    if gespeichertes_erg[0]==False: # if the saved data is a failure message
        bot.send_message(message.chat.id,gespeichertes_erg[1]) # just reply with the failure message
    else: # derivate integrate the function
        erg = gespeichertes_erg[1]
        rückgabe=''
        if len(erg)==2: # if var was specified
            rückgabe= str(get_derivative(erg[0],var=erg[1]))
        elif len(erg)==1: # if var was not specified
            rückgabe= str(get_derivative(erg[0]))
        saving_last_function(rückgabe,str(message.chat.id)) # save the result as last function 
        bot.send_message(message.chat.id, rückgabe.replace('**','^'))  # reply the function
    
    

@bot.message_handler(commands=['help','dir','start'])
def help_message(message):
    "This function is suppose to return a explanaition of all commands used"
    with open('dir_of_commands.txt','r') as f:
        bot.send_message(message.chat.id, f.read())


@bot.message_handler(func=bool_function)
def set_function(message):
    """This function is suposse to set a function that was newly send in as the current function for the user"""
    gespeichertes_erg = getting_buffer()  
    if gespeichertes_erg[0]==False:  # if the saved data is a failure message
        bot.send_message(message.chat.id,gespeichertes_erg[1])  # just reply with the failure message
    else: # else save the function 
        function = str(gespeichertes_erg[1])
        dir_of_set_functions = eval(pickle.load(open("temp/set_functions.dat","rb"))) # get the directory of set_functions
        dir_of_set_functions[str(message.chat.id)]= function # add new function
        pickle.dump(str(dir_of_set_functions),open("temp/set_functions.dat","wb")) # save the changed directory
        bot.send_message(message.chat.id, 'The current function is now '+function.replace("**","^") +'\nYou can now plot, derivate or integrate it') # reply with function 
    
@bot.message_handler(func=lambda message:message.text in ['derivate','plot','integrate'])
def use_saved_function(message):
    """This function is suposse to plot, derivate or integrate the saved function"""
    dir_of_set_functions = eval(pickle.load(open("temp/set_functions.dat","rb"))) # get the saved function
    if str(message.chat.id) in dir_of_set_functions.keys(): # if Messager has already saved a function
        function=parse_expr(dir_of_set_functions[str(message.chat.id)]) # get it
        if message.text == 'plot': # if plotting was written
            Plot = plot_func(function) # Plot the function
            if Plot==True:
                img = open('temp/plot.png','rb')
                bot.send_photo(message.chat.id, img) # if it worked reply the photo
            else:
                bot.send_message(message.chat.id,Plot) # else send failure message
            
        elif message.text == 'derivate': # if derivate was written
            awnser = str(get_derivative(function)) # derivate the function
            saving_last_function(awnser,str(message.chat.id)) # save it 
            bot.send_message(message.chat.id,awnser.replace("**","^")) # reply the function
        else: # if integrate was written
            try:
                awnser = str(get_integral(function)) # try to integrate the function
                saving_last_function(awnser,str(message.chat.id)) # save it 
                bot.send_message(message.chat.id,awnser.replace("**","^")) # reply it
            except:
                bot.send_message(message.chat.id,'Integration failed') # if integration failed, reply with faulure message
    else:
        bot.send_message(message.chat.id,"You have not already saved a function") # if Messager has not already saved a function, tell him
     

@bot.message_handler(func= lambda message: message.text in ['/set','set'])
def set_function(message):
    """This function is suposse to set the last function that was returned as the main function"""
    dir_of_last_functions = eval(pickle.load(open("temp/last_functions.dat","rb"))) # get the directory of the last returned functions
    if str(message.chat.id) in dir_of_last_functions.keys(): # if Messager has already gotten a function returned
        function=dir_of_last_functions[str(message.chat.id)] # get the function
        dir_of_set_functions = eval(pickle.load(open("temp/set_functions.dat","rb"))) # get the directory of set_functions
        dir_of_set_functions[str(message.chat.id)]= function  # add new function
        pickle.dump(str(dir_of_set_functions),open("temp/set_functions.dat","wb"))  # save the changed directory
        bot.send_message(message.chat.id,"You have set the function to "+function) # reply the Messager
    else:
        bot.send_message(message.chat.id,"There is no last function you have used") # if Messager has not already gotten a function returned, tell him


@bot.message_handler(func= lambda message:True)
def default_awnser(message):
    """This function is just simply the deafult awnser"""
    bot.send_message(message.chat.id, "Sorry, I can't understand what you send. Have a look at the /dir command") 


bot.polling(none_stop=True) # run the bot
