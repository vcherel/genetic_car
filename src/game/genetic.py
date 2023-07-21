import src.data.variables as var  # Import the data
import random  # Used to generate random numbers

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
        if list_parameters is not None:        # If we have the parameters of the genetic algorithm
            self.dice_values = list_parameters.copy()  # Dice values corresponding to this genome (we copy the list)
        else:                                  # If we don't have the parameters we randomize them
            self.dice_values = [random.randint(1, 6) for _ in range(6)]  # Dice values corresponding to this genome

        self.length_slow = self.length_medium = self.length_fast = None  # We initialize the parameters
        self.width_slow = self.width_medium = self.width_fast = None  # We initialize the parameters
        self.save_values()  # Update the genetic algorithm (fill the parameters)

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
            bool: True if the two genetic algorithms are equals, False otherwise
        """
        return self.dice_values == other.dice_values

    def copy(self):
        """
        Copy the genetic algorithm

        Returns:
            Genetic: copy of the genetic algorithm
        """
        return Genetic(self.dice_values)

    def save_values(self):
        """
        Update the genetic algorithm (the dice values have changed, so we update the parameters)
        """
        self.length_slow = self.dice_values[0] * var.LENGTH_CONE  # Length of the detection cone when the car is going slow
        self.length_medium = self.dice_values[1] * var.LENGTH_CONE  # Length of the detection cone when the car is going at medium speed
        self.length_fast = self.dice_values[2] * var.LENGTH_CONE  # Length of the detection cone when the car is going fast

        self.width_slow = self.dice_values[3] * var.WIDTH_CONE  # Width of the detection cone when the car is going slow
        self.width_medium = self.dice_values[4] * var.WIDTH_CONE  # Width of the detection cone when the car is going at medium speed
        self.width_fast = self.dice_values[5] * var.WIDTH_CONE  # Width of the detection cone when the car is going fast