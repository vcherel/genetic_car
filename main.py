import sys  # To quit the game
import pygame  # To use pygame
import variables  # Import the variables
from variables import CHANGE_CHECKPOINT, SEE_CHECKPOINTS, change_map  # Import the variables
from display import display_checkpoints, edit_background  # To see the checkpoints
from constants import WINDOW, START_POS, CLOCK, FPS   # Import the constants
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

    while variables.PLAY:  # While the game is not stopped
        detect_events_ui()  # Detect events in the ui and do the corresponding action
        if variables.PAUSE:
            activate_ui()  # Activate the buttons
            pygame.display.update()  # Update the screen

        if not variables.PAUSE:
            # Erase the screen
            if variables.DEBUG:
                WINDOW.blit(variables.BACKGROUND, (0, 0))  # Screen initialization only in debug mode (for the cones)
            else:
                WINDOW.blit(variables.BACKGROUND, variables.RECT_BLIT, variables.RECT_BLIT)  # We delete only the cars

            activate_ui()  # Draw the buttons and do the corresponding action
            if SEE_CHECKPOINTS:
                display_checkpoints()   # Display the checkpoints

            all_dead = True     # True if all cars are dead
            rects = []          # List of rects for the blit
            for car in cars:    # For each car
                if not car.dead:
                    all_dead = False    # At least one car is alive
                    car.move()          # Move the car
                    rects.append(car.rotated_rect)    # Draw the car and add the rect to the list
                car.draw()  # Draw the car

            variables.RECT_BLIT = union_rect(rects)  # Union of the rects for the blit
            # pygame.draw.rect(WINDOW, (120, 0, 0), variables.RECT_BLIT, 1)  # Draw the rect for the blit

            pygame.display.update()  # Update the screen

            if all_dead:    # If all cars are dead
                WINDOW.blit(variables.BACKGROUND, (0, 0))  # Reset the screen
                if variables.USE_GENETIC:
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
    change_map(variables.NUM_MAP)  # Change the map to the first one
    edit_background()  # Add elements not clickable to the background
    open_window()  # Start the game
