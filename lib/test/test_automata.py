from lib.custom import automata # Updated import
import unittest
import numpy as np

class TestAutomata(unittest.TestCase): # Renamed class for clarity

    def test_still(self) -> None:
        """2x2 block"""

        A: np.ndarray = np.zeros((10,10))
        A[1:3,1:3] = 1
        B: np.ndarray = automata(A) # Use automata
        assert (A == B).all()

    def test_oscillator(self) -> None: # Corrected typo: scillator -> oscillator
        """blinker"""
        A: np.ndarray = np.zeros((10,10))
        A[1:4,1] = 1
        B: np.ndarray = automata(A) # Use automata
        assert (B[2, 0:3] == 1).all()

        B = automata(B) # Use automata
        assert (A == B).all()

    def test_evolution(self) -> None:
        """test that something changes"""
        m, n = 10, 10
        A: np.ndarray = np.random.random(m*n).reshape((m, n)).round()
        B: np.ndarray = automata(A) # Use automata
        assert (B != A).any()



if __name__ == '__main__':
    unittest.main()
