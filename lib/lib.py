from numpy.fft import fft2, ifft2, fftshift
import numpy as np
import scipy.signal as signal

def fft_convolve2d(x,y):
    """
    2D convolution, using FFT
    """
    cc = signal.convolve2d(x, y, mode="same", boundary="wrap")
    return cc
