from render.resizing import convert_to_new_window  # To convert the coordinates to the new window
import data.variables as var  # To use the variables
import warnings  # To ignore warnings
import math  # To use math functions
import numpy as np  # To use numpy
import pygame  # To use pygame


"""
This file contains all the utils functions related to the detection of the dice
"""


def verif_coordinates(circles, rect, coordinates):
    """
    Verify if the coordinates of the circle are one of the coordinates in parameters

    Args:
        circles (numpy.ndarray): Array of circles detected by the HoughCircles function
        rect (tuple): Coordinates of the rectangle
        coordinates (list): List of coordinates to check

    Returns:
        (bool): True if the coordinates are the same
    """
    x, y = rect[:2]
    for circle in circles:
        circle_found = False
        for pos in coordinates:
            if pos[0] - 5 < circle[0] + x < pos[0] + 5 and pos[1] - 5 < circle[1] + y < pos[1] + 5:
                circle_found = True
                break
        if not circle_found:
            return False

    return True


def add_offset(rectangles, offset):
    """
    Add an offset to the rectangles

    Args:
        rectangles (list): List of rectangles found
        offset (int): Offset to add to the rectangles

    Returns:
        list: List of rectangles found
    """
    new_rectangles = []
    for rectangle in rectangles:
        x, y, w, h = rectangle
        new_rectangles.append((x - offset, y - offset, w + 2 * offset, h + 2 * offset))

    return new_rectangles


def overlapping_rectangles(rect1, rect2, area_threshold):
    """
    Check if two rectangles are overlapping for more than the area threshold

    Args:
        rect1 (tuple(int, int, int, int)): the first rectangle (x, y, w, h)
        rect2 (tuple(int, int, int, int)): the second rectangle (x, y, w, h)
        area_threshold (float): the minimum overlapping area threshold

    Returns:
        bool: True if the rectangles are overlapping
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


def circles_too_close(circle1, circle2, distance_threshold=7):
    """
        Check if two circles are overlapping for more than the area threshold

        Args:
            circle1 (tuple(int, int, int)): the first circle (x, y, r)
            circle2 (tuple(int, int, int)): the second circle (x, y, r)
            distance_threshold (float): the minimum distance between the centers of the circles

        Returns:
            bool: True if the circles are overlapping
        """
    x1, y1, _ = circle1
    x2, y2, _ = circle2

    # Calculate the distance between the centers of the circles
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    # Check if the circles are overlapping
    if distance <= distance_threshold:
        return True

    return False


def compute_mean_bgr(image):
    """
    Compute the mean BGR values of the image without the white or black dots

    Args:
        image (numpy.ndarray): Image of the dice

    Returns:
        (numpy.ndarray): Mean BGR values of the image without the white or black dots
    """
    threshold_distance = 150  # The threshold distance to consider a pixel as a white or black dot
    white = np.array([200, 200, 200])  # Assuming white color value
    array = np.array(image)  # Convert the image to a numpy array

    # Create a boolean mask to filter out pixels based on the condition
    mask = (np.linalg.norm(array - white, axis=2) > threshold_distance)

    # Filter the array based on the mask
    new_list = array[mask]

    # Calculate the mean BGR values on the filtered array
    with warnings.catch_warnings():  # I expect to see RuntimeWarnings in this block
        warnings.simplefilter("ignore", category=RuntimeWarning)
        mean_bgr = np.mean(new_list, axis=0)

    return mean_bgr


def update_pygame_camera_frame(frame):
    """
    Transform the openCV frame to a pygame frame and update the variables of the camera frame in the dice menu

    Args:
        frame (numpy.ndarray): Frame of the camera
    """
    frame = pygame.surfarray.make_surface(frame)  # Convert the camera frame to a surface

    # Resize, rotate and flip the camera frame
    var.CAMERA_FRAME = pygame.transform.flip(pygame.transform.rotate(pygame.transform.scale(frame, (int(frame.get_width() * 0.75), int(frame.get_height() * 0.75))), -90), True, False)

    # Get the rectangle of the camera frame
    var.RECT_CAMERA_FRAME = var.CAMERA_FRAME.get_rect()
    var.RECT_CAMERA_FRAME.x, var.RECT_CAMERA_FRAME.y = 0, 200  # We place the camera frame in the window at the right place

    # Resize the camera frame to fit the window
    var.RECT_CAMERA_FRAME = pygame.rect.Rect(convert_to_new_window(var.RECT_CAMERA_FRAME))  # Convert the rectangle to the new window
    var.CAMERA_FRAME = pygame.transform.scale(var.CAMERA_FRAME, (var.RECT_CAMERA_FRAME.width, var.RECT_CAMERA_FRAME.height))  # Resize the camera frame
