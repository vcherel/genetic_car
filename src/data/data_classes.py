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
            bad_colors (list): The colors that we know is not the color of the dice
        """
        self.color, self.rect = color, rect

        if distances is None:
            self.distances = {}  # Default value
        else:
            self.distances = distances  # Distances between the color of the dice and each color
        if bad_colors is None:
            self.bad_colors = []  # Default value
        else:
            self.bad_colors = bad_colors  # The color that we know is not the color of the dice

    def __str__(self):
        """
        Return the string of the dice
        """
        return f'ColorDice {self.color} : {self.distances}'


class MemoryCar:
    """
    This class represents a car in the memory for the garage
    """
    def __init__(self, id_car, name, color, genetic, best_scores):
        """
        Initialize the MemoryCar object

        Args:
            id_car (int): Id of the car (unique)
            name (str): Name of the car
            color (str): Color of the car
            genetic (Genetic): Genetic of the car
            best_scores (list): Scores of the car
        """
        self.id, self.name = id_car, name
        self.color, self.genetic = color, genetic
        self.best_scores = best_scores

    def __str__(self):
        """
        Return the string of the car (to write it in the file)
        """
        string = f'{self.id} {self.name} {self.color} {self.genetic}'
        for score in self.best_scores:
            string += f' {score}'
        return string