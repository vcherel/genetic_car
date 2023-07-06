import src.other.variables as var  # Import the variables
import random  # Used to generate random numbers

"""
This file contains the Genetic class used to store the genetic parameters of a car
"""


class Genetic:
    """
    The class is used to represent a genetic algorithm and store the genetic parameters of a car
    """
    def __init__(self, list_parameters=None):
        """
        Initialization of the genetic algorithm

        Args:
            list_parameters (list(int)): list of the parameters of the genetic algorithm in this order : (length_slow, length_medium, length_fast, width_slow, width_medium, width_fast)
        """
        if list_parameters is not None:        # If we have the parameters of the genetic algorithm
            self.length_slow = list_parameters[0] * var.LENGTH_CONE  # Length of the detection cone when the car is going slow
            self.length_medium = list_parameters[1] * var.LENGTH_CONE  # Length of the detection cone when the car is going at medium speed
            self.length_fast = list_parameters[2] * var.LENGTH_CONE  # Length of the detection cone when the car is going fast

            self.width_slow = list_parameters[3] * var.WIDTH_CONE  # Width of the detection cone when the car is going slow
            self.width_medium = list_parameters[4] * var.WIDTH_CONE  # Width of the detection cone when the car is going at medium speed
            self.width_fast = list_parameters[5] * var.WIDTH_CONE  # Width of the detection cone when the car is going fast

        else:                                  # If we don't have the parameters we randomize them
            self.length_slow = var.LENGTH_CONE * random.randint(1, 6)  # Length of the detection cone when the car is going slow
            self.length_medium = var.LENGTH_CONE * random.randint(1, 6)  # Length of the detection cone when the car is going at medium speed
            self.length_fast = var.LENGTH_CONE * random.randint(1, 6)  # Length of the detection cone when the car is going fast

            self.width_slow = var.WIDTH_CONE * random.randint(1, 6)  # Width of the detection cone when the car is going slow
            self.width_medium = var.WIDTH_CONE * random.randint(1, 6)  # Width of the detection cone when the car is going at medium speed
            self.width_fast = var.WIDTH_CONE * random.randint(1, 6)  # Width of the detection cone when the car is going fast

    def __str__(self):
        """
        String representation of the genetic algorithm

        Returns:
            str: string representation of the genetic algorithm
        """
        return f' {self.length_slow // var.LENGTH_CONE} {self.length_medium // var.LENGTH_CONE} {self.length_fast // var.LENGTH_CONE} ' \
               f'{self.width_slow // var.WIDTH_CONE} {self.width_medium // var.WIDTH_CONE} {self.width_fast // var.WIDTH_CONE}'

    def __eq__(self, other):
        """
        Check if two genetic algorithms are equals, two genetic algorithms are equals if they have the same parameters

        Args:
            other (Genetic): genetic algorithm to compare with

        Returns:
            bool: True if the two genetic algorithms are equals, False otherwise
        """
        return self.width_fast == other.width_fast and self.length_fast == other.length_fast and \
            self.width_medium == other.width_medium and self.length_medium == other.length_medium and \
            self.width_slow == other.width_slow and self.length_slow == other.length_slow

    def copy(self):
        """
        Copy the genetic algorithm

        Returns:
            Genetic: copy of the genetic algorithm
        """
        return Genetic(self.get_list())

    def get_list(self):
        """
        Get the list of the genetic parameters

        Returns:
            list: list of the genetic parameters
        """
        return [self.length_slow // var.LENGTH_CONE, self.length_medium // var.LENGTH_CONE, self.length_fast // var.LENGTH_CONE,
                self.width_slow // var.WIDTH_CONE, self.width_medium // var.WIDTH_CONE, self.width_fast // var.WIDTH_CONE]
