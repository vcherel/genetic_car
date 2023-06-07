import time  # To use time
import pygame  # To use pygame
from constants import WIDTH_SCREEN, HEIGHT_SCREEN, CAR_SIZES, TIME_GENERATION, START_POSITIONS  # Import the screen size
from utils import scale_image, convert_to_grayscale  # Import the utils functions
from genetic import Genetic  # Import the Genetic class

DEBUG = False  # True for debug mode, False for normal mode

CHANGE_CHECKPOINT = False  # Change the checkpoint for the actual map
SEE_CHECKPOINTS = False  # See the checkpoints
CHECKPOINTS = None  # List of checkpoints

RECT_BLIT_CAR = pygame.rect.Rect(0, 0, 0, 0)  # Coordinates of the rect used to erase the cars of the screen
RECTS_BLIT_UI = []  # Coordinates of the rects used to erase the ui of the screen

START = False  # Start the game (True or False)
PLAY = False  # Stop the game (True or False)

PAUSE = False  # Pause the game (True or False)
DURATION_PAUSES = 0  # Duration of all the pauses
START_TIME_PAUSE = 0  # Time when the game has been paused
TIME_REMAINING_PAUSE = 0  # Time remaining when the game has been paused

TIME_REMAINING = 0  # Time remaining for the genetic algorithm
START_TIME = 0  # Start time of the genetic algorithm

NUM_MAP = 0  # Number of the map
START_POSITION = None  # Start position of the car

RED_CAR_IMAGE = None  # Image of the original car
GREY_CAR_IMAGE = None  # Image of the car in view only mode

MEMORY_CARS = {}  # Memory of the cars : {id_run1: [car1, car2, ...], id_run2: [car1, car2, ...], dice: [car1, car2, ...]}
ACTUAL_ID_MEMORY_GENETIC = 0  # Biggest id of the memory for the genetic cars
ACTUAL_ID_MEMORY_DICE = 0  # Biggest id of the memory for the dice cars

NB_CARS = 0  # Number of cars
CHANGE_NB_CARS = False  # Change the number of cars
STR_NB_CARS = ""  # Text of the number of cars

BACKGROUND = None  # Image of the background
BACKGROUND_MASK = None    # Mask of the black pixels of the background (used to detect collisions)


USE_GENETIC = True  # True to use the genetic algorithm, False to just play
NUM_GENERATION = 1  # Number of the generation
NB_CARS_ALIVE = 0  # Number of cars alive

DISPLAY_GARAGE = False  # True to see the garage
GENETICS_FROM_GARAGE = []  # Car from the garage


def change_map(num):
    """
    Change the map and all the variables associated

    Args:
        num (int): number of the new map
    """
    global NUM_MAP, BACKGROUND, BACKGROUND_MASK, RED_CAR_IMAGE, GREY_CAR_IMAGE, CHECKPOINTS, START_POSITION
    NUM_MAP = num  # New map number

    BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
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


def init_variables(nb_cars, replay=False):
    """
    Initialize the variables of the game (number of car alive, time remaining, start time, ...)
    """
    global NB_CARS_ALIVE, TIME_REMAINING, START_TIME, DURATION_PAUSES, DISPLAY_GARAGE, NUM_GENERATION, ACTUAL_ID_MEMORY_GENETIC

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
        lines = file_cars_read.readlines()
        for line in lines:
            line = line.split(" ")
            # We add the car to the memory
            id_run = int(line[0].split("_")[1])
            id_generation = int(line[0].split("_")[3])

            if MEMORY_CARS.get(id_run) is None:
                MEMORY_CARS[id_run] = [(
                    id_generation, Genetic(width_fast=int(line[1]), height_fast=int(line[2]), width_medium=int(line[3]),
                                           height_medium=int(line[4]), width_slow=int(line[5]), height_slow=int(line[6])))]
            else:
                MEMORY_CARS.get(id_run).append(
                    (id_generation, Genetic(width_fast=int(line[1]), height_fast=int(line[2]), width_medium=int(line[3]),
                                            height_medium=int(line[4]), width_slow=int(line[5]), height_slow=int(line[6]))))
            if line[0].startswith("run") and id_run > ACTUAL_ID_MEMORY_GENETIC:  # We change the biggest id of the memory if necessary
                ACTUAL_ID_MEMORY_GENETIC = id_run
            elif line[0].startswith("dice") and id_run > ACTUAL_ID_MEMORY_DICE:
                ACTUAL_ID_MEMORY_DICE = id_run


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
                    file_cars_write.write("dice_" + str(key) + "_number_" + str(car[0]) + " " +
                                          str(car[1].width_fast) + " " + str(car[1].height_fast) + " " +
                                          str(car[1].width_medium) + " " + str(car[1].height_medium) + " " +
                                          str(car[1].width_slow) + " " + str(car[1].height_slow) + "\n")
            else:
                for car in MEMORY_CARS.get(key):
                    file_cars_write.write("run_" + str(key) + "_generation_" + str(car[0]) + " " +
                                          str(car[1].width_fast) + " " + str(car[1].height_fast) + " " +
                                          str(car[1].width_medium) + " " + str(car[1].height_medium) + " " +
                                          str(car[1].width_slow) + " " + str(car[1].height_slow) + "\n")
