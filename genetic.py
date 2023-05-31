import random  # Used to generate random numbers


class Genetic:
    """
    The class is used to represent a genetic algorithm and store the genetic parameters of a car
    """
    def __init__(self, genetic=None):
        """
        Initialization of the genetic algorithm

        Args:
            genetic (Genetic): genetic algorithm to copy
        """
        self.fitness = 0  # Car score

        if genetic is None:
            width_fast = 15 * random.randint(1, 6)  # Width of the detection cone when the car is going fast
            height_fast = 15 * random.randint(1, 6)  # Height of the detection cone when the car is going fast

            width_medium = 15 * random.randint(1, 6)  # Width of the detection cone when the car is going at medium speed
            height_medium = 15 * random.randint(1, 6)  # Height of the detection cone when the car is going at medium speed

            width_slow = 15 * random.randint(1, 6)  # Width of the detection cone when the car is going slow
            height_slow = 15 * random.randint(1, 6)  # Height of the detection cone when the car is going slow



