import numpy as np
import time
from lib import fft_convolve2d
import matplotlib.pyplot as plt
plt.ion()

def high_life(state, k=None):
    """
    'HighLife' automata state transition
    http://www.conwaylife.com/wiki/HighLife
    """
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m/2-1 : m/2+2, n/2-1 : n/2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # computes sums around each pixel
    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)

    c[np.where((b == 2) & (state == 1))] = 1
    c[np.where((b == 3) & (state == 1))] = 1

    c[np.where((b == 3) & (state == 0))] = 1
    c[np.where((b == 6) & (state == 0))] = 1

    # return new state
    return c

if __name__ == "__main__":
    # set up board randomly
    m,n = 100,100
    A = np.zeros((m,n))
    A = 0.63*np.random.random(m*n).reshape((m, n))
    A = A.round()

    # start up an isolated replicator pattern in the upper left
    A[:75, :75] = 0
    A[10,11] = 1
    A[10,12] = 1
    A[10,13] = 1
    A[11,10] = 1
    A[12,10] = 1
    A[13,10] = 1

    # plot each frame
    plt.figure()
    img_plot = plt.imshow(A, interpolation="nearest", cmap = plt.cm.gray)
    plt.show()
    while True:
        A = high_life(A)
        img_plot.set_data(A)
        plt.draw()
        time.sleep(0.01)
