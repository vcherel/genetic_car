import data.variables as var  # Import the data
import pygame  # To use pygame

"""
This file contains all the functions related to the resizing of the application window
"""


def convert_to_new_window(x):
    """
    Convert the coordinates of a point from a 1500x700 window to the current window

    Args:
        x (tuple(int, int)) or tuple(int, int, int, int) or float: the position or the rect or the factor to convert

    Returns:
        tuple(int, int) or float: the converted position or the converted factor
    """
    if type(x) == float:   # If x is a factor
        return x * var.WIDTH_SCREEN * var.HEIGHT_SCREEN / (1500 * 700)
    elif len(x) == 2:    # If x is a position
        return int(x[0] * var.WIDTH_SCREEN / 1500), int(x[1] * var.HEIGHT_SCREEN / 700)
    else:   # If x is a rect
        return int(x[0] * var.WIDTH_SCREEN / 1500), int(x[1] * var.HEIGHT_SCREEN / 700), \
               int(x[2] * var.SCALE_RESIZE_X), int(x[3] * var.SCALE_RESIZE_Y)


def scale_image(img, factor=None):
    """
    Change the scale of an image

    Args:
        img (pygame.Surface): the image to scale
        factor (float or tuple(float, float)): the scale factor, if it is a tuple the factor is different for the width and the height
        If the factor is None, we scale the image to the size of the new window

    Returns:
        scaled_image (pygame.image): the scaled image
    """
    if factor is None:
        x, y = var.SCALE_RESIZE_X, var.SCALE_RESIZE_Y
    elif isinstance(factor, float) or isinstance(factor, int):
        x, y = factor, factor
    else:
        x, y = factor[0], factor[1]

    size = round(img.get_width() * x), round(img.get_height() * y)
    return pygame.transform.scale(img, size)


def scale_positions(x, y, positions, factor):
    """
    Scale the positions of a list of points

    Args:
        x (int): the x coordinate of the window
        y (int): the y coordinate of the window
        positions (list(tuple(int, int))): the list of points
        factor (float): the scaling factor

    Returns:
        new_positions (list(tuple(int, int))): the scaled positions
    """
    new_positions = []

    for i, position in enumerate(positions):
        new_positions.append(convert_to_new_window((x + int(position[0] * factor), y + int(position[1] * factor))))

    return new_positions