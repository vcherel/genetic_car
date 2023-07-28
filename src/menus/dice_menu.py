from render.display import draw_detection_cone, draw_dice  # Import the display functions
from data.constants import RGB_VALUES_DICE, NB_MAPS  # Import the constants
from data.data_classes import MemoryCar  # Import the car memory
from game.genetic import Genetic  # Import the genetic class
from render.button import Button  # Import the button class
import data.variables as var  # Import the data
import pygame  # Import pygame module

from render.resizing import convert_to_new_window, scale_image

"""
This file contains the DiceMenu class used to display the dice menu and change the value of dice
"""


# Positions of the dice
x1, x2, x3 = 175, 355, 535  # x coordinates of the dice
y1, y2 = 120, 315           # y coordinates of the dice

# Camera
camera_frame = None  # Frame of the camera at the last update
rect_camera_frame = pygame.rect.Rect(0, 0, 0, 0)  # Rect of the camera frame


class DiceMenu:
    """
    This class is used to represent the dice menu that appears when we want to change the value of the parameters of a car
    """
    def __init__(self):
        """
        Initialize the dice menu
        """
        self.dice_values = None  # Values of the dice
        self.id_memory_car = None  # Id of the dice
        self.by_camera = None  # True if the dice menu is called by the camera, False if we are modifying the dice
        self.rect = None  # Rectangle of the dice menu
        self.x = self.y = None  # Coordinates of the dice menu
        self.values_button = None  # List of the rectangles to write the text
        self.check_button = None  # The button to validate the dice

    def init(self, values, id_memory_car=None, by_camera=False):
        """
        Initialize the dice menu during the game

        Args:
            values (list): List of the scores of the dice
            id_memory_car (int): Id of the memory car
            by_camera (bool): True if the dice menu is called by the camera, False if we are modifying the dice
        """
        self.dice_values = values
        self.id_memory_car = id_memory_car
        self.by_camera = by_camera

        if self.by_camera:  # By camera
            self.rect = pygame.rect.Rect(convert_to_new_window((480, 125, 1000, 550)))  # From camera
            self.x = 480  # The x coordinate of the rectangle before the conversion
            self.y = 125  # The y coordinate of the rectangle before the conversion
        else:    # By garage
            self.rect = pygame.rect.Rect(convert_to_new_window((300, 125, 1000, 550)))  # From garage
            self.x = 300
            self.y = 125

        self.values_button = [self.dice_button(x1, y1, self.dice_values[0]), self.dice_button(x2, y1, self.dice_values[1]),
                              self.dice_button(x3, y1, self.dice_values[2]), self.dice_button(x1, y2, self.dice_values[3]),
                              self.dice_button(x2, y2, self.dice_values[4]), self.dice_button(x3, y2, self.dice_values[5])]

        self.check_button = Button(x=self.x + 888, y=self.y + 445, image_name='check', scale=0.4)

    def dice_button(self, x, y, value):
        """
        To create a dice button

        Args:
            x (int): x coordinate of the button
            y (int): y coordinate of the button
            value (int): Value of the dice

        Returns:
            Button: The dice button
        """

        return Button(x=self.x + x + 45, y=self.y + y + 140, image_name='writing', variable=value, name='dice', scale_x=0.25)

    def display_dice_menu(self):
        """
        To display the dice menu

        Returns:
            bool: True if the user has validated the value of the dice
        """
        # We display the window
        pygame.draw.rect(var.WINDOW, (128, 128, 128), self.rect, 0)  # Display the background
        pygame.draw.rect(var.WINDOW, (1, 1, 1), self.rect, 2)  # Display the border

        # Display the texts
        var.WINDOW.blit(var.TEXT_SLOW, (convert_to_new_window((self.x + x1 + 30, self.y + 50))))
        var.WINDOW.blit(var.TEXT_MEDIUM, (convert_to_new_window((self.x + x2 + 14, self.y + 50))))
        var.WINDOW.blit(var.TEXT_FAST, (convert_to_new_window((self.x + x3 + 14, self.y + 50))))
        var.WINDOW.blit(var.TEXT_LENGTH, (convert_to_new_window((self.x + 22, self.y + 160))))
        var.WINDOW.blit(var.TEXT_WIDTH, (convert_to_new_window((self.x + 35, self.y + 350))))

        # Display the car
        x, y = self.x + 750, self.y + 275
        var.WINDOW.blit(scale_image(var.BIG_RED_CAR_IMAGE, var.SCALE_RESIZE_X), (convert_to_new_window((x, y))))
        draw_detection_cone((x + 52, y - 3), self.dice_values, factor=3, width_line=5)

        # Display the dice
        draw_dice(x=self.x + x1, y=self.y + y1, color=RGB_VALUES_DICE[0], value=self.dice_values[0])
        draw_dice(x=self.x + x2, y=self.y + y1, color=RGB_VALUES_DICE[1], value=self.dice_values[1])
        draw_dice(x=self.x + x3, y=self.y + y1, color=RGB_VALUES_DICE[2], value=self.dice_values[2])
        draw_dice(x=self.x + x1, y=self.y + y2, color=RGB_VALUES_DICE[3], value=self.dice_values[3], black_dots=True)
        draw_dice(x=self.x + x2, y=self.y + y2, color=RGB_VALUES_DICE[4], value=self.dice_values[4])
        draw_dice(x=self.x + x3, y=self.y + y2, color=RGB_VALUES_DICE[5], value=self.dice_values[5])

        # Display the buttons
        for index, writing_button in enumerate(self.values_button):  # Buttons to change the dice values
            writing_button.draw()
            if writing_button.just_clicked:  # We erase the value of the dice if the user has clicked on the button
                self.values_button[index].text = ''

        # Display the image of the last frame of the camera
        if self.by_camera and camera_frame is not None:  # If we are modifying dice from the camera
            var.WINDOW.blit(camera_frame, (rect_camera_frame.x, rect_camera_frame.y))
            pygame.draw.rect(var.WINDOW, (1, 1, 1), rect_camera_frame, 2)

        # Display the button to validate the value of the dice
        self.check_button.draw()

        return self.check_button.just_clicked

    def erase_dice_menu(self):
        """
        To erase the dice menu and save the value of the dice
        """
        var.DISPLAY_DICE_MENU = False  # We don't display the dice menu anymore
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)  # We erase the dice menu

        if self.by_camera:
            var.WINDOW.blit(var.BACKGROUND, rect_camera_frame, rect_camera_frame)  # We erase the dice menu
            var.MEMORY_CARS.append(MemoryCar(id_car=var.ACTUAL_IDS_MEMORY_CARS, name=f'Dé_{var.ACTUAL_IDS_MEMORY_CARS}',
                                   color='gray', genetic=Genetic(self.dice_values), best_scores=[0] * NB_MAPS))
            var.ACTUAL_IDS_MEMORY_CARS += 1  # We increment the id of the dice

    def save_values(self, index, writing_button):
        """
        To save the values of the dice in case we are editing a dice from the memory

        Args:
            index (int): Index of the dice in the memory
            writing_button (Button): Button to write the value of the dice
        """
        self.dice_values[index] = writing_button.variable

        if not self.by_camera:
            for memory_car in var.MEMORY_CARS:
                if memory_car.id == self.id_memory_car:
                    memory_car.genetic = Genetic(self.dice_values)


def update_pygame_camera_frame(frame):
    """
    Transform the openCV frame to a pygame frame and update the variables of the camera frame in the dice menu

    Args:
        frame (numpy.ndarray): Frame of the camera
    """
    global camera_frame, rect_camera_frame

    frame = pygame.surfarray.make_surface(frame)  # Convert the camera frame to a surface

    # Resize, rotate and flip the camera frame
    camera_frame = pygame.transform.flip(pygame.transform.rotate(pygame.transform.scale(frame, (int(frame.get_width() * 0.75), int(frame.get_height() * 0.75))), -90), True, False)

    # Get the rectangle of the camera frame
    rect_camera_frame = camera_frame.get_rect()
    rect_camera_frame.x, rect_camera_frame.y = 0, 200  # We place the camera frame in the window at the right place

    # Resize the camera frame to fit the window
    rect_camera_frame = pygame.rect.Rect(convert_to_new_window(rect_camera_frame))  # Convert the rectangle to the new window
    camera_frame = pygame.transform.scale(camera_frame, (rect_camera_frame.width, rect_camera_frame.height))  # Resize the camera frame


DICE_MENU = DiceMenu()  # Dice menu of the game