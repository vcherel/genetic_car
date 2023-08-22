from data.constants import PATH_DATA
from other.camera_utils import *  # Utils functions for the camera
from data.data_classes import ColorDice  # To find the color of each dice
from menus.dice_menu import update_pygame_camera_frame  # To save the camera frame
import data.variables as var  # Variables
import random  # To generate random numbers
import numpy as np  # To use numpy
import pygame  # To use Pygame
import cv2  # To use OpenCV

from render.resizing import convert_to_new_window

"""
This file contains the functions used to get the score of the dice from the camera with OpenCV
"""

NUM_CAMERA = 0  # The number of the camera we want to use

# The rects kept in memory (when we detect a rectangle, if it overlaps with a rectangle in memory, we display the rectangle in memory)
memory_rects = {}  # Format : {rect : lifetime_remaining} ; lifetime_remaining : the number of frames the rectangle will be displayed unless it is detected again

# We take in memory for each color the bgr color and the rectangle to prevent 2 colors from being the same
colors = {}  # List of the colors of the dice (key: name_color, value: ColorDice)

# The circles kept in memory (when we detect a circle, if it overlaps with a circle in memory, we display the circle in memory)
memory_circles = {'yellow': {}, 'orange': {}, 'red': {}, 'dark_yellow': {}, 'green': {}, 'black': {}}  # Format : {color : {circle : lifetime_remaining}}

# The last scores we stored for each color (used to compare with the new scores to avoid changing the score too often)
scores_colors = {'yellow': [], 'orange': [], 'red': [], 'dark_yellow': [], 'green': [], 'black': []}

frame_view = np.empty([2, 2])  # The frame of the camera (viewed by the user)
frame = np.empty([2, 2])  # The frame of the camera (used by the program)

count_iterations = 0  # The number of iterations of the program

# The parameters of the HoughCircles function
param_1, param_2, param_dp = 150, 16, 5
max_radius_circle = 7  # The maximum radius of the circles we want to detect


# Optimization and debug parameters

show_clicks = False  # To show the coordinates and color of the position where the user clicked

# To find what is the color of each dice
write_mean_bgr = False
file_write_mean_bgr = None  # The file in which we will write the parameters

# Optimization parameters for HoughCircles function
optimize_hough_circle = False  # To optimize the parameters of the HoughCircles function
# The min and max values of the parameters
p1_min, p1_max = 50, 200
p2_min, p2_max = 10, 80
dp_min, dp_max = 30, 150
# The colors we want to optimize and the value of the dice we want to optimize
theorical_values = {}  # Format : {color : value}
# The coordinates of the dice we want to optimize
theorical_coordinates = {}  # Format : {color : [(x1, y1), (x2, y2)]}
wait_optimize = 100  # The number of iterations we wait before starting to optimize
dict_p1_opti, dict_p2_opti, dict_dp_opti = {}, {}, {}  # Format : {value : count}

# Create a VideoCapture object
cap = cv2.VideoCapture(NUM_CAMERA)  # 0 corresponds to the default camera, you can change it if you have multiple cameras


def capture_dice():
    """
    Main program, find the values of the different dice from the camera and return them when the user clicks on the window
    The dice are identified by their color

    Returns:
        (list) : The scores of the dice
    """
    global frame_view, frame

    final_score = {'yellow': random.randint(1, 6), 'orange': random.randint(1, 6), 'red': random.randint(1, 6),
                   'dark_yellow': random.randint(1, 6), 'green': random.randint(1, 6), 'black': random.randint(1, 6)}

    rect_window = pygame.rect.Rect(convert_to_new_window((425, 175, 640, 480)))

    while True:
        res = find_dice_values(final_score)  # Find the values of the dice from the camera
        if res is not None:
            # If we are here it means there is no camera connected
            return res  # We quit the dice capture


        # We display the frame on the window
        display_frame(rect_window)

        if count_iterations == wait_optimize and optimize_hough_circle:
            display_dictionaries_optimization()  # Sort the dictionaries and print them

        # Detect a click on the window to stop the program
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:  # We stop the program after a click
                if show_clicks:
                    show_click(rect_window, frame)  # We display the click
                var.WINDOW.blit(var.BACKGROUND, rect_window, rect_window)  # We erase the window

                frame_view = cv2.cvtColor(frame_view, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
                update_pygame_camera_frame(frame_view)  # Update the frame of the camera shown in pygame

                return end_capture_dice(final_score)  # End the capture of the dice, and return the scores in a list


def find_dice_values(final_score):
    """
    Find the values of the dice from the camera (one frame)

    Args:
        final_score (dict): The scores of the dice
    """
    global count_iterations, frame_view, frame, colors

    count_iterations += 1  # We increment the number of iterations

    _, frame = cap.read()  # Read a frame from the camera

    if frame is None:  # We don't have a camera connected
        print('Aucune caméra détectée')
        return end_capture_dice(final_score)

    frame_view = frame.copy()  # We make a copy of the frame to display it on the window (with rectangles, texts, ...)

    rectangles = find_rectangles()  # Find the rectangles on the image

    # Draw all the rectangles found on the image
    # draw_rectangle(rectangles, thickness=1)

    # Initialize the colors memory
    colors = {}  # List of the colors of the dice (key: name_color, value: ColorDice)

    for rect in rectangles:
        find_colors(rect)  # Modify the colors dictionary inplace

    for color in colors:
        draw_score(color, final_score)


def find_rectangles():
    """
    Find the rectangles on the frame of the camera

    Returns:
        list: The list of rectangles found
    """
    contours = find_contours(frame)  # We find the contours
    rectangles = get_rectangles_from_contours(contours)  # We check the validity of the contours
    rectangles = add_offset(rectangles, offset=7)  # We add an offset to each rectangle in case the rectangle has cut the dice
    rectangles = add_rect_from_memory(rectangles)  # We add the rectangles from the memory to the list of rectangles

    update_memory(memory_rects)  # We update the memory of the rectangles (we decrease the lifetime of the rectangles)

    return rectangles


def find_contours(image):
    """
    Find the contours of the dice on the image

    Args:
        image (numpy.ndarray): Image on which to find the contours

    Returns:
        list: The list of contours found
    """
    # The parameters of the threshold to make a black and white image for each color
    param_thresh = {'yellow': 170, 'orange': 90, 'red': 60, 'dark_yellow': 100, 'green': 80, 'black': 20}

    contours = []  # The list of contours found

    for (str_color, value) in param_thresh.items():  # For each color we have a threshold_color
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
        gray_img = cv2.medianBlur(gray_img, 3)  # We apply a median blur to the image to erase useless details

        # We apply a threshold to the image : it turns the image into a black and white image
        thresh = cv2.threshold(gray_img, value, 255, cv2.THRESH_BINARY_INV)[1]

        # We create a kernel to close the edges of the dice
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        edges_1 = cv2.Canny(gray_img, 9, 150, 3)  # Detect edges from the gray image
        edges_2 = cv2.Canny(thresh, 9, 150, 3)  # Detect edges from the threshold image

        for edges in [edges_1, edges_2]:
            close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice
            contour_found, _ = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # We find the contours of the image
            contours += contour_found  # We merge the contours found by the two methods

    return contours


def get_rectangles_from_contours(contours):
    """
    We create a list of valid rectangles from the list of contours without duplicates

    Args:
        contours (list): List of contours found

    Returns:
        list: List of rectangles found
    """
    rectangles = []  # List of rectangles
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)  # We get the coordinates of the rectangle

        if valid_rectangle(x, y, w, h):  # We check if the rectangle is valid
            # Check if the rectangle is not already in the list (if it is we add the biggest one)
            rectangle_already_in_list = False  # Boolean to know if the rectangle is already in the list
            for rectangle in rectangles:
                if overlapping_rectangles((x, y, w, h), rectangle, area_threshold=0.6):
                    rectangle_already_in_list = True
                    if w * h > rectangle[2] * rectangle[3]:   # We keep the biggest rectangle
                        rectangles.remove(rectangle)
                        rectangles.append((x, y, w, h))
                    break

            if not rectangle_already_in_list:
                rectangles.append((x, y, w, h))

    return rectangles


def valid_rectangle(x, y, w, h, min_size=40, max_size=75):
    """
    Check if the rectangle is valid (not too big or too small, not too close to the edge of the image)
    """
    return min_size < w < max_size and min_size < h < max_size and x > 5 and y > 5 and x + w < 635 and y + h < 475


def add_rect_from_memory(rectangles, lifetime=25, area_threshold=0.9):
    """
    Add the rectangles from the memory to the list of rectangles, without duplicates

    Args:
        rectangles (list): List of rectangles found
        lifetime (int): Lifetime of the rectangles in the memory when they are detected
        area_threshold (float): Threshold of the area of the rectangles to consider that they are the same

    Returns:
        list: List of rectangles found
    """
    new_rectangles = list(memory_rects.keys())  # List of rectangles to add to the list of rectangles

    # We look at each rectangle
    for rectangle in rectangles:
        rect_already_in_memory = False  # Boolean to know if the rectangle is already in the memory

        # We look if the rectangle is already in the memory
        for memory_rect in memory_rects:
            if overlapping_rectangles(rectangle, memory_rect, area_threshold):
                rect_already_in_memory = True
                memory_rects[memory_rect] = lifetime  # We reset the lifetime of the rectangle
                break

        if not rect_already_in_memory:
            new_rectangles.append(rectangle)
            memory_rects[rectangle] = lifetime  # We add the rectangle to the memory

    return new_rectangles


def search_rectangle(rect, rectangles):
    """
    Search if a rectangle is in the list of rectangles

    Args:
        rect (tuple): Rectangle to search
        rectangles (list): List of rectangles

    Returns:
        rect: rect if it's not in the list, the biggest rectangle between rect and the rectangle in the list if it's in the list
    """
    for rectangle in rectangles:
        if overlapping_rectangles(rect, rectangle, area_threshold=0.6) and rect[2] * rect[3] < rectangle[2] * rectangle[3]:
            return rectangle

    return rect


def update_memory(memory):
    """
    Update the memory of the rectangles or the circles (we decrease the lifetime of the objects and delete the objects if the lifetime reach 0)

    Args:
        memory (dict): Dictionary of the objects in the memory
    """
    memory_to_delete = []  # List of objects to delete from the memory
    for key in memory:  # We look at each object in the memory
        memory[key] -= 1  # We decrease the lifetime of the object
        if memory[key] == 0:  # If the object die
            memory_to_delete.append(key)  # We add the object to the list of objects to delete

    for key in memory_to_delete:  # We delete the objects from the memory
        del memory[key]


def find_colors(rect):
    """
    Find the colors of the dice
    """
    x, y, w, h = rect  # We get the coordinates of the rectangle
    image = frame[y:y + h, x:x + w]  # We get the image of the rectangle

    mean_bgr = compute_mean_bgr(image)  # We compute the mean BGR values of the rectangle

    # Write the mean BGR values in a file
    if write_mean_bgr:
        write_mean_bgr_value(rect, mean_bgr)

    determine_color(ColorDice(mean_bgr, rect))  # We determine the color of the rectangle (it modifies the colors dictionary)


def determine_color(color_dice):
    """
    Determine the colors of the dice on the image. We try to find the color with the minimum distance between the mean
    BGR values and the BGR values of each color. There may be conflicts between the colors, and in this case, we
    keep the better one, and we recall the function with the other one.

    Args:
        color_dice (ColorDice): ColorDice object representing the dice

    Returns:
        (dict) : Dictionary of the ColorDice objects
    """
    # The BGR values of each color (observation)
    bgr_values = {'yellow': (49, 113, 149), 'orange': (44, 66, 169), 'red': (50, 35, 111),
                  'dark_yellow': (41, 73, 121), 'green': (70, 93, 41), 'black': (44, 38, 39)}

    # Calculate the distance between the mean BGR values and the BGR values of each color if necessary
    if not color_dice.distances:
        color_dice.distances = {}  # Format: {name_color: distance}
        for name, bgr in bgr_values.items():
            color_dice.distances[name] = np.linalg.norm(color_dice.color - bgr)

    if color_dice.bad_colors is None:  # If we don't have any bad colors for the dice
        # We simply get the color with the minimum distance
        name_color = min(color_dice.distances, key=color_dice.distances.get)  # We get the color with the minimum distance

    else:  # If we know the dice has some colors that are not possible
        # We get the color with the minimum distance, except the bad colors
        min_distance = None
        name_color = ''
        for name, distance in color_dice.distances.items():
            if name not in color_dice.bad_colors and (min_distance is None or distance < min_distance):
                min_distance = distance
                name_color = name
        if min_distance is None:  # If we didn't find any color, we reject this color and exit the function
            return

    # We check if the color is already in the list
    if name_color not in colors:
        colors[name_color] = color_dice  # We add the color to the list if it is not in it
    else:
        # We check what dice has the closest mean_bgr to the BGR value we want
        if np.linalg.norm(colors[name_color].color - bgr_values[name_color]) > np.linalg.norm(color_dice.color - bgr_values[name_color]):
            # If the new dice is closer to the color we want, we replace the old dice by the new one
            old_dice = colors[name_color]
            colors[name_color] = color_dice

            # We restart the function with the old dice
            old_dice.bad_colors.append(name_color)
            determine_color(old_dice)
        else:
            # If the old dice is closer to the color we want, we restart the function with the new dice
            color_dice.bad_colors.append(name_color)
            determine_color(color_dice)


def write_mean_bgr_value(rect, mean_bgr):
    """
    Write the mean BGR values of the dice at the center of the image in the file mean_bgr

    Args:
        rect (tuple): Coordinates of the rectangle (x, y, w, h)
        mean_bgr (numpy.ndarray): Mean BGR values of the dice
    """
    global file_write_mean_bgr

    if file_write_mean_bgr is None:
        file_write_mean_bgr = open(PATH_DATA + 'mean_bgr', 'a')  # The file in which we will write the parameters

    rect_detection = (250, 150, 150, 150)
    draw_rectangle(rect_detection, color=(0, 255, 0), thickness=1)
    if overlapping_rectangles(rect, rect_detection, area_threshold=0.1):
        draw_rectangle(rect, color=(255, 0, 0), thickness=20)
        file_write_mean_bgr.write(f'{mean_bgr[0]} {mean_bgr[1]} {mean_bgr[2]}\n')


def draw_score(color, final_score):
    """
    Find the score of the dice
    """
    # The BGR values of each color (real)
    real_bgr_values = {'yellow': (0, 255, 255), 'orange': (0, 102, 204), 'red': (0, 0, 204),
                       'dark_yellow': (0, 152, 152), 'green': (0, 204, 0), 'black': (0, 0, 0)}

    rect = x, y, w, h = colors[color].rect  # We get the coordinates of the rectangle
    image = frame[y:y + h, x:x + w]  # We get the image of the rectangle

    if np.size(image) == 0:  # If the image is empty, we don't do anything
        return None

    # We draw the rectangle on the image
    draw_rectangle((x, y, w, h), real_bgr_values[color])

    score = determine_score(image, rect, color, scores_colors[color])  # We determine the score of the dice

    if color in final_score:
        final_score[color] = score  # We add the score to the final score

    # We write the value of the dice on the image
    cv2.putText(frame_view, f'Score: {score}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 50, 50), 2)


def determine_score(image, rect, color, scores, len_memory=40):
    """
    Determine the score of the dice

    Args:
        image (numpy.ndarray): Image of the dice
        rect (tuple): Coordinates of the rectangle (x, y, w, h)
        color (str): Color of the dice
        scores (list): List of the previous scores of the dice
        len_memory (int): Number of previous scores to keep in memory

    Returns:
        (int): Score of the dice
    """

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert the image to grayscale
    circles = find_circles(gray_image, color)  # We find the circles on the image

    # Optimize the parameters of the HoughCircles function if necessary
    if count_iterations == wait_optimize and optimize_hough_circle:
        if color in theorical_values:
            optimize_parameters(gray_image, color, rect)

    if circles:
        score = len(circles)  # We count the number of circles

        # We convert the coordinates of the circles to the coordinates of the window
        circles_to_draw = []
        for circle in circles:
            circles_to_draw.append((circle[0] + rect[0], circle[1] + rect[1], circle[2]))

        # We draw the circles
        draw_circle(circles_to_draw)
    else:
        score = random.randint(1, 6)  # If we don't find any circle, we choose a random number between 1 and 6

    if score > 6:
        score = 6

    scores.append(score)  # We add the score to the list of scores
    if len(scores) > len_memory:
        scores.pop(0)  # We remove the first score

    # We find the number the most present in the list of scores
    score = max(set(scores), key=scores.count)

    return score


def find_circles(gray_image, color):
    """
    Find the circles in the image

    Args:
        gray_image (numpy.ndarray): Image of the dice in grayscale
        color (str): Color of the dice

    Returns:
        (list): List of circles
    """
    circles = []
    circles = add_circles(circles, gray_image)

    blur_image = cv2.medianBlur(gray_image, 3)  # We blur the image
    circles = add_circles(circles, blur_image)

    canny_image = cv2.Canny(gray_image, 50, 120)  # We apply the Canny filter to the image
    circles = add_circles(circles, canny_image)

    # We add the circle from the memory
    circles = add_circle_from_memory(circles, color)

    update_memory(memory_circles[color])

    return circles


def add_circles(actual_circles, image):
    """
    Find new circles with the houghCircle function and add them to the list of circles

    Args:
        actual_circles (list): List of circles
        image (numpy.ndarray): Image of the dice

    Returns:
        (list): List of circles with the new circles
    """
    new_circles = cv2.HoughCircles(image=image, method=cv2.HOUGH_GRADIENT, dp=param_dp / 10, minDist=3,
                                   param1=param_1, param2=param_2, minRadius=0, maxRadius=max_radius_circle)

    if new_circles is not None:
        # Transform the circles to a list of tuple instead of numpy.ndarray of numpy.ndarray (to be able to add them to a dictionary like a key)
        new_circles = [tuple(new_circle.tolist()) for new_circle in new_circles[0, :]]

        # We add the new circles to the list of circles
        for circle_to_add in new_circles:
            circle_already_in_list = False  # Boolean to know if the circle is already in the list

            for circle in actual_circles:  # We look if the circle is already in the list
                if circles_too_close(circle, circle_to_add):
                    circle_already_in_list = True
                    break

            if not circle_already_in_list:
                actual_circles.append(circle_to_add)

    return actual_circles


def add_circle_from_memory(circles, color, lifetime=30):
    """
    Add the circles from the memory to the list of circles

    Args:
        circles (list): List of circles
        color (str): Color of the dice
        lifetime (int): Lifetime of the circles in the memory when they are detected
    """
    new_circles = list(memory_circles[color].keys())  # List of circles to add to the list of circles

    # We look at each circle
    for circle in circles:
        circle_already_in_memory = False  # Boolean to know if the circle is already in the memory

        # We look if the circle is already in the memory
        for memory_circle in memory_circles[color]:
            if circles_too_close(circle, memory_circle):
                circle_already_in_memory = True
                memory_circles[color][memory_circle] = lifetime
                break

        if not circle_already_in_memory:
            new_circles.append(circle)
            memory_circles[color][circle] = lifetime  # We add the circle to the memory

    return new_circles


def optimize_parameters(image, color, rect):
    """
    Optimize the parameters of the HoughCircles function by testing different values and printing the results
    Args:
        image (numpy.ndarray): Image on which to optimize the parameters (must be in grayscale)
        color (str): Color of the dice
        rect (tuple): Coordinates of the rectangle
    """
    for p1 in range(p1_min, p1_max + 1):
        print(p1)
        for p2 in range(p2_min, p2_max + 1):
            for dp in range(dp_min, dp_max + 1):
                if p1 > p2:
                    optimize_hough_circles(image, color, rect, p1, p2, dp)


def optimize_hough_circles(image, color, rect, p1, p2, dp):
    """
    Run the HoughCircles function with the given parameters and verify if the result is correct to save the parameters
    in dictionaries

    Args:
        image (numpy.ndarray): Image on which to optimize the parameters (must be in grayscale)
        color (str): Color of the dice
        rect (tuple): Coordinates of the rectangle
        p1 (int): First parameter of the HoughCircles function
        p2 (int): Second parameter of the HoughCircles function
        dp (int): Third parameter of the HoughCircles function
    """
    c = cv2.HoughCircles(image=image, method=cv2.HOUGH_GRADIENT, dp=dp / 10, minDist=5, param1=p1, param2=p2,
                         minRadius=1, maxRadius=max_radius_circle)
    if c is not None and verif_coordinates(c[0, :], rect, theorical_coordinates[color]):
        if p1 not in dict_p1_opti:
            dict_p1_opti[p1] = 1
        else:
            dict_p1_opti[p1] += 1
        if p2 not in dict_p2_opti:
            dict_p2_opti[p2] = 1
        else:
            dict_p2_opti[p2] += 1
        if dp not in dict_dp_opti:
            dict_dp_opti[dp] = 1
        else:
            dict_dp_opti[dp] += 1


def display_dictionaries_optimization():
    """
    Sort the dictionaries of the optimization of the parameters of the HoughCircles function
    """
    global dict_p1_opti, dict_p2_opti, dict_dp_opti

    # We sort the dictionaries
    dict_p1_opti = {k: v for k, v in sorted(dict_p1_opti.items(), key=lambda item: item[1], reverse=True)}
    dict_p2_opti = {k: v for k, v in sorted(dict_p2_opti.items(), key=lambda item: item[1], reverse=True)}
    dict_dp_opti = {k: v for k, v in sorted(dict_dp_opti.items(), key=lambda item: item[1], reverse=True)}

    # We create the file
    with open(PATH_DATA + 'optimization', 'w') as file_write:
        # We print the dictionaries
        file_write.write(f'p1 : {dict_p1_opti}\np2 : {dict_p2_opti}\ndp : {dict_dp_opti}')


def draw_rectangle(rectangle, color=(0, 0, 0), thickness=3):
    """
    Draw the rectangles on the frame used to view things

    Args:
        rectangle (tuple or list of tuple): The rectangle or the rectangles
        color (tuple): The color of the rectangle
        thickness (int): The thickness of the rectangle
    """
    if type(rectangle) == tuple:
        rectangle = [rectangle]
    for rect in rectangle:
        x, y, w, h = rect
        cv2.rectangle(frame_view, (x, y), (x + w, y + h), color, thickness)


def draw_circle(circles):
    """
    Draw the circles on the frame used to view things

    Args:
        circles (list): The circles to draw
    """
    for circle in circles:
        # Draw the outer circle
        cv2.circle(frame_view, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 255, 0), 2)
        # Draw the center of the circle
        cv2.circle(frame_view, (int(circle[0]), int(circle[1])), 2, (0, 0, 255), 3)


def display_frame(rect_window):
    """
    Display the frame on the window

    Args:
        rect_window (pygame.rect.Rect) : The rectangle of the window
    """
    image_rgb = cv2.cvtColor(frame_view, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
    image_pygame = pygame.surfarray.make_surface(image_rgb)  # Convert the image to a pygame image
    image_turned = pygame.transform.rotate(image_pygame, -90)  # Rotate the image
    image = pygame.transform.flip(image_turned, True, False)  # Flip the image
    image = pygame.transform.scale(image, (rect_window.width, rect_window.height))  # Resize the image
    var.WINDOW.blit(image, rect_window)  # We display the frame on the window
    pygame.draw.rect(var.WINDOW, (1, 1, 1), rect_window, 2)  # We draw a rectangle on the window
    var.WINDOW.blit(var.LARGE_FONT.render("Cliquez n'importe où pour quitter cette fenêtre", True, (255, 0, 255)),
                    convert_to_new_window((440, 600)))  # Text of the selected dice
    pygame.display.flip()  # We update the window


def end_capture_dice(final_score):
    """
    End the capture of the dice

    Args:
        final_score (dict): Final score of the dice

    Returns:
        (list) : The scores of the dice
    """
    cv2.destroyAllWindows()  # Close all windows

    return list(final_score.values())
