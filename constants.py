import pygame

# Game
NUM_MAP = 1  # Map number

# Display
pygame.init()  # Pygame initialization
info = pygame.display.Info()  # Get the screen size
WINDOW_SIZE = WIDTH_SCREEN, HEIGHT_SCREEN = info.current_w, info.current_h  # Screen size
WINDOW = pygame.display.set_mode(WINDOW_SIZE)  # Initialization of the window
pygame.display.set_caption("Genetic algorithm")  # Window title

BACKGROUND = pygame.transform.scale(pygame.image.load("images/background_" + str(NUM_MAP) + ".bmp"), (WIDTH_SCREEN, HEIGHT_SCREEN))  # Background
