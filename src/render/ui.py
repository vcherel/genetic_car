from other.utils import convert_to_new_window, union_rect  # Import the function to convert the coordinates
from render.display import show_car_window, erase_car_window  # Import the function to show the car
from other.camera import capture_dice  # Import the function to capture the dice
from render.display import display_text_ui  # Import functions from display
from menus.dice_menu import DICE_MENU  # Import functions from dice menu
from menus.settings_menu import SETTINGS  # Import the settings window
from data.data_classes import MemoryCar  # Import the car memory
from menus.garage_menu import GARAGE  # Import the garage window
from data.constants import NB_MAPS  # Import constants
from game.genetic import Genetic  # Import the genetic class
from render.button import Button  # Import the button
import data.variables as var  # Import the data
import pygame  # To use pygame
import time  # To get the time


"""
This file contains all the functions to display the UI and check the events
"""


use_camera = True  # If we don't use the camera

stop_button = Button()  # Button to stop the game
pause_button = Button()  # Button to pause the game
start_button = Button()  # Button to start the game
nb_cars_button = Button()  # Button to change the number of cars
garage_button = Button()  # Button to open the garage
dice_button = Button()  # Button to see the dice with the camera
restart_button = Button()  # Button to restart the game
settings_button = Button()  # Button to open the settings
skip_button = Button()  # Button to go to the next generation
previous_map_button = Button()  # Button to change the map
next_map_button = Button()  # Button to change the map

BUTTONS = [stop_button, pause_button, start_button, nb_cars_button, garage_button, dice_button, restart_button, settings_button, skip_button, previous_map_button, next_map_button]  # List of all the buttons


def init():
    global stop_button, pause_button, start_button, nb_cars_button, garage_button, dice_button, restart_button, settings_button, skip_button, previous_map_button, next_map_button

    # Buttons
    stop_button = Button(x=1425, y=4, image_name='main_menu/stop', scale=0.25)
    pause_button = Button(x=1425, y=56, image_name='main_menu/pause', checkbox=True, scale=0.25)
    start_button = Button(x=1330, y=18, image_name='main_menu/start', scale=0.35)
    nb_cars_button = Button(x=1095, y=58, image_name='writing', variable=var.NB_CARS, name='nb_cars')
    garage_button = Button(x=350, y=30, image_name='main_menu/garage', checkbox=True)
    dice_button = Button(x=500, y=30, image_name='main_menu/dice')
    restart_button = Button(x=1287, y=4, image_name='main_menu/restart', scale=0.2)
    settings_button = Button(x=285, y=5, image_name='main_menu/settings', checkbox=True, scale=0.65)
    skip_button = Button(x=1290, y=80, image_name='main_menu/skip', scale=0.45)
    previous_map_button = Button(x=820, y=70, image_name='main_menu/previous_map', scale=0.45)
    next_map_button = Button(x=920, y=70, image_name='main_menu/next_map', scale=0.45)



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
        GARAGE.resize()  # Reinitialize the garage window

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
        for index, writing_button in enumerate(DICE_MENU.values_button):
            if writing_button.activated:
                writing_button.deactivate()  # Stop changing the value of the dice
                DICE_MENU.save_values(index, writing_button)  # Save the values of the dice

        if not DICE_MENU.rect.collidepoint(pygame.mouse.get_pos()):
            DICE_MENU.erase_dice_menu()  # Erase the dice menu if we click outside of it

    if GARAGE.rectangles:
        for rect_garage in GARAGE.rectangles:
            if rect_garage.name_button.activated and not rect_garage.name_button.rect.collidepoint(pygame.mouse.get_pos()):  # If we click outside the writing button, we stop changing the name of the car
                rect_garage.name_button.deactivate()  # Stop changing the name of the car
                rect_garage.save_new_car_name()  # Save the name of the car

    if var.DISPLAY_GARAGE and not GARAGE.rect.collidepoint(pygame.mouse.get_pos()) and not\
            garage_button.rect.collidepoint(pygame.mouse.get_pos()) and not var.DISPLAY_DICE_MENU:
        # We don't want to delete the garage if we click during the dice menu (modification of the values of a car)
        delete_garage()  # Delete the garage if we click outside of it

    if var.DISPLAY_SETTINGS:
        for button in SETTINGS.writing_buttons:
            if button.activated:
                button.deactivate()  # Stop changing the value of the button
                setattr(var, button.name, button.variable)

        # If we click outside the settings, we close it
        if not SETTINGS.rect.collidepoint(pygame.mouse.get_pos()):
            settings_button.deactivate()  # Deactivate the settings button
            SETTINGS.erase()  # Erase the settings
            unpause()  # Unpause the game

    if var.SHOW_CLICS_INFO:
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
        if nb_cars_button.update_after_key_press(event):  # If the value has been saved
            var.NB_CARS = nb_cars_button.variable  # We change the value of the variable

    # We change value of dice if necessary
    if var.DISPLAY_DICE_MENU:
        for index, value_button in enumerate(DICE_MENU.values_button):
            if value_button.activated:
                if value_button.update_after_key_press(event):  # If the value has been saved
                    DICE_MENU.save_values(index, value_button)  # Save the values of the dice

    # We change value of car name if necessary
    if GARAGE.rectangles:
        for rect_garage in GARAGE.rectangles:
            if rect_garage.name_button.activated:
                if rect_garage.name_button.update_after_key_press(event):  # If the value has been saved
                    rect_garage.save_new_car_name()  # Save the name of the car

    # We change value of settings if necessary
    if var.DISPLAY_SETTINGS:
        for button in SETTINGS.writing_buttons:
            if button.activated and button.update_after_key_press(event):  # If the value has been saved
                setattr(var, button.name, button.variable)  # Change the value of the variable


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
    Draw the buttons and change the state of the data

    Args:
        cars (list): List of cars in case we want to change the map and init the positions of the cars
    """
    display_stop_button()  # Display the stop button
    display_pause_button()  # Display the pause button
    display_start_button()  # Display the start button
    display_nb_cars_button()  # Display the nb cars button
    display_garage_button()  # Display the garage button
    display_map_button(cars)  # Display the map button
    display_restart_button()  # Display the restart button
    display_settings_button()  # Display the settings button
    display_skip_button()  # Display the next generation button
    display_dice_button()  # Display the dice button


def display_stop_button():
    """
    Display the stop button used to stop the simulation
    """
    stop_button.draw()  # Draw the stop button
    if stop_button.mouse_over_button:
        var.add_to_rects_blit_ui(stop_button.rect)  # We add the rect to the list of rects to blit
    if stop_button.just_clicked:
        if var.PLAY:
            var.PLAY = False  # We stop the simulation
            var.blit_circuit()  # We blit the circuit
        if var.DISPLAY_GARAGE:
            delete_garage()


def display_pause_button():
    """
    Display the pause button used to pause the simulation
    """
    var.PAUSE = pause_button.draw()  # Draw the pause button
    if pause_button.mouse_over_button:
        var.add_to_rects_blit_ui(pause_button.rect, offset=1)
    if pause_button.just_clicked:  # Pause button is just clicked
        if var.PAUSE:
            pause(from_button=True)  # We pause the simulation
        else:
            unpause(from_button=True)  # We unpause the simulation


def display_start_button():
    """
    Display the start button used to start the simulation
    """
    var.START = start_button.draw()  # Draw the start button
    if start_button.mouse_over_button:
        var.add_to_rects_blit_ui(start_button.rect, offset=5)  # To erase the contour of button
    if start_button.just_clicked and (var.NB_CARS != 0 or var.SELECTED_MEMORY_CARS):
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
    if garage_button.mouse_over_button:
        var.add_to_rects_blit_ui(garage_button.rect, offset=3)  # We add the rect of the garage button to the list of rects to blit
    if garage_button.just_clicked:  # Garage button is just clicked
        if var.DISPLAY_GARAGE:
            pause()
        else:
            unpause()
            GARAGE.erase_garage()
    if var.DISPLAY_GARAGE and not var.DISPLAY_DICE_MENU:  # If the garage is displayed we draw it and do the actions
        GARAGE.draw()


def display_dice_button():
    """
    Display the dice button used to create a car by filming dice
    """
    dice_button.draw()  # Draw the dice button
    if dice_button.mouse_over_button:
        var.add_to_rects_blit_ui(dice_button.rect, offset=1)  # We add the rect of the dice button to the list of rects to blit
    if dice_button.just_clicked:   # Dice button is just clicked
        if var.DISPLAY_GARAGE:
            delete_garage()  # We erase the garage when the dice button is pressed

        if var.DISPLAY_DICE_MENU:  # If the dice menu is displayed we erase it
            DICE_MENU.erase_dice_menu()
            unpause()

        elif not use_camera:  # If we don't use the camera we create a random dice
            var.MEMORY_CARS.append(MemoryCar(id_car=var.ACTUAL_IDS_MEMORY_CARS, name=f'Dé_{var.ACTUAL_IDS_MEMORY_CARS}',
                                             color='gray', genetic=Genetic(), best_scores=[0] * NB_MAPS))  # We add the dice to the memory
            var.ACTUAL_IDS_MEMORY_CARS += 1  # We increment the id of the dice

        else:  # If we use the camera we capture the dice
            pause()
            DICE_MENU.init(values=capture_dice(), by_camera=True)  # We initialize the data of the dice
            var.DISPLAY_DICE_MENU = True  # We display the dice menu
            GARAGE.reload_page = True  # We reload the page of the garage

    if var.DISPLAY_DICE_MENU:  # If the dice menu is displayed we draw it and do the actions
        if DICE_MENU.display_dice_menu():  # If the user has validated the dice
            DICE_MENU.erase_dice_menu()  # We erase the dice menu when the check button is pressed


def display_map_button(cars):
    """
    Display the map button used to change the map
    """
    previous_map_button.draw()  # Draw the map button
    if previous_map_button.mouse_over_button:
        var.add_to_rects_blit_ui(previous_map_button.rect, offset=6)  # We add the rect of the map button to the list of rects to blit
    if previous_map_button.just_clicked:  # Map button is just clicked
        var.change_map(reverse=True)  # We change the map to the previous one
        pygame.display.flip()  # To see the new map
        update_value_nb_cars_button()  # We update the value of the nb cars button
        if cars:
            for car in cars:
                car.reset()  # We reset the cars
            var.NB_CARS_ALIVE = len(cars)

    next_map_button.draw()  # Draw the map button
    if next_map_button.mouse_over_button:
        var.add_to_rects_blit_ui(next_map_button.rect, offset=6)  # We add the rect of the map button to the list of rects to blit
    if next_map_button.just_clicked:  # Map button is just clicked
        var.change_map()  # We change the map to the previous one
        pygame.display.flip()  # To see the new map
        update_value_nb_cars_button()  # We update the value of the nb cars button
        if cars:
            for car in cars:
                car.reset()  # We reset the cars
            var.NB_CARS_ALIVE = len(cars)


def display_restart_button():
    """
    Display the restart button used to restart the last run
    """
    if restart_button.draw() and var.CARS_LAST_RUN:  # Draw the restart button
        var.PLAY_LAST_RUN = True  # We play the last run
        var.blit_circuit()  # We blit the circuit to hide the dead cars
        if not var.LAST_RUN_PLAYING:
            var.NUM_GENERATION -= 1  # We decrement the number of generation
        var.LAST_RUN_PLAYING = True  # We indicate that we are playing the last run
    if restart_button.mouse_over_button:
        var.add_to_rects_blit_ui(restart_button.rect)


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
        SETTINGS.draw()
    if settings_button.mouse_over_button:
        var.add_to_rects_blit_ui(settings_button.rect)


def display_skip_button():
    """
    Display the next generation button used to skip to the next generation
    """
    skip_button.draw()  # Draw the next generation button
    if skip_button.just_clicked:  # Next generation button is just clicked
        var.CHANGE_GENERATION = True  # We change the generation
    if skip_button.mouse_over_button:
        var.add_to_rects_blit_ui(skip_button.rect, offset=2)  # We add the rect of the next generation button to the list of rects to blit


def display_text():
    """
    Display the text of the UI (time remaining, nb cars, generation, FPS)
    """
    # Time remaining
    if var.PLAY and var.ACTUAL_FPS != 0:  # If the simulation is playing we display the time remaining in seconds if the simulation stays at this fps
        time_remaining = int(var.TICKS_REMAINING / var.ACTUAL_FPS)
        var.LAST_TIME_REMAINING.append(time_remaining)
        if len(var.LAST_TIME_REMAINING) > 50:
            var.LAST_TIME_REMAINING.pop(0)
        time_remaining = max(set(var.LAST_TIME_REMAINING), key=var.LAST_TIME_REMAINING.count)  # We take the most common value
    else:  # If the simulation is paused we display the time remaining theoretically in seconds
        time_remaining = int(var.TICKS_REMAINING / var.FPS)

    display_text_ui(f'Tours restants : {var.TICKS_REMAINING} ({time_remaining}s)', convert_to_new_window((1, 20)), var.FONT)
    display_text_ui(f'Nombre de voitures restantes : {var.NB_CARS_ALIVE}', convert_to_new_window((1, 50)), var.FONT)
    display_text_ui(f'Génération : {var.NUM_GENERATION}', convert_to_new_window((1, 80)), var.FONT)

    # FPS display
    if var.PLAY:
        fps = str(var.ACTUAL_FPS)
    else:
        fps = str(int(var.CLOCK.get_fps()))
    display_text_ui('FPS : ' + fps, convert_to_new_window((1, 1)), var.VERY_SMALL_FONT)


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
        var.add_to_rects_blit_ui(pause_button.rect)  # We add the rect of the pause button to the list of rects to blit

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


def update_value_nb_cars_button():
    """
    Update the value of the nb cars button
    """
    nb_cars_button.update_text(var.NB_CARS)
