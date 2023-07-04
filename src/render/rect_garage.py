from src.other.utils import convert_to_new_window  # To convert positions when resizing the window
from src.render.dice_menu import DICE_MENU  # Import the dice menu
from src.render.button import Button  # Import the button class
import src.other.variables as var  # Import the variables
import pygame  # To play the game


"""
This file contains the RectGarage class and all the functions related to it. A rectangle garage is a rectangle that contains the cars saved in the garage menu.
"""

dict_check = [False] * 10  # List of the state of the checkbox


class RectGarage:
    def __init__(self, id_car, type_car, name, genetic, id_rect, pos):
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
        self.genetic = genetic  # Genetic of the car
        self.type_car = type_car  # Type of the car

        # Buttons
        self.edit_button = Button(pos[0] + 188, pos[1] + 40, pygame.image.load(var.PATH_IMAGE + '/pen.png'), scale=0.032)  # Button to edit the car
        self.select_button = Button(pos[0] + 188, pos[1] + 8, pygame.image.load(var.PATH_IMAGE + '/checkbox_1.png'),
                                    pygame.image.load(var.PATH_IMAGE + '/checkbox_2.png'),
                                    pygame.image.load(var.PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.07)  # Button of the writing button
        self.delete_button = Button(pos[0] + 153, pos[1] + 5, pygame.image.load(var.PATH_IMAGE + '/trash_button_1.png'),
                                    pygame.image.load(var.PATH_IMAGE + '/trash_button_2.png'),
                                    pygame.image.load(var.PATH_IMAGE + '/trash_button_3.png'),
                                    scale=0.14)  # Button to delete the car
        self.name_button = Button(pos[0] + 10, pos[1] + 10, pygame.image.load(var.PATH_IMAGE + '/grey.png'), writing_button=True, text=name, scale=6)  # Button to edit the name of the car

        if dict_check[self.id_rect]:
            self.select_button.activated = True
            var.GENETICS_FROM_GARAGE.append(self.genetic)

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
        # We draw the rectangle
        new_pos = convert_to_new_window(self.pos)
        pygame.draw.rect(var.WINDOW, (0, 0, 0), (new_pos[0], new_pos[1], var.SCALE_RESIZE_X * 225,  var.SCALE_RESIZE_Y * 75), 2)

        self.name_button.check_state()
        if self.name_button.just_clicked:
            self.name_button.text = ''  # We reset the name at the beginning

        # Button to select a car
        if self.select_button.check_state():
            if not dict_check[self.id_rect]:
                dict_check[self.id_rect] = True
                var.GENETICS_FROM_GARAGE.append(self.genetic)
        else:
            if dict_check[self.id_rect]:
                dict_check[self.id_rect] = False
                var.GENETICS_FROM_GARAGE.remove(self.genetic)

        # Button to edit a car
        if self.edit_button is not None and self.edit_button.check_state():  # We check the state of the button
            DICE_MENU.init(self.type_car, self.genetic.get_list(), self.id_car)  # We initialize the dice variables
            var.DISPLAY_DICE_MENU = True  # We display the dice menu

        # Button to delete a car
        if self.delete_button.check_state() and pygame.time.get_ticks() - time_since_last_delete > 200:  # We check the state of the button

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


    def save(self):
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
