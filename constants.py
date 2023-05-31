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
CAR_SIZES = [0.2]


MAX_SPEED = 3  # Maximum speed of the car
TURN_ANGLE = 5  # Angle of rotation of the car

ACCELERATION = 0.03  # Acceleration of the car
DECELERATION = 0.08  # Deceleration of the car

# Cone
WIDTH_MULTIPLIER = 10  # Width multiplier of the cone
HEIGHT_MULTIPLIER = 20  # Height multiplier of the cone

# To know what is the speed of the car :
"""
Low speed: 0 < speed < 2
Medium speed: 2 < speed < 4
High speed: 4 < speed < 6
"""
MIN_MEDIUM_SPEED = 2
MIN_HIGH_SPEED = 4


