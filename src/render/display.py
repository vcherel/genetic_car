from src.other.utils import text_rec, compute_detection_cone_points  # Import the utils functions
from src.game.constants import RADIUS_CHECKPOINT, WIDTH_MULTIPLIER, HEIGHT_MULTIPLIER, RGB_VALUES  # Import the constants
from src.other.utils import convert_to_grayscale, convert_to_yellow_scale, scale_positions  # Import the utils functions
from src.other import variables as var  # Import the variables
import pygame  # To use pygame
import cv2  # To use OpenCV


"""
This function contains all the functions to display elements on the screen
"""


def edit_background():
    """
    Add elements to the background for the rest of the game
    """
    # Add a text for the debug_0 mode
    var.BACKGROUND.blit(var.FONT.render('Nombre de voitures', True, (0, 0, 0), (128, 128, 128)), (1060, 25))  # Add the yes text
    pygame.draw.line(var.BACKGROUND, (0, 0, 0), (1280, 120), (1280, 0), 2)  # Line at the right
    pygame.draw.line(var.BACKGROUND, (0, 0, 0), (325, 120), (325, 0), 2)  # Line at the left


def show_checkpoints():
    for checkpoint in var.CHECKPOINTS:
        pygame.draw.circle(var.WINDOW, (255, 0, 0), checkpoint, RADIUS_CHECKPOINT, 1)


def display_text_ui(caption, pos, font, background_color=(128, 128, 128)):
    """
    Display a text with a variable

    Args:
        caption (str): caption of the text
        pos (tuple): position of the text
        font (pygame.font.Font): font of the text
        background_color (tuple): background color of the text
    """
    text = font.render(caption, True, (0, 0, 0), background_color)  # Create the text
    var.WINDOW.blit(text, pos)  # Draw the text
    var.RECTS_BLIT_UI.append(text_rec(text, pos))  # Add the rectangle of the text to the list of rectangles to blit


def draw_circle(circle, image):
    """
    Draw the circles on the image

    Args:
        circle (numpy.ndarray): The circle to draw
        image (numpy.ndarray): Image on which to draw the circles
    """
    # Draw the outer circle
    cv2.circle(image, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 255, 0), 2)
    # Draw the center of the circle
    cv2.circle(image, (int(circle[0]), int(circle[1])), 2, (0, 0, 255), 3)


def draw_detection_cone(pos, dice_values, factor=50):
    """
    Draw the detection cones for a car

    Args:
        pos (int, int): position of the car
        dice_values (list): list of the dice values for the detection cones [height_slow, height_medium, height_fast, width_slow, width_medium, width_fast]
        factor (float): factor to multiply the width and height of the detection cone
    """
    left, top, right = compute_detection_cone_points(90, pos, dice_values[3] * factor, dice_values[0] * factor)
    pygame.draw.polygon(var.WINDOW, (255, 255, 0), (pos, left, top, right), 5)

    left, top, right = compute_detection_cone_points(90, pos, dice_values[4] * factor, dice_values[1] * factor)
    pygame.draw.polygon(var.WINDOW, (255, 128, 0), (pos, left, top, right), 5)

    left, top, right = compute_detection_cone_points(90, pos, dice_values[5] * factor, dice_values[2] * factor)
    pygame.draw.polygon(var.WINDOW, (255, 0, 0), (pos, left, top, right), 5)


def show_car_window(car):
    """
    Display the car with the detection cones on the screen

    Args:
        car (Car): car to display
    """
    var.DISPLAY_CAR_WINDOW = True  # Display the car

    rect = pygame.Rect(350, 125, 700, 550)  # Create the rectangle for the window
    pygame.draw.rect(var.WINDOW, (128, 128, 128), rect, 0)  # Draw the rectangle (inside)
    pygame.draw.rect(var.WINDOW, (115, 205, 255), rect, 2)  # Draw the rectangle (contour)

    x, y = rect[0] + 425, rect[1] + 300  # Position of the car

    if car.view_only:
        image = convert_to_grayscale(var.BIG_RED_CAR_IMAGE)
    elif car.best_car:
        image = convert_to_yellow_scale(var.BIG_RED_CAR_IMAGE)
    else:
        image = var.BIG_RED_CAR_IMAGE

    var.WINDOW.blit(image, (x, y))  # Draw the red car
    draw_detection_cone((x + 125, y + 25), car.genetic.get_list())  # Draw the detection cones

    var.WINDOW.blit(var.TEXT_SLOW, (rect[0] + 90, rect[1] + 150))  # Draw the slow text
    var.WINDOW.blit(var.TEXT_MEDIUM, (rect[0] + 200, rect[1] + 150))  # Draw the medium text
    var.WINDOW.blit(var.TEXT_FAST, (rect[0] + 325, rect[1] + 150))  # Draw the fast text

    x1, x2, x3 = 75, 200, 325
    y1, y2 = 225, 350
    draw_dice(x=rect[0] + x1, y=rect[1] + y1, color=RGB_VALUES[0], value=car.genetic.height_slow // HEIGHT_MULTIPLIER, factor=0.75, black_dots=True)
    draw_dice(x=rect[0] + x2, y=rect[1] + y1, color=RGB_VALUES[1], value=car.genetic.height_medium // HEIGHT_MULTIPLIER, factor=0.75)
    draw_dice(x=rect[0] + x3, y=rect[1] + y1, color=RGB_VALUES[2], value=car.genetic.height_fast // HEIGHT_MULTIPLIER, factor=0.75)
    draw_dice(x=rect[0] + x1, y=rect[1] + y2, color=RGB_VALUES[3], value=car.genetic.width_slow // WIDTH_MULTIPLIER, factor=0.75)
    draw_dice(x=rect[0] + x2, y=rect[1] + y2, color=RGB_VALUES[4], value=car.genetic.width_medium // WIDTH_MULTIPLIER, factor=0.75)
    draw_dice(x=rect[0] + x3, y=rect[1] + y2, color=RGB_VALUES[5], value=car.genetic.width_fast // WIDTH_MULTIPLIER, factor=0.75)


def erase_car_window():
    """
    Erase the car window with the detection cones on the screen
    """
    var.DISPLAY_CAR_WINDOW = False  # Don't display the car

    rect = pygame.Rect(350, 125, 700, 550)  # Create the rectangle for the window
    var.WINDOW.blit(var.BACKGROUND, rect, rect)  # Blit the background on the rectangle


def draw_dice(x, y, color, value, factor=1, black_dots=False):
    """
    To draw a dice

    Args:
        x (int): x coordinate of the dice
        y (int): y coordinate of the dice
        color (tuple): color of the dice
        value (int): value of the dice
        factor (float): factor to multiply the size of the dice
        black_dots (bool): if the dots are black
    """

    pygame.draw.rect(var.WINDOW, color, (x, y, int(120 * factor), int(120 * factor)), 0)
    pygame.draw.rect(var.WINDOW, (100, 100, 100), (x, y, int(120 * factor), int(120 * factor)), 3)

    if black_dots:  # If the dice is dark_yellow the dots are black
        draw_dots(x, y, value, factor, (0, 0, 0))
    else:
        draw_dots(x, y, value, factor)


def draw_dots(x, y, nb_dots, factor, color=(255, 255, 255)):
    """
    To draw the dots on the dice

    Args:
        x (int): x coordinate of the dice
        y (int): y coordinate of the dice
        nb_dots (int): Number of dots on the dice
        factor (float): factor to multiply the size of the dots
        color (tuple): Color of the dots. Defaults to white.
    """
    dot_radius = 10
    dot_padding = 32
    position_dot = []

    # Calculate the positions of the dots based on the number of dots
    if nb_dots == 1:
        position_dot = scale_positions(x, y, [(60, 60)], factor)
    elif nb_dots == 2:
        position_dot = scale_positions(x, y, [(dot_padding, dot_padding), (120 - dot_padding, 120 - dot_padding)], factor)
    elif nb_dots == 3:
        position_dot = scale_positions(x, y, [(dot_padding, dot_padding), (60, 60), (120 - dot_padding, 120 - dot_padding)], factor)
    elif nb_dots == 4:
        position_dot = scale_positions(x, y, [(dot_padding, dot_padding), (dot_padding, 120 - dot_padding), (120 - dot_padding, dot_padding),
                                              (120 - dot_padding, 120 - dot_padding)], factor)
    elif nb_dots == 5:
        position_dot = scale_positions(x, y, [(dot_padding, dot_padding), (dot_padding, 120 - dot_padding), (120 - dot_padding, dot_padding),
                                       (120 - dot_padding, 120 - dot_padding), (60, 60)], factor)
    elif nb_dots == 6:
        position_dot = scale_positions(x, y, [(dot_padding, dot_padding), (dot_padding, 120 - dot_padding), (120 - dot_padding, dot_padding),
                                              (120 - dot_padding, 120 - dot_padding), (dot_padding, 60), (120 - dot_padding, 60)], factor)

    # Draw the dots on the dice
    for dot_pos in position_dot:
        pygame.draw.circle(var.WINDOW, color, dot_pos, int(dot_radius * factor))