import pygame  # To use pygame
import sys  # To quit the game
from constants import WINDOW, FONT  # Import the window
from variables import BACKGROUND  # Import the variables
from button import Button  # Import the button


def detect_events():
    """
    Detect events in the ui and do the corresponding action
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Quit the game
        # Detection of clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Click at position", pygame.mouse.get_pos())  # Print the position of the click
            print("Color of the pixel", WINDOW.get_at(pygame.mouse.get_pos()))  # Print the color of the pixel


def edit_background():
    """
    Initialize the ui by adding elements to the BACKGROUND
    """
    # Add a text for the debug mode
    BACKGROUND.blit(FONT.render("Debug mode :", True, (255, 255, 255), (0, 0, 0)), (1300, 640))  # Add the text to the screen
