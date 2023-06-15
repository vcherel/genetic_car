import pygame  # Pygame library
import math  # Math library
import variables as var  # Variables of the game
from constants import RADIUS_CHECKPOINT, WIDTH_SCREEN, HEIGHT_SCREEN  # Constants of the game
from utils import compute_detection_cone_points, detect_wall  # To compute the coordinates of the point of the detection cone
from genetic import Genetic  # Genetic algorithm of the car


# Constants
max_speed = 8  # Maximum speed of the car
min_speed = 1  # Minimum speed of the car
min_medium_speed = max_speed / 3
min_high_speed = max_speed / 3 * 2
turn_angle = 5  # Angle of rotation of the car
acceleration = 0.2  # Acceleration of the car
deceleration = -1  # Deceleration of the car


class Car:
    def __init__(self, genetic=None, view_only=False, best_car=False):
        """
        Initialization of the car

        Args:
            genetic (Genetic): genetic of the car to copy (if None, create a new genetic)
            view_only (bool): True if the car is in view only mode, False otherwise (view only is when the car is grey)
        """
        if genetic is None:
            self.genetic = Genetic()  # Genetic of the car
        else:
            self.genetic = Genetic(genetic)

        self.dead = False  # True if the car is dead, False otherwise

        self.speed = 0  # Current speed of the car
        self.acceleration = 0  # Current acceleration of the car

        self.angle = 0  # Current angle of the car
        self.pos = var.START_POSITION  # Current position of the car

        if view_only:
            self.image = var.GREY_CAR_IMAGE  # Image of the car but grey
        elif best_car:
            self.image = var.YELLOW_CAR_IMAGE  # Image of the car but yellow
        else:
            self.image = var.RED_CAR_IMAGE  # Image of the car

        self.rotated_image = self.image  # Rotated image of the car
        self.rotated_rect = self.image.get_rect()  # Rotated rectangle of the car

        self.view_only = view_only  # True if the car is in view only mode, False otherwise

        self.next_checkpoint = 0  # Next checkpoint to reach
        self.score = 0  # Score of the car

        self.points_detection_cone = []  # Points of the detection cone if DEBUG is True

    def __str__(self):
        """
        Return the string representation of the car

        Return:
            str: string representation of the car
        """
        return "Car: " + str(self.genetic)

    def move(self):
        """
        Move the car and update its state
        """
        self.detect_checkpoint()  # Detect if the car has reached a checkpoint
        self.change_speed_angle()  # Change the speed and the angle of the car (depending on the genetic cone)
        self.update_pos()  # Update the position and orientation of the car
        self.detect_collision()  # Detect if the car is dead

    def detect_checkpoint(self):
        """
        Detect if the car has reached a checkpoint (or multiple checkpoints)

        Return:
            bool: True if the car has reached a checkpoint, False otherwise
        """
        checkpoint_passed = False  # True if the car has passed a checkpoint, False otherwise
        actual_checkpoint = var.CHECKPOINTS[self.next_checkpoint]  # Actual checkpoint to reach
        if actual_checkpoint[0] - RADIUS_CHECKPOINT < self.pos[0] < actual_checkpoint[0] + RADIUS_CHECKPOINT and\
                actual_checkpoint[1] - RADIUS_CHECKPOINT < self.pos[1] < actual_checkpoint[1] + RADIUS_CHECKPOINT:
            self.score += 1
            self.next_checkpoint += 1
            checkpoint_passed = True
            if self.next_checkpoint == len(var.CHECKPOINTS):
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
        width, height = self.determine_size_cone()

        front_of_car = self.determine_front_of_car()  # Point of the front of the car
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, width, height)  # Points of the detection cone

        wall_at_top = detect_wall(front_of_car, top)  # Detect if the car is near a wall (top)
        wall_at_left = detect_wall(front_of_car, left)  # Detect if the car is near a wall (left)
        wall_at_right = detect_wall(front_of_car, right)  # Detect if the car is near a wall (right)

        # If there is a wall in front of the car, we decelerate it
        if wall_at_top:
            self.acceleration = deceleration
        else:
            self.acceleration = acceleration
        
        # If there is a wall on the left or on the right of the car, we turn it
        if wall_at_left:
            self.angle -= turn_angle
        if wall_at_right:
            self.angle += turn_angle

    def update_pos(self):
        """
        Update the position and the angle of the car
        """
        # Change the speed of the car
        self.speed += self.acceleration  # Update the speed of the car

        # Limit the speed of the car (between MIN_SPEED and MAX_SPEED)
        if self.speed > max_speed:  # If the speed is too high
            self.speed = max_speed  # Set the speed to the maximum speed
        elif self.speed < min_speed:  # If the speed is negative
            self.speed = min_speed  # Set the speed to 0

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
        Detect collision of the car with the walls
        """
        if self.pos[0] < 0 or self.pos[0] > WIDTH_SCREEN or self.pos[1] < 0 or self.pos[1] > HEIGHT_SCREEN:
            self.kill()  # Collision with the wall of the window

        car_mask = pygame.mask.from_surface(self.rotated_image)
        if var.BACKGROUND_MASK.overlap(car_mask, self.rotated_rect.topleft) is not None:
            self.kill()  # Collision with the walls of the circuit

    def determine_size_cone(self):
        """
        Determine the size of the detection cone according to the speed of the car

        Returns:
            width, height (int, int): the width and the height of the detection cone
        """
        if self.speed < min_medium_speed:
            width = self.genetic.width_slow
            height = self.genetic.height_slow
        elif self.speed < min_high_speed:
            width = self.genetic.width_medium
            height = self.genetic.height_medium
        else:
            width = self.genetic.width_fast
            height = self.genetic.height_fast
        return width, height

    def determine_front_of_car(self):
        """
        Compute the coordinates of the front of the car
        Args:

        Returns:
            front_of_car (tuple(int, int)): the coordinates of the front of the car
        """
        return self.pos[0] + math.cos(math.radians(-self.angle)) * self.image.get_width() / 2,\
            self.pos[1] + math.sin(math.radians(-self.angle)) * self.image.get_width() / 2

    def kill(self):
        """
        Kill the car
        """
        self.dead = True  # The car is dead
        var.NB_CARS_ALIVE -= 1  # Decrease the number of cars alive

    def draw(self):
        """
        Draw the car
        """
        var.WINDOW.blit(self.rotated_image, self.rotated_rect)  # We display the car
        if var.DEBUG and not self.dead:
            self.draw_detection_cone()  # Draw the detection cone of the car

    def erase(self):
        """
        Erase the car
        """
        var.WINDOW.blit(var.BACKGROUND, self.rotated_rect, self.rotated_rect)  # Erase the car

    def draw_detection_cone(self):
        """
        Draw the 3 detection cones of the car
        """
        front_of_car = self.determine_front_of_car()  # Point of the front of the car

        # Slow detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_slow, self.genetic.height_slow)
        if self.speed < min_medium_speed:
            pygame.draw.polygon(var.WINDOW, (10, 10, 10), (front_of_car, left, top, right), 3)
        else:
            pygame.draw.polygon(var.WINDOW, (0, 0, 255), (front_of_car, left, top, right), 1)

        # Medium detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_medium, self.genetic.height_medium)
        if min_medium_speed < self.speed < min_high_speed:
            pygame.draw.polygon(var.WINDOW, (10, 10, 10), (front_of_car, left, top, right), 3)
        else:
            pygame.draw.polygon(var.WINDOW, (0, 255, 0), (front_of_car, left, top, right), 1)

        # Fast detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_fast, self.genetic.height_fast)
        if self.speed > min_high_speed:
            pygame.draw.polygon(var.WINDOW, (10, 10, 10), (front_of_car, left, top, right), 3)
        else:
            pygame.draw.polygon(var.WINDOW, (255, 0, 0), (front_of_car, left, top, right), 1)
