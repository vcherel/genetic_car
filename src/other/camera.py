from src.other.utils import overlapping_rectangles, convert_to_new_window  # Utils functions
from src.other.data_structures import ColorDice  # To find the color of each dice
from src.render.dice_menu import save_camera_frame  # To save the camera frame
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
param_thresh = {'yellow': 170, 'orange': 90, 'red': 60, 'dark_yellow': 100, 'green': 80, 'black': 20}

# The BGR values of each color (observation)
bgr_values = {'yellow': (49, 113, 149), 'orange': (44, 66, 169), 'red': (50, 35, 111), 'dark_yellow': (41, 73, 121), 'green': (70, 93, 41), 'black': (44, 38, 39)}
# , 'purple': (112, 96, 107), 'dark_green': (119, 101, 86)

# The BGR values of each color (real)
real_bgr_values = {'yellow': (0, 255, 255), 'orange': (0, 102, 204), 'red': (0, 0, 204), 'dark_yellow': (0, 152, 152), 'green': (0, 204, 0), 'black': (0, 0, 0)}
# , 'purple': (100, 0, 50), 'dark_green': (0, 102, 0)

# The last scores we stored for each color (used to compare with the new scores to avoid changing the score too often)
scores_colors = {'yellow': [], 'orange': [], 'red': [], 'dark_yellow': [], 'green': [], 'black': []}
# , 'purple': [], 'dark_green': []

# The rects kept in memory (when we detect a rectangle, if it overlaps with a rectangle in memory, we display the rectangle in memory)
memory_rects = {}  # Format : {rect : lifetime_remaining}
# lifetime_remaining : the number of frames the rectangle will be displayed unless it is detected again
# bool : True if the rectangle has been detected again, False otherwise

# The scores we will return, initialized to random values(65, 128, 49)
final_score = {'yellow': random.randint(1, 6), 'orange': random.randint(1, 6), 'red': random.randint(1, 6),
               'dark_yellow': random.randint(1, 6), 'green': random.randint(1, 6), 'black': random.randint(1, 6)}

frame = np.empty([2, 2])  # The frame of the camera


write_mean_bgr = False
file_write = open(var.PATH_DATA + '/mean_bgr', 'a')  # The file in which we will write the parameters


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
        colors = {}  # List of the colors of the dice (key: name_color, value: ColorDice)

        for rect in rectangles:
            x, y, w, h = rect  # We get the coordinates of the rectangle
            image = frame[y:y+h, x:x+w]  # We get the image of the rectangle

            mean_bgr = compute_mean_bgr(image)  # We compute the mean BGR values of the rectangle

            # Write the mean BGR values in a file
            if write_mean_bgr:
                write_mean_bgr_value(rect, mean_bgr)

            colors = determine_colors(ColorDice(mean_bgr, rect), colors)  # We determine the color of the rectangle

        for color in colors:
            rect = x, y, w, h = colors[color].rect  # We get the coordinates of the rectangle
            image = frame[y:y+h, x:x+w]  # We get the image of the rectangle

            # We draw the rectangle on the image
            draw_rectangle((x, y, w, h), real_bgr_values[color])

            score = determine_score(image, rect, color, scores_colors[color])  # We determine the score of the dice

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
            pos = pygame.mouse.get_pos()
            pos = (pos[0] - rect_window.x, pos[1] - rect_window.y)
            # Print the color of the pixel
            # print(frame[pos[1], pos[0]])
            var.WINDOW.blit(var.BACKGROUND, rect_window, rect_window)  # We erase the window
            break

    cap.release()  # Release the VideoCapture object
    cv2.destroyAllWindows()  # Close all windows

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert the image to RGB
    save_camera_frame(frame)  # Save the image into the variables (CAMERA_FRAME and RECT_CAMERA_FRAME)

    return list(final_score.values())


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
    rectangles = add_offset_to_rectangles(rectangles)  # We add an offset to the rectangles
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
        min_size = 35  # Minimum size of the rectangle
        max_size = 80  # Maximum size of the rectangle
        if min_size < w < max_size and min_size < h < max_size:  # If the rectangle is not too big or too small
            # Check if the rectangle is not too close to the edge of the image
            if x > 5 and y > 5 and x + w < 635 and y + h < 475:
                rectangles.append((x, y, w, h))

    return rectangles


def add_offset_to_rectangles(rectangles):
    """
    Add an offset to the rectangles

    Args:
        rectangles (list): List of rectangles found

    Returns:
        list: List of rectangles found
    """
    offset = 7  # Offset to add to the rectangles
    new_rectangles = []
    for rectangle in rectangles:
        x, y, w, h = rectangle
        new_rectangles.append((x - offset, y - offset, w + 2 * offset, h + 2 * offset))

    return new_rectangles



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
            # If we find a rect that is already in the memory, we reset the lifetime of the rectangle
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


def determine_colors(color_dice, dict_color_dice):
    """
    Determine the colors of the dice on the image. We try to find the color with the minimum distance between the mean
    BGR values and the BGR values of each color. There may be conflicts between the colors, and in this case, we
    keep the better one, and we recall the function with the other one.

    Args:
        color_dice (ColorDice): ColorDice object representing the dice
        dict_color_dice (dict): Dictionary of the ColorDice objects, with the name of the color as key

    Returns:
        (dict) : Dictionary of the ColorDice objects
    """
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
            return dict_color_dice

    # We check if the color is already in the list
    if name_color not in dict_color_dice:
        dict_color_dice[name_color] = color_dice  # We add the color to the list if it is not in it
    else:
        # We check what dice has the closest mean_bgr to the BGR value we want
        if np.linalg.norm(dict_color_dice[name_color].color - bgr_values[name_color]) > np.linalg.norm(color_dice.color - bgr_values[name_color]):
            # If the new dice is closer to the color we want, we replace the old dice by the new one
            old_dice = dict_color_dice[name_color]
            dict_color_dice[name_color] = color_dice

            # We restart the function with the old dice
            old_dice.bad_colors.append(name_color)
            dict_color_dice = determine_colors(old_dice, dict_color_dice)
        else:
            # If the old dice is closer to the color we want, we restart the function with the new dice
            color_dice.bad_colors.append(name_color)
            dict_color_dice = determine_colors(color_dice, dict_color_dice)

    return dict_color_dice


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


def determine_score(image, rect, color, scores):
    """
    Determine the score of the dice

    Args:
        image (numpy.ndarray): Image of the dice
        rect (tuple): Coordinates of the rectangle (x, y, w, h)
        color (str): Color of the dice
        scores (list): List of the previous scores of the dice

    Returns:
        (int): Score of the dice
    """
    thresh = cv2.threshold(image, param_thresh[color], 255, cv2.THRESH_BINARY_INV)[1]  # Black and white image

    detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges

    # Find the circles in the image (corresponding to the points of the dice)
    circles = cv2.HoughCircles(image=detected_edges, method=cv2.HOUGH_GRADIENT, dp=6.8, minDist=1,
                               param1=150, param2=68, minRadius=1, maxRadius=15)

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

        # We convert the coordinates of the circles to the coordinates of the window
        for circle in circles:
            circle[0], circle[1] = circle[0] + rect[0], circle[1] + rect[1]

        # We draw the circles
        # draw_circle(circles)
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


def compute_mean_bgr(image):
    """
    Compute the mean BGR values of the image without the white or black dots
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
    mean_bgr = np.mean(new_list, axis=0)

    return mean_bgr


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


def draw_circle(circles):
    """
    Draw the circles on the frame

    Args:
        circles (numpy.ndarray): The circles to draw
    """
    for circle in circles:
        # Draw the outer circle
        cv2.circle(frame, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 255, 0), 2)
        # Draw the center of the circle
        cv2.circle(frame, (int(circle[0]), int(circle[1])), 2, (0, 0, 255), 3)


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