import numpy as np
import time
from lib import fft_convolve2d
import matplotlib.pyplot as plt
plt.ion()

from PIL import Image


def conway(state, k=None):
    """
    Conway's game of life state transition
    """

    # set up kernel if not given
    if k is None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m//2-1 : m//2+2, n//2-1 : n//2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

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
    img = Image.open("test.png")
    # Resize image to 50%
    new_width = int(img.width * 0.5)
    new_height = int(img.height * 0.5)
    A_original = np.array(img.resize((new_width, new_height)))

    threshold = 180
    # Convert to binary based on threshold, handling potential alpha channel
    if A_original.shape[2] == 4: # Check for alpha channel
        A_original = A_original[:,:,:3] # Drop alpha channel if present
    A = np.where(np.mean(A_original, axis=2) > threshold, 0, 1) # Use mean for grayscale conversion

    R, G, B = A[:,:,0], A[:,:,1], A[:,:,2]

    # plot each frame
    plt.figure()
    plt.subplot(121)
    plt.imshow(A_original,interpolation="nearest")

    plt.subplot(122)
    img_plot = plt.imshow(A,interpolation="nearest")
    plt.show(block=False)
    while True:
        R, G, B = conway(R), conway(G), conway(B)
        A[:,:,0], A[:,:,1], A[:,:,2] = R,G,B
        img_plot.set_data(A)
        plt.draw()
        plt.pause(0.01) # Use plt.pause to allow GUI updates
