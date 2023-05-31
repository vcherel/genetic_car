import pygame  # To use pygame
import sys  # To exit the game
from constants import WINDOW, BACKGROUND  # Import the window and the background
from variables import DEBUG  # Import the debug mode


def play():
    """
    Play the game
    """
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Quit the game
            # Detection of clicks
            elif DEBUG and event.type == pygame.MOUSEBUTTONDOWN:
                print("Click at position", pygame.mouse.get_pos())  # Print the position of the click


if __name__ == '__main__':
    """
    Main program
    """
    WINDOW.blit(BACKGROUND, (0, 0))  # Screen initialization
    pygame.display.update()  # Update the screen
    play()  # Play the game
