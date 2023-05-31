import pygame  # To use pygame
from variables import BACKGROUND, START, MULTIPLE_CARS, NB_CARS, NUM_MAP, CAR_IMAGE  # Import the variables
from constants import WINDOW, START_POS   # Import the constants
from ui import detect_events  # Import the detect_events function
from car import Car  # Import the car


def open_window():
    """
    Open the window of the game
    """
    WINDOW.blit(BACKGROUND, (0, 0))  # Screen initialization
    pygame.display.update()  # Update the screen

    while 1:
        detect_events()  # Detect events

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
        # Erase all the cars and detection cones
        WINDOW.blit(BACKGROUND, (0, 0))

        all_dead = True     # True if all cars are dead
        for car in cars:    # For each car
            if not car.dead:
                all_dead = False    # At least one car is alive
                car.move()          # Move the car
            car.draw()  # Draw the car

        detect_events()  # Detect events in the ui
        pygame.display.update()  # Update the screen

        if all_dead:
            print("All dead")


if __name__ == '__main__':
    """
    Main program
    """
    open_window()  # Start the game
