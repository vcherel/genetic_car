from src.other.utils import convert_to_new_window, union_rect  # Import the function to convert the coordinates
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

stop_button = Button()  # Button to stop the game
pause_button = Button()  # Button to pause the game
play_button = Button()  # Button to start the game
nb_cars_button = Button()  # Button to change the number of cars
garage_button = Button()  # Button to open the garage
dice_button = Button()  # Button to see the dice with the camera
map_button = Button()  # Button to change the map
restart_button = Button()  # Button to restart the game
settings_button = Button()  # Button to open the settings
skip_button = Button()  # Button to go to the next generation

BUTTONS = [stop_button, pause_button, play_button, nb_cars_button, garage_button, dice_button, map_button, restart_button, settings_button, skip_button]  # List of all the buttons


def init():
    global stop_button, pause_button, play_button, nb_cars_button, garage_button, dice_button, map_button, restart_button, settings_button, skip_button

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
    skip_button = Button(1290, 80, pygame.image.load(var.PATH_IMAGE + '/skip_button.png'), scale=0.05)


def handle_events(cars=None):
    """
    Detect events in the ui and do the corresponding action

    Args:
        cars (list): List of cars in case we want to display a car by clicking on it
    """
    # If we were resizing, and we stop pressing the mouse we resize the window
    if var.RESIZE and not pygame.mouse.get_pressed()[0] and time.time() - var.TIME_RESIZE > 0.05:
        delete_all_windows()  # Delete all the windows
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
            if not found and car.rotated_rect_shown.collidepoint(pygame.mouse.get_pos()):
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
    Display the ui (buttons, text, menus...)

    Args:
        cars (list): List of cars in case we want to change the map and init the positions of the cars
    """
    display_text()  # Display the different texts
    display_buttons(cars)  # Display the buttons


def display_buttons(cars):
    """
    Draw the buttons and change the state of the variables

    Args:
        cars (list): List of cars in case we want to change the map and init the positions of the cars
    """
    display_stop_button()  # Display the stop button
    display_pause_button()  # Display the pause button
    display_start_button()  # Display the start button
    display_nb_cars_button()  # Display the nb cars button
    display_garage_button()  # Display the garage button
    display_dice_button()  # Display the dice button
    display_map_button(cars)  # Display the map button
    display_restart_button()  # Display the restart button
    display_settings_button()  # Display the settings button
    display_skip_button()  # Display the next generation button


def display_stop_button():
    """
    Display the stop button used to stop the simulation
    """
    stop_button.draw()  # Draw the stop button
    if stop_button.just_clicked:
        if var.PLAY:
            var.PLAY = False  # We stop the simulation
        if var.DISPLAY_GARAGE:
            delete_garage()


def display_pause_button():
    """
    Display the pause button used to pause the simulation
    """
    var.PAUSE = pause_button.draw()  # Draw the pause button
    if pause_button.just_clicked:  # Pause button is just clicked
        if var.PAUSE:
            pause(from_button=True)  # We pause the simulation
        else:
            unpause(from_button=True)  # We unpause the simulation


def display_start_button():
    """
    Display the start button used to start the simulation
    """
    var.START = play_button.draw()  # Draw the start button
    if play_button.just_clicked and (var.NB_CARS != 0 or var.GENETICS_FROM_GARAGE):
        var.PLAY = True  # We start the simulation
        if var.DISPLAY_GARAGE:
            delete_garage()  # We erase the garage
        if var.DISPLAY_DICE_MENU:
            DICE_MENU.erase_dice_menu()  # We erase the dice menu
    if var.START and var.PAUSE:    # We also resume the simulation if the start button is pressed
        unpause()  # We unpause the simulation


def display_nb_cars_button():
    """
    Display the nb cars button used to change the number of cars
    """
    nb_cars_button.draw()  # Draw the nb cars button
    if nb_cars_button.just_clicked:  # Nb cars button is just clicked
        nb_cars_button.text = ''


def display_garage_button():
    """
    Display the garage button used to see what cars are stored in the garage
    """
    var.DISPLAY_GARAGE = garage_button.draw()  # Draw the garage button
    var.RECTS_BLIT_UI.append(garage_button.rect)  # We add the rect of the garage button to the list of rects to blit
    if garage_button.just_clicked:  # Garage button is just clicked
        if var.DISPLAY_GARAGE:
            pause()
            GARAGE.init()
        else:
            unpause()
            GARAGE.erase_garage()
    if var.DISPLAY_GARAGE:  # If the garage is displayed we draw it and do the actions
        GARAGE.display_garage()


def display_dice_button():
    """
    Display the dice button used to create a car by filming dice
    """
    dice_button.draw()  # Draw the dice button
    var.RECTS_BLIT_UI.append(dice_button.rect)  # We add the rect of the dice button to the list of rects to blit
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

    if var.DISPLAY_DICE_MENU:  # If the dice menu is displayed we draw it and do the actions
        if DICE_MENU.display_dice_menu():
            DICE_MENU.erase_dice_menu()  # We erase the dice menu when the check button is pressed


def display_map_button(cars):
    """
    Display the map button used to change the map
    """
    map_button.draw()  # Draw the map button
    var.RECTS_BLIT_UI.append(map_button.rect)  # We add the rect of the map button to the list of rects to blit
    if map_button.just_clicked:  # Map button is just clicked
        pause()
        var.change_map()  # We change the map
        if cars:
            for car in cars:
                car.reset()  # We reset the cars
        unpause()


def display_restart_button():
    """
    Display the restart button used to restart the last run
    """
    if restart_button.draw() and var.CARS_LAST_RUN:  # Draw the restart button
        var.PLAY_LAST_RUN = True  # We play the last run


def display_settings_button():
    """
    Display the settings button used to change the different settings
    """
    var.DISPLAY_SETTINGS = settings_button.draw()  # Draw the garage button
    if settings_button.just_clicked:  # Garage button is just clicked
        if var.DISPLAY_SETTINGS:
            pause()
        else:
            unpause()
            SETTINGS.erase()
    if var.DISPLAY_SETTINGS:  # If the garage is displayed we draw it and do the actions
        SETTINGS.show()


def display_skip_button():
    """
    Display the next generation button used to skip to the next generation
    """
    skip_button.draw()  # Draw the next generation button
    if skip_button.just_clicked:  # Next generation button is just clicked
        var.CHANGE_GENERATION = True  # We change the generation


def display_text():
    """
    Display the text of the UI (time remaining, nb cars, generation, FPS)
    """
    # Time remaining
    display_text_ui(f'Tours restants : {var.TICKS_REMAINING} ({int(var.TICKS_REMAINING / var.FPS)}s)', convert_to_new_window((1, 20)), var.FONT)
    display_text_ui(f'Nombre de voitures restantes : {var.NB_CARS_ALIVE}', convert_to_new_window((1, 50)), var.FONT)
    display_text_ui(f'Génération : {var.NUM_GENERATION}', convert_to_new_window((1, 80)), var.FONT)

    # FPS display
    if var.PLAY:
        fps = str(var.ACTUAL_FPS)
    else:
        fps = str(int(var.CLOCK.get_fps()))
    display_text_ui('FPS : ' + fps, convert_to_new_window((1, 1)), var.SMALL_FONT)


def pause(from_button=False):
    """
    To pause the simulation

    Args:
        from_button (bool): If the pause is from the pause button
    """
    if not from_button:  # If the pause is not from the pause button we have to check the button
        var.PAUSE = True  # We pause the simulation
        pause_button.activated = True  # We check the pause button


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


def delete_all_windows():
    """
    To delete all the windows
    """
    if var.DISPLAY_CAR_WINDOW:
        erase_car_window()
    if var.DISPLAY_GARAGE:
        delete_garage()
    if var.DISPLAY_DICE_MENU:
        DICE_MENU.erase_dice_menu()
    if var.DISPLAY_SETTINGS:
        delete_settings()


def delete_garage():
    """
    To stop showing the garage
    """
    var.DISPLAY_GARAGE = False
    garage_button.deactivate()
    GARAGE.erase_garage()
    unpause()


def delete_settings():
    """
    To stop showing the settings
    """
    var.DISPLAY_SETTINGS = False
    settings_button.deactivate()  # Deactivate the settings button
    SETTINGS.erase()  # Erase the settings
    unpause()  # Unpause the game


def erase():
    """
    To erase the UI by erasing the rect saved in var.RECTS_BLIT_UI
    """
    rect_blit_ui = union_rect(var.RECTS_BLIT_UI)  # Union of the rects for the blit
    var.WINDOW.blit(var.BACKGROUND, rect_blit_ui, rect_blit_ui)  # Erase the ui
    var.RECTS_BLIT_UI = []  # We reset the list of rects to blit
