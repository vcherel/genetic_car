import pygame  # To use pygame
import time  # To get the time

# Game
START_POS = [(735, 245)]  # Start position
START_TIME = time.time()  # Start time of the game


# Display
pygame.init()  # Pygame initialization
info = pygame.display.Info()  # Get the screen size
WINDOW_SIZE = WIDTH_SCREEN, HEIGHT_SCREEN = info.current_w - 75, info.current_h - 50  # Screen size (we remove pixels to see the window)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Initialization of the window
pygame.display.set_caption("Genetic algorithm")  # Window title


# Car
CAR_SIZES = [1]

MAX_SPEED = 6  # Maximum speed of the car
TURN_ANGLE = 5  # Angle of rotation of the car

MIN_MEDIUM_SPEED = 2  # Minimum medium speed of the car
MIN_HIGH_SPEED = 4  # Minimum high speed of the car


