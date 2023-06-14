import time  # To get the time
import pygame  # To use pygame
import variables as var  # Import the variables
import random  # To generate random numbers
from display import display_checkpoints, edit_background  # To see the checkpoints
from ui import detect_events_ui, detect_buttons_click, init_ui  # Import the ui
from genetic_algorithm import apply_genetic  # Import the genetic algorithm
from utils import union_rect  # Import the utils
from garage import add_garage_cars  # Import the garage
from car import Car  # Import the car

fps = 60  # FPS of the game
seed = 1  # Seed of the game

change_checkpoint = False  # Change the checkpoint for the actual map
see_checkpoints = False  # See the checkpoints


def open_window():
    """
    Open the window of the game and manage the events until the game is started or closed
    """
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization

    while 1:
        # If we want to change the checkpoints
        if change_checkpoint:
            # We display the image that explain that we are in the checkpoint mode
            image_checkpoint = pygame.image.load("images/checkpoint.png")  # Image of the checkpoint
            var.WINDOW.blit(image_checkpoint, (450, 25))  # We add the image to the screen
            pygame.display.flip()  # Update the screen
            # We open the file to write the checkpoints
            with open("data/checkpoints_" + str(var.NUM_MAP), "w") as file_checkpoint_write:
                while 1:
                    # We detect the mouse click to write the coordinates in the file
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            var.exit_game()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                x, y = event.pos
                                file_checkpoint_write.write(str(x) + " " + str(y) + "\n")

        detect_events_ui()  # Detect events in the ui and do the corresponding action=
        detect_buttons_click()  # Activate the buttons

        if see_checkpoints:
            display_checkpoints()   # Display the checkpoints

        pygame.display.flip()  # Update the screen

        if var.START:   # When the game starts
            play()  # Play the game

        var.CLOCK.tick(fps)  # Limit FPS


def play(cars=None):
    """
    Play the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)
    """
    if cars is None:  # If it is the first time we play
        cars = [Car() for _ in range(var.NB_CARS)]  # List of cars
        cars = add_garage_cars(cars)  # Add the cars in the garage
        var.init_variables(len(cars))

    else:           # If we already played
        var.init_variables(len(cars), replay=True)  # Initialize the variables

    while var.PLAY:  # While the game is not stopped
        time_begin_turn = time.time()

        detect_events_ui()  # Detect events in the ui and do the corresponding action

        if not var.PAUSE:  # If the game is not paused
            # Erase the screen
            if var.DEBUG:
                var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization only in debug mode (for the cones)
            else:
                var.WINDOW.blit(var.BACKGROUND, var.RECT_BLIT_CAR, var.RECT_BLIT_CAR)  # We delete only the cars
            for rect in var.RECTS_BLIT_UI:
                var.WINDOW.blit(var.BACKGROUND, rect, rect)  # We delete the ui
            var.RECTS_BLIT_UI = []  # We reset the list of rects to blit the ui

            if see_checkpoints:
                display_checkpoints()   # Display the checkpoints

            rects = []          # List of rects for the blit
            for car in cars:    # For each car
                if not car.dead:    # If the car is not dead
                    car.move()          # Move the car
                    rects.append(car.rotated_rect)    # Draw the car and add the rect to the list
                car.draw()  # Draw the car

            var.RECT_BLIT_CAR = union_rect(rects)  # Union of the rects for the blit
            # pygame.draw.rect(var.WINDOW, (120, 0, 0), var.RECT_BLIT_CAR, 1)  # Draw the rect for the blit of the cars

            if var.NB_CARS_ALIVE == 0 or time.time() - var.START_TIME - var.DURATION_PAUSES > var.TIME_REMAINING:    # If all cars are dead
                var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Reset the screen
                if var.USE_GENETIC:
                    cars = apply_genetic(cars)  # Genetic algorithm
                    play(cars)  # Restart the game with the new cars
                else:
                    play()  # Restart the game

        detect_buttons_click()  # Activate the buttons
        pygame.display.update()  # Update the screen

        try:  # To avoid division by 0
            var.ACTUAL_FPS = int(1 / (time.time() - time_begin_turn))  # Actual FPS
        except ZeroDivisionError:
            var.ACTUAL_FPS = 0

        while time.time() - time_begin_turn < 1 / fps:  # Wait to have the right FPS
            var.ACTUAL_FPS = fps

    open_window()  # Restart the game


if __name__ == '__main__':
    """
    Main program
    """
    var.init_variables_pygame()  # Initialize the variables
    if seed:
        random.seed(seed)  # Initialize the random seed
    var.load_variables()  # Load the variables
    var.change_map(var.NUM_MAP)  # Change the map to the first one
    init_ui()  # Initialize the ui
    edit_background()  # Add elements not clickable to the background
    open_window()  # Start the game
