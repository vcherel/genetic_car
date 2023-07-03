"""
This file contains all the constants of the game used in multiple other files
"""

# Display
WINDOW_SIZE = WIDTH_SCREEN, HEIGHT_SCREEN = 1500, 700  # Screen size (small to avoid lag)

# Debug
SEE_CURSOR = False  # True to see the cursor position and color when clicking
CHANGE_CHECKPOINTS = False  # Change the checkpoint for the actual map
SEE_CHECKPOINTS = False  # See the checkpoints
USE_GENETIC = True  # True to use the genetic algorithm, False to just play

# Cone
WIDTH_MULTIPLIER = 20  # Width multiplier of the cone
HEIGHT_MULTIPLIER = 17  # Height multiplier of the cone

# Game
TIME_GENERATION = 120  # Time of a generation (s)
SEED = 22  # Seed of the game

RGB_VALUES = [(240, 170, 25), (255, 100, 0), (204, 0, 0), (0, 200, 0), (102, 0, 102), (0, 0, 0)]  # RGB values of the dice
# The order is: dark_yellow, orange, red, green, purple, black
