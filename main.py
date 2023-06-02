import sys  # To quit the game
import pygame  # To use pygame
import variables  # Import the variables
from variables import CHANGE_CHECKPOINT, SEE_CHECKPOINTS, change_map  # Import the variables
from display import display_checkpoints, edit_background  # To see the checkpoints
from ui import detect_events_ui  # Import the detect_events function
from constants import WINDOW, START_POS   # Import the constants
from genetic_algorithm import apply_genetic  # Import the genetic algorithm
from car import Car  # Import the car


def open_window():
    """
    Open the window of the game
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

        WINDOW.blit(variables.BACKGROUND, (0, 0))  # Screen initialization
        detect_events_ui()  # Detect events in the ui and draw buttons

        if SEE_CHECKPOINTS:
            display_checkpoints()   # Display the checkpoints

        pygame.display.flip()  # Update the screen

        if variables.START:   # When the game starts
            play()  # Play the game


def play(cars=None):
    """
    Play the game

    Args:
        cars (list): list of cars (if None, it is the first time we play)
    """
    if cars is None:
        cars = [Car(variables.CAR_IMAGE, START_POS[variables.NUM_MAP]) for _ in range(variables.NB_CARS)]  # List of cars

    while variables.PLAY:  # While the game is not stopped
        WINDOW.blit(variables.BACKGROUND, (0, 0))  # Screen initialization
        detect_events_ui()  # Detect events in the ui and draw buttons

        if SEE_CHECKPOINTS:
            display_checkpoints()   # Display the checkpoints

        all_dead = True     # True if all cars are dead
        for car in cars:    # For each car
            if not car.dead:
                all_dead = False    # At least one car is alive
                car.move()          # Move the car
            car.draw()  # Draw the car

        pygame.display.update()  # Update the screen

        if all_dead:    # If all cars are dead
            if variables.USE_GENETIC:
                cars = apply_genetic(cars)  # Genetic algorithm
                play(cars)  # Restart the game with the new cars
            else:
                play()  # Restart the game

    open_window()  # Restart the game


if __name__ == '__main__':
    """
    Main program
    """
    change_map(variables.NUM_MAP)  # Change the map to the first one
    edit_background()  # Add elements not clickable to the background
    open_window()  # Start the game
