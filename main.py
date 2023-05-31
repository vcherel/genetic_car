import pygame  # To use pygame
import sys  # To exit the game
from constants import WINDOW, BACKGROUND  # Import the window and the background


def play():
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()  # Quit the game


if __name__ == '__main__':
    """
    Main program
    """
    WINDOW.blit(BACKGROUND, (0, 0))  # Screen initialization
    pygame.display.update()  # Update the screen
    play()  # Play the game
