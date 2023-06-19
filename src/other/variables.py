from src.game.constants import WINDOW_SIZE, WIDTH_MULTIPLIER, HEIGHT_MULTIPLIER, TIME_GENERATION, USE_GENETIC  # Import the constants
from src.other.utils import scale_image, convert_to_grayscale, convert_to_yellow_scale  # Import the utils functions
from src.render.display import edit_background  # Import the display functions
from src.game.genetic import Genetic  # Import the Genetic class
import os.path  # To get the path of the file
import pygame  # To use pygame
import sys  # To quit the game
import time  # To use time

"""
This file contains all the variables of the game used in multiple other files
"""

start_positions = [(600, 165), (760, 180), (600, 197)]  # Start position
car_sizes = [0.13, 0.09, 0.06]  # Size of the car

PATH_DATA = os.path.dirname(__file__) + '/../../data'  # Path of the data folder
PATH_IMAGE = os.path.dirname(__file__) + '/../../images'  # Path of the image folder

# Pygame variables
pygame.init()  # Pygame initialization
pygame.display.set_caption('Algorithme génétique')  # Window title

WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Initialization of the window
FONT = pygame.font.SysFont('Arial', 20)  # Font of the text
SMALL_FONT = pygame.font.SysFont('Arial', 10)  # Font of the text
LARGE_FONT = pygame.font.SysFont('Arial', 30)  # Font of the text
CLOCK = pygame.time.Clock()  # Clock of the game

# Map variables
BACKGROUND = None  # Image of the background
BACKGROUND_MASK = None  # Mask of the black pixels of the background (used to detect collisions)
NUM_MAP = None  # Number of the map
START_POSITION = None  # Start position of the car
RED_CAR_IMAGE = None  # Image of the original car
GREY_CAR_IMAGE = None  # Image of the car in view only mode
YELLOW_CAR_IMAGE = None  # Image of the best car

# Show detection cones
BIG_RED_CAR_IMAGE = pygame.transform.rotate(pygame.image.load(PATH_IMAGE + '/car.bmp'), 90)
TEXT_SLOW = LARGE_FONT.render('Lent', True, (0, 0, 255), (128, 128, 128))  # Text of the slow button
TEXT_MEDIUM = LARGE_FONT.render('Moyen', True, (0, 255, 0), (128, 128, 128))  # Text of the medium button
TEXT_FAST = LARGE_FONT.render('Rapide', True, (255, 0, 0), (128, 128, 128))  # Text of the fast button


# Debug variables
DEBUG = False  # True for debug mode, False for normal mode
CHECKPOINTS = None  # List of checkpoints

TEST_ALL_CARS = False  # True to test_0 all the cars, False to play the game normally
SHOW_ANALYSIS = False  # True to show the analysis of the cars on the checkpoints, False otherwise

# Game variables
START = False  # Start the game (True or False)
PLAY = False  # Stop the game (True or False)
ACTUAL_FPS = 0  # Actual FPS
RECTS_BLIT_UI = []  # Coordinates of the rects used to erase the ui of the screen

# Pause variables
PAUSE = False  # Pause the game (True or False)
DURATION_PAUSES = 0  # Duration of all the pauses
START_TIME_PAUSE = 0  # Time when the game has been paused

# Genetic variables
TIME_REMAINING = 0  # Time remaining for the genetic algorithm
START_TIME = 0  # Start time of the genetic algorithm
NUM_GENERATION = 1  # Number of the generation
NB_CARS_ALIVE = 0  # Number of cars alive

MUTATION_CHANCE = 0.2  # Chance of mutation
CROSSOVER_CHANCE = 0.2  # Chance of crossover
PERCENTAGE_BEST_CARS = 0.2  # Percentage used to know how many cars we keep for the next generation
DECREASE_PERCENTAGE = 0.9  # Percentage used to decrease the mutation and crossover chance

# Garage variables
DISPLAY_GARAGE = False  # True to see the garage
GENETICS_FROM_GARAGE = []  # Genetics from the garage that we want to add to the game
MEMORY_CARS = {'dice': [], 'genetic': []}  # Memory of the cars, Dice are cars from the camera, generation are cars from the genetic algorithm
# Format of MEMORY_CARS:   {"dice": [[id, name, Genetic], ...], "genetic": [[id, name, Genetic], ...]}

ACTUAL_ID_MEMORY_GENETIC = 1  # Biggest id of the memory for the genetic cars
ACTUAL_ID_MEMORY_DICE = 1  # Biggest id of the memory for the dice cars

# Car variables
NB_CARS = 0  # Number of cars
STR_NB_CARS = ''  # Text of the number of cars

PLAY_LAST_RUN = False  # True if we want to play the last run again, False otherwise
CARS_LAST_RUN = []  # Cars of the last run

DISPLAY_DICE_MENU = False  # True if we are displaying the dice menu
DISPLAY_CAR_WINDOW = False  # True if we are displaying the cone of a car


def exit_game():
    """
    Exit the game
    """
    save_variables()  # Save the cars
    sys.exit()  # Quit pygame


def change_map(first_time=False):
    """
    Change the map and all the variables associated

    Args:
        first_time (bool): True if it's the first time we change the map, False otherwise
    """
    global NUM_MAP, BACKGROUND, BACKGROUND_MASK, RED_CAR_IMAGE, GREY_CAR_IMAGE, YELLOW_CAR_IMAGE, CHECKPOINTS, START_POSITION

    # If we change map for the first time, we don't change the map
    if not first_time:
        if NUM_MAP >= len(start_positions) - 1:
            NUM_MAP = 0
        else:
            NUM_MAP += 1

    """
    WINDOW RECT :
    0, 0, 1500, 700
    RACE RECT :
    0, 115, 1500, 585
    """
    BACKGROUND = pygame.Surface(WINDOW_SIZE)  # Image of the background
    BACKGROUND.fill((128, 128, 128))  # Fill the background with grey
    image_circuit = pygame.transform.scale(pygame.image.load(f'{PATH_IMAGE}/background_{str(NUM_MAP)}.png'), (1500, 585))  # Image of the background
    BACKGROUND.blit(image_circuit, (0, 115))  # Blit the image of the background on the background surface
    BACKGROUND_MASK = pygame.mask.from_threshold(BACKGROUND, (0, 0, 0, 255), threshold=(1, 1, 1, 1))  # Mask of the black pixels of the background (used to detect collisions)
    RED_CAR_IMAGE = scale_image(pygame.image.load(PATH_IMAGE + '/car.bmp'), car_sizes[NUM_MAP])  # Image of the car
    GREY_CAR_IMAGE = convert_to_grayscale(RED_CAR_IMAGE)  # Image of the car in view only mode (grayscale)
    YELLOW_CAR_IMAGE = convert_to_yellow_scale(RED_CAR_IMAGE)  # Image of the best car (yellow scale)
    START_POSITION = start_positions[NUM_MAP]  # Start position of the car

    CHECKPOINTS = []  # List of checkpoints
    with open(PATH_DATA + '/checkpoints_' + str(NUM_MAP), 'r') as file_checkpoint_read:
        """
        Format of the file checkpoints:
        x1 y1
        x2 y2
        ...
        """
        checkpoints = file_checkpoint_read.readlines()
        for checkpoint in checkpoints:
            a, b = checkpoint.split(' ')
            CHECKPOINTS.append((int(a), int(b)))

    edit_background()  # Edit the background
    rect = pygame.rect.Rect(0, 115, 1500, 585)  # Only blit the rect where there is the circuit
    WINDOW.blit(BACKGROUND, rect, rect)  # Blit the background on the window


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
    if replay and USE_GENETIC:  # If we replay from the last cars
        NUM_GENERATION += 1
        update_genetic_variables()  # Update the genetic variables
    else:  # If we start a new run
        NUM_GENERATION = 1  # Number of the generation
        ACTUAL_ID_MEMORY_GENETIC += 1  # We increment the id of the memory


def load_variables():
    """
    Load the variables of the game (number of the map, number of cars, cars, ...)
    """
    global NUM_MAP, NB_CARS, STR_NB_CARS, ACTUAL_ID_MEMORY_GENETIC, ACTUAL_ID_MEMORY_DICE

    # We open the file parameters to read the number of the map and the number of cars
    with open(PATH_DATA + '/parameters', 'r') as file_parameters_read:
        """
        Format of the file parameters:
        num_map
        nb_cars
        """
        num_map, nb_cars = file_parameters_read.readlines()
        NUM_MAP = int(num_map)  # Map number
        NB_CARS = int(nb_cars)  # Number of cars
        STR_NB_CARS = nb_cars  # Text of the number of cars

    with open(PATH_DATA + '/cars', 'r') as file_cars_read:
        """
        Format of the file cars:
        id1 type_car1 name1   width_fast1   height_fast1   width_medium1   height_medium1   width_slow1   height_slow1
        id2 type_car2 name2   width_fast2   height_fast2   width_medium2   height_medium2   width_slow2   height_slow2
        ...
        """
        lines = file_cars_read.readlines()  # We read the file
        for line in lines:
            line = line.split(' ')

            id_car = int(line[0])  # Id of the car
            type_car = line[1]  # Type of the car (generation or dice)
            name = line[2]  # Name of the car

            genetic = Genetic(height_slow=int(line[3]), height_medium=int(line[4]), height_fast=int(line[5]),
                              width_slow=int(line[6]), width_medium=int(line[7]), width_fast=int(line[8]))

            MEMORY_CARS.get(type_car).append([id_car, name, genetic])  # We add the car to the memory
            if type_car == 'dice' and id_car >= ACTUAL_ID_MEMORY_DICE:  # We change the biggest id of the memory if necessary
                ACTUAL_ID_MEMORY_DICE = id_car + 1


def save_variables():
    """"
    Load the variables of the game (number of the map, number of cars, cars, ...)
    """
    # We change the variable in the file parameters
    with open(PATH_DATA + '/parameters', 'w') as file_parameters_write:
        file_parameters_write.write(str(NUM_MAP) + "\n" + str(NB_CARS))

    with open(PATH_DATA + '/cars', 'w') as file_cars_write:
        for key in MEMORY_CARS.keys():
            for car in MEMORY_CARS.get(key):
                file_cars_write.write(str(car[0]) + ' ' + key + ' ' + car[1] + ' ' +
                                      str(car[2].height_slow // HEIGHT_MULTIPLIER) + ' ' + str(
                    car[2].height_medium // HEIGHT_MULTIPLIER) + ' ' +
                                      str(car[2].height_fast // HEIGHT_MULTIPLIER) + ' ' + str(
                    car[2].width_slow // WIDTH_MULTIPLIER) + ' ' +
                                      str(car[2].width_medium // WIDTH_MULTIPLIER) + ' ' + str(
                    car[2].width_fast // WIDTH_MULTIPLIER) + '\n')


def update_car_name(type_car, id_car, name):
    """
    Update the name of the car in the memory

    Args:
        type_car: type of the car (generation or dice)
        id_car: id of the car
        name: new name of the car
    """
    for car in MEMORY_CARS.get(type_car):
        if car[0] == id_car:
            car[1] = name
            break


def update_genetic_variables():
    """
    Update the genetic variables of the cars in the memory, it decreases at each round of the game to find the best car
    at the end
    """
    global MUTATION_CHANCE, CROSSOVER_CHANCE, PERCENTAGE_BEST_CARS

    MUTATION_CHANCE *= DECREASE_PERCENTAGE
    CROSSOVER_CHANCE *= DECREASE_PERCENTAGE
    PERCENTAGE_BEST_CARS *= DECREASE_PERCENTAGE
