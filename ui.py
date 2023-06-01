import pygame  # To use pygame
import sys  # To quit the game
import variables  # Import the variables
from constants import WINDOW, FONT  # Import the window
from button import Button  # Import the button

DEBUG_BUTTON = Button(1435, 642, pygame.image.load("images/checkbox_1.png"), pygame.image.load("images/checkbox_2.png"),
                      pygame.image.load("images/checkbox_3.png"), check_box=True, scale=0.03)
STOP_BUTTON = Button(1400, 20, pygame.image.load("images/stop_button.png"), scale=0.15)
START_BUTTON = Button(1300, 15, pygame.image.load("images/start_button.png"), scale=0.18)


def detect_events_ui():
    """
    Detect events in the ui and do the corresponding action
    """
    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Quit the game
        # Detection of clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Click at position", pygame.mouse.get_pos())  # Print the position of the click
            print("Color of the pixel", WINDOW.get_at(pygame.mouse.get_pos()))  # Print the color of the pixel

    # Button events
    draw_buttons()  # Draw the buttons and do the corresponding action


def edit_background():
    """
    Initialize the ui by adding elements to the BACKGROUND
    """
    # Add a text for the debug mode
    variables.BACKGROUND.blit(FONT.render("Debug mode :", True, (255, 255, 255), (0, 0, 0)), (1300, 640))  # Add the text to the screen
    line = pygame.draw.line(variables.BACKGROUND, (0, 0, 0), (1280, 120), (1280, 0), 2)


def draw_buttons():
    """
    Draw the buttons
    """
    variables.DEBUG = DEBUG_BUTTON.draw()  # Draw the debug button
    variables.PLAY = not STOP_BUTTON.draw()  # Draw the stop button
    variables.START = START_BUTTON.draw()  # Draw the start button
