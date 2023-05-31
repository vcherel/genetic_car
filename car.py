import pygame  # Pygame library
import math  # Math library
from constants import MAX_SPEED, WINDOW, MIN_MEDIUM_SPEED, MIN_HIGH_SPEED  # Constants of the game
from variables import BACKGROUND_MASK, BACKGROUND, DEBUG  # Variables of the game
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
        self.acceleration = 0.5  # Current acceleration of the car

        self.angle = 0  # Current angle of the car
        self.pos = pos      # Current position of the car

        self.image = image  # Image of the car
        self.rotated_image = self.image  # Rotated image of the car
        self.rotated_rect = self.image.get_rect()  # Rotated rectangle of the car

        self.next_checkpoint = 0  # Next checkpoint to reach

    def init(self, pos):
        """
        Initialize the car (after a death)
        """
        self.dead = False

        self.speed = 0

        self.angle = 0
        self.pos = pos

        self.next_checkpoint = 0

    def move(self):
        """
        Move the car and update its state
        """
        self.change_acceleration()  # Change the acceleration of the car (depending on the genetic cone)
        self.update_pos()  # Erase the previous position of the car and update its position / orientation
        self.detect_collision()  # Detect if the car is dead and erase it if it is the case
        if DEBUG:
            self.draw_detection_cone()  # Draw the detection cone of the car

    def change_acceleration(self):
        """
        Change the acceleration of the car (depending on the genetic cone)

        Return:
            float: acceleration of the car
        """
        if self.speed < MIN_MEDIUM_SPEED:
            width = self.genetic.width_slow
            height = self.genetic.height_slow
        elif self.speed < MIN_HIGH_SPEED:
            width = self.genetic.width_medium
            height = self.genetic.height_medium
        else:
            width = self.genetic.width_fast
            height = self.genetic.height_fast

        # Get the point at the middle of the front of the car
        front_of_car = self.pos[0] + math.cos(math.radians(self.angle)) * self.image.get_width() / 2, self.pos[1] + math.sin(math.radians(self.angle)) * self.image.get_width() / 2

        # Get the points of the detection cone
        left = front_of_car[0] + math.cos(math.radians(self.angle + 90)) * width, front_of_car[1] + math.sin(math.radians(self.angle + 90)) * width
        right = front_of_car[0] + math.cos(math.radians(self.angle - 90)) * width, front_of_car[1] + math.sin(math.radians(self.angle - 90)) * width
        top = front_of_car[0] + math.cos(math.radians(self.angle)) * height, front_of_car[1] + math.sin(math.radians(self.angle)) * height

    def update_pos(self):
        """
        Update the position and the angle of the car
        """
        # Change the speed of the car
        self.speed += self.acceleration  # Update the speed of the car
        if self.speed > MAX_SPEED:  # If the speed is too high
            self.speed = MAX_SPEED  # Set the speed to the maximum speed
        elif self.speed < 0:  # If the speed is negative
            self.speed = 0  # Set the speed to 0

        # Move the car
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

    def draw(self):
        """
        Draw the car
        """
        WINDOW.blit(self.rotated_image, self.rotated_rect)  # We display the car

    def draw_detection_cone(self):
        """
        Draw the 3 detection cones of the car
        """
        front_of_car = self.pos[0] + math.cos(math.radians(self.angle)) * self.image.get_width() / 2, self.pos[1] + math.sin(math.radians(self.angle)) * self.image.get_width() / 2

        # Slow detection cone
        top = front_of_car[0] + math.sqrt((self.genetic.width_slow / 2)**2 + self.genetic.height_slow**2) + math.cos(math.radians(self.angle)) * self.genetic.height_slow,\
            front_of_car[1] + math.sin(math.radians(self.angle)) * self.genetic.height_slow
        left = front_of_car[0] + self.genetic.height_slow + math.cos(math.radians(self.angle)) * self.genetic.height_slow,\
            front_of_car[1] - self.genetic.width_slow / 2 + math.sin(math.radians(self.angle)) * self.genetic.height_slow
        right = front_of_car[0] + self.genetic.height_slow + math.cos(math.radians(self.angle)) * self.genetic.height_slow,\
            front_of_car[1] + self.genetic.width_slow / 2 + math.sin(math.radians(self.angle)) * self.genetic.height_slow
        pygame.draw.polygon(WINDOW, (255, 0, 0), (front_of_car, left, top, right), 1)

        # Medium detection cone
        top = front_of_car[0] + math.sqrt((self.genetic.width_medium / 2)**2 + self.genetic.height_medium**2) + math.cos(math.radians(self.angle)) * self.genetic.height_medium,\
            front_of_car[1] + math.sin(math.radians(self.angle)) * self.genetic.height_medium
        left = front_of_car[0] + self.genetic.height_medium + math.cos(math.radians(self.angle)) * self.genetic.height_medium,\
            front_of_car[1] - self.genetic.width_medium / 2 + math.sin(math.radians(self.angle)) * self.genetic.height_medium
        right = front_of_car[0] + self.genetic.height_medium + math.cos(math.radians(self.angle)) * self.genetic.height_medium,\
            front_of_car[1] + self.genetic.width_medium / 2 + math.sin(math.radians(self.angle)) * self.genetic.height_medium
        pygame.draw.polygon(WINDOW, (0, 255, 0), (front_of_car, left, top, right), 1)

        # Fast detection cone
        top = front_of_car[0] + math.sqrt((self.genetic.width_fast / 2)**2 + self.genetic.height_fast**2) + math.cos(math.radians(self.angle)) * self.genetic.height_fast,\
            front_of_car[1] + math.sin(math.radians(self.angle)) * self.genetic.height_fast
        left = front_of_car[0] + self.genetic.height_fast + math.cos(math.radians(self.angle)) * self.genetic.height_fast,\
            front_of_car[1] - self.genetic.width_fast / 2 + math.sin(math.radians(self.angle)) * self.genetic.height_fast
        right = front_of_car[0] + self.genetic.height_fast + math.cos(math.radians(self.angle)) * self.genetic.height_fast,\
            front_of_car[1] + self.genetic.width_fast / 2 + math.sin(math.radians(self.angle)) * self.genetic.height_fast
        pygame.draw.polygon(WINDOW, (0, 0, 255), (front_of_car, left, top, right), 1)
