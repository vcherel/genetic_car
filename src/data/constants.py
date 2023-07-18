import os.path  # To get the path of the file

"""
This file contains all the constants of the game used in multiple other files
"""

# Debug
CHANGE_CHECKPOINTS = False  # Change the checkpoint for the actual map
RGB_VALUES_DICE = [(220, 220, 0), (250, 120, 0), (204, 0, 0), (240, 170, 25), (0, 175, 0), (0, 0, 0), (255, 255, 255)]
# The order is: yellow, orange, red, dark_yellow, green, black

# The different colors of the cars (black, blue, brown, gray, light_blue, light_green, orange, pink, purple)
CAR_COLORS = {'black': (0, 0, 0), 'blue': (0, 0, 255), 'brown': (153, 76, 0), 'gray': (128, 128, 128), 'light_blue': (0, 255, 255),
              'light_green': (0, 255, 0), 'orange': (255, 128, 0), 'pink': (204, 0, 204), 'purple': (102, 0, 204)}

START_POSITIONS = [(718, 168), (760, 180), (355, 184), (725, 165), (734, 241), (820, 395)]  # Start position
CAR_SIZES = [13, 10, 12, 9, 15, 15]  # Size of the cars

PATH_DATA = os.path.dirname(__file__) + '/../../data'  # Path of the data folder
PATH_IMAGE = os.path.dirname(__file__) + '/../../images'  # Path of the image folder
