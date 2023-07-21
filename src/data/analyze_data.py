from src.data.constants import PATH_DATA  # Import the path of the data
from statistics import mean, median, variance  # To use statistics on the data
import matplotlib.pyplot as plt  # For plotting the histogram
import src.data.variables as var  # For the path of the data
import os  # To iterate over the files in a folder
import pylab  # To use the boxplot
import pygame  # To use pygame

"""
This file contains the functions to analyze the data from the test file (created from the file main.py)
This data can the score of the cars, to determine where each car died ; or the mean BGR value of values
"""


def analyze_data_scores(name_file_read, name_file_write):
    """
    Analyze the data from the test file (created from the file main.py) and write the results in a file
    The data concerns the score of the cars, to determine where each car died

    Args:
        name_file_read (str): Name of the file to read
        name_file_write (str): Name of the file to write

    Returns:
        scores (list): List of the scores
    """
    scores = []  # List of the scores
    best_cars = []  # List of the best cars (cars that completed a lap)

    with open(PATH_DATA + name_file_read, 'r') as file_read:
        with open(PATH_DATA + name_file_write, 'w') as file_write:
            for line in file_read:
                data = line.split(' ')
                score = int(data[7][:-1])  # We remove the \n

                scores.append(score)  # We add the score to the list of the scores

                # Find when the car died
                if score > 150:
                    best_cars.append((int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), score))

            # Sort the best cars by score
            best_cars.sort(key=lambda x: x[6], reverse=True)
            file_write.write('Cars that completed a lap:\n')
            for car in best_cars:
                file_write.write(f'{car[0]}, {car[1]}, {car[2]}, {car[3]}, {car[4]}, {car[5]} ; Score : {car[6]}\n')

    # Plotting the histogram
    plt.hist(scores, bins=50, range=(0, 100), edgecolor='black')  # Adjust the number of bins as needed
    plt.xlabel('Score')
    plt.ylabel('Count')
    plt.title('Distribution of Scores')

    # Display the plot
    plt.show()

    return scores


def show_positions_crash(scores):
    """
    Show the analysis of the death of cars obtained by the function analyze_data, by drawing circles on the background
    """
    scores = [score for score in scores if score < len(var.CHECKPOINTS)]

    turns = [0] * len(var.CHECKPOINTS)
    for score in scores:
        turns[score] += 1
    max_turns = max(turns)

    # Draw the circles
    for pos, score in zip(var.CHECKPOINTS, turns):

        # Calculate the red value based on the score
        red_value = int(score / max_turns * 255)  # Adjust the scaling if needed

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
    with open(var.PATH_DATA + 'mean_bgr', 'r') as file:
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
    mutation_crossover = []  # The number of generations to complete a lap with mutation and then crossover
    crossover_mutation = []  # The number of generations to complete a lap with crossover and then mutation
    with open(var.PATH_DATA + 'test_mutation_only_2', 'r') as file:
        for line in file:
            data = line.split()
            mutation_only.append(int(data[0]))

    with open(var.PATH_DATA + 'test_mutation_crossover_2', 'r') as file:
        for line in file:
            data = line.split()
            mutation_crossover.append(int(data[0]))

    with open(var.PATH_DATA + 'test_crossover_mutation_2', 'r') as file:
        for line in file:
            data = line.split()
            crossover_mutation.append(int(data[0]))

    data = [mutation_only, mutation_crossover, crossover_mutation]
    plt.boxplot(data)  # Plot the boxplot
    plt.title('Nombre de générations pour compléter un tour\n pour les 3 algorithmes génétiques (sur 150 essais)')
    plt.ylim(0, 15)  # Adjust the y-axis as needed
    plt.ylabel('Nombre de générations')
    pylab.xticks([1, 2, 3], ['Mutation', 'Mutation-crossover', 'Crossover-mutation'])  # Add legend

    plt.savefig('algo_gen.png')
    plt.show()

    print(mean(mutation_only), mean(mutation_crossover), mean(crossover_mutation))
    print(median(mutation_only), median(mutation_crossover), median(crossover_mutation))
    print(variance(mutation_only), variance(mutation_crossover), variance(crossover_mutation))


def analyze_value_genetic_parameters():
    """
    This function analyzes the values that we got from the test of genetic parameters
    We read all files in the data/test folder, and we look at the mean number of generation needed to complete a lap
    """
    dict_mean_values = {}  # Dictionary of the mean values for each parameter

    for filename in os.listdir(var.PATH_DATA + 'tests/'):
        f = var.PATH_DATA + 'tests/' + filename
        list_values = []  # List of the values for the current file
        with open(f, 'r') as file:
            for line in file:
                list_values.append(int(line.split()[0]))
        if len(list_values) != 0:
            dict_mean_values[filename] = mean(list_values)

    # Sort the dictionary by values
    dict_mean_values = {k: v for k, v in sorted(dict_mean_values.items(), key=lambda item: item[1])}
    print(dict_mean_values)  # The name of the file is test_MutationRate_CrossoverRate_SelectionRate


if __name__ == '__main__':
    analyze_value_genetic_parameters()