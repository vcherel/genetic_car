from data.constants import PATH_IMAGE, CAR_SIZES, START_POSITIONS, START_ANGLES, PATH_DATA  # Import the constants
from render.resizing import scale_image, convert_to_new_window  # To resize the images
from data.data_classes import MemoryCar  # Import the class MemoryCar
from render.display import edit_background  # Display functions
from menus.settings_menu import SETTINGS  # Import the settings
from game.genetic import Genetic  # Import the class Genetic
import data.variables as var  # Import the variables
import pygame  # To use pygame
import sys  # To use sys.exit


"""
This file contains all the functions related to the global variables of the game
"""


def init_variables(nb_cars, replay=False):
    """
    Initialize the data of the game (number of car alive, time remaining, start time, ...)
    """
    var.NB_CARS_ALIVE = nb_cars  # Number of cars alive
    var.TICKS_REMAINING = var.TIME_GENERATION * 60  # Number of iterations remaining for the generation
    var.DISPLAY_GARAGE = False  # We don't display the garage
    if replay:  # If we replay from the last cars
        var.NUM_GENERATION += 1
    else:  # If we start a new run
        var.NUM_GENERATION = 1  # Number of the generation


def resize_window(dimensions):
    """
    Resize the window (called when the user resizes the window) and change all the data associated

    Args:
        dimensions (tuple): Dimensions of the window
    """
    var.WIDTH_SCREEN, var.HEIGHT_SCREEN = dimensions  # Update the dimensions
    var.WINDOW = pygame.display.set_mode((var.WIDTH_SCREEN, var.HEIGHT_SCREEN), pygame.RESIZABLE)  # Resize the window
    update_visual_variables()  # Update the visual data
    pygame.display.flip()  # Update the display
    var.BIG_RED_CAR_IMAGE = pygame.transform.rotate(scale_image(pygame.image.load(PATH_IMAGE + '/car.png'), 1.5), 90)

    load_explosions()  # Load the images of the explosions


def update_visual_variables():
    """
    Update the data used to display things according to the size of the new window
    """
    var.SCALE_RESIZE_X = var.WIDTH_SCREEN / 1500  # Scale used to resize the images
    var.SCALE_RESIZE_Y = var.HEIGHT_SCREEN / 700  # Scale used to resize the images
    create_background()  # Create the background
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Blit the background on the window
    pygame.display.flip()  # Update the display


def load_explosions():
    """
    Load the images of the explosions
    """
    var.EXPLOSION_IMAGES = []  # List of all the images of the explosion
    for num in range(1, 10):
        image = pygame.image.load(f'{PATH_IMAGE}explosion/{num}.png')  # Load the image
        image = scale_image(image, CAR_SIZES[var.NUM_MAP] / 25 * var.SCALE_RESIZE_X)  # Scale the image
        var.EXPLOSION_IMAGES.append(image)


def change_map(first_time=False, reverse=False):
    """
    Change the map and all the data associated. It is used at the beginning of the game and when we press the button to change the map
    When it's the first time we keep the actual map but when it's not the case we change the map to the next one

    Args:
        first_time (bool): True if it's the first time we change the map
        reverse (bool): True if we want to go to the previous map
    """
    if not first_time:  # We change the number of the map only if it's not the first time
        if not reverse:
            if var.NUM_MAP >= var.NB_MAPS - 1:
                var.NUM_MAP = 0
            else:
                var.NUM_MAP += 1
        else:
            if var.NUM_MAP == 0:
                var.NUM_MAP = var.NB_MAPS - 1
            else:
                var.NUM_MAP -= 1

    var.START_POSITION = START_POSITIONS[var.NUM_MAP]  # Start position of the cars
    var.START_ANGLE = START_ANGLES[var.NUM_MAP]  # Start angle of the cars
    var.RADIUS_CHECKPOINT = 7.5 * CAR_SIZES[var.NUM_MAP]  # Radius of the checkpoints

    # We create a background to create the mask of collision, this background has a size of 1500*700
    background = pygame.Surface((1500, 700))  # Image of the background
    background.blit(pygame.transform.scale(pygame.image.load(f'{PATH_IMAGE}background/background_{str(var.NUM_MAP)}.png'), (1500, 585)), (0, 115))  # Blit the circuit on the background surface
    var.BACKGROUND_MASK = pygame.mask.from_threshold(background, (0, 0, 0, 255), threshold=(1, 1, 1, 1))  # Mask of the black pixels of the background (used to detect collisions)

    var.RED_CAR_IMAGE = scale_image(pygame.image.load(PATH_IMAGE + 'car.png'), CAR_SIZES[var.NUM_MAP] / 75)  # Image of the car
    create_background()  # Create the background
    var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Screen initialization

    var.CHECKPOINTS = []  # List of checkpoints
    with open(f'{PATH_DATA}/checkpoints/{var.NUM_MAP}', 'r') as file_checkpoint_read:
        """
        Format of the file checkpoints:
        x1 y1
        x2 y2
        ...
        """
        checkpoints = file_checkpoint_read.readlines()
        for checkpoint in checkpoints:
            a, b = checkpoint.split(' ')
            var.CHECKPOINTS.append((int(a), int(b)))

    update_cars_parameters()  # Update all the parameters of the cars
    if SETTINGS.x is not None:  # If the settings window has been initialized
        SETTINGS.update_parameters()  # Update the settings parameters
    load_explosions()  # The explosions are loaded here because they depend on the size of the car


def update_cars_parameters():
    """
    Update the parameters of the cars according to the map
    """
    var.NB_CARS = var.LIST_NB_CARS[var.NUM_MAP]  # Number of cars for the current map
    var.TIME_GENERATION = var.LIST_TIME_GENERATION[var.NUM_MAP]  # Time of a generation for the current map
    var.SEED = var.LIST_SEED[var.NUM_MAP]  # Seed of the game for the current map
    var.MAX_SPEED = var.LIST_MAX_SPEED[var.NUM_MAP]  # Maximum speed of the car for the current map
    var.MIN_MEDIUM_SPEED = var.MAX_SPEED / 3  # Minimum speed of the car to be considered as medium speed
    var.MIN_HIGH_SPEED = var.MAX_SPEED / 1.5  # Minimum speed of the car to be considered as high speed
    var.TURN_ANGLE = var.LIST_TURN_ANGLE[var.NUM_MAP]  # Angle of rotation of the car for the current map
    var.ACCELERATION = var.LIST_ACCELERATION[var.NUM_MAP]  # Acceleration of the car for the current map
    var.DECELERATION = var.LIST_DECELERATION[var.NUM_MAP]  # Deceleration of the car for the current map
    var.DRIFT_FACTOR = var.LIST_DRIFT_FACTOR[var.NUM_MAP]  # Factor of the drift for the current map
    var.WIDTH_CONE = var.LIST_WIDTH_CONE[var.NUM_MAP]  # Width multiplier of the cone for the current map
    var.LENGTH_CONE = var.LIST_LENGTH_CONE[var.NUM_MAP]  # Length multiplier of the cone for the current map
    var.CHANCE_CROSSOVER = var.LIST_CHANCE_CROSSOVER[var.NUM_MAP]  # Chance of crossover for the current map
    var.CHANCE_MUTATION = var.LIST_CHANCE_MUTATION[var.NUM_MAP]  # Chance of mutation for the current map
    var.PROPORTION_CARS_KEPT = var.LIST_PROPORTION_CARS_KEPT[var.NUM_MAP]  # Percentage used to know how many cars we keep for the next generation for the current map


def create_background():
    """
    Create the background
    This background will be shown but will not be used to detect collisions
    """
    var.BACKGROUND = pygame.Surface((var.WIDTH_SCREEN, var.HEIGHT_SCREEN))  # Image of the background
    var.BACKGROUND.fill((128, 128, 128))  # Fill the background with grey
    edit_background()  # Edit the background
    blit_circuit()  # Blit the circuit on the background surface


def blit_circuit():
    """
    Blit the circuit on the background surface. The size of the circuit is 1500*585
    """
    if not var.SHOW_HEATMAP or var.NUM_MAP == 5:
        var.BACKGROUND.blit(scale_image(pygame.image.load(f'{PATH_IMAGE}background/background_{str(var.NUM_MAP)}.png')), convert_to_new_window((0, 115)))
    else:
        var.BACKGROUND.blit(scale_image(pygame.image.load(f'{PATH_IMAGE}background/heatmap_{str(var.NUM_MAP)}.png')), convert_to_new_window((0, 115)))


def load_parameters():
    """
    Load the parameters of the different maps stored in the file parameters, and the number of the camera
    """
    # The number of the camera is stored in a file
    with open(PATH_DATA + 'num_camera', 'r') as file_num_camera_read:
        var.NUM_CAMERA = int(file_num_camera_read.readline())  # Number of the camera

    with open(PATH_DATA + 'parameters_map', 'r') as file_parameters_read:
        """
        Format of the file parameters_map:
        # Circuit x
        param1 = value1
        param2 = value2
        ...
        # Circuit y
        param1 = value1
        ...
        """
        lines = file_parameters_read.readlines()  # We read the file
        actual_map = -1  # Actual map (-1 because we start with the map 0)
        for line in lines:
            if line[0] == '#':
                actual_map += 1  # We change the map
            else:
                line_split = line.split()
                if line_split:
                    param = line.split()[0]
                    if param == 'nombre_voitures':
                        var.LIST_NB_CARS[actual_map] = int(line.split()[2])
                    elif param == 'temps_par_generation':
                        var.LIST_TIME_GENERATION[actual_map] = int(line.split()[2])
                    elif param == 'seed':
                        var.LIST_SEED[actual_map] = int(line.split()[2])
                    elif param == 'vitesse_max':
                        var.LIST_MAX_SPEED[actual_map] = int(line.split()[2])
                    elif param == 'angle_rotation':
                        var.LIST_TURN_ANGLE[actual_map] = int(line.split()[2])
                    elif param == 'force_acceleration':
                        var.LIST_ACCELERATION[actual_map] = float(line.split()[2])
                    elif param == 'force_freinage':
                        var.LIST_DECELERATION[actual_map] = float(line.split()[2])
                    elif param == 'coef_derapage':
                        var.LIST_DRIFT_FACTOR[actual_map] = float(line.split()[2])
                    elif param == 'largeur_cone':
                        var.LIST_WIDTH_CONE[actual_map] = int(line.split()[2])
                    elif param == 'longueur_cone':
                        var.LIST_LENGTH_CONE[actual_map] = int(line.split()[2])
                    elif param == 'chance_croisement':
                        var.LIST_CHANCE_CROSSOVER[actual_map] = float(line.split()[2])
                    elif param == 'chance_mutation':
                        var.LIST_CHANCE_MUTATION[actual_map] = float(line.split()[2])
                    elif param == 'proportion_selection':
                        var.LIST_PROPORTION_CARS_KEPT[actual_map] = float(line.split()[2])


def load_cars():
    """
    Load the cars stored in the file cars (and initialize the big red car image)
    """
    with open(PATH_DATA + 'cars', 'r') as file_cars_read:
        """
        Format of the file cars:
        id name color width_fast  length_slow  length_medium  length_fast  width_slow  width_medium  width_fast score_map1  score_map2  score_map3  score_map4  score_map5
        ...
        """
        lines = file_cars_read.readlines()  # We read the file
        for line in lines:
            line = line.split(' ')

            id_car = int(line[0])  # Id of the car (unique int)
            name = line[1]  # Name of the car
            color = line[2]  # Color of the car
            genetic = Genetic([int(line[i]) for i in range(3, 9)])  # Genetic of the car
            scores = [int(line[i]) for i in range(9, 9 + var.NB_MAPS)]  # Scores of the car for each map

            var.MEMORY_CARS.append(MemoryCar(id_car, name, color, genetic, scores))  # We create the memory car
            if var.ACTUAL_IDS_MEMORY_CARS <= id_car:
                var.ACTUAL_IDS_MEMORY_CARS = id_car + 1

    # We load the image of the car (we do it here because we have to do it during the initialization of the game so why not)
    var.BIG_RED_CAR_IMAGE = pygame.transform.rotate(scale_image(pygame.image.load(PATH_IMAGE + '/car.png'), 1.5), 90)


def save_cars():
    """"
    Save the cars in the file cars
    """
    with open(PATH_DATA + 'cars', 'w') as file_cars_write:
        for memory_car in var.MEMORY_CARS:
            str_to_write = f'{memory_car.id} {memory_car.name} {memory_car.color} {memory_car.genetic}'
            for score in memory_car.best_scores:
                str_to_write += f' {int(score)}'  # We cast to int because it can be a float vor the waiting map
            str_to_write += '\n'
            file_cars_write.write(str_to_write)


def exit_game():
    """
    Exit the game
    """
    save_cars()  # Save the cars
    sys.exit()  # Quit pygame


def checkpoint_reached(pos, checkpoint):
    """
    Check if the position is in the radius of a checkpoint

    Args:
        pos (tuple(int, int)): the position to check
        checkpoint (tuple(int, int)): the checkpoint to check

    Returns:
        True if the position is in the radius of the checkpoint
    """
    return checkpoint[0] - var.RADIUS_CHECKPOINT < pos[0] < checkpoint[0] + var.RADIUS_CHECKPOINT and \
        checkpoint[1] - var.RADIUS_CHECKPOINT < pos[1] < checkpoint[1] + var.RADIUS_CHECKPOINT
