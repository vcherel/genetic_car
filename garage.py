import pygame  # To use pygame
import variables  # Import the variables
from constants import WINDOW, LARGE_FONT, FONT  # Import the constants
from rect_garage import RectGarage  # Import the rectangle garage

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
        for key in variables.MEMORY_CARS:
            if NB_RECTANGLE_MAX * ACTUAL_PAGE <= NB_RECTANGLE < NB_RECTANGLE_MAX * (ACTUAL_PAGE + 1):  # If the rectangle is in the good page
                if key == "dice":
                    for car in variables.MEMORY_CARS.get(key):
                        TAB_RECTANGLE.append(RectGarage((ACTUAL_X, ACTUAL_Y), "Dé " + car[0], car[1]))
                else:
                    TAB_RECTANGLE.append(RectGarage((ACTUAL_X, ACTUAL_Y), "Génération " + str(key), variables.MEMORY_CARS.get(key)))

                # We change the values of the variables
                update_variables()

            NB_RECTANGLE += 1  # We add one to the number of rectangle in the garage

        CHANGE_PAGE = False  # We don't have to change the page of the garage anymore

    for rect_garage in TAB_RECTANGLE:  # For each rectangle in the garage
        draw_next_rect(rect_garage)  # We draw the next rectangle in the garage


def erase_garage():
    """
    Erase the garage
    """
    rect = pygame.Rect(RECT_GARAGE)  # We create a rectangle with the position of the garage
    WINDOW.blit(variables.BACKGROUND, rect, rect)  # We erase the garage


def draw_next_rect(rect_garage):
    """
    Draw the next rectangle in the garage

    Args:
        rect_garage (RectGarage): rectangle to draw
    """
    # We draw the rectangle
    pygame.draw.rect(WINDOW, (0, 0, 0), (rect_garage.pos[0], rect_garage.pos[1], 225, 75), 2)
    # We write the name of the save
    WINDOW.blit(FONT.render(rect_garage.name, True, (0, 0, 0), (128, 128, 128)), (rect_garage.pos[0] + 10, rect_garage.pos[1] + 10))


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