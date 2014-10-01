import numpy as np
import time
from lib import fft_convolve2d
import matplotlib.pyplot as plt
plt.ion()

def conway(state, k=None):
    """
    Conway's game of life state transition
    """

    # set up kernel if not given
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

    # return new state
    return c

if __name__ == "__main__":
    # set up board
    m,n = 100,100
    A = np.random.random(m*n).reshape((m, n)).round()

    # plot each frame
    plt.figure()
    img_plot = plt.imshow(A, interpolation="nearest", cmap = plt.cm.gray)
    plt.show(block=False)
    while True:
        A = conway(A)
        img_plot.set_data(A)
        plt.draw()
        time.sleep(0.01)
