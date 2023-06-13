import time  # To get the time
import pygame  # To play the game
import variables as var  # Import the variables
from button import Button  # Import the button class
from dice_menu import init_dice_variables, display_dice_menu  # Import the function to use the dice menu


image_check_box_1 = pygame.image.load("images/checkbox_1.png")  # Image of the checkbox when it is checked
image_check_box_2 = pygame.image.load("images/checkbox_2.png")  # Image of the checkbox when it is not checked
image_check_box_3 = pygame.image.load("images/checkbox_3.png")  # Image of the checkbox when the mouse is over it

dict_checked = [False] * 10  # List of the checked cars


class RectGarage:
    def __init__(self, pos, name, num, genetic, type_car):
        """
        Initialization of the rectangle garage
        A Rectangle garage is a rectangle that contains the cars saved in the garage menu

        Args:
            pos (tuple): position of the rectangle
            name (str): name of the rectangle
            num (int): id of the car
            genetic (Genetic): genetic of the car
            type_car (str): type of the car ('dice' or 'genetic')
        """
        self.pos = pos  # Position of the rectangle
        self.name = name  # Name of the rectangle
        self.id = num  # Id of the car
        self.genetic = genetic  # Genetic of the car
        self.type_car = type_car  # Type of the car

        # Buttons
        self.edit_button = Button(x=pos[0] + 188, y=pos[1] + 40, image=pygame.image.load("images/pen.png"), scale=0.032)  # Button to edit the car
        self.select_button = Button(x=pos[0] + 190, y=pos[1] + 8, image=image_check_box_1, image_hover=image_check_box_2,
                                    image_clicked=image_check_box_3, check_box=True, scale=0.035)  # Button of the writing rectangle
        self.delete_button = Button(x=pos[0] + 153, y=pos[1] + 4, image=pygame.image.load("images/trash.png"), scale=0.059)  # Button to delete the car

        if dict_checked[self.id]:  # If the car is checked
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
        var.WINDOW.blit(var.FONT.render(self.name, True, (0, 0, 0), (128, 128, 128)), (self.pos[0] + 10, self.pos[1] + 10))

        # We add the buttons
        if self.select_button.check_state():
            dict_checked[self.id] = True  # We take in memory the state of the button
            var.GENETICS_FROM_GARAGE.append(self.genetic)
        else:
            dict_checked[self.id] = False  # We take in memory the state of the button
            if self.genetic in var.GENETICS_FROM_GARAGE:
                var.GENETICS_FROM_GARAGE.remove(self.genetic)

        if self.edit_button is not None and self.edit_button.check_state():  # We check the state of the button
            var.DICE_RECT_GARAGE = self  # We don't display the dice from camera but from the garage
            init_dice_variables(self.genetic)  # We initialize the dice variables
            var.DISPLAY_DICE_MENU = True  # We display the dice menu

        if self.delete_button.check_state() and pygame.time.get_ticks() - time_since_last_delete > 500:  # We check the state of the button
            for item in var.MEMORY_CARS.get(self.type_car):
                if item[1] == self.genetic:
                    var.MEMORY_CARS.get(self.type_car).remove(item)
                    return True

        return False
