"""
This file contains data structures used in the project
"""


class ColorDice:
    """
    This class represents a dice detected in the image, with its color and its rect. It's used to identify which dice
    is which in the image
    """
    def __init__(self, color, rect, distances=None, bad_colors=None):
        """
        Initialize the ColorDice object

        Args:
            color (numpy.ndarray): Mean BGR color of the dice
            rect (tuple): Rect of the dice in the image
            distances (dict): Distances between the color of the dice and each color
            bad_colors (list): The color that we know is not the color of the dice
        """
        self.color = color  # Mean BGR color of the dice
        self.rect = rect  # Rect of the dice in the image

        if distances is None:
            self.distances = {}
        else:
            self.distances = distances  # Distances between the color of the dice and each color
        if bad_colors is None:
            self.bad_colors = []
        else:
            self.bad_colors = bad_colors  # The color that we know is not the color of the dice