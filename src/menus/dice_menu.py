from src.data.constants import RGB_VALUES_DICE, PATH_IMAGE, START_POSITIONS  # Import the constants
from src.other.utils import convert_to_new_window, scale_image  # Import the convert_to_new_window function
from src.render.display import draw_detection_cone, draw_dice  # Import the display functions
from src.game.genetic import Genetic  # Import the genetic class
from src.render.button import Button  # Import the button class
import src.data.variables as var  # Import the data
import pygame  # Import pygame module


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
        self.type_car = None  # Type of the car ("dice" or "genetic")
        self.dice_values = None  # Values of the dice
        self.id_car = None  # Id of the dice
        self.by_camera = None  # True if the dice menu is called by the camera, False if we are modifying the dice
        self.rect = None  # Rectangle of the dice menu
        self.rect_x = None  # The x coordinate of the rectangle
        self.rect_y = None  # The y coordinate of the rectangle
        self.writing_buttons = None  # List of the rectangles to write the text
        self.check_button = None  # List of the check buttons

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

        return Button(x=self.rect_x + x + 45, y=self.rect_y + y + 140, image_name='writing', variable=value, name='dice', scale_x=0.25)

    def init(self, type_car, scores, id_car=None, by_camera=False):
        """
        Initialize the dice menu during the game

        Args:
            type_car (str): Type of the dice ("dice" or "genetic")
            scores (list): List of the scores of the dice
            id_car (int): Id of the dice
            by_camera (bool): True if the dice menu is called by the camera, False if we are modifying the dice
        """
        self.type_car = type_car
        self.dice_values = scores
        self.id_car = id_car
        self.by_camera = by_camera

        if self.by_camera:  # By camera
            self.rect = pygame.rect.Rect(convert_to_new_window((480, 125, 1000, 550)))  # From camera
            self.rect_x = 480  # The x coordinate of the rectangle before the conversion
            self.rect_y = 125  # The y coordinate of the rectangle before the conversion
        else:    # By garage
            self.rect = pygame.rect.Rect(convert_to_new_window((300, 125, 1000, 550)))  # From garage
            self.rect_x = 300
            self.rect_y = 125

        self.writing_buttons = [self.dice_button(x1, y1, self.dice_values[0]), self.dice_button(x2, y1, self.dice_values[1]),
                                self.dice_button(x3, y1, self.dice_values[2]), self.dice_button(x1, y2, self.dice_values[3]),
                                self.dice_button(x2, y2, self.dice_values[4]), self.dice_button(x3, y2, self.dice_values[5])]

        self.check_button = Button(x=self.rect_x + 888, y=self.rect_y + 445, image_name='check', scale=0.4)

    def display_dice_menu(self):
        """
        To display the dice menu

        Returns:
            bool: True if the user has validated the value of the dice
        """
        # We display the window
        pygame.draw.rect(var.WINDOW, (128, 128, 128), self.rect, 0)  # Display the background
        pygame.draw.rect(var.WINDOW, (1, 1, 1), self.rect, 2)  # Display the border

        var.WINDOW.blit(var.TEXT_SLOW, (convert_to_new_window((self.rect_x + x1 + 30, self.rect_y + 50))))
        var.WINDOW.blit(var.TEXT_MEDIUM, (convert_to_new_window((self.rect_x + x2 + 14, self.rect_y + 50))))
        var.WINDOW.blit(var.TEXT_FAST, (convert_to_new_window((self.rect_x + x3 + 14, self.rect_y + 50))))
        var.WINDOW.blit(var.TEXT_LENGTH, (convert_to_new_window((self.rect_x + 20, self.rect_y + 350))))
        var.WINDOW.blit(var.TEXT_WIDTH, (convert_to_new_window((self.rect_x + 30, self.rect_y + 160))))

        x, y = self.rect_x + 750, self.rect_y + 275
        var.WINDOW.blit(scale_image(var.BIG_RED_CAR_IMAGE, var.SCALE_RESIZE_X), (convert_to_new_window((x, y))))
        draw_detection_cone((x + 52, y - 3), self.dice_values, factor=3, width_line=5)

        # Display the dice
        draw_dice(x=self.rect_x + x1, y=self.rect_y + y1, color=RGB_VALUES_DICE[0], value=self.dice_values[0])
        draw_dice(x=self.rect_x + x2, y=self.rect_y + y1, color=RGB_VALUES_DICE[1], value=self.dice_values[1])
        draw_dice(x=self.rect_x + x3, y=self.rect_y + y1, color=RGB_VALUES_DICE[2], value=self.dice_values[2])
        draw_dice(x=self.rect_x + x1, y=self.rect_y + y2, color=RGB_VALUES_DICE[3], value=self.dice_values[3], black_dots=True)
        draw_dice(x=self.rect_x + x2, y=self.rect_y + y2, color=RGB_VALUES_DICE[4], value=self.dice_values[4])
        draw_dice(x=self.rect_x + x3, y=self.rect_y + y2, color=RGB_VALUES_DICE[5], value=self.dice_values[5])

        # Display the buttons
        for index, writing_button in enumerate(self.writing_buttons):
            writing_button.draw()
            if writing_button.just_clicked:  # We erase the value of the dice if the user has clicked on the button
                self.writing_buttons[index].text = ''

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
            var.MEMORY_CARS.get('dice').append([var.ACTUAL_ID_MEMORY_DICE, 'Dé_' + str(var.ACTUAL_ID_MEMORY_DICE),
                                                Genetic(self.dice_values), 'gray', [0] * len(START_POSITIONS)])  # We add the dice to the memory
            var.ACTUAL_ID_MEMORY_DICE += 1  # We increment the id of the dice

    def save_values(self, index, writing_button):
        """
        To save the values of the dice in case we are editing a dice from the memory

        Args:
            index (int): Index of the dice in the memory
            writing_button (Button): Button to write the value of the dice
        """
        self.dice_values[index] = writing_button.variable

        if not self.by_camera:
            for car in var.MEMORY_CARS.get(self.type_car):
                if car[0] == self.id_car:
                    car[2] = Genetic(self.dice_values)


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


DICE_MENU = DiceMenu()   # We create the dice menu