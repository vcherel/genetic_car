import pygame  # To use pygame
import variables  # Import the variables
from constants import WINDOW, RADIUS_CHECKPOINT, FONT  # Import the constants


def edit_background():
    """
    Add elements to the background for the rest of the game
    """
    # Add a text for the debug mode
    variables.BACKGROUND.blit(FONT.render("Activer debug :", True, (255, 255, 255), (0, 0, 0)), (1290, 640))  # Add the debug text
    variables.BACKGROUND.blit(FONT.render("Nombre de voitures", True, (0, 0, 0), (128, 128, 128)), (1060, 25))  # Add the yes text
    pygame.draw.line(variables.BACKGROUND, (0, 0, 0), (1280, 120), (1280, 0), 2)  # Line at the left of start button


def display_checkpoints():
    for checkpoint in variables.CHECKPOINTS:
        pygame.draw.circle(WINDOW, (255, 0, 0), checkpoint, RADIUS_CHECKPOINT, 1)
