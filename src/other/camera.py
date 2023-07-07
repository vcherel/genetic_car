from src.other.utils import overlapping_rectangles, convert_to_new_window  # Utils functions
from src.render.dice_menu import save_camera_frame  # To save the camera frame
from src.render.display import draw_circle  # To draw the circles
import matplotlib.pyplot as plt  # To show images
import src.other.variables as var  # Variables
import random  # To generate random numbers
import numpy as np  # To use numpy
import pygame  # To use Pygame
import cv2  # To use OpenCV

"""
This file contains the functions used to get the score of the dice from the camera with OpenCV
"""

# The parameters of the threshold to make a black and white image for each color
param_thresh = {'yellow': 80, 'orange': 120, 'red': 100, 'dark_yellow': 50, 'green': 125, 'black': 25}

# The BGR values of each color (observation)
bgr_values = {'yellow': (125, 155, 175), 'orange': (114, 115, 183), 'red': (124, 108, 149), 'dark_yellow': (106, 110, 137), 'green': (127, 128, 92), 'black': (119, 102, 104)}
# 'white': (163, 111, 102)

# The BGR values of each color (real)
real_bgr_values = {'yellow': (0, 255, 255), 'orange': (0, 102, 204), 'red': (0, 0, 204), 'dark_yellow': (0, 152, 152), 'green': (0, 204, 0), 'black': (0, 0, 0)}

# The last scores we stored for each color (used to compare with the new scores to avoid changing the score too often)
scores_colors = {'yellow': [], 'orange': [], 'red': [], 'dark_yellow': [], 'green': [], 'black': []}

# The rects kept in memory (when we detect a rectangle, if it overlaps with a rectangle in memory, we display the rectangle in memory)
memory_rects = {}  # Format : {rect : lifetime_remaining}
# lifetime_remaining : the number of frames the rectangle will be displayed unless it is detected again
# bool : True if the rectangle has been detected again, False otherwise

# The scores we will return, initialized to random values(65, 128, 49)
final_score = {'yellow': random.randint(1, 6), 'orange': random.randint(1, 6), 'red': random.randint(1, 6),
               'dark_yellow': random.randint(1, 6), 'green': random.randint(1, 6), 'black': random.randint(1, 6)}

frame = np.empty([2, 2])  # The frame of the camera

file_write = open(var.PATH_DATA + '/mean_bgr', 'a')  # The file in which we will write the parameters


def optimize_parameters(image, value):
    """
    Optimize the parameters of the HoughCircles function by testing different values and printing the results
    Args:
        image (numpy.ndarray): Image on which to optimize the parameters
        value (int): Number of circles to detect
    """
    dico_p1 = {}
    dico_p2 = {}
    dico_dp = {}

    for p1 in range(150, 151):
        print(p1)
        for p2 in range(52, 53):
            for dp in range(68, 69):
                if p1 > p2:
                    c = cv2.HoughCircles(image=image, method=cv2.HOUGH_GRADIENT, dp=dp / 10, minDist=1, param1=p1, param2=p2, minRadius=1, maxRadius=15)
                    if c is not None and len(c[0, :]) == value:
                        if p1 not in dico_p1:
                            dico_p1[p1] = 1
                        else:
                            dico_p1[p1] += 1
                        if p2 not in dico_p2:
                            dico_p2[p2] = 1
                        else:
                            dico_p2[p2] += 1
                        if dp not in dico_dp:
                            dico_dp[dp] = 1
                        else:
                            dico_dp[dp] += 1

    # We sort the dictionaries
    dico_p1 = {k: v for k, v in sorted(dico_p1.items(), key=lambda item: item[1], reverse=True)}
    dico_p2 = {k: v for k, v in sorted(dico_p2.items(), key=lambda item: item[1], reverse=True)}
    dico_dp = {k: v for k, v in sorted(dico_dp.items(), key=lambda item: item[1], reverse=True)}

    print(dico_p1, dico_p2, dico_dp)


def find_rectangles():
    """
    Find the rectangles on the frame of the camera

    Returns:
        list: The list of rectangles found
    """
    contours = find_contours(frame)  # We find the contours
    rectangles = check_contours_validity(contours)  # We check the validity of the contours
    rectangles = add_rect_from_memory(rectangles)  # We add the rectangles from the memory
    update_memory_rect()  # We update the memory of the rectangles (we decrease the lifetime of the rectangles)
    rectangles = check_overlapping_rectangles(rectangles)  # We check the overlapping rectangles

    return rectangles


def find_contours(image):
    """
    Find the contours of the dice on the image

    Args:
        image (numpy.ndarray): Image on which to find the contours

    Returns:
        list: The list of contours found
    """
    contours = []  # The list of contours found
    for (str_color, value) in param_thresh.items():  # For each color we have a threshold_color

        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
        gray_img = cv2.medianBlur(gray_img, 5)  # We apply a median blur to the image to erase useless details

        # We apply a threshold to the image : it turns the image into a black and white image
        thresh = cv2.threshold(gray_img, value, 255, cv2.THRESH_BINARY_INV)[1]

        if str_color == 'yellow':
            # show_image(thresh)
            pass

        # We create a kernel to close the edges of the dice
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        edges_1 = cv2.Canny(gray_img, 9, 150, 3)  # Detect edges from the gray image
        edges_2 = cv2.Canny(thresh, 9, 150, 3)  # Detect edges from the threshold image

        for edges in [edges_1, edges_2]:
            close = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice
            contour_found, _ = cv2.findContours(close, cv2.RETR_TREE,
                                                cv2.CHAIN_APPROX_SIMPLE)  # We find the contours of the image
            contours += contour_found  # We merge the contours found by the two methods

    return contours


def check_contours_validity(contours):
    """
    Verify that the rectangle is not too big or too small, and that it is not too close to the edge of the image

    Args:
        contours (list): List of contours found

    Returns:
        list: List of rectangles found
    """
    rectangles = []  # List of rectangles
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)  # We get the coordinates of the rectangle
        min_size = 40  # Minimum size of the rectangle
        max_size = 95  # Maximum size of the rectangle
        if min_size < w < max_size and min_size < h < max_size:  # If the rectangle is not too big or too small
            # Check if the rectangle is not too close to the edge of the image
            if x > 5 and y > 5 and x + w < 635 and y + h < 475:
                rectangles.append((x, y, w, h))

    return rectangles


def add_rect_from_memory(rectangles):
    """
    Add the rectangles from the memory to the list of rectangles

    Args:
        rectangles (list): List of rectangles found

    Returns:
        list: List of rectangles found
    """
    new_rectangles = []

    for memory_rect in memory_rects:
        new_rectangles.append(memory_rect)
        for rect in rectangles:
            if overlapping_rectangles(rect, memory_rect, area_threshold=0.8):
                memory_rects[memory_rect] = 20  # We reset the lifetime of the rectangle
                break

    for rect in rectangles:
        new_rectangles.append(rect)
        memory_rects[rect] = 20  # We add the rectangle to the memory

    return new_rectangles


def update_memory_rect():
    """
    Update the memory of the rectangles (we decrease the lifetime of the rectangles and delete the old ones)
    """
    # We update the lifetime of the rectangles in memory
    memory_rect_to_delete = []
    for rect in memory_rects:
        memory_rects[rect] -= 1  # We decrease the number of times the rectangle is in the memory
        if memory_rects[rect] == 0:  # If the rectangle is not in the memory anymore
            memory_rect_to_delete.append(rect)  # We add the rectangle to the list of rectangles to delete

    # We delete the rectangles from the memory
    for rect in memory_rect_to_delete:
        del memory_rects[rect]


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
            if overlapping_rectangles(rect, new_rect, area_threshold=0.5):
                # If the rectangles are overlapping, we take the biggest one
                overlapping = True
                if rect[2] * rect[3] > new_rect[2] * new_rect[3]:
                    new_rectangles.remove(new_rect)
                    new_rectangles.append(rect)
                break

        if not overlapping:
            new_rectangles.append(rect)

    return new_rectangles


def determine_colors(image, rect, colors, bad_color=None, mean_bgr=None):
    """
    Determine the colors of the dice on the image

    Args:
        image (numpy.ndarray): Image of the dice
        rect (tuple): Coordinates of the rectangle (x, y, w, h)
        colors (dict) : Dictionary of the colors {color_1: ((B, G, R), rect), color_2: ((B, G, R), rect), ...}
        bad_color (str): Color that was misplaced and that we want to find what the color should be
        mean_bgr (tuple): Mean BGR values of the dice

    Returns:
        (str): Color of the dice
    """
    # If we don't have the mean BGR values of the dice, we calculate it
    if mean_bgr is None:
        # Convert the image to a numpy array
        image_array = np.array(image)

        # Calculate the mean BGR values
        mean_bgr = np.mean(image_array, axis=(0, 1))

        # Write the mean BGR values in a file
        # write_mean_bgr_value(rect, mean_bgr)

    # Calculate the distance between the mean BGR values and the BGR values of each color
    distances = {}
    for color, bgr in bgr_values.items():
        if color != bad_color:
            distances[color] = np.linalg.norm(mean_bgr - bgr)

    # We get the color with the minimum distance
    color = min(distances, key=distances.get)

    # We check if the color is already in the dictionary
    if color not in colors:
        colors[color] = (mean_bgr, rect)  # We add the color to the dictionary if it is not in it
    else:
        # We check what rect has the closest mean_bgr to the BGR value we want
        if np.linalg.norm(colors[color][0] - bgr_values[color]) > np.linalg.norm(mean_bgr - bgr_values[color]):
            # We memorize the rect that was misplaced to change it of place
            value_to_change = colors[color]
            bad_color = color  # List of the colors that don't correspond to the rect

            colors[color] = (mean_bgr, rect)  # We save the good rect in the dictionary

            # We call the function again to find the color of the rect that was misplaced
            colors = determine_colors(image, value_to_change[1], colors, bad_color, value_to_change[0])

    return colors


def write_mean_bgr_value(rect, mean_bgr):
    """
    Write the mean BGR values of the dice at the center of the image in the file mean_bgr

    Args:
        rect (tuple): Coordinates of the rectangle (x, y, w, h)
        mean_bgr (numpy.ndarray): Mean BGR values of the dice
    """
    rect_detection = (250, 150, 150, 150)
    draw_rectangle(rect_detection, color=(0, 255, 0), thickness=1)
    if overlapping_rectangles(rect, rect_detection, area_threshold=0.1):
        draw_rectangle(rect, color=(255, 0, 0), thickness=20)
        file_write.write(f'{mean_bgr[0]} {mean_bgr[1]} {mean_bgr[2]}\n')



def determine_score(image, color, scores):
    """
    Determine the score of the dice

    Args:
        image (numpy.ndarray): Image of the dice
        color (str): Color of the dice
        scores (list): List of the previous scores of the dice

    Returns:
        (int): Score of the dice
    """
    thresh = cv2.threshold(image, param_thresh[color], 255, cv2.THRESH_BINARY_INV)[1]  # Black and white image

    detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges

    # Find the circles in the image (corresponding to the points of the dice)
    circles = cv2.HoughCircles(image=detected_edges, method=cv2.HOUGH_GRADIENT, dp=6.8, minDist=1,
                               param1=150, param2=68, minRadius=1, maxRadius=5)

    # This part is used to optimize the parameters of the HoughCircles function
    """
    global counter
    counter += 1
    if counter > 60:
        counter = 0
        optimize_parameters(detected_edges, 5)
    """

    if circles is not None:
        circles = circles[0, :]  # The array is in an array, we take the first element

        score = len(circles)  # We count the number of circles
        for circle in circles:
            draw_circle(circle, image)
    else:
        score = random.randint(1, 6)  # If we don't find any circle, we choose a random number between 1 and 6

    if score > 6:
        score = 6

    scores.append(score)  # We add the score to the list of scores
    if len(scores) > 1000:
        scores.pop(0)  # We remove the first score

    # We find the number the most present in the list of scores
    score = max(set(scores), key=scores.count)

    return score


def capture_dice():
    """
    Main program

    Returns:
        (dict) : The scores of the dice
    """
    global frame

    rect_window = pygame.rect.Rect(convert_to_new_window((425, 175, 640, 480)))

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can change it if you have multiple cameras

    while True:
        _, frame = cap.read()  # Read a frame from the camera

        rectangles = find_rectangles()  # Find the rectangles on the image

        # Draw the rectangles on the image
        draw_rectangle(rectangles, thickness=1)

        # We take in memory for each color the bgr color and the rectangle to prevent 2 colors from being the same
        colors = {}  # Format: {color: (bgr, rect)}

        for rect in rectangles:
            x, y, w, h = rect
            img_rect = frame[y:y+h, x:x+w]  # We get the image of the rectangle
            colors = determine_colors(img_rect, rect, colors)  # We determine the color of the rectangle

        for color in colors:
            x, y, w, h = colors[color][1]  # We get the coordinates of the rectangle
            img_rect = frame[y:y+h, x:x+w]  # We get the image of the rectangle

            # We draw the rectangle on the image
            draw_rectangle((x, y, w, h), real_bgr_values[color])

            score = determine_score(img_rect, color, scores_colors[color])  # We determine the score of the dice

            if color in final_score:
                final_score[color] = score  # We add the score to the final score

            # We write the value of the dice on the image
            cv2.putText(frame, f'score: {score}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # We display the frame on the window
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
        image_pygame = pygame.surfarray.make_surface(image_rgb)  # Convert the image to a pygame image
        image_turned = pygame.transform.rotate(image_pygame, -90)  # Rotate the image
        image = pygame.transform.flip(image_turned, True, False)  # Flip the image
        image = pygame.transform.scale(image, (rect_window.width, rect_window.height))  # Resize the image
        var.WINDOW.blit(image, rect_window)  # We display the frame on the window
        pygame.draw.rect(var.WINDOW, (1, 1, 1), rect_window, 2)  # We draw a rectangle on the window
        var.WINDOW.blit(var.LARGE_FONT.render("Cliquez n'importe où pour quitter cette fenêtre", True, (255, 0, 255)), convert_to_new_window((440, 600)))  # Text of the selected dice
        pygame.display.flip()  # We update the window

        # Detect a click on the window to stop the program
        click = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                break

        if click:  # We stop the program after a click
            var.WINDOW.blit(var.BACKGROUND, rect_window, rect_window)  # We erase the window
            break

    cap.release()  # Release the VideoCapture object
    cv2.destroyAllWindows()  # Close all windows

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
    save_camera_frame(frame)  # Save the image into the variables (CAMERA_FRAME and RECT_CAMERA_FRAME)

    return list(final_score.values())


def draw_rectangle(rectangle, color=(0, 0, 0), thickness=3):
    """
    Draw the rectangles on the frame

    Args:
        rectangle (tuple or list of tuple): The rectangle or the rectangles
        color (tuple): The color of the rectangle
        thickness (int): The thickness of the rectangle
    """
    if type(rectangle) == tuple:
        rectangle = [rectangle]
    for rect in rectangle:
        x, y, w, h = rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, thickness)


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