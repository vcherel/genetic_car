import matplotlib.pyplot as plt  # To show images
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


def show_click(rect_window, frame):
    """
    Display the click in the terminal

    Args:
        rect_window (pygame.rect.Rect): Rectangle of the window
        frame (numpy.ndarray): Image of the camera
    """
    pos = pygame.mouse.get_pos()
    pos = (pos[0] - rect_window.x, pos[1] - rect_window.y)
    # Print the position of the click
    print(pos)
    # Print the color of the pixel
    print(frame[pos[1], pos[0]])


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


def check_overlapping_rectangles(rectangles):
    """
    Check if the rectangles are overlapping or not

    Args:
        rectangles (list): List of rectangles found

    Returns:
        list: List of rectangles found
    """
    new_rectangles = []
    # We check if the rectangles are overlapping or not
    for rect in rectangles:
        overlapping = False
        for new_rect in new_rectangles:
            if overlapping_rectangles(rect, new_rect, area_threshold=0.4):
                # If the rectangles are overlapping, we take the biggest one
                overlapping = True
                if rect[2] * rect[3] > new_rect[2] * new_rect[3]:
                    new_rectangles.remove(new_rect)
                    new_rectangles.append(rect)
                break

        if not overlapping:
            new_rectangles.append(rect)

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


def calculate_intersection_area(circle1, circle2, distance):
    """
    Calculate the area of intersection between two circles

    Args:
        circle1 (tuple(int, int, int)): the first circle (x, y, r)
        circle2 (tuple(int, int, int)): the second circle (x, y, r)
        distance (float): the distance between the centers of the circles
    """
    x1, y1, r1 = circle1
    x2, y2, r2 = circle2

    # Calculate the area of intersection using the formula for two overlapping circles
    if distance >= abs(r1 - r2):
        if distance <= r1 + r2:
            a = (r1**2 - r2**2 + distance**2) / (2 * distance)
            h = math.sqrt(r1**2 - a**2)
            intersection_area = r1**2 * math.acos(a / r1) - a * h
        else:
            intersection_area = min(math.pi * r1**2, math.pi * r2**2)
    else:
        intersection_area = 0

    return intersection_area


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

    # To see what the threshold distance should be
    """
    count = 0
    count_white = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            count += 1
            if np.linalg.norm(array[i][j] - white) < 150:
                count_white += 1
    print(count_white * 100 / count)
    """

    # Create a boolean mask to filter out pixels based on the condition
    mask = (np.linalg.norm(array - white, axis=2) > threshold_distance)

    # Filter the array based on the mask
    new_list = array[mask]

    # Calculate the mean BGR values on the filtered array
    with warnings.catch_warnings():  # I expect to see RuntimeWarnings in this block
        warnings.simplefilter("ignore", category=RuntimeWarning)
        mean_bgr = np.mean(new_list, axis=0)

    return mean_bgr


def biggest_rect(rect1, rect2):
    """
    Return the biggest rectangle (in terms of area)
    """
    if rect1[2] * rect1[3] > rect2[2] * rect2[3]:
        return rect1
    else:
        return rect2


def show_image(image, gray=True):
    """
    Show an image in a window

    Args:
        image (numpy.ndarray): The image
        gray (bool): If the image is in gray scale
    """
    if gray:
        plt.imshow(image, cmap='gray')  # Image with the edges
    else:
        plt.imshow(image)
    plt.show()
