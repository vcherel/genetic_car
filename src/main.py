from data.variables_functions import load_cars, create_background, load_parameters, change_map, exit_game, \
    init_variables, blit_circuit
from data.constants import PATH_DATA, PATH_IMAGE  # Import the constants
from game.genetic_algorithm import apply_genetic  # Import the genetic algorithm
from menus.settings_menu import SETTINGS  # Import the settings menu
from other.camera import change_camera  # To change the camera
from game.genetic import Genetic  # Import the genetic class
from game.car import Car, add_garage_cars  # Import the car
from other.utils import union_rect  # Import the utils
import render.display as display  # Import the display
import data.variables as var  # Import the data
import traceback  # To get the traceback of errors
import itertools  # To iterate over the cars
import random  # To generate random numbers
import render.ui as ui  # Import the ui
import pygame  # To use pygame
import time  # To get the time


"""
This file contains all the functions used to play the game
"""


def open_window():
    """
    Open the window of the game and manage the events until the game is started or closed
    """
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization

    while 1:
        # If we want to change the checkpoints
        if var.CHANGE_CHECKPOINTS:
            change_checkpoints()  # Change the checkpoints

        ui.handle_events()  # Detect events in the ui and do the corresponding actions
        ui.erase()  # Erase the buttons
        ui.display()  # Activate the buttons

        if var.SHOW_CHECKPOINTS:
            display.show_checkpoints()   # Display the checkpoints

        pygame.display.flip()  # Update the screen

        if var.START:   # When the game starts
            play()  # Play the game to begin

        var.CLOCK.tick(25)  # Limit the fps


def play(cars=None):
    """
    Play the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)
    """
    blit_circuit()  # Blit the circuit (to hide the dead cars)
    cars = init_cars_to_play(cars)  # Initialize the cars and add cars from the garage if needed

    while var.PLAY:  # While the game is not stopped
        ui.handle_events(cars)  # Detect events in the ui and do the corresponding action

        if not var.PAUSE and not var.FPS_TOO_HIGH:  # If the game is not paused
            play_turn(cars)  # Play a turn

            # Display explosions
            var.EXPLOSIONS.draw(var.WINDOW)  # Display the explosions
            var.EXPLOSIONS.update()  # Update the explosions

            # If we want to restart the last_run
            if var.PLAY_LAST_RUN:
                replay_last_run()  # Replay the last run

            # We stop the game if all the cars are dead or if the time is over or if we want to change the generation
            if var.NB_CARS_ALIVE == 0 or var.TICKS_REMAINING == 0 or var.CHANGE_GENERATION:
                stop_play(cars)  # Stop the game
                if var.TEST_ALL_CARS:
                    return  # If we want to test all the cars, we stop the game here so that we can test the next cars
                if (var.TEST_VALUE_GENETIC_PARAMETERS or var.TEST_MUTATION_CROSSOVER) and var.TEST_FINISHED:
                    return  # We quit if we finished the tests

        ui.erase()  # Erase the buttons
        ui.display(cars)  # Activate the buttons (This is here because we have to do this after erasing the screen and
        # We have ton continue to check the buttons even if the game is paused)

        pygame.display.flip()  # Update the screen

        update_fps()  # Update the fps

    open_window()  # Restart the game


def init_cars_to_play(cars):
    """
    Initialize the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)

    Returns:
        list: list of cars
    """
    random.seed(var.SEED)  # Initialize the random seed

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
        init_variables(len(cars))  # Initialize the data

    else:           # If we already played
        cars = add_garage_cars(cars)  # We add the car from the garage to the list of cars
        init_variables(len(cars), replay=True)  # Initialize the data

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

    # Erase explosions
    rect_blit_explosion = union_rect(var.RECTS_BLIT_EXPLOSION)  # Union of the rects for the blit
    var.WINDOW.blit(var.BACKGROUND, rect_blit_explosion, rect_blit_explosion)  # Erase the explosions
    var.RECTS_BLIT_EXPLOSION = []  # We reset the list of rects to blit

    if var.SHOW_CHECKPOINTS:
        display.show_checkpoints()  # Display the checkpoints

    for car in cars:  # For each car
        if not car.dead:  # If the car is not dead
            car.move()  # Move the car
            car.draw()  # Draw the cars

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

    if not var.TEST_MUTATION_CROSSOVER and not var.TEST_ALL_CARS:  # If we don't want to test the mutation and crossover
        while time.time() - time_before < 1:  # We wait 1 second
            # Erase explosions
            rect_blit_explosion = union_rect(var.RECTS_BLIT_EXPLOSION)  # Union of the rects for the blit
            var.WINDOW.blit(var.BACKGROUND, rect_blit_explosion, rect_blit_explosion)  # Erase the explosions
            var.RECTS_BLIT_EXPLOSION = []  # We reset the list of rects to blit

            # Erase cars
            rect_blit_car = union_rect(var.RECTS_BLIT_CAR)  # Union of the rects for the blit
            var.WINDOW.blit(var.BACKGROUND, rect_blit_car, rect_blit_car)  # Erase the cars
            var.RECTS_BLIT_CAR = []  # We reset the list of rects to blit

            # Display cars
            for car in cars:  # For each car
                car.draw()  # Draw the cars

            # Display explosions
            var.EXPLOSIONS.draw(var.WINDOW)  # Display the explosions
            var.EXPLOSIONS.update()  # Update the explosions

            # Display the buttons
            ui.handle_events(cars)  # Detect events in the ui and do the corresponding action
            ui.erase()  # Erase the buttons
            ui.display(cars)  # Activate the buttons

            pygame.display.flip()  # Update the screen

    var.CHANGE_GENERATION = False  # We stop the change of generation
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Reset the screen

    var.CARS_LAST_RUN = cars  # Save the last run
    if var.LAST_RUN_PLAYING:
        var.PLAY_LAST_RUN = False  # We are no longer replaying something

    if var.TEST_ALL_CARS:  # If we want to test all cars
        for car in cars:
            var.FILE_TEST.write(f'{car.genetic} {car.score}\n')  # Write the score of the car
        return  # We stop the game

    else:
        if var.TEST_MUTATION_CROSSOVER or var.TEST_VALUE_GENETIC_PARAMETERS:  # If we want to test the mutation and the crossover order
            var.LAP_COMPLETED = False
            for car in cars:
                if car.score > 150:
                    var.FILE_TEST.write(f'{var.NUM_GENERATION}\n')
                    var.TEST_FINISHED = True
                    return  # We stop the game
            if var.NUM_GENERATION > 24:
                var.FILE_TEST.write(f'{var.NUM_GENERATION}\n')
                var.TEST_FINISHED = True
                return

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
    image_checkpoint = pygame.image.load(f'{PATH_IMAGE}checkpoints/checkpoint.png')  # Image of the checkpoint
    var.WINDOW.blit(image_checkpoint, (450, 25))  # We add the image to the screen
    pygame.display.flip()  # Update the screen
    # We open the file to write the checkpoints
    with open(f'{PATH_DATA}checkpoints/{var.NUM_MAP}', 'w') as file_checkpoint_write:
        while 1:
            # We detect the mouse click to write the coordinates in the file
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game()  # Exit the game if we close the window
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    file_checkpoint_write.write(str(x) + ' ' + str(y) + '\n')


def run_test_all_cars():
    """
    Run all cars and save the results in a file
    """
    var.FPS = 9999
    var.SHOW_EXPLOSIONS = False

    var.FILE_TEST = open(f'{PATH_DATA}tests/all_cars/results/{var.NUM_MAP}', 'w')  # We open the file to write the results
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization
    var.PLAY = True

    tab_cars = []
    genetic_combinations = itertools.product(range(1, 7), repeat=6)
    for combination in genetic_combinations:
        genetic = Genetic(list(combination))
        tab_cars.append(Car(genetic))
        if len(tab_cars) == 10000:
            play(tab_cars)  # We play the game to test the cars
            tab_cars = []
    play(tab_cars)  # We play the game to test the cars


def run_test_mutation_crossover():
    """
    Run the genetic algorithm with different mutation and crossover orders
    """
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization
    var.PLAY = True

    for var.TEST_MODE in ['crossover_mutation']:
        var.FILE_TEST = open(f'{PATH_DATA}tests/genetic_parameters/{var.TEST_MODE}_{var.NUM_MAP}', 'a')
        for var.SEED in range(100, 200):
            play()
            var.NUM_GENERATION = 0


def run_test_value_genetic_parameters():
    """
    Run the genetic algorithm with different genetic parameters and save the results in a file
    """
    var.FPS = 9999  # We set the fps to a high value to run the game faster
    var.SHOW_EXPLOSIONS = False  # We don't show the explosions to run the game faster

    path_test = f'{PATH_DATA}tests/'
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization
    var.PLAY = True

    for var.CHANCE_MUTATION, var.CHANCE_CROSSOVER, var.PROPORTION_CARS_KEPT in [(0.3, 0.1, 0.2)]:
        var.FILE_TEST = open(f'{path_test}tests/genetic_parameters/{var.CHANCE_MUTATION}_{var.CHANCE_CROSSOVER}_{var.PROPORTION_CARS_KEPT}', 'a')
        for var.SEED in range(50):
            play()
            var.NUM_GENERATION = 0


def main():
    """
    Main function
    """
    try:
        load_parameters()  # Load the data
        change_camera(first_time=True)  # Change the camera
        create_background()  # Create the background
        change_map(first_time=True)  # Change the map to the first one
        load_cars()  # Load the cars (we do it here because we need the map to be loaded so Genetic can be initialized)
        ui.init()  # Initialize the ui
        SETTINGS.init()  # Initialize the settings

        # If we want to run all the cars
        if var.TEST_ALL_CARS:
            run_test_all_cars()  # Run all cars
        # If we want to see what is the best genetic algorithm
        elif var.TEST_MUTATION_CROSSOVER:
            run_test_mutation_crossover()  # Test the mutation and the crossover
        elif var.TEST_VALUE_GENETIC_PARAMETERS:
            run_test_value_genetic_parameters()
        else:
            open_window()  # Start the application

    except Exception as e:
        traceback.print_exc()  # Print the error
        exit_game()  # Exit the game if there is an error
        raise e


if __name__ == '__main__':
    """
    Main program
    """
    main()
