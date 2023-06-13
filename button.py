import pygame  # To use pygame
import variables as var  # Import the variables


class Button:
    def __init__(self, x=None, y=None, image=None, image_hover=None, image_clicked=None, check_box=False, writing_rectangle=False, scale=None):
        """
        Initialization of a button

        Args:
            x (int): x position of the button
            y (int): y position of the button
            image (pygame.Surface): image of the button
            scale (float): scale of the button
            image_hover (pygame.Surface): image of the button when the mouse is over it
            image_clicked (pygame.Surface): image of the button when it is clicked
            check_box (bool): True if the button is a checkbox, False otherwise
        """
        if x is not None:  # If it's a real object
            self.x = x  # x position of the button
            self.y = y  # y position of the button
            self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))  # Image of the button
            self.rect = self.image.get_rect()  # Rectangle of the button
            self.rect.topleft = (x, y)  # Position of the button
            self.check_box = check_box   # True if the button is a checkbox, False otherwise
            self.writing_rectangle = writing_rectangle   # True if the button is a writing rectangle, False otherwise
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
            " ; check_box = " + str(self.check_box) + " ; writing_rectangle = " + str(self.writing_rectangle)

    def check_state(self):
        """
        Detect if the mouse is over the button and if it is clicked, and draw the button on the screen with the appropriate image

        Returns:
            bool: True if button activated ; False otherwise
        """
        image = self.image  # Image of the button
        if self.rect.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            if pygame.mouse.get_pressed()[0] == 1 and pygame.time.get_ticks() - self.time_clicked > 150:    # Mouse clicked for the first time
                self.time_clicked = pygame.time.get_ticks()  # Get the time when the button is clicked
                if self.check_box or self.writing_rectangle:
                    self.activated = not self.activated  # Change the state of the checkbox
                else:
                    self.activated = True     # Activate the button
                if self.activated:
                    self.just_clicked = 1
                else:
                    self.just_clicked = -1

            else:
                self.just_clicked = 0   # The button has not just been clicked
                if not self.check_box and not self.writing_rectangle:
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

    def update_writing_rectangle(self, event, variable, str_variable, text, nb_cars=False):
        """
        Save the text in the writing rectangle
        """
        bool_active = True  # True if the writing rectangle is active, False otherwise

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                variable, str_variable, text = self.save_writing_rectangle(str_variable, text, nb_cars)
                bool_active = False  # Deactivate the writing rectangle

            elif event.key == pygame.K_BACKSPACE:
                # Remove the last character
                str_variable = str_variable[:-1]
                var.WINDOW.blit(var.BACKGROUND, (text.get_rect().x, text.get_rect().y))
            else:
                # Append the entered character to the text
                str_variable += event.unicode

        return variable, str_variable, bool_active, text


    def save_writing_rectangle(self, str_variable, text, nb_cars=False):
        """
        Save the text in the writing rectangle
        """
        try:
            variable = int(str_variable)  # Convert the text to an integer

            if nb_cars:  # If it's the number of cars we change the variable in the file parameters
                if variable < 0:
                    variable = 0
                with open("data/parameters", "w") as file_parameters_write:
                    file_parameters_write.write(str(var.NUM_MAP) + "\n" + str(variable))

            # We check if the value is correct for a dice
            else:
                if variable < 1:
                    variable = 1
                elif variable > 6:
                    variable = 6

        except ValueError:
            print("Erreur sur la valeur rentrée")
            variable = 0

        str_variable = str(variable)  # Reset the text
        self.activated = False  # Uncheck the button
        var.WINDOW.blit(var.BACKGROUND, (text.get_rect().x, text.get_rect().y))
        text = var.FONT.render(str_variable, True, (0, 0, 0), (255, 255, 255))  # Change the text one last time

        return variable, str_variable, text
