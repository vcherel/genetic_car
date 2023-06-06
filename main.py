import sys  # To quit the game
import time  # To get the time
import pygame  # To use pygame
import variables  # Import the variables
import random  # To generate random numbers
from constants import WINDOW, START_POS, CLOCK, FPS, TIME_GENERATION, SEED   # Import the constants
from variables import CHANGE_CHECKPOINT, SEE_CHECKPOINTS, change_map  # Import the variables
from display import display_checkpoints, edit_background  # To see the checkpoints
from genetic_algorithm import apply_genetic  # Import the genetic algorithm
from utils import union_rect  # Import the union_rect function
from ui import detect_events_ui, activate_ui  # Import the ui
from car import Car  # Import the car


def open_window():
    WINDOW.blit(variables.BACKGROUND, (0, 0))  # Screen initialization
    """
    Open the window of the game and manage the events until the game is started or closed
    """
    while 1:
        # If we want to change the checkpoints
        if CHANGE_CHECKPOINT:
            # We display the image that explain that we are in the checkpoint mode
            image_checkpoint = pygame.image.load("images/checkpoint.png")  # Image of the checkpoint
            WINDOW.blit(image_checkpoint, (450, 25))  # We add the image to the screen
            pygame.display.flip()  # Update the screen
            # We open the file to write the checkpoints
            with open("data/checkpoints_" + str(variables.NUM_MAP), "w") as file_checkpoint_write:
                while 1:
                    # We detect the mouse click to write the coordinates in the file
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()  # Quitter le jeu
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                x, y = event.pos
                                file_checkpoint_write.write(str(x) + " " + str(y) + "\n")

        detect_events_ui()  # Detect events in the ui and do the corresponding action

        activate_ui()  # Activate the buttons
        if SEE_CHECKPOINTS:
            display_checkpoints()   # Display the checkpoints

        pygame.display.flip()  # Update the screen

        if variables.START:   # When the game starts
            play()  # Play the game

        CLOCK.tick(FPS)  # Limit FPS


def play(cars=None):
    """
    Play the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)
    """
    if cars is None:
        cars = [Car(variables.CAR_IMAGE, START_POS[variables.NUM_MAP]) for _ in range(variables.NB_CARS)]  # List of cars

    variables.NB_CARS_ALIVE = variables.NB_CARS  # Number of cars alive

    variables.TIME_REMAINING = TIME_GENERATION  # Time remaining for the generation
    variables.START_TIME = time.time()  # Start time of the generation
    variables.DURATION_PAUSES = 0  # We initialize the duration of the pause to 0

    while variables.PLAY:  # While the game is not stopped
        detect_events_ui()  # Detect events in the ui and do the corresponding action

        # If the game is paused
        if variables.PAUSE:
            activate_ui()  # Activate the buttons
            pygame.display.update()  # Update the screen

        if not variables.PAUSE:
            # Erase the screen
            if variables.DEBUG:
                WINDOW.blit(variables.BACKGROUND, (0, 0))  # Screen initialization only in debug mode (for the cones)
            else:
                WINDOW.blit(variables.BACKGROUND, variables.RECT_BLIT_CAR, variables.RECT_BLIT_CAR)  # We delete only the cars
            for rect in variables.RECTS_BLIT_UI:
                WINDOW.blit(variables.BACKGROUND, rect, rect)  # We delete the ui
            variables.RECTS_BLIT_UI = []  # We reset the list of rects to blit the ui

            activate_ui()  # Draw the buttons and do the corresponding action
            if SEE_CHECKPOINTS:
                display_checkpoints()   # Display the checkpoints

            rects = []          # List of rects for the blit
            for car in cars:    # For each car
                if not car.dead:    # If the car is not dead
                    car.move()          # Move the car
                    rects.append(car.rotated_rect)    # Draw the car and add the rect to the list
                car.draw()  # Draw the car

            variables.RECT_BLIT_CAR = union_rect(rects)  # Union of the rects for the blit
            # pygame.draw.rect(WINDOW, (120, 0, 0), variables.RECT_BLIT, 1)  # Draw the rect for the blit of the cars

            pygame.display.update()  # Update the screen

            if variables.NB_CARS_ALIVE == 0 or time.time() - variables.START_TIME - variables.DURATION_PAUSES > variables.TIME_REMAINING:    # If all cars are dead
                WINDOW.blit(variables.BACKGROUND, (0, 0))  # Reset the screen
                if variables.USE_GENETIC:
                    variables.GENERATION += 1  # Increment the number of generation
                    cars = apply_genetic(cars)  # Genetic algorithm
                    play(cars)  # Restart the game with the new cars
                else:
                    play()  # Restart the game

            CLOCK.tick(FPS)  # Limit FPS

    open_window()  # Restart the game


if __name__ == '__main__':
    """
    Main program
    """
    if SEED:
        random.seed(SEED)  # Initialize the random seed
    change_map(variables.NUM_MAP)  # Change the map to the first one
    edit_background()  # Add elements not clickable to the background
    open_window()  # Start the game
