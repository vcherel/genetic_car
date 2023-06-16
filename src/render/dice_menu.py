from src.render.display import display_text_ui, draw_detection_cone  # Import the display functions
from src.game.constants import HEIGHT_MULTIPLIER, WIDTH_MULTIPLIER  # Import the constants
from src.render.button import Button  # Import the button class
from src.game.genetic import Genetic  # Import the genetic class
import src.other.variables as var  # Import the variables
import os.path  # To get the path of the images
import pygame  # Import pygame module


path_image = os.path.dirname(__file__) + '/../../images/'  # Path of the actual file

rgb_values = [(240, 170, 25), (255, 100, 0), (204, 0, 0), (0, 200, 0), (102, 0, 102), (0, 0, 0)]  # RGB values of the dice
# The order is: dark_yellow, orange, red, green, purple, black

# Positions of the dice
x1, x2, x3 = 90, 300, 510  # x coordinates of the dice
y1, y2 = 170, 365           # y coordinates of the dice

# Camera
camera_frame = pygame.image.load(path_image + '/nothing.png')  # Frame of the camera at the last update
rect_camera_frame = pygame.rect.Rect(0, 0, 0, 0)  # Rect of the camera frame

# Display
text_selected_dice = var.LARGE_FONT.render('Dés sélectionnés', True, (0, 0, 0), (128, 128, 128))  # Text of the selected dice



class DiceMenu:
    def __init__(self):
        """
        Initialize the dice menu (in the structures.py file)
        """
        self.type_car = None  # Type of the car ("dice" or "genetic")
        self.genetic = None  # Genetic corresponding to the dice
        self.by_camera = None  # True if the dice menu is called by the camera, False if we are modifying the dice
        self.rect = None  # Rectangle of the dice menu
        self.writing_rectangles = None  # List of the rectangles to write the text
        self.check_button = None  # List of the check buttons
        self.str_scores = None  # String of the scores of the dice
        self.text_scores = None  # Text of the scores of the dice
        self.bool_scores = None  # Boolean of the scores of the dice
        self.id_car = None  # Id of the dice

    def dice_button(self, x, y):
        """
        To create a dice button

        Args:
            x (int): x coordinate of the button
            y (int): y coordinate of the button

        Returns:
            Button: The dice button
        """

        return Button(self.rect[0] + x - 50, self.rect[1] + y + 140,
                      pygame.image.load(path_image + '/writing_rectangle_1.png'),
                      pygame.image.load(path_image + '/writing_rectangle_2.png'),
                      pygame.image.load(path_image + '/writing_rectangle_3.png'), writing_rectangle=True, scale=0.9)

    def init(self, type_car, id_car=None, dict_scores=None, genetic=None):
        """
        Initialize the dice menu during the game

        Args:
            type_car (str): Type of the dice ("dice" or "genetic")
            id_car (int): Id of the dice
            dict_scores (dict): Dictionary of the scores of the dice
            genetic (Genetic): Genetic corresponding to the dice
        """
        self.type_car = type_car
        self.id_car = id_car

        if genetic:
            self.genetic = genetic  # Genetic corresponding to the dice
            self.by_camera = False  # True if the dice menu is called by the camera
        else:
            self.genetic = Genetic(height_slow=dict_scores.get('dark_yellow'),
                                   height_medium=dict_scores.get('orange'),
                                   height_fast=dict_scores.get('red'),
                                   width_slow=dict_scores.get('green'),
                                   width_medium=dict_scores.get('purple'),
                                   width_fast=dict_scores.get('black'))
            self.by_camera = True

        if dict_scores:
            self.rect = pygame.rect.Rect(500, 125, 1000, 550)
        else:
            self.rect = pygame.rect.Rect(200, 125, 1000, 550)

        # To store the buttons to write the score of each dice
        self.writing_rectangles = [self.dice_button(x1, y1), self.dice_button(x2, y1), self.dice_button(x3, y1),
                                   self.dice_button(x1, y2), self.dice_button(x2, y2), self.dice_button(x3, y2)]
        self.check_button = Button(self.rect[0] + 917, self.rect[1] + 460, pygame.image.load(path_image + '/check.png'), scale=0.12)

        self.str_scores = []  # To store the score of each dice (the number of dots on each dice in string format)
        self.text_scores = []  # To store the score of each dice (the number of dots on each dice in pygame text format)

        # We fill str_scores and text_scores
        for height in [self.genetic.height_slow, self.genetic.height_medium, self.genetic.height_fast]:
            number = height // HEIGHT_MULTIPLIER
            self.add_value(number)
        for width in [self.genetic.width_slow, self.genetic.width_medium, self.genetic.width_fast]:
            number = width // WIDTH_MULTIPLIER
            self.add_value(number)

        self.bool_scores = [False] * 6  # To store the boolean values of the dice buttons (are we actually changing the score or not)

    def add_value(self, number):
        str_number = str(number)
        self.str_scores.append(str_number)
        self.text_scores.append(var.FONT.render(str_number, True, (0, 0, 0), (255, 255, 255)))

    def draw_dice(self, x, y, index):
        """
        To draw a dice

        Args:
            x (int): x coordinate of the dice
            y (int): y coordinate of the dice
            index (int): Index of the dice (0 to 5)
        """

        pygame.draw.rect(var.WINDOW, rgb_values[index], (self.rect[0] + x, self.rect[1] + y, 120, 120), 0)
        pygame.draw.rect(var.WINDOW, (100, 100, 100), (self.rect[0] + x, self.rect[1] + y, 120, 120), 3)

        if not index:  # If the dice is dark_yellow the dots are black
            draw_dots(self.rect[0] + x, self.rect[1] + y, self.genetic.get_dice_value(index), (0, 0, 0))
        else:
            draw_dots(self.rect[0] + x, self.rect[1] + y, self.genetic.get_dice_value(index))

    def display_dice_menu(self):
        """
        To display the dice menu

        Returns:
            bool: True if the user has validated the value of the dice
        """
        # We display the window
        pygame.draw.rect(var.WINDOW, (128, 128, 128), self.rect, 0)  # Display the background
        pygame.draw.rect(var.WINDOW, (115, 205, 255), self.rect, 2)  # Display the border

        var.WINDOW.blit(text_selected_dice, (self.rect[0] + 350, self.rect[1] + 20))
        var.WINDOW.blit(var.TEXT_SLOW, (self.rect[0] + x1 + 30, self.rect[1] + 100))
        var.WINDOW.blit(var.TEXT_MEDIUM, (self.rect[0] + x2 + 14, self.rect[1] + 100))
        var.WINDOW.blit(var.TEXT_FAST, (self.rect[0] + x3 + 14, self.rect[1] + 100))

        x, y = self.rect[0] + 685, self.rect[1] + 290
        var.WINDOW.blit(var.RED_CAR_CONE, (x, y))
        draw_detection_cone((x + 125, y + 25), self.genetic, 2.5)


        # Display the dice
        self.draw_dice(x=x1, y=y1, index=0)
        self.draw_dice(x=x2, y=y1, index=1)
        self.draw_dice(x=x3, y=y1, index=2)
        self.draw_dice(x=x1, y=y2, index=3)
        self.draw_dice(x=x2, y=y2, index=4)
        self.draw_dice(x=x3, y=y2, index=5)

        # Display the buttons
        for index, button in enumerate(self.writing_rectangles):
            self.bool_scores[index] = button.check_state()
            if button.just_clicked:  # We erase the value of the dice if the user has clicked on the button
                self.str_scores[index] = ''

        for index, dice_bool in enumerate(self.bool_scores):
            if dice_bool:
                display_text_ui(self.str_scores[index], (self.writing_rectangles[index].x + 102, self.writing_rectangles[index].y + 6),
                                var.FONT, background_color=(255, 255, 255))
            else:
                var.WINDOW.blit(self.text_scores[index], (self.writing_rectangles[index].x + 102, self.writing_rectangles[index].y + 6))

        # Display the image of the last frame of the camera
        if self.by_camera:  # If we are modifying dice from the camera
            var.WINDOW.blit(camera_frame, (rect_camera_frame.x, rect_camera_frame.y))
            pygame.draw.rect(var.WINDOW, (115, 205, 255), rect_camera_frame, 2)

        # Display the button to validate the value of the dice
        self.check_button.check_state()

        return self.check_button.just_clicked

    def erase_dice_menu(self):
        """
        To erase the dice menu and save the value of the dice
        """
        var.DISPLAY_DICE_MENU = False  # We don't display the dice menu anymore
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)  # We erase the dice menu

        if self.by_camera:
            var.WINDOW.blit(var.BACKGROUND, rect_camera_frame, rect_camera_frame)  # We erase the dice menu
            var.MEMORY_CARS.get('dice').append((var.ACTUAL_ID_MEMORY_DICE, self.genetic))  # We add the dice to the memory
            var.ACTUAL_ID_MEMORY_DICE += 1  # We increment the id of the dice

    def save_values(self):
        """
        To save the values of the dice in case we are editing a dice from the memory
        """
        if not self.by_camera:
            for car in var.MEMORY_CARS.get(self.type_car):
                if car[0] == self.id_car:
                    var.MEMORY_CARS.get(self.type_car).remove(car)
                    break
            var.MEMORY_CARS.get(self.type_car).append((self.id_car, self.genetic))


def draw_dots(x, y, nb_dots, color=(255, 255, 255)):
    """
    To draw the dots on the dice

    Args:
        x (int): x coordinate of the dice
        y (int): y coordinate of the dice
        nb_dots (int): Number of dots on the dice
        color (tuple): Color of the dots. Defaults to (255, 255, 255).
    """
    dot_radius = 10
    dot_padding = 32
    position_dot = []

    # Calculate the positions of the dots based on the number of dots
    if nb_dots == 1:
        position_dot = [(x + 0.5 * 120, y + 0.5 * 120)]
    elif nb_dots == 2:
        position_dot = [(x + dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding)]
    elif nb_dots == 3:
        position_dot = [(x + dot_padding, y + dot_padding), (x + 0.5 * 120, y + 0.5 * 120),
                        (x + 120 - dot_padding, y + 120 - dot_padding)]
    elif nb_dots == 4:
        position_dot = [(x + dot_padding, y + dot_padding), (x + dot_padding, y + 120 - dot_padding),
                        (x + 120 - dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding)]
    elif nb_dots == 5:
        position_dot = [(x + dot_padding, y + dot_padding), (x + dot_padding, y + 120 - dot_padding),
                        (x + 120 - dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding),
                        (x + 0.5 * 120, y + 0.5 * 120)]
    elif nb_dots == 6:
        position_dot = [(x + dot_padding, y + dot_padding), (x + dot_padding, y + 120 - dot_padding),
                        (x + 120 - dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding),
                        (x + dot_padding, y + 0.5 * 120), (x + 120 - dot_padding, y + 0.5 * 120)]

    # Draw the dots on the dice
    for dot_pos in position_dot:
        pygame.draw.circle(var.WINDOW, color, dot_pos, dot_radius)


def save_camera_frame(frame):
    """
    We save the frame of the camera in variables (CAMERA_FRAME, RECT_CAMERA_FRAME) to display it on the screen
    """
    global camera_frame, rect_camera_frame

    frame = pygame.surfarray.make_surface(frame)  # Convert the camera frame to a surface
    # Resize, rotate and flip the camera frame
    frame = pygame.transform.scale(frame, (int(frame.get_width() * 0.8), int(frame.get_height() * 0.8)))
    frame = pygame.transform.rotate(frame, -90)
    camera_frame = pygame.transform.flip(frame, True, False)

    # Get the rectangle of the camera frame
    rect_camera_frame = camera_frame.get_rect()
    rect_camera_frame.x = 0
    rect_camera_frame.y = 200


DICE_MENU = DiceMenu()   # We create the dice menu
