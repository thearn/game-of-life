Python implementation of Conway's game of life.

Requires Python 2.7 (will check Python 3 soon), with Numpy and Matplotlib.

To run:
```bash
$ python conway.py
```
End the program using a keyboard interrupt (ctrl-c).

The state of the grid is stored in a binary array.
The rules of the game (basically computing the sum of all 8 elements of the 
array surrounding each element) is implemented using fast FFT based convolution.

One side effect: the convolution using FFT implicitly involves periodic 
boundary conditions, so the game grid is "wrapped" around itself (like Pacman).
If you wanted to change this, you would just have to modify the 2d convolution
method to use an orthogonal form of the DCT instead of the FFT. This would 
correspond to "hard" (i.e. Dirichlet) boundary conditions for the operator.