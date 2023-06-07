import pygame  # To use pygame
import time  # To get the time

# Game
START_POSITIONS = [(600, 165)]  # Start position
START_TIME = time.time()  # Start time of the game
RADIUS_CHECKPOINT = 80  # Radius of the checkpoint

CLOCK = pygame.time.Clock()  # Clock
FPS = 144  # Frame per second

KEYBOARD_CONTROL = False  # True to control the car with the keyboard
SEE_CURSOR = False  # True to see the cursor position and color when clicking
SEED = 69  # Seed of the random (None to not use a seed)

# Display
pygame.init()  # Pygame initialization
info = pygame.display.Info()  # Get the screen size
WINDOW_SIZE = WIDTH_SCREEN, HEIGHT_SCREEN = 1500, 700  # Screen size (small to avoid lag)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Initialization of the window
pygame.display.set_caption("Genetic algorithm")  # Window title

LARGE_FONT = pygame.font.SysFont("Arial", 30)  # Large font
FONT = pygame.font.SysFont("Arial", 20)  # Font
SMALL_FONT = pygame.font.SysFont("Arial", 10)  # Small font

# Car
CAR_SIZES = [0.15]

MAX_SPEED = 8  # Maximum speed of the car
MIN_SPEED = 1  # Minimum speed of the car
TURN_ANGLE = 5  # Angle of rotation of the car

ACCELERATION = 0.2  # Acceleration of the car
DECELERATION = -1  # Deceleration of the car

# To know what is the speed of the car :
"""
Low speed: speed < MIN_MEDIUM_SPEED
Medium speed: MIN_MEDIUM_SPEED < speed < MIN_HIGH_SPEED
High speed: MIN_HIGH_SPEED < speed
"""
MIN_MEDIUM_SPEED = MAX_SPEED / 3
MIN_HIGH_SPEED = MAX_SPEED / 3 * 2

# Cone
WIDTH_MULTIPLIER = 15  # Width multiplier of the cone
HEIGHT_MULTIPLIER = 17  # Height multiplier of the cone

# Genetic algorithm
MUTATION_CHANCE = 0.1  # Chance of mutation
CROSSOVER_CHANCE = 0.1  # Chance of crossover

TIME_GENERATION = 25  # Time of a generation (s)
