import pygame  # To play the game
import variables as var  # Import the variables
from button import Button  # Import the button class
from dice_menu import init_dice_variables, display_dice_menu  # Import the function to use the dice menu


image_check_box_1 = pygame.image.load("images/checkbox_1.png")  # Image of the checkbox when it is checked
image_check_box_2 = pygame.image.load("images/checkbox_2.png")  # Image of the checkbox when it is not checked
image_check_box_3 = pygame.image.load("images/checkbox_3.png")  # Image of the checkbox when the mouse is over it

dict_checked = [False] * 10  # List of the checked cars


class RectGarage:
    def __init__(self, pos, name, num, genetic):
        """
        Initialization of the rectangle garage
        A Rectangle garage is a rectangle that contains the cars saved in the garage menu

        Args:
            pos (tuple): position of the rectangle
            name (str): name of the rectangle
            num (int): id of the car
            genetic(tuple(int, Genetic) or list tuple(int, Genetic)): genetic of the car (can be a list)
        """
        self.pos = pos  # Position of the rectangle
        self.name = name  # Name of the rectangle
        self.id = num  # Id of the car

        if type(genetic) is list:  # If it's a list of genetic
            self.genetic = []
            for gen in genetic:
                self.genetic.append(gen[1])  # We only keep the genetic (gen[0] is the id)

            self.edit_button = None  # We don't need the edit button
        else:
            self.genetic = genetic  # Genetic of the car
            self.edit_button = Button(x=pos[0] + 188, y=pos[1] + 40, image=pygame.image.load("images/pen.png"), scale=0.032)  # Button to edit the car

        self.select_button = Button(x=pos[0] + 190, y=pos[1] + 8, image=image_check_box_1, image_hover=image_check_box_2,
                                    image_clicked=image_check_box_3, check_box=True, scale=0.035)  # Button of the writing rectangle

        self.delete_button = Button(x=pos[0] + 153, y=pos[1] + 4, image=pygame.image.load("images/trash.png"), scale=0.059)  # Button to delete the car

        if dict_checked[self.id]:  # If the car is checked
            self.select_button.activated = True  # Activate the button

    def draw(self):
        """
        Draw the rectangle in the garage menu
        """
        # We draw the rectangle
        pygame.draw.rect(var.WINDOW, (0, 0, 0), (self.pos[0], self.pos[1], 225, 75), 2)
        # We write the name of the save
        var.WINDOW.blit(var.FONT.render(self.name, True, (0, 0, 0), (128, 128, 128)), (self.pos[0] + 10, self.pos[1] + 10))

        # We add the buttons
        if self.select_button.check_state():
            dict_checked[self.id] = True  # We take in memory the state of the button
            if type(self.genetic) is list:
                for genetic in self.genetic:
                    var.GENETICS_FROM_GARAGE.append(genetic)
            else:
                var.GENETICS_FROM_GARAGE.append(self.genetic)
        else:
            dict_checked[self.id] = False  # We take in memory the state of the button

        if self.edit_button is not None and self.edit_button.check_state():  # We check the state of the button
            var.DICE_RECT_GARAGE = self  # We don't display the dice from camera but from the garage
            init_dice_variables(self.genetic)  # We initialize the dice variables
            var.DISPLAY_DICE_MENU = True  # We display the dice menu

        if self.delete_button.check_state():
            print("J'ai pas encore ajouté ça...")
