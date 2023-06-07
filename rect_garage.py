from genetic import Genetic  # To use the genetic of the car


class RectGarage:
    def __init__(self, pos, name, genetic):
        """
        Initialization of the rectangle garage
        A Rectangle garage is a rectangle that contains the cars saved in the garage menu

        Args:
            pos (tuple): position of the rectangle
            name (str): name of the rectangle
            genetic (Genetic or list Genetic): genetic of the car (can be a list)
        """
        self.pos = pos  # Position of the rectangle
        self.name = name  # Name of the rectangle
        self.genetic = genetic  # Genetic of the car