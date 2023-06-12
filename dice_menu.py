import pygame  # Import pygame module
import variables as var  # Import the variables
from button import Button  # Import the button class
from genetic import Genetic  # Import the genetic class


rect_dice_menu = (300, 125, 1000, 550)  # Display rectangle of the dice menu

rgb_values = {"black": (0, 0, 0), "orange": (204, 102, 0), "green": (0, 153, 76), "purple": (102, 0, 102), "red": (204, 0, 0), "dark_yellow": (102, 102, 0)}

# Positions of the dice
x1, x2, x3, y1, y2 = 120, 420, 720, 100, 325

# Buttons
button_check = Button(1185, 575, pygame.image.load('images/check.png'), scale=0.15)


def draw_dice(x, y, color):
    """
    To draw a dice

    Args:
        x (int): x coordinate of the dice
        y (int): y coordinate of the dice
        color (str): Color of the dice
    """
    pygame.draw.rect(var.WINDOW, rgb_values.get(color), (rect_dice_menu[0] + x, rect_dice_menu[1] + y, 120, 120), 0)
    pygame.draw.rect(var.WINDOW, (100, 100, 100), (rect_dice_menu[0] + x, rect_dice_menu[1] + y, 120, 120), 3)
    if color == 'dark_yellow':
        draw_dots(rect_dice_menu[0] + x, rect_dice_menu[1] + y, var.ACTUAL_DICT_DICE.get(color), (0, 0, 0))
    else:
        draw_dots(rect_dice_menu[0] + x, rect_dice_menu[1] + y, var.ACTUAL_DICT_DICE.get(color))


def draw_dots(x, y, nb_dots, color=(255, 255, 255)):
    """
    To draw the dots on the dice

    Args:
        x (int): x coordinate of the dice
        y (int): y coordinate of the dice
        nb_dots (int): Number of dots on the dice
        color (tuple): Color of the dots. Defaults to (255, 255, 255).
    """
    dot_radius = 10
    dot_padding = 32
    position_dot = []

    # Calculate the positions of the dots based on the number of dots
    if nb_dots == 1:
        position_dot = [(x + 0.5 * 120, y + 0.5 * 120)]
    elif nb_dots == 2:
        position_dot = [(x + dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding)]
    elif nb_dots == 3:
        position_dot = [(x + dot_padding, y + dot_padding), (x + 0.5 * 120, y + 0.5 * 120),
                        (x + 120 - dot_padding, y + 120 - dot_padding)]
    elif nb_dots == 4:
        position_dot = [(x + dot_padding, y + dot_padding), (x + dot_padding, y + 120 - dot_padding),
                        (x + 120 - dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding)]
    elif nb_dots == 5:
        position_dot = [(x + dot_padding, y + dot_padding), (x + dot_padding, y + 120 - dot_padding),
                        (x + 120 - dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding),
                        (x + 0.5 * 120, y + 0.5 * 120)]
    elif nb_dots == 6:
        position_dot = [(x + dot_padding, y + dot_padding), (x + dot_padding, y + 120 - dot_padding),
                        (x + 120 - dot_padding, y + dot_padding), (x + 120 - dot_padding, y + 120 - dot_padding),
                        (x + dot_padding, y + 0.5 * 120), (x + 120 - dot_padding, y + 0.5 * 120)]

    # Draw the dots on the dice
    for dot_pos in position_dot:
        pygame.draw.circle(var.WINDOW, color, dot_pos, dot_radius)


def display_dice_menu():
    """
    To display the dice menu

    Returns:
        bool: True if the user has validated the value of the dice
    """
    # We display the window
    pygame.draw.rect(var.WINDOW, (128, 128, 128), rect_dice_menu, 0)
    pygame.draw.rect(var.WINDOW, (115, 205, 255), rect_dice_menu, 2)
    var.WINDOW.blit(var.LARGE_FONT.render('Dés sélectionnés', True, (0, 0, 0), (128, 128, 128)), (rect_dice_menu[0] + 350, rect_dice_menu[1] + 20))

    # Display the dice
    draw_dice(x=x1, y=y1, color='dark_yellow')
    draw_dice(x=x2, y=y1, color='orange')
    draw_dice(x=x3, y=y1, color='red')
    draw_dice(x=x1, y=y2, color='green')
    draw_dice(x=x2, y=y2, color='purple')
    draw_dice(x=x3, y=y2, color='black')

    # Display the buttons
    button_check.check_state()

    # If the button is checked we close the window
    return button_check.just_clicked


def erase_dice_menu():
    """
    To erase the dice menu and save the value of the dice
    """
    var.DISPLAY_DICE_MENU = False  # We don't display the dice menu anymore
    rect = pygame.Rect(rect_dice_menu)  # We create a rectangle with the coordinates of the dice menu
    var.WINDOW.blit(var.BACKGROUND, rect, rect)  # We erase the dice menu

    genetic = Genetic(height_slow=var.ACTUAL_DICT_DICE.get("dark_yellow"), width_slow=var.ACTUAL_DICT_DICE.get("green"),
                      height_medium=var.ACTUAL_DICT_DICE.get("orange"), width_medium=var.ACTUAL_DICT_DICE.get("purple"),
                      height_fast=var.ACTUAL_DICT_DICE.get("red"), width_fast=var.ACTUAL_DICT_DICE.get("black"))
    var.MEMORY_CARS.get("dice").append((var.ACTUAL_ID_MEMORY_DICE, genetic))  # We add the dice to the memory
    var.ACTUAL_ID_MEMORY_DICE += 1  # We increment the id of the dice
