import random  # Used to generate random numbers
import variables  # Variables of the game
from constants import WIDTH_MULTIPLIER, HEIGHT_MULTIPLIER, CROSSOVER_CHANCE, MUTATION_CHANCE   # Constants of the game
from car import Car  # Import the car


def apply_genetic(cars):
    """
    Apply the genetic algorithm to the cars

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars with the genetic algorithm applied
    """
    cars = sorted(cars, key=lambda c: c.score, reverse=True)  # Sort the cars by score
    best_car = Car(cars[0].genetic)  # Get the best car
    if variables.MEMORY_CARS.get(variables.ACTUAL_ID_MEMORY_GENETIC) is None:  # If it is the first time we run the genetic algorithm
        variables.MEMORY_CARS[variables.ACTUAL_ID_MEMORY_GENETIC] = [[1, best_car.genetic]]  # Add the best car to the memory
    else:
        variables.MEMORY_CARS[variables.ACTUAL_ID_MEMORY_GENETIC].append((variables.NUM_GENERATION, best_car.genetic))  # Add the best car to the memory

    cars = select_best_cars(cars)  # Select the best cars
    cars = mutate(cars)  # Mutate the cars
    cars = crossover(cars)  # Crossover the cars

    cars.append(best_car)  # Add the best car to the list

    # We add the car from the garage to the list
    """
    if variables.CAR_FROM_GARAGE is not None:  # If we have a car from the garage
        if type(variables.CAR_FROM_GARAGE) is list:  # If we have a car from the garage
            for car in variables.CAR_FROM_GARAGE:
                cars.append(car)  # Add cars from the garage to the list
        else:
            cars.append(variables.CAR_FROM_GARAGE)  # Add the car from the garage to the list
    """
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
    return [Car(cars[0].genetic) for _ in range(variables.NB_CARS - 1)]  # List of cars (-1 because we will add the best car)


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
