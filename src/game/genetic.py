import random  # Used to generate random numbers
import data.variables as var  # Import the variables

"""
This file contains the Genetic class used to store the genetic parameters of a car
"""


class Genetic:
    """
    This class is used to represent a genetic algorithm and store the genetic parameters of a car
    """
    def __init__(self, list_parameters=None):
        """
        Initialization of the genetic algorithm

        Args:
            list_parameters (list(int)): list of the parameters of the genetic algorithm in this order : (length_slow, length_medium, length_fast, width_slow, width_medium, width_fast)
        """
        if list_parameters is None:  # If we don't have the parameters we randomize them
            self.dice_values = [random.randint(1, 6) for _ in range(6)]  # Dice values corresponding to this genome
        else:
            self.dice_values = list_parameters.copy()  # Dice values corresponding to this genome (we copy the list)

    def __str__(self):
        """
        String representation of the genetic algorithm

        Returns:
            str: string representation of the genetic algorithm
        """
        str_to_return = ''
        for value in self.dice_values:
            str_to_return += str(value) + ' '
        return str_to_return[:-1]  # We remove the last space

    def __eq__(self, other):
        """
        Check if two genetic algorithms are equals, two genetic algorithms are equals if they have the same parameters

        Args:
            other (Genetic): genetic algorithm to compare with

        Returns:
            bool: True if the two genetic algorithms are equals
        """
        return self.dice_values == other.dice_values

    def copy(self):
        """
        Copy the genetic algorithm

        Returns:
            Genetic: copy of the genetic algorithm
        """
        return Genetic(self.dice_values)

    def length_slow(self):
        """
        Get the length of the slow dice

        Returns:
            int: length of the slow dice
        """
        return self.dice_values[0] * var.LENGTH_CONE

    def length_medium(self):
        """
        Get the length of the medium dice

        Returns:
            int: length of the medium dice
        """
        return self.dice_values[1] * var.LENGTH_CONE

    def length_fast(self):
        """
        Get the length of the fast dice

        Returns:
            int: length of the fast dice
        """
        return self.dice_values[2] * var.LENGTH_CONE

    def width_slow(self):
        """
        Get the width of the slow dice

        Returns:
            int: width of the slow dice
        """
        return self.dice_values[3] * var.WIDTH_CONE

    def width_medium(self):
        """
        Get the width of the medium dice

        Returns:
            int: width of the medium dice
        """
        return self.dice_values[4] * var.WIDTH_CONE

    def width_fast(self):
        """
        Get the width of the fast dice

        Returns:
            int: width of the fast dice
        """
        return self.dice_values[5] * var.WIDTH_CONE
