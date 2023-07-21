from src.other.utils import text_rec, compute_detection_cone_points, convert_to_new_window, scale_image, scale_positions, change_color_car  # Import the utils functions
from src.data.constants import RGB_VALUES_DICE  # Import the constants
from src.data import variables as var
import pygame  # To use pygame

"""
This file contains all the functions to display elements on the screen
"""


def edit_background():
    """
    Add elements to the background for the rest of the game
    """
    font = pygame.font.SysFont('Arial', 20, bold=True)  # Create the font
    var.BACKGROUND.blit(font.render('Nombre de voitures', True, (0, 0, 0), (128, 128, 128)), convert_to_new_window((1060, 25)))  # Add the yes text
    pygame.draw.line(var.BACKGROUND, (0, 0, 0), convert_to_new_window((1280, 120)), convert_to_new_window((1280, 0)), 2)  # Line at the right
    pygame.draw.line(var.BACKGROUND, (0, 0, 0), convert_to_new_window((325, 120)), convert_to_new_window((325, 0)), 2)  # Line at the left


def show_checkpoints():
    for checkpoint in var.CHECKPOINTS:
        pygame.draw.circle(var.WINDOW, (255, 0, 0), convert_to_new_window(checkpoint), var.RADIUS_CHECKPOINT * var.SCALE_RESIZE_X, 1)


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


def draw_detection_cone(pos, dice_values, angle=90, factor=1, width_line=2, actual_mode=None):
    """
    Draw the detection cones for a car

    Args:
        pos (int, int): position of the car
        dice_values (list): list of the dice values for the detection cones [length_slow, length_medium, length_fast, width_slow, width_medium, width_fast]
        angle (int): angle of the detection cones
        factor (int): factor to multiply the dice values
        width_line (int): width of the line of the detection cones
        actual_mode (str): actual mode of the car (slow, medium, fast)

    Returns:
        list: list of the points of the detection cones (to blit it easily)
    """

    pos = convert_to_new_window(pos)  # Convert the position to the new window
    width_multiplier = var.SCALE_RESIZE_X * var.WIDTH_CONE * factor  # Multiplier for the width of the cone
    length_multiplier = var.SCALE_RESIZE_Y * var.LENGTH_CONE * factor  # Multiplier for the length of the cone

    left, top, right = compute_detection_cone_points(angle, pos, dice_values[3] * width_multiplier, dice_values[0] * length_multiplier)
    points = [pos, left, top, right]
    if actual_mode == 'slow':
        pygame.draw.polygon(var.WINDOW, (255, 255, 0), (pos, left, top, right), width_line * 2)
    else:
        pygame.draw.polygon(var.WINDOW, (255, 255, 0), (pos, left, top, right), width_line)

    left, top, right = compute_detection_cone_points(angle, pos, dice_values[4] * width_multiplier, dice_values[1] * length_multiplier)
    if actual_mode == 'medium':
        pygame.draw.polygon(var.WINDOW, (255, 128, 0), (pos, left, top, right), width_line * 2)
    else:
        pygame.draw.polygon(var.WINDOW, (255, 128, 0), (pos, left, top, right), width_line)
    points.append(left)
    points.append(top)
    points.append(right)

    left, top, right = compute_detection_cone_points(angle, pos, dice_values[5] * width_multiplier, dice_values[2] * length_multiplier)
    if actual_mode == 'fast':
        pygame.draw.polygon(var.WINDOW, (255, 0, 0), (pos, left, top, right), width_line * 2)
    else:
        pygame.draw.polygon(var.WINDOW, (255, 0, 0), (pos, left, top, right), width_line)
    points.append(left)
    points.append(top)
    points.append(right)

    return points


def show_car_window(car):
    """
    Display the car with the detection cones on the screen

    Args:
        car (Car): car to display
    """
    var.DISPLAY_CAR_WINDOW = True  # Display the car

    rect_x = 300
    rect_y = 190
    rect = pygame.Rect(convert_to_new_window((rect_x, rect_y, 750, 500)))  # Create the rectangle for the window
    pygame.draw.rect(var.WINDOW, (128, 128, 128), rect, 0)  # Draw the rectangle (inside)
    pygame.draw.rect(var.WINDOW, (1, 1, 1), rect, 2)  # Draw the rectangle (contour)

    x, y = rect_x + 565, rect_y + 230  # Position of the car

    image = change_color_car(var.BIG_RED_CAR_IMAGE, car.color)  # Change the color of the car

    image = scale_image(image, var.SCALE_RESIZE_X)  # Scale the image
    var.WINDOW.blit(image, convert_to_new_window((x, y)))  # Draw the red car
    draw_detection_cone((x + 52, y - 3), car.genetic.dice_values, factor=3, width_line=5)  # Draw the detection cones

    # Draw the dice
    x_distance = 120
    x1 = 160
    x2 = x1 + x_distance
    x3 = x2 + x_distance
    y1, y2 = 225, 350
    draw_dice(x=rect_x + x1, y=rect_y + y1, color=RGB_VALUES_DICE[0], value=car.genetic.length_slow // var.LENGTH_CONE, factor=0.75, black_dots=True)
    draw_dice(x=rect_x + x2, y=rect_y + y1, color=RGB_VALUES_DICE[1], value=car.genetic.length_medium // var.LENGTH_CONE, factor=0.75)
    draw_dice(x=rect_x + x3, y=rect_y + y1, color=RGB_VALUES_DICE[2], value=car.genetic.length_fast // var.LENGTH_CONE, factor=0.75)
    draw_dice(x=rect_x + x1, y=rect_y + y2, color=RGB_VALUES_DICE[3], value=car.genetic.width_slow // var.WIDTH_CONE, factor=0.75)
    draw_dice(x=rect_x + x2, y=rect_y + y2, color=RGB_VALUES_DICE[4], value=car.genetic.width_medium // var.WIDTH_CONE, factor=0.75)
    draw_dice(x=rect_x + x3, y=rect_y + y2, color=RGB_VALUES_DICE[5], value=car.genetic.width_fast // var.WIDTH_CONE, factor=0.75)

    # Draw the text
    var.WINDOW.blit(var.TEXT_SLOW, convert_to_new_window((rect_x + 175, rect_y + 150)))  # Draw the slow text
    var.WINDOW.blit(var.TEXT_MEDIUM, convert_to_new_window((rect_x + 277, rect_y + 150)))  # Draw the medium text
    var.WINDOW.blit(var.TEXT_FAST, convert_to_new_window((rect_x + 400, rect_y + 150)))  # Draw the fast text
    var.WINDOW.blit(var.TEXT_LENGTH, convert_to_new_window((rect_x + 25, rect_y + 250)))  # Draw the length text
    var.WINDOW.blit(var.TEXT_WIDTH, convert_to_new_window((rect_x + 15, rect_y + 375)))  # Draw the width text


def erase_car_window():
    """
    Erase the car window with the detection cones on the screen
    """
    var.DISPLAY_CAR_WINDOW = False  # Don't display the car

    rect = pygame.Rect(convert_to_new_window((300, 190, 750, 500)))  # Create the rectangle for the window
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

    pygame.draw.rect(var.WINDOW, color, (convert_to_new_window((x, y, int(120 * factor), int(120 * factor)))), 0)
    pygame.draw.rect(var.WINDOW, (100, 100, 100), (convert_to_new_window((x, y, int(120 * factor), int(120 * factor)))), 3)

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
    dot_offset = 32
    position_dot = []  # They will correspond to the positions of the dots in the new window

    # Calculate the positions of the dots based on the number of dots
    if nb_dots == 1:
        position_dot = scale_positions(x, y, [(60, 60)], factor)
    elif nb_dots == 2:
        position_dot = scale_positions(x, y, [(dot_offset, dot_offset), (120 - dot_offset, 120 - dot_offset)], factor)
    elif nb_dots == 3:
        position_dot = scale_positions(x, y, [(dot_offset, dot_offset), (60, 60), (120 - dot_offset, 120 - dot_offset)], factor)
    elif nb_dots == 4:
        position_dot = scale_positions(x, y, [(dot_offset, dot_offset), (dot_offset, 120 - dot_offset), (120 - dot_offset, dot_offset),
                                              (120 - dot_offset, 120 - dot_offset)], factor)
    elif nb_dots == 5:
        position_dot = scale_positions(x, y, [(dot_offset, dot_offset), (dot_offset, 120 - dot_offset), (120 - dot_offset, dot_offset),
                                       (120 - dot_offset, 120 - dot_offset), (60, 60)], factor)
    elif nb_dots == 6:
        position_dot = scale_positions(x, y, [(dot_offset, dot_offset), (dot_offset, 120 - dot_offset), (120 - dot_offset, dot_offset),
                                              (120 - dot_offset, 120 - dot_offset), (dot_offset, 60), (120 - dot_offset, 60)], factor)

    # Draw the dots on the dice
    for dot_pos in position_dot:
        pygame.draw.circle(var.WINDOW, color, dot_pos, int(dot_radius * factor * var.SCALE_RESIZE_X))
