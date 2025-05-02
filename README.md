![Alt text](http://i.imgur.com/6B84SNI.png "Screenshot")

### Fast Python implementation of Conway's game of life [and other cellular automata](http://www.conwaylife.com/wiki/Cellular_automaton#Well-known_Life-like_cellular_automata)

Running
=========
First, install the required dependencies:
```bash
pip install -r requirements.txt
```

To run the main interactive application using Gradio:
```bash
python app.py
```
This will launch a web interface (usually at http://127.0.0.1:7860) where you can select predefined rulesets, enter custom rules, adjust the board size, and control the simulation.

To see a basic example of running a simulation directly with Matplotlib for visualization:
```bash
python example.py
```
You can modify `example.py` to experiment with different rules and initial states outside the Gradio app.

End command-line programs like `example.py` using a keyboard interrupt (Ctrl+C). The Gradio app can be stopped by closing the terminal where it's running.

How it's written
==================

The game grid is encoded as a simple `m` by `n` array (default 100x100 in the code) of zeros and ones.
In each program, a state transition is determined for each pixel by looking at the 8 pixel values all around it, and counting how many of them are "alive", then applying some rules based that number. Since the "alive" or "dead" states are just encoded as 1 or 0, this is equivalent to summing up the values of all 8 neighbors.

If you want to do this for all pixels in a single shot, this is equivalent to computing the [2D convolution](http://en.wikipedia.org/wiki/Convolution) between the game state array and a kernel matrix (e.g., [[1,1,1],[1,0,1],[1,1,1]] for counting neighbors). Convolution applies this kernel as a "stencil" across the grid to sum neighbor values. This implementation uses `scipy.signal.convolve2d` for this calculation.

An important aspect of convolution is how edges are handled. This application supports two common boundary conditions, which can be selected in the Gradio interface (`app.py`):
*   **Periodic ('wrap'):** The grid wraps around itself, connecting the top edge to the bottom and the left edge to the right (like in Pac-Man).
*   **Zero-Padding ('fill'):** The grid is assumed to be surrounded by zeros (dead cells) beyond its boundaries.

Goals
======

Ultimately, I'd like to study automata patterns with rule sets that depend on information beyond only the immediate 8 neighbors to a cell. For this code, this basically comes down to finding interesting behavior that results from using different convolution kernels.
