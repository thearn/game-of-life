from lib import automata
import matplotlib.pyplot as plt
plt.ion()
import numpy as np
import time

# game board size
m,n = 100,100

# uncomment any of the rule string and
# initial state arrays (A) below to see each
# automata

# Game of Life
# rule_string = 'B36/S23'
# A = np.random.random(m*n).reshape((m, n)).round()

# # Replicator
# rule_string = 'B1357/S1357'
# A = np.zeros((m,n))
# A[20,20] = 1
# A[20,21] = 1

# Day & Night
# rule_string = 'B3678/S34678'
# A = 0.69*np.random.random(m*n).reshape((m, n))
# A = A.round()

# HighLife
# rule_string = 'B36/S23'
# A = 0.63*np.random.random(m*n).reshape((m, n))
# A = A.round()

# Seeds
# rule_string = 'B2/S'
# A = np.zeros((m,n))
# A[20,20] = 1
# A[20,21] = 1
# A[75,30] = 1
# A[76,30] = 1

# walled cities
# rule_string = 'B45678/S2345'
# A = 0.63*np.random.random(m*n).reshape((m, n))
# A = A.round()

# maze
rule_string = 'B3/S12345'
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
