import src.other.variables as var  # To use the variables
import pygame  # To use pygame
import math  # To use math

"""
This file contains all the utility functions used in multiple other files
"""


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
        True if the point is out of the window, False otherwise
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

    return_rect = pygame.Rect(0, 0, 0, 0)  # The union of the two rectangles we will return
    return_rect.x = min([rect.x for rect in rects])
    return_rect.y = min([rect.y for rect in rects])
    return_rect.width = max([rect.x + rect.width for rect in rects]) - return_rect.x
    return_rect.height = max([rect.y + rect.height for rect in rects]) - return_rect.y
    offset = 5
    return_rect.x -= offset
    return_rect.y -= offset
    return_rect.width += 2 * offset
    return_rect.height += 2 * offset
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


def overlapping_rectangles(rect1, rect2, area_threshold=0.5):
    """
    Check if two rectangles are overlapping for more than half of their area

    Args:
        rect1 (tuple(int, int, int, int)): the first rectangle (x, y, w, h)
        rect2 (tuple(int, int, int, int)): the second rectangle (x, y, w, h)
        area_threshold (float): the minimum overlapping area threshold

    Returns:
        bool: True if the rectangles are overlapping, False otherwise
    """
    x1, y1, w1, h1 = rect1
    x2, y2, w2, h2 = rect2

    # Calculate the coordinates of the intersection rectangle
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    # Check if the rectangles are not overlapping
    if x_right <= x_left or y_bottom <= y_top:
        return False

    # Calculate the areas of the rectangles and the intersection
    area1 = w1 * h1
    area2 = w2 * h2
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    return intersection_area > area_threshold * min(area1, area2)


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
    new_image = pygame.Surface(image.get_size(), flags=image.get_flags(), depth=image.get_bitsize())
    new_image.convert_alpha()

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
