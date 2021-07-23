# Import libraries
import matplotlib.pyplot as plt
import numpy as np

# Creating vectors X and Y
x = np.linspace(-10, 10, 100)
f = "x ** 3"
print(eval(f))
#print(type(np.ndarray(f)))

fig = plt.figure(figsize=(10, 5))
# Create the plot
plt.plot(x, eval(f))

# Show the plot
plt.show()