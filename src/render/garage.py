from src.render.rect_garage import RectGarage  # Import the rectangle garage
import src.other.variables as var  # Import the variable
from src.game.car import Car  # Import the car
import pygame  # To use pygame


rect_display_garage = (500, 125, 500, 550)  # Display rectangle of the garage
nb_rectangle_max = 10  # Maximum number of rectangle in the garage


class Garage:
    def __init__(self):
        """
        Initialize the garage (in the structures.py file)
        """
        self.nb_rectangle = None  # Number of rectangle in the garage
        self.tab_rectangle = None  # List of the rectangle in the garage
        self.actual_x = None  # Actual x position to write the rectangles
        self.actual_y = None  # Actual y position to write the rectangles
        self.change_y = None  # True if the y position has to change in the next rectangle (it means we are at the right of the garage)
        self.actual_page = None  # Actual page of the garage
        self.reload_page = None  # True if we have to change the page of the garage (for example at the beginning)
        self.time_since_last_delete = None  # Time since the last delete of a car

    def init_garage(self):
        """
        Initialize the garage during the game
        """
        self.nb_rectangle = 0  # Number of rectangle in the garage
        self.tab_rectangle = []  # List of the rectangle in the garage
        self.actual_x = 0  # Actual x position to write the rectangles
        self.actual_y = 0  # Actual y position to write the rectangles
        self.change_y = False  # True if the y position has to change in the next rectangle (it means we are at the right of the garage)
        self.actual_page = 0  # Actual page of the garage
        self.reload_page = True  # True if we have to change the page of the garage (for example at the beginning)
        self.time_since_last_delete = 0  # Time since the last delete of a car
        self.display_garage()

    def display_garage(self):
        """
        Display the garage
        """

        # Create rectangles for the garage
        pygame.draw.rect(var.WINDOW, (128, 128, 128), rect_display_garage, 0)
        pygame.draw.rect(var.WINDOW, (115, 205, 255), rect_display_garage, 2)
        var.WINDOW.blit(var.LARGE_FONT.render('Voitures sauvegardées', True, (0, 0, 0), (128, 128, 128)), (rect_display_garage[0] + 95, rect_display_garage[1] + 10))

        # Reset the variables
        self.reset_variables()

        if self.reload_page:  # If we have to change the page of the garage
            self.tab_rectangle = []  # We reset the list of the rectangle in the garage

            # Create the rectangles for the pages
            num = 0  # The number to identify the id of the rectangle

            for key in var.MEMORY_CARS.keys():
                str_name = 'Dé ' if key == 'dice' else 'Génération '
                for car in var.MEMORY_CARS.get(key):
                    if nb_rectangle_max * self.actual_page <= self.nb_rectangle < nb_rectangle_max * (
                            self.actual_page + 1):  # If the rectangle is in the good page
                        self.tab_rectangle.append(RectGarage(num, car[0], (self.actual_x, self.actual_y), str_name + str(car[0]), car[1], key))
                        num += 1  # We add one to the number to identify the id of the rectangle
                        self.update_variables()  # We change the values of the variables
                    self.nb_rectangle += 1  # We add one to the number of rectangle in the garage

            self.reload_page = False  # We don't have to change the page of the garage anymore

        var.GENETICS_FROM_GARAGE = []  # We reset the list of the cars from the garage

        for rect_garage in self.tab_rectangle:  # For each rectangle in the garage
            if rect_garage.draw(self.time_since_last_delete):  # We draw the next rectangle in the garage
                self.reload_page = True  # We have to change the page of the garage
                self.time_since_last_delete = pygame.time.get_ticks()  # We reset the time since the last delete of a car

    def update_variables(self):
        """
        Update the variables to draw the next rectangle in the garage
        """
        if self.change_y:  # If we have to change the y position (it means we are at the right of the garage)
            self.actual_y += 90
            self.actual_x -= 240
        else:
            self.actual_x += 240
        self.change_y = not self.change_y  # At the next rectangle, we are going to change of axis

    def reset_variables(self):
        """
        Reset the variables
        """
        self.nb_rectangle = 0  # Number of rectangle in the garage
        self.actual_y = rect_display_garage[1] + 60  # Actual y position to write the rectangles
        self.actual_x = rect_display_garage[0] + 15  # Actual x position to write the rectangles
        self.change_y = False  # True if the y position has to change in the next rectangle


def erase_garage():
    """
    Erase the garage
    """
    rect = pygame.Rect(rect_display_garage)  # We create a rectangle with the position of the garage
    var.WINDOW.blit(var.BACKGROUND, rect, rect)  # We erase the garage


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


GARAGE = Garage()  # We create the garage
