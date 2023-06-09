import time  # To get the time
import pygame  # To use pygame
import variables as var  # Import the variables
from constants import SEE_CURSOR, FPS  # Import constants
from garage import init_garage, display_garage, erase_garage  # Import functions from garage
from display import display_text_ui  # Import functions from display
from genetic import Genetic  # Import the genetic class
from button import Button  # Import the button

debug_button = Button()  # Button to activate the debug mode
stop_button = Button()  # Button to stop the game
pause_button = Button()  # Button to pause the game
start_button = Button()  # Button to start the game
nb_cars_button = Button()  # Button to change the number of cars
garage_button = Button()  # Button to open the garage
dice_button = Button()  # Button to see the dice
text_nb_cars = Button()  # Text to display the number of cars


def init_ui():
    global debug_button, stop_button, pause_button, start_button, nb_cars_button, garage_button, dice_button, text_nb_cars
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
    dice_button = Button(600, 28, pygame.image.load("images/dice_button.png"), scale=0.4, check_box=False)

    # Text
    text_nb_cars = var.FONT.render(var.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Add the debug text


def detect_events_ui():
    """
    Detect events in the ui and do the corresponding action
    """
    global text_nb_cars

    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            var.exit_game()  # Quit the game
        # Detection of clicks
        elif SEE_CURSOR and event.type == pygame.MOUSEBUTTONDOWN:
            print("Click at position", pygame.mouse.get_pos())  # Print the position of the click
            print("Color of the pixel", var.WINDOW.get_at(pygame.mouse.get_pos()))  # Print the color of the pixel
        if var.CHANGE_NB_CARS:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Process the entered text
                    try:
                        var.NB_CARS = int(var.STR_NB_CARS)  # Convert the text to an integer
                        # We change the variable in the file parameters
                        with open("data/parameters", "w") as file_parameters_write:
                            file_parameters_write.write(str(var.NUM_MAP) + "\n" + str(var.NB_CARS))
                    except ValueError:
                        print("Erreur sur la valeur du nombre de voitures")
                        var.NB_CARS = 0
                        var.STR_NB_CARS = "0"  # Reset the text

                    var.STR_NB_CARS = str(var.NB_CARS)  # Reset the text
                    var.CHANGE_NB_CARS = False  # Stop the change of the nb cars
                    nb_cars_button.activate_button()  # Uncheck the button
                    text_nb_cars = var.FONT.render(var.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Change the text one last time

                elif event.key == pygame.K_BACKSPACE:
                    # Remove the last character
                    var.STR_NB_CARS = var.STR_NB_CARS[:-1]
                else:
                    # Append the entered character to the text
                    var.STR_NB_CARS += event.unicode


def detect_buttons_click():
    """
    Draw the buttons and change the state of the variables
    """
    global text_nb_cars

    # Debug button
    var.DEBUG = debug_button.check_state()  # Draw the debug button
    if debug_button.just_clicked and not var.DEBUG:
        var.WINDOW.blit(var.BACKGROUND, (0, 0))  # We redraw the background

    # Stop button
    stop_button.check_state()  # Draw the stop button
    if stop_button.just_clicked:
        if var.PLAY:
            var.PLAY = False  # We stop the simulation
        if var.DISPLAY_GARAGE:
            delete_garage()

    # Pause button
    var.PAUSE = pause_button.check_state()  # Draw the pause button
    if pause_button.just_clicked:  # Pause button is just clicked
        if var.PAUSE:
            pause(from_button=True)  # We pause the simulation
        else:
            unpause(from_button=True)  # We unpause the simulation

    # Start button
    var.START = start_button.check_state()  # Draw the start button
    if start_button.just_clicked:
        var.PLAY = True  # We start the simulation
        if var.DISPLAY_GARAGE:
            delete_garage()  # We erase the garage
    if var.START and var.PAUSE:    # We also resume the simulation if the start button is pressed
        unpause()  # We unpause the simulation

    # Nb cars button
    var.CHANGE_NB_CARS = nb_cars_button.check_state()  # Draw the nb cars button
    if var.CHANGE_NB_CARS:
        display_text_ui(var.STR_NB_CARS, (1200, 62), var.FONT, background_color=(255, 255, 255))  # Display the text of the nb cars button
    else:
        var.WINDOW.blit(text_nb_cars, (1200, 62))  # Draw the text of the nb cars button

    # FPS
    if var.PLAY:
        fps = str(var.ACTUAL_FPS)
    else:
        fps = str(int(var.CLOCK.get_fps()))
    display_text_ui("FPS : " + fps, (1, 1), var.SMALL_FONT)

    # Time remaining
    if not var.PLAY:
        time_remaining = var.TIME_REMAINING
    elif var.PAUSE:
        time_remaining = var.TIME_REMAINING_PAUSE
    else:
        time_remaining = int(var.TIME_REMAINING + var.DURATION_PAUSES - (time.time() - var.START_TIME)) + 1  # We add 1 to the time remaining to avoid the 0
    if time_remaining < 0:
        time_remaining = 0
    display_text_ui("Temps restant : " + str(time_remaining) + "s", (1, 20), var.FONT)

    # Num generation and nb cars alive
    display_text_ui("Nombre de voitures restantes : " + str(var.NB_CARS_ALIVE), (1, 50), var.FONT)
    display_text_ui("Génération : " + str(var.NUM_GENERATION), (1, 80), var.FONT)

    # Garage
    var.DISPLAY_GARAGE = garage_button.check_state()  # Draw the garage button
    if garage_button.just_clicked:  # Garage button is just clicked
        if var.DISPLAY_GARAGE:
            pause()
            init_garage()
        else:
            unpause()
            delete_garage()

    if var.DISPLAY_GARAGE:  # If the garage is displayed we draw it and do the actions
        display_garage()

    # Dice
    dice_button.check_state()  # Draw the dice button
    if dice_button.just_clicked:   # Dice button is just clicked
        if var.MEMORY_CARS.get("dice"):   # If the memory of the dice already exists
            var.MEMORY_CARS.get("dice").append((var.ACTUAL_ID_MEMORY_DICE, Genetic()))
        else:                               # If the memory of the dice doesn't exist
            var.MEMORY_CARS["dice"] = [(var.ACTUAL_ID_MEMORY_DICE, Genetic())]
        var.ACTUAL_ID_MEMORY_DICE += 1


def pause(from_button=False):
    """
    To pause the simulation

    Args:
        from_button (bool): If the pause is from the pause button
    """
    if not from_button:  # If the pause is not from the pause button we have to check the button
        var.PAUSE = True  # We pause the simulation
        pause_button.deactivate_button()  # We check the pause button

    var.START_TIME_PAUSE = time.time()  # We get the time when the pause started
    var.TIME_REMAINING_PAUSE = int(var.TIME_REMAINING + var.DURATION_PAUSES - (time.time() - var.START_TIME)) + 1  # We save the time remaining before the pause


def unpause(from_button=False):
    """
    To unpause the simulation

    Args:
        from_button (bool): If the unpause is from the pause button
    """
    if not from_button:  # If the unpause is not from the pause button we have to uncheck the button
        var.PAUSE = False  # We unpause the simulation
        pause_button.activate_button()  # We uncheck the pause button

    if var.DISPLAY_GARAGE:
        delete_garage()

    var.DURATION_PAUSES += time.time() - var.START_TIME_PAUSE  # We add the duration of the pause to the total duration of the pause


def delete_garage():
    var.DISPLAY_GARAGE = False
    garage_button.activated = False
    erase_garage()