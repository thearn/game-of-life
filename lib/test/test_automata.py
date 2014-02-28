from conway import conway
import unittest
import numpy as np

class TestConway(unittest.TestCase):

    def test_still(self):
        """2x2 block"""

        A = np.zeros((10,10))
        A[1:3,1:3] = 1
        B = conway(A)
        assert (A == B).all()

    def test_scillator(self):
        """blinker"""
        A = np.zeros((10,10))
        A[1:4,1] = 1
        B = conway(A)
        assert (B[2, 0:3] == 1).all()

        B = conway(B)
        assert (A == B).all()

    def test_evolution(self):
        """test that something changes"""
        m, n = 10, 10
        A = np.random.random(m*n).reshape((m, n)).round()
        B = conway(A)
        assert (B != A).any()



if __name__ == '__main__':
    unittest.main()
