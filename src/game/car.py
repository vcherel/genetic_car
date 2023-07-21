from src.other.utils import compute_detection_cone_points, point_out_of_window, create_rect_from_points, scale_image, convert_to_new_window, change_color_car  # Utils functions
from src.render.display import draw_detection_cone  # To draw the detection cone
from src.data.constants import START_POSITIONS  # Start positions of the cars
from src.game.genetic import Genetic  # Genetic algorithm of the car
from src.render.explosion import Explosion  # To render explosions
import src.data.variables as var  # Variables of the game
import pygame  # Pygame library
import math  # Math library

"""
This file contains the class Car used to represent a car in the game. The car is controlled by genetic parameters of the detection cone.
"""

# Constants
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
            genetic (Genetic): genetic of the car to copy (if None, create a new genetic)
            best_scores (list): list of the best scores of the car for each map
            color (str): color of the car
            id_memory_car (int): id of the car in the memory (it means the car is in view only mode)
        """
        if genetic is None:
            self.genetic = Genetic()  # Genetic of the car
        else:
            self.genetic = genetic.copy()  # Genetic of the car


        self.speed = 0  # Current speed of the car
        self.acceleration = 0  # Current acceleration of the car

        self.angle = 0  # Current angle of the car
        self.drift_angle = 0  # Current speed angle of the car (when the car turns the angle change but the speed angle turns slower)

        self.pos = var.START_POSITION  # Current position of the car
        self.front_of_car = self.pos  # Current position of the front of the car

        self.image = change_color_car(var.RED_CAR_IMAGE, color)  # Image of the car but grey
        self.color = color  # Color of the car

        self.rotated_image = self.image  # Rotated image of the car
        self.rotated_rect = self.image.get_rect()  # Rotated rectangle of the car
        self.rotated_rect_shown = self.image.get_rect()  # Rotated rectangle of the car shown on the screen

        self.next_checkpoint = 0  # Next checkpoint to reach
        self.turn_without_checkpoint = 0  # Number of turn played by the car without reaching a checkpoint

        self.dead = False  # True if the car is dead, False otherwise
        self.reverse = False  # True if the car is going in the wrong way, False otherwise

        self.id_memory_car = id_memory_car  # Id of the car in the memory (it means the car is in view only mode)

        self.score = 0  # Score of the car
        if best_scores:
            self.best_scores = best_scores
        else:
            self.best_scores = [0] * len(START_POSITIONS)  # Best scores of the car

    def __str__(self):
        """
        Return the string representation of the car

        Return:
            str: string representation of the car
        """
        return f'Car: genetic : {self.genetic} ; color : {self.color} ; position : {self.pos} ; angle : {self.angle} ; speed : {self.speed} ; acceleration : {self.acceleration} ; scores : {self.score}'

    def __eq__(self, other):
        """
        Test the equality between the car and the other car, two cars are equal if they have the same genetic

        Args:
            other (Car): other car to compare

        Return:
            bool: True if the car is equal to the other car, False otherwise
        """
        return self.genetic == other.genetic

    def copy(self):
        """
        Copy the car

        Return:
            Car: copy of the car
        """
        return Car(self.genetic.copy(), self.best_scores, self.color, self.id_memory_car)

    def move(self):
        """
        Move the car and update its state
        """
        if var.NUM_MAP == 5:  # This map is a waiting room where the car just have to drive the longest distance possible
            self.score += self.speed  # Increment the score of the car
        else:
            self.detect_checkpoint()  # Detect if the car has reached a checkpoint

        wall_left, wall_top, wall_right = self.detect_walls()  # Detect if there is wall in the detection cone of the car
        self.update_acceleration(wall_top)  # Change the acceleration of the car depending on the detected walls
        turn_angle = self.update_angle(wall_left, wall_right)  # Change the speed and the angle of the car depending on the detected walls
        self.update_drift_angle(turn_angle)  # Update the drift angle of the car
        self.update_speed()  # Update the speed of the car
        self.update_pos()  # Update the position and orientation of the car
        self.detect_collision()  # Detect if the car is dead

        # If we are in a circuit and the car is going backwards, we force it to go in the wall
        if var.NUM_MAP != 5 and self.turn_without_checkpoint > 150 and not self.reverse:
            if self.id_memory_car is None and not self.color == 'yellow':
                self.image = change_color_car(self.image, 'light_gray')  # We convert the image of the car to light grayscale if it's a red car
            self.reverse = True

        # We update the best scores of the car
        if self.score > self.best_scores[var.NUM_MAP]:
            self.best_scores[var.NUM_MAP] = self.score

    def detect_checkpoint(self):
        """
        Detect if the car has reached a checkpoint (or multiple checkpoints)

        Return:
            bool: True if the car has reached a checkpoint, False otherwise
        """
        checkpoint_passed = False  # True if the car has passed a checkpoint, False otherwise
        actual_checkpoint = var.CHECKPOINTS[self.next_checkpoint]  # Actual checkpoint to reach
        if actual_checkpoint[0] - var.RADIUS_CHECKPOINT < self.pos[0] < actual_checkpoint[0] + var.RADIUS_CHECKPOINT and\
                actual_checkpoint[1] - var.RADIUS_CHECKPOINT < self.pos[1] < actual_checkpoint[1] + var.RADIUS_CHECKPOINT:
            self.score += 1
            self.next_checkpoint += 1
            self.turn_without_checkpoint = -1
            checkpoint_passed = True
            if self.next_checkpoint == len(var.CHECKPOINTS):
                self.next_checkpoint = 0

        if checkpoint_passed:   # If the car has passed a checkpoint, we check if it has passed multiple checkpoints
            self.detect_checkpoint()
        else:
            self.turn_without_checkpoint += 1

    def detect_walls(self):
        """
        Detect if there is wall in the detection cone of the car, and return boolean values depending on the presence
        of wall at the left top and right of the cone

        Returns:
            bool: True if there is a wall at the left of the cone, False otherwise
            bool: True if there is a wall at the top of the cone, False otherwise
            bool: True if there is a wall at the right of the cone, False otherwise
        """
        width, length = self.determine_size_cone()  # We select the right cone depending on the speed of the car
        self.front_of_car = self.compute_front_of_car()  # Point at the front of the car
        left, top, right = compute_detection_cone_points(self.angle, self.front_of_car, width, length)  # Points of the detection cone (represented by a triangle)

        return self.detect_wall(left), self.detect_wall(top), self.detect_wall(right)

    def update_acceleration(self, wall_top):
        """
        Change the acceleration of the car (depending on the genetic cone)
        If there is a wall in front of the car, we decelerate it

        Args:
            wall_top (bool or float) : True if there is a wall, False otherwise
            If it is a float, it is the distance between the front of the car and the wall in this direction
        """
        if not wall_top or self.reverse:  # We don't brake if the car is going backwards
            self.acceleration = var.ACCELERATION
        else:
            self.acceleration -= var.DECELERATION

    def update_angle(self, wall_left, wall_right):
        """
        Change the angle of the car depending on the genetic cone
        If the closest wall is on the left of the car, we turn it to the right, and vice versa
        We also change the drift angle of the car depending on the angle of the car

        Args:
            wall_left (bool or float): True if there is a wall at the left, False otherwise
            wall_right (bool or float) : True if there is a wall at the right, False otherwise
            If it is a float, it is the distance between the front of the car and the wall in this direction

        Return:
            float: angle of the turn of the car in this turn
        """
        # The angle of turn is different depending on the speed of the car (the faster the car goes, the less it turns)
        if self.speed == 0:  # To avoid division by 0
            turn_angle = var.TURN_ANGLE
        else:
            # When at high speed, the car turns 'turn_decrease_factor' times slower
            turn_angle = min(var.TURN_ANGLE, var.TURN_ANGLE * var.MAX_SPEED / (turn_decrease_factor * self.speed))  # Angle of the turn of the car
        
        # If there is a wall on the left or on the right of the car, we turn it (if there is a wall on the left and on the right, we turn the car in the direction where there is the most space)
        if not wall_left and not wall_right:
            turn_angle = 0  # We don't turn the car if there is no wall
        elif wall_left:
            if wall_right:  # In the case where there is a wall on the left and on the right, we turn the car in the direction where there is the most space
                if wall_left < wall_right:
                    turn_angle = -turn_angle
            else:  # The case where there is only a wall on the left
                turn_angle = -turn_angle

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
        if not math.isclose(self.drift_angle, self.angle):
            # If it can be done in one turn, we do it exactly
            if self.angle - add_to_speed_angle < self.drift_angle < self.angle + add_to_speed_angle:
                self.drift_angle = self.angle
            # If it can't be done in one turn, we approach the good value
            elif self.drift_angle > self.angle:
                self.drift_angle -= add_to_speed_angle
            else:
                self.drift_angle += add_to_speed_angle

        if not self.reverse:  # We don't change the drift angle if the car is going backward because it is not turning anymore
            self.drift_angle += turn_angle / var.DRIFT_FACTOR

    def update_speed(self):
        """
        Change the speed of the car depending on the acceleration of the car
        """
        self.speed += self.acceleration  # Update the speed of the car

        # Limit the speed of the car (between MIN_SPEED and MAX_SPEED)
        self.speed = max(min(self.speed, var.MAX_SPEED), min_speed)

    def update_pos(self):
        """
        Update the position of the car
        """
        # Move the car
        if var.DO_DRIFT:
            radians = math.radians(-self.drift_angle)  # Convert the angle to radians
        else:
            radians = math.radians(-self.angle)
        dx = math.cos(radians) * self.speed  # The movement of the car on the x-axis
        dy = math.sin(radians) * self.speed  # The movement of the car on the y-axis
        self.pos = self.pos[0] + dx, self.pos[1] + dy  # Update the position of the car
        self.front_of_car = self.compute_front_of_car()  # Update the position of the front of the car

        # Rotate the car
        self.rotated_image = pygame.transform.rotate(self.image, self.angle)  # Rotate the image of the car
        self.rotated_rect = self.rotated_image.get_rect(center=self.image.get_rect(center=self.pos).center)  # Rotate the rectangle of the car

    def detect_collision(self):
        """
        Detect collision of the car with the walls
        """
        if self.pos[0] < 0 or self.pos[0] > 1500 or self.pos[1] < 0 or self.pos[1] > 700:
            self.kill()  # Collision with the wall of the window

        car_mask = pygame.mask.from_surface(self.rotated_image)

        
        if var.BACKGROUND_MASK.overlap(car_mask, self.rotated_rect.topleft) is not None:
            # This part was used to avoid determinism problems
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

    def determine_size_cone(self):
        """
        Determine the size of the detection cone according to the speed of the car

        Returns:
            width, length (int, int): the width and the length of the detection cone
        """
        if self.speed < var.MIN_MEDIUM_SPEED:
            width = self.genetic.width_slow
            length = self.genetic.length_slow
        elif self.speed < var.MIN_HIGH_SPEED:
            width = self.genetic.width_medium
            length = self.genetic.length_medium
        else:
            width = self.genetic.width_fast
            length = self.genetic.length_fast
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

    def kill(self):
        """
        Kill the car
        """
        self.dead = True  # The car is dead
        var.NB_CARS_ALIVE -= 1  # Decrease the number of cars alive
        self.draw(var.BACKGROUND)  # Draw the car on the background so it stays
        if var.SHOW_EXPLOSIONS:
            var.EXPLOSIONS.add(Explosion(self.pos))  # Add an explosion  # at the position of the car

    def draw(self, surface=var.WINDOW):
        """
        Draw the car
        """
        image_shown = scale_image(self.rotated_image, var.SCALE_RESIZE_X)  # Scale the image of the car
        self.rotated_rect_shown = image_shown.get_rect(center=convert_to_new_window(self.pos))  # Rotate the rectangle of the car
        surface.blit(image_shown, self.rotated_rect_shown)  # We display the car
        var.RECTS_BLIT_CAR.append(self.rotated_rect_shown)    # Draw the car and add the rect to the list

        if var.DEBUG and not self.dead:
            self.draw_detection_cone()  # Draw the detection cone of the car

    def reset(self):
        """
        Reset the car
        """
        self.__init__(genetic=self.genetic, best_scores=self.best_scores, color=self.color, id_memory_car=self.id_memory_car)

    def draw_detection_cone(self):
        """
        Draw the 3 detection cones of the car
        """
        if self.speed < var.MIN_MEDIUM_SPEED:
            actual_mode = 'slow'
        elif self.speed > var.MIN_HIGH_SPEED:
            actual_mode = 'fast'
        else:
            actual_mode = 'medium'

        # We draw the detection cone
        points_detection_cone = draw_detection_cone(self.front_of_car, self.genetic.dice_values, self.angle, actual_mode=actual_mode)
        var.RECTS_BLIT_CAR.append(create_rect_from_points(points_detection_cone))  # Add the rect of the cones to the list to blit it

    def change_color(self, color):
        """
        Change the color of the car

        Args:
            color (str): the new color of the car
        """
        self.color = color


    def detect_wall(self, point):
        """
        Detect if there is a wall between the front of the car and the point

        Args:
            point (tuple(int, int)): the coordinates of the point

        Returns:
            bool or float : True if there is a wall, False otherwise
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
