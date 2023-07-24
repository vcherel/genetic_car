from src.other.utils import convert_to_new_window  # Utils functions
import src.data.variables as var  # Import the variables
import pygame  # To use pygame

"""
This file contains the Explosion class, used to render explosions.
"""


class Explosion(pygame.sprite.Sprite):
    """
    This class is used to represent an explosion, it's a subclass of the Sprite class.
    """
    def __init__(self, pos):
        """
        Constructor of the Explosion class

        Args:
            pos (tuple): Position of the explosion
        """
        pygame.sprite.Sprite.__init__(self)   # Call the parent class (Sprite) constructor
        self.images = var.EXPLOSION_IMAGES   # List of all the images of the explosion
        self.index = 0  # Index of the current image
        self.image = self.images[self.index]  # First image of the explosion

        self.rect = self.image.get_rect()  # Rectangle of the explosion
        self.rect.center = convert_to_new_window(pos)  # Position of the explosion

        self.timer = 0  # Counter used to know when to change the image
        self.delay = 125  # Delay between each image change

    def update(self):
        """
        Update the explosion
        """
        if pygame.time.get_ticks() - self.timer > self.delay and self.index < len(self.images) - 1:
            self.timer = pygame.time.get_ticks()
            self.index += 1
            self.image = self.images[self.index]  # Update the image
            var.RECTS_BLIT_EXPLOSION.append(self.rect)  # We blit the background to remove the last image of the explosion

        if self.index >= len(self.images) - 1:  # We have reached the end of the animation, and we can kill the explosion
            var.RECTS_BLIT_EXPLOSION.append(self.rect)  # We blit the background to remove the explosion
            self.kill()  # Kill the explosion
