from src.game.constants import CHANGE_CHECKPOINTS, SEE_CHECKPOINTS, FPS, USE_GENETIC, SEED  # Import the constants
from src.game.genetic_algorithm import apply_genetic  # Import the genetic algorithm
from src.render.garage import add_garage_cars  # Import the garage
from src.game.genetic import Genetic  # Import the genetic class
from src.other.utils import union_rect  # Import the utils
import src.render.display as display  # Import the display
import src.other.variables as var  # Import the variables
from src.game.car import Car  # Import the car
from src.other.analyze_data import analyze_data  # Import the analyze_data function
import os.path  # To get the path of the file
import random  # To generate random numbers
import src.render.ui as ui  # Import the ui
import pygame  # To use pygame
import time  # To get the time

"""
This file contains all the functions used to play the game
"""

rect_blit_car = pygame.rect.Rect(0, 0, 0, 0)  # Coordinates of the rect used to erase the cars of the screen

if var.TEST_ALL_CARS:  # If we want to test_0 all the cars
    file = open(os.path.dirname(__file__) + '/../data/test_0', 'a')  # File to write the scores of every possible car if necessary


def open_window():
    """
    Open the window of the game and manage the events until the game is started or closed
    """
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization

    while 1:
        # If we want to change the checkpoints
        if CHANGE_CHECKPOINTS:
            # We display the image that explain that we are in the checkpoint mode
            image_checkpoint = pygame.image.load(os.path.dirname(__file__) + '/../images/checkpoint.png')  # Image of the checkpoint
            var.WINDOW.blit(image_checkpoint, (450, 25))  # We add the image to the screen
            pygame.display.flip()  # Update the screen
            # We open the file to write the checkpoints
            with open(os.path.dirname(__file__) + '/../data/checkpoints_' + str(var.NUM_MAP), 'w') as file_checkpoint_write:
                while 1:
                    # We detect the mouse click to write the coordinates in the file
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            var.exit_game()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                x, y = event.pos
                                file_checkpoint_write.write(str(x) + ' ' + str(y) + '\n')

        ui.handle_events()  # Detect events in the ui and do the corresponding action=
        ui.display()  # Activate the buttons

        if SEE_CHECKPOINTS:
            display.show_checkpoints()   # Display the checkpoints

        pygame.display.flip()  # Update the screen

        if var.START:   # When the game starts
            play()  # Play the game

        var.CLOCK.tick(FPS)  # Limit FPS


def play(cars=None):
    """
    Play the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)
    """
    global rect_blit_car

    if cars is None:  # If it is the first time we play
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


    while var.PLAY:  # While the game is not stopped
        time_begin_turn = time.time()

        ui.handle_events(cars)  # Detect events in the ui and do the corresponding action

        if not var.PAUSE:  # If the game is not paused
            # Erase the ui
            rect_blit_ui = union_rect(var.RECTS_BLIT_UI)  # Union of the rects for the blit
            var.WINDOW.blit(var.BACKGROUND, rect_blit_ui, rect_blit_ui)  # Erase the ui
            var.RECTS_BLIT_UI = []  # We reset the list of rects to blit

            # Erase the cars
            rect_blit_car = union_rect(var.RECTS_BLIT_CAR)  # Union of the rects for the blit
            var.WINDOW.blit(var.BACKGROUND, rect_blit_car, rect_blit_car)  # Erase the cars
            var.RECTS_BLIT_CAR = []  # We reset the list of rects to blit

            if SEE_CHECKPOINTS:
                display.show_checkpoints()   # Display the checkpoints

            for car in cars:    # For each car
                if not car.dead:    # If the car is not dead
                    car.move()         # Move the car
                    var.RECTS_BLIT_CAR.append(car.rotated_rect)    # Draw the car and add the rect to the list
                car.draw_car()  # Draw the car

            # pygame.draw.rect(var.WINDOW, (120, 0, 0), rect_blit_car, 1)  # Draw the rect for the blit of the cars

            # If we want to restart the last_run
            if var.PLAY_LAST_RUN:
                var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Reset the screen
                var.PLAY_LAST_RUN = False  # We stop the replay
                var.NUM_GENERATION -= 1  # We go back to the previous generation

                # We reset the cars
                cars = [car.reset() for car in var.CARS_LAST_RUN if not car.view_only and not car.best_car]
                play(cars)  # We restart the game with the last run

            if var.NB_CARS_ALIVE == 0 or time.time() - var.START_TIME - var.DURATION_PAUSES > var.TIME_REMAINING:    # If all cars are dead
                var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Reset the screen

                var.CARS_LAST_RUN = cars  # Save the last run

                if var.TEST_ALL_CARS:  # If we want to test all cars
                    for car in cars:
                        file.write(f'{car.genetic} {car.score}\n')  # Write the score of the car
                    return  # We stop the game
                elif USE_GENETIC:
                    cars = apply_genetic(cars)  # Genetic algorithm
                    play(cars)  # Restart the game with the new cars
                else:
                    play()  # Restart the game

        ui.display()  # Activate the buttons (This is here because we have to do this after erasing the screen and
        # we have ton continue to check the buttons even if the game is paused)

        pygame.display.flip()  # Update the screen

        try:  # To avoid division by 0
            var.ACTUAL_FPS = int(1 / (time.time() - time_begin_turn))  # Actual FPS
        except ZeroDivisionError:
            var.ACTUAL_FPS = 0

        while time.time() - time_begin_turn < 1 / FPS:  # Wait to have the right FPS
            var.ACTUAL_FPS = FPS

    open_window()  # Restart the game


if __name__ == '__main__':
    """
    Main program
    """
    if SEED:
        random.seed(SEED)  # Initialize the random seed
    var.load_variables()  # Load the variables
    var.change_map(first_time=True)  # Change the map to the first one
    ui.init()  # Initialize the ui
    display.edit_background()  # Add elements not clickable to the background


    if var.SHOW_ANALYSIS:
        scores = analyze_data('/test_' + str(var.NUM_MAP), '/result_analysis')
        scores = [score for score in scores if score < len(var.CHECKPOINTS)]

        turns = [0] * len(var.CHECKPOINTS)
        for score in scores:
            turns[score] += 1
        max_turns = max(turns)

        # Draw the circles
        for pos, score in zip(var.CHECKPOINTS, turns):

            # Calculate the red value based on the score
            red_value = int(score / max_turns * 255)  # Adjust the scaling if needed

            # If it is not white
            if red_value != 0:
                # Create the color tuple with the adjusted red value
                circle_color = (255, 255 - red_value, 255 - red_value)

                # Draw the circle with the calculated color
                pygame.draw.circle(var.BACKGROUND, circle_color, pos, 25)

        # var.BACKGROUND.blit(var.BACKGROUND_MASK.to_surface(), (0, 0))  # Reset the screen

    # If we want to run all the cars
    if var.TEST_ALL_CARS:
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
                                    play(tab_cars)
                                    tab_cars = []
    else:
        open_window()  # Start the game
