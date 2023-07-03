from src.render.button import Button  # Import the button class
import src.other.variables as var  # Import the variables
import pygame  # To use pygame


class Settings:
    def __init__(self):
        """
        Initialize the settings window the first time
        """
        self.rect = None  # Rectangle of the window
        self.fps_button = None  # Button to change the FPS
        self.fps_text = None  # Text of the button to change the FPS

        self.debug_button = None  # Button to activate the debug mode
        self.debug_text = None  # Text of the button to activate the debug mode

    def init(self):
        """
        Initialize the settings window
        """
        self.rect = pygame.Rect(500, 125, 500, 550)  # Create the rectangle for the window
        self.fps_text = var.FONT.render('FPS :', True, (0, 0, 0), (128, 128, 128))  # Text of the fps button
        self.debug_text = var.FONT.render('Debug :', True, (0, 0, 0), (128, 128, 128))  # Text of the debug button

        self.fps_button = Button(self.rect.x + 100, self.rect.y + 20, pygame.image.load(var.PATH_IMAGE + '/writing_rectangle_1.png'),
                                 pygame.image.load(var.PATH_IMAGE + '/writing_rectangle_2.png'),
                                 pygame.image.load(var.PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True, variable=var.FPS, text=str(var.FPS), scale_x=0.5, scale_y=1)  # Create the button to change the FPS
        self.debug_button = Button(self.rect.x + 120, self.rect.y + 72, pygame.image.load(var.PATH_IMAGE + '/checkbox_1.png'), pygame.image.load(var.PATH_IMAGE + '/checkbox_2.png'),
                                   pygame.image.load(var.PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.1)

    def show(self):
        """
        Display the settings window
        """
        pygame.draw.rect(var.WINDOW, (128, 128, 128), self.rect, 0)  # Draw the rectangle (inside)
        pygame.draw.rect(var.WINDOW, (115, 205, 255), self.rect, 2)  # Draw the rectangle (contour)


        var.WINDOW.blit(self.fps_text, (self.rect.x + 40, self.rect.y + 27))
        var.WINDOW.blit(self.debug_text, (self.rect.x + 40, self.rect.y + 77))

        self.fps_button.check_state()  # Check the state of the button
        if self.fps_button.just_clicked:
            self.fps_button.text = ''  # We delete the text of the button

        var.DEBUG = self.debug_button.check_state()  # Check the state of the button

    def erase(self):
        """
        Erase the settings window
        """
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)


SETTINGS = Settings()  # Create the settings window