import pygame

# Game
NUM_MAP = 0  # Map number
START_POS = [(0, 0)]  # Start position


# Display
pygame.init()  # Pygame initialization
info = pygame.display.Info()  # Get the screen size
WINDOW_SIZE = WIDTH_SCREEN, HEIGHT_SCREEN = info.current_w - 75, info.current_h - 50  # Screen size (we remove pixels to see the window)
WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Initialization of the window
pygame.display.set_caption("Genetic algorithm")  # Window title

BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".png"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Background


# Car
MAX_SPEED = 5  # Maximum speed of the car
TURN_ANGLE = 5  # Angle of rotation of the car


