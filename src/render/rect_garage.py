from src.other.utils import convert_to_new_window  # To convert positions when resizing the window
from src.data.constants import PATH_IMAGE, CAR_COLORS  # Import the constants
from src.render.dice_menu import DICE_MENU  # Import the dice menu
from src.render.button import Button  # Import the button class
import src.data.variables as var  # Import the data
from src.game.car import Car  # Import the car class
import random  # To get random numbers
import pygame  # To play the game
import time  # To get the time


"""
This file contains the RectGarage class and all the functions related to it. A rectangle garage is a rectangle that contains the cars saved in the garage menu.
"""

dict_check = [False] * 10  # List of the state of the checkbox


class RectGarage:
    """
    This class is used to represent a slot for a car in the garage menu
    """
    def __init__(self, id_car, type_car, name, genetic, id_rect, pos, color, scores):
        """
        Initialization of the rectangle garage
        A Rectangle garage is a rectangle that contains the cars saved in the garage menu

        Args:
            id_car (int): id of the car
            type_car (str): type of the car ('dice' or 'genetic')
            name (str): name of the rectangle
            genetic (Genetic): genetic of the car
            id_rect (int): id of the rectangle
            pos (tuple): position of the rectangle
        """
        self.pos = pos  # Position of the rectangle
        self.id_car = id_car  # Id of the car
        self.id_rect = id_rect  # Id of the rectangle
        self.type_car = type_car  # Type of the car
        self.car = Car(genetic, scores, color, view_only=True)  # Car of the rectangle

        self.last_time_color_clicked = 0  # Last time the color was clicked

        # Buttons
        self.edit_button = Button(pos[0] + 188, pos[1] + 40, pygame.image.load(PATH_IMAGE + '/pen_1.png'),
                                  pygame.image.load(PATH_IMAGE + '/pen_2.png'), scale=0.15)  # Button to edit the car
        self.select_button = Button(pos[0] + 188, pos[1] + 8, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                    pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                    pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.07)  # Button of the writing button
        self.delete_button = Button(pos[0] + 153, pos[1] + 5, pygame.image.load(PATH_IMAGE + '/trash_button_1.png'),
                                    pygame.image.load(PATH_IMAGE + '/trash_button_2.png'),
                                    pygame.image.load(PATH_IMAGE + '/trash_button_3.png'),
                                    scale=0.14)  # Button to delete the car
        self.name_button = Button(pos[0] + 10, pos[1] + 10, pygame.image.load(PATH_IMAGE + '/grey.png'), writing_button=True, text=name, scale=6)  # Button to edit the name of the car

        if dict_check[self.id_rect]:
            self.select_button.activated = True
            var.CARS_FROM_GARAGE.append(self.car)

    def __str__(self):
        """
        Return the string of the rectangle

        Returns:
            str: string of the rectangle
        """
        return f'RectGarage {self.id_rect} : Checked = {self.select_button.activated}, Name = {self.name_button.name}'

    def draw_rect_garage(self, time_since_last_delete=0):
        """
        Draw the rectangle in the garage menu

        Args:
            time_since_last_delete (int): time since the last deletion of a car to avoid multiple deletions

        Returns:
            bool: True if the car is deleted, False otherwise
        """
        # We draw the rectangle for the car
        new_pos = convert_to_new_window(self.pos)
        pygame.draw.rect(var.WINDOW, (1, 1, 1), (new_pos[0], new_pos[1], var.SCALE_RESIZE_X * 225,  var.SCALE_RESIZE_Y * 75), 2)

        # We draw the rects for the color of the car
        pos_color = convert_to_new_window((self.pos[0] + 154, self.pos[1] + 40))
        rect_color = pygame.rect.Rect(pos_color[0], pos_color[1], var.SCALE_RESIZE_X * 26, var.SCALE_RESIZE_Y * 26)
        pygame.draw.rect(var.WINDOW, CAR_COLORS[self.car.color], rect_color, 0)

        if rect_color.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            pygame.draw.rect(var.WINDOW, (1, 1, 1), rect_color, 4)
            # We change the color of the car if the user clicked on the color
            if pygame.mouse.get_pressed()[0] and time.time() - self.last_time_color_clicked > 0.2:
                self.last_time_color_clicked = time.time()
                self.car.change_color(random.choice(list(CAR_COLORS.keys())))  # We change the color of the car randomly
                var.update_car_color(self.type_car, self.id_car, self.car.color)  # We update the color of the car in the file
        else:
            pygame.draw.rect(var.WINDOW, (1, 1, 1), rect_color, 2)

        # Button with the name of the car
        self.name_button.draw()
        if self.name_button.just_clicked:
            self.name_button.text = ''  # We reset the name at the beginning

        # Text for the score of the car
        if var.NUM_MAP == 5:   # If it's the map 5 (waiting screen), we divide the score by 100 and cast it to an int
            text = var.SMALL_FONT.render(f'Score : {int(self.car.best_scores[var.NUM_MAP] / 100)}', True, (0, 0, 0))
        else:
            text = var.SMALL_FONT.render(f'Score : {self.car.best_scores[var.NUM_MAP]}', True, (0, 0, 0))
        var.WINDOW.blit(text, (new_pos[0] + 20, new_pos[1] + 45))

        # Button to select a car
        if self.select_button.draw():
            if not dict_check[self.id_rect]:
                dict_check[self.id_rect] = True
                var.CARS_FROM_GARAGE.append(self.car)
        else:
            if dict_check[self.id_rect]:
                dict_check[self.id_rect] = False
                var.CARS_FROM_GARAGE.remove(self.car)

        # Button to edit a car
        if self.edit_button is not None and self.edit_button.draw():  # We check the state of the button
            DICE_MENU.init(self.type_car, self.car.genetic.get_list(), self.id_car)  # We initialize the dice data
            var.DISPLAY_DICE_MENU = True  # We display the dice menu

        # Button to delete a car
        if self.delete_button.draw() and pygame.time.get_ticks() - time_since_last_delete > 200:  # We check the state of the button

            # We change the state of the checkbox
            if self.id_rect == 9:
                dict_check[self.id_rect] = False
            else:
                for i in range(self.id_rect, 9):
                    dict_check[i] = dict_check[i + 1]

            for item in var.MEMORY_CARS.get(self.type_car):
                if item[0] == self.id_car:
                    var.MEMORY_CARS.get(self.type_car).remove(item)
                    return True

        return False


    def save_new_car_name(self):
        """
        Save the car in the memory (when the user has finished editing the name of the car)
        """
        if self.name_button.text == '':
            self.name_button.text = f'Voiture_{self.id_car}'

        # We change the value of the car in the memory
        var.update_car_name(self.type_car, self.id_car, self.name_button.text)

        self.name_button.activated = False  # We stop changing the name of the car
        self.draw_rect_garage()  # We display the rectangle with the new text


def reset_dict_check():
    """
    Reset the state of the checkbox
    """
    global dict_check
    dict_check = [False] * 10
