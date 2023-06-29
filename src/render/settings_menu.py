from src.render.button import Button  # Import the button class
import src.other.variables as var  # Import the variables
import os.path  # To get the path of the file
import pygame  # To use pygame


class Settings:
    def __init__(self):
        path_images = os.path.dirname(__file__) + '/../../images/'  # Path of the images

        self.rect = pygame.Rect(500, 125, 500, 550)  # Create the rectangle for the window

        self.fps_button = Button(self.rect.x + 100, self.rect.y + 20, pygame.image.load(path_images + '/writing_rectangle_1.png'),
                                 pygame.image.load(path_images + '/writing_rectangle_2.png'),
                                 pygame.image.load(path_images + '/writing_rectangle_3.png'), checkbox=True, scale_x=0.2, scale_y=1)  # Create the button to change the FPS
        self.fps_text = var.FONT.render('FPS :', True, (0, 0, 0), (128, 128, 128))  # Text of the medium button



    def show(self):
        """
        Display the settings window
        """
        pygame.draw.rect(var.WINDOW, (128, 128, 128), self.rect, 0)  # Draw the rectangle (inside)
        pygame.draw.rect(var.WINDOW, (115, 205, 255), self.rect, 2)  # Draw the rectangle (contour)

        self.fps_button.check_state()  # Check the state of the button
        var.WINDOW.blit(self.fps_text, (self.rect.x + 40, self.rect.y + 27))

    def erase(self):
        """
        Erase the settings window
        """
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)


SETTINGS = Settings()  # Create the settings window