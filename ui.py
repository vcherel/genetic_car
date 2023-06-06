import sys  # To quit the game
import time  # To get the time
import pygame  # To use pygame
import variables  # Import the variables
from constants import WINDOW, FONT, CLOCK, SMALL_FONT, SEE_CURSOR  # Import constants
from display import display_text_ui, display_garage, erase_garage  # Import functions from display
from button import Button  # Import the button

# Buttons
DEBUG_BUTTON = Button(1435, 642, pygame.image.load("images/checkbox_1.png"), pygame.image.load("images/checkbox_2.png"),
                      pygame.image.load("images/checkbox_3.png"), check_box=True, scale=0.03)
STOP_BUTTON = Button(1420, 4, pygame.image.load("images/stop_button.png"), scale=0.1)
PAUSE_BUTTON = Button(1417, 56, pygame.image.load("images/pause_button.png"), check_box=True, scale=0.11)
START_BUTTON = Button(1310, 15, pygame.image.load("images/start_button.png"), scale=0.18)
NB_CARS_BUTTON = Button(1049, 58, pygame.image.load("images/writing_rectangle_1.png"), pygame.image.load("images/writing_rectangle_2.png"),
                        pygame.image.load("images/writing_rectangle_3.png"), writing_rectangle=True, scale=0.8)
GARAGE_BUTTON = Button(400, 30, pygame.image.load("images/garage_button.png"), scale=0.2, check_box=True)

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
        elif SEE_CURSOR and event.type == pygame.MOUSEBUTTONDOWN:
            print("Click at position", pygame.mouse.get_pos())  # Print the position of the click
            print("Color of the pixel", WINDOW.get_at(pygame.mouse.get_pos()))  # Print the color of the pixel
        if variables.CHANGE_NB_CARS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Process the entered text
                    try:
                        variables.NB_CARS = int(variables.STR_NB_CARS)  # Convert the text to an integer
                        # We change the variable in the file parameters
                        with open("data/parameters", "w") as file_parameters_write:
                            file_parameters_write.write(str(variables.NUM_MAP) + "\n" + str(variables.NB_CARS))
                    except ValueError:
                        variables.NB_CARS = 0
                        variables.STR_NB_CARS = "0"  # Reset the text

                    variables.STR_NB_CARS = str(variables.NB_CARS)  # Reset the text
                    variables.CHANGE_NB_CARS = False  # Stop the change of the nb cars
                    NB_CARS_BUTTON.activate_button()  # Uncheck the button
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

    # Debug button
    variables.DEBUG = DEBUG_BUTTON.activate()  # Draw the debug button
    if DEBUG_BUTTON.just_clicked and not variables.DEBUG:
        WINDOW.blit(variables.BACKGROUND, (0, 0))  # We redraw the background

    # Stop button
    stopped = STOP_BUTTON.activate()  # Draw the stop button
    variables.PLAY = not stopped  # We invert the state of the button
    if STOP_BUTTON.just_clicked and stopped:
        unpause()  # We unpause the simulation
        erase_garage()  # We erase the garage

    # Pause button
    variables.PAUSE = PAUSE_BUTTON.activate()  # Draw the pause button
    if PAUSE_BUTTON.just_clicked:  # Pause button is just clicked
        if variables.PAUSE:
            pause(from_button=True)  # We pause the simulation
        else:
            unpause(from_button=True)  # We unpause the simulation

    # Start button
    variables.START = START_BUTTON.activate()  # Draw the start button
    if variables.START and variables.PAUSE:    # We also resume the simulation if the start button is pressed
        unpause()  # We unpause the simulation
        if variables.DISPLAY_GARAGE:
            erase_garage()

    # Nb cars button
    variables.CHANGE_NB_CARS = NB_CARS_BUTTON.activate()  # Draw the nb cars button
    if variables.CHANGE_NB_CARS:
        TEXT_NB_CARS = FONT.render(variables.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Add the debug text
    WINDOW.blit(TEXT_NB_CARS, (1200, 62))  # Draw the text of the nb cars button

    # FPS
    WINDOW.blit(SMALL_FONT.render("FPS : " + str(int(CLOCK.get_fps())), True, (0, 0, 0), (128, 128, 128)), (1, 1))

    # Time remaining
    if variables.PAUSE:
        time_remaining = variables.TIME_REMAINING_PAUSE
    else:
        time_remaining = int(variables.TIME_REMAINING + variables.DURATION_PAUSES - (time.time() - variables.START_TIME)) + 1  # We add 1 to the time remaining to avoid the 0
    if time_remaining < 0:
        time_remaining = 0
    display_text_ui("Temps restant : " + str(time_remaining) + "s", (1, 20))

    # Num generation and nb cars alive
    display_text_ui("Nombre de voitures restantes : " + str(variables.NB_CARS_ALIVE), (1, 50))
    display_text_ui("Génération : " + str(variables.GENERATION), (1, 80))

    # Garage
    variables.DISPLAY_GARAGE = GARAGE_BUTTON.activate()  # Draw the garage button
    if GARAGE_BUTTON.just_clicked:  # Garage button is just clicked
        if variables.DISPLAY_GARAGE:
            pause()
            display_garage()
        else:
            unpause()
            erase_garage()


def pause(from_button=False):
    """
    To pause the simulation

    Args:
        from_button (bool): If the pause is from the pause button
    """
    if not from_button:  # If the pause is not from the pause button we have to check the button
        variables.PAUSE = True  # We pause the simulation
        PAUSE_BUTTON.deactivate_button()  # We check the pause button

    variables.START_TIME_PAUSE = time.time()  # We get the time when the pause started
    variables.TIME_REMAINING_PAUSE = int(variables.TIME_REMAINING + variables.DURATION_PAUSES - (time.time() - variables.START_TIME)) + 1  # We save the time remaining before the pause


def unpause(from_button=False):
    """
    To unpause the simulation

    Args:
        from_button (bool): If the unpause is from the pause button
    """
    if not from_button:  # If the unpause is not from the pause button we have to uncheck the button
        variables.PAUSE = False  # We unpause the simulation
        PAUSE_BUTTON.activate_button()  # We uncheck the pause button

    variables.DURATION_PAUSES += time.time() - variables.START_TIME_PAUSE  # We add the duration of the pause to the total duration of the pause
