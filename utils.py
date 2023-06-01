import pygame  # To use pygame
import math  # To use math


def scale_image(img, factor):
    """
    Change the scale of an image

    Args:
        img (pygame.Surface): the image to scale
        factor (float): the scale factor

    Returns:
        scaled_image (pygame.image): the scaled image
    """
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


def compute_front_of_car(pos, angle, image):
    """
    Compute the coordinates of the front of the car
    Args:
        pos (tuple(float, float)): the position of the car
        angle (float): the angle of the car
        image (pygame.Surface): the image of the car

    Returns:
        front_of_car (tuple(int, int)): the coordinates of the front of the car
    """
    return pos[0] + math.cos(math.radians(-angle)) * image.get_width() / 2, \
        pos[1] + math.sin(math.radians(-angle)) * image.get_width() / 2


def compute_detection_cone_points(angle, front_of_car, width, height):
    """
    Compute the coordinates of the points of the detection cone
    Args:
        angle (float): the angle of the car
        front_of_car (tuple(int, int)): the coordinates of the front of the car
        width (int): the width of the window
        height (int): the height of the window

    Returns:
        [left, top, right] (list(tuple(int, int))): the coordinates of the points of the detection cone
    """
    angle_cone = math.degrees(math.atan(width / (2 * height)))  # Angle of the detection cone

    top = front_of_car[0] + math.cos(math.radians(angle)) * height, \
        front_of_car[1] - math.sin(math.radians(angle)) * height  # Position of the top of the cone
    left = front_of_car[0] + math.cos(math.radians(angle + angle_cone)) * height, \
        front_of_car[1] - math.sin(math.radians(angle + angle_cone)) * height  # Position of the left of the cone
    right = front_of_car[0] + math.cos(math.radians(angle - angle_cone)) * height,\
        front_of_car[1] - math.sin(math.radians(angle - angle_cone)) * height  # Position of the right of the cone

    return [left, top, right]
