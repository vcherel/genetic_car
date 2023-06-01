import pygame  # To use pygame
import time  # To get the time

# Game
START_POS = [(600, 165)]  # Start position
START_TIME = time.time()  # Start time of the game
RADIUS_CHECKPOINT = 80  # Radius of the checkpoint

# Display
pygame.init()  # Pygame initialization
info = pygame.display.Info()  # Get the screen size
WINDOW_SIZE = WIDTH_SCREEN, HEIGHT_SCREEN = 1500, 700  # Screen size (small to avoid lag)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Initialization of the window
pygame.display.set_caption("Genetic algorithm")  # Window title

FONT = pygame.font.SysFont("Arial", 20)  # Font


# Car
CAR_SIZES = [0.15]

MAX_SPEED = 7  # Maximum speed of the car
MIN_SPEED = 0.5  # Minimum speed of the car
TURN_ANGLE = 5  # Angle of rotation of the car

ACCELERATION = 0.07  # Acceleration of the car
DECELERATION = -0.9  # Deceleration of the car

# Cone
WIDTH_MULTIPLIER = 9  # Width multiplier of the cone
HEIGHT_MULTIPLIER = 17  # Height multiplier of the cone

# To know what is the speed of the car :
"""
Low speed: speed < MIN_MEDIUM_SPEED
Medium speed: MIN_MEDIUM_SPEED < speed < MIN_HIGH_SPEED
High speed: MIN_HIGH_SPEED < speed
"""
MIN_MEDIUM_SPEED = MAX_SPEED / 3
MIN_HIGH_SPEED = MAX_SPEED / 3 * 2


