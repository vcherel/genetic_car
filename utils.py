import math  # To use math
import pygame  # To use pygame
from constants import WIDTH_SCREEN, HEIGHT_SCREEN  # Import the constants


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


def detect_wall(front_of_car, point):
    """
    Detect if there is a wall between the front of the car and the point

    Args:
        front_of_car (tuple(int, int)): the coordinates of the front of the car
        point (tuple(int, int)): the coordinates of the point

    Returns:
        bool : True if there is a wall, False otherwise
    """
    x1, y1 = front_of_car  # Coordinates of the front of the car
    x2, y2 = point  # Coordinates of the point

    surface_display = pygame.display.get_surface()  # We get the surface of the window

    if x1 == x2:  # If the car is parallel to the wall
        # We check if there is a wall between the front of the car and the point
        for y in range(int(min(y1, y2)), int(max(y1, y2))):
            x1 = int(x1)
            # We check if the pixel is black (wall)
            if point_out_of_window((x1, y)) or surface_display.get_at((x1, y)) == (0, 0, 0, 255):
                return True  # There is a wall

    # We determine the equation of the line between the front of the car and the point (y = ax + b)
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1

    # We check if there is a wall between the front of the car and the point
    for x in range(int(min(x1, x2)), int(max(x1, x2))):
        y = int(a * x + b)
        # We check if the pixel is black (wall)
        if point_out_of_window((x, y)) or surface_display.get_at((x, y)) == (0, 0, 0, 255):
            return math.sqrt((x1 - x) ** 2 + (y1 - y) ** 2)  # We return the distance between the front of the car and the wall
    return False  # There is no wall


def point_out_of_window(point):
    """
    Check if a point is out of the window

    Args:
        point (tuple(int, int)): the coordinates of the point

    Returns:
        True if the point is out of the window, False otherwise
    """
    return point[0] < 0 or point[0] >= WIDTH_SCREEN or point[1] < 0 or point[1] >= HEIGHT_SCREEN


def union_rect(rects):
    """
    Compute the union of two rectangles

    Args:
        rects (list(pygame.Rect)): the list of the rectangles

    Returns:
        return_rect (pygame.Rect): the union of the two rectangles
    """
    if len(rects) == 0:
        return pygame.Rect(0, 0, 0, 0)
    elif len(rects) == 1:
        return rects[0]

    return_rect = pygame.Rect(0, 0, 0, 0)
    return_rect.x = min([rect.x for rect in rects])
    return_rect.y = min([rect.y for rect in rects])
    return_rect.width = max([rect.x + rect.width for rect in rects]) - return_rect.x
    return_rect.height = max([rect.y + rect.height for rect in rects]) - return_rect.y
    return return_rect


def text_rec(text, pos):
    """
    Compute the rect corresponding to the text

    Args:
        text (pygame.surface.Surface): the surface of the text
        pos (tuple(int, int)): the position of the text

    Returns:
        rect (pygame.Rect): the rect of the text
    """
    rect = text.get_rect()  # Get the rect of the text
    rect.x, rect.y = pos[0], pos[1]  # Change the position of the rect
    return rect
