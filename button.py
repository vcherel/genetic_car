import pygame  # To use pygame


class Button:
    def __init__(self, x, y, image, scale, check_box=False, image_hover=None, image_clicked=None):
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
        self.clicked = False  # True if the button is clicked, False otherwise
        self.check_box = check_box   # True if the button is a checkbox, False otherwise
        self.image_hover = image_hover  # Image of the button when the mouse is over it
        self.image_clicked = image_clicked  # Image of the button when it is clicked

    def draw(self, surface):
        """
        Detect if the mouse is over the button and if it is clicked, and draw the button on the screen with the appropriate image

        Args:
            surface (pygame.Surface): surface on which the button is drawn
        """
        if self.clicked and self.image_clicked is not None:  # Button clicked and has a clicked image
            image = self.image_clicked
        else:
            image = self.image  # Image of the button

        if self.rect.collidepoint(pygame.mouse.get_pos()):  # Mouse over the button
            if pygame.mouse.get_pressed()[0] == 1:    # Mouse clicked
                if self.clicked:       # Button already clicked
                    if self.check_box:
                        self.clicked = False
                else:   # Button not already clicked
                    self.clicked = True
                    if self.image_clicked is not None:
                        image = self.image_clicked

            else:  # Mouse not clicked
                if self.image_hover is not None:   # Button has a hover image
                    image = self.image_hover    # We change the image of the button if the mouse is over it
                if not self.check_box:
                    self.clicked = False    # We reset the clicked state of the button if it is not a checkbox

        # Draw button on screen
        surface.blit(image, (self.rect.x, self.rect.y))

        return self.clicked  # Return True if the button is clicked (or activated), False otherwise
