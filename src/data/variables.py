from data.constants import NB_MAPS  # Import the constants
import pygame  # To use pygame


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
WINDOW = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN), pygame.RESIZABLE)  # Initialization of the window
BACKGROUND = pygame.Surface((WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
SHOW_HEATMAP = False  # True if we want to see the heatmap
BACKGROUND_MASK = None  # Mask of the black pixels of the background (used to detect collisions)
RECTS_BLIT_UI = []  # Coordinates of the rects used to erase the ui of the screen
RECTS_BLIT_CAR = []  # Coordinates of the rects used to erase the cars of the screen
RED_CAR_IMAGE = None  # Image of the original car
BIG_RED_CAR_IMAGE = None  # Image of the car used in the menus


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
TEXT_LENGTH = LARGE_FONT.render('Longueur', True, (0, 0, 0), (128, 128, 128))  # Text of the length button
TEXT_WIDTH = LARGE_FONT.render('Largeur', True, (0, 0, 0), (128, 128, 128))  # Text of the width button


# GAME
LIST_SEED = [0] * NB_MAPS  # Seed of the game for each map
SEED = None  # Seed of the game for the current map
START = False  # Start the game
PLAY = False  # Play the game
CHANGE_GENERATION = False  # True if we want to change the generation
PLAY_LAST_RUN = False  # True if we want to play the last run again
LAST_RUN_PLAYING = False  # True if we are playing the last run


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


# CAMERA
CAMERA_FRAME = None  # Frame of the camera at the last update (displayed in the dice menu)
RECT_CAMERA_FRAME = pygame.rect.Rect(0, 0, 0, 0)  # Rect of the camera frame (displayed in the dice menu)
NUM_CAMERA = 0  # Number of the camera


# OTHER
FPS = 60  # FPS of the game
ACTUAL_FPS = 60  # Actual FPS
BUTTONS = []  # List of the buttons
