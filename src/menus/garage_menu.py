from src.other.utils import convert_to_new_window, scale_image  # Utils functions
from src.menus.rect_garage import RectGarage  # Import the rectangle garage
from src.render.button import Button  # Import the button
import src.data.variables as var  # Import the variable
from src.game.car import Car  # Import the car
import pygame  # To use pygame
import time  # To get the time


"""
This function contains the Garage class and all the functions related to it. The garage is the place where the cars are stored.
"""


class Garage:
    """
    This class is used to represent the garage, used to store the cars
    """
    def __init__(self):
        """
        Initialize the garage
        """
        self.x, self.y = convert_to_new_window((500, 125))  # Position of the garage
        self.image = scale_image(pygame.image.load(var.PATH_IMAGE + '/garage_menu.png'))  # Image of the garage
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())  # Rect of the garage
        self.nb_rectangles = 0  # Number of rectangle in the garage (we use this as a counter to see if we are on the page to draw)
        self.rectangles = []  # List of the rectangles in the garage
        self.selected_rects = [False] * len(var.MEMORY_CARS)  # Selected rectangles
        self.actual_page = 0  # Actual page of the garage
        self.reload_page = True  # True if we have to change the page of the garage (for example at the beginning, when we change of page, or after a deletion)
        self.time_since_last_delete = 0  # Time since the last delete of a car
        self.trash_button = Button(x=930, y=135, image_name='trash', scale=0.2)
        self.next_button = Button(x=940, y=623, image_name='next_page', scale=0.2)
        self.previous_button = Button(x=520, y=623, image_name='previous_page', scale=0.2)

    def __str__(self):
        """
        Return the string to display with the print function

        Returns:
            str: string of the garage
        """
        string = f'Garage : {self.nb_rectangles} rectangles :'
        for rect in self.rectangles:
            string += f'\n{rect}'
        return string

    def reset(self):
        """
        Reset the data
        """
        self.rectangles = []  # We reset the list of the rectangle in the garage
        self.nb_rectangles = 0  # Number of rectangle in the garage

    def resize(self):
        """
        Resize the garage
        """
        self.x, self.y = convert_to_new_window((500, 125))
        self.image = scale_image(pygame.image.load(var.PATH_IMAGE + '/garage_menu.png'))  # Image of the garage
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())  # Rect of the garage
        self.trash_button = Button(x=930, y=135, image_name='trash', scale=0.2)
        self.next_button = Button(x=940, y=623, image_name='next_page', scale=0.2)
        self.previous_button = Button(x=520, y=623, image_name='previous_page', scale=0.2)
        self.reload()  # We reload the page of the garage

    def draw(self):
        """
        Display the garage
        """
        var.WINDOW.blit(self.image, (self.x, self.y))  # Display the garage window

        self.draw_rects_garage()  # We draw the rectangles corresponding to the cars of the garage
        self.draw_trash_button()  # We draw the trash button

        if self.reload_page:  # If we have to change the page of the garage
            self.reload()  # We reload the page

        self.draw_arrows()  # We change the page of the garage

    def draw_rects_garage(self):
        """
        Draw the rectangles corresponding to cars in the garage
        """
        for rect_garage in self.rectangles:  # For each rectangle in the garage
            deleted, selected = rect_garage.draw(self.time_since_last_delete)  # We draw the rectangle

            if deleted:  # If the rect has been deleted
                # We delete the rectangle : we just have to reload the page and update the variable selected_rects
                self.reload_page = True  # We have to change the page of the garage
                self.time_since_last_delete = time.time()  # We reset the time since the last delete of a car (to avoid deleting all in one long click)
                self.update_selected_rects(rect_garage.id_rect)  # We update which rectangles are selected

            elif selected:  # If the rect has been selected (clicked)
                self.selected_rects[self.get_index_rect(rect_garage.id_rect)] = not self.selected_rects[self.get_index_rect(rect_garage.id_rect)]  # We update the selected_rects variable

    def update_selected_rects(self, id_rect_to_delete):
        """
        Update the selected_rects variables so there is still the good rectangles selected after a rectangle is deleted

        Args:
            id_rect_to_delete (int): id of the rectangle to delete
        """
        index_rect_to_delete = self.get_index_rect(id_rect_to_delete)  # Index of the rectangle to delete
        for i in range(index_rect_to_delete, len(var.MEMORY_CARS) - 1):
            self.selected_rects[i] = self.selected_rects[i + 1]
        self.selected_rects.pop(len(var.MEMORY_CARS) - 1)

    def draw_trash_button(self):
        """
        Draw the trash button and delete the cars if the button is activated
        """
        self.trash_button.draw()  # We draw the trash button
        if self.trash_button.activated:
            var.MEMORY_CARS = []  # We reset the memory of the cars
            var.SELECTED_MEMORY_CARS = []  # We reset the selected memory of the cars
            var.ACTUAL_IDS_MEMORY_CARS = 1  # We reset the actual ids of the memory cars
            self.selected_rects = []  # We reset the selected rectangles
            self.reload_page = True  # We have to change the page of the garage

    def reload(self):
        """
        Reload the page of the garage
        """
        # We add False to the selected_rects list if there is more cars in the memory than before
        if len(var.MEMORY_CARS) > len(self.selected_rects):
            for _ in range(len(var.MEMORY_CARS) - len(self.selected_rects)):
                self.selected_rects.append(False)

        self.reset()  # We reset the variables of the menu
        id_rect = 0  # The number to identify the id of the rectangle
        for memory_car in var.MEMORY_CARS:  # For each car in the memory
            # If the rectangle is in the good page
            if 10 * self.actual_page <= self.nb_rectangles < 10 * (self.actual_page + 1):
                # We add the rectangle to the list of the rectangles
                self.rectangles.append(RectGarage(id_rect=id_rect, memory_car=memory_car, selected=self.selected_rects[self.get_index_rect(id_rect)]))
                id_rect += 1  # We add one to the number to identify the id of the rectangle
            self.nb_rectangles += 1  # We add one to the number of rectangle in the garage

        self.reload_page = False  # We don't have to change the page of the garage anymore

    def draw_arrows(self):
        """
        Check if we have to change the page of the garage (click on the arrows)
        """
        if (self.actual_page + 1) * 10 < self.nb_rectangles:  # If we are not at the last page
            self.next_button.draw()  # We draw the next button
            if self.next_button.just_clicked:
                self.actual_page += 1
                self.reload_page = True  # We have to change the page of the garage

        if self.actual_page > 0:  # If we are not at the first page
            self.previous_button.draw()  # We draw the previous button
            if self.previous_button.just_clicked:
                self.actual_page -= 1
                self.reload_page = True  # We have to change the page of the garage


    def erase_garage(self):
        """
        Erase the garage
        """
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)  # We erase the garage

    def get_index_rect(self, id_rect):
        """
        Return the index of a rectangle in the self.selected list
        We have to take into account the actual page
        """
        return 10 * self.actual_page + id_rect


def add_garage_cars(cars):
    """
    Add the cars from the garage to the list of cars
    """
    for memory_car in var.SELECTED_MEMORY_CARS:
        cars.append(Car(genetic=memory_car.genetic, best_scores=memory_car.best_scores, color=memory_car.color, id_memory_car=memory_car.id))  # Add cars from the garage to the list
    return cars


GARAGE = Garage()  # We create the garage
