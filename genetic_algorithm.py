import random  # Used to generate random numbers
import variables  # Variables of the game
from constants import WIDTH_MULTIPLIER, HEIGHT_MULTIPLIER, START_POS, CROSSOVER_CHANCE, MUTATION_CHANCE  # Constants of the game
from utils import random_attribution  # Used to randomly attribute a value to a variable
from car import Car  # Import the car


def apply_genetic(cars):
    """
    Apply the genetic algorithm to the cars

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars with the genetic algorithm applied
    """
    cars = sorted(cars, key=lambda car: car.score, reverse=True)  # Sort the cars by score
    cars = select_best_cars(cars)  # Select the best cars
    cars = mutate(cars)  # Mutate the cars
    cars = crossover(cars)  # Crossover the cars
    return cars


def select_best_cars(cars):
    """
    Select the best cars to keep for the next generation
    We keep the best car and we copy them

    Args:
        cars (list): list of cars

    Returns:
        list: list of the best cars
    """
    return [Car(variables.CAR_IMAGE, START_POS[variables.NUM_MAP], cars[0].genetic) for _ in range(variables.NB_CARS)]  # List of cars


def mutate(cars):
    """
    Mutate the cars

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars mutated
    """
    for car in cars:
        for attribute_name, attribute_value in vars(car.genetic).items():
            if random.random() < MUTATION_CHANCE:
                # See if it is a width or a height
                if attribute_name.startswith("width"):
                    multiplier = WIDTH_MULTIPLIER
                else:
                    multiplier = HEIGHT_MULTIPLIER
                actual_value = int(getattr(car.genetic, attribute_name) / multiplier)  # Get the actual value of the attribute
                setattr(car.genetic, attribute_name, multiplier * random_attribution(actual_value))
    return cars


def crossover(cars):
    """
    Crossover the cars

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars crossed
    """
    for i in range(len(cars)):
        for j in range(i + 1, len(cars)):  # We search for all pairs of cars
            if random.random() < CROSSOVER_CHANCE:  # If we do a crossover
                car1, car2 = (cars[i], cars[j])
                id_changed_attribute = random.randint(0, 5)  # We choose a random attribute to exchange
                for k, (attribute_name, attribute_value) in enumerate(vars(car1.genetic).items()):
                    if k == id_changed_attribute:
                        setattr(car1.genetic, attribute_name, getattr(car2.genetic, attribute_name))
                        setattr(car2.genetic, attribute_name, attribute_value)
                        break
    return cars
