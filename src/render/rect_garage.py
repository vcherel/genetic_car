from src.render.button import Button  # Import the button class
from src.render.dice_menu import DICE_MENU  # Import the dice menu
import src.other.variables as var  # Import the variables
import pygame  # To play the game


image_check_box_1 = pygame.image.load(var.PATH_IMAGE + '/checkbox_1.png')  # Image of the checkbox when it is checked
image_check_box_2 = pygame.image.load(var.PATH_IMAGE + '/checkbox_2.png')  # Image of the checkbox when it is not checked
image_check_box_3 = pygame.image.load(var.PATH_IMAGE + '/checkbox_3.png')  # Image of the checkbox when the mouse is over it

dict_checked = [False] * 10  # List of the checked rect


class RectGarage:
    def __init__(self, id_rect, id_car, pos, name, genetic, type_car):
        """
        Initialization of the rectangle garage
        A Rectangle garage is a rectangle that contains the cars saved in the garage menu

        Args:
            pos (tuple): position of the rectangle
            name (str): name of the rectangle
            id_car (int): id of the car
            genetic (Genetic): genetic of the car
            type_car (str): type of the car ('dice' or 'genetic')
        """
        self.pos = pos  # Position of the rectangle
        self.id_car = id_car  # Id of the car
        self.id_rect = id_rect  # Id of the rectangle
        self.genetic = genetic  # Genetic of the car
        self.type_car = type_car  # Type of the car

        self.change_text = False
        self.name = name  # Name of the rectangle
        self.text = var.FONT.render(self.name, True, (0, 0, 0), (128, 128, 128))


        # Buttons
        self.edit_button = Button(x=pos[0] + 188, y=pos[1] + 40, image=pygame.image.load(var.PATH_IMAGE + '/pen.png'), scale=0.032)  # Button to edit the car
        self.select_button = Button(x=pos[0] + 190, y=pos[1] + 8, image=image_check_box_1, image_hover=image_check_box_2,
                                    image_clicked=image_check_box_3, checkbox=True, scale=0.035)  # Button of the writing rectangle
        self.delete_button = Button(x=pos[0] + 153, y=pos[1] + 4, image=pygame.image.load(var.PATH_IMAGE + '/trash.png'), scale=0.059)  # Button to delete the car
        self.name_button = Button(x=pos[0] + 10, y=pos[1] + 10, image=self.text, checkbox=True)  # Button to edit the name of the car

        if dict_checked[self.id_rect]:  # If the car is checked
            self.select_button.activated = True  # Activate the button

    def draw(self, time_since_last_delete):
        """
        Draw the rectangle in the garage menu

        Returns:
            bool: True if the car is deleted, False otherwise
        """
        # We draw the rectangle
        pygame.draw.rect(var.WINDOW, (0, 0, 0), (self.pos[0], self.pos[1], 225, 75), 2)
        # We write the name of the save
        self.change_text = self.name_button.check_state()

        # We add the buttons
        if self.select_button.check_state():
            dict_checked[self.id_rect] = True  # We take in memory the state of the button
            var.GENETICS_FROM_GARAGE.append(self.genetic)
        else:
            dict_checked[self.id_rect] = False  # We take in memory the state of the button
            if self.genetic in var.GENETICS_FROM_GARAGE:
                var.GENETICS_FROM_GARAGE.remove(self.genetic)

        if self.edit_button is not None and self.edit_button.check_state():  # We check the state of the button
            DICE_MENU.init(self.type_car, self.id_car, genetic=self.genetic)  # We initialize the dice variables
            var.DISPLAY_DICE_MENU = True  # We display the dice menu

        if self.delete_button.check_state() and pygame.time.get_ticks() - time_since_last_delete > 200:  # We check the state of the button
            for item in var.MEMORY_CARS.get(self.type_car):
                if item[0] == self.id_car and item[1] == self.name and item[2] == self.genetic:
                    var.MEMORY_CARS.get(self.type_car).remove(item)
                    return True

        return False
