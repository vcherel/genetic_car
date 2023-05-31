import pygame  # Pygame library
import math  # Math library
from constants import MAX_SPEED, WINDOW, MIN_MEDIUM_SPEED, MIN_HIGH_SPEED, ACCELERATION  # Constants of the game
from variables import BACKGROUND_MASK # Background mask of the game
from genetic import Genetic  # Genetic algorithm of the car


class Car:
    def __init__(self, image, pos):
        """
        Initialization of the car

        Args:
            image (pygame.surface.Surface): image of the car
            pos (tuple(int,int)): position of the car
        """
        self.genetic = Genetic()  # Genetic of the car
        self.dead = False   # True if the car is dead, False otherwise

        self.speed = 0  # Current speed of the car
        self.speed_state = 0  # Current speed state of the car (0: low, 1: medium, 2: high)

        self.angle = 0  # Current angle of the car
        self.pos = pos      # Current position of the car

        self.image = image  # Image of the car
        self.rotated_image = self.image  # Rotated image of the car
        self.rotated_rect = self.image.get_rect()  # Rotated rectangle of the car

        self.next_checkpoint = 0  # Next checkpoint to reach

    def init(self, pos):
        """
        Initialize the car
        """
        self.dead = False

        self.speed = 0
        self.speed_state = 0

        self.angle = 0
        self.pos = pos

        self.next_checkpoint = 0

    def move(self):
        """
        Move the car and update its state
        """
        self.update_pos()
        self.detect_collision()
        self.update_state()
        self.draw()

    def update_pos(self):
        """
        Update the position and the angle of the car
        """
        self.speed += ACCELERATION

        radians = math.radians(-self.angle)  # Convert the angle to radians
        dx = math.cos(radians) * self.speed  # The movement of the car on the x-axis
        dy = math.sin(radians) * self.speed  # The movement of the car on the y-axis
        self.pos = self.pos[0] + dx, self.pos[1] + dy  # Update the position of the car

        # Rotate the car
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image of the car
        self.rotated_rect = self.rotated_image.get_rect(center=self.image.get_rect(center=self.pos).center)  # Rotate the rectangle of the car

    def detect_collision(self):
        """
        Detect the collision of the car
        """
        if self.pos[0] < 0 or self.pos[0] > WINDOW.get_width() or self.pos[1] < 0 or self.pos[1] > WINDOW.get_height():
            self.dead = True    # Collision with the wall of the window

        # Collision with the walls of the circuit
        car_mask = pygame.mask.from_surface(self.rotated_image)
        if BACKGROUND_MASK.overlap(car_mask, self.rotated_rect.topleft) is not None:
            self.dead = True

    def update_state(self):
        """
        Update the state of the car
        """
        if self.speed > MAX_SPEED:
            self.speed = MAX_SPEED
        elif self.speed < 0:
            self.speed = 0

        if self.speed < MIN_MEDIUM_SPEED:
            self.speed_state = 0
        elif self.speed < MIN_HIGH_SPEED:
            self.speed_state = 1
        else:
            self.speed_state = 2

    def draw(self):
        """
        Draw the car
        """
        WINDOW.blit(self.rotated_image, self.rotated_rect)  # We display the car
