import pygame  # To use pygame
from constants import WINDOW  # Import the window


class Button:
    def __init__(self, x, y, image, image_hover=None, image_clicked=None, check_box=False, writing_rectangle=False, scale=1):
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
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))  # Image of the button
        self.rect = self.image.get_rect()  # Rectangle of the button
        self.rect.topleft = (x, y)  # Position of the button
        self.check_box = check_box   # True if the button is a checkbox, False otherwise
        self.writing_rectangle = writing_rectangle   # True if the button is a writing rectangle, False otherwise
        self.checked = False    # True if the checkbox is checked, False otherwise
        self.time_clicked = 0   # Time when the button is clicked

        if image_hover is not None:
            self.image_hover = pygame.transform.scale(image_hover, (int(image_hover.get_width() * scale), int(image_hover.get_height() * scale)))
        else:
            self.image_hover = None  # Image of the button when the mouse is over it
        if image_clicked is not None:
            self.image_clicked = pygame.transform.scale(image_clicked, (int(image_clicked.get_width() * scale), int(image_clicked.get_height() * scale)))
        else:
            self.image_clicked = None  # Image of the button when it is clicked

    def draw(self):
        """
        Detect if the mouse is over the button and if it is clicked, and draw the button on the screen with the appropriate image

        Returns:
            bool: True if the button is clicked (or activated), False otherwise
        """
        image = self.image  # Image of the button

        if self.rect.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            if pygame.mouse.get_pressed()[0] == 1 and pygame.time.get_ticks() - self.time_clicked > 100:    # Mouse clicked for the first time
                self.time_clicked = pygame.time.get_ticks()  # Get the time when the button is clicked
                if self.check_box:
                    self.checked = not self.checked  # Change the state of the checkbox
                else:
                    self.checked = True     # Activate the button

            else:
                if not self.check_box and not self.writing_rectangle:
                    self.checked = False  # Change the state if it's a simple button

            if self.image_hover is not None:
                image = self.image_hover   # Change the image if it's possible

        if self.checked and self.image_clicked is not None:
            image = self.image_clicked  # Change the image if it's possible

        # Draw button on screen
        WINDOW.blit(image, (self.rect.x, self.rect.y))

        return self.checked  # Return True if the button is clicked (or activated), False otherwise

    def uncheck_button(self):
        """
        Uncheck the button
        """
        self.checked = False    # Uncheck the button
