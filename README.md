![Alt text](http://i.imgur.com/6B84SNI.png "Screenshot")

Fast Python implementation of Conway's game of life [and other cellular automata](http://www.conwaylife.com/wiki/Cellular_automaton#Well-known_Life-like_cellular_automata).

Requires Python 2.7 (will check Python 3 soon), with Numpy and Matplotlib.

To run [Game of Life](http://www.conwaylife.com/wiki/Conway%27s_Game_of_Life):
```bash
$ python conway.py
```

To run [Replicator](http://www.conwaylife.com/wiki/Replicator_(CA)):
```bash
$ python replicator.py
```

Other cellular automata implementations are run the same way.

End each program using a keyboard interrupt (ctrl-c).

The game grid is encoded as a simple `m` by `n` array (default 100x100 in the code) of zeros and ones.
In each program, a state transition is determined for each pixel by looking at the 8 pixel values all around it, and counting how many of them are "alive", then applying some rules based that number. Since the "alive" or "dead" states are just encoded as 1 or 0, this is equivalent to summing up the values of all 8 neighbors.

If you want to do this for all pixels in a single shot, this is equivalent to computing the [2D convolution](http://en.wikipedia.org/wiki/Convolution) between the game state array and the matrix [[1,1,1],[1,0,1],[1,1,1]]. Convolution is an operation that basically applies that matrix as a "stencil" at every position around the game grid array, and sums up the values according to the values in that stencil. And convolution can be very efficiently computed using the FFT, thanks to the [Fourier Convolution Theorem](http://en.wikipedia.org/wiki/Convolution_theorem).

One side effect: the convolution using FFT implicitly involves periodic
boundary conditions, so the game grid is "wrapped" around itself (like in Pacman, or Mario Bros. 2).
If you wanted to change this, you would just have to modify the 2D convolution
function to use an orthogonal form of the DCT instead of the FFT. This would
correspond to "hard" (i.e. Dirichlet) boundary conditions on the convolution operator.

I think you could do this with scipy using the 1D orthogonal dct provided:

```python
from scipy import fftpack
fftpack.dct(data, norm='ortho')
```

but I haven't tried that yet. You'd have to define a `dct2()` method using `fftpack.dct` and separability (ie. the 1D transform matrix is rank-one, and the 2D transform operator is the Kronecker product of two 1D transforms ).
