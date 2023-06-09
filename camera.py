import cv2  # To use OpenCV
from statistics import mean  # To compute the mean of a list
from utils import overlapping_rectangles, draw_circles  # Utils functions

param_thresh = {"black": 30, "orange": 120, "green": 100, "yellow": 165, "purple": 100, "red": 100, "dark_green": 75, "dark_yellow": 50}


def find_rectangles(img, rectangles):
    """
    Find the rectangles on the image

    Args:
        img (numpy.ndarray): Image on which to find the rectangles
        rectangles (list): List of rectangles to draw
    """
    for p in param_thresh.values():
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
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
                    if overlapping_rectangles(rect, (x, y, w, h)):
                        rect_is_in_list = True

                # If the rectangle is not in the list, we add it
                if not rect_is_in_list:
                    rectangles.append((x, y, w, h))

    # We draw the rectangles
    for rect in rectangles:
        x, y, w, h = rect
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)


def determine_color(img):
    """
    Determine the color of the dice on the image

    Args:
        img (numpy.ndarray): Image of the dice
    """
    pass


def determine_score(img, color, tab_score):
    """
    Determine the score of the dice

    Args:
        img (numpy.ndarray): Image of the dice
        color (str): Color of the dice
        tab_score (list): List of the scores of the dice

    Returns:
        (img, int): Image of the dice with the score
    """

    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
    gray_img = cv2.medianBlur(gray_img, 5)  # We apply a median blur to the image to erase useless details

    # We apply a threshold to the image : it turns the image into a black and white image
    thresh = cv2.threshold(gray_img, param_thresh.get(color), 255, cv2.THRESH_BINARY_INV)[1]

    detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges

    # Find the circles in the image (corresponding to the points of the dice)
    circles = cv2.HoughCircles(image=detected_edges, method=cv2.HOUGH_GRADIENT, dp=1.6, minDist=5,
                               param1=63, param2=25, minRadius=2, maxRadius=10)
    if circles is not None:
        circles = circles[0, :]  # The array is in an array, we take the first element
        draw_circles(circles, img)  # We draw the circles on the image

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # We create a kernel to close the edges
    close = cv2.morphologyEx(detected_edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice

    # Find the contours of the dice
    contours, hierarchy = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)  # Draw the contour of the dice

    score = 0
    if contours:  # If there is a contour (if the dice is in the image)
        # Find the coordinates of the rectangle around the dice
        # (x0, y0) is the upper left corner, w0 and h0 are the width and height of the rectangle
        x0, y0, w0, h0 = cv2.boundingRect(contours[0])
        cv2.rectangle(img, (x0, y0), (x0 + w0, y0 + h0), (255, 0, 0), 5)  # Draw the rectangle around the dice

        if circles is not None:
            score = len(circles)  # We count the number of circles
        else:
            score = 0

        tab_score.append(score)  # We add the score to the list of scores
        if len(tab_score) > 50:  # If there are more than 10 scores in the list, we remove the first one
            tab_score.pop(0)  # We remove the first score

        score = int(mean(tab_score))  # We reset the actual score
        # We write the value of the dice on the image
        cv2.putText(img, f'score: {score}', (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    return img, score


def main():
    """
        Main program
    """
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can change it if you have multiple cameras

    tab_score = []  # List of the scores of the dice

    while True:
        color = "black"

        rectangles = []  # List of the rectangles on the image

        ret, frame = cap.read()  # Read a frame from the camera

        find_rectangles(frame, rectangles)  # Find the rectangles on the image

        # frame, score = determine_score(frame, color, tab_score)  # Determine the score of the dice

        cv2.imshow('Camera', frame)  # Display the frame

        # If the user presses 'q', we exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the VideoCapture object
    cv2.destroyAllWindows()  # Destroy all the windows


if __name__ == "__main__":
    main()


