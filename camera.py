import cv2  # To use OpenCV
from statistics import mean  # To compute the mean of a list


param_thresh = {"black": 30, "orange": 125, "green": 100, "yellow": 165, "purple": 100, "red": 100, "dark_green": 75, "dark_yellow": 50}


def capture_stabilized_image():
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can change it if you have multiple cameras

    # Initialize variables
    prev_frame = None
    stable_frames = 0
    stabilization_threshold = 30  # Number of stable frames required for stabilization

    while True:
        # Read the frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            # Compute the absolute difference between the current and previous frame
            frame_diff = cv2.absdiff(gray, prev_frame)

            # Calculate the mean pixel intensity difference
            mean_diff = frame_diff.mean()

            # Check if the mean difference is below a certain threshold
            if mean_diff < stabilization_threshold:
                stable_frames += 1
            else:
                stable_frames = 0

            # Check if stabilization is achieved
            if stable_frames >= stabilization_threshold:
                # Save the stabilized frame as an image file
                cv2.imwrite('camera/image.jpg', frame)
                break

        # Update the previous frame
        prev_frame = gray.copy()

        # Display the frame
        cv2.imshow('Capture en cours', frame)

        # Check for the 'q' key to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the VideoCapture object and close the OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


def see_camera():
    """
    See the camera
    """
    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can change it if you have multiple cameras

    while True:
        ret, frame = cap.read()  # Read a frame from the camera
        cv2.imshow('frame', frame)  # Display the frame

        # If the user presses 'q', we exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the VideoCapture object
    cv2.destroyAllWindows()  # Destroy all the windows


def draw_circles(circles_to_draw, image):
    """
    Draw the circles on the image

    Args:
        circles_to_draw (numpy.ndarray): List of circles to draw
        image (numpy.ndarray): Image on which to draw the circles
    """
    # Draw the circles
    for circle in circles_to_draw:
        # draw the outer circle
        cv2.circle(image, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 255, 0), 2)
        # draw the center of the circle
        cv2.circle(image, (int(circle[0]), int(circle[1])), 2, (0, 0, 255), 3)


def optimize_parameters(image):
    """
    Optimize the parameters of the HoughCircles function by testing different values and printing the results

    Args:
        image (numpy.ndarray): Image on which to optimize the parameters
    """
    dico_p1 = {}
    dico_p2 = {}
    dico_dp = {}

    for p1 in range(1, 200):
        print(p1)
        for p2 in range(1, 200):
            for dp in range(1, 30):
                if p1 > p2:
                    c = cv2.HoughCircles(image=image, method=cv2.HOUGH_GRADIENT, dp=dp / 10, minDist=1, param1=p1, param2=p2, minRadius=1, maxRadius=30)
                    if c is not None and len(c[0, :]) == 5:
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


def recognize_score(color):
    """
    Recognize the score of the dice and display it on the image

    Args:
        color (str): Color of the dice
    """

    # Create a VideoCapture object
    cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera, you can change it if you have multiple cameras

    tab_score = []  # List of the scores of the dice

    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
        gray_img = cv2.medianBlur(gray_img, 5)  # We apply a median blur to the image to erase useless details

        # We define the threshold parameters for each color
        thresh = cv2.threshold(gray_img, param_thresh.get(color), 255, cv2.THRESH_BINARY_INV)[1]  # We apply a threshold to the image : it turns the image into a black and white image

        detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges

        # Draw the circles around the points of the dice
        circles = cv2.HoughCircles(image=detected_edges, method=cv2.HOUGH_GRADIENT, dp=1.6, minDist=5, param1=63, param2=25, minRadius=2, maxRadius=10)  # Find the circles in the image (corresponding to the points of the dice)
        if circles is not None:
            circles = circles[0, :]  # The array is in an array, we take the first element
            draw_circles(circles, frame)  # We draw the circles on the image

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # We create a kernel to close the edges (a rectangular structuring element of size 2x2)
        close = cv2.morphologyEx(detected_edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice

        # Draw the rectangle around the dice
        contours, hierarchy = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find the contours of the dice
        # cv2.drawContours(frame, contours, -1, (0, 0, 255), 3)  # Draw the contour of the dice

        if contours:       # If there is a contour (if the dice is in the image)
            x0, y0, w0, h0 = cv2.boundingRect(contours[0])  # Find the coordinates of the rectangle around the dice (x0, y0) is the upper left corner, w0 and h0 are the width and height of the rectangle
            cv2.rectangle(frame, (x0, y0), (x0 + w0, y0 + h0), (255, 0, 0), 5)  # Draw the rectangle around the dice

            if circles is not None:
                score = len(circles)  # We count the number of circles
            else:
                score = 0

            tab_score.append(score)  # We add the score to the list of scores
            if len(tab_score) > 50:  # If there are more than 10 scores in the list, we remove the first one
                tab_score.pop(0)  # We remove the first score

            score = int(mean(tab_score))  # We reset the actual score
            print(score)

            cv2.putText(frame, f'score: {score}', (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # We write the value of the dice on the image

        cv2.imshow('Camera', thresh)  # Display the frame

        # If the user presses 'q', we exit the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()  # Release the VideoCapture object
    cv2.destroyAllWindows()  # Destroy all the windows


if __name__ == '__main__':
    recognize_score('orange')
