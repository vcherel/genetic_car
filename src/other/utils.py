import pygame  # To use pygame
import math  # To use math

"""
This file contains all the utility functions used in multiple other files
"""


def compute_detection_cone_points(angle, front_of_car, width, length):
    """
    Compute the coordinates of the points of the detection cone
    Args:
        angle (float): the angle of the car
        front_of_car (tuple(int, int)): the coordinates of the front of the car
        width (int): the width of the cone
        length (int): the length of the cone

    Returns:
        [left, top, right] (list(tuple(int, int))): the coordinates of the points of the detection cone
    """
    angle_cone = math.degrees(math.atan(width / (2 * length)))  # Angle of the detection cone

    top = front_of_car[0] + math.cos(math.radians(angle)) * length, front_of_car[1] - math.sin(math.radians(angle)) * length  # Position of the top of the cone
    left = front_of_car[0] + math.cos(math.radians(angle + angle_cone)) * length, front_of_car[1] - math.sin(math.radians(angle + angle_cone)) * length  # Position of the left of the cone
    right = front_of_car[0] + math.cos(math.radians(angle - angle_cone)) * length, front_of_car[1] - math.sin(math.radians(angle - angle_cone)) * length  # Position of the right of the cone
    return [left, top, right]


def point_out_of_window(point):
    """
    Check if a point is out of the window

    Args:
        point (tuple(int, int)): the coordinates of the point

    Returns:
        True if the point is out of the window
    """
    return point[0] < 0 or point[0] >= 1500 or point[1] < 0 or point[1] >= 700


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

    offset = 5  # Offset to add to the union of the two rectangles
    return_rect = pygame.Rect(min([rect.x for rect in rects]), min([rect.y for rect in rects]), 0, 0)  # The union of the two rectangles we will return
    return_rect.width = max([rect.x + rect.width for rect in rects]) - return_rect.x + 2 * offset
    return_rect.height = max([rect.y + rect.height for rect in rects]) - return_rect.y + 2 * offset
    return_rect.x -= offset
    return_rect.y -= offset
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


def change_color_car(image, str_color):
    """
    Change the color of an image representing a car

    Args:
        image (pygame.surface.Surface): the image to change
        str_color (str): the color to apply (black, blue, brown, gray, light_blue, light_gray, light_green, orange, pink, purple, red, yellow)
    """
    if str_color == 'red':   # If the color is red, we don't need to change it (the car is already red)
        return image

    # Create a new surface with the same dimensions and transparency settings as the original image
    new_image = pygame.Surface(image.get_size(), flags=image.get_flags(), depth=image.get_bitsize()).convert_alpha()

    # Iterate over each pixel in the original image
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            # Get the color of the pixel at (x, y)
            color = image.get_at((x, y))

            # Check if the pixel is transparent
            if color.a != 0:
                average_value = sum(color[:3]) // 3

                if str_color == 'black':
                    r, g, b = average_value // 2, average_value // 2, average_value // 2
                elif str_color == 'blue':
                    r, g, b = 0, 0, average_value
                elif str_color == 'brown':
                    orange_value = min(average_value, 255)
                    r, g, b = orange_value, orange_value // 2, 0
                elif str_color == 'gray':
                    r, g, b = average_value, average_value, average_value
                elif str_color == 'green':
                    r, g, b = 0, average_value, 0
                elif str_color == 'light_blue':
                    light_blue_value = min(average_value + 100, 255)
                    r, g, b = 0, light_blue_value, light_blue_value
                elif str_color == 'light_gray':
                    light_gray_value = min(average_value + 75, 255)
                    r, g, b = light_gray_value, light_gray_value, light_gray_value
                elif str_color == 'light_green':
                    light_green_value = min(average_value + 100, 255)
                    r, g, b = 0, light_green_value, 0
                elif str_color == 'orange':
                    orange_value = min(average_value + 125, 255)
                    r, g, b = orange_value, orange_value // 2, 0
                elif str_color == 'pink':
                    pink_value = min(average_value + 100, 255)
                    r, g, b = pink_value, 0, pink_value
                elif str_color == 'purple':
                    r, g, b = average_value, 0, average_value
                elif str_color == 'yellow':
                    yellow_value = min(average_value + 50, 255)
                    r, g, b = yellow_value, yellow_value, 0
                else:
                    r, g, b = 0, 0, 0

                # Set the pixel in the new image to the correct value
                new_image.set_at((x, y), (r, g, b, color.a))

    return new_image


def create_rect_from_points(points):
    """
    Create a rectangle from three points (used to get the rect associated to the detection cones)

    Args:
        points (list(tuple(int, int))): the list of points

    Returns:
        rect (pygame.Rect): the pygame Rect
    """
    # Check if the points list is empty
    if not points:
        return None

    # Initialize the min and max coordinates with the first point
    min_x = max_x = points[0][0]
    min_y = max_y = points[0][1]

    # Find the minimum and maximum coordinates
    for point in points:
        x, y = point
        min_x = min(min_x, x)
        max_x = max(max_x, x)
        min_y = min(min_y, y)
        max_y = max(max_y, y)

    # Create and return the pygame Rect
    rect_width = max_x - min_x
    rect_height = max_y - min_y

    return pygame.Rect(min_x, min_y, rect_width, rect_height)


def add_offset_to_rect(rect, offset):
    """
    Add an offset to a rect

    Args:
        rect: the rect
        offset: the offset to add

    Returns:
        the rect with the offset added
    """
    return pygame.Rect(rect.x - offset, rect.y - offset, rect.width + 2 * offset, rect.height + 2 * offset)
