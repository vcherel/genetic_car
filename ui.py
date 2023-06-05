import pygame  # To use pygame
import sys  # To quit the game
import variables  # Import the variables
from constants import WINDOW, FONT, CLOCK, SMALL_FONT  # Import constants
from button import Button  # Import the button

# Buttons
DEBUG_BUTTON = Button(1435, 642, pygame.image.load("images/checkbox_1.png"), pygame.image.load("images/checkbox_2.png"),
                      pygame.image.load("images/checkbox_3.png"), check_box=True, scale=0.03)
STOP_BUTTON = Button(1420, 4, pygame.image.load("images/stop_button.png"), scale=0.1)
PAUSE_BUTTON = Button(1417, 56, pygame.image.load("images/pause_button.png"), check_box=True, scale=0.11)
START_BUTTON = Button(1310, 15, pygame.image.load("images/start_button.png"), scale=0.18)
NB_CARS_BUTTON = Button(1049, 58, pygame.image.load("images/writing_rectangle_1.png"), pygame.image.load("images/writing_rectangle_2.png"),
                        pygame.image.load("images/writing_rectangle_3.png"), writing_rectangle=True, scale=0.8)

# Texts
TEXT_NB_CARS = FONT.render(variables.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Add the debug text


def detect_events_ui():
    """
    Detect events in the ui and do the corresponding action
    """
    global TEXT_NB_CARS

    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Quit the game
        # Detection of clicks
        elif variables.SEE_CURSOR and event.type == pygame.MOUSEBUTTONDOWN:
            print("Click at position", pygame.mouse.get_pos())  # Print the position of the click
            print("Color of the pixel", WINDOW.get_at(pygame.mouse.get_pos()))  # Print the color of the pixel
        if variables.CHANGE_NB_CARS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Process the entered text
                    try:
                        variables.NB_CARS = int(variables.STR_NB_CARS)  # Convert the text to an integer
                    except ValueError:
                        variables.NB_CARS = 0
                        variables.STR_NB_CARS = "0"  # Reset the text

                    variables.STR_NB_CARS = str(variables.NB_CARS)  # Reset the text
                    variables.CHANGE_NB_CARS = False  # Stop the change of the nb cars
                    NB_CARS_BUTTON.uncheck_button()  # Uncheck the button
                    TEXT_NB_CARS = FONT.render(variables.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Change the text one last time

                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character
                    variables.STR_NB_CARS = variables.STR_NB_CARS[:-1]
                else:
                    # Append the entered character to the text
                    variables.STR_NB_CARS += event.unicode


def activate_ui():
    """
    Draw the buttons and change the state of the variables
    """
    global TEXT_NB_CARS

    variables.DEBUG = DEBUG_BUTTON.activate()  # Draw the debug button
    variables.PLAY = not STOP_BUTTON.activate()  # Draw the stop button
    pause_before = variables.PAUSE
    variables.PAUSE = PAUSE_BUTTON.activate()  # Draw the pause button
    if pause_before and not variables.PAUSE:  # If the pause button is unchecked, we resume the simulation and blit the screen
        WINDOW.blit(variables.BACKGROUND, (0, 0))

    variables.START = START_BUTTON.activate()  # Draw the start button
    if variables.START and variables.PAUSE:    # We also resume the simulation if the start button is pressed
        PAUSE_BUTTON.uncheck_button()
        variables.PAUSE = False

    variables.CHANGE_NB_CARS = NB_CARS_BUTTON.activate()  # Draw the nb cars button
    if variables.CHANGE_NB_CARS:
        TEXT_NB_CARS = FONT.render(variables.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Add the debug text
    WINDOW.blit(TEXT_NB_CARS, (1200, 62))  # Draw the text of the nb cars button

    # Display the FPS
    WINDOW.blit(SMALL_FONT.render("FPS : " + str(int(CLOCK.get_fps())), True, (0, 0, 0), (128, 128, 128)), (1, 1))
