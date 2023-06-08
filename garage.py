import pygame  # To use pygame
import variables  # Import the variables
from constants import WINDOW, LARGE_FONT, FONT  # Import the constants
from rect_garage import RectGarage  # Import the rectangle garage
from car import Car  # Import the car


RECT_GARAGE = (500, 125, 500, 550)  # Position of the garage
NB_RECTANGLE_MAX = 10  # Maximum number of rectangle in the garage
NB_RECTANGLE = 0    # Number of rectangle in the garage

TAB_RECTANGLE = []  # List of the rectangle in the garage

ACTUAL_Y = 0        # Actual y position to write the rectangles
ACTUAL_X = 0        # Actual x position to write the rectangles
CHANGE_Y = False    # True if the y position has to change in the next rectangle (it means we are at the right of the garage)

ACTUAL_PAGE = 0     # Actual page of the garage
CHANGE_PAGE = True   # True if we have to change the page of the garage (for example at the beginning)


def init_garage():
    """
    Initialize the garage
    """
    global CHANGE_PAGE, ACTUAL_PAGE

    ACTUAL_PAGE = 0  # Actual page of the garage
    CHANGE_PAGE = True  # We have to change the page of the garage
    display_garage()  # Display the garage


def display_garage():
    """
    Display the garage
    """
    global ACTUAL_Y, ACTUAL_X, CHANGE_Y, NB_RECTANGLE, CHANGE_PAGE, TAB_RECTANGLE

    # Create rectangles for the garage
    pygame.draw.rect(WINDOW, (128, 128, 128), RECT_GARAGE, 0)
    pygame.draw.rect(WINDOW, (115, 205, 255), RECT_GARAGE, 2)
    WINDOW.blit(LARGE_FONT.render("Voitures sauvegardées", True, (0, 0, 0), (128, 128, 128)), (RECT_GARAGE[0] + 95, RECT_GARAGE[1] + 10))

    # Reset the variables
    reset_variables()

    if CHANGE_PAGE:  # If we have to change the page of the garage
        TAB_RECTANGLE = []  # We reset the list of the rectangle in the garage

        # Create the rectangles for the pages
        num = 0   # The number to identify the id of the rectangle

        # We first add the rectangles for the dice
        if variables.MEMORY_CARS.get("dice"):
            for car in variables.MEMORY_CARS.get("dice"):
                if NB_RECTANGLE_MAX * ACTUAL_PAGE <= NB_RECTANGLE < NB_RECTANGLE_MAX * (ACTUAL_PAGE + 1):  # If the rectangle is in the good page
                    TAB_RECTANGLE.append(RectGarage((ACTUAL_X, ACTUAL_Y), "Dés " + str(car[0]), num, car[1]))
                    num += 1  # We add one to the number to identify the id of the rectangle
                    update_variables()  # We change the values of the variables
                NB_RECTANGLE += 1  # We add one to the number of rectangle in the garage

        # We add the rectangles for the genetics
        for key in variables.MEMORY_CARS:
            if NB_RECTANGLE_MAX * ACTUAL_PAGE <= NB_RECTANGLE < NB_RECTANGLE_MAX * (ACTUAL_PAGE + 1) and key != "dice":  # If the rectangle is in the good page and it's not the dice
                TAB_RECTANGLE.append(RectGarage((ACTUAL_X, ACTUAL_Y), "Génétique " + str(key), num, variables.MEMORY_CARS.get(key)))
                num += 1  # We add one to the number to identify the id of the rectangle
                update_variables()  # We change the values of the variables

            NB_RECTANGLE += 1  # We add one to the number of rectangle in the garage

        CHANGE_PAGE = False  # We don't have to change the page of the garage anymore

    variables.GENETICS_FROM_GARAGE = []  # We reset the list of the cars from the garage

    for rect_garage in TAB_RECTANGLE:  # For each rectangle in the garage
        rect_garage.draw()  # We draw the next rectangle in the garage


def erase_garage():
    """
    Erase the garage
    """
    rect = pygame.Rect(RECT_GARAGE)  # We create a rectangle with the position of the garage
    WINDOW.blit(variables.BACKGROUND, rect, rect)  # We erase the garage


def reset_variables():
    """
    Reset the variables
    """
    global ACTUAL_Y, ACTUAL_X, CHANGE_Y, NB_RECTANGLE

    NB_RECTANGLE = 0  # Number of rectangle in the garage
    ACTUAL_Y = RECT_GARAGE[1] + 60  # Actual y position to write the rectangles
    ACTUAL_X = RECT_GARAGE[0] + 15  # Actual x position to write the rectangles
    CHANGE_Y = False  # True if the y position has to change in the next rectangle


def update_variables():
    """
    Update the variables to draw the next rectangle in the garage
    """
    global ACTUAL_Y, ACTUAL_X, CHANGE_Y
    if CHANGE_Y:
        ACTUAL_Y += 90
        ACTUAL_X -= 240
    else:
        ACTUAL_X += 240
    CHANGE_Y = not CHANGE_Y  # At the next rectangle, we are going to change of axis


def add_garage_cars(cars):
    """
    Add the cars from the garage to the list of cars
    """
    if variables.GENETICS_FROM_GARAGE:  # If we have a car from the garage
        if type(variables.GENETICS_FROM_GARAGE) is list:  # If we have a car from the garage
            for gen in variables.GENETICS_FROM_GARAGE:
                cars.append(Car(gen, view_only=True))  # Add cars from the garage to the list
        else:
            cars.append(Car(variables.GENETICS_FROM_GARAGE, view_only=True))  # Add the car from the garage to the list
    return cars
