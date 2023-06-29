from src.render.button import Button  # Import the button class
from src.render.dice_menu import DICE_MENU  # Import the dice menu
import src.other.variables as var  # Import the variables
import pygame  # To play the game


"""
This file contains the RectGarage class and all the functions related to it. A rectangle garage is a rectangle that contains the cars saved in the garage menu.
"""


image_check_box_1 = pygame.image.load(var.PATH_IMAGE + '/checkbox_1.png')  # Image of the checkbox when it is checked
image_check_box_2 = pygame.image.load(var.PATH_IMAGE + '/checkbox_2.png')  # Image of the checkbox when it is not checked
image_check_box_3 = pygame.image.load(var.PATH_IMAGE + '/checkbox_3.png')  # Image of the checkbox when the mouse is over it

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

        self.change_text = False  # Boolean to know if we change the text of the writing button
        self.name = name  # Name of the rectangle
        self.text = var.FONT.render(self.name, True, (0, 0, 0), (128, 128, 128))

        # Buttons
        self.edit_button = Button(x=pos[0] + 188, y=pos[1] + 40, image=pygame.image.load(var.PATH_IMAGE + '/pen.png'), scale=0.032)  # Button to edit the car
        self.select_button = Button(x=pos[0] + 190, y=pos[1] + 8, image=image_check_box_1, image_hover=image_check_box_2,
                                    image_clicked=image_check_box_3, checkbox=True, scale=0.035)  # Button of the writing button
        self.delete_button = Button(x=pos[0] + 153, y=pos[1] + 4, image=pygame.image.load(var.PATH_IMAGE + '/trash.png'), scale=0.059)  # Button to delete the car
        self.name_button = Button(x=pos[0] + 10, y=pos[1] + 10, image=self.text, writing_button=True)  # Button to edit the name of the car

        if dict_check[self.id_rect]:
            self.select_button.activated = True
            var.GENETICS_FROM_GARAGE.append(self.genetic)

    def __str__(self):
        """
        Return the string of the rectangle

        Returns:
            str: string of the rectangle
        """
        return f'RectGarage {self.id_rect} : Checked = {self.select_button.activated}, Name = {self.name}'

    def draw_rect_garage(self, time_since_last_delete=0):
        """
        Draw the rectangle in the garage menu

        Args:
            time_since_last_delete (int): time since the last deletion of a car to avoid multiple deletions

        Returns:
            bool: True if the car is deleted, False otherwise
        """
        # We draw the rectangle
        pygame.draw.rect(var.WINDOW, (0, 0, 0), (self.pos[0], self.pos[1], 225, 75), 2)

        self.change_text = self.name_button.check_state()

        if self.name_button.just_clicked and self.change_text:
            self.name = ''  # We reset the name at the beginning
            self.text = var.FONT.render(self.name, True, (0, 0, 0), (128, 128, 128))  # We change the text of the writing button
            self.name_button.image = self.text  # We change the image of the writing button

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
            DICE_MENU.init(self.type_car, self.id_car, genetic=self.genetic)  # We initialize the dice variables
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
        if self.name == '':
            self.name = f'Voiture_{self.id_car}'

        # We change the value of the car in the memory
        var.update_car_name(self.type_car, self.id_car, self.name)

        self.name_button.activated = False  # We stop changing the name of the car
        self.text = var.FONT.render(self.name, True, (0, 0, 0), (128, 128, 128))  # We change the text of the writing button
        self.name_button.image = self.text  # We change the image of the writing button
        self.draw_rect_garage()  # We display the rectangle with the new text


def reset_dict_check():
    """
    Reset the state of the checkbox
    """
    global dict_check
    dict_check = [False] * 10