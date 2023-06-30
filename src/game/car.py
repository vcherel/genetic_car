from src.other.utils import compute_detection_cone_points, point_out_of_window, create_rect_from_points  # To compute the coordinates of the point of the detection cone
from src.game.constants import RADIUS_CHECKPOINT, WIDTH_SCREEN, HEIGHT_SCREEN  # Constants of the game
from src.game.genetic import Genetic  # Genetic algorithm of the car
import src.other.variables as var  # Variables of the game
import pygame  # Pygame library
import math  # Math library

"""
This file contains the class Car used to represent a car in the game. The car is controlled by genetic parameters of the detection cone.
"""

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
            self.genetic = genetic.copy()  # Genetic of the car

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
        self.best_car = best_car  # True if the car is the best car, False otherwise

        self.next_checkpoint = 0  # Next checkpoint to reach
        self.score = 0  # Score of the car
        self.turn_played = 0  # Number of turn played by the car

        self.points_detection_cone = []  # Points of the detection cone if DEBUG is True

    def __str__(self):
        """
        Return the string representation of the car

        Return:
            str: string representation of the car
        """
        return f'Car: genetic : {self.genetic} ; view_only : {self.view_only} ; best_car : {self.best_car}'

    def __eq__(self, other):
        """
        Test the equality between the car and the other car, two cars are equal if they have the same genetic

        Args:
            other (Car): other car to compare

        Return:
            bool: True if the car is equal to the other car, False otherwise
        """
        return self.genetic == other.genetic

    def move(self):
        """
        Move the car and update its state
        """
        self.turn_played += 1  # Increment the number of turn played by the car
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
        if wall_at_left and wall_at_right:
            if wall_at_left < wall_at_right:
                self.angle -= turn_angle
            else:
                self.angle += turn_angle
        elif wall_at_left:
            self.angle -= turn_angle
        elif wall_at_right:
            self.angle += turn_angle

    def debug(self):
        # We select the right cone depending on the speed of the car
        width, height = self.determine_size_cone()

        front_of_car = self.determine_front_of_car()  # Point of the front of the car
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, width, height)  # Points of the detection cone

        wall_at_top = detect_wall(front_of_car, top)  # Detect if the car is near a wall (top)
        wall_at_left = detect_wall(front_of_car, left)  # Detect if the car is near a wall (left)
        wall_at_right = detect_wall(front_of_car, right)  # Detect if the car is near a wall (right)

        print(wall_at_top, wall_at_left, wall_at_right)


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
            # We move the car backward because we don't want the car to bo on top of the wall
            speed = 1  # Speed of the car
            radians = math.radians(-self.angle)  # Convert the angle to radians
            dx = math.cos(radians) * speed  # The movement of the car on the x-axis
            dy = math.sin(radians) * speed  # The movement of the car on the y-axis
            # While it touches the wall
            while var.BACKGROUND_MASK.overlap(car_mask, self.rotated_rect.topleft) is not None:
                self.pos = self.pos[0] - dx, self.pos[1] - dy  # Update the position of the car
                self.rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image of the car
                self.rotated_rect = self.rotated_image.get_rect(center=self.image.get_rect(center=self.pos).center)  # Rotate the rectangle of the car
                car_mask = pygame.mask.from_surface(self.rotated_image)

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

    def draw_car(self):
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

    def reset(self):
        """
        Reset the car
        """
        self.pos = var.START_POSITION  # Reset the position of the car
        self.angle = 0  # Reset the angle of the car


    def draw_detection_cone(self):
        """
        Draw the 3 detection cones of the car
        """
        front_of_car = self.determine_front_of_car()  # Point of the front of the car

        # Slow detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_slow, self.genetic.height_slow)
        points = [front_of_car, left, top, right]  # Points of the detection cone for the rect

        if self.speed < min_medium_speed:
            pygame.draw.polygon(var.WINDOW, (50, 50, 50), (front_of_car, left, top, right), 3)
        else:
            pygame.draw.polygon(var.WINDOW, (255, 255, 0), (front_of_car, left, top, right), 1)


        # Medium detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_medium, self.genetic.height_medium)
        points.append(left)
        points.append(top)
        points.append(right)

        if min_medium_speed < self.speed < min_high_speed:
            pygame.draw.polygon(var.WINDOW, (50, 50, 50), (front_of_car, left, top, right), 3)
        else:
            pygame.draw.polygon(var.WINDOW, (255, 128, 0), (front_of_car, left, top, right), 1)


        # Fast detection cone
        left, top, right = compute_detection_cone_points(self.angle, front_of_car, self.genetic.width_fast, self.genetic.height_fast)
        points.append(left)
        points.append(top)
        points.append(right)
        if self.speed > min_high_speed:
            pygame.draw.polygon(var.WINDOW, (50, 50, 50), (front_of_car, left, top, right), 3)
        else:
            pygame.draw.polygon(var.WINDOW, (255, 0, 0), (front_of_car, left, top, right), 1)

        # We add the rect to the rects to blit
        var.RECTS_BLIT_CAR.append(create_rect_from_points(points))


def detect_wall(front_of_car, point):
    """
    Detect if there is a wall between the front of the car and the point

    Args:
        front_of_car (tuple(int, int)): the coordinates of the front of the car
        point (tuple(int, int)): the coordinates of the point

    Returns:
        bool : True if there is a wall, False otherwise
    """
    x1, y1 = front_of_car  # Coordinates of the front of the car
    x2, y2 = point  # Coordinates of the point

    if x1 == x2:  # If the car is parallel to the wall
        # We check if there is a wall between the front of the car and the point
        for y in range(int(min(y1, y2)), int(max(y1, y2))):
            x1 = int(x1)
            # We check if the pixel is black (wall)
            if point_out_of_window((x1, y)) or var.BACKGROUND_MASK.get_at((x1, y)):
                return True  # There is a wall

    # We determine the equation of the line between the front of the car and the point (y = ax + b)
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    # We check if there is a wall between the front of the car and the point
    for x in range(int(min(x1, x2)), int(max(x1, x2))):
        y = int(a * x + b)
        # We check if the pixel is black (wall)
        if point_out_of_window((x, y)) or var.BACKGROUND_MASK.get_at((x, y)):
            return math.sqrt(
                (x1 - x) ** 2 + (y1 - y) ** 2)  # We return the distance between the front of the car and the wall
    return False  # There is no wall
