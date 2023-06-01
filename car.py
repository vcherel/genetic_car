import pygame  # Pygame library
import math  # Math library
import variables  # Variables of the game
from constants import WINDOW, MAX_SPEED, MIN_MEDIUM_SPEED, MIN_HIGH_SPEED, DECELERATION, ACCELERATION, WIDTH_SCREEN, \
    HEIGHT_SCREEN, TURN_ANGLE, MIN_SPEED, RADIUS_CHECKPOINT  # Constants of the game
from utils import compute_detection_cone_points, compute_front_of_car  # To compute the coordinates of the point of the detection cone
from variables import KEYBOARD_CONTROL, CHECKPOINTS, NUM_MAP  # Variables of the game
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
        self.dead = False  # True if the car is dead, False otherwise

        self.speed = 0  # Current speed of the car
        self.speed_state = "slow"  # Current speed state of the car
        self.acceleration = 0  # Current acceleration of the car

        self.angle = 0  # Current angle of the car
        self.pos = pos  # Current position of the car

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
        self.speed_state = "slow"

        self.angle = 0
        self.pos = pos

        self.next_checkpoint = 0

    def move(self):
        """
        Move the car and update its state
        """
        self.detect_checkpoint()  # Detect if the car has reached a checkpoint
        self.change_speed_angle()  # Change the speed and the angle of the car (depending on the genetic cone)
        self.update_pos()  # Update the position and orientation of the car
        self.detect_collision()  # Detect if the car is dead and erase it if it is the case
        if variables.DEBUG:
            self.draw_detection_cone()  # Draw the detection cone of the car

    def detect_checkpoint(self):
        """
        Detect if the car has reached a checkpoint (or multiple checkpoints)

        Return:
            bool: True if the car has reached a checkpoint, False otherwise
        """
        checkpoint_passed = False  # True if the car has passed a checkpoint, False otherwise
        actual_checkpoint = variables.CHECKPOINTS[self.next_checkpoint]  # Actual checkpoint to reach
        if actual_checkpoint[0] - RADIUS_CHECKPOINT < self.pos[0] < actual_checkpoint[0] + RADIUS_CHECKPOINT and\
                actual_checkpoint[1] - RADIUS_CHECKPOINT < self.pos[1] < actual_checkpoint[1] + RADIUS_CHECKPOINT:
            self.genetic.fitness += 1
            self.next_checkpoint += 1
            checkpoint_passed = True
            if self.next_checkpoint == len(variables.CHECKPOINTS):
                self.next_checkpoint = 0

        if checkpoint_passed:   # If the car has passed a checkpoint, we check if it has passed multiple checkpoints
            self.detect_checkpoint()

    def change_speed_angle(self):
        """
        Change the acceleration and the angle of the car (depending on the genetic cone)

        Return:
            float: acceleration of the car
        """
        # We select the right cone depending on the speed of the car
        if self.speed < MIN_MEDIUM_SPEED:
            width = self.genetic.width_slow
            height = self.genetic.height_slow
            self.speed_state = "slow"
        elif self.speed < MIN_HIGH_SPEED:
            width = self.genetic.width_medium
            height = self.genetic.height_medium
            self.speed_state = "medium"
        else:
            width = self.genetic.width_fast
            height = self.genetic.height_fast
            self.speed_state = "fast"

        front_of_car = compute_front_of_car(self.pos, self.angle, self.image)  # Point of the front of the car
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, width, height)  # Points of the detection cone

        if variables.DEBUG:
            pygame.draw.polygon(WINDOW, (0, 0, 0), (front_of_car, left, top, right), 3)  # Draw the detection cone

        # If the point top is outside the window or if the point top is on a black pixel of the background
        if top[0] <= 0 or top[0] >= WIDTH_SCREEN or top[1] <= 0 or top[1] >= HEIGHT_SCREEN or variables.BACKGROUND.get_at(
                (int(top[0]), int(top[1]))) == (0, 0, 0, 255):
            self.acceleration = DECELERATION  # The car decelerates
        else:
            self.acceleration = ACCELERATION  # Else the car accelerates

        if left[0] <= 0 or left[0] >= WIDTH_SCREEN or left[1] <= 0 or left[1] >= HEIGHT_SCREEN or variables.BACKGROUND.get_at(
                (int(left[0]), int(left[1]))) == (0, 0, 0, 255):
            self.angle -= TURN_ANGLE
        if right[0] <= 0 or right[0] >= WIDTH_SCREEN or right[1] <= 0 or right[1] >= HEIGHT_SCREEN or variables.BACKGROUND.get_at(
                (int(right[0]), int(right[1]))) == (0, 0, 0, 255):
            self.angle += TURN_ANGLE

    def update_pos(self):
        """
        Update the position and the angle of the car
        """
        if KEYBOARD_CONTROL:
            # Control of the car with the keyboard
            keys = pygame.key.get_pressed()  # Key pressed
            if keys[pygame.K_LEFT]:
                self.angle += TURN_ANGLE
            elif keys[pygame.K_RIGHT]:
                self.angle -= TURN_ANGLE
            if keys[pygame.K_UP]:
                self.speed += self.acceleration
            else:
                self.speed = 0

        else:
            # Change the speed of the car
            self.speed += self.acceleration  # Update the speed of the car

        # Limit the speed of the car (between MIN_SPEED and MAX_SPEED)
        if self.speed > MAX_SPEED:  # If the speed is too high
            self.speed = MAX_SPEED  # Set the speed to the maximum speed
        elif self.speed < MIN_SPEED:  # If the speed is negative
            self.speed = MIN_SPEED  # Set the speed to 0

        # Move the car
        radians = math.radians(-self.angle)  # Convert the angle to radians
        dx = math.cos(radians) * self.speed  # The movement of the car on the x-axis
        dy = math.sin(radians) * self.speed  # The movement of the car on the y-axis
        self.pos = self.pos[0] + dx, self.pos[1] + dy  # Update the position of the car

        # Rotate the car
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image of the car
        self.rotated_rect = self.rotated_image.get_rect(
            center=self.image.get_rect(center=self.pos).center)  # Rotate the rectangle of the car

    def detect_collision(self):
        """
        Detect collision of the car with the walls
        """
        if self.pos[0] < 0 or self.pos[0] > WINDOW.get_width() or self.pos[1] < 0 or self.pos[1] > WINDOW.get_height():
            self.dead = True  # Collision with the wall of the window

        # Collision with the walls of the circuit
        car_mask = pygame.mask.from_surface(self.rotated_image)
        if variables.BACKGROUND_MASK.overlap(car_mask, self.rotated_rect.topleft) is not None:
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
        front_of_car = compute_front_of_car(self.pos, self.angle, self.image)  # Point of the front of the car

        # Slow detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_slow, self.genetic.height_slow)
        pygame.draw.polygon(WINDOW, (0, 0, 255), (front_of_car, left, top, right), 1)

        # Medium detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_medium, self.genetic.height_medium)
        pygame.draw.polygon(WINDOW, (0, 255, 0), (front_of_car, left, top, right), 1)

        # Fast detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_fast, self.genetic.height_fast)
        pygame.draw.polygon(WINDOW, (255, 0, 0), (front_of_car, left, top, right), 1)
