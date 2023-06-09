import time  # To get the time
import cv2  # To use OpenCV
import random  # To generate random numbers
import numpy as np  # To use numpy
from display import draw_circle  # To draw the circles
from utils import overlapping_rectangles  # Utils functions
import matplotlib.pyplot as plt  # To plot the images


# The parameters of the threshold to make a black and white image for each color
param_thresh = {"black": 25, "orange": 120, "green": 100, "purple": 100, "red": 100, "dark_yellow": 50}
# The BGR values of each color (observation)
bgr_values = {"black": (66, 66, 66), "orange": (52, 107, 165), "green": (65, 128, 49), "purple": (53, 67, 68), "red": (53, 87, 123), "dark_yellow": (51, 86, 134), "white": (150, 130, 126)}
# The BGR values of each color (real)
real_bgr_values = {"black": (0, 0, 0), "orange": (0, 102, 204), "green": (76, 153, 0), "purple": (102, 0, 102), "red": (0, 0, 204), "dark_yellow": (0, 102, 102)}


def find_rectangles(image, rectangles):
    """
    Find the rectangles on the image

    Args:
        image (numpy.ndarray): Image on which to find the rectangles
        rectangles (list): List of rectangles to draw
    """
    for p in param_thresh.values():
        gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
        gray_img = cv2.medianBlur(gray_img, 5)  # We apply a median blur to the image to erase useless details

        # We apply a threshold to the image : it turns the image into a black and white image
        thresh = cv2.threshold(gray_img, p, 255, cv2.THRESH_BINARY_INV)[1]

        detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges
        # We create a kernel to close the edges (a rectangular structuring element of size 9x9)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        close = cv2.morphologyEx(detected_edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice

        contours, _ = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # We find the contours of the image

        min_size = 50  # Minimum size of the rectangle
        max_size = 150  # Maximum size of the rectangle

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)  # We get the coordinates of the rectangle
            if min_size < w < max_size and min_size < h < max_size:  # If the rectangle is not too big or too small

                # We check if the rectangle is already in the list
                rect_is_in_list = False
                for rect in rectangles:
                    if rect_is_in_list:
                        break
                    if overlapping_rectangles(rect, (x, y, w, h), area_threshold=0.7):
                        rect_is_in_list = True

                # If the rectangle is not in the list, we add it
                if not rect_is_in_list:
                    rectangles.append((x, y, w, h))


def determine_color(image):
    """
    Determine the color of the dice on the image

    Args:
        image (numpy.ndarray): Image of the dice

    Returns:
        (str): Color of the dice
    """
    # Convert the image to a numpy array
    image_array = np.array(image)

    # Calculate the mean BGR values
    mean_bgr = np.mean(image_array, axis=(0, 1))

    # Calculate the distance between the mean BGR values and the BGR values of each color
    distances = {}
    for color, bgr in bgr_values.items():
        distances[color] = np.linalg.norm(mean_bgr - bgr)

    # We get the color with the minimum distance
    color = min(distances, key=distances.get)

    return color


def determine_score(image, color, frame, scores):
    """
    Determine the score of the dice

    Args:
        image (numpy.ndarray): Image of the dice
        color (str): Color of the dice
        frame (numpy.ndarray): Frame of the video
        scores (list): List of the previous scores of the dice

    Returns:
        (int): Score of the dice
    """
    thresh = cv2.threshold(image, param_thresh[color], 255, cv2.THRESH_BINARY_INV)[1]  # Black and white image

    detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges

    # Find the circles in the image (corresponding to the points of the dice)
    circles = cv2.HoughCircles(image=detected_edges, method=cv2.HOUGH_GRADIENT, dp=1.6, minDist=15,
                               param1=63, param2=25, minRadius=5, maxRadius=10)
    if circles is not None:
        circles = circles[0, :]  # The array is in an array, we take the first element

        score = len(circles)  # We count the number of circles
        for circle in circles:
            draw_circle(circle, image)
    else:
        score = 0

    if score > 6:
        score = 6

    scores.append(score)  # We add the score to the list of scores
    if len(scores) > 50:
        scores.pop(0)  # We remove the first score

    # We find the number the most present in the list of scores
    score = max(set(scores), key=scores.count)

    return score


def verify_circle(circle, frame):
    """
    Verify that the circle is not a false positive (a circle that is not a point of the dice)

    Args:
        circle (numpy.ndarray): Circle to verify
        frame (numpy.ndarray): Frame of the video

    Returns:
        (bool): True if the circle is not a false positive, False otherwise
    """

    x, y = int(circle[0]), int(circle[1])  # Coordinates of the center of the circle

    color_center = frame[x, y]  # Color of the center of the circle

    bgr_center = np.array([color_center[0], color_center[1], color_center[2]])  # BGR values of the center of the circle

    # We calculate the distance between the mean BGR values and the BGR values of each color
    distance = np.linalg.norm(bgr_center-bgr_values["white"])

    # We get the color with a distance less than the threshold
    threshold = 75

    if distance < threshold:
        return True
    else:
        return False


def capture_dice():
    """
    Main program

    Returns:
        (dict): Dictionary containing the score of each color
    """
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can change it if you have multiple cameras

    scores_all_colors = {"black": [], "orange": [], "green": [], "purple": [], "red": [], "dark_yellow": []}

    # The scores we will return, initialized to random values
    final_score = {"black": random.randint(1, 6), "orange": random.randint(1, 6), "green": random.randint(1, 6),
                   "purple": random.randint(1, 6), "red": random.randint(1, 6), "dark_yellow": random.randint(1, 6)}

    start_time = time.time()  # We get the current time

    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        rectangles = []  # List of the rectangles on the image
        find_rectangles(frame, rectangles)  # Find the rectangles on the image

        for rect in rectangles:
            x, y, w, h = rect
            img_rect = frame[y:y+h, x:x+w]  # We get the image of the rectangle
            color = determine_color(img_rect)  # We determine the color of the rectangle
            if color != 'white':
                # We draw the rectangle on the image
                cv2.rectangle(frame, (x, y), (x + w, y + h), real_bgr_values[color], 5)

                score = determine_score(img_rect, color, frame, scores_all_colors[color])  # We determine the score of the dice
                final_score[color] = score  # We add the score to the final score

                # We write the value of the dice on the image
                cv2.putText(frame, f'score: {score}', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Camera', frame)  # Display the frame

        if cv2.waitKey(1) & 0xFF == ord('q'):
            # We quit the program if the user presses the 'q' key
            break

        if time.time() - start_time > 10:  # If 10 seconds have passed
            # We quit the program after 10 seconds
            break

    cap.release()  # Release the VideoCapture object
    cv2.destroyAllWindows()  # Close all windows

    return final_score