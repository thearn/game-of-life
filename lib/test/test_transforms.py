from lib import fft_convolve2d
import unittest
import numpy as np

class TestFFTconvolve(unittest.TestCase):

    def test_uniform(self):

        A = np.random.randn(10,10)
        K = np.ones((10,10))
        a,b = fft_convolve2d(A,K).max(), A.sum()

        self.assertAlmostEqual(a, b)



if __name__ == '__main__':
    unittest.main()
