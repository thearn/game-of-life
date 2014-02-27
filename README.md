![Alt text](http://i.imgur.com/6B84SNI.png "Screenshot")

Python implementation of Conway's game of life.

Requires Python 2.7 (will check Python 3 soon), with Numpy and Matplotlib.

To run:
```bash
$ python conway.py
```
End the program using a keyboard interrupt (ctrl-c).

The state of the grid is stored in a 2D binary array.
The rules of the game (basically computing the sum of all 8 elements of the 
array surrounding each element) is implemented using fast FFT based convolution.

One side effect: the convolution using FFT implicitly involves periodic 
boundary conditions, so the game grid is "wrapped" around itself (like in Pacman, or Mario Bros. 2).
If you wanted to change this, you would just have to modify the 2D convolution
function to use an orthogonal form of the DCT instead of the FFT. This would 
correspond to "hard" (i.e. Dirichlet) boundary conditions for the operator.

I think you could do this with scipy:

```python
from scipy import fftpack
fftpack.dct(data, norm='ortho')
```

but I haven't tried that yet for this. You'd have to define a `dct2()` method using `fftpack.dct` and separability. 
