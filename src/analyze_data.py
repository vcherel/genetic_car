from data.constants import PATH_DATA  # Import the path of the data
from statistics import mean  # To use statistics on the data
import data.variables as var  # To use the global variables
import matplotlib.pyplot as plt  # To plot the boxplot
import os  # To iterate over the files in a folder
import matplotlib  # To export the boxplot to pgf
import pylab  # To use the boxplot
import pygame  # To use pygame

matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'font.size': 11,
    'text.usetex': True,
    'pgf.rcfonts': False,
})

"""
This file contains the functions to analyze the data from the test file (created from the file main.py)
This data can be the score of the cars, to determine where each car died ; or the mean BGR value of values
"""

number_checkpoints = [143, 131, 144, 113, 57, 0, 146, 156]


def analyze_test_all_cars(num_map, show_graph=False):
    """
    Analyze the data from the test file 'test_all_cars_X' created from the file main.py (with X the number of the map) and write the results in a file
    named 'analysis_X'
    The data concerns the score of the cars, to determine where each car died on the track and how many cars completed a lap

    Args:
        num_map (int): The number of the map
        show_graph (bool): If True, show the histogram of the scores
    """
    scores = []  # List of the scores
    best_cars = []  # List of the best cars (cars that completed a lap)

    with open(f'{PATH_DATA}tests/all_cars/results/{num_map}', 'r') as file_read:
        with open(f'{PATH_DATA}tests/all_cars/analysis/{num_map}', 'w') as file_write:
            for line in file_read:
                data = line.split(' ')
                if num_map == 5:
                    score = int(float(data[6][:-1]) / 100)  # We remove the \n and transform the score to a smaller value (int)
                else:
                    score = int(data[6][:-1])  # We remove the \n

                scores.append(score)  # We add the score to the list of the scores

                # Find when the car died
                if score > number_checkpoints[num_map]:
                    best_cars.append((int(data[0]), int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), score))

            # Sort the best cars by score
            best_cars.sort(key=lambda x: x[6], reverse=True)
            file_write.write(f'Cars that completed a lap: ({len(best_cars)})\n')
            for car in best_cars:
                file_write.write(f'{car[0]}, {car[1]}, {car[2]}, {car[3]}, {car[4]}, {car[5]} ; Score : {car[6]}\n')

    if show_graph:
        # Plotting the histogram
        plt.hist(scores, bins=50, range=(0, 100), edgecolor='black')  # Adjust the number of bins as needed
        plt.xlabel('Score')
        plt.ylabel('Count')
        plt.title('Distribution of Scores')

        # Display the plot
        plt.show()


def show_positions_crash(scores):
    """
    Show the analysis of the death of cars obtained by the function analyze_data_scores, by drawing circles on the background
    The more car crashed at a position, the more the circle is red

    Args:
        scores (list): List of the scores
    """
    scores = [score for score in scores if score < len(var.CHECKPOINTS)]

    deaths_by_checkpoints = [0] * len(var.CHECKPOINTS)
    for score in scores:
        deaths_by_checkpoints[score] += 1

    deaths_worst_checkpoint = max(deaths_by_checkpoints)  # Best score

    # Draw the circles
    for pos, score in zip(var.CHECKPOINTS, deaths_by_checkpoints):  # Iterate over the checkpoints

        # Calculate the red value based on the score
        red_value = int(score / deaths_worst_checkpoint * 255)  # Adjust the scaling if needed

        # If it is not white
        if red_value != 0:
            # Create the color tuple with the adjusted red value
            circle_color = (255, 255 - red_value, 255 - red_value)

            # Draw the circle with the calculated color
            pygame.draw.circle(var.BACKGROUND, circle_color, pos, 25)

    pygame.display.flip()


def compute_mean_bgr():
    """
    Compute the mean BGR value using the data in the mean_bgr file

    Returns:
        mean_b (float): Mean B value
        mean_g (float): Mean G value
        mean_r (float): Mean R value
    """
    b, g, r = [], [], []
    with open(PATH_DATA + 'mean_bgr', 'r') as file:
        for line in file:
            bgr = line.split()
            b.append(float(bgr[0]))
            g.append(float(bgr[1]))
            r.append(float(bgr[2]))

    return mean(b), mean(g), mean(r)


def analyze_genetic_algorithm():
    """
    Analyze the data from the genetic algorithm
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

    fig = matplotlib.pyplot.gcf()  # Get the current figure
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


if __name__ == '__main__':
    analyze_genetic_algorithm()
