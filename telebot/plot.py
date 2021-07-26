from sympy import *
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits import mplot3d

x, y, z = symbols('x y z')

def plot_func(Funktion,Interval=np.linspace(-10,10,50)):
    if len(Funktion.atoms(Symbol))==2:
        try:
            fig = plt.figure()
            d=lambdify(list(Funktion.atoms(Symbol)),Funktion,"numpy")
            A,B = np.meshgrid(Interval,Interval)
            Z=d(A,B)
            ax = plt.axes(projection='3d')
            ax.contour3D(A, B, Z, 50, cmap='magma')
            fig.savefig('temp/test.png')
            return True
        except:
            return False
        
    elif len(Funktion.atoms(Symbol))==1:
        try: 
            f=lambdify(list(Funktion.atoms(Symbol))[0],Funktion)
            fig, ax = plt.subplots()
            ax.plot(Interval,f(Interval))
            fig.savefig('temp/test.png')
            return True
        except:
            return False
    return False