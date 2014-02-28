from lib import automata
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
import time

# Game of Life
rule_string = 'B36/S23'

# Day & Night
rule_string = 'B3678/S34678'

# set up board randomly
m,n = 100,100
A = np.zeros((m,n))
A = 0.63*np.random.random(m*n).reshape((m, n))
A = A.round()

plt.figure()
img_plot = plt.imshow(A, interpolation="nearest", cmap = plt.cm.gray)
plt.show()
while True:
    # input state array, and rule string in 'Bxx/Sxx' format
    A = automata(A, rule_string)
    img_plot.set_data(A)
    plt.draw()
    time.sleep(0.01)