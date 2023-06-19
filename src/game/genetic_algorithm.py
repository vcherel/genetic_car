from src.game.constants import WIDTH_MULTIPLIER, HEIGHT_MULTIPLIER   # Constants of the game
from src.render.garage import add_garage_cars  # Add the cars from the garage
import src.other.variables as var  # Variables of the game
import random  # Used to generate random numbers
from src.game.car import Car  # Import the car

"""
This file contains all the functions used to apply the genetic algorithm to the cars (selection, mutation, crossover)
"""


def apply_genetic(cars):
    """
    Apply the genetic algorithm to the cars

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars with the genetic algorithm applied
    """
    cars = [car for car in cars if not car.view_only]  # We remove the cars that are only here for the visuals

    # Update the score of the cars to take into account the time
    for car in cars:
        car.update_score()  # Update the score of the cars

    cars = sorted(cars, key=lambda c: c.score, reverse=True)  # Sort the cars by score

    if cars:  # If there is at least one car
        best_car = Car(cars[0].genetic, best_car=True)  # Get the best car

        var.MEMORY_CARS.get('genetic').append([var.NUM_GENERATION, 'Génération_' + str(var.NUM_GENERATION), best_car.genetic])  # Add the best car to the memory

        cars = select_best_cars(cars)  # Select the best cars
        cars = mutate(cars)  # Mutate the cars
        cars = crossover(cars)  # Crossover the cars

        cars.append(best_car)  # Add the best car to the list
    cars = add_garage_cars(cars)  # We add the car from the garage to the list

    return cars


def select_best_cars(cars):
    """
    Select the best cars to keep for the next generation
    We keep the best car, and we copy it to have the same number of cars

    Args:
        cars (list): list of cars

    Returns:
        list: list of the best cars
    """
    # We keep the best cars
    best_cars = cars[:int(len(cars) * var.PERCENTAGE_BEST_CARS)]
    if not best_cars:
        best_cars = [Car()]  # If there is no cars we add a new one

    # We copy the best car randomly to have the same number of cars as before
    cars = []
    while len(cars) < var.NB_CARS - 1:  # Not <= because we will add the best car at the end
        cars.append(Car(random.choice(best_cars).genetic))

    return cars  # List of cars


def mutate(cars):
    """
    Mutate the cars

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars mutated
    """
    for car in cars:
        has_muted = False
        while not has_muted:
            for attribute_name, attribute_value in vars(car.genetic).items():
                if random.random() < var.MUTATION_CHANCE:
                    has_muted = True
                    # See if it is a width or a height
                    if attribute_name.startswith('width'):
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
            if random.random() < var.CROSSOVER_CHANCE:  # If we do a crossover
                car1, car2 = (cars[i], cars[j])
                id_changed_attribute = random.randint(0, 5)  # We choose a random attribute to exchange
                for k, (attribute_name, attribute_value) in enumerate(vars(car1.genetic).items()):
                    if k == id_changed_attribute:
                        setattr(car1.genetic, attribute_name, getattr(car2.genetic, attribute_name))
                        setattr(car2.genetic, attribute_name, attribute_value)
                        break
    return cars


def random_attribution(value):
    """
    We want to attribute a random value to a variable, but we want that values close to the actual value has more chance

    Args:
        value (int): the actual value (between 1 and 6)

    Returns:
        value (int): the new value (between 1 and 6)
    """
    rand = random.random()
    if rand < 1/5:
        value = value + random.uniform(-5, 5)  # We add a random value between -1 and 1
    elif rand < 1/4:
        value = value + random.uniform(-4, 4)
    elif rand < 1/3:
        value = value + random.uniform(-3, 3)
    elif rand < 1/2:
        value = value + random.uniform(-2, 2)
    else:
        value = value + random.uniform(-1, 1)
    return max(1, min(6, round(value)))  # We round the value between 1 and 6
