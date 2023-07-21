from src.data.data_classes import MemoryCar  # Import the car memory
import itertools  # Used to get all the combinations of cars
import src.data.variables as var  # Variables of the game
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
    cars = [car for car in cars if not car.id_memory_car]  # We remove the cars that are only here for the visuals

    if cars:
        # We sort the cars by score
        cars = sorted(cars, key=lambda c: c.score, reverse=True)  # Sort the cars by score

        cars_to_keep = find_cars_to_keep(cars)  # We find the cars to keep (the best cars)
        cars = init_cars(cars_to_keep, var.NB_CARS - len(cars_to_keep))  # Select the best cars that we will mutate


        # We change the genetic algorithm mode if we are in the test mode
        if var.TEST_MUTATION_CROSSOVER:
            cars = apply_genetic_test(cars, cars_to_keep)
        else:
            crossover(cars)  # Crossover the cars
            cars = mutate(cars, cars_to_keep)  # Mutate the cars


        add_cars_to_keep(cars, cars_to_keep)  # We add the best cars to the list
    else:
        cars = [Car() for _ in range(var.NB_CARS)]  # If there is no car, we add random cars

    for car in cars:
        print(car)

    return cars


def apply_genetic_test(cars, cars_to_keep):
    """
    Do the correct genetic algorithm based on the test mode

    Args:
        cars (list): list of cars
        cars_to_keep (list): list of cars we will not mutate and keep in the next turn

    Returns:
        list: list of cars with the genetic algorithm applied
    """
    if var.TEST_MODE == 'mutation_only':
        cars = mutate(cars, cars_to_keep)  # Mutate the cars
    elif var.TEST_MODE == 'mutation_crossover':
        cars = mutate(cars, cars_to_keep)  # Mutate the cars
        crossover(cars)  # Crossover the cars
    elif var.TEST_MODE == 'crossover_mutation':
        crossover(cars)
        cars = mutate(cars, cars_to_keep)  # Mutate the cars

    return cars


def find_cars_to_keep(cars):
    """
    Find the cars to keep (the best cars) and add the best car to the memory

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars to keep
    """
    number_to_keep = max(min(int(var.PROPORTION_CARS_KEPT * len(cars)), var.NB_CARS), 1)  # Number of cars to keep
    cars_to_keep = cars[:number_to_keep]  # We keep the best cars

    best_car = cars_to_keep[0]  # We get the best car
    var.MEMORY_CARS.append(MemoryCar(var.ACTUAL_IDS_MEMORY_CARS, f'Génération_{var.NUM_GENERATION}',
                                     'gray', best_car.genetic, best_car.best_scores))  # Add the best car to the memory
    var.ACTUAL_IDS_MEMORY_CARS += 1  # We increment the id of the memory cars

    return cars_to_keep


def init_cars(cars_to_keep, number_cars):
    """
    Initialize the cars we will mutate and crossover

    Args:
        cars_to_keep (list): list of cars we will copy
        number_cars (int): number of cars we will mutate and crossover

    Returns:
        list: list of the cars we will mutate and crossover
    """
    # Calculate the weights based on the car scores
    weights = [car.score for car in cars_to_keep]
    total_weight = sum(weights)
    if total_weight == 0:  # To avoid division by 0
        total_weight = 1
    probabilities = [weight / total_weight for weight in weights]

    selected_cars = random.choices(cars_to_keep, probabilities, k=number_cars)  # We choose the cars based on their probabilities
    cars = [car.copy() for car in selected_cars]

    return cars


def mutate(cars, cars_to_keep):
    """
    Mutate the cars

    Args:
        cars (list): list of cars
        cars_to_keep (list): list of cars we will not mutate and keep in the next turn

    Returns:
        list: list of cars mutated
    """
    new_cars = []  # List of new cars

    for car in cars:
        added = False
        while not added:
            mutate_one_car(car)  # Mutate the car
            if car not in new_cars and car not in cars_to_keep:  # If the car is not already in the list or if we have tried too many times
                added = True
                new_cars.append(car)  # We add the car to the list

    return new_cars


def mutate_one_car(car):
    """
    Mutate one car

    Args:
        car (Car): the car to mutate
    """
    has_muted = False  # True if the car has mutated
    while not has_muted:  # We try mutating the car until it mutates
        dice_values = car.genetic.dice_values.copy()  # We copy the dice values
        for index, value in enumerate(car.genetic.dice_values):
            if random.random() < var.CHANCE_MUTATION:
                has_muted = True
                dice_values[index] = random_attribution(value)  # We change the value of the dice
        car.genetic.dice_values = dice_values


def crossover(cars):
    """
    Crossover the cars (exchange some attributes between two cars)

    Args:
        cars (list): list of cars

    Returns:
        list: list of cars crossed
    """
    for car1, car2 in itertools.combinations(cars, 2):  # We take all the combinations of cars
        if random.random() < var.CHANCE_CROSSOVER and car1 != car2:  # If we do a crossover
            car_added = False
            count = 0
            while not car_added and count < 10:  # We try to add the cars until we succeed, or we have tried too many times
                count += 1
                number_attributes_exchanged = random.randint(1, 6)  # We choose a random number of attributes to exchange
                ids_changed_attributes = random.sample(range(0, 6), number_attributes_exchanged)  # We choose the attributes to exchange
                for i, value in enumerate(car1.genetic.dice_values):
                    if i in ids_changed_attributes:
                        car1.genetic.dice_values[i], car2.genetic.dice_values[i] = car2.genetic.dice_values[i], value
                        new_car_1 = Car(genetic=car1.genetic, best_scores=car1.best_scores, color=car1.color)
                        new_car_2 = Car(genetic=car2.genetic, best_scores=car2.best_scores, color=car2.color)

                        # We verify that the new cars are not already in the list
                        if new_car_1 not in cars and new_car_2 not in cars:
                            cars.remove(car1)
                            cars.remove(car2)
                            cars.append(new_car_1)
                            cars.append(new_car_2)
                        break


def add_cars_to_keep(cars, cars_to_keep):
    """
    Add the best cars to the list

    Args:
        cars (list): list of cars that have been mutated and crossed
        cars_to_keep (list): list of cars to keep (the best cars)

    Returns:
        list: list of cars
    """
    for car in cars_to_keep[1:]:
        cars.append(Car(genetic=car.genetic, best_scores=car.best_scores))

    best_car = cars_to_keep[0]  # We add the best car at the end, so we will see it on top of the others
    cars.append(Car(genetic=best_car.genetic, best_scores=best_car.best_scores, color='yellow'))


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
