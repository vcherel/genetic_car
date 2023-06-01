import pygame  # To use pygame
from constants import WIDTH_SCREEN, HEIGHT_SCREEN, CAR_SIZES  # Import the screen size
from utils import scale_image  # Import the scale_image function


MULTIPLE_CARS = True  # True if we want to have multiple cars, False if we want to have only one car
DEBUG = False  # True for debug mode, False for normal mode
KEYBOARD_CONTROL = False  # True to control the car with the keyboard
CHANGE_CHECKPOINT = False  # Change the checkpoint for the actual map
START = True  # Start the game (True or False)
PLAY = False  # Stop the game (True or False)

NB_CARS = 50  # Number of cars
NUM_MAP = 0  # Map number

BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
BACKGROUND_MASK = pygame.mask.from_threshold(BACKGROUND, (0, 0, 0, 255), threshold=(1, 1, 1, 1))    # Mask of the black pixels of the background (used to detect collisions)
CAR_IMAGE = scale_image(pygame.image.load("images/car.bmp"), CAR_SIZES[NUM_MAP]).convert_alpha()   # Image of the car


def change_map(num_map):
    """
    Change the map and all the variables associated

    Args:
        num_map (int): number of the new map
    """
    global NUM_MAP, BACKGROUND, BACKGROUND_MASK, CAR_IMAGE
    NUM_MAP = num_map  # New map number

    BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
    BACKGROUND_MASK = pygame.mask.from_threshold(BACKGROUND, (0, 0, 0, 255), threshold=(1, 1, 1, 1))  # Mask of the black pixels of the background (used to detect collisions)
    CAR_IMAGE = scale_image(pygame.image.load("images/car.bmp"), CAR_SIZES[NUM_MAP])    # Image of the car
