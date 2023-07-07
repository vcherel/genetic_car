from src.other.utils import convert_to_new_window  # To convert the position if we resize the window
from src.other.constants import PATH_IMAGE  # To get the path of the image
from src.render.button import Button  # Import the button class
import src.other.variables as var  # Import the variables
import pygame  # To use pygame


def fill_y_lists():
    """
    Fill the y_list with the y position of the texts / buttons

    Returns:
        list, list: The y positions of the texts / buttons for each column
    """
    y_1 = []
    big_space, small_space = 80, 55  # The space between the texts
    y = 150  # The y position of the first text
    y_1.append(y)
    y += small_space
    y_1.append(y)
    y += small_space
    y_1.append(y)
    y += small_space
    y_1.append(y)
    y += big_space

    y_1.append(y)
    y += small_space
    y_1.append(y)
    y += small_space
    y_1.append(y)
    y += small_space
    y_1.append(y)
    y += small_space
    y_1.append(y)

    y_2 = []
    big_space, small_space = 50, 48
    y = 145
    y_2.append(y)
    y += small_space
    y_2.append(y)
    y += small_space
    y_2.append(y)
    y += small_space
    y_2.append(y)
    y += big_space

    y_2.append(y)
    y += small_space
    y_2.append(y)
    y += small_space
    y_2.append(y)
    y += small_space
    y_2.append(y)
    y += big_space

    y_2.append(y)
    y += small_space
    y_2.append(y)
    y += small_space
    y_2.append(y)

    return y_1, y_2


x1, x2 = 460, 760  # The y position of the first and the last text
temp = fill_y_lists()
y1, y2 = temp[0], temp[1]  # The y positions of the texts / buttons for each column

general_text = var.LARGE_FONT.render('Général', True, (0, 0, 0), (128, 128, 128))  # Text of the window
fps_text = var.FONT.render('FPS :', True, (0, 0, 0), (128, 128, 128))  # Text of the button to change the FPS
debug_text = var.FONT.render('Debug :', True, (0, 0, 0), (128, 128, 128))  # Text of the debug button
timer_text = var.FONT.render('Temps :', True, (0, 0, 0), (128, 128, 128))  # Text of the timer button

genetic_text = var.LARGE_FONT.render('Génétique', True, (0, 0, 0), (128, 128, 128))  # Text of the window
mutation_text = var.FONT.render('Chance mutation :', True, (0, 0, 0), (128, 128, 128))  # Text of the mutation button
crossover_text = var.FONT.render('Chance crossover :', True, (0, 0, 0), (128, 128, 128))  # Text of the crossover button
proportion_text = var.FONT.render('Proportion conservée :', True, (0, 0, 0), (128, 128, 128))  # Text of the percentage car button

car_text = var.LARGE_FONT.render('Voitures', True, (0, 0, 0), (128, 128, 128))  # Text of the window
max_speed_text = var.FONT.render('Vitesse max :', True, (0, 0, 0), (128, 128, 128))  # Text of the max speed button
turn_angle_text = var.FONT.render('Angle de rotation :', True, (0, 0, 0), (128, 128, 128))  # Text of the turn angle button
acceleration_text = var.FONT.render('Accélération :', True, (0, 0, 0), (128, 128, 128))  # Text of the acceleration button
deceleration_text = var.FONT.render('Freinage :', True, (0, 0, 0), (128, 128, 128))  # Text of the deceleration button

other_text = var.LARGE_FONT.render('Autre', True, (0, 0, 0), (128, 128, 128))  # Text of the window
seed_text = var.FONT.render('Seed :', True, (0, 0, 0), (128, 128, 128))  # Text of the seed button
see_cursor_text = var.FONT.render('Voir les clics :', True, (0, 0, 0), (128, 128, 128))  # Text of the see clics button
see_checkpoints_text = var.FONT.render('Voir les checkpoints :', True, (0, 0, 0), (128, 128, 128))  # Text of the see checkpoints button

cone_text = var.LARGE_FONT.render('Cônes', True, (0, 0, 0), (128, 128, 128))  # Text of the window
width_cone_text = var.FONT.render('Largeur :', True, (0, 0, 0), (128, 128, 128))  # Text of the width cone button
length_cone_text = var.FONT.render('Hauteur :', True, (0, 0, 0), (128, 128, 128))  # Text of the length cone button


class Settings:
    """
    This class is used to create the settings window, used to change the settings of the simulation
    """
    def __init__(self):
        """
        Initialize the settings window the first time
        """
        self.rect = None  # Rectangle of the window

        # General section
        self.fps_button = None  # The button to change the FPS
        self.debug_button = None  # The button to activate the debug mode
        self.timer_button = None  # The button to change the time per generation

        # Car section
        self.max_speed_button = None  # The button to change the max speed of the car
        self.turn_angle_button = None  # The button to change the turn angle of the car
        self.acceleration_button = None  # The button to change the acceleration of the car
        self.deceleration_button = None  # The button to change the deceleration of the car

        # Genetic section
        self.mutation_button = None  # The button to change the mutation chance
        self.crossover_button = None  # The button to change the crossover chance
        self.proportion_button = None  # The button to change the proportion of cars kept per generation

        # Other section
        self.seed_button = None  # The button to change the seed
        self.see_cursor_button = None  # The button to see the clics
        self.see_checkpoints_button = None  # The button to see the checkpoints

        # Cone section
        self.width_cone_button = None  # The button to change the width of the cones
        self.length_cone_button = None  # The button to change the length of the cones

        self.writing_buttons = []   # List of all the buttons with writing buttons


    def init(self):
        """
        Initialize the settings window
        """
        self.rect = pygame.Rect(convert_to_new_window((428, 125, 650, 557)))  # Create the rectangle for the window

        # General section
        self.fps_button = Button(x1 + 145, y1[1] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                 pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                 pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                 variable=var.FPS, text=str(var.FPS), scale_x=0.5, scale_y=1)
        self.debug_button = Button(x1 + 153, y1[2] - 8, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                   pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                   pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.1)
        self.timer_button = Button(x1 + 145, y1[3] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                   pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                   pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                   variable=var.TIME_GENERATION, text=str(var.TIME_GENERATION), scale_x=0.5, scale_y=1)

        # Car section
        self.max_speed_button = Button(x1 + 185, y1[5] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                       variable=var.MAX_SPEED, text=str(var.MAX_SPEED), scale_x=0.5, scale_y=1)
        self.turn_angle_button = Button(x1 + 185, y1[6] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                        variable=var.TURN_ANGLE, text=str(var.TURN_ANGLE), scale_x=0.5, scale_y=1)
        self.acceleration_button = Button(x1 + 185, y1[7] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'),
                                          writing_button=True, variable=var.ACCELERATION,
                                          text=str(var.ACCELERATION), scale_x=0.5, scale_y=1)
        self.deceleration_button = Button(x1 + 185, y1[8] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'),
                                          writing_button=True, variable=var.DECELERATION,
                                          text=str(var.DECELERATION), scale_x=0.5, scale_y=1)

        # Genetic section
        self.mutation_button = Button(x2 + 225, y2[1] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                      pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                      pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                      variable=var.MUTATION_CHANCE, text=str(var.MUTATION_CHANCE), scale_x=0.5,
                                      scale_y=1)
        self.crossover_button = Button(x2 + 225, y2[2] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                       variable=var.CROSSOVER_CHANCE, text=str(var.CROSSOVER_CHANCE), scale_x=0.5,
                                       scale_y=1)
        self.proportion_button = Button(x2 + 225, y2[3] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                        variable=var.PROPORTION_CARS_KEPT, text=str(var.PROPORTION_CARS_KEPT), scale_x=0.5, scale_y=1)

        # Other section
        self.seed_button = Button(x2 + 210, y2[5] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                  pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                  pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                  variable=var.SEED, text=str(var.SEED), scale_x=0.5, scale_y=1)
        self.see_cursor_button = Button(x2 + 218, y2[6] - 8, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.1)
        self.see_checkpoints_button = Button(x2 + 218, y2[7] - 8, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                             pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                             pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True,
                                             scale=0.1)

        # Cone section
        self.width_cone_button = Button(x2 + 160, y2[9] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                        variable=var.WIDTH_CONE, text=str(var.WIDTH_CONE), scale_x=0.5, scale_y=1)
        self.length_cone_button = Button(x2 + 160, y2[10] - 3, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                         pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                         pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                         variable=var.LENGTH_CONE, text=str(var.LENGTH_CONE), scale_x=0.5, scale_y=1)

        self.writing_buttons = [self.fps_button, self.timer_button, self.max_speed_button, self.turn_angle_button,
                                self.acceleration_button, self.deceleration_button, self.mutation_button, self.crossover_button,
                                self.proportion_button, self.seed_button, self.width_cone_button, self.length_cone_button]

    def show(self):
        """
        Display the settings window
        """
        pygame.draw.rect(var.WINDOW, (128, 128, 128), self.rect, 0)  # Draw the rectangle (inside)
        pygame.draw.rect(var.WINDOW, (1, 1, 1), self.rect, 2)  # Draw the rectangle (contour)

        show_texts()  # Show the texts

        # To make the buttons work, you have to add code in the handle_key_press function of the ui.py file
        for button in self.writing_buttons:
            button.draw()  # Draw the buttons
            if button.just_clicked:
                button.text = ''

        var.DEBUG = self.debug_button.draw()  # Check the state of the button
        var.SEE_CURSOR = self.see_cursor_button.draw()  # Check the state of the button
        var.SEE_CHECKPOINTS = self.see_checkpoints_button.draw()  # Check the state of the button
        if self.see_checkpoints_button.just_clicked and not var.SEE_CHECKPOINTS:
            var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Erase the checkpoints

        # Draw the rectangle around each section
        pygame.draw.rect(var.WINDOW, (1, 1, 1), pygame.rect.Rect(convert_to_new_window((450, 140, 274, 236))), 2)  # General section
        pygame.draw.rect(var.WINDOW, (1, 1, 1), pygame.rect.Rect(convert_to_new_window((450, 388, 274, 278))), 2)  # Car section
        pygame.draw.rect(var.WINDOW, (1, 1, 1), pygame.rect.Rect(convert_to_new_window((740, 140, 316, 186))), 2)  # Genetic section
        pygame.draw.rect(var.WINDOW, (1, 1, 1), pygame.rect.Rect(convert_to_new_window((740, 337, 316, 185))), 2)  # Other section
        pygame.draw.rect(var.WINDOW, (1, 1, 1), pygame.rect.Rect(convert_to_new_window((758, 530, 280, 140))), 2)  # Cone section

    def erase(self):
        """
        Erase the settings window
        """
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)


def show_texts():
    var.WINDOW.blit(general_text, convert_to_new_window((x1 + 75, y1[0])))
    var.WINDOW.blit(fps_text, convert_to_new_window((x1 + 45, y1[1])))
    var.WINDOW.blit(debug_text, convert_to_new_window((x1 + 45, y1[2])))
    var.WINDOW.blit(timer_text, convert_to_new_window((x1 + 45, y1[3])))

    var.WINDOW.blit(car_text, convert_to_new_window((x1 + 60, y1[4])))
    var.WINDOW.blit(max_speed_text, convert_to_new_window((x1 + 10, y1[5])))
    var.WINDOW.blit(turn_angle_text, convert_to_new_window((x1 + 10, y1[6])))
    var.WINDOW.blit(acceleration_text, convert_to_new_window((x1 + 10, y1[7])))
    var.WINDOW.blit(deceleration_text, convert_to_new_window((x1 + 10, y1[8])))

    var.WINDOW.blit(genetic_text, convert_to_new_window((x2 + 50, y2[0])))
    var.WINDOW.blit(mutation_text, convert_to_new_window((x2, y2[1])))
    var.WINDOW.blit(crossover_text, convert_to_new_window((x2, y2[2])))
    var.WINDOW.blit(proportion_text, convert_to_new_window((x2, y2[3])))

    var.WINDOW.blit(other_text, convert_to_new_window((x2 + 85, y2[4])))
    var.WINDOW.blit(seed_text, convert_to_new_window((x2 + 10, y2[5])))
    var.WINDOW.blit(see_cursor_text, convert_to_new_window((x2 + 10, y2[6])))
    var.WINDOW.blit(see_checkpoints_text, convert_to_new_window((x2 + 10, y2[7])))

    var.WINDOW.blit(cone_text, convert_to_new_window((x2 + 85, y2[8])))
    var.WINDOW.blit(width_cone_text, convert_to_new_window((x2 + 50, y2[9])))
    var.WINDOW.blit(length_cone_text, convert_to_new_window((x2 + 50, y2[10])))


SETTINGS = Settings()  # Create the settings window
