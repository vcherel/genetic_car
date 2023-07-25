from src.data.constants import START_POSITIONS, CAR_SIZES, PATH_IMAGE, PATH_DATA, START_ANGLES, NB_MAPS  # Import the constants
from src.other.utils import scale_image, convert_to_new_window  # Import the utils functions
from src.render.display import edit_background  # Import the display functions
from src.menus.settings_menu import SETTINGS  # Import the Settings class
from src.data.data_classes import MemoryCar  # Import the MemoryCar class
from src.game.genetic import Genetic  # Import the Genetic class
import pygame  # To use pygame
import sys  # To quit the game


"""
This file contains all the data of the game used in multiple other files
"""


# PYGAME
pygame.init()  # Pygame initialization
pygame.display.set_caption('Algorithme génétique')  # Window title
# Fonts used in the application
VERY_SMALL_FONT = pygame.font.SysFont('Arial', 10)
SMALL_FONT = pygame.font.SysFont('Arial', 17)
FONT = pygame.font.SysFont('Arial', 20)
LARGE_FONT = pygame.font.SysFont('Arial', 30)


# DISPLAY
WIDTH_SCREEN, HEIGHT_SCREEN = 1500, 700  # Screen size
BACKGROUND = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
BACKGROUND_MASK = None  # Mask of the black pixels of the background (used to detect collisions)
RECTS_BLIT_UI = []  # Coordinates of the rects used to erase the ui of the screen
RECTS_BLIT_CAR = []  # Coordinates of the rects used to erase the cars of the screen


# EXPLOSIONS
SHOW_EXPLOSIONS = True  # True if we want to see the explosions
EXPLOSIONS = pygame.sprite.Group()  # Group of all the explosions
EXPLOSION_IMAGES = []  # List of all the images of the explosion
RECTS_BLIT_EXPLOSION = []  # Coordinates of the rects used to erase the explosions of the screen


# RESIZE
RESIZE = False  # True if we are resizing the window
TIME_RESIZE = 0  # Time when we started to resize the window
RESIZE_DIMENSIONS = None  # Dimensions of the window after resizing
SCALE_RESIZE_X = 1  # Scale of the window after resizing on the x-axis
SCALE_RESIZE_Y = 1  # Scale of the window after resizing on the y-axis


# TEXT (for the dice menu)
TEXT_SLOW = LARGE_FONT.render('Lent', True, (255, 255, 0), (128, 128, 128))  # Text of the slow button
TEXT_MEDIUM = LARGE_FONT.render('Moyen', True, (255, 128, 0), (128, 128, 128))  # Text of the medium button
TEXT_FAST = LARGE_FONT.render('Rapide', True, (255, 0, 0), (128, 128, 128))  # Text of the fast button
TEXT_LENGTH = LARGE_FONT.render('Largeur', True, (0, 0, 0), (128, 128, 128))  # Text of the length button
TEXT_WIDTH = LARGE_FONT.render('Longueur', True, (0, 0, 0), (128, 128, 128))  # Text of the width button


# IMAGES
WINDOW = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.RESIZABLE)  # Initialization of the window
RED_CAR_IMAGE = None  # Image of the original car
BIG_RED_CAR_IMAGE = None  # Image of the car used in the menus


# GAME
LIST_SEED = [0] * NB_MAPS  # Seed of the game for each map
SEED = None  # Seed of the game for the current map
START = False  # Start the game
PLAY = False  # Play the game
CHANGE_GENERATION = False  # True if we want to change the generation
PLAY_LAST_RUN = False  # True if we want to play the last run again


# CARS
START_POSITION = None  # Start position of the car
START_ANGLE = None  # Start angle of the car
NB_CARS_ALIVE = 0  # Number of cars alive
LIST_NB_CARS = [30] * NB_MAPS  # Number of cars for each map
NB_CARS = None  # Number of cars for the current map
CARS_LAST_RUN = []  # Cars of the last run
LIST_DRIFT_FACTOR = [2.0] * NB_MAPS  # Factor of the drift for each map
DRIFT_FACTOR = None  # Factor of the drift for the current map


# CHARACTERISTICS CARS
LIST_WIDTH_CONE = [16] * NB_MAPS  # Width multiplier of the cone for each map
WIDTH_CONE = None  # Width multiplier of the cone for the current map
LIST_LENGTH_CONE = [11] * NB_MAPS  # Length multiplier of the cone for each map
LENGTH_CONE = None  # Length multiplier of the cone for the current map
LIST_MAX_SPEED = [9] * NB_MAPS  # Maximum speed of the car for each map
MAX_SPEED = None  # Maximum speed of the car for the current map
MIN_MEDIUM_SPEED = None  # Minimum speed of the car to be considered as medium speed (determined by the maximum speed)
MIN_HIGH_SPEED = None  # Minimum speed of the car to be considered as high speed  (determined by the maximum speed)
LIST_TURN_ANGLE = [8] * NB_MAPS  # Angle of rotation of the car for each map
TURN_ANGLE = None  # Angle of rotation of the car for the current map
LIST_ACCELERATION = [0.1] * NB_MAPS  # Acceleration of the car for each map
ACCELERATION = None  # Acceleration of the car for the current map
LIST_DECELERATION = [0.7] * NB_MAPS  # Deceleration of the car for each map
DECELERATION = None  # Deceleration of the car for the current map


# DEBUG
SHOW_CLICS_INFO = False  # True to see the cursor position and color when clicking
SHOW_DETECTION_CONES = False  # True to see the detection cones of the cars


# TESTS
TEST_ALL_CARS = False  # True to test all the cars
TEST_MUTATION_CROSSOVER = False  # True to test the mutation and crossover
TEST_VALUE_GENETIC_PARAMETERS = False  # True to test the value of the genetic parameters
TEST_FINISHED = False  # True if a car completed a lap
TEST_MODE = ''  # Mode of the test ('mutation_only' or 'crossover_mutation')
FILE_TEST = None  # File to save the results of the tests (it's the same object for all the tests)


# CHECKPOINTS
NUM_MAP = 0  # Number of the map
CHANGE_CHECKPOINTS = False  # Change the checkpoint for the actual map (erase the checkpoints !)
CHECKPOINTS = None  # List of checkpoints for the current map
RADIUS_CHECKPOINT = None  # Radius of the checkpoints
SHOW_CHECKPOINTS = False  # Show the checkpoints and the radius of the checkpoints


# TIME
CLOCK = pygame.time.Clock()  # Clock of the game
PAUSE = False  # True when the game is paused
TICKS_REMAINING = 0  # Iterations remaining for the genetic algorithm
TIME_LAST_TURN = 0  # Time of the last turn (to compute the FPS or limit it)
FPS_TOO_HIGH = False  # True if the FPS is too high (when it's the case we don't play and wait for it to become False)
LAST_TIME_REMAINING = []  # List of the remaining time during the last turns (used to compute the time remaining without changing it too much)


# GENETIC
LIST_TIME_GENERATION = [60] * NB_MAPS  # Time for a generation for each map
TIME_GENERATION = 0  # Time for a generation for the current map
NUM_GENERATION = 1  # Number of the generation (starts at 1)
LIST_CHANCE_MUTATION = [0.3] * NB_MAPS  # Chance of mutation for each map
CHANCE_MUTATION = None  # Chance of mutation for the current map
LIST_CHANCE_CROSSOVER = [0.3] * NB_MAPS  # Chance of crossover for each map
CHANCE_CROSSOVER = None  # Chance of crossover for the current map
LIST_PROPORTION_CARS_KEPT = [0.1] * NB_MAPS  # Percentage used to know how many cars we keep for the next generation for each map
PROPORTION_CARS_KEPT = None  # Percentage used to know how many cars we keep for the next generation for the current map


# MENU
DISPLAY_GARAGE = False  # True if we are displaying the garage menu
DISPLAY_DICE_MENU = False  # True if we are displaying the dice menu
DISPLAY_CAR_WINDOW = False  # True if we are displaying the cone of a car in a window
DISPLAY_SETTINGS = False  # True if we are displaying the settings menu


# MEMORY
MEMORY_CARS = []  # Memory of the cars, format: [car_memory_1, car_memory_2, ...] (used to save the cars of the garage)
SELECTED_MEMORY_CARS = []  # Genetics from the garage that we want to add to the game
ACTUAL_IDS_MEMORY_CARS = 1  # Biggest id of the memory for the dice cars (to know the id of the next car)


# OTHER
FPS = 60  # FPS of the game
ACTUAL_FPS = 60  # Actual FPS
BUTTONS = []  # List of the buttons


def init_variables(nb_cars, replay=False):
    """
    Initialize the data of the game (number of car alive, time remaining, start time, ...)
    """
    global NB_CARS_ALIVE, DISPLAY_GARAGE, NUM_GENERATION, TICKS_REMAINING

    NB_CARS_ALIVE = nb_cars  # Number of cars alive
    TICKS_REMAINING = TIME_GENERATION * 60  # Number of iterations remaining for the generation
    DISPLAY_GARAGE = False  # We don't display the garage
    if replay:  # If we replay from the last cars
        NUM_GENERATION += 1
    else:  # If we start a new run
        NUM_GENERATION = 1  # Number of the generation


def resize_window(dimensions):
    """
    Resize the window (called when the user resizes the window) and change all the data associated

    Args:
        dimensions (tuple): Dimensions of the window
    """
    global WINDOW, WIDTH_SCREEN, HEIGHT_SCREEN, BIG_RED_CAR_IMAGE, EXPLOSION_IMAGES

    WIDTH_SCREEN, HEIGHT_SCREEN = dimensions  # Update the dimensions
    WINDOW = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.RESIZABLE)  # Resize the window
    update_visual_variables()  # Update the visual data
    pygame.display.flip()  # Update the display
    BIG_RED_CAR_IMAGE = pygame.transform.rotate(scale_image(pygame.image.load(PATH_IMAGE + '/car.png'), 1.5), 90)

    load_explosions()  # Load the images of the explosions


def update_visual_variables():
    """
    Update the data used to display things according to the size of the new window
    """
    global SCALE_RESIZE_X, SCALE_RESIZE_Y

    SCALE_RESIZE_X = WIDTH_SCREEN / 1500  # Scale used to resize the images
    SCALE_RESIZE_Y = HEIGHT_SCREEN / 700  # Scale used to resize the images
    create_background()  # Create the background
    WINDOW.blit(BACKGROUND, (0, 0))  # Blit the background on the window
    pygame.display.flip()  # Update the display


def load_explosions():
    """
    Load the images of the explosions
    """
    global EXPLOSION_IMAGES
    EXPLOSION_IMAGES = []  # List of all the images of the explosion
    for num in range(1, 10):
        image = pygame.image.load(f'{PATH_IMAGE}explosion/{num}.png')  # Load the image
        image = scale_image(image, CAR_SIZES[NUM_MAP] / 25 * SCALE_RESIZE_X)  # Scale the image
        EXPLOSION_IMAGES.append(image)


def change_map(first_time=False, reverse=False):
    """
    Change the map and all the data associated. It is used at the beginning of the game and when we press the button to change the map
    When it's the first time we keep the actual map but when it's not the case we change the map to the next one

    Args:
        first_time (bool): True if it's the first time we change the map
        reverse (bool): True if we want to go to the previous map
    """
    global NUM_MAP, START_POSITION, START_ANGLE, RADIUS_CHECKPOINT, BACKGROUND_MASK, RED_CAR_IMAGE, CHECKPOINTS

    if not first_time:  # We change the number of the map only if it's not the first time
        if not reverse:
            if NUM_MAP >= NB_MAPS - 1:
                NUM_MAP = 0
            else:
                NUM_MAP += 1
        else:
            if NUM_MAP == 0:
                NUM_MAP = NB_MAPS - 1
            else:
                NUM_MAP -= 1

        blit_circuit()  # Blit the circuit on the background surface


    START_POSITION = START_POSITIONS[NUM_MAP]  # Start position of the cars
    START_ANGLE = START_ANGLES[NUM_MAP]  # Start angle of the cars
    RADIUS_CHECKPOINT = 7.5 * CAR_SIZES[NUM_MAP]  # Radius of the checkpoints

    # We create a background to create the mask of collision, this background has a size of 1500*700
    background = pygame.Surface((1500, 700))  # Image of the background
    background.blit(pygame.transform.scale(pygame.image.load(f'{PATH_IMAGE}/background_{str(NUM_MAP)}.png'), (1500, 585)), (0, 115))  # Blit the circuit on the background surface
    BACKGROUND_MASK = pygame.mask.from_threshold(background, (0, 0, 0, 255), threshold=(1, 1, 1, 1))  # Mask of the black pixels of the background (used to detect collisions)

    RED_CAR_IMAGE = scale_image(pygame.image.load(PATH_IMAGE + 'car.png'), CAR_SIZES[NUM_MAP] / 75)  # Image of the car
    create_background()  # Create the background
    WINDOW.blit(BACKGROUND, (0, 0))  # Screen initialization

    CHECKPOINTS = []  # List of checkpoints
    with open(PATH_DATA + 'checkpoints_' + str(NUM_MAP), 'r') as file_checkpoint_read:
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

    update_cars_parameters()  # Update all the parameters of the cars


def update_cars_parameters():
    """
    Update the parameters of the cars according to the map
    """
    global NB_CARS, TIME_GENERATION, SEED, MAX_SPEED, MIN_MEDIUM_SPEED, MIN_MEDIUM_SPEED, MIN_HIGH_SPEED, TURN_ANGLE,\
        ACCELERATION, DECELERATION, DRIFT_FACTOR, WIDTH_CONE, LENGTH_CONE, CHANCE_CROSSOVER, CHANCE_MUTATION, PROPORTION_CARS_KEPT

    NB_CARS = LIST_NB_CARS[NUM_MAP]  # Number of cars for the current map
    TIME_GENERATION = LIST_TIME_GENERATION[NUM_MAP]  # Time of a generation for the current map
    SEED = LIST_SEED[NUM_MAP]  # Seed of the game for the current map
    MAX_SPEED = LIST_MAX_SPEED[NUM_MAP]  # Maximum speed of the car for the current map
    MIN_MEDIUM_SPEED = MAX_SPEED / 3  # Minimum speed of the car to be considered as medium speed
    MIN_HIGH_SPEED = MAX_SPEED / 1.5  # Minimum speed of the car to be considered as high speed
    TURN_ANGLE = LIST_TURN_ANGLE[NUM_MAP]  # Angle of rotation of the car for the current map
    ACCELERATION = LIST_ACCELERATION[NUM_MAP]  # Acceleration of the car for the current map
    DECELERATION = LIST_DECELERATION[NUM_MAP]  # Deceleration of the car for the current map
    DRIFT_FACTOR = LIST_DRIFT_FACTOR[NUM_MAP]  # Factor of the drift for the current map
    WIDTH_CONE = LIST_WIDTH_CONE[NUM_MAP]  # Width multiplier of the cone for the current map
    LENGTH_CONE = LIST_LENGTH_CONE[NUM_MAP]  # Length multiplier of the cone for the current map
    CHANCE_CROSSOVER = LIST_CHANCE_CROSSOVER[NUM_MAP]  # Chance of crossover for the current map
    CHANCE_MUTATION = LIST_CHANCE_MUTATION[NUM_MAP]  # Chance of mutation for the current map
    PROPORTION_CARS_KEPT = LIST_PROPORTION_CARS_KEPT[NUM_MAP]  # Percentage used to know how many cars we keep for the next generation for the current map

    if SETTINGS.x is not None:  # If the settings window has been initialized
        SETTINGS.update_parameters()  # Update the settings parameters


def create_background():
    """
    Create the background
    This background will be shown but will not be used to detect collisions
    """
    global BACKGROUND

    BACKGROUND = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
    BACKGROUND.fill((128, 128, 128))  # Fill the background with grey
    edit_background()  # Edit the background
    blit_circuit()  # Blit the circuit on the background surface


def blit_circuit():
    """
    Blit the circuit on the background surface
    """
    BACKGROUND.blit(pygame.transform.scale(pygame.image.load(f'{PATH_IMAGE}background_{str(NUM_MAP)}.png'),
                                           convert_to_new_window((1500, 585))), convert_to_new_window((0, 115)))


def load_parameters():
    """
    Load the parameters of the different maps stored in the file parameters
    """
    with open(PATH_DATA + 'parameters', 'r') as file_parameters_read:
        """
        Format of the file parameters:
        # Circuit x
        param1 = value1
        param2 = value2
        ...
        # Circuit y
        param1 = value1
        ...
        """
        lines = file_parameters_read.readlines()  # We read the file
        actual_map = -1  # Actual map (-1 because we start with the map 0)
        for line in lines:
            if line[0] == '#':
                actual_map += 1  # We change the map
            else:
                line_split = line.split()
                if line_split:
                    param = line.split()[0]
                    if param == 'nombre_voitures':
                        LIST_NB_CARS[actual_map] = int(line.split()[2])
                    elif param == 'temps_par_generation':
                        LIST_TIME_GENERATION[actual_map] = int(line.split()[2])
                    elif param == 'seed':
                        LIST_SEED[actual_map] = int(line.split()[2])
                    elif param == 'vitesse_max':
                        LIST_MAX_SPEED[actual_map] = int(line.split()[2])
                    elif param == 'angle_rotation':
                        LIST_TURN_ANGLE[actual_map] = int(line.split()[2])
                    elif param == 'force_acceleration':
                        LIST_ACCELERATION[actual_map] = float(line.split()[2])
                    elif param == 'force_freinage':
                        LIST_DECELERATION[actual_map] = float(line.split()[2])
                    elif param == 'coef_derapage':
                        LIST_DRIFT_FACTOR[actual_map] = float(line.split()[2])
                    elif param == 'largeur_cone':
                        LIST_WIDTH_CONE[actual_map] = int(line.split()[2])
                    elif param == 'longueur_cone':
                        LIST_LENGTH_CONE[actual_map] = int(line.split()[2])
                    elif param == 'chance_croisement':
                        LIST_CHANCE_CROSSOVER[actual_map] = float(line.split()[2])
                    elif param == 'chance_mutation':
                        LIST_CHANCE_MUTATION[actual_map] = float(line.split()[2])
                    elif param == 'proportion_selection':
                        LIST_PROPORTION_CARS_KEPT[actual_map] = float(line.split()[2])


def load_cars():
    """
    Load the cars stored in the file cars (and initialize the big red car image)
    """
    global ACTUAL_IDS_MEMORY_CARS, BIG_RED_CAR_IMAGE

    with open(PATH_DATA + 'cars', 'r') as file_cars_read:
        """
        Format of the file cars:
        id name color width_fast  length_slow  length_medium  length_fast  width_slow  width_medium  width_fast score_map1  score_map2  score_map3  score_map4  score_map5
        ...
        """
        lines = file_cars_read.readlines()  # We read the file
        for line in lines:
            line = line.split(' ')

            id_car = int(line[0])  # Id of the car (unique int)
            name = line[1]  # Name of the car
            color = line[2]  # Color of the car
            genetic = Genetic([int(line[i]) for i in range(3, 9)])  # Genetic of the car
            scores = [int(line[i]) for i in range(9, 9 + NB_MAPS)]  # Scores of the car for each map

            MEMORY_CARS.append(MemoryCar(id_car, name, color, genetic, scores))  # We create the memory car
            if ACTUAL_IDS_MEMORY_CARS <= id_car:
                ACTUAL_IDS_MEMORY_CARS = id_car + 1

    # We load the image of the car (we do it here because we have to do it during the initialization of the game so why not)
    BIG_RED_CAR_IMAGE = pygame.transform.rotate(scale_image(pygame.image.load(PATH_IMAGE + '/car.png'), 1.5), 90)


def save_cars():
    """"
    Save the cars in the file cars
    """
    with open(PATH_DATA + 'cars', 'w') as file_cars_write:
        for memory_car in MEMORY_CARS:
            str_to_write = f'{memory_car.id} {memory_car.name} {memory_car.color} {memory_car.genetic}'
            for score in memory_car.best_scores:
                str_to_write += f' {int(score)}'  # We cast to int because it can be a float vor the waiting map
            str_to_write += '\n'
            file_cars_write.write(str_to_write)


def add_to_rects_blit_ui(rect, offset=0):
    """
    Add a rect to the list of rects used to erase the ui of the screen
    (we increase the size of the rect, so we don't see the borders left on the screen)

    Args:
        rect (pygame.Rect): Rect to add
        offset (int): Offset to add to the rect
    """
    rect_to_add = pygame.Rect(rect.x, rect.y, rect.width + offset, rect.height + offset)  # Rect to add
    RECTS_BLIT_UI.append(rect_to_add)  # We add the rect to the list


def exit_game():
    """
    Exit the game
    """
    save_cars()  # Save the cars
    sys.exit()  # Quit pygame
