import time  # To get the time
import pygame  # To use pygame
import variables  # Import the variables
from constants import WINDOW, FONT, CLOCK, SMALL_FONT, SEE_CURSOR  # Import constants
from garage import init_garage, display_garage, erase_garage  # Import functions from garage
from display import display_text_ui  # Import functions from display
from utils import exit_game  # Import the exit_game function
from button import Button  # Import the button

debug_button = Button()  # Button to activate the debug mode
stop_button = Button()  # Button to stop the game
pause_button = Button()  # Button to pause the game
start_button = Button()  # Button to start the game
nb_cars_button = Button()  # Button to change the number of cars
garage_button = Button()  # Button to open the garage
text_nb_cars = Button()  # Text to display the number of cars


def init_ui():
    global debug_button, stop_button, pause_button, start_button, nb_cars_button, garage_button, text_nb_cars
    # Buttons
    debug_button = Button(1435, 642, pygame.image.load("images/checkbox_1.png"),
                          pygame.image.load("images/checkbox_2.png"),
                          pygame.image.load("images/checkbox_3.png"), check_box=True, scale=0.03)
    stop_button = Button(1420, 4, pygame.image.load("images/stop_button.png"), scale=0.1)
    pause_button = Button(1417, 56, pygame.image.load("images/pause_button.png"), check_box=True, scale=0.11)
    start_button = Button(1310, 15, pygame.image.load("images/start_button.png"), scale=0.18)
    nb_cars_button = Button(1049, 58, pygame.image.load("images/writing_rectangle_1.png"),
                            pygame.image.load("images/writing_rectangle_2.png"),
                            pygame.image.load("images/writing_rectangle_3.png"), writing_rectangle=True, scale=0.8)
    garage_button = Button(400, 30, pygame.image.load("images/garage_button.png"), scale=0.2, check_box=True)

    # Texts
    text_nb_cars = FONT.render(variables.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Add the debug text


def detect_events_ui():
    """
    Detect events in the ui and do the corresponding action
    """
    global text_nb_cars

    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_game()  # Quit the game
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
                        print("Erreur sur la valeur du nombre de voitures")
                        variables.NB_CARS = 0
                        variables.STR_NB_CARS = "0"  # Reset the text

                    variables.STR_NB_CARS = str(variables.NB_CARS)  # Reset the text
                    variables.CHANGE_NB_CARS = False  # Stop the change of the nb cars
                    nb_cars_button.activate_button()  # Uncheck the button
                    text_nb_cars = FONT.render(variables.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Change the text one last time

                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character
                    variables.STR_NB_CARS = variables.STR_NB_CARS[:-1]
                else:
                    # Append the entered character to the text
                    variables.STR_NB_CARS += event.unicode


def detect_buttons_click():
    """
    Draw the buttons and change the state of the variables
    """
    global text_nb_cars

    # Debug button
    variables.DEBUG = debug_button.check_state()  # Draw the debug button
    if debug_button.just_clicked and not variables.DEBUG:
        WINDOW.blit(variables.BACKGROUND, (0, 0))  # We redraw the background

    # Stop button
    stop_button.check_state()  # Draw the stop button
    if stop_button.just_clicked:
        if variables.PLAY:
            variables.PLAY = False  # We stop the simulation
        if variables.DISPLAY_GARAGE:
            delete_garage()

    # Pause button
    variables.PAUSE = pause_button.check_state()  # Draw the pause button
    if pause_button.just_clicked:  # Pause button is just clicked
        if variables.PAUSE:
            pause(from_button=True)  # We pause the simulation
        else:
            unpause(from_button=True)  # We unpause the simulation

    # Start button
    variables.START = start_button.check_state()  # Draw the start button
    if start_button.just_clicked:
        variables.PLAY = True  # We start the simulation
        if variables.DISPLAY_GARAGE:
            delete_garage()  # We erase the garage
    if variables.START and variables.PAUSE:    # We also resume the simulation if the start button is pressed
        unpause()  # We unpause the simulation

    # Nb cars button
    variables.CHANGE_NB_CARS = nb_cars_button.check_state()  # Draw the nb cars button
    if variables.CHANGE_NB_CARS:
        text_nb_cars = FONT.render(variables.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Add the debug text
    WINDOW.blit(text_nb_cars, (1200, 62))  # Draw the text of the nb cars button

    # FPS
    WINDOW.blit(SMALL_FONT.render("FPS : " + str(int(CLOCK.get_fps())), True, (0, 0, 0), (128, 128, 128)), (1, 1))

    # Time remaining
    if not variables.PLAY:
        time_remaining = variables.TIME_REMAINING
    elif variables.PAUSE:
        time_remaining = variables.TIME_REMAINING_PAUSE
    else:
        time_remaining = int(variables.TIME_REMAINING + variables.DURATION_PAUSES - (time.time() - variables.START_TIME)) + 1  # We add 1 to the time remaining to avoid the 0
    if time_remaining < 0:
        time_remaining = 0
    display_text_ui("Temps restant : " + str(time_remaining) + "s", (1, 20))

    # Num generation and nb cars alive
    display_text_ui("Nombre de voitures restantes : " + str(variables.NB_CARS_ALIVE), (1, 50))
    display_text_ui("Génération : " + str(variables.NUM_GENERATION), (1, 80))

    # Garage
    variables.DISPLAY_GARAGE = garage_button.check_state()  # Draw the garage button
    if garage_button.just_clicked:  # Garage button is just clicked
        if variables.DISPLAY_GARAGE:
            pause()
            init_garage()
        else:
            unpause()
            delete_garage()

    if variables.DISPLAY_GARAGE:  # If the garage is displayed we draw it and do the actions
        display_garage()


def pause(from_button=False):
    """
    To pause the simulation

    Args:
        from_button (bool): If the pause is from the pause button
    """
    if not from_button:  # If the pause is not from the pause button we have to check the button
        variables.PAUSE = True  # We pause the simulation
        pause_button.deactivate_button()  # We check the pause button

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
        pause_button.activate_button()  # We uncheck the pause button

    if variables.DISPLAY_GARAGE:
        delete_garage()

    variables.DURATION_PAUSES += time.time() - variables.START_TIME_PAUSE  # We add the duration of the pause to the total duration of the pause


def delete_garage():
    variables.DISPLAY_GARAGE = False
    garage_button.activated = False
    erase_garage()