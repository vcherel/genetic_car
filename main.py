import sys  # To quit the game
import pygame  # To use pygame
from variables import BACKGROUND, START, MULTIPLE_CARS, NB_CARS, NUM_MAP, CAR_IMAGE, CHANGE_CHECKPOINT  # Import the variables
from constants import WINDOW, START_POS   # Import the constants
from ui import detect_events_ui, edit_background  # Import the detect_events function
from car import Car  # Import the car


def open_window():
    """
    Open the window of the game
    """
    edit_background()  # Add elements not clickable to the background
    WINDOW.blit(BACKGROUND, (0, 0))  # Screen initialization
    pygame.display.flip()  # Update the screen

    while 1:
        detect_events_ui()  # Detect events in the ui and draw buttons

        # If we want to change the checkpoints
        if CHANGE_CHECKPOINT:
            # We display the image that explain that we are in the checkpoint mode
            image_checkpoint = pygame.image.load("images/checkpoint.png")  # Image of the checkpoint
            WINDOW.blit(image_checkpoint, (450, 25))  # We add the image to the screen
            pygame.display.flip()  # Update the screen
            # We open the file to write the checkpoints
            with open("data/checkpoints_" + str(NUM_MAP), "w") as file_checkpoint_write:
                while 1:
                    # We detect the mouse click to write the coordinates in the file
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()  # Quitter le jeu
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if event.button == 1:
                                x, y = event.pos
                                file_checkpoint_write.write(str(x) + " " + str(y) + "\n")
        if START:   # When the game starts
            play()  # Play the game


def play():
    """
    Play the game
    """
    pos = START_POS[NUM_MAP]  # Position of the car

    if MULTIPLE_CARS:       # One car
        cars = [Car(CAR_IMAGE, pos) for _ in range(NB_CARS)]  # List of cars
    else:                   # Multiple cars
        cars = [Car(CAR_IMAGE, pos)]

    while 1:

        WINDOW.blit(BACKGROUND, (0, 0))  # Screen initialization
        detect_events_ui()  # Detect events in the ui and draw buttons

        all_dead = True     # True if all cars are dead
        for car in cars:    # For each car
            if not car.dead:
                all_dead = False    # At least one car is alive
                car.move()          # Move the car
            car.draw()  # Draw the car

        detect_events_ui()  # Detect events in the ui
        pygame.display.update()  # Update the screen

        if all_dead:    # If all cars are dead
            play()


if __name__ == '__main__':
    """
    Main program
    """
    open_window()  # Start the game
