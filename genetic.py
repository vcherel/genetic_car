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
            self.width_fast = 15 * random.randint(1, 6)  # Width of the detection cone when the car is going fast
            self.height_fast = 15 * random.randint(1, 6)  # Height of the detection cone when the car is going fast

            self.width_medium = 15 * random.randint(1, 6)  # Width of the detection cone when the car is going at medium speed
            self.height_medium = 15 * random.randint(1, 6)  # Height of the detection cone when the car is going at medium speed

            self.width_slow = 15 * random.randint(1, 6)  # Width of the detection cone when the car is going slow
            self.height_slow = 15 * random.randint(1, 6)  # Height of the detection cone when the car is going slow




