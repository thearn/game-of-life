import numpy as np
import time
from lib import fft_convolve2d
import matplotlib.pyplot as plt
plt.ion() # Turn on interactive mode for plotting

def example_rule(state, k=None):
    """
    Placeholder for a custom rule state transition.
    Replace this with the specific logic for the desired simulation.
    For example, see conway.py for Conway's Game of Life implementation.

    Parameters:
    state (np.ndarray): The current state of the grid.
    k (np.ndarray, optional): The convolution kernel. Defaults to None.

    Returns:
    np.ndarray: The next state of the grid.
    """
    # Example: A simple rule that inverts the state (replace with actual rule)
    # This is just a placeholder to make the example runnable.
    # return 1 - state

    # Default behavior: return the current state if no rule is implemented
    print("Warning: example_rule is a placeholder. Implement your simulation logic.")
    return state

if __name__ == "__main__":
    # --- Simulation Configuration ---
    # Set the dimensions of the grid
    m, n = 100, 100

    # Initialize the starting state (e.g., random, specific pattern)
    # A = np.zeros((m, n)) # Example: Start with an empty grid
    # A[m//2, n//2] = 1    # Example: Place a single cell in the center
    A = np.random.random(m*n).reshape((m, n)).round() # Example: Random start

    # --- Simulation Loop ---
    plt.figure()
    img_plot = plt.imshow(A, interpolation="nearest", cmap=plt.cm.gray)
    plt.title("Example Simulation")
    plt.show(block=False) # Display the plot without blocking execution

    running = True
    while running:
        try:
            # Apply the rule to get the next state
            A = example_rule(A) # Replace example_rule with your actual rule function if needed

            # Update the plot
            img_plot.set_data(A)
            plt.draw()

            # Pause briefly to control animation speed and allow GUI updates
            plt.pause(0.1)

        except KeyboardInterrupt:
            # Allow stopping the simulation with Ctrl+C in the terminal
            running = False
            print("Simulation stopped by user.")
        except Exception as e:
            # Catch other potential errors during simulation
            print(f"An error occurred: {e}")
            running = False

    print("Simulation finished.")
    plt.ioff() # Turn off interactive mode
    plt.show() # Keep the final plot window open until manually closed
