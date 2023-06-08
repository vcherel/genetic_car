import pygame  # Import pygame to load the image of the button
import variables  # Import the variables
from button import Button  # Import the button class
from constants import WINDOW, FONT  # Import the constants

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
        else:
            self.genetic = genetic  # Genetic of the car

        self.button = Button(x=pos[0] + 190, y=pos[1] + 8, image=image_check_box_1, image_hover=image_check_box_2,
                             image_clicked=image_check_box_3, check_box=True, scale=0.035)  # Button of the rectangle
        if dict_checked[self.id]:  # If the car is checked
            self.button.activated = True  # Activate the button

    def draw(self):
        """
        Draw the rectangle in the garage menu
        """
        # We draw the rectangle
        pygame.draw.rect(WINDOW, (0, 0, 0), (self.pos[0], self.pos[1], 225, 75), 2)
        # We write the name of the save
        WINDOW.blit(FONT.render(self.name, True, (0, 0, 0), (128, 128, 128)),
                    (self.pos[0] + 10, self.pos[1] + 10))

        # We add the button
        if self.button.check_state():
            dict_checked[self.id] = True  # We take in memory the state of the button
            if type(self.genetic) is list:
                for genetic in self.genetic:
                    variables.GENETICS_FROM_GARAGE.append(genetic)
            else:
                variables.GENETICS_FROM_GARAGE.append(self.genetic)
        else:
            dict_checked[self.id] = False  # We take in memory the state of the button