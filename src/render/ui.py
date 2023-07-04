from src.render.display import show_car_window, erase_car_window  # Import the function to show the car
from src.other.camera import capture_dice  # Import the function to capture the dice
from src.render.display import display_text_ui  # Import functions from display
from src.render.dice_menu import DICE_MENU  # Import functions from dice menu
from src.render.settings_menu import SETTINGS  # Import the settings window
from src.render.garage import GARAGE  # Import functions from garage
from src.game.genetic import Genetic  # Import the genetic class
from src.game.constants import SEE_CURSOR  # Import constants
import src.other.variables as var  # Import the variables
from src.render.button import Button  # Import the button
import pygame  # To use pygame
import time  # To get the time


"""
This file contains all the functions to display the UI and check the events
"""


use_camera = True  # If we don't use the camera
time_remaining_pause = 0  # Time remaining when the game has been paused

stop_button = Button()  # Button to stop the game
pause_button = Button()  # Button to pause the game
play_button = Button()  # Button to start the game
nb_cars_button = Button()  # Button to change the number of cars
garage_button = Button()  # Button to open the garage
dice_button = Button()  # Button to see the dice
map_button = Button()  # Button to change the map
restart_button = Button()  # Button to restart the game
settings_button = Button()  # Button to open the settings
next_button = Button()  # Button to go to the next generation

BUTTONS = [stop_button, pause_button, play_button, nb_cars_button, garage_button, dice_button, map_button, restart_button, settings_button, next_button]  # List of all the buttons


def init():
    global stop_button, pause_button, play_button, nb_cars_button, garage_button, dice_button, map_button, restart_button, settings_button, next_button

    # Buttons
    stop_button = Button(1420, 4, pygame.image.load(var.PATH_IMAGE + '/stop_button.png'), scale=0.1)
    pause_button = Button(1417, 56, pygame.image.load(var.PATH_IMAGE + '/pause_button.png'), checkbox=True, scale=0.11)
    play_button = Button(1320, 15, pygame.image.load(var.PATH_IMAGE + '/start_button.png'), scale=0.18)
    nb_cars_button = Button(1095, 58, pygame.image.load(var.PATH_IMAGE + '/writing_rectangle_1.png'),
                            pygame.image.load(var.PATH_IMAGE + '/writing_rectangle_2.png'),
                            pygame.image.load(var.PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                            text=str(var.NB_CARS), variable=var.NB_CARS, name='nb_cars')
    garage_button = Button(350, 30, pygame.image.load(var.PATH_IMAGE + '/garage_button_1.png'),
                           pygame.image.load(var.PATH_IMAGE + '/garage_button_2.png'),
                           pygame.image.load(var.PATH_IMAGE + '/garage_button_3.png'), checkbox=True)
    dice_button = Button(500, 30, pygame.image.load(var.PATH_IMAGE + '/dice_button_1.png'),
                         pygame.image.load(var.PATH_IMAGE + '/dice_button_2.png'),
                         pygame.image.load(var.PATH_IMAGE + '/dice_button_3.png'))
    map_button = Button(780, 30, pygame.image.load(var.PATH_IMAGE + '/map_button_1.png'),
                        pygame.image.load(var.PATH_IMAGE + '/map_button_2.png'),
                        pygame.image.load(var.PATH_IMAGE + '/map_button_3.png'))
    restart_button = Button(1290, 2, pygame.image.load(var.PATH_IMAGE + '/restart_button.png'), scale=0.08)
    settings_button = Button(285, 5, pygame.image.load(var.PATH_IMAGE + '/settings_button.png'), scale=0.065, checkbox=True)
    next_button = Button(1290, 80, pygame.image.load(var.PATH_IMAGE + '/next_button.png'), scale=0.05)


def handle_events(cars=None):
    """
    Detect events in the ui and do the corresponding action

    Args:
        cars (list): List of cars in case we want to display a car by clicking on it
    """
    # If we were resizing, and we stop pressing the mouse we resize the window
    if var.RESIZE and not pygame.mouse.get_pressed()[0] and time.time() - var.TIME_RESIZE > 0.05:
        var.RESIZE = False  # We indicate that we are not resizing the window anymore
        var.resize_window(var.RESIZE_DIMENSIONS)  # Resize the window
        init()   # Reinitialize the buttons
        SETTINGS.init()  # Reinitialize the settings window
        GARAGE.init()  # Reinitialize the garage window


    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            var.exit_game()  # Exit the game if the user click on the cross or press escape

        # If we resize the window
        elif event.type == pygame.VIDEORESIZE:
            var.RESIZE = True  # We indicate that we are resizing the window
            var.RESIZE_DIMENSIONS = (event.w, event.h)  # Save the new dimensions
            var.TIME_RESIZE = time.time()  # Save the time when we started resizing

        # Detection of clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_clicks(cars)

        # If we press return (enter) or backspace (delete) we change the value of the writing button if needed
        elif event.type == pygame.KEYDOWN:
            handle_key_press(event)



def handle_clicks(cars):
    """
    Detect clicks in the ui and do the corresponding action

    Args:
        cars (list): List of cars in case we want to display a car by clicking on it
    """
    if nb_cars_button.activated:  # If we click outside the writing button, we stop changing the number of cars
        nb_cars_button.deactivate()
        var.NB_CARS = nb_cars_button.variable

    if var.DISPLAY_DICE_MENU:  # If we click outside the dice menu, we stop changing the value of the dice and we save it
        for index, writing_button in enumerate(DICE_MENU.writing_buttons):
            if writing_button.activated:
                writing_button.deactivate()  # Stop changing the value of the dice
                DICE_MENU.save_values(index, writing_button)  # Save the values of the dice

        if not DICE_MENU.rect.collidepoint(pygame.mouse.get_pos()):
            DICE_MENU.erase_dice_menu()  # Erase the dice menu if we click outside of it

    if GARAGE.rectangles:
        for rect_garage in GARAGE.rectangles:
            if rect_garage.name_button.activated:
                rect_garage.name_button.activated = False
                rect_garage.save()  # Save the name of the car

    if var.DISPLAY_GARAGE and not GARAGE.rect.collidepoint(pygame.mouse.get_pos()) and not garage_button.rect.collidepoint(pygame.mouse.get_pos()):
        delete_garage()  # Delete the garage if we click outside of it

    if var.DISPLAY_SETTINGS:
        if SETTINGS.fps_button.activated:
            SETTINGS.fps_button.deactivate()  # Stop changing the value of the fps
            var.FPS = SETTINGS.fps_button.variable  # Change the value of the fps

        # If we click outside the settings, we close it
        if not SETTINGS.rect.collidepoint(pygame.mouse.get_pos()):
            settings_button.deactivate()  # Deactivate the settings button
            SETTINGS.erase()  # Erase the settings
            unpause()  # Unpause the game


    if SEE_CURSOR:
        print('Click at position', pygame.mouse.get_pos())  # Print the position of the click
        print('Color of the pixel', var.WINDOW.get_at(pygame.mouse.get_pos()))  # Print the color of the pixel

    if var.DISPLAY_CAR_WINDOW:
        unpause()  # Unpause the game (erase the car window)

    if cars and not var.DISPLAY_SETTINGS and not var.DISPLAY_GARAGE and not var.DISPLAY_DICE_MENU:  # If we click on a car, we display it, we don't want to display a car if we are in a menu
        found = False  # Boolean to know if we found a car
        for car in cars:
            if not found and car.rotated_rect.collidepoint(pygame.mouse.get_pos()):
                found = True
                pause()  # Pause the game
                show_car_window(car)  # Display the car


def handle_key_press(event):
    """
    Detect key press and do the corresponding action

    Args:
        event (pygame.event.Event): Event detected by pygame
    """
    # We change value of nb cars if necessary
    if nb_cars_button.activated:
        if nb_cars_button.update(event):  # If the value has been saved
            var.NB_CARS = nb_cars_button.variable  # We change the value of the variable

    # We change value of dice if necessary
    if var.DISPLAY_DICE_MENU:
        for index, writing_button in enumerate(DICE_MENU.writing_buttons):
            if writing_button.activated:
                if writing_button.update(event):  # If the value has been saved
                    DICE_MENU.save_values(index, writing_button)  # Save the values of the dice

    if GARAGE.rectangles:
        for rect_garage in GARAGE.rectangles:
            if rect_garage.name_button.activated:
                if rect_garage.name_button.update(event):  # If the value has been saved
                    rect_garage.save()

    if var.DISPLAY_SETTINGS:
        if SETTINGS.fps_button.activated:
            if SETTINGS.fps_button.update(event):
                var.FPS = SETTINGS.fps_button.variable


def display(cars=None):
    """
    Draw the buttons and change the state of the variables

    Args:
        cars (list): List of cars in case we want to change the map and init the positions of the cars
    """
    # Time remaining
    if not var.PLAY:
        time_remaining = var.TIME_REMAINING
    elif var.PAUSE:
        time_remaining = time_remaining_pause
    else:
        time_remaining = int(var.TIME_REMAINING + var.DURATION_PAUSES - (time.time() - var.START_TIME)) + 1  # We add 1 to the time remaining to avoid the 0
    if time_remaining < 0:
        time_remaining = 0
    display_text_ui('Temps restant : ' + str(time_remaining) + 's', (1, 20), var.FONT)

    # Text
    display_text_ui('Nombre de voitures restantes : ' + str(var.NB_CARS_ALIVE), (1, 50), var.FONT)
    display_text_ui('Génération : ' + str(var.NUM_GENERATION), (1, 80), var.FONT)

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
    var.START = play_button.check_state()  # Draw the start button
    if play_button.just_clicked and (var.NB_CARS != 0 or var.GENETICS_FROM_GARAGE):
        var.PLAY = True  # We start the simulation
        if var.DISPLAY_GARAGE:
            delete_garage()  # We erase the garage
        if var.DISPLAY_DICE_MENU:
            DICE_MENU.erase_dice_menu()  # We erase the dice menu

    if var.START and var.PAUSE:    # We also resume the simulation if the start button is pressed
        unpause()  # We unpause the simulation


    # Nb cars button
    nb_cars_button.check_state()  # Draw the nb cars button
    if nb_cars_button.just_clicked:  # Nb cars button is just clicked
        nb_cars_button.text = ''


    # Garage
    var.DISPLAY_GARAGE = garage_button.check_state()  # Draw the garage button
    if garage_button.just_clicked:  # Garage button is just clicked
        if var.DISPLAY_GARAGE:
            pause()
            GARAGE.init()
        else:
            unpause()
            GARAGE.erase_garage()
    if var.DISPLAY_GARAGE:  # If the garage is displayed we draw it and do the actions
        GARAGE.display_garage()


    # Dice
    dice_button.check_state()  # Draw the dice button
    if dice_button.just_clicked:   # Dice button is just clicked
        if var.DISPLAY_GARAGE:
            delete_garage()  # We erase the garage when the dice button is pressed

        if var.DISPLAY_DICE_MENU:  # If the dice menu is displayed we erase it
            DICE_MENU.erase_dice_menu()
            unpause()

        elif not use_camera:  # If we don't use the camera we create a random dice
            var.MEMORY_CARS.get('dice').append([var.ACTUAL_ID_MEMORY_DICE, 'Dé_' + str(var.ACTUAL_ID_MEMORY_DICE), Genetic()])  # We add the dice to the memory
        else:  # If we use the camera we capture the dice
            pause()
            DICE_MENU.init('dice', scores=capture_dice(), by_camera=True)  # We initialize the variables of the dice
            var.DISPLAY_DICE_MENU = True  # We display the dice menu


    # Dice menu
    if var.DISPLAY_DICE_MENU:  # If the dice menu is displayed we draw it and do the actions
        if DICE_MENU.display_dice_menu():
            DICE_MENU.erase_dice_menu()  # We erase the dice menu when the check button is pressed


    # Map button
    map_button.check_state()  # Draw the map button
    if map_button.just_clicked:  # Map button is just clicked
        pause()
        var.change_map()  # We change the map
        if cars:
            for car in cars:
                car.reset()  # We reset the cars
        unpause()


    # Restart button
    if restart_button.check_state() and var.CARS_LAST_RUN:  # Draw the restart button
        var.PLAY_LAST_RUN = True  # We play the last run


    # Settings button
    var.DISPLAY_SETTINGS = settings_button.check_state()  # Draw the garage button
    if settings_button.just_clicked:  # Garage button is just clicked
        if var.DISPLAY_SETTINGS:
            pause()
        else:
            unpause()
            SETTINGS.erase()
    if var.DISPLAY_SETTINGS:  # If the garage is displayed we draw it and do the actions
        SETTINGS.show()


    # FPS display
    if var.PLAY:
        fps = str(var.ACTUAL_FPS)
    else:
        fps = str(int(var.CLOCK.get_fps()))
    display_text_ui('FPS : ' + fps, (1, 1), var.SMALL_FONT)


    # Next generation button
    next_button.check_state()  # Draw the next generation button
    if next_button.just_clicked:  # Next generation button is just clicked
        var.CHANGE_GENERATION = True  # We change the generation


def pause(from_button=False):
    """
    To pause the simulation

    Args:
        from_button (bool): If the pause is from the pause button
    """
    global time_remaining_pause

    if not from_button:  # If the pause is not from the pause button we have to check the button
        var.PAUSE = True  # We pause the simulation
        pause_button.activated = True  # We check the pause button

    var.START_TIME_PAUSE = time.time()  # We get the time when the pause started
    time_remaining_pause = int(var.TIME_REMAINING + var.DURATION_PAUSES - (time.time() - var.START_TIME)) + 1  # We save the time remaining before the pause


def unpause(from_button=False):
    """
    To unpause the simulation

    Args:
        from_button (bool): If the unpause is from the pause button
    """
    if not from_button:  # If the unpause is not from the pause button we have to uncheck the button
        var.PAUSE = False  # We unpause the simulation
        pause_button.activated = False  # We uncheck the pause button

    if var.DISPLAY_CAR_WINDOW:
        erase_car_window()

    var.DURATION_PAUSES += time.time() - var.START_TIME_PAUSE  # We add the duration of the pause to the total duration of the pause


def delete_garage():
    var.DISPLAY_GARAGE = False
    garage_button.activated = False
    GARAGE.erase_garage()
    unpause()
