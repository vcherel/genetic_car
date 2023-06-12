import time  # To use time
import sys  # To quit the game
import pygame  # To use pygame
from constants import CAR_SIZES, TIME_GENERATION, START_POSITIONS, WINDOW_SIZE  # Import the screen size
from utils import scale_image, convert_to_grayscale  # Import the utils functions
from genetic import Genetic  # Import the Genetic class

# Pygame variables
WINDOW = None  # Window of the game
FONT = None  # Font of the game
SMALL_FONT = None  # Small font of the game
LARGE_FONT = None  # Big font of the game
CLOCK = None  # Clock of the game

# Map variables
BACKGROUND = None  # Image of the background
BACKGROUND_MASK = None    # Mask of the black pixels of the background (used to detect collisions)
NUM_MAP = 0  # Number of the map
START_POSITION = None  # Start position of the car
RED_CAR_IMAGE = None  # Image of the original car
GREY_CAR_IMAGE = None  # Image of the car in view only mode

# Debug variables
DEBUG = False  # True for debug mode, False for normal mode
CHANGE_CHECKPOINT = False  # Change the checkpoint for the actual map
SEE_CHECKPOINTS = False  # See the checkpoints
CHECKPOINTS = None  # List of checkpoints

# Game variables
START = False  # Start the game (True or False)
PLAY = False  # Stop the game (True or False)
ACTUAL_FPS = 0  # Actual FPS

# Pause variables
PAUSE = False  # Pause the game (True or False)
DURATION_PAUSES = 0  # Duration of all the pauses
START_TIME_PAUSE = 0  # Time when the game has been paused
TIME_REMAINING_PAUSE = 0  # Time remaining when the game has been paused

# Genetic variables
TIME_REMAINING = 0  # Time remaining for the genetic algorithm
START_TIME = 0  # Start time of the genetic algorithm
USE_GENETIC = True  # True to use the genetic algorithm, False to just play
NUM_GENERATION = 1  # Number of the generation
NB_CARS_ALIVE = 0  # Number of cars alive

# Garage variables
DISPLAY_GARAGE = False  # True to see the garage
GENETICS_FROM_GARAGE = []  # Genetics from the garage
MEMORY_CARS = {"dice": []}  # Memory of the cars
"""
Format of MEMORY_CARS:   {id_run1: [car1, car2, ...], id_run2: [car1, car2, ...], dice: [car1, car2, ...]}
Format of car:   (id, Genetic)
"""
ACTUAL_ID_MEMORY_GENETIC = 1  # Biggest id of the memory for the genetic cars
ACTUAL_ID_MEMORY_DICE = 1  # Biggest id of the memory for the dice cars

# Car variables
NB_CARS = 0  # Number of cars
CHANGE_NB_CARS = False  # Change the number of cars
STR_NB_CARS = ""  # Text of the number of cars

# Screen variables
RECT_BLIT_CAR = pygame.rect.Rect(0, 0, 0, 0)  # Coordinates of the rect used to erase the cars of the screen
RECTS_BLIT_UI = []  # Coordinates of the rects used to erase the ui of the screen

# Dice capture variables
DISPLAY_DICE_MENU = False  # True to see the dice after capturing the dice with the camera
ACTUAL_DICT_DICE = {}  # Actual dict of the dice

DICE_BUTTONS = []           # To store the dice buttons
DICE_VARIABLES = []         # To store the dice variables (the number of dots on each dice)
DICE_STR_VARIABLES = []     # To store the dice variables (the number of dots on each dice in string format)
DICE_TEXTS = []             # To store the dice texts (the number of dots on each dice in pygame text format)
DICE_BOOLS = []             # To store the boolean values of the dice buttons (are we actually changing the dice variable or not)


def exit_game():
    """
    Exit the game
    """
    save_variables()  # Save the cars
    sys.exit()  # Quit pygame


def change_map(num):
    """
    Change the map and all the variables associated

    Args:
        num (int): number of the new map
    """
    global NUM_MAP, BACKGROUND, BACKGROUND_MASK, RED_CAR_IMAGE, GREY_CAR_IMAGE, CHECKPOINTS, START_POSITION
    NUM_MAP = num  # New map number

    BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), WINDOW_SIZE)  # Image of the background
    BACKGROUND_MASK = pygame.mask.from_threshold(BACKGROUND, (0, 0, 0, 255), threshold=(1, 1, 1, 1))  # Mask of the black pixels of the background (used to detect collisions)
    RED_CAR_IMAGE = scale_image(pygame.image.load("images/car.bmp"), CAR_SIZES[NUM_MAP])    # Image of the car
    GREY_CAR_IMAGE = convert_to_grayscale(RED_CAR_IMAGE)  # Image of the car in view only mode (grayscale)

    START_POSITION = START_POSITIONS[NUM_MAP]  # Start position of the car

    CHECKPOINTS = []  # List of checkpoints
    with open("data/checkpoints_" + str(NUM_MAP), "r") as file_checkpoint_read:
        """
        Format of the file checkpoints:
        x1 y1
        x2 y2
        ...
        """
        checkpoints = file_checkpoint_read.readlines()
        for checkpoint in checkpoints:
            a, b = checkpoint.split(" ")
            CHECKPOINTS.append((int(a), int(b)))


def init_variables_pygame():
    """
    Initialize the variables of pygame (window, font, clock, ...)
    """
    global WINDOW, FONT, SMALL_FONT, LARGE_FONT, CLOCK

    pygame.init()  # Pygame initialization
    pygame.display.set_caption("Algorithme génétique")  # Window title

    WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Initialization of the window
    FONT = pygame.font.SysFont("Arial", 20)  # Font of the text
    SMALL_FONT = pygame.font.SysFont("Arial", 10)  # Font of the text
    LARGE_FONT = pygame.font.SysFont("Arial", 30)  # Font of the text
    CLOCK = pygame.time.Clock()  # Clock of the game


def init_variables(nb_cars, replay=False):
    """
    Initialize the variables of the game (number of car alive, time remaining, start time, ...)
    """
    global NB_CARS_ALIVE, TIME_REMAINING, START_TIME, DURATION_PAUSES, DISPLAY_GARAGE, NUM_GENERATION, \
        ACTUAL_ID_MEMORY_GENETIC

    NB_CARS_ALIVE = nb_cars  # Number of cars alive
    TIME_REMAINING = TIME_GENERATION  # Time remaining for the generation
    START_TIME = time.time()  # Start time of the generation
    DURATION_PAUSES = 0  # We initialize the duration of the pause to 0
    DISPLAY_GARAGE = False  # We don't display the garage
    if replay:      # If we replay from the last cars
        NUM_GENERATION += 1
    else:           # If we start a new run
        NUM_GENERATION = 1  # Number of the generation
        ACTUAL_ID_MEMORY_GENETIC += 1  # We increment the id of the memory


def load_variables():
    """
    Load the variables of the game (number of the map, number of cars, cars, ...)
    """
    global NUM_MAP, NB_CARS, STR_NB_CARS, ACTUAL_ID_MEMORY_GENETIC, ACTUAL_ID_MEMORY_DICE

    # We open the file parameters to read the number of the map and the number of cars
    with open("data/parameters", "r") as file_parameters_read:
        """
        Format of the file parameters:
        num_map
        nb_cars
        """
        num_map, nb_cars = file_parameters_read.readlines()
        NUM_MAP = int(num_map)  # Map number
        NB_CARS = int(nb_cars)  # Number of cars
        STR_NB_CARS = nb_cars  # Text of the number of cars

    with open("data/cars", "r") as file_cars_read:
        """
        Format of the file cars:
        name1   width_fast1   height_fast1   width_medium1   height_medium1   width_slow1   height_slow1
        name2   width_fast2   height_fast2   width_medium2   height_medium2   width_slow2   height_slow2
        ...
        
        Format of names for genetic cars:
        run_x_generation_y
        Format of names for dice cars:
        dice_x_number_y
        """
        lines = file_cars_read.readlines()  # We read the file
        for line in lines:
            line = line.split(" ")
            # We add the car to the memory
            id_run = int(line[0].split("_")[1])
            genetic = Genetic(width_fast=int(line[1]), height_fast=int(line[2]), width_medium=int(line[3]),
                              height_medium=int(line[4]), width_slow=int(line[5]), height_slow=int(line[6]))

            if line[0].startswith("run"):   # If it's a genetic car
                id_generation = int(line[0].split("_")[3])  # Id of the generation

                if str(id_run) in MEMORY_CARS:  # If the id of the run is already in the memory
                    MEMORY_CARS[str(id_run)].append((id_generation, genetic))  # We add the car to the memory
                else:  # If the id of the run is not in the memory
                    MEMORY_CARS[str(id_run)] = [(id_generation, genetic)]  # We add the car to the memory

                if id_run >= ACTUAL_ID_MEMORY_GENETIC:  # We change the biggest id of the memory if necessary
                    ACTUAL_ID_MEMORY_GENETIC = id_run + 1

            else:   # If it's a dice car
                MEMORY_CARS.get("dice").append((id_run, genetic))
                if id_run >= ACTUAL_ID_MEMORY_DICE:  # We change the biggest id of the memory if necessary
                    ACTUAL_ID_MEMORY_DICE = id_run + 1


def save_variables():
    """
    Load the variables of the game (number of the map, number of cars, cars, ...)
    """
    # We change the variable in the file parameters
    with open("data/parameters", "w") as file_parameters_write:
        file_parameters_write.write(str(NUM_MAP) + "\n" + str(NB_CARS))

    with open("data/cars", "w") as file_cars_write:
        for key in MEMORY_CARS.keys():
            if key == "dice":
                for car in MEMORY_CARS.get(key):
                    file_cars_write.write("dice_" + str(car[0]) + " " +
                                          str(car[1].width_fast) + " " + str(car[1].height_fast) + " " +
                                          str(car[1].width_medium) + " " + str(car[1].height_medium) + " " +
                                          str(car[1].width_slow) + " " + str(car[1].height_slow) + "\n")
            else:
                for car in MEMORY_CARS.get(key):
                    file_cars_write.write("run_" + str(key) + "_generation_" + str(car[0]) + " " +
                                          str(car[1].width_fast) + " " + str(car[1].height_fast) + " " +
                                          str(car[1].width_medium) + " " + str(car[1].height_medium) + " " +
                                          str(car[1].width_slow) + " " + str(car[1].height_slow) + "\n")
