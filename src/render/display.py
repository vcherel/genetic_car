from src.other.utils import text_rec, compute_detection_cone_points  # Import the utils functions
from src.game.constants import RADIUS_CHECKPOINT  # Import the constants
from src.other import variables as var  # Import the variables
import pygame  # To use pygame
import cv2  # To use OpenCV


def edit_background():
    """
    Add elements to the background for the rest of the game
    """
    # Add a text for the debug mode
    var.BACKGROUND.blit(var.FONT.render('Activer debug :', True, (255, 255, 255), (0, 0, 0)), (1290, 640))  # Add the debug text
    var.BACKGROUND.blit(var.FONT.render('Nombre de voitures', True, (0, 0, 0), (128, 128, 128)), (1060, 25))  # Add the yes text
    pygame.draw.line(var.BACKGROUND, (0, 0, 0), (1280, 120), (1280, 0), 2)  # Line at the right
    pygame.draw.line(var.BACKGROUND, (0, 0, 0), (325, 120), (325, 0), 2)  # Line at the left


def show_checkpoints():
    for checkpoint in var.CHECKPOINTS:
        pygame.draw.circle(var.WINDOW, (255, 0, 0), checkpoint, RADIUS_CHECKPOINT, 1)


def display_text_ui(caption, pos, font, background_color=(128, 128, 128)):
    """
    Display a text with a variable

    Args:
        caption (str): caption of the text
        pos (tuple): position of the text
        font (pygame.font.Font): font of the text
        background_color (tuple): background color of the text
    """
    text = font.render(caption, True, (0, 0, 0), background_color)  # Create the text
    var.WINDOW.blit(text, pos)  # Draw the text
    var.RECTS_BLIT_UI.append(text_rec(text, pos))  # Add the rectangle of the text to the list of rectangles to blit


def draw_circle(circle, image):
    """
    Draw the circles on the image

    Args:
        circle (numpy.ndarray): The circle to draw
        image (numpy.ndarray): Image on which to draw the circles
    """
    # Draw the outer circle
    cv2.circle(image, (int(circle[0]), int(circle[1])), int(circle[2]), (0, 255, 0), 2)
    # Draw the center of the circle
    cv2.circle(image, (int(circle[0]), int(circle[1])), 2, (0, 0, 255), 3)


def draw_detection_cone(pos, genetic, factor=1):
    """
    Draw the detection cones for a car

    Args:
        pos (int, int): position of the car
        genetic (Genetic): genetic of the car
        factor (float): factor to multiply the width and height of the detection cone
    """
    left, top, right = compute_detection_cone_points(90, pos, genetic.width_slow * factor, genetic.height_slow * factor)
    pygame.draw.polygon(var.WINDOW, (0, 0, 255), (pos, left, top, right), 5)

    left, top, right = compute_detection_cone_points(90, pos, genetic.width_medium * factor, genetic.height_medium * factor)
    pygame.draw.polygon(var.WINDOW, (0, 255, 0), (pos, left, top, right), 5)

    left, top, right = compute_detection_cone_points(90, pos, genetic.width_fast * factor, genetic.height_fast * factor)
    pygame.draw.polygon(var.WINDOW, (255, 0, 0), (pos, left, top, right), 5)


def show_car(car):
    """
    Display the car with the detection cones on the screen

    Args:
        car (Car): car to display
    """
    var.DISPLAY_CAR = True  # Display the car

    rect = pygame.Rect(500, 125, 400, 550)  # Create the rectangle for the window
    pygame.draw.rect(var.WINDOW, (128, 128, 128), rect, 0)  # Draw the rectangle (inside)
    pygame.draw.rect(var.WINDOW, (115, 205, 255), rect, 2)  # Draw the rectangle (contour)

    x, y = rect[0] + 100, rect[1] + 280  # Position of the car
    var.WINDOW.blit(var.RED_CAR_CONE, (x, y))  # Draw the red car
    draw_detection_cone((x + 125, y + 25), car.genetic, 2.5)  # Draw the detection cones

    var.WINDOW.blit(var.TEXT_SLOW, (x - 50, y + 50))  # Draw the slow text
    var.WINDOW.blit(var.TEXT_MEDIUM, (x - 50, y))  # Draw the medium text
    var.WINDOW.blit(var.TEXT_FAST, (x - 50, y - 50))  # Draw the fast text
