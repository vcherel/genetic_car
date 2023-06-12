import pygame  # To use pygame
import variables as var  # Import the variables
from rect_garage import RectGarage  # Import the rectangle garage
from car import Car  # Import the car


rect_display_garage = (500, 125, 500, 550)  # Display rectangle of the garage

nb_rectangle_max = 10  # Maximum number of rectangle in the garage
nb_rectangle = 0    # Number of rectangle in the garage
tab_rectangle = []  # List of the rectangle in the garage

actual_y = 0        # Actual y position to write the rectangles
actual_x = 0        # Actual x position to write the rectangles
change_y = False    # True if the y position has to change in the next rectangle (it means we are at the right of the garage)

actual_page = 0     # Actual page of the garage
change_page = True   # True if we have to change the page of the garage (for example at the beginning)


def init_garage():
    """
    Initialize the garage
    """
    global change_page, actual_page

    actual_page = 0  # Actual page of the garage
    change_page = True  # We have to change the page of the garage
    display_garage()  # Display the garage


def display_garage():
    """
    Display the garage
    """
    global actual_y, actual_x, change_y, nb_rectangle, change_page, tab_rectangle

    # Create rectangles for the garage
    pygame.draw.rect(var.WINDOW, (128, 128, 128), rect_display_garage, 0)
    pygame.draw.rect(var.WINDOW, (115, 205, 255), rect_display_garage, 2)
    var.WINDOW.blit(var.LARGE_FONT.render('Voitures sauvegardées', True, (0, 0, 0), (128, 128, 128)), (rect_display_garage[0] + 95, rect_display_garage[1] + 10))

    # Reset the variables
    reset_variables()

    if change_page:  # If we have to change the page of the garage
        tab_rectangle = []  # We reset the list of the rectangle in the garage

        # Create the rectangles for the pages
        num = 0   # The number to identify the id of the rectangle

        # We first add the rectangles for the dice
        if var.MEMORY_CARS.get('dice'):
            for car in var.MEMORY_CARS.get('dice'):
                if nb_rectangle_max * actual_page <= nb_rectangle < nb_rectangle_max * (actual_page + 1):  # If the rectangle is in the good page
                    tab_rectangle.append(RectGarage((actual_x, actual_y), 'Dés ' + str(car[0]), num, car[1]))
                    num += 1  # We add one to the number to identify the id of the rectangle
                    update_variables()  # We change the values of the variables
                nb_rectangle += 1  # We add one to the number of rectangle in the garage

        # We add the rectangles for the genetics
        for key in var.MEMORY_CARS:
            if nb_rectangle_max * actual_page <= nb_rectangle < nb_rectangle_max * (actual_page + 1) and key != "dice":  # If the rectangle is in the good page and it's not the dice
                tab_rectangle.append(RectGarage((actual_x, actual_y), 'Génétique ' + str(key), num, var.MEMORY_CARS.get(key)))
                num += 1  # We add one to the number to identify the id of the rectangle
                update_variables()  # We change the values of the variables

            nb_rectangle += 1  # We add one to the number of rectangle in the garage

        change_page = False  # We don't have to change the page of the garage anymore

    var.GENETICS_FROM_GARAGE = []  # We reset the list of the cars from the garage

    for rect_garage in tab_rectangle:  # For each rectangle in the garage
        rect_garage.draw()  # We draw the next rectangle in the garage


def erase_garage():
    """
    Erase the garage
    """
    rect = pygame.Rect(rect_display_garage)  # We create a rectangle with the position of the garage
    var.WINDOW.blit(var.BACKGROUND, rect, rect)  # We erase the garage


def reset_variables():
    """
    Reset the variables
    """
    global actual_y, actual_x, change_y, nb_rectangle

    nb_rectangle = 0  # Number of rectangle in the garage
    actual_y = rect_display_garage[1] + 60  # Actual y position to write the rectangles
    actual_x = rect_display_garage[0] + 15  # Actual x position to write the rectangles
    change_y = False  # True if the y position has to change in the next rectangle


def update_variables():
    """
    Update the variables to draw the next rectangle in the garage
    """
    global actual_y, actual_x, change_y
    if change_y:
        actual_y += 90
        actual_x -= 240
    else:
        actual_x += 240
    change_y = not change_y  # At the next rectangle, we are going to change of axis


def add_garage_cars(cars):
    """
    Add the cars from the garage to the list of cars
    """
    if var.GENETICS_FROM_GARAGE:  # If we have a car from the garage
        if type(var.GENETICS_FROM_GARAGE) is list:  # If we have a car from the garage
            for gen in var.GENETICS_FROM_GARAGE:
                cars.append(Car(gen, view_only=True))  # Add cars from the garage to the list
        else:
            cars.append(Car(var.GENETICS_FROM_GARAGE, view_only=True))  # Add the car from the garage to the list
    return cars
