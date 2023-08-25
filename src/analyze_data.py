from data.constants import PATH_DATA  # Import the path of the data
from render.resizing import scale_image  # To scale the image
from statistics import mean  # To use statistics on the data
import matplotlib.pyplot as plt  # To plot the boxplot
import data.variables as var  # To get the window size
import os  # To iterate over the files in a folder
import numpy as np  # To use numpy arrays
import pylab  # To use the boxplot
import pygame  # To use pygame


# Used to save image for LaTeX
"""
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'font.size': 11,
    'text.usetex': True,
    'pgf.rcfonts': False,
})
"""


"""
This file contains the functions to analyze the data from the test file (created from the file main.py)
This data can be the score of the cars, to determine where each car died ; or the mean BGR value of values
"""

number_checkpoints = [143, 131, 144, 113, 57, 0, 146, 156]


class BestCar:
    def __init__(self, data):
        """
        Initialize the BestCar object

        Args:
            data (list): The data of the car (x1, y1, x2, y2, x3, y3, score)
        """
        data = [int(data) for data in data]
        self.x1, self.y1, self.x2, self.y2, self.x3, self.y3, self.score = data
        self.tab = [self.x1, self.y1, self.x2, self.y2, self.x3, self.y3]

    def __str__(self):
        """
        Return the string representation of the BestCar object to write it in a file
        Returns:
            str: The string representation of the BestCar object
        """
        return f'({self.x1}, {self.y1}, {self.x2}, {self.y2}, {self.x3}, {self.y3}) ; Score : {self.score}'

    def __getitem__(self, item):
        """
        Return the item of the BestCar object corresponding to the index
        Args:
            item (int): The index of the item to return

        Returns:
            int: The parameter of the BestCar object corresponding to the index
        """
        return self.tab[item]


def analyze_test_all_cars(num_map):
    """
    Analyze the data from the test file 'test_all_cars_X' created from the file main.py (with X the number of the map) and write the results in a file
    named 'analysis_X'
    The data concerns the score of the cars, to determine where each car died on the track and how many cars completed a lap

    Args:
        num_map (int): The number of the map
    """
    nb_checkpoints = number_checkpoints[num_map]  # The number of checkpoints of the map

    scores = []  # List of the scores [score1, score2, ...]
    cars = []  # List of all the cars [(x1, y1, x2, y2, x3, y3, score1), (x1, y1, x2, y2, x3, y3, score2), ...]
    best_cars = []  # List of the cars that completed a lap [(x1, y1, x2, y2, x3, y3, score1), (x1, y1, x2, y2, x3, y3, score2), ...]

    with open(f'{PATH_DATA}tests/all_cars/results/{num_map}', 'r') as file_read:
        for line in file_read:
            data = line.split(' ')

            # We get the score of the cars
            if num_map == 5:
                return  # We don't analyze the data of the map 5
            else:
                score = int(data[6][:-1])  # We remove
            scores.append(score)  # We add the score to the list
            cars.append(BestCar(data))

            if score > nb_checkpoints:
                best_cars.append(BestCar(data))

        # Sort the scores
        scores.sort(reverse=True)  # We sort the scores in descending order

        # Sort the best cars by score
        best_cars.sort(key=lambda x: x.score, reverse=True)

    with open(f'{PATH_DATA}tests/all_cars/analysis/{num_map}', 'w') as file_write:

        # We count how many cars completed at least 1 lap, 2 laps, 3 laps, ...
        multiplier = 1  # The number of laps
        end_loop = False  # If True, we stop the loop
        nb_cars = 0  # The number of cars that completed at least multiplier laps
        while not end_loop:
            for car in best_cars:
                if car.score >= multiplier * nb_checkpoints:
                    nb_cars += 1
            if nb_cars > 0:
                if multiplier == 1:
                    file_write.write(f'Cars that completed at least one lap : {nb_cars}\n')
                else:
                    file_write.write(f'Cars that completed at least {multiplier} lap : {nb_cars}\n')
                multiplier += 1
                nb_cars = 0
            else:
                end_loop = True

        # Statistics on the scores
        file_write.write(f'\nMean score : {mean(scores)}\n')
        file_write.write(f'Max score : {max(scores)}\n')
        file_write.write(f'Min score : {min(scores)}\n')
        file_write.write(f'Median score : {scores[len(scores) // 2]}\n')

        # Correlation between the parameters and the score
        name_parameters = ['Length slow', 'Length medium', 'Length fast', 'Width slow', 'Width medium', 'Width fast']
        file_write.write('\nCorrelation between the parameters and the score:\n')
        for j in range(0, 6):
            file_write.write(f'{name_parameters[j]} : {np.corrcoef([car[j] for car in cars], scores)[0][1]}\n')

        # We write the scores of the cars that completed at least 1 lap
        file_write.write('\nParameters of the cars that completed at least one lap:\n')
        for car in best_cars:
            file_write.write(f'{car}\n')


def show_graph(num_map):
    """
    Show the graph of the scores

    Args:
        num_map (int): The number of the map
    """
    scores = []  # List of the scores [score1, score2, ...]

    with open(f'{PATH_DATA}tests/all_cars/results/{num_map}', 'r') as file_read:
        for line in file_read:
            data = line.split(' ')

            # We get the score of the cars
            if num_map == 5:
                score = int(float(data[6][:-1]) / 100)  # We remove the \n and transform the score to a smaller value (int)
                data[6] = str(score)  # We replace the score in the data
            else:
                score = int(data[6][:-1])  # We remove
            scores.append(score)  # We add the score to the list of the

    # Sort the scores
    scores.sort(reverse=True)  # We sort the scores in descending order

    plt.plot(scores, range(1, len(scores) + 1))
    plt.xlabel('Score')
    plt.ylabel('Number of cars')
    plt.title('Cars remaining on the track /number of checkpoints passed')
    fig = pylab.gcf()
    fig.canvas.manager.set_window_title(f'Map {num_map}')
    plt.show()


def analyze_genetic_algorithm():
    """
    Analyze the data from the two different genetic algorithms (mutation only and crossover then mutation) and plot the boxplot
    """
    mutation_only = []  # The number of generations to complete a lap with only mutation
    crossover_mutation = []  # The number of generations to complete a lap with crossover and then mutation
    with open(f'{PATH_DATA}tests/mutation_only', 'r') as file:
        for line in file:
            data = line.split()
            mutation_only.append(int(data[0]))

    with open(f'{PATH_DATA}tests/crossover_mutation', 'r') as file:
        for line in file:
            data = line.split()
            crossover_mutation.append(int(data[0]))

    data = [mutation_only, crossover_mutation]
    red_square = dict(marker='2', markeredgecolor='red')  # Create a red square for the mean
    plt.boxplot(data, showmeans=True, meanprops=red_square)  # Plot the boxplot
    plt.title('Box-plot du nombre de générations nécessaire pour compléter un tour\n avec 2 algorithmes génétiques différents (sur 150 essais)')
    plt.ylim(0, 15)  # Adjust the y-axis as needed
    plt.ylabel('Nombre de générations')
    pylab.xticks([1, 2], ['Mutations seulement', 'Croisements puis mutations'])  # Add legend

    fig = plt.gcf()  # Get the current figure
    fig.set_size_inches(5.2, 3.2)  # Adjust the size of the boxplot
    plt.savefig('algo.pgf')  # Save the boxplot to a pgf file (for LaTeX)


def analyze_value_genetic_parameters():
    """
    This function analyzes the values that we got from the test of genetic parameters
    We read all files in the /data/test folder, and we look at the mean number of generation needed to complete a lap
    """
    dict_mean_values = {}  # keys : the filenames (test_MutationRate_CrossoverRate_SelectionRate), values : the mean number of generations needed to complete a lap

    for filename in os.listdir(PATH_DATA + 'tests/genetic_parameters/'):
        f = f'{PATH_DATA}tests/genetic_parameters/' + filename
        list_values = []  # List of the values for the current file
        with open(f, 'r') as file:
            for line in file:
                list_values.append(int(line.split()[0]))
        if len(list_values) == 50:
            dict_mean_values[filename] = mean(list_values)
        else:
            print(f'Le fichier {filename} ne contient pas 50 valeurs')

    # Sort the dictionary by values
    dict_mean_values = {k: v for k, v in sorted(dict_mean_values.items(), key=lambda item: item[1])}
    for key in dict_mean_values.keys():
        print(f'{key} : {dict_mean_values[key]}')


def show_heat_map(num_map):
    """
    Show the heatmap of death directly on the map
    Args:
        num_map: the number of the map
    """
    scores = []  # List of the scores [score1, score2, ...]
    nb_checkpoints = number_checkpoints[num_map]  # The number of checkpoints of the map

    with open(f'{PATH_DATA}tests/all_cars/results/{num_map}', 'r') as file_read:
        for line in file_read:
            data = line.split(' ')

            # We get the score of the cars
            if num_map == 5:
                return
            else:
                score = int(data[6][:-1])  # We remove

            if score > nb_checkpoints:
                scores.append(score // nb_checkpoints)  # We add the score to the list
            else:
                scores.append(score)  # We add the score to the list

        # Sort the scores
        scores.sort(reverse=True)  # We sort the scores in descending order

    # Transform the scores to a 2D array of coordinates
    with open(f'{PATH_DATA}checkpoints/{num_map}', 'r') as file_read:
        checkpoints = []
        for line in file_read:
            data = line.split(' ')
            checkpoints.append((int(data[0]), int(data[1])))

    coordinate_list = [checkpoints[scores[i] - 1] for i in range(len(scores))]

    # Create a numpy array to store the heatmap intensity
    heat_map = np.zeros((1500, 700))

    # Calculate intensity at each coordinate and update the heatmap
    for coord in coordinate_list:
        x, y = coord
        heat_map[x, y] += 1  # Increase intensity at this coordinate

    heat_map_surface = pygame.Surface((1500, 700), pygame.SRCALPHA)

    for x in heat_map:
        for y in x:
            pygame.draw.circle(heat_map_surface, (255, 0, 0, y * 10), (x, y), 1)

    var.WINDOW.blit(scale_image(heat_map_surface), (0, 0))


if __name__ == '__main__':
    pass