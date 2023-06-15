import matplotlib.pyplot as plt


def analyze_file(file_name_read, file_name_write):
    """
    Analyze the file file_name_read and write the result in the file file_name_write

    Args:
        file_name_read (str): Name of the file to read
        file_name_write (str): Name of the file to write
    """
    scores = []  # List of the scores

    best_score = 0  # Score of the best car
    best_genetic = (0, 0, 0, 0, 0, 0)  # Genetic of the best car

    turns = [0] * 11  # The list of the number of cars that died at each turn

    best_cars = []  # List of the best cars (cars that completed a lap)

    with open(file_name_read, 'r') as file_read:
        with open(file_name_write, 'w') as file_write:
            for line in file_read:
                data = line.split(' ')
                score = int(data[7][:-1])  # We remove the \n
                if score < 110:
                    scores.append(score)  # We add the score to the list of the scores

                # Find the best score
                if score > best_score:
                    best_score = int(data[7][:-1])  # We remove the \n
                    best_genetic = (int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]))

                # Find when the car died
                if score > 160:
                    turns[0] += 1  # Number of car that completed a lap
                    best_cars.append((int(data[1]), int(data[2]), int(data[3]), int(data[4]), int(data[5]), int(data[6]), score))
                elif score > 140:
                    turns[10] += 1  # Number of cars that died after the 10th turn
                elif score > 137:
                    turns[9] += 1  # Number of cars that died at the 9th turn
                elif score > 125:
                    turns[8] += 1  # Number of cars that died at the 8th turn
                elif score > 105:
                    turns[7] += 1  # Number of cars that died at the 7th turn
                elif score > 95:
                    turns[6] += 1  # Number of cars that died at the 6th turn
                elif score > 85:
                    turns[5] += 1  # Number of cars that died at the 5th turn
                elif score > 60:
                    turns[4] += 1  # Number of cars that died at the 4th turn
                elif score > 50:
                    turns[3] += 1  # Number of cars that died at the 3rd turn
                elif score > 30:
                    turns[2] += 1  # Number of cars that died at the 2nd turn
                else:
                    turns[1] += 1  # Number of cars that died at the 1st turn

            file_write.write(f'Best car:\nScore : {best_score}\n{best_genetic[0]}, {best_genetic[1]}, {best_genetic[2]}, {best_genetic[3]}, {best_genetic[4]}, {best_genetic[5]}\n\n')

            file_write.write('Best cars:\n')
            for car in best_cars:
                file_write.write(f'{car[0]}, {car[1]}, {car[2]}, {car[3]}, {car[4]}, {car[5]} ; Score : {car[6]}\n')

            file_write.write(f'\nNumber of cars that completed a lap: {turns[0]}\n\n'
                             f'Number of deaths by turn:\n'
                             f'Turn 1: {turns[1]}\n'
                             f'Turn 2: {turns[2]}\n'
                             f'Turn 3: {turns[3]}\n'
                             f'Turn 4: {turns[4]}\n'
                             f'Turn 5: {turns[5]}\n'
                             f'Turn 6: {turns[6]}\n'
                             f'Turn 7: {turns[7]}\n'
                             f'Turn 8: {turns[8]}\n'
                             f'Turn 9: {turns[9]}\n'
                             f'Turn 10: {turns[10]}\n\n')

    # Plotting the histogram
    plt.hist(scores, bins=10, edgecolor='black')  # Adjust the number of bins as needed
    plt.xlabel('Score')
    plt.ylabel('Count')
    plt.title('Distribution of Scores')

    # Display the plot
    plt.show()


if __name__ == '__main__':
    analyze_file('data/test_1', 'data/result_analysis')