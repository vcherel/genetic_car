from data.variables_functions import checkpoint_reached
from other.utils import compute_detection_cone_points, point_out_of_window, create_rect_from_points, change_color_car  # Utils functions
from render.display import draw_detection_cone  # To draw the detection cone
from data.constants import NB_MAPS  # Number of different tracks
from game.genetic import Genetic  # Genetic algorithm of the car
from render.explosion import Explosion  # To render explosions
import data.variables as var  # Variables of the game
import pygame  # Pygame library
import math  # Math library

from render.resizing import convert_to_new_window, scale_image

"""
This file contains the class Car used to represent a car in the game. The car is controlled by genetic parameters of the detection cone.
"""


# Constants for the car
min_speed = 1  # Minimum speed of the car
add_to_speed_angle = 2  # Value added to the speed angle each turn to make it equals to the real angle
turn_decrease_factor = 1  # Factor of the decrease of the turn angle (when at high speed, the car turns 'turn_decrease_factor' times slower)


class Car:
    """
    Class representing a car in the game
    """
    def __init__(self, genetic=None, best_scores=None, color='red', id_memory_car=None):
        """
        Initialization of the car

        Args:
            genetic (Genetic): genetic of the car to copy
            best_scores (list): list of the best scores of the car for each map
            color (str): color of the car
            id_memory_car (int): id of the car in the memory (it means the car is in view only mode)
        """
        # Genetic of the car
        if genetic is None:
            self.genetic = Genetic()
        else:
            self.genetic = genetic.copy()

        # Best scores of the car in memory
        if best_scores:
            self.best_scores = best_scores
        else:
            self.best_scores = [0] * NB_MAPS

        self.id_memory_car = id_memory_car  # Id of the car in the memory (it means the car is in view only mode)
        self.color = color  # Color of the car

        self.speed, self.acceleration = 0, 0  # Speed and acceleration of the car

        self.angle = var.START_ANGLE  # Current angle of the car
        self.drift_angle = var.START_ANGLE  # Current speed angle of the car (when the car turns the angle change but the speed angle turns slower)

        self.pos = var.START_POSITION  # Current position of the car
        self.front_of_car = self.pos  # Current position of the front of the car

        self.image = change_color_car(var.RED_CAR_IMAGE, self.color)  # Image of the car but with the right color
        self.rotated_image = self.image  # Rotated image of the car
        self.rotated_rect = self.image.get_rect()  # Rotated rectangle of the car
        self.rotated_rect_shown = self.image.get_rect()  # Rotated rectangle of the car shown on the screen

        self.score = 0  # Score of the car
        self.next_checkpoint = 0  # Next checkpoint to reach
        self.turn_without_checkpoint = 0  # Number of turn played by the car without reaching a checkpoint

        self.dead = False  # True if the car is dead
        self.reverse = False  # True if the car is going in the wrong way (the direction of the car will no longer change)


    def __str__(self):
        """
        Return the string representation of the car

        Return:
            str: string representation of the car
        """
        return f'Car: genetic : {self.genetic} ; color : {self.color} ; position : {self.pos} ; angle : {self.angle} ; speed : {self.speed} ; acceleration : {self.acceleration} ; score : {self.score}'

    def __eq__(self, other):
        """
        Test the equality between the car and the other car, two cars are equal if they have the same genetic

        Args:
            other (Car): other car to compare

        Return:
            bool: True if the car is equal to the other car
        """
        return self.genetic == other.genetic

    def copy(self):
        """
        Copy the car

        Return:
            Car: copy of the car
        """
        return Car(genetic=self.genetic)

    def move(self):
        """
        Move the car and update its state depending on its genetic and environment
        """
        self.update_score()  # Update the score of the car

        wall_left, wall_top, wall_right = self.detect_walls()  # Detect if there is wall in the detection cone of the car

        self.update_acceleration(wall_top)  # Change the acceleration of the car depending on the detected walls
        self.update_speed()  # Update the speed of the car depending on the acceleration of the car

        turn_angle = self.update_angle(wall_left, wall_right)  # Change the speed and the angle of the car depending on the detected walls
        self.update_drift_angle(turn_angle)  # Update the drift angle of the car

        self.update_pos()  # Update the position and orientation of the car
        self.detect_collision()  # Detect if the car is dead

        self.detect_reverse()  # Detect if the car is going in the wrong way
        self.update_best_scores()  # Update the best scores of the car

    def update_score(self):
        """
        Update the score of the car depending on the map and the checkpoints reached
        """
        if var.NUM_MAP == 5:  # This map is a waiting room where the car just have to drive the longest distance possible
            self.score += self.speed  # Increment the score of the car
        else:
            self.detect_checkpoint()  # Detect if the car has reached a checkpoint

    def detect_checkpoint(self):
        """
        Detect if the car has reached a checkpoint or multiple checkpoints recursively
        """
        checkpoint_found = False  # True if the car has passed a checkpoint
        actual_checkpoint = var.CHECKPOINTS[self.next_checkpoint]  # Actual checkpoint to reach
        if checkpoint_reached(self.front_of_car, actual_checkpoint):  # If the car has passed a checkpoint
            self.score += 1
            self.next_checkpoint += 1
            self.turn_without_checkpoint = -1
            checkpoint_found = True
            if self.next_checkpoint == len(var.CHECKPOINTS):
                self.next_checkpoint = 0

        if checkpoint_found:   # If the car has passed a checkpoint, we check if it has passed multiple checkpoints
            self.detect_checkpoint()
        else:
            self.turn_without_checkpoint += 1

    def detect_walls(self):
        """
        Detect if there is wall in the detection cone of the car
        For each direction, it returns a bool value if there is a wall or not, or the distance between the front of the
         car and the wall in this direction if there is a wall

        Returns:
            bool or float: Detection of the wall at the left of the cone
            bool or float: Detection of the wall at the top of the cone
            bool or float: Detection of the wall at the right of the cone
        """
        width, length = self.determine_size_cone()  # We select the right cone depending on the speed of the car
        self.front_of_car = self.compute_front_of_car()  # Point at the front of the car
        left, top, right = compute_detection_cone_points(self.angle, self.front_of_car, width, length)  # Points of the detection cone (represented by a triangle)

        return self.detect_wall(left), self.detect_wall(top), self.detect_wall(right)

    def detect_wall(self, point):
        """
        Detect if there is a wall between the front of the car and the point (it's in this function that we are taking
         most of the time in the simulation)

        Args:
            point (tuple(int, int)): the coordinates of the point

        Returns:
            bool or float : True if there is a wall
            If it is a float, it is the distance between the front of the car and the wall in this direction
        """
        x1, y1 = self.front_of_car  # Coordinates of the front of the car
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
                return math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)  # We return the distance between the front of the car and the wall
        return False  # There is no wall

    def determine_size_cone(self):
        """
        Determine the size of the detection cone according to the speed of the car

        Returns:
            width, length (int, int): the width and the length of the detection cone
        """
        if self.speed < var.MIN_MEDIUM_SPEED:
            width = self.genetic.width_slow()
            length = self.genetic.length_slow()
        elif self.speed < var.MIN_HIGH_SPEED:
            width = self.genetic.width_medium()
            length = self.genetic.length_medium()
        else:
            width = self.genetic.width_fast()
            length = self.genetic.length_fast()

        return width, length

    def compute_front_of_car(self):
        """
        Compute the coordinates of the front of the car
        Args:

        Returns:
            front_of_car (tuple(int, int)): the coordinates of the front of the car
        """
        return self.pos[0] + math.cos(math.radians(-self.angle)) * self.image.get_width() / 2,\
            self.pos[1] + math.sin(math.radians(-self.angle)) * self.image.get_width() / 2

    def update_acceleration(self, wall_top):
        """
        Change the acceleration of the car (depending on the genetic cone)
        If there is a wall in front of the car, we decelerate it
        Furthermore, if the car is going in the wrong way, we accelerate it

        Args:
            wall_top (bool or float) : True if there is a wall
            If it is a float, it is the distance between the front of the car and the wall in this direction
        """
        if not wall_top or self.reverse:  # We don't brake if the car is going backwards
            self.acceleration = var.ACCELERATION
        else:
            self.acceleration -= var.DECELERATION

    def update_speed(self):
        """
        Change the speed of the car depending on the acceleration of the car
        We make sure that the speed of the car is between MIN_SPEED and MAX_SPEED
        """
        self.speed += self.acceleration  # Update the speed of the car

        # Limit the speed of the car (between MIN_SPEED and MAX_SPEED)
        self.speed = max(min(self.speed, var.MAX_SPEED), min_speed)

    def update_angle(self, wall_left, wall_right):
        """
        Change the angle of the car depending on the genetic cone
        If the closest wall is on the left of the car, we turn it to the right, and vice versa
        The angle of turn is different depending on the speed of the car (the faster the car goes, the less it turns)
        We don't turn the car if it is going backward

        Args:
            wall_left (bool or float): True if there is a wall at the left
            wall_right (bool or float) : True if there is a wall at the right
            If it is a float, it is the distance between the front of the car and the wall in this direction

        Return:
            float: angle of the turn of the car in this iteration
        """
        if self.speed == 0:  # To avoid division by 0
            turn_angle = var.TURN_ANGLE
        else:
            # When at high speed, the car turns 'turn_decrease_factor' times slower
            turn_angle = min(var.TURN_ANGLE, var.TURN_ANGLE * var.MAX_SPEED / (turn_decrease_factor * self.speed))  # Angle of the turn of the car

        if not wall_left and not wall_right:
            turn_angle = 0  # We don't turn the car if there is no wall
        elif wall_left:
            if wall_right:  # In the case where there is a wall on the left and on the right, we turn the car in the direction where there is the most space
                if wall_left < wall_right:
                    turn_angle = -turn_angle
            else:  # The case where there is only a wall on the left
                turn_angle = -turn_angle  # We modify the angle of the turn of the car to turn it to the right
        # elif wall_right: we don't need to do anything because the car is already turning to the left

        if not self.reverse:  # We don't turn the car if it is going backward
            self.angle += turn_angle

        return turn_angle

    def update_drift_angle(self, turn_angle):
        """
        Update the drift angle of the car depending on the angle of the car and the turn angle
        The speed of the car is applied in the drift angle, and the direction of the car is applied in the angle of the car

        Args:
            turn_angle (float): angle of the turn of the car in this turn
        """
        # If the drift angle is different from the angle of the car, we change it to be closer to the angle of the car
        if not math.isclose(self.drift_angle, self.angle):  # It's float values, so it's better not to use the == operator
            # If it can be done in one turn, we make the drift angle equals to the angle of the car
            if self.angle - add_to_speed_angle < self.drift_angle < self.angle + add_to_speed_angle:
                self.drift_angle = self.angle
            # If it can't be done in one turn, we approach the good value
            elif self.drift_angle > self.angle:
                self.drift_angle -= add_to_speed_angle
            else:
                self.drift_angle += add_to_speed_angle

        self.drift_angle += turn_angle / var.DRIFT_FACTOR

    def update_pos(self):
        """
        Update the position and angle of the car, update its image and rectangle
        """
        # Update the position of the car
        radians = math.radians(-self.drift_angle)  # Convert the angle to radians
        self.pos = self.pos[0] + math.cos(radians) * self.speed, self.pos[1] + math.sin(radians) * self.speed
        self.front_of_car = self.compute_front_of_car()

        # Rotate the car
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image of the car
        self.rotated_rect = self.rotated_image.get_rect(center=self.image.get_rect(center=self.pos).center)  # Rotate the rectangle of the car

    def detect_collision(self):
        """
        Detect collision of the car with the walls
        """
        if self.pos[0] < 0 or self.pos[0] > 1500 or self.pos[1] < 0 or self.pos[1] > 700:
            self.kill()  # Collision with the wall of the window

        if var.BACKGROUND_MASK.overlap(pygame.mask.from_surface(self.rotated_image), self.rotated_rect.topleft) is not None:
            # This part was used to avoid determinism problems, it seems to work now, but we never know
            """
            # We move the car backward because we don't want the car to bo on top of the wall
            speed = 1  # Speed of the car
            radians = math.radians(-self.speed_angle)  # Convert the angle to radians
            dx = math.cos(radians) * speed  # The movement of the car on the x-axis
            dy = math.sin(radians) * speed  # The movement of the car on the y-axis
            # While it touches the wall
            count = 0
            while var.BACKGROUND_MASK.overlap(car_mask, self.rotated_rect.topleft) is not None:
                count += 1
                if count == 20:  # To avoid a car teleporting we try to move in the other direction (to avoid the case when the back of the car is in the wall)
                    dx = -dx
                    dy = -dy

                self.pos = self.pos[0] - dx, self.pos[1] - dy  # Update the position of the car
                self.rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image of the car
                self.rotated_rect = self.rotated_image.get_rect(center=self.image.get_rect(center=self.pos).center)  # Rotate the rectangle of the car
                car_mask = pygame.mask.from_surface(self.rotated_image)
            """
            self.kill()  # Collision with a wall

    def detect_reverse(self):
        """
        Detect if the car is going in the wrong way in order to make it stop driving
        """
        # If we are in a circuit and the car is going backwards, we change its color and reverse variable
        if var.NUM_MAP != 5 and self.turn_without_checkpoint > 150 and not self.reverse:
            if self.id_memory_car is None and not self.color == 'yellow':
                # We convert the image of the car to light grayscale if it's not the best car (to show that it's going in the wrong way)
                self.image = change_color_car(self.image, 'light_gray')
            self.reverse = True

    def update_best_scores(self):
        """
        Update the best scores of the car if we reached a new best score
        """
        if self.score > self.best_scores[var.NUM_MAP]:
            self.best_scores[var.NUM_MAP] = self.score

    def draw(self, surface=var.WINDOW):
        """
        Draw the car on the window or on the background

        Args:
            surface (pygame.Surface): surface on which we draw the car (default: the window of the game)
        """
        image_shown = scale_image(self.rotated_image, var.SCALE_RESIZE_X)  # Scale the image of the car
        self.rotated_rect_shown = image_shown.get_rect(center=convert_to_new_window(self.pos))  # Rotate the rectangle of the car
        surface.blit(image_shown, self.rotated_rect_shown)  # We display the car
        var.RECTS_BLIT_CAR.append(self.rotated_rect_shown)    # Draw the car and add the rect to the list

        if var.SHOW_DETECTION_CONES:
            self.draw_detection_cone()  # Draw the detection cone of the car

    def draw_detection_cone(self):
        """
        Draw the 3 detection cones of the car, the cone which is currently used is bigger than the others
        """
        if self.speed < var.MIN_MEDIUM_SPEED:
            actual_mode = 'slow'
        elif self.speed > var.MIN_HIGH_SPEED:
            actual_mode = 'fast'
        else:
            actual_mode = 'medium'

        # We draw the detection cone
        points_detection_cone = draw_detection_cone(pos=self.front_of_car, dice_values=self.genetic.dice_values, angle=self.angle, actual_mode=actual_mode)
        var.RECTS_BLIT_CAR.append(create_rect_from_points(points_detection_cone))  # Add the rect of the cones to the list to blit it

    def reset(self):
        """
        Reset the car
        """
        self.__init__(genetic=self.genetic, best_scores=self.best_scores, color=self.color, id_memory_car=self.id_memory_car)

    def kill(self):
        """
        Kill the car
        """
        self.dead = True  # The car is dead
        var.NB_CARS_ALIVE -= 1  # Decrease the number of cars alive
        self.draw(var.BACKGROUND)  # Draw the car on the background so it stays
        if var.SHOW_EXPLOSIONS:
            var.EXPLOSIONS.add(Explosion(self.pos))  # Add an explosion at the position of the car



def add_garage_cars(cars):
    """
    Add the cars from the garage to the list of cars
    """
    for memory_car in var.SELECTED_MEMORY_CARS:
        cars.append(Car(genetic=memory_car.genetic, best_scores=memory_car.best_scores, color=memory_car.color, id_memory_car=memory_car.id))  # Add cars from the garage to the list
    return cars
