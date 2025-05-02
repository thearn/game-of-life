from lib.lib import fft_convolve2d # Corrected import path
import unittest
import numpy as np

class TestFFTconvolve(unittest.TestCase):

    def test_uniform(self) -> None:

        A: np.ndarray = np.random.randn(10,10)
        K: np.ndarray = np.ones((10,10))
        a: float = fft_convolve2d(A,K).max()
        b: float = A.sum()

        self.assertAlmostEqual(a, b)



if __name__ == '__main__':
    unittest.main()
