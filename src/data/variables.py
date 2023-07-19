from src.data.constants import START_POSITIONS, CAR_SIZES, PATH_IMAGE, PATH_DATA  # Import the constants
from src.other.utils import scale_image, convert_to_new_window  # Import the utils functions
from src.render.display import edit_background  # Import the display functions
from src.game.genetic import Genetic  # Import the Genetic class
import pygame  # To use pygame
import sys  # To quit the game

"""
This file contains all the data of the game used in multiple other files
"""

# PYGAME
pygame.init()  # Pygame initialization
pygame.display.set_caption('Algorithme génétique')  # Window title
VERY_SMALL_FONT = pygame.font.SysFont('Arial', 10)  # Font of the text
SMALL_FONT = pygame.font.SysFont('Arial', 17)  # Font of the text
FONT = pygame.font.SysFont('Arial', 20)  # Font of the text
LARGE_FONT = pygame.font.SysFont('Arial', 30)  # Font of the text


# DISPLAY
WIDTH_SCREEN, HEIGHT_SCREEN = 1500, 700  # Screen size
BACKGROUND = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
BACKGROUND_MASK = None  # Mask of the black pixels of the background (used to detect collisions)
RECTS_BLIT_UI = []  # Coordinates of the rects used to erase the ui of the screen
RECTS_BLIT_CAR = []  # Coordinates of the rects used to erase the cars of the screen


# EXPLOSIONS
SEE_EXPLOSIONS = True  # True if we want to see the explosions, False otherwise
EXPLOSIONS = pygame.sprite.Group()  # Group of all the explosions
EXPLOSION_IMAGES = []  # List of all the images of the explosion
RECTS_BLIT_EXPLOSION = []  # Coordinates of the rects used to erase the explosions of the screen


# RESIZE
RESIZE = False  # True if we are resizing the window, False otherwise
TIME_RESIZE = 0  # Time when we started to resize the window
RESIZE_DIMENSIONS = None  # Dimensions of the window after resizing
SCALE_RESIZE_X = 1  # Scale of the window after resizing on the x-axis
SCALE_RESIZE_Y = 1  # Scale of the window after resizing on the y-axis


# TEXT
TEXT_SLOW = LARGE_FONT.render('Lent', True, (255, 255, 0), (128, 128, 128))  # Text of the slow button
TEXT_MEDIUM = LARGE_FONT.render('Moyen', True, (255, 128, 0), (128, 128, 128))  # Text of the medium button
TEXT_FAST = LARGE_FONT.render('Rapide', True, (255, 0, 0), (128, 128, 128))  # Text of the fast button
TEXT_LENGTH = LARGE_FONT.render('Largeur', True, (0, 0, 0), (128, 128, 128))  # Text of the length button
TEXT_WIDTH = LARGE_FONT.render('Longueur', True, (0, 0, 0), (128, 128, 128))  # Text of the width button


# IMAGES
WINDOW = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.RESIZABLE)  # Initialization of the window
RED_CAR_IMAGE = None  # Image of the original car
BIG_RED_CAR_IMAGE = None


# GAME
SEED = None  # Seed of the game
NUM_MAP = 0  # Number of the map
START = False  # Start the game (True or False)
PLAY = False  # Stop the game (True or False)
CHANGE_GENERATION = False  # True if we want to change the generation, False otherwise
PLAY_LAST_RUN = False  # True if we want to play the last run again, False otherwise


# CARS
START_POSITION = None  # Start position of the car
NB_CARS_ALIVE = 0  # Number of cars alive
NB_CARS = 50  # Number of cars
CARS_LAST_RUN = []  # Cars of the last run
DO_DRIFT = True  # True if we want to see the drift of the cars, False otherwise
DRIFT_FACTOR = 2.6  # Factor of the drift


# CHARACTERISTICS CARS
WIDTH_CONE = 16  # Width multiplier of the cone
LENGTH_CONE = 11  # Length multiplier of the cone
MAX_SPEED = 9  # Maximum speed of the car
TURN_ANGLE = 8  # Angle of rotation of the car
ACCELERATION = 0.1  # Acceleration of the car
DECELERATION = 0.6  # Deceleration of the car


# DEBUG
SEE_CURSOR = False  # True to see the cursor position and color when clicking
DEBUG = False  # True for debug mode, False for normal mode


# TESTS
TEST_ALL_CARS = False  # True to test all the cars, False to play the game normally
SHOW_ANALYSIS = False  # True to see the analysis of the tests, False otherwise
TEST_MUTATION_CROSSOVER = False  # True to test the mutation and crossover, False to play the game normally
TEST_VALUE_GENETIC_PARAMETERS = False  # True to test the value of the genetic parameters, False to play the game normally
TEST_FINISHED = False  # True if a car completed a lap, False otherwise
TEST_MODE = ''  # Mode of the test ('mutation_only', 'mutation_crossover', crossover_mutation')
FILE_TEST = None  # File to save the results of the tests


# CHECKPOINTS
CHECKPOINTS = None  # List of checkpoints
RADIUS_CHECKPOINT = None  # Radius of the checkpoints
SEE_CHECKPOINTS = False  # See the checkpoints


# TIME
CLOCK = pygame.time.Clock()  # Clock of the game
PAUSE = False  # Pause the game (True or False)
TICKS_REMAINING = 0  # Iterations remaining for the genetic algorithm
TIME_LAST_TURN = 0  # Time of the last turn
FPS_TOO_HIGH = False  # True if the FPS is too high, False otherwise
LAST_TIME_REMAINING = []  # List of the remaining time during the last turns


# GENETIC
TIME_GENERATION = 60  # Time of a generation
NUM_GENERATION = 1  # Number of the generation
CHANCE_MUTATION = 0.3  # Chance of mutation
CHANCE_CROSSOVER = 0.3  # Chance of crossover
PROPORTION_CARS_KEPT = 0.1  # Percentage used to know how many cars we keep for the next generation


# MENU
DISPLAY_GARAGE = False  # True to see the garage
DISPLAY_DICE_MENU = False  # True if we are displaying the dice menu
DISPLAY_CAR_WINDOW = False  # True if we are displaying the cone of a car
DISPLAY_SETTINGS = False  # True if we are displaying the settings


# MEMORY
CARS_FROM_GARAGE = []  # Genetics from the garage that we want to add to the game
MEMORY_CARS = {'dice': [], 'genetic': []}  # Memory of the cars, Dice are cars from the camera, genetic are cars from the genetic algorithm
# Format of MEMORY_CARS:   {"dice": [[id, name, Genetic, score, color], ...], "genetic": [[id, name, Genetic, score, color], ...]}
ACTUAL_ID_MEMORY_GENETIC = 1  # Biggest id of the memory for the genetic cars
ACTUAL_ID_MEMORY_DICE = 1  # Biggest id of the memory for the dice cars


# OTHER
FPS = 60  # FPS of the game
ACTUAL_FPS = 60  # Actual FPS
BUTTONS = []  # List of the buttons



def exit_game():
    """
    Exit the game
    """
    save_variables()  # Save the cars
    sys.exit()  # Quit pygame


def resize_window(dimensions):
    """
    Resize the window

    Args:
        dimensions (tuple): Dimensions of the window
    """
    global WINDOW, WIDTH_SCREEN, HEIGHT_SCREEN, BACKGROUND

    WIDTH_SCREEN, HEIGHT_SCREEN = dimensions  # Update the dimensions
    WINDOW = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.RESIZABLE)  # Resize the window
    update_visual_variables()  # Update the visual data
    pygame.display.flip()  # Update the display


def change_map(first_time=False):
    """
    Change the map and all the data associated. It is used at the beginning of the game and when we press the button to change the map
    When it's the first time we keep the actual map but when we press the button we change the map to the next one

    Args:
        first_time (bool): True if it's the first time we change the map, False otherwise
    """
    global NUM_MAP, CHECKPOINTS, RADIUS_CHECKPOINT, START_POSITION, BACKGROUND_MASK, RED_CAR_IMAGE, EXPLOSION_IMAGES

    # If we change map for the first time, we don't change the map
    if not first_time:
        if NUM_MAP >= len(START_POSITIONS) - 1:
            NUM_MAP = 0
        else:
            NUM_MAP += 1

    START_POSITION = START_POSITIONS[NUM_MAP]  # Start position of the cars
    RADIUS_CHECKPOINT = 7.5 * CAR_SIZES[NUM_MAP]  # Radius of the checkpoints

    # We create a background to create the mask of collision, this background has a size of 1500*700
    background = pygame.Surface((1500, 700))  # Image of the background
    background.blit(pygame.transform.scale(pygame.image.load(f'{PATH_IMAGE}/background_{str(NUM_MAP)}.png'), (1500, 585)), (0, 115))  # Blit the circuit on the background surface
    BACKGROUND_MASK = pygame.mask.from_threshold(background, (0, 0, 0, 255), threshold=(1, 1, 1, 1))  # Mask of the black pixels of the background (used to detect collisions)

    RED_CAR_IMAGE = scale_image(pygame.image.load(PATH_IMAGE + '/car.png'), CAR_SIZES[NUM_MAP] / 75)  # Image of the car

    EXPLOSION_IMAGES = []  # List of all the images of the explosion
    for num in range(1, 10):
        image = pygame.image.load(f'{PATH_IMAGE}/explosion/{num}.png')  # Load the image
        image = scale_image(image, CAR_SIZES[NUM_MAP] / 25)  # Scale the image
        EXPLOSION_IMAGES.append(image)

    update_visual_variables()  # Update the data used to display things

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


def update_visual_variables():
    """
    Update the data used to display things according to the size of the new window
    """
    global BACKGROUND, START_POSITION, RADIUS_CHECKPOINT, SCALE_RESIZE_X, SCALE_RESIZE_Y

    # This background will be shown but will not be used to detect collisions
    BACKGROUND = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
    BACKGROUND.fill((128, 128, 128))  # Fill the background with grey
    BACKGROUND.blit(pygame.transform.scale(pygame.image.load(f'{PATH_IMAGE}/background_{str(NUM_MAP)}.png'), convert_to_new_window((1500, 585))), convert_to_new_window((0, 115)))  # Blit the circuit on the background surface

    SCALE_RESIZE_X = WIDTH_SCREEN / 1500  # Scale used to resize the images
    SCALE_RESIZE_Y = HEIGHT_SCREEN / 700  # Scale used to resize the images

    edit_background()  # Edit the background
    WINDOW.blit(BACKGROUND, (0, 0))  # Blit the background on the window
    pygame.display.flip()  # Update the display


def init_variables(nb_cars, replay=False):
    """
    Initialize the data of the game (number of car alive, time remaining, start time, ...)
    """
    global NB_CARS_ALIVE, DISPLAY_GARAGE, NUM_GENERATION, ACTUAL_ID_MEMORY_GENETIC, TICKS_REMAINING

    NB_CARS_ALIVE = nb_cars  # Number of cars alive
    TICKS_REMAINING = TIME_GENERATION * 60  # Number of iterations remaining for the generation
    DISPLAY_GARAGE = False  # We don't display the garage
    if replay:  # If we replay from the last cars
        NUM_GENERATION += 1
    else:  # If we start a new run
        NUM_GENERATION = 1  # Number of the generation
        ACTUAL_ID_MEMORY_GENETIC += 1  # We increment the id of the memory


def load_variables():
    """
    Load the data of the game (number of the map, number of cars, cars, ...)
    """
    global NUM_MAP, NB_CARS, FPS, ACTUAL_ID_MEMORY_GENETIC, ACTUAL_ID_MEMORY_DICE, TIME_GENERATION, MAX_SPEED, TURN_ANGLE,\
        ACCELERATION, DECELERATION, CHANCE_MUTATION, CHANCE_CROSSOVER, PROPORTION_CARS_KEPT, SEED, WIDTH_CONE, LENGTH_CONE, BIG_RED_CAR_IMAGE

    # We open the file parameters to read the number of the map and the number of cars
    with open(PATH_DATA + '/parameters', 'r') as file_parameters_read:
        try:
            num_map, nb_cars, fps, time_generation, max_speed, turn_angle, acceleration, deceleration, mutation_chance,\
                crossover_chance, proportion_car_kept, seed, width_cone, length_cone = file_parameters_read.readlines()
        except ValueError:
            # Sometimes the file parameters is not complete, so we complete it
            num_map, nb_cars, fps, time_generation, max_speed, turn_angle, acceleration, deceleration, mutation_chance, \
                crossover_chance, proportion_car_kept, seed, width_cone, length_cone = 0, 50, 60, 60, 9, 8, 0.1, 0.6, 0.3, 0.3, 0.1, 0, 16, 11

        NUM_MAP = int(num_map)  # Map number
        NB_CARS = int(nb_cars)  # Number of cars
        FPS = int(fps)  # FPS
        TIME_GENERATION = int(time_generation)  # Time of a generation
        MAX_SPEED = int(max_speed)  # Max speed of the car
        TURN_ANGLE = int(turn_angle)  # Angle of the turn of the car
        ACCELERATION = float(acceleration)  # Acceleration of the car
        DECELERATION = float(deceleration)  # Deceleration of the car
        CHANCE_MUTATION = float(mutation_chance)  # Chance of mutation
        CHANCE_CROSSOVER = float(crossover_chance)  # Chance of crossover
        PROPORTION_CARS_KEPT = float(proportion_car_kept)  # Proportion of car kept
        SEED = int(seed)  # Seed of the random
        WIDTH_CONE = int(width_cone)  # Width of the cone of vision
        LENGTH_CONE = int(length_cone)  # Length of the cone of vision


    with open(PATH_DATA + '/cars', 'r') as file_cars_read:
        """
        Format of the file cars:
        id  type_car name  width_fast  length_slow  length_medium  length_fast  width_slow  width_medium  width_fast  color  score_map1  score_map2  score_map3  score_map4  score_map5
        id  type_car name  width_fast  length_slow  length_medium  length_fast  width_slow  width_medium  width_fast  color  score_map1  score_map2  score_map3  score_map4  score_map5
        ...
        """
        lines = file_cars_read.readlines()  # We read the file
        for line in lines:
            line = line.split(' ')

            id_car = int(line[0])  # Id of the car
            type_car = line[1]  # Type of the car (generation or dice)
            name = line[2]  # Name of the car

            genetic = Genetic([int(line[i]) for i in range(3, 9)])  # Genetic of the car
            color = line[9]
            score = [int(line[i]) for i in range(10, 10 + len(START_POSITIONS))]  # Score of the car

            MEMORY_CARS.get(type_car).append([id_car, name, genetic, color, score])  # We add the car to the memory
            if type_car == 'dice' and id_car >= ACTUAL_ID_MEMORY_DICE:  # We change the biggest id of the memory if necessary
                ACTUAL_ID_MEMORY_DICE = id_car + 1

    BIG_RED_CAR_IMAGE = pygame.transform.rotate(scale_image(pygame.image.load(PATH_IMAGE + '/car.png'), 1.5), 90)


def save_variables():
    """"
    Load the data of the game (number of the map, number of cars, cars, ...)
    """
    # We change the variable in the file parameters
    with open(PATH_DATA + '/parameters', 'w') as file_parameters_write:
        file_parameters_write.write(f'{NUM_MAP}\n{NB_CARS}\n{FPS}\n{TIME_GENERATION}\n{MAX_SPEED}\n{TURN_ANGLE}\n'
                                    f'{ACCELERATION}\n{DECELERATION}\n{CHANCE_MUTATION}\n{CHANCE_CROSSOVER}\n'
                                    f'{PROPORTION_CARS_KEPT}\n{SEED}\n{WIDTH_CONE}\n{LENGTH_CONE}')

    with open(PATH_DATA + '/cars', 'w') as file_cars_write:
        for key in MEMORY_CARS.keys():
            for memory_car in MEMORY_CARS.get(key):
                """
                Format of memory_car:
                [id_car, name, genetic, color, score]
                """

                str_to_write = f'{memory_car[0]} {key} {memory_car[1]} {memory_car[2].length_slow // LENGTH_CONE}' \
                               f' {memory_car[2].length_medium // LENGTH_CONE} {memory_car[2].length_fast // LENGTH_CONE}' \
                               f' {memory_car[2].width_slow // WIDTH_CONE} {memory_car[2].width_medium // WIDTH_CONE}' \
                               f' {memory_car[2].width_fast // WIDTH_CONE} {memory_car[3]}'

                for score in memory_car[4]:
                    str_to_write += f' {int(score)}'
                str_to_write += '\n'
                file_cars_write.write(str_to_write)


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


def update_car_color(type_car, id_car, color):
    """
    Update the color of the car in the memory

    Args:
        type_car: type of the car (generation or dice)
        id_car: id of the car
        color: new color of the car
    """
    for car in MEMORY_CARS.get(type_car):
        if car[0] == id_car:
            car[3] = color
            break
