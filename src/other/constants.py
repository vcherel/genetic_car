import os.path  # To get the path of the file

"""
This file contains all the constants of the game used in multiple other files
"""

# Debug
CHANGE_CHECKPOINTS = False  # Change the checkpoint for the actual map

RGB_VALUES_DICE = [(240, 170, 25), (255, 100, 0), (204, 0, 0), (0, 200, 0), (102, 0, 102), (0, 0, 0)]  # RGB values of the dice
# The order is: dark_yellow, orange, red, green, purple, black

# The different colors of the cars (black, blue, brown, gray, light_blue, light_green, orange, pink, purple)
CAR_COLORS = {'black': (0, 0, 0), 'blue': (0, 0, 255), 'brown': (153, 76, 0), 'gray': (128, 128, 128), 'light_blue': (0, 255, 255),
              'light_green': (0, 255, 0), 'orange': (255, 128, 0), 'pink': (204, 0, 204), 'purple': (102, 0, 204)}

START_POSITIONS = [(600, 165), (760, 180), (600, 197), (725, 165), (734, 241), (820, 395)]  # Start position
CAR_SIZES = [0.13, 0.1, 0.06, 0.09, 0.15, 0.11]  # Size of the cars

PATH_DATA = os.path.dirname(__file__) + '/../../data'  # Path of the data folder
PATH_IMAGE = os.path.dirname(__file__) + '/../../images'  # Path of the image folder
