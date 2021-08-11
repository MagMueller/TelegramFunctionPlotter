from sympy import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

x, y, z = symbols('x y z')

def plot_func(Funktion,Interval=np.linspace(-10,10,50)):
    """
    Input: Funktion
    Output: True if Plotting suceeded, an Error message when it failed"""
    if len(Funktion.atoms(Symbol))==2: # if function is two dimensional
        try:
            fig = plt.figure()
            lambdified_function=lambdify(list(Funktion.atoms(Symbol)),Funktion,"numpy") # lambdify is a sympy function that creates a lamba function out of a sympy expression
            X_Axes,Y_Axes = np.meshgrid(Interval,Interval) # create X,Y axes
            Z_Axes=lambdified_function(X_Axes,Y_Axes) 
            ax = plt.axes(projection='3d') # 3d plot
            ax.contour3D(X_Axes,Y_Axes, Z_Axes, 50, cmap='magma')
            fig.savefig('temp/plot.png') # save the plot
            return True
        except:
            return 'Plotting failed' # failure message
        
    elif len(Funktion.atoms(Symbol))==1: # if function is one dimensional
        try: 
            lambdified_function=lambdify(list(Funktion.atoms(Symbol))[0],Funktion)
            fig, ax = plt.subplots()
            ax.plot(Interval,lambdified_function(Interval))
            fig.savefig('temp/plot.png') # save plot
            return True
        except:
            return 'Plotting failed'
    
    else: # if function is either 0 or 3 dimensional
        try: 
            f = lambda x : x-x+float(Funktion) # if it is 0 dimensional without unspecified variables float(Funktion) workes, else it will fail
            fig, ax = plt.subplots()
            ax.plot(Interval,f(Interval))
            fig.savefig('temp/plot.png')
            return True
        except:
            return 'Function not one or two dimensionals with out factors' # failure message