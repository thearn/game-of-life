import numpy as np
import time
from lib import fft_convolve2d
import matplotlib.pyplot as plt
plt.ion()


def seeds(state, k):
    """
    'Seeds' cellular automaton state transition
    http://www.conwaylife.com/wiki/Seeds
    """
    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)
    # checks the values, and sets alive vs. dead state
    c[np.where((b == 2) & (state == 0))] = 1

    # return new state
    return c

if __name__ == "__main__":
    # set up board
    m,n = 100,150
    A = np.zeros((m,n))
    A[20,20] = 1
    A[20,21] = 1

    A[75,30] = 1
    A[76,30] = 1

    # construct convolution kernel
    k = np.zeros((m, n))
    k[m/2-1 : m/2+2, n/2-1 : n/2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # plot each frame
    plt.figure()
    img_plot = plt.imshow(A, interpolation="nearest", cmap = plt.cm.gray)
    plt.show()
    while True:
        A = seeds(A, k)
        img_plot.set_data(A)
        plt.draw()
        time.sleep(0.01)
