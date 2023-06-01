import pygame  # To use pygame
import variables  # Import the variables
from constants import WINDOW, RADIUS_CHECKPOINT  # Import the constants


def display_checkpoints():
    for checkpoint in variables.CHECKPOINTS:
        pygame.draw.circle(WINDOW, (255, 0, 0), checkpoint, RADIUS_CHECKPOINT, 1)
