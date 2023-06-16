from src.render.display import show_car_window, erase_car_window  # Import the function to show the car
from src.other.camera import capture_dice  # Import the function to capture the dice
from src.render.garage import erase_garage, GARAGE  # Import functions from garage
from src.render.display import display_text_ui  # Import functions from display
from src.render.dice_menu import DICE_MENU  # Import functions from dice menu
from src.game.genetic import Genetic  # Import the genetic class
from src.game.constants import SEE_CURSOR  # Import constants
import src.other.variables as var  # Import the variables
from src.render.button import Button  # Import the button
import os.path  # To get the path of images
import pygame  # To use pygame
import time  # To get the time


use_camera = True  # If we don't use the camera
time_remaining_pause = 0  # Time remaining when the game has been paused
change_nb_cars = False  # Change the number of cars

debug_button = Button()  # Button to activate the debug mode
stop_button = Button()  # Button to stop the game
pause_button = Button()  # Button to pause the game
start_button = Button()  # Button to start the game
nb_cars_button = Button()  # Button to change the number of cars
garage_button = Button()  # Button to open the garage
dice_button = Button()  # Button to see the dice
map_button = Button()  # Button to change the map
text_nb_cars = None  # Text to display the number of cars


def init():
    global debug_button, stop_button, pause_button, start_button, nb_cars_button, garage_button, dice_button, map_button, text_nb_cars

    path_images = os.path.dirname(__file__) + '/../../images/'  # Path of the images

    # Buttons
    debug_button = Button(1435, 642, pygame.image.load(path_images + '/checkbox_1.png'),
                          pygame.image.load(path_images + '/checkbox_2.png'),
                          pygame.image.load(path_images + '/checkbox_3.png'), checkbox=True, scale=0.03)
    stop_button = Button(1420, 4, pygame.image.load(path_images + '/stop_button.png'), scale=0.1)
    pause_button = Button(1417, 56, pygame.image.load(path_images + '/pause_button.png'), checkbox=True, scale=0.11)
    start_button = Button(1310, 15, pygame.image.load(path_images + '/start_button.png'), scale=0.18)
    nb_cars_button = Button(1049, 58, pygame.image.load(path_images + '/writing_rectangle_1.png'),
                            pygame.image.load(path_images + '/writing_rectangle_2.png'),
                            pygame.image.load(path_images + '/writing_rectangle_3.png'), checkbox=True, scale=0.8)
    garage_button = Button(400, 30, pygame.image.load(path_images + '/garage_button.png'), scale=0.2, checkbox=True)
    dice_button = Button(600, 28, pygame.image.load(path_images + '/dice_button.png'), scale=0.4)
    map_button = Button(845, 37, pygame.image.load(path_images + '/map_button.png'), scale=0.8)

    # Text
    text_nb_cars = var.FONT.render(var.STR_NB_CARS, True, (0, 0, 0), (255, 255, 255))  # Add the text for the number of cars


def handle_events(cars=None):
    """
    Detect events in the ui and do the corresponding action

    Args:
        cars (list): List of cars in case we want to display a car by clicking on it
    """
    global change_nb_cars, text_nb_cars

    # Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            var.exit_game()  # Exit the game if the user click on the cross or press escape

        # Detection of clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_clicks(cars)

        # If we press return (enter) or backspace (delete) we change the value of the writing rectangle if needed
        if event.type == pygame.KEYDOWN:
            if change_nb_cars:
                var.NB_CARS, var.STR_NB_CARS, change_nb_cars, text_nb_cars = \
                    nb_cars_button.update_writing_rectangle(event, var.NB_CARS, var.STR_NB_CARS, text_nb_cars, nb_cars=True)

            if var.DISPLAY_DICE_MENU:  # We check if the dice menu has been opened
                for index, dice_bool in enumerate(DICE_MENU.bool_scores):
                    if dice_bool:
                        # We change the value of the dice using the writing rectangle
                        writing_rectangle = DICE_MENU.writing_rectangles[index]  # Get the writing rectangle
                        score = DICE_MENU.genetic.get_dice_value(index)  # Get the score of the dice
                        str_score = DICE_MENU.str_scores[index]  # Get the string before the change
                        text_score = DICE_MENU.text_scores[index]  # Get the text before the change

                        score, str_score, dice_bool, text_score = \
                            writing_rectangle.update_writing_rectangle(event, score, str_score, text_score, dice_value=True)

                        DICE_MENU.genetic.set_dice_value(index, score)  # Change the value of the dice
                        DICE_MENU.str_scores[index] = str_score  # Change the string of the score
                        DICE_MENU.text_scores[index] = text_score  # Change the text of the score

                        if not dice_bool:
                            DICE_MENU.bool_scores[index] = False
                            DICE_MENU.save_values()  # Save the values of the dice

            if GARAGE.rectangles:
                for rect_garage in GARAGE.rectangles:
                    if rect_garage.change_text:

                        _, rect_garage.name, rect_garage.change_text, _ = \
                            rect_garage.name_button.update_writing_rectangle(event, None, rect_garage.name, rect_garage.text, int_variable=False)

                        if not rect_garage.change_text:
                            if rect_garage.name == '':
                                rect_garage.name = 'car'

                            # We change the value of the car in the memory
                            var.update_car_name(rect_garage.type_car, rect_garage.id_car, rect_garage.name)

                        rect_garage.text = var.FONT.render(rect_garage.name, True, (0, 0, 0), (255, 255, 255))  # We change the text of the writing rectangle
                        rect_garage.name_button.image = rect_garage.text  # We change the image of the writing rectangle
                        rect_garage.draw()  # We display the rectangle with the new text


def handle_clicks(cars):
    """
    Detect clicks in the ui and do the corresponding action

    Args:
        cars (list): List of cars in case we want to display a car by clicking on it
    """
    global change_nb_cars, text_nb_cars

    if change_nb_cars:  # If we click outside the writing rectangle, we stop changing the number of cars
        var.NB_CARS, var.STR_NB_CARS, text_nb_cars = nb_cars_button.save_writing_rectangle(var.STR_NB_CARS, text_nb_cars, nb_cars=True)
        change_nb_cars = False

    if var.DISPLAY_DICE_MENU:  # If we click outside the dice menu, we stop changing the value of the dice and we save it
        for index, dice_bool in enumerate(DICE_MENU.bool_scores):
            if dice_bool:
                writing_rectangle = DICE_MENU.writing_rectangles[index]  # Get the writing rectangle
                str_score = DICE_MENU.str_scores[index]  # Get the value of the dice before the change
                text_score = DICE_MENU.text_scores[index]  # Get the text before the change

                score, str_score, text_score = writing_rectangle.save_writing_rectangle(str_score, text_score)

                DICE_MENU.genetic.set_dice_value(index, score)  # Change the value of the dice
                DICE_MENU.str_scores[index] = str_score  # Change the string of the score
                DICE_MENU.text_scores[index] = text_score  # Change the text of the score

                DICE_MENU.bool_scores[index] = False  # Stop changing the value of the dice
                DICE_MENU.save_values()  # Save the values of the dice

    if GARAGE.rectangles:
        for rect_garage in GARAGE.rectangles:
            if rect_garage.change_text:
                print("1")
                rect_garage.change_text = False

                if rect_garage.name == '':
                    rect_garage.name = 'car'

                # We change the value of the car in the memory
                var.update_car_name(rect_garage.type_car, rect_garage.id_car, rect_garage.name)

                rect_garage.text = var.FONT.render(rect_garage.name, True, (0, 0, 0), (255, 255, 255))  # We change the text of the writing rectangle
                rect_garage.name_button.image = rect_garage.text  # We change the image of the writing rectangle
                rect_garage.draw()  # We display the rectangle with the new text


    if SEE_CURSOR:
        print('Click at position', pygame.mouse.get_pos())  # Print the position of the click
        print('Color of the pixel', var.WINDOW.get_at(pygame.mouse.get_pos()))  # Print the color of the pixel

    if var.DISPLAY_CAR_WINDOW:
        unpause()  # Unpause the game (erase the car window)

    if cars:
        found = False  # Boolean to know if we found a car
        for car in cars:
            if not found and car.rotated_rect.collidepoint(pygame.mouse.get_pos()):
                found = True
                pause()  # Pause the game
                show_car_window(car)  # Display the car


def display():
    """
    Draw the buttons and change the state of the variables
    """
    global text_nb_cars, change_nb_cars


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
    if start_button.just_clicked and (var.NB_CARS != 0 or var.GENETICS_FROM_GARAGE):
        var.PLAY = True  # We start the simulation
        if var.DISPLAY_GARAGE:
            delete_garage()  # We erase the garage
        if var.DISPLAY_DICE_MENU:
            DICE_MENU.erase_dice_menu()  # We erase the dice menu

    if var.START and var.PAUSE:    # We also resume the simulation if the start button is pressed
        unpause()  # We unpause the simulation


    # Nb cars button
    change_nb_cars = nb_cars_button.check_state()  # Draw the nb cars button
    if nb_cars_button.just_clicked:
        var.STR_NB_CARS = ''  # We empty the string for the number of cars


    # Garage
    var.DISPLAY_GARAGE = garage_button.check_state()  # Draw the garage button
    if garage_button.just_clicked:  # Garage button is just clicked
        if var.DISPLAY_GARAGE:
            pause()
            GARAGE.init_garage()
        else:
            unpause()
            erase_garage()
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
            DICE_MENU.init('dice', dict_scores=capture_dice())  # We initialize the variables of the dice
            var.DISPLAY_DICE_MENU = True  # We display the dice menu


    # Dice menu
    if var.DISPLAY_DICE_MENU:  # If the dice menu is displayed we draw it and do the actions
        if DICE_MENU.display_dice_menu():
            DICE_MENU.erase_dice_menu()  # We erase the dice menu when the check button is pressed


    # Map button
    map_button.check_state()  # Draw the map button
    if map_button.just_clicked:  # Map button is just clicked
        var.change_map()  # We change the map



    # Draw the number of cars
    if change_nb_cars:
        display_text_ui(var.STR_NB_CARS, (1195, 62), var.FONT, background_color=(255, 255, 255))
    else:
        var.WINDOW.blit(text_nb_cars, (1195, 62))


    # FPS
    if var.PLAY:
        fps = str(var.ACTUAL_FPS)
    else:
        fps = str(int(var.CLOCK.get_fps()))
    display_text_ui('FPS : ' + fps, (1, 1), var.SMALL_FONT)


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

    if var.DISPLAY_GARAGE:
        delete_garage()

    if var.DISPLAY_CAR_WINDOW:
        erase_car_window()

    var.DURATION_PAUSES += time.time() - var.START_TIME_PAUSE  # We add the duration of the pause to the total duration of the pause


def delete_garage():
    var.DISPLAY_GARAGE = False
    garage_button.activated = False
    erase_garage()