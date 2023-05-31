import pygame  # Pygame library
from genetic import Genetic  # Genetic algorithm of the car
from constants import MAX_SPEED, WINDOW  # Maximum speed of the car


class Car:
    def __init__(self, image, pos):
        """
        Initialization of the car

        Args:
            image (pygame.surface.Surface): image of the car
            pos (tuple(int,int)): position of the car
        """
        self.genetic = Genetic()  # Genetic of the car

        self.speed = MAX_SPEED  # Current speed of the car
        self.angle = 0  # Current angle of the car

        self.pos = pos  # Current position of the car
        self.state = "alive"  # Current state of the car

        self.image = image  # Image of the car
        self.rotated_image = self.image  # Rotated image of the car
        self.rotated_rect = self.image.get_rect()  # Rotated rectangle of the car

        self.next_checkpoint = 0  # Next checkpoint to reach

    def update(self):
        """
        Update the car
        """

        # Rotate the car
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.image.get_rect(center=self.pos).center)

    def draw(self):
        """
        Draw the car
        """
        WINDOW.blit(self.rotated_image, self.rotated_rect)  # We display the car
