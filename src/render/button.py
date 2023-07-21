from src.other.utils import convert_to_new_window  # To convert the position of the button
import src.data.variables as var  # Import the data
import pygame  # To use pygame
import time  # To get the time


"""
This file contains the Button class and all the functions related to it
"""


class Button:
    """
    This class is used to represent a button used in the ui
    """
    def __init__(self, x=None, y=None, image_name=None, only_one_image=False, checkbox=False, writing_button=False, variable=None, name=None, scale=1, scale_x=None, scale_y=None):
        """
        Initialization of a button

        Args:
            x (int): x position of the button
            y (int): y position of the button
            image_name (str): name of the image of the button (int the images folder)
            only_one_image (bool): True if the button has only one image, False otherwise (it means there is three images depending on the state of the button)
            checkbox (bool): True if the button is a checkbox, False otherwise
            writing_button (bool): True if the button is a writing button, False otherwise
            variable (int or str) : variable associated to the text of the writing button
            name (str): name of the button (used to know if there is special actions to do) or the name of the variable
            associated to the text of the writing button (used for the settings)
            scale (float): scale of the button
            scale_x (float): scale of the button on the x-axis
            scale_y (float): scale of the button on the y-axis

        """
        if x is not None:  # If it's a real object we initialize it
            # If the scale is the same for x and y we can use scale instead of scale_x and scale_y
            if scale_x is None:
                scale_x = scale
            if scale_y is None:
                scale_y = scale
            scale_x, scale_y = scale_x * var.SCALE_RESIZE_X, scale_y * var.SCALE_RESIZE_Y  # Scale of the button (converted to the new window)

            self.x, self.y = convert_to_new_window((x, y))  # Position of the button (converted to the new window)

            # In this case we only have one image for the button
            if only_one_image:
                image = pygame.image.load(var.PATH_IMAGE + image_name + '.png')  # Image of the button
                self.image_hover = None
                self.image_clicked = None
            else:  # In this case we have three images for the button
                image = pygame.image.load(var.PATH_IMAGE + image_name + '_1.png')
                image_hover = pygame.image.load(var.PATH_IMAGE + image_name + '_2.png')
                self.image_hover = pygame.transform.scale(image_hover, (int(image_hover.get_width() * scale_x), int(image_hover.get_height() * scale_y)))
                image_clicked = pygame.image.load(var.PATH_IMAGE + image_name + '_3.png')
                self.image_clicked = pygame.transform.scale(image_clicked, (int(image_clicked.get_width() * scale_x), int(image_clicked.get_height() * scale_y)))

            self.image = pygame.transform.scale(image, (int(image.get_width() * scale_x), int(image.get_height() * scale_y)))  # Image of the button
            self.rect = self.image.get_rect()  # Rectangle of the button
            self.rect.topleft = (self.x, self.y)  # Position of the button

            self.activated = False    # True if the checkbox is checked, False otherwise
            self.just_clicked = 0   # 0 if nothing happened ; 1 if the button has just been clicked
            self.time_clicked = 0   # Time when the button is clicked
            self.mouse_over_button = False  # True if the mouse is over the button, False otherwise

            self.checkbox = checkbox  # True if the button is a checkbox, False otherwise
            if image_name == 'checkbox':
                self.checkbox = True

            self.writing_button = writing_button  # True if the button is a writing button, False otherwise
            if image_name == 'writing':
                self.writing_button = True

            self.text = str(variable)  # Text of the button
            self.variable = variable  # Variable of the button

            self.name = name    # Name of the button

    def __str__(self):
        """
        String representation of the button

        Returns:
            str: string representation of the button
        """
        return f'Button : x = {self.x} ; y = {self.y} ; activated = {self.activated} ; just_clicked = {self.just_clicked}' \
               f' ; time_clicked = {self.time_clicked} ; check_box = {self.checkbox} ; writing_button = {self.writing_button}' \
               f' ; text = {self.text} ; variable = {self.variable} ; name = {self.name}'

    def draw(self, debug=False):
        """
        Detect if the mouse is over the button and if it is clicked, and draw the button on the screen with the appropriate image

        Returns:
            bool: True if button activated ; False otherwise
        """

        image = self.image  # Image of the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            self.mouse_over_button = True
            if pygame.mouse.get_pressed()[0] == 1 and time.time() - self.time_clicked > 0.3:    # Mouse clicked for the first time
                self.time_clicked = time.time()  # Get the time when the button is clicked
                if self.checkbox or self.writing_button:
                    self.activated = not self.activated  # Change the state of the checkbox
                else:
                    self.activated = True     # Activate the button
                self.just_clicked = 1

            else:
                self.just_clicked = 0   # The button has not just been clicked
                if not self.checkbox and not self.writing_button:
                    self.activated = False  # Change the state if it's a simple button

            if self.image_hover:
                image = self.image_hover   # Change the image if it's possible
        else:
            self.mouse_over_button = False
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

    def update_after_key_press(self, event):
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

    def update_text(self, parameter):
        """
        Update the parameter of the button (writing button) after we changed the map
        """
        self.variable = parameter
        self.text = str(parameter)

    def deactivate(self):
        """
        Deactivate the button (save the text if necessary)
        """
        self.activated = False
        self.just_clicked = -1
        self.time_clicked = time.time()
        if self.writing_button:
            self.save_text()

    def save_text(self):
        """
        Save the text of the button into the variable
        """
        if self.variable is not None:
            try:
                if self.name == 'dice':  # If it's a dice value we check if it's between 1 and 6
                    self.variable = int(self.text)
                    self.variable = max(1, self.variable)
                    self.variable = min(6, self.variable)

                elif self.name == 'car_name':
                    self.variable = self.text

                elif '.' in self.text:
                    self.variable = float(self.text)
                    if self.variable <= 0:
                        self.variable = 0.1
                else:
                    self.variable = int(self.text)  # Convert the text to an integer
                    if self.variable < 0:
                        self.variable = 30

            except ValueError:
                if self.name == 'dice':
                    self.variable = 1
                else:
                    self.variable = 30

            self.text = str(self.variable)  # Reset the text
