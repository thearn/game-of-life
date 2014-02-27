from numpy.fft import fft2, ifft2, fftshift
import numpy as np
import time
 
import matplotlib.pyplot as plt
plt.ion()

def fft_convolve2d(x,y):
    """
    2D convolution, using FFT
    """
    fr = fft2(x)
    fr2 = fft2(np.flipud(np.fliplr(y)))
    m,n = fr.shape
    cc = np.real(ifft2(fr*fr2))
    cc = np.roll(cc, -m/2+1,axis=0)
    cc = np.roll(cc, -n/2+1,axis=1)
    return cc

def step(state, k):
    """
    Iterates one step using the rules for CGOL.
    """
    # computes sums around each pixel
    b = fft_convolve2d(state,k).round()

    # checks the values, and sets alive vs. dead state
    b[np.where(b < 2)] = 0
    b[np.where(b > 3)] = 0
    b[np.where((b == 2) & (state == 1))] = 1
    b[np.where(b == 3)] = 1
    b[np.where(b == 2)] = 0

    # return new state
    return b

if __name__ == "__main__":
    # set up board
    m,n = 100,100
    A = np.random.random(m*n).reshape((m, n)).round()

    # construct convolution kernel 
    k = np.zeros((m, n))
    k[m/2-1 : m/2+2, n/2-1 : n/2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # plot each frame
    plt.figure()
    img_plot = plt.imshow(A, interpolation="nearest", cmap = plt.cm.gray)
    plt.show()
    for i in xrange(1,5000):
        A = step(A, k)
        img_plot.set_data(A)
        plt.draw()
        time.sleep(0.01)
