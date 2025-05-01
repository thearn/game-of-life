import gradio as gr
import numpy as np
import time
from lib.custom import automata
from PIL import Image # Import Pillow

# --- Simulation Parameters ---
DEFAULT_BOARD_SIZE = 100 # Default edge size for the square board
DISPLAY_SIZE = (400, 400) # Target size for display
INITIAL_FILL_FACTOR = 0.3 # Percentage of initially alive cells

# --- Predefined Rulesets ---
PREDEFINED_RULESETS = {
    "Conway's Game of Life": "B3/S23",
    "HighLife": "B36/S23",
    "Day & Night": "B3678/S34678",
    "Replicator": "B1357/S1357",
    "Seeds": "B2/S",
    "Maze": "B3/S12345",
    "Walled Cities": "B45678/S2345",
    "2x2": "B36/S125",
}
DEFAULT_RULESET_NAME = "Conway's Game of Life"
DEFAULT_RULESET_STRING = PREDEFINED_RULESETS[DEFAULT_RULESET_NAME]

# --- Helper Functions ---
def scale_board(board_array, target_size=DISPLAY_SIZE):
    """Scales the board array using Pillow."""
    if board_array is None or board_array.size == 0:
        return np.zeros(target_size, dtype=np.uint8)
    if board_array.ndim == 2:
        try:
            img = Image.fromarray(board_array.astype(np.uint8), mode='L')
            img_resized = img.resize(target_size, Image.NEAREST)
            return np.array(img_resized)
        except Exception as e:
            print(f"Error scaling board: {e}")
            return np.zeros(target_size, dtype=np.uint8)
    else:
        print(f"Warning: Board array has unexpected dimensions {board_array.shape}. Returning blank.")
        return np.zeros(target_size, dtype=np.uint8)

def initialize_board(size_tuple=(DEFAULT_BOARD_SIZE, DEFAULT_BOARD_SIZE), fill_factor=INITIAL_FILL_FACTOR):
    """Creates a random initial board state with given dimensions."""
    if not (isinstance(size_tuple, tuple) and len(size_tuple) == 2 and
            isinstance(size_tuple[0], int) and isinstance(size_tuple[1], int) and
            size_tuple[0] > 0 and size_tuple[1] > 0):
        print(f"Invalid size_tuple {size_tuple}, using default.")
        size_tuple = (DEFAULT_BOARD_SIZE, DEFAULT_BOARD_SIZE)
    print(f"Initializing board with size: {size_tuple}")
    board = (np.random.rand(size_tuple[0], size_tuple[1]) < fill_factor).astype(np.uint8) * 255
    return board

def get_initial_display_board(board):
    """Scales the initial board for display."""
    return scale_board(board)

# --- Gradio Interface ---
with gr.Blocks() as demo:
    # State variables
    board_size_state = gr.State((DEFAULT_BOARD_SIZE, DEFAULT_BOARD_SIZE)) # Stores the desired board dimensions
    initial_raw_board = initialize_board(size_tuple=board_size_state.value)
    board_state = gr.State(initial_raw_board) # Stores the current raw simulation board
    running = gr.State(False)
    ruleset = gr.State(DEFAULT_RULESET_STRING)

    gr.Markdown("# Cellular Automata Explorer")
    gr.Markdown("Select/enter ruleset, set board size (press Enter), then Start/Pause/Restart.")

    with gr.Row():
        ruleset_dropdown = gr.Dropdown(
            choices=list(PREDEFINED_RULESETS.keys()),
            value=DEFAULT_RULESET_NAME,
            label="Predefined Rulesets",
        )
        custom_ruleset_input = gr.Textbox(
            value=DEFAULT_RULESET_STRING,
            label="Ruleset String (e.g., B3/S23)",
            interactive=True
        )
        board_size_input = gr.Number(
            value=DEFAULT_BOARD_SIZE,
            label="Board Size (N x N)",
            minimum=10,
            maximum=500,
            step=10,
            interactive=True
        )

    with gr.Row():
        start_btn = gr.Button("Start")
        pause_btn = gr.Button("Pause")
        restart_btn = gr.Button("Restart")

    output_image = gr.Image(
        label="Simulation",
        value=get_initial_display_board(initial_raw_board),
        type="numpy",
        image_mode="L",
        interactive=False,
        height=DISPLAY_SIZE[1],
        width=DISPLAY_SIZE[0]
    )

    # --- Event Handlers ---
    def update_ruleset_string(dropdown_choice):
        new_ruleset = PREDEFINED_RULESETS.get(dropdown_choice, "")
        ruleset.value = new_ruleset
        return new_ruleset

    def handle_custom_ruleset_input(custom_input):
        ruleset.value = custom_input

    def simulation_loop(current_raw_board, current_ruleset):
        """Generator that runs the simulation loop and yields SCALED frames."""
        print(f"Simulation loop entered with board shape: {current_raw_board.shape}")

        if running.value:
             print("Simulation already running.")
             yield scale_board(current_raw_board)
             return

        print("Starting simulation loop...")
        running.value = True
        current_board_internal = current_raw_board.copy() / 255

        while running.value:
            if not current_ruleset:
                print("No valid ruleset provided.")
                yield scale_board((current_board_internal * 255).astype(np.uint8))
                time.sleep(0.1)
                continue
            try:
                current_board_internal = automata(current_board_internal, rule=current_ruleset)
                new_raw_frame = (current_board_internal * 255).astype(np.uint8)
                board_state.value = new_raw_frame
                yield scale_board(new_raw_frame)
            except Exception as e:
                print(f"Error during automata step: {e}")
                running.value = False
                yield scale_board((current_board_internal * 255).astype(np.uint8))
                break
            time.sleep(0.05)

        print("Simulation loop stopped.")
        yield scale_board(board_state.value)

    def handle_pause():
        print("Pausing simulation...")
        running.value = False

    def handle_restart(desired_size_tuple):
        """Stops simulation, initializes new board of desired size, updates state, returns scaled board."""
        print(f"Restart button clicked. Desired size: {desired_size_tuple}")
        running.value = False
        new_raw_board = initialize_board(size_tuple=desired_size_tuple)
        print(f"handle_restart: New raw board shape: {new_raw_board.shape}")
        board_state.value = new_raw_board
        return scale_board(new_raw_board)

    def handle_size_change(new_size_value):
        """Updates the desired size state ONLY."""
        print(f"Board size input submitted: {new_size_value}")
        try:
            new_size_int = int(new_size_value)
            if new_size_int < 10: new_size_int = 10
            elif new_size_int > 500: new_size_int = 500
        except (ValueError, TypeError):
             print("Invalid size input, using default.")
             new_size_int = DEFAULT_BOARD_SIZE

        new_size_tuple = (new_size_int, new_size_int)
        board_size_state.value = new_size_tuple
        print(f"Desired board size state updated to: {new_size_tuple}")

    # MODIFIED: Removed desired_size_tuple from arguments
    def start_simulation_wrapper(current_raw_board, current_ruleset):
        """Checks board size, initializes if needed, then starts simulation_loop."""
        # MODIFIED: Get desired size directly from state inside the function
        desired_size_tuple = board_size_state.value

        print("-" * 20)
        print(f"Start Wrapper Entered.")
        print(f"  Desired size (read directly from state): {desired_size_tuple}") # Updated print
        current_shape = current_raw_board.shape if current_raw_board is not None else None
        print(f"  Current board shape (from board_state input): {current_shape}") # Clarified source

        board_to_start = current_raw_board
        needs_reinit = False
        if current_raw_board is None:
            print("  Current board is None. Needs re-initialization.")
            needs_reinit = True
        elif current_shape != desired_size_tuple:
            print(f"  Board size mismatch ({current_shape} != {desired_size_tuple}). Needs re-initialization.")
            needs_reinit = True

        if needs_reinit:
            print(f"  Initializing new board with size {desired_size_tuple}...")
            board_to_start = initialize_board(size_tuple=desired_size_tuple)
            board_state.value = board_to_start
            print(f"  New board initialized. board_state updated. Shape: {board_to_start.shape}")
        else:
            print("  Board size matches. Starting simulation with current board.")
        print("-" * 20)

        yield from simulation_loop(board_to_start, current_ruleset)

    # --- Component Interactions ---
    ruleset_dropdown.change(
        fn=update_ruleset_string,
        inputs=ruleset_dropdown,
        outputs=custom_ruleset_input
    )

    custom_ruleset_input.change(
        fn=handle_custom_ruleset_input,
        inputs=custom_ruleset_input,
        outputs=None
    )

    board_size_input.submit(
        fn=handle_size_change,
        inputs=board_size_input,
        outputs=None
    )

    # MODIFIED: Removed board_size_state from inputs
    start_btn.click(
        fn=start_simulation_wrapper,
        inputs=[board_state, ruleset], # Only pass current board and ruleset
        outputs=output_image
    )

    pause_btn.click(
        fn=handle_pause,
        inputs=None,
        outputs=None
    )

    restart_btn.click(
        fn=handle_restart,
        inputs=board_size_state,
        outputs=output_image
    )

if __name__ == "__main__":
    demo.launch()
