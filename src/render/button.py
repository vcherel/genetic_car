from src.other.utils import convert_to_new_window  # To convert the position of the button
import src.other.variables as var  # Import the variables
import os.path  # To get the path of the file
import pygame  # To use pygame

"""
This file contains the Button class and all the functions related to it
"""


class Button:
    def __init__(self, x=None, y=None, image=None, image_hover=None, image_clicked=None, checkbox=False, writing_button=False, text=None, variable=None, name=None, scale=1, scale_x=None, scale_y=None):
        """
        Initialization of a button

        Args:
            x (int): x position of the button
            y (int): y position of the button
            image (pygame.Surface): image of the button
            image_hover (pygame.Surface): image of the button when the mouse is over it
            image_clicked (pygame.Surface): image of the button when it is clicked
            checkbox (bool): True if the button is a checkbox, False otherwise
            writing_button (bool): True if the button is a writing button, False otherwise
            text (str): text of the writing button
            variable (int) : variable associated to the text of the writing button
            name (str): name of the button (used to know if there is special actions to do)
            scale (float): scale of the button
            scale_x (float): scale of the button on the x-axis
            scale_y (float): scale of the button on the y-axis

        """
        if x is not None:  # If it's a real object

            # If the scale is the same for x and y we can use scale instead of scale_x and scale_y
            if scale_x is None:
                scale_x = scale
            if scale_y is None:
                scale_y = scale
            scale_x, scale_y = scale_x * var.SCALE_RESIZE_X, scale_y * var.SCALE_RESIZE_Y  # Scale of the button (converted to the new window)

            self.x, self.y = convert_to_new_window((x, y))  # Position of the button (converted to the new window)

            self.image = pygame.transform.scale(image, (int(image.get_width() * scale_x), int(image.get_height() * scale_y)))  # Image of the button
            if image_hover is not None:
                self.image_hover = pygame.transform.scale(image_hover, (int(image_hover.get_width() * scale_x), int(image_hover.get_height() * scale_y)))
            else:
                self.image_hover = None  # Image of the button when the mouse is over it
            if image_clicked is not None:
                self.image_clicked = pygame.transform.scale(image_clicked, (int(image_clicked.get_width() * scale_x), int(image_clicked.get_height() * scale_y)))
            else:
                self.image_clicked = None  # Image of the button when it is clicked

            self.rect = self.image.get_rect()  # Rectangle of the button
            self.rect.topleft = (self.x, self.y)  # Position of the button
            self.checkbox = checkbox   # True if the button is a checkbox, False otherwise
            self.activated = False    # True if the checkbox is checked, False otherwise
            self.just_clicked = 0   # 0 if nothing happened ; 1 if the button has just been activated ; -1 if the button has just been deactivated
            self.time_clicked = 0   # Time when the button is clicked


            self.writing_button = writing_button  # True if the button is a writing button, False otherwise
            self.text = text  # Text of the button
            self.variable = variable  # Variable of the button
            self.name = name    # Name of the button

    def __str__(self):
        """
        String representation of the button

        Returns:
            str: string representation of the button
        """
        return f'Button : x = {self.x} ; y = {self.y} ; activated = {self.activated} ; just_clicked = {self.just_clicked} ; time_clicked = {self.time_clicked} ; check_box = {self.checkbox} ; writing_button = {self.writing_button} ; text = {self.text} ; variable = {self.variable} ; name = {self.name}'

    def draw(self):
        """
        Detect if the mouse is over the button and if it is clicked, and draw the button on the screen with the appropriate image

        Returns:
            bool: True if button activated ; False otherwise
        """
        image = self.image  # Image of the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            if pygame.mouse.get_pressed()[0] == 1 and pygame.time.get_ticks() - self.time_clicked > 300:    # Mouse clicked for the first time
                self.time_clicked = pygame.time.get_ticks()  # Get the time when the button is clicked
                if self.checkbox or self.writing_button:
                    self.activated = not self.activated  # Change the state of the checkbox
                else:
                    self.activated = True     # Activate the button
                if self.activated:
                    self.just_clicked = 1
                else:
                    self.just_clicked = -1

            else:
                self.just_clicked = 0   # The button has not just been clicked
                if not self.checkbox and not self.writing_button:
                    self.activated = False  # Change the state if it's a simple button

            if self.image_hover:
                image = self.image_hover   # Change the image if it's possible
        else:
            self.just_clicked = 0   # The button has not just been clicked
            if not self.checkbox and not self.writing_button:
                self.activated = False  # Change the state if it's a simple button

        if self.activated and self.image_clicked:
            image = self.image_clicked  # Change the image if it's possible

        # Draw button on screen
        var.WINDOW.blit(image, (self.rect.x, self.rect.y))

        # Draw text on button if it's a writing button
        if self.writing_button:
            var.WINDOW.blit(var.FONT.render(self.text, True, (0, 0, 0)), (self.rect.x + 10, self.rect.y + 4))

        return self.activated  # Return True if the button is clicked (or activated), False otherwise

    def update(self, event):
        """
        Update the button

        Args:
            event (pygame.event.Event): event detected (keyboard)

        Returns:
            bool: True if the button is deactivated ; False otherwise
        """
        if event.key == pygame.K_RETURN:
            self.deactivate()   # Deactivate the writing button (and save the text)
            return True

        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]  # Remove the last character

        elif self.variable is None and event.unicode == ' ':  # If the variable is a string we don't want space
            self.text += '_'

        else:
            self.text += event.unicode

        return False

    def deactivate(self):
        self.activated = False
        self.just_clicked = -1
        self.time_clicked = pygame.time.get_ticks()
        if self.writing_button:
            self.save()

    def save(self):
        if self.variable is not None:
            try:
                # We detect if there is a decimal point
                if '.' in self.text:
                    self.variable = float(self.text)
                else:
                    self.variable = int(self.text)  # Convert the text to an integer

                if self.name == 'dice':  # If it's a dice value we check if it's between 1 and 6
                    self.variable = max(1, self.variable)
                    self.variable = min(6, self.variable)
                else:
                    if self.variable < 0:
                        self.variable = 0

                # If it's the number of cars we change the variable in the file parameters
                if self.name == 'nb_cars':
                    with open(os.path.dirname(__file__) + "/../../data/parameters", "w") as file_parameters_write:
                        file_parameters_write.write(str(var.NUM_MAP) + "\n" + str(self.variable))

            except ValueError:
                if self.name == 'dice':
                    self.variable = 1
                else:
                    self.variable = 50

            self.text = str(self.variable)  # Reset the text
