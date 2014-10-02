import numpy as np
import time
from lib import fft_convolve2d
import matplotlib.pyplot as plt
plt.ion()

def two_by_two(state, k=None):
    """
    '2x2' automata state transition
    http://www.conwaylife.com/wiki/2x2
    """
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m/2-1 : m/2+2, n/2-1 : n/2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # computes sums around each pixel
    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)
    # checks the values, and sets alive vs. dead state

    c[np.where((b == 1) & (state == 1))] = 1
    c[np.where((b == 2) & (state == 1))] = 1
    c[np.where((b == 5) & (state == 1))] = 1

    c[np.where((b == 3) & (state == 0))] = 1
    c[np.where((b == 6) & (state == 0))] = 1

    # return new state
    return c

if __name__ == "__main__":
    # set up board
    m,n = 100,100
    A = np.zeros((m,n))
    A = 0.6*np.random.random(m*n).reshape((m, n))
    A = A.round()

    # plot each frame
    plt.figure()
    img_plot = plt.imshow(A, interpolation="nearest", cmap = plt.cm.gray)
    plt.show(block=False)
    while True:
        A = two_by_two(A)
        img_plot.set_data(A)
        plt.draw()
        time.sleep(0.01)
