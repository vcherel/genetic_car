import pygame  # Import pygame module
import variables as var  # Import the variables
from button import Button  # Import the button class
from genetic import Genetic  # Import the genetic class
from constants import HEIGHT_MULTIPLIER, WIDTH_MULTIPLIER  # Import the constants
from display import display_text_ui  # Import the display_text_ui function


rect_dice_menu = pygame.rect.Rect(0, 125, 1000, 550)  # Display rectangle of the dice menu
rgb_values = [(240, 170, 25), (255, 100, 0), (204, 0, 0), (0, 200, 0), (102, 0, 102), (0, 0, 0)]  # RGB values of the dice
# The order is: dark_yellow, orange, red, green, purple, black

# Positions of the dice
x1, x2, x3 = 120, 420, 720  # x coordinates of the dice
y1, y2 = 100, 325           # y coordinates of the dice


def dice_button(x, y):
    """
    To create a dice button

    Args:
        x (int): x coordinate of the button
        y (int): y coordinate of the button

    Returns:
        Button: The dice button
    """
    return Button(rect_dice_menu[0] + x - 50, rect_dice_menu[1] + y + 140, pygame.image.load("images/writing_rectangle_1.png"),
                  pygame.image.load("images/writing_rectangle_2.png"),
                  pygame.image.load("images/writing_rectangle_3.png"), writing_rectangle=True, scale=0.9)


def init_dice_variables(genetic=None):
    """
    To initialize the dice variables

    Args:
        genetic (Genetic) : the genetic of the car if we are loading a car from the garage menu
    """
    if genetic:   # If we are modifying dice from the garage
        rect_dice_menu[0] = 200
    else:
        rect_dice_menu[0] = 500

    var.DICE_BUTTONS = [dice_button(x1, y1), dice_button(x2, y1), dice_button(x3, y1),
                        dice_button(x1, y2), dice_button(x2, y2), dice_button(x3, y2)]

    var.BUTTON_CHECK = Button(rect_dice_menu[0] + 917, rect_dice_menu[1] + 460, pygame.image.load('images/check.png'), scale=0.12)

    for button in var.DICE_BUTTONS:
        button.activated = False

    if not genetic:
        var.DICE_VARIABLES = [var.ACTUAL_DICT_DICE.get('dark_yellow'), var.ACTUAL_DICT_DICE.get('orange'), var.ACTUAL_DICT_DICE.get('red'),
                              var.ACTUAL_DICT_DICE.get('green'), var.ACTUAL_DICT_DICE.get('purple'), var.ACTUAL_DICT_DICE.get('black')]
    else:
        var.DICE_VARIABLES = [genetic.height_slow // HEIGHT_MULTIPLIER, genetic.height_medium // HEIGHT_MULTIPLIER, genetic.height_fast // HEIGHT_MULTIPLIER,
                              genetic.width_slow // WIDTH_MULTIPLIER, genetic.width_medium // WIDTH_MULTIPLIER, genetic.width_fast // WIDTH_MULTIPLIER]

    var.DICE_STR_VARIABLES = []
    var.DICE_TEXTS = []
    for number in var.DICE_VARIABLES:
        str_number = str(number)
        var.DICE_STR_VARIABLES.append(str_number)
        var.DICE_TEXTS.append(var.FONT.render(str_number, True, (0, 0, 0), (255, 255, 255)))

    var.DICE_BOOLS = [False] * 6


def draw_dice(x, y, index):
    """
    To draw a dice

    Args:
        x (int): x coordinate of the dice
        y (int): y coordinate of the dice
        index (int): Index of the dice (0 to 5)
    """

    pygame.draw.rect(var.WINDOW, rgb_values[index], (rect_dice_menu[0] + x, rect_dice_menu[1] + y, 120, 120), 0)
    pygame.draw.rect(var.WINDOW, (100, 100, 100), (rect_dice_menu[0] + x, rect_dice_menu[1] + y, 120, 120), 3)

    if not index:   # If the dice is dark_yellow the dots are black
        draw_dots(rect_dice_menu[0] + x, rect_dice_menu[1] + y, var.DICE_VARIABLES[index], (0, 0, 0))
    else:
        draw_dots(rect_dice_menu[0] + x, rect_dice_menu[1] + y, var.DICE_VARIABLES[index])


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


def display_dice_menu():
    """
    To display the dice menu

    Returns:
        bool: True if the user has validated the value of the dice
    """
    # We display the window
    pygame.draw.rect(var.WINDOW, (128, 128, 128), rect_dice_menu, 0)
    pygame.draw.rect(var.WINDOW, (115, 205, 255), rect_dice_menu, 2)
    var.WINDOW.blit(var.LARGE_FONT.render('Dés sélectionnés', True, (0, 0, 0), (128, 128, 128)), (rect_dice_menu[0] + 350, rect_dice_menu[1] + 20))

    # Display the dice
    draw_dice(x=x1, y=y1, index=0)
    draw_dice(x=x2, y=y1, index=1)
    draw_dice(x=x3, y=y1, index=2)
    draw_dice(x=x1, y=y2, index=3)
    draw_dice(x=x2, y=y2, index=4)
    draw_dice(x=x3, y=y2, index=5)

    # Display the buttons
    for index, button in enumerate(var.DICE_BUTTONS):
        var.DICE_BOOLS[index] = button.check_state()
        if button.just_clicked:  # We erase the value of the dice if the user has clicked on the button
            var.DICE_STR_VARIABLES[index] = ''

    for index, dice_bool in enumerate(var.DICE_BOOLS):
        if dice_bool:
            display_text_ui(var.DICE_STR_VARIABLES[index], (var.DICE_BUTTONS[index].x + 102, var.DICE_BUTTONS[index].y + 6), var.FONT, background_color=(255, 255, 255))
        else:
            var.WINDOW.blit(var.DICE_TEXTS[index], (var.DICE_BUTTONS[index].x + 102, var.DICE_BUTTONS[index].y + 6))

    # Display the image of the last frame of the camera
    if not var.DICE_RECT_GARAGE:   # If we are modifying dice from the camera
        var.WINDOW.blit(var.CAMERA_FRAME, (var.RECT_CAMERA_FRAME.x, var.RECT_CAMERA_FRAME.y))
        pygame.draw.rect(var.WINDOW, (115, 205, 255), var.RECT_CAMERA_FRAME, 2)

    # Display the button to validate the value of the dice
    var.BUTTON_CHECK.check_state()

    return var.BUTTON_CHECK.just_clicked


def erase_dice_menu():
    """
    To erase the dice menu and save the value of the dice
    """
    var.DISPLAY_DICE_MENU = False  # We don't display the dice menu anymore
    var.WINDOW.blit(var.BACKGROUND, rect_dice_menu, rect_dice_menu)  # We erase the dice menu

    genetic = Genetic(height_slow=var.DICE_VARIABLES[0], height_medium=var.DICE_VARIABLES[1], height_fast=var.DICE_VARIABLES[2],
                      width_slow=var.DICE_VARIABLES[3], width_medium=var.DICE_VARIABLES[4], width_fast=var.DICE_VARIABLES[5])

    if var.DICE_RECT_GARAGE:  # We are modifying dice from garage
        var.DICE_RECT_GARAGE.genetic = genetic
    else:  # We are modifying dice from camera
        var.WINDOW.blit(var.BACKGROUND, var.RECT_CAMERA_FRAME, var.RECT_CAMERA_FRAME)  # We erase the dice menu

        var.MEMORY_CARS.get("dice").append((var.ACTUAL_ID_MEMORY_DICE, genetic))  # We add the dice to the memory
        var.ACTUAL_ID_MEMORY_DICE += 1  # We increment the id of the dice


def save_camera_frame(frame):
    """
    To modify the camera frame
    """
    frame = pygame.surfarray.make_surface(frame)  # Convert the camera frame to a surface
    # Resize, rotate and flip the camera frame
    frame = pygame.transform.scale(frame, (int(frame.get_width() * 0.8), int(frame.get_height() * 0.8)))
    frame = pygame.transform.rotate(frame, -90)
    var.CAMERA_FRAME = pygame.transform.flip(frame, True, False)

    # Get the rectangle of the camera frame
    var.RECT_CAMERA_FRAME = var.CAMERA_FRAME.get_rect()
    var.RECT_CAMERA_FRAME.x = 0
    var.RECT_CAMERA_FRAME.y = 200

