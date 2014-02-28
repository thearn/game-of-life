from lib import fft_convolve2d
import numpy as np

def automata(state, rule = 'B3/S23', k=None):
    """
    Apply a custom automata transition from a rulestring
    """
    # set up kernel if not given
    if k == None:
        m, n = state.shape
        k = np.zeros((m, n))
        k[m/2-1 : m/2+2, n/2-1 : n/2+2] = np.array([[1,1,1],[1,0,1],[1,1,1]])

    # computes sums around each pixel
    b = fft_convolve2d(state,k).round()
    c = np.zeros(b.shape)
    # checks the values, and sets alive vs. dead state

    born = [int(i) for i in rule.split('/')[0].replace('B','')]
    survive = [int(i) for i in rule.split('/')[1].replace('S','')]

    for i in born:
        c[np.where((b == i) & (state == 0))] = 1
    for i in survive:
        c[np.where((b == i) & (state == 1))] = 1

    # return new state
    return c