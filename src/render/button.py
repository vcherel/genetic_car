import src.other.variables as var  # Import the variables
import os.path  # To get the path of the file
import pygame  # To use pygame


class Button:
    def __init__(self, x=None, y=None, image=None, image_hover=None, image_clicked=None, checkbox=False, scale=1):
        """
        Initialization of a button

        Args:
            x (int): x position of the button
            y (int): y position of the button
            image (pygame.Surface): image of the button
            scale (float): scale of the button
            image_hover (pygame.Surface): image of the button when the mouse is over it
            image_clicked (pygame.Surface): image of the button when it is clicked
            checkbox (bool): True if the button is a checkbox, False otherwise
        """
        if x is not None:  # If it's a real object
            self.x = x  # x position of the button
            self.y = y  # y position of the button
            self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))  # Image of the button
            self.rect = self.image.get_rect()  # Rectangle of the button
            self.rect.topleft = (x, y)  # Position of the button
            self.checkbox = checkbox   # True if the button is a checkbox, False otherwise
            self.activated = False    # True if the checkbox is checked, False otherwise
            self.just_clicked = 0   # 0 if nothing happened ; 1 if the button has just been activated ; -1 if the button has just been deactivated
            self.time_clicked = 0   # Time when the button is clicked

            if image_hover is not None:
                self.image_hover = pygame.transform.scale(image_hover, (int(image_hover.get_width() * scale), int(image_hover.get_height() * scale)))
            else:
                self.image_hover = None  # Image of the button when the mouse is over it
            if image_clicked is not None:
                self.image_clicked = pygame.transform.scale(image_clicked, (int(image_clicked.get_width() * scale), int(image_clicked.get_height() * scale)))
            else:
                self.image_clicked = None  # Image of the button when it is clicked

    def __str__(self):
        """
        String representation of the button

        Returns:
            str: string representation of the button
        """
        return "Button : x = " + str(self.x) + " ; y = " + str(self.y) + " ; activated = " + str(self.activated) + \
            " ; just_clicked = " + str(self.just_clicked) + " ; time_clicked = " + str(self.time_clicked) +\
            " ; check_box = " + str(self.checkbox)

    def check_state(self):
        """
        Detect if the mouse is over the button and if it is clicked, and draw the button on the screen with the appropriate image

        Returns:
            bool: True if button activated ; False otherwise
        """
        image = self.image  # Image of the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            if pygame.mouse.get_pressed()[0] == 1 and pygame.time.get_ticks() - self.time_clicked > 300:    # Mouse clicked for the first time
                self.time_clicked = pygame.time.get_ticks()  # Get the time when the button is clicked
                if self.checkbox:
                    self.activated = not self.activated  # Change the state of the checkbox
                else:
                    self.activated = True     # Activate the button
                if self.activated:
                    self.just_clicked = 1
                else:
                    self.just_clicked = -1

            else:
                self.just_clicked = 0   # The button has not just been clicked
                if not self.checkbox:
                    self.activated = False  # Change the state if it's a simple button

            if self.image_hover:
                image = self.image_hover   # Change the image if it's possible
        else:
            self.just_clicked = 0   # The button has not just been clicked

        if self.activated and self.image_clicked:
            image = self.image_clicked  # Change the image if it's possible

        # Draw button on screen
        var.WINDOW.blit(image, (self.rect.x, self.rect.y))

        return self.activated  # Return True if the button is clicked (or activated), False otherwise

    def update_writing_rectangle(self, event, variable, str_variable, text, dice_value=False, nb_cars=False, int_variable=True):
        """
        Save the text in the writing rectangle

        Args:
            event (pygame.event.Event): event detected (keyboard)
            variable (int): value of the int in the text
            str_variable (str): text in the writing rectangle
            text (pygame.Surface): text to display
            dice_value (bool): True if the writing rectangle is limited (for dice_values) false otherwise
            nb_cars (bool): True if the writing rectangle is for nb_cars, false otherwise (to save the value in the file parameters)
            int_variable (bool): True if the variable is an int, False otherwise

        Returns:
            int: value of the int in the text
            str: text in the writing rectangle
            bool: True if the writing rectangle is active, False otherwise
            pygame.Surface: text to display
        """
        bool_active = True  # True if the writing rectangle is active, False otherwise

        if event.key == pygame.K_RETURN:
            variable, str_variable, text = self.save_writing_rectangle(str_variable, text, dice_value=dice_value, nb_cars=nb_cars, int_variable=int_variable)
            bool_active = False  # Deactivate the writing rectangle

        elif event.key == pygame.K_BACKSPACE:
            # Remove the last character
            str_variable = str_variable[:-1]
            var.WINDOW.blit(var.BACKGROUND, (text.get_rect().x, text.get_rect().y))
        else:
            # Append the entered character to the text
            str_variable += event.unicode

        return variable, str_variable, bool_active, text


    def save_writing_rectangle(self, str_variable, text, dice_value=False, nb_cars=False, int_variable=True):
        """
        Save the text in the writing rectangle

        Args:
            str_variable (str): text in the writing rectangle
            text (pygame.Surface): text to display
            dice_value (bool): True if the writing rectangle is limited (for dice_values) false otherwise
            nb_cars (bool): True if the writing rectangle is for nb_cars, false otherwise (to save the value in the file parameters)
            int_variable (bool): True if the variable is an integer, False otherwise

        Returns:
            int: variable corresponding to the text
            str: text in the writing rectangle
            pygame.Surface: text to display
        """
        if int_variable:
            try:
                variable = int(str_variable)  # Convert the text to an integer

                if dice_value:  # If it's a dice value we check if it's between 1 and 6
                    variable = max(1, variable)
                    variable = min(6, variable)
                else:  # If it's the number of cars we change the variable in the file parameters
                    if variable < 0:
                        variable = 0

                if nb_cars:
                    with open(os.path.dirname(__file__) + "/../../data/parameters", "w") as file_parameters_write:
                        file_parameters_write.write(str(var.NUM_MAP) + "\n" + str(variable))

            except ValueError:
                print("Erreur sur la valeur rentrée")
                variable = 1

            str_variable = str(variable)  # Reset the text
        else:
            variable = None

        self.activated = False  # Uncheck the button
        var.WINDOW.blit(var.BACKGROUND, (text.get_rect().x, text.get_rect().y))  # Erase the text
        text = var.FONT.render(str_variable, True, (0, 0, 0), (255, 255, 255))  # Change the text one last time
        return variable, str_variable, text
