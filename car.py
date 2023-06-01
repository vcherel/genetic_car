import pygame  # Pygame library
import math  # Math library
from constants import WINDOW, MAX_SPEED, MIN_MEDIUM_SPEED, MIN_HIGH_SPEED, DECELERATION, ACCELERATION, WIDTH_SCREEN, HEIGHT_SCREEN, TURN_ANGLE, MIN_SPEED  # Constants of the game
from variables import BACKGROUND, BACKGROUND_MASK, DEBUG, KEYBOARD_CONTROL  # Variables of the game
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
        self.speed_state = "slow"  # Current speed state of the car
        self.acceleration = 0  # Current acceleration of the car

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
        self.speed_state = "slow"

        self.angle = 0
        self.pos = pos

        self.next_checkpoint = 0

    def move(self):
        """
        Move the car and update its state
        """

        self.change_speed_angle()  # Change the speed and the angle of the car (depending on the genetic cone)
        self.update_pos()  # Update the position and orientation of the car
        self.detect_collision()  # Detect if the car is dead and erase it if it is the case
        if DEBUG:
            self.draw_detection_cone()  # Draw the detection cone of the car

    def change_speed_angle(self):
        """
        Change the acceleration of the car (depending on the genetic cone)

        Return:
            float: acceleration of the car
        """
        # We select the right acceleration depending on the speed of the car
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

        front_of_car = self.pos[0] + math.cos(math.radians(-self.angle)) * self.image.get_width() / 2,\
            self.pos[1] + math.sin(math.radians(-self.angle)) * self.image.get_width() / 2  # Position of the front of the car
        angle_cone = math.degrees(math.atan(width / (2 * height)))  # Angle of the cone

        top = front_of_car[0] + math.cos(math.radians(self.angle)) * height,\
            front_of_car[1] - math.sin(math.radians(self.angle)) * height
        left = front_of_car[0] + math.cos(math.radians(self.angle + angle_cone)) * height,\
            front_of_car[1] - math.sin(math.radians(self.angle + angle_cone)) * height
        right = front_of_car[0] + math.cos(math.radians(self.angle - angle_cone)) * height,\
            front_of_car[1] - math.sin(math.radians(self.angle - angle_cone)) * height
        if DEBUG:
            pygame.draw.polygon(WINDOW, (0, 0, 255), (front_of_car, left, top, right), 3)

        # If the point top is outside the window or if the point top is on a black pixel of the background
        if top[0] <= 0 or top[0] >= WIDTH_SCREEN or top[1] <= 0 or top[1] >= HEIGHT_SCREEN or BACKGROUND.get_at((int(top[0]), int(top[1]))) == (0, 0, 0, 255):
            self.acceleration = DECELERATION  # The car decelerates
        else:
            self.acceleration = ACCELERATION  # Else the car accelerates

        if left[0] <= 0 or left[0] >= WIDTH_SCREEN or left[1] <= 0 or left[1] >= HEIGHT_SCREEN or BACKGROUND.get_at((int(left[0]), int(left[1]))) == (0, 0, 0, 255):
            self.angle -= TURN_ANGLE
        if right[0] <= 0 or right[0] >= WIDTH_SCREEN or right[1] <= 0 or right[1] >= HEIGHT_SCREEN or BACKGROUND.get_at((int(right[0]), int(right[1]))) == (0, 0, 0, 255):
            self.angle += TURN_ANGLE

    def update_pos(self):
        """
        Update the position and the angle of the car
        """
        if DEBUG and KEYBOARD_CONTROL:
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
        front_of_car = self.pos[0] + math.cos(math.radians(-self.angle)) * self.image.get_width() / 2,\
            self.pos[1] + math.sin(math.radians(-self.angle)) * self.image.get_width() / 2  # Position of the front of the car
        angle_cone = math.degrees(math.atan(self.genetic.width_slow / (2 * self.genetic.height_slow)))  # Angle of the cone

        # Slow detection cone
        # Compute angle of the cone with height and width of the cone
        top = front_of_car[0] + math.cos(math.radians(self.angle)) * self.genetic.height_slow,\
            front_of_car[1] - math.sin(math.radians(self.angle)) * self.genetic.height_slow
        left = front_of_car[0] + math.cos(math.radians(self.angle + angle_cone)) * self.genetic.height_slow,\
            front_of_car[1] - math.sin(math.radians(self.angle + angle_cone)) * self.genetic.height_slow
        right = front_of_car[0] + math.cos(math.radians(self.angle - angle_cone)) * self.genetic.height_slow,\
            front_of_car[1] - math.sin(math.radians(self.angle - angle_cone)) * self.genetic.height_slow
        pygame.draw.polygon(WINDOW, (255, 0, 0), (front_of_car, left, top, right), 1)

        # Medium detection cone
        top = front_of_car[0] + math.cos(math.radians(self.angle)) * self.genetic.height_medium,\
            front_of_car[1] - math.sin(math.radians(self.angle)) * self.genetic.height_medium
        left = front_of_car[0] + math.cos(math.radians(self.angle + angle_cone)) * self.genetic.height_medium,\
            front_of_car[1] - math.sin(math.radians(self.angle + angle_cone)) * self.genetic.height_medium
        right = front_of_car[0] + math.cos(math.radians(self.angle - angle_cone)) * self.genetic.height_medium,\
            front_of_car[1] - math.sin(math.radians(self.angle - angle_cone)) * self.genetic.height_medium
        pygame.draw.polygon(WINDOW, (0, 255, 0), (front_of_car, left, top, right), 1)

        # Fast detection cone
        top = front_of_car[0] + math.cos(math.radians(self.angle)) * self.genetic.height_fast,\
            front_of_car[1] - math.sin(math.radians(self.angle)) * self.genetic.height_fast
        left = front_of_car[0] + math.cos(math.radians(self.angle + angle_cone)) * self.genetic.height_fast,\
            front_of_car[1] - math.sin(math.radians(self.angle + angle_cone)) * self.genetic.height_fast
        right = front_of_car[0] + math.cos(math.radians(self.angle - angle_cone)) * self.genetic.height_fast,\
            front_of_car[1] - math.sin(math.radians(self.angle - angle_cone)) * self.genetic.height_fast
        pygame.draw.polygon(WINDOW, (0, 0, 255), (front_of_car, left, top, right), 1)
