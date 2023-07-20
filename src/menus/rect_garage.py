from src.other.utils import convert_to_new_window  # To convert positions when resizing the window
from src.data.data_classes import MemoryCar  # Import the memory car class
from src.data.constants import CAR_COLORS  # Import the constants
from src.menus.dice_menu import DICE_MENU  # Import the dice menu
from src.render.button import Button  # Import the button class
import src.data.variables as var  # Import the data
import random  # To get random numbers
import pygame  # To play the game
import time  # To get the time


"""
This file contains the RectGarage class and all the functions related to it. A rectangle garage is a rectangle that contains the cars saved in the garage menu.
"""


class RectGarage:
    """
    This class is used to represent a slot for a car in the garage menu
    """
    def __init__(self, x, y, id_rect, memory_car, selected):
        """
        Initialization of the rectangle garage
        A Rectangle garage is a rectangle that contains the cars saved in the garage menu

        Args:
            x (int): x position of the rectangle
            y (int): y position of the rectangle
            id_rect (int): id of the rectangle
            memory_car (MemoryCar): memory car of the rectangle
        """
        self.x, self.y = x, y  # Position of the rectangle
        self.id_rect = id_rect  # Id of the rectangle
        self.memory_car = memory_car  # Memory car of the rectangle
        self.last_time_color_clicked = 0  # Last time the color was clicked

        # Buttons
        self.edit_button = Button(x=x + 188, y=y + 40, image_name='pen', scale=0.15)  # Button to edit the car
        self.select_button = Button(x=x + 188, y=y + 8, image_name='checkbox', scale=0.07)  # Button of the writing button
        self.selected = selected  # If the car is selected or not
        self.delete_button = Button(x=x + 153, y=y + 5, image_name='trash', scale=0.14)  # Button to delete the car
        self.name_button = Button(x=x + 10, y=y + 10, only_one_image=True, image_name='grey', writing_button=True, variable=self.memory_car.name, name='car_name', scale=6)  # Button to edit the name of the car

    def __str__(self):
        """
        Return the string of the rectangle

        Returns:
            str: string of the rectangle
        """
        return f'RectGarage {self.id_rect} : Checked = {self.select_button.activated}, Name = {self.name_button.name}'

    def draw(self, time_since_last_delete):
        """
        Draw the rectangle in the garage menu

        Args:
            time_since_last_delete (int): time since the last deletion of a car to avoid multiple deletions

        Returns:
            (bool, bool): (True if the car is deleted, False otherwise ; True if the select button is clicked, False otherwise)
        """
        # We draw the rectangle itself
        pygame.draw.rect(var.WINDOW, (1, 1, 1), (convert_to_new_window((self.x, self.y, 225,  75))), 2)

        self.draw_rect_color()  # We draw the rectangle of the color
        self.draw_name_button()  # We draw the name button
        self.draw_score()  # We draw the score
        select_car = self.draw_select_button()  # We draw the select button
        self.draw_edit_button()  # We draw the edit button
        delete_car = self.draw_delete_button(time_since_last_delete)  # We draw the delete button

        return delete_car, select_car

    def draw_rect_color(self):
        """
        Draw the rectangle where we can find the color of the car, depending on the mouse state
        """
        # We draw the rects for the color of the car
        rect_color = pygame.rect.Rect(convert_to_new_window((self.x + 154, self.y + 40, 26, 26)))
        pygame.draw.rect(var.WINDOW, CAR_COLORS[self.memory_car.color], rect_color, 0)  # We fill the rectangle with the color of the car

        if rect_color.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            pygame.draw.rect(var.WINDOW, (1, 1, 1), rect_color, 4)
            # We change the color of the car if the user clicked on the color
            if pygame.mouse.get_pressed()[0] and time.time() - self.last_time_color_clicked > 0.3:
                self.last_time_color_clicked = time.time()
                self.memory_car.color = random.choice(list(CAR_COLORS.keys()))  # We change the color of the car randomly
        else:
            pygame.draw.rect(var.WINDOW, (1, 1, 1), rect_color, 2)

    def draw_name_button(self):
        """
        Draw the button to edit the name of the car
        """
        self.name_button.draw(True)
        if self.name_button.just_clicked:
            self.name_button.text = ''  # We reset the name at the beginning

    def draw_score(self):
        """
        Draw the score of the car
        """
        if var.NUM_MAP == 5:  # If it's the map 5 (waiting screen), we divide the score by 100 and cast it to an int
            text = var.SMALL_FONT.render(f'Score : {int(self.memory_car.best_scores[var.NUM_MAP] / 100)}', True, (0, 0, 0))
        else:
            text = var.SMALL_FONT.render(f'Score : {self.memory_car.best_scores[var.NUM_MAP]}', True, (0, 0, 0))
        var.WINDOW.blit(text, convert_to_new_window((self.x + 20, self.y + 45)))

    def draw_select_button(self):
        """
        Draw the button to select a car

        Returns:
            bool: True if the select button is clicked, False otherwise
        """
        self.select_button.draw()
        if self.select_button.just_clicked:
            if self.select_button.activated:  # Button activated
                var.SELECTED_MEMORY_CARS.append(self.memory_car)
                self.selected = True

            else:  # Button deactivated
                for selected_memory_car in var.SELECTED_MEMORY_CARS:
                    if selected_memory_car.id == self.memory_car.id:
                        var.SELECTED_MEMORY_CARS.remove(selected_memory_car)
                        break
                self.selected = False

            return True
        return False

    def draw_edit_button(self):
        """
        Draw the button to edit a car
        """
        if self.edit_button.draw():  # We check the state of the button
            DICE_MENU.init(values=self.memory_car.genetic.get_list(), id_memory_car=self.memory_car.id)  # We initialize the dice data
            var.DISPLAY_DICE_MENU = True  # We display the dice menu

    def draw_delete_button(self, time_since_last_delete):
        """
        Draw the button to delete a car if necessary

        Args:
            time_since_last_delete (int): time since the last deletion of a car to avoid multiple deletions

        Returns:
            bool: True if the car is deleted, False otherwise
        """
        if self.delete_button.draw() and time.time() - time_since_last_delete > 0.2:  # We check the state of the button
            var.MEMORY_CARS.remove(self.memory_car)
            return True

        return False

    def save_new_car_name(self):
        """
        Save the new name of the car when it is changed
        """
        for memory_car in var.MEMORY_CARS:
            if memory_car.id == self.memory_car.id:
                memory_car.name = self.name_button.variable
                break
