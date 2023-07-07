from src.other.constants import PATH_DATA  # Import the path of the data
import matplotlib.pyplot as plt  # For plotting the histogram
import src.other.variables as var  # For the path of the data
import pygame  # To use pygame

"""
This file contains the functions to analyze the data from the test file (created in the file main.py)
This data concerns the score of the cars, to determine where each car died
It has been created by 
"""


def analyze_data(file_name_read, file_name_write):
    """
    Analyze the file file_name_read and write the result in the file file_name_write

    Args:
        file_name_read (str): Name of the file to read
        file_name_write (str): Name of the file to write

    Returns:
        scores (list): List of the scores
    """
    scores = []  # List of the scores
    best_cars = []  # List of the best cars (cars that completed a lap)

    with open(PATH_DATA + file_name_read, 'r') as file_read:
        with open(PATH_DATA + file_name_write, 'w') as file_write:
            for line in file_read:
                data = line.split(' ')
                score = int(data[7][:-1])  # We remove the \n

                scores.append(score)  # We add the score to the list of the scores

                # Find when the car died
                if score > 150:
                    best_cars.append((int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), score))

            # Sort the best cars by score
            best_cars.sort(key=lambda x: x[6], reverse=True)
            file_write.write('Best cars:\n')
            for car in best_cars:
                file_write.write(f'{car[0]}, {car[1]}, {car[2]}, {car[3]}, {car[4]}, {car[5]} ; Score : {car[6]}\n')

    # Plotting the histogram
    plt.hist(scores, bins=10, edgecolor='black')  # Adjust the number of bins as needed
    plt.xlabel('Score')
    plt.ylabel('Count')
    plt.title('Distribution of Scores')

    # Display the plot
    plt.show()

    return scores


def show_analysis(scores):
    """
    Show the analysis of the scores obtained by the function analyze_data, by drawing circles on the background
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


def compute_mean_bgr():
    """
    Compute the mean BGR value using the data in the mean_bgr file
    """
    b, g, r = [], [], []
    with open(var.PATH_DATA + '/mean_bgr', 'r') as file:
        for line in file:
            bgr = line.split()
            b.append(float(bgr[0]))
            g.append(float(bgr[1]))
            r.append(float(bgr[2]))

    mean_b = sum(b) / len(b)
    mean_g = sum(g) / len(g)
    mean_r = sum(r) / len(r)

    return mean_b, mean_g, mean_r



if __name__ == '__main__':
    mean_bgr = compute_mean_bgr()
    print(mean_bgr)