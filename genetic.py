import random  # Used to generate random numbers
from constants import WIDTH_MULTIPLIER, HEIGHT_MULTIPLIER  # Constants of the game


class Genetic:
    """
    The class is used to represent a genetic algorithm and store the genetic parameters of a car
    """
    def __init__(self, genetic=None, width_fast=None, height_fast=None, width_medium=None, height_medium=None, width_slow=None, height_slow=None):
        """
        Initialization of the genetic algorithm

        Args:
            genetic (Genetic): genetic algorithm to copy
        """
        if width_fast is not None:        # If we have the parameters of the genetic algorithm
            self.width_fast = WIDTH_MULTIPLIER * width_fast
            self.height_fast = HEIGHT_MULTIPLIER * height_fast

            self.width_medium = WIDTH_MULTIPLIER * width_medium
            self.height_medium = HEIGHT_MULTIPLIER * height_medium

            self.width_slow = WIDTH_MULTIPLIER * width_slow
            self.height_slow = HEIGHT_MULTIPLIER * height_slow
        elif genetic is not None:  # If we have a genetic algorithm to copy
            self.width_fast = genetic.width_fast
            self.height_fast = genetic.height_fast

            self.width_medium = genetic.width_medium
            self.height_medium = genetic.height_medium

            self.width_slow = genetic.width_slow
            self.height_slow = genetic.height_slow
        else:  # If we don't have a genetic algorithm to copy
            self.width_fast = WIDTH_MULTIPLIER * random.randint(1, 6)  # Width of the detection cone when the car is going fast
            self.height_fast = HEIGHT_MULTIPLIER * random.randint(1, 6)  # Height of the detection cone when the car is going fast

            self.width_medium = WIDTH_MULTIPLIER * random.randint(1, 6)  # Width of the detection cone when the car is going at medium speed
            self.height_medium = HEIGHT_MULTIPLIER * random.randint(1, 6)  # Height of the detection cone when the car is going at medium speed

            self.width_slow = WIDTH_MULTIPLIER * random.randint(1, 6)  # Width of the detection cone when the car is going slow
            self.height_slow = HEIGHT_MULTIPLIER * random.randint(1, 6)  # Height of the detection cone when the car is going slow





    def __str__(self):
        """
        String representation of the genetic algorithm

        Returns:
            str: string representation of the genetic algorithm
        """
        return f"Genetic algorithm: height_slow={self.height_slow}, height_medium={self.height_medium}, height_fast={self.height_fast}, width_slow={self.width_slow}, width_medium={self.width_medium}, width_fast={self.width_fast}"
