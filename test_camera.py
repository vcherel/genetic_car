import cv2  # OpenCV
import matplotlib.pyplot as plt  # Matplotlib


# 0
img = cv2.imread('img_test/0.jpg')  # Read the image


rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # We convert the image from BGR to RGB
plt.imshow(rgb_img)  # RGB image

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
plt.imshow(gray_img, cmap='gray')  # Gray image


detected_edges = cv2.Canny(gray_img, 9, 150, 3)  # Detect edges
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))  # We create a kernel to close the edges (a rectangular structuring element of size 9x9)
close = cv2.morphologyEx(detected_edges, cv2.MORPH_CLOSE, kernel, iterations=2)  # Close the edges of the dice
plt.imshow(close, cmap='gray')  # Image with the edges

circles = cv2.HoughCircles(image=close, method=cv2.HOUGH_GRADIENT, dp=1.1, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=55)  # Find the circles in the image (corresponding to the points of the dice)
circles = circles[0, :]  # The array is in an array, we take the first element
# Draw the circles
for i in circles:
    # draw the outer circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), int(i[2]), (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)
plt.imshow(rgb_img)  # Image with the circles


contours, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find the contours of the dice
x0, y0, w0, h0 = cv2.boundingRect(contours[0])  # Find the coordinates of the rectangle around the dice (x0, y0) is the upper left corner, w0 and h0 are the width and height of the rectangle
cv2.rectangle(rgb_img, (x0, y0), (x0 + w0, y0 + h0), (0, 255, 0), 5)  # Draw the rectangle around the dice
plt.imshow(rgb_img)  # Image with the rectangle and circles


dice0 = close[y0:y0+h0, x0:x0+w0]  # We crop the image to keep only the dice
plt.imshow(dice0, cmap='gray')  # Image of the dice zoomed in with the edges

circles0 = cv2.HoughCircles(image=dice0, method=cv2.HOUGH_GRADIENT, dp=1.3, minDist=20, param1=50, param2=30, minRadius=5, maxRadius=55)   # Find the circles in the image (corresponding to the points of the dice)
circles0 = circles0[0, :]  # The array is in an array, we take the first element


cv2.putText(rgb_img, f'score: {len(circles0)}', (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)  # We write the value of the dice on the image
plt.imshow(rgb_img)  # Image with the rectangle and circles and the value of the dice




# 1
img = cv2.imread('img_test/1.jpg')

rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # We convert the image from BGR to RGB
plt.imshow(rgb_img)  # RGB image

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
plt.imshow(gray_img, cmap='gray')  # Gray image

thresh = cv2.threshold(gray_img, 220, 255, cv2.THRESH_BINARY_INV)[1]  # We apply a threshold to the image : it turns the image into a black and white image
plt.imshow(thresh, cmap='gray')  # Black and white image

detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges
circles = cv2.HoughCircles(detected_edges, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)  # Find the circles in the image (corresponding to the points of the dice)
circles = circles[0, :]  # The array is in an array, we take the first element
plt.imshow(detected_edges, cmap='gray')  # Image with the edges

contours, hierarchy = cv2.findContours(detected_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Find the contours of the dice

# Since we have 2 dices, and we want score of each one we need to split them into two image then recognise their scores.
x0, y0, w0, h0 = cv2.boundingRect(contours[0])  # Find the rectangle around the first dice
cv2.rectangle(rgb_img, (x0, y0), (x0+w0, y0+h0), (0, 255, 0), 5)  # Draw the rectangle around the first dice

x1, y1, w1, h1 = cv2.boundingRect(contours[1])  # Find the rectangle around the second dice
cv2.rectangle(rgb_img, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 5)  # Draw the rectangle around the second dice
plt.imshow(rgb_img)  # Image with the rectangles and circles

# We crop the image to keep only the dice
dice0 = detected_edges[y0:y0+h0, x0:x0+w0]
dice1 = detected_edges[y1:y1+h1, x1:x1+w1]
plt.imshow(dice0, cmap='gray')
plt.imshow(dice1, cmap='gray')

# We find the circles on the images
circles0 = cv2.HoughCircles(dice0, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)
circles1 = cv2.HoughCircles(dice1, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)
circles0 = circles0[0, :]
circles1 = circles1[0, :]
print(len(circles0), len(circles1))  # We print the number of circles found on each image
# We draw the circles on the image
for i in circles:
    # draw the outer circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), int(i[2]), (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)

# We write the value of the dices on the image
cv2.putText(rgb_img, f'score: {len(circles0)}', (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
cv2.putText(rgb_img, f'score: {len(circles1)}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
plt.imshow(rgb_img)  # Image with the rectangles and circles and the values of the dices




# 2
img = cv2.imread('img_test/2.jpg')  # We load the image

rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # We convert the image from BGR to RGB
plt.imshow(rgb_img)  # RGB image

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray
plt.imshow(gray_img, cmap='gray')  # Gray image

thresh = cv2.threshold(gray_img, 250, 255, cv2.THRESH_BINARY_INV)[1]  # We apply a threshold to the image : it turns the image into a black and white image
detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges
circles = cv2.HoughCircles(detected_edges, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)  # Find the circles in the image (corresponding to the points of the dice)
circles = circles[0, :]  # The array is in an array, we take the first element
plt.imshow(detected_edges, cmap='gray')  # Image with the edges

# We draw the circles on the image
for i in circles:
    # draw the outer circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), int(i[2]), (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)
plt.imshow(rgb_img)  # Image with the circles and the values of the dices


kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # We create a kernel to dilate the image (a rectangular structuring element of size 3x3)
dil = cv2.dilate(detected_edges, kernel, iterations=1)  # We dilate the image to make it easier to find the contours

contours, hierarchy = cv2.findContours(dil, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # We find the contours of the dices

# We find the contours of the dices and draw the rectangles around them
x0, y0, w0, h0 = cv2.boundingRect(contours[0])
cv2.rectangle(rgb_img, (x0, y0), (x0+w0, y0+h0), (0, 255, 0), 5)
x1, y1, w1, h1 = cv2.boundingRect(contours[1])
cv2.rectangle(rgb_img, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 5)
x2, y2, w2, h2 = cv2.boundingRect(contours[2])
cv2.rectangle(rgb_img, (x2, y2), (x2+w2, y2+h2), (0, 255, 0), 5)

# We crop the image to keep only the dice
dice0 = detected_edges[y0:y0+h0, x0:x0+w0]
dice1 = detected_edges[y1:y1+h1, x1:x1+w1]
dice2 = detected_edges[y2:y2+h2, x2:x2+w2]

# We find the circles on the images
circles0 = cv2.HoughCircles(dice0, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)
circles1 = cv2.HoughCircles(dice1, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)
circles2 = cv2.HoughCircles(dice2, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)

# We write the value of the dices on the image
cv2.putText(rgb_img, f'score: {len(circles0[0])}', (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(rgb_img, f'score: {len(circles1[0])}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(rgb_img, f'score: {len(circles2[0])}', (x2, y2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

plt.imshow(rgb_img)  # Image with the rectangles and circles and the values of the dices




# 3
img = cv2.imread('img_test/3.jpg')  # We load the image
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # We convert the image from BGR to RGB
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # We convert the image from BGR to gray

thresh = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)[1]  # Black and white image
detected_edges = cv2.Canny(thresh, 9, 150, 3)  # Detect edges

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))  # We create a kernel to close the image (a rectangular structuring element of size 3x3)
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)  # Close the edges of the dice

circles = cv2.HoughCircles(close, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)  # Find the circles in the image (corresponding to the points of the dice)
circles = circles[0, :]
for i in circles:
    # draw the outer circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), int(i[2]), (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(rgb_img, (int(i[0]), int(i[1])), 2, (0, 0, 255), 3)

contours, hierarchy = cv2.findContours(detected_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # We find the contours of the dices

# We find the contours of the dices and draw the rectangles around them
x0, y0, w0, h0 = cv2.boundingRect(contours[0])
cv2.rectangle(rgb_img, (x0, y0), (x0+w0, y0+h0), (0, 255, 0), 5)
x1, y1, w1, h1 = cv2.boundingRect(contours[1])
cv2.rectangle(rgb_img, (x1, y1), (x1+w1, y1+h1), (0, 255, 0), 5)
plt.imshow(rgb_img)  # Image with the circles and rectangles

# We crop the image to keep only the dice
dice0 = detected_edges[y0:y0+h0, x0:x0+w0]
dice1 = detected_edges[y1:y1+h1, x1:x1+w1]

# We find the circles on the images
circles0 = cv2.HoughCircles(dice0, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)
circles1 = cv2.HoughCircles(dice1, cv2.HOUGH_GRADIENT, 1.2, 20, param1=50, param2=25, minRadius=3, maxRadius=35)

# We write the value of the dices on the image
cv2.putText(rgb_img, f'score: {len(circles0[0])}', (x0, y0), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
cv2.putText(rgb_img, f'score: {len(circles1[0])}', (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

plt.imshow(rgb_img)  # Image with the rectangles and circles and the values of the dices
