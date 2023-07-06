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
param_thresh = {"yellow": 80, "orange": 120, "red": 100, "dark_yellow": 50, "green": 125, "black": 25}

# The BGR values of each color (observation)
bgr_values = {"yellow": (255, 255, 0), "orange": (52, 107, 165), "red": (70, 105, 140), "dark_yellow": (40, 75, 110), "green": (65, 128, 49), "black": (38, 38, 38), "white": (150, 130, 126)}

# The BGR values of each color (real)
real_bgr_values = {"yellow": (0, 220, 220), "orange": (0, 102, 204), "red": (0, 0, 204), "dark_yellow": (25, 170, 240), "green": (0, 204, 0), "black": (0, 0, 0), "white": (255, 255, 255)}

# The last scores we stored for each color (used to compare with the new scores to avoid changing the score too often)
scores_colors = {"yellow": [], "orange": [], "red": [], "dark_yellow": [], "green": [], "black": []}

# The rects kept in memory (when we detect a rectangle, if it overlaps with a rectangle in memory, we display the rectangle in memory)
memory_rects = {}  # Format : {rect : counter} (counter is initialized to a certain value and decreases each frame, if it reaches 0, we delete the rect)

# The scores we will return, initialized to random values(65, 128, 49)
final_score = {"yellow": random.randint(1, 6), "orange": random.randint(1, 6), "red": random.randint(1, 6),
               "dark_yellow": random.randint(1, 6), "green": random.randint(1, 6), "black": random.randint(1, 6)}


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


def find_rectangles(image, rectangles):
    """
    Find the rectangles on the image

    Args:
        image (numpy.ndarray): Image on which to find the rectangles
        rectangles (list): List of rectangles to draw
    """
    for (str_color, value) in param_thresh.items():  # For each color we have a threshold_color

        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
        gray_img = cv2.medianBlur(gray_img, 5)  # We apply a median blur to the image to erase useless details

        # We apply a threshold to the image : it turns the image into a black and white image
        thresh = cv2.threshold(gray_img, value, 255, cv2.THRESH_BINARY_INV)[1]

        if str_color == 'yellow':
            # show_image(thresh)
            pass

        # We create a kernel to close the edges (a rectangular structuring element of size 9x9)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        detected_edges = cv2.Canny(gray_img, 9, 150, 3)  # Detect edges from the gray image
        close = cv2.morphologyEx(detected_edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice
        contours_1, _ = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # We find the contours of the image

        detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges from the threshold image
        close = cv2.morphologyEx(detected_edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice
        contours_2, _ = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # We find the contours of the image

        contours = contours_1 + contours_2  # We merge the contours found by the two methods

        min_size = 40  # Minimum size of the rectangle
        max_size = 95  # Maximum size of the rectangle

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)  # We get the coordinates of the rectangle
            if min_size < w < max_size and min_size < h < max_size:  # If the rectangle is not too big or too small

                # We check if the rectangle is already in the list
                rect_in_list = False
                for rect in rectangles:
                    if overlapping_rectangles(rect, (x, y, w, h), area_threshold=0.7):
                        rect_in_list = True
                        break

                # We check if the rectangle is in the memory to avoid changing rectangle at each frame
                if not rect_in_list:
                    # We check if the rectangle is in the memory
                    rect_in_memory = False
                    rect_to_delete = []  # List of rectangles to delete from the memory after the loop
                    for rect in memory_rects:
                        if overlapping_rectangles(rect, (x, y, w, h), area_threshold=0.9):  # If the rectangle is in the memory
                            rect_in_memory = True
                            x, y, w, h = rect  # We replace the current rectangle by the one in the memory
                            break
                        elif memory_rects[rect] == 0:  # If the rectangle is not in the memory anymore
                            rect_to_delete.append(rect)  # We add the rectangle to the list of rectangles to delete
                        else:
                            memory_rects[rect] -= 1  # We decrease the number of times the rectangle is in the memory
                            rectangles.append(rect)  # We add the rectangle to the list

                    # We delete the rectangles that are not in the memory anymore
                    for rect in rect_to_delete:
                        del memory_rects[rect]

                    if not rect_in_memory:
                        memory_rects[(x, y, w, h)] = 20  # We add the rectangle to the memory

                    rectangles.append((x, y, w, h))  # We add the rectangle to the list


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

    # Calculate the distance between the mean BGR values and the BGR values of each color
    distances = {}
    for color, bgr in bgr_values.items():
        if color != bad_color:
            distances[color] = np.linalg.norm(mean_bgr - bgr)

    # We get the color with the minimum distance
    color = min(distances, key=distances.get)

    if color != 'white':
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
    rect_window = pygame.rect.Rect(convert_to_new_window((425, 175, 640, 480)))

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can change it if you have multiple cameras

    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        rectangles = []  # List of the rectangles on the image
        find_rectangles(frame, rectangles)  # Find the rectangles on the image

        # Draw the rectangles on the image
        # draw_rectangle(frame, rectangles)

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
            draw_rectangle(frame, (x, y, w, h), real_bgr_values[color])

            score = determine_score(img_rect, color, scores_colors[color])  # We determine the score of the dice
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

        # Detect a click on the window
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


def draw_rectangle(frame, rectangle, color=(0, 0, 0)):
    """
    Draw the rectangles on the frame

    Args:
        frame (numpy.ndarray): The frame
        rectangle (tuple or list of tuple): The rectangle or the rectangles
        color (tuple): The color of the rectangle
    """
    if type(rectangle) == tuple:
        rectangle = [rectangle]
    for rect in rectangle:
        x, y, w, h = rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 5)


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