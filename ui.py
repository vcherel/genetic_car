import pygame  # To use pygame
import sys  # To exit the game
from variables import DEBUG  # Import the variables


def detect_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()  # Quit the game
        # Detection of clicks
        elif DEBUG and event.type == pygame.MOUSEBUTTONDOWN:
            print("Click at position", pygame.mouse.get_pos())  # Print the position of the click
