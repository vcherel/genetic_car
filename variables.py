import pygame  # To use pygame
from constants import WIDTH_SCREEN, HEIGHT_SCREEN, CAR_SIZES  # Import the screen size
from utils import scale_image  # Import the scale_image function

DEBUG = False  # True for debug mode, False for normal mode
KEYBOARD_CONTROL = False  # True to control the car with the keyboard
SEE_CURSOR = False  # True to see the cursor position and color when clicking

START = False  # Start the game (True or False)
PLAY = False  # Stop the game (True or False)
PAUSE = False  # Pause the game (True or False)

CHANGE_CHECKPOINT = False  # Change the checkpoint for the actual map
SEE_CHECKPOINTS = False  # See the checkpoints

NUM_MAP = 0  # Map number

NB_CARS = 20  # Number of cars
CHANGE_NB_CARS = False  # Change the number of cars
STR_NB_CARS = str(NB_CARS)  # Text of the number of cars

BACKGROUND = None  # Image of the background
BACKGROUND_MASK = None    # Mask of the black pixels of the background (used to detect collisions)
CAR_IMAGE = None  # Image of the car
CHECKPOINTS = None  # List of checkpoints

USE_GENETIC = True  # True to use the genetic algorithm, False to just play


def change_map(num_map):
    """
    Change the map and all the variables associated

    Args:
        num_map (int): number of the new map
    """
    global NUM_MAP, BACKGROUND, BACKGROUND_MASK, CAR_IMAGE, CHECKPOINTS
    NUM_MAP = num_map  # New map number

    BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
    BACKGROUND_MASK = pygame.mask.from_threshold(BACKGROUND, (0, 0, 0, 255), threshold=(1, 1, 1, 1))  # Mask of the black pixels of the background (used to detect collisions)
    CAR_IMAGE = scale_image(pygame.image.load("images/car.bmp"), CAR_SIZES[NUM_MAP])    # Image of the car

    CHECKPOINTS = []  # List of checkpoints
    with open("data/checkpoints_" + str(NUM_MAP), "r") as file_checkpoint_read:
        checkpoints = file_checkpoint_read.readlines()
        for checkpoint in checkpoints:
            a, b = checkpoint.split(" ")
            CHECKPOINTS.append((int(a), int(b)))
