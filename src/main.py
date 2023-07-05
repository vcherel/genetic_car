from src.other.constants import CHANGE_CHECKPOINTS, PATH_DATA, PATH_IMAGE  # Import the constants
from src.other.analyze_data import analyze_data, show_analysis  # To analyze the data of all the cars
from src.game.genetic_algorithm import apply_genetic  # Import the genetic algorithm
from src.render.settings_menu import SETTINGS  # Import the settings
from src.render.garage import add_garage_cars  # Import the garage
from src.game.genetic import Genetic  # Import the genetic class
from src.other.utils import union_rect  # Import the utils
import src.render.display as display  # Import the display
import src.other.variables as var  # Import the variables
import traceback  # To get the traceback of errors
from src.game.car import Car  # Import the car
import random  # To generate random numbers
import src.render.ui as ui  # Import the ui
import pygame  # To use pygame
import time  # To get the time

"""
This file contains all the functions used to play the game
"""

if var.TEST_ALL_CARS:  # If we want to test all the cars
    file = open(PATH_DATA + '/test_0', 'a')  # File to write the scores of every possible car if necessary


def open_window():
    """
    Open the window of the game and manage the events until the game is started or closed
    """
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization

    while 1:
        # If we want to change the checkpoints
        if CHANGE_CHECKPOINTS:
            change_checkpoints()  # Change the checkpoints

        ui.handle_events()  # Detect events in the ui and do the corresponding actions
        ui.erase()  # Erase the buttons
        ui.display()  # Activate the buttons

        if var.SEE_CHECKPOINTS:
            display.show_checkpoints()   # Display the checkpoints

        pygame.display.flip()  # Update the screen

        if var.START:   # When the game starts
            play()  # Play the game to begin


def play(cars=None):
    """
    Play the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)
    """

    cars = init_play(cars)

    while var.PLAY:  # While the game is not stopped
        ui.handle_events(cars)  # Detect events in the ui and do the corresponding action

        if not var.PAUSE and not var.FPS_TOO_HIGH:  # If the game is not paused
            play_turn(cars)  # Play a turn

            # If we want to restart the last_run
            if var.PLAY_LAST_RUN:
                replay_last_run()  # Replay the last run

            # We stop the game if all the cars are dead or if the time is over or if we want to change the generation
            if var.NB_CARS_ALIVE == 0 or var.TICKS_REMAINING == 0 or var.CHANGE_GENERATION:
                stop_play(cars)  # Stop the game

        ui.erase()  # Erase the buttons
        ui.display(cars)  # Activate the buttons (This is here because we have to do this after erasing the screen and
        # we have ton continue to check the buttons even if the game is paused)

        pygame.display.flip()  # Update the screen

        update_fps()  # Update the fps

    open_window()  # Restart the game


def init_play(cars):
    """
    Initialize the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)

    Returns:
        list: list of cars
    """
    if not cars:  # If it is the first time we play (or if we were watching to cars from the garage only)
        # We add the cars without repetition
        cars = []  # List of cars
        for i in range(var.NB_CARS):
            added = False
            while not added:
                car = Car()  # Create a car
                if car not in cars:
                    added = True
                    cars.append(car)

        cars = add_garage_cars(cars)  # We add the car from the garage to the list of cars
        var.init_variables(len(cars))  # Initialize the variables

    else:           # If we already played
        cars = add_garage_cars(cars)  # We add the car from the garage to the list of cars
        var.init_variables(len(cars), replay=True)  # Initialize the variables

    return cars


def play_turn(cars):
    """
    Play one turn of the game

    Args:
        cars (list): list of cars
    """
    var.TIME_LAST_TURN = time.time()  # We get the time at the beginning of the turn

    # Erase cars
    rect_blit_car = union_rect(var.RECTS_BLIT_CAR)  # Union of the rects for the blit
    var.WINDOW.blit(var.BACKGROUND, rect_blit_car, rect_blit_car)  # Erase the cars
    var.RECTS_BLIT_CAR = []  # We reset the list of rects to blit

    if var.SEE_CHECKPOINTS:
        display.show_checkpoints()  # Display the checkpoints

    for car in cars:  # For each car
        if not car.dead:  # If the car is not dead
            car.move()  # Move the car
        car.draw_car()  # Draw the cars

    var.TICKS_REMAINING -= 1  # We decrease the number of iterations remaining

    # pygame.draw.rect(var.WINDOW, (120, 0, 0), rect_blit_car, 1)  # Draw the rect for the blit of the cars


def replay_last_run():
    """
    If we want to replay the last run
    """

    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Reset the screen
    var.PLAY_LAST_RUN = False  # We stop the replay
    var.NUM_GENERATION -= 1  # We go back to the previous generation

    # We reset the cars
    cars = []
    for car in var.CARS_LAST_RUN:
        car.reset()
        cars.append(car)
    play(cars)  # We restart the game with the last run


def stop_play(cars):
    """
    Stop the game

    Args:
        cars (list): list of cars
    """

    time_before = time.time()  # We get the time before the genetic algorithm
    while time.time() - time_before < 1:  # We wait 1 second
        ui.handle_events(cars)  # Detect events in the ui and do the corresponding action
        ui.erase()  # Erase the buttons
        ui.display(cars)  # Activate the buttons

    var.CHANGE_GENERATION = False  # We stop the change of generation
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Reset the screen

    var.CARS_LAST_RUN = cars  # Save the last run

    if var.TEST_ALL_CARS:  # If we want to test all cars
        for car in cars:
            file.write(f'{car.genetic} {car.score}\n')  # Write the score of the car
        return  # We stop the game
    else:
        cars = apply_genetic(cars)  # Genetic algorithm
        play(cars)  # Restart the game with the new cars


def update_fps():
    """
    Update the fps
    """
    try:  # To avoid division by 0
        var.ACTUAL_FPS = int(1 / (time.time() - var.TIME_LAST_TURN))  # Actual FPS
    except ZeroDivisionError:
        var.ACTUAL_FPS = 0

    if time.time() - var.TIME_LAST_TURN < 1 / var.FPS:  # Wait to have the right FPS
        var.ACTUAL_FPS = var.FPS
        var.FPS_TOO_HIGH = True  # The fps are too high
    else:
        var.FPS_TOO_HIGH = False  # The fps are not too high


def change_checkpoints():
    """
    Change the checkpoints of the actual map
    """
    # We display the image that explain that we are in the checkpoint mode
    image_checkpoint = pygame.image.load(PATH_IMAGE + '/checkpoint.png')  # Image of the checkpoint
    var.WINDOW.blit(image_checkpoint, (450, 25))  # We add the image to the screen
    pygame.display.flip()  # Update the screen
    # We open the file to write the checkpoints
    with open(PATH_DATA + '/checkpoints_' + str(var.NUM_MAP), 'w') as file_checkpoint_write:
        while 1:
            # We detect the mouse click to write the coordinates in the file
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    var.exit_game()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    file_checkpoint_write.write(str(x) + ' ' + str(y) + '\n')


def run_all_cars():
    """
    Run all cars and save the results in a file
    """
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization
    var.PLAY = True
    tab_cars = []
    for height_slow in range(1, 7):
        for height_medium in range(1, 7):
            for height_fast in range(1, 7):
                for width_slow in range(1, 7):
                    for width_medium in range(1, 7):
                        for width_fast in range(1, 7):
                            genetic = Genetic([height_slow, height_medium, height_fast, width_slow, width_medium, width_fast])
                            tab_cars.append(Car(genetic))
                            if len(tab_cars) == 15:
                                play(tab_cars)  # We play the game to test the cars
                                tab_cars = []



if __name__ == '__main__':
    """
    Main program
    """
    try:
        random.seed(var.SEED)  # Initialize the random seed
        var.load_variables()  # Load the variables
        var.change_map(first_time=True)  # Change the map to the first one
        ui.init()  # Initialize the ui
        SETTINGS.init()  # Initialize the settings
        display.edit_background()  # Add elements not clickable to the background

        if var.SHOW_ANALYSIS:
            scores = analyze_data('/test_' + str(var.NUM_MAP), '/result_analysis')
            show_analysis(scores)

        # If we want to run all the cars
        if var.TEST_ALL_CARS:
            run_all_cars()  # Run all cars
        else:
            open_window()  # Start the game

    except Exception as e:
        traceback.print_exc()  # Print the error
        var.exit_game()  # Exit the game
        raise e