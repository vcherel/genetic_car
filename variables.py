import pygame  # To use pygame
from constants import WIDTH_SCREEN, HEIGHT_SCREEN, CAR_SIZES  # Import the screen size
from utils import scale_image  # Import the scale_image function


MODE = "car"  # Mode of the game ("car" for one car, "cars" for multiple cars)
DEBUG = True  # Debug mode (True or False)
START = True  # Start the game (True or False)

NB_CARS = 30  # Number of cars
NUM_MAP = 0  # Map number

BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
CAR_IMAGE = scale_image(pygame.image.load("images/car.jpg"), CAR_SIZES[NUM_MAP])    # Image of the car


def change_map(num_map):
    """
    Change the map

    Args:
        num_map (int): number of the new map
    """
    global NUM_MAP, BACKGROUND, CAR_IMAGE
    NUM_MAP = num_map  # New map number

    BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Image of the background
    CAR_IMAGE = scale_image(pygame.image.load("images/car.jpg"), CAR_SIZES[NUM_MAP])    # Image of the car
