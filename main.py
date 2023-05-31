import pygame  # To use pygame
from variables import BACKGROUND, START, MODE, NB_CARS, NUM_MAP  # Import the variables
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
    image = pygame.image.load("images/car.jpg")  # Image of the car
    pos = START_POS[NUM_MAP]  # Position of the car

    if MODE == "car":       # One car
        cars = [Car(image, pos)]  # List of cars
    else:                   # Multiple cars
        cars = [Car(image, pos) for _ in range(NB_CARS)]

    while 1:
        for car in cars:
            car.update()
            car.draw()

        detect_events()


if __name__ == '__main__':
    """
    Main program
    """
    open_window()  # Start the game
