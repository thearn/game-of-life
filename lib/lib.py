from numpy.fft import fft2, ifft2, fftshift
import numpy as np

def fft_convolve2d(x,y):
    """
    2D convolution, using FFT
    """
    fr = fft2(x)
    fr2 = fft2(np.flipud(np.fliplr(y)))
    m,n = fr.shape
    cc = np.real(ifft2(fr*fr2))
    cc = np.roll(cc, - int(m / 2) + 1, axis=0)
    cc = np.roll(cc, - int(n / 2) + 1, axis=1)
    return cc