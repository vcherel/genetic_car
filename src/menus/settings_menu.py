from src.other.utils import scale_image, convert_to_new_window  # To convert the position if we resize the window
from src.data.constants import PATH_IMAGE  # To get the path of the image
from src.render.button import Button  # Import the button class
import src.data.variables as var  # Import the data
import pygame  # To use pygame


class Settings:
    """
    This class is used to create the settings window, used to change the settings of the simulation
    """
    def __init__(self):
        """
        Initialize the settings window the first time
        """
        self.rect = None  # Rectangle of the window
        self.image = None  # Image of the window
        self.x = self.y = None  # Position of the window

        self.see_cursor_button = None  # The button to see the clics

        # General section
        self.fps_button = None  # The button to change the FPS
        self.seed_button = None  # The button to change the seed

        # Display section
        self.see_cones_button = None  # The button to activate the debug mode
        self.see_explosions_button = None  # The button to see the explosions
        self.see_checkpoints_button = None  # The button to see the checkpoints

        # Car section
        self.max_speed_button = None  # The button to change the max speed of the car
        self.turn_angle_button = None  # The button to change the turn angle of the car
        self.acceleration_button = None  # The button to change the acceleration of the car
        self.deceleration_button = None  # The button to change the deceleration of the car
        self.drift_button = None  # The button to change the drift of the car

        # Genetic section
        self.crossover_button = None  # The button to change the crossover chance
        self.mutation_button = None  # The button to change the mutation chance
        self.proportion_button = None  # The button to change the proportion of cars kept per generation
        self.time_generation_button = None  # The button to change the time per generation

        # Cone section
        self.width_cone_button = None  # The button to change the width of the cones
        self.length_cone_button = None  # The button to change the length of the cones

        self.writing_buttons = []   # List of all the buttons with writing buttons


    def init(self):
        """
        Initialize the settings window
        """
        self.x, self.y = convert_to_new_window((175, 125))  # Position of the window
        self.image = scale_image(pygame.image.load(PATH_IMAGE + '/settings_menu.png'))  # Load the image of the window
        self.rect = self.image.get_rect()  # Get the rectangle of the image
        self.rect.x, self.rect.y = self.x, self.y  # Set the position of the rectangle

        self.see_cursor_button = Button(1340, 650, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.02)

        # General section
        self.fps_button = Button(292, 221, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                 pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                 pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                 variable=var.FPS, variable_name='FPS', text=str(var.FPS), scale_x=0.5)
        self.seed_button = Button(290, 288, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                  pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                  pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                  variable=var.SEED, variable_name='SEED', text=str(var.SEED), scale_x=0.5)

        # Display section
        self.see_cones_button = Button(474, 455, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                       pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                       pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.1)
        self.see_explosions_button = Button(402, 530, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                            pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                            pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True, scale=0.1)
        self.see_checkpoints_button = Button(412, 597, pygame.image.load(PATH_IMAGE + '/checkbox_1.png'),
                                             pygame.image.load(PATH_IMAGE + '/checkbox_2.png'),
                                             pygame.image.load(PATH_IMAGE + '/checkbox_3.png'), checkbox=True,
                                             scale=0.1)  # The button to see the checkpoints

        # Car section
        self.max_speed_button = Button(847, 223, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                       variable=var.MAX_SPEED, variable_name='MAX_SPEED', text=str(var.MAX_SPEED), scale_x=0.5)

        self.turn_angle_button = Button(864, 278, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                        variable=var.TURN_ANGLE, variable_name='TURN_ANGLE',
                                        text=str(var.TURN_ANGLE), scale_x=0.5)
        self.acceleration_button = Button(791, 343, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'),
                                          writing_button=True, variable_name='ACCELERATION', variable=var.ACCELERATION,
                                          text=str(var.ACCELERATION), scale_x=0.5)
        self.deceleration_button = Button(742, 402, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                          pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'),
                                          writing_button=True, variable_name='DECELERATION', variable=var.DECELERATION,
                                          text=str(var.DECELERATION), scale_x=0.5)
        self.drift_button = Button(777, 461, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                   pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                   pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'),
                                   writing_button=True, variable_name='DRIFT_FACTOR', variable=var.DRIFT_FACTOR,
                                   text=str(var.DRIFT_FACTOR), scale_x=0.5)

        # Genetic section
        self.crossover_button = Button(1229, 221, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                       pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                       variable=var.CHANCE_CROSSOVER, variable_name='CHANCE_CROSSOVER',
                                       text=str(var.CHANCE_CROSSOVER), scale_x=0.5)
        self.mutation_button = Button(1222, 298, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                      pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                      pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                      variable=var.CHANCE_MUTATION, variable_name='CHANCE_MUTATION',
                                      text=str(var.CHANCE_MUTATION), scale_x=0.5)
        self.proportion_button = Button(1280, 370, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                        variable=var.PROPORTION_CARS_KEPT, variable_name='PROPORTION_CARS_KEPT',
                                        text=str(var.PROPORTION_CARS_KEPT), scale_x=0.5)
        self.time_generation_button = Button(1260, 446, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                             pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                             pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                             variable=var.TIME_GENERATION, variable_name='TIME_GENERATION',
                                             text=str(var.TIME_GENERATION), scale_x=0.5)

        # Cone section
        self.width_cone_button = Button(718, 610, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                        pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'), writing_button=True,
                                        variable=var.WIDTH_CONE, variable_name='SEED', text=str(var.WIDTH_CONE), scale_x=0.5)
        self.length_cone_button = Button(1110, 610, pygame.image.load(PATH_IMAGE + '/writing_rectangle_1.png'),
                                         pygame.image.load(PATH_IMAGE + '/writing_rectangle_2.png'),
                                         pygame.image.load(PATH_IMAGE + '/writing_rectangle_3.png'),
                                         writing_button=True, variable=var.LENGTH_CONE, variable_name='LENGTH_CONE',
                                         text=str(var.LENGTH_CONE), scale_x=0.5)

        self.writing_buttons = [self.fps_button, self.time_generation_button, self.max_speed_button, self.turn_angle_button,
                                self.acceleration_button, self.deceleration_button, self.mutation_button, self.crossover_button,
                                self.proportion_button, self.seed_button, self.width_cone_button, self.length_cone_button,
                                self.drift_button]

    def show(self):
        """
        Display the settings window
        """
        var.WINDOW.blit(self.image, (self.x, self.y))  # Display the settings window

        # To make the buttons work, you have to add code in the handle_key_press function of the ui.py file
        for button in self.writing_buttons:
            button.draw()  # Draw the buttons
            if button.just_clicked:
                button.text = ''

        var.DEBUG = self.see_cones_button.draw()  # Check the state of the button
        var.SEE_CURSOR = self.see_cursor_button.draw()  # Check the state of the button
        var.SEE_CHECKPOINTS = self.see_checkpoints_button.draw()  # Check the state of the button
        if self.see_checkpoints_button.just_clicked and not var.SEE_CHECKPOINTS:
            var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Erase the checkpoints
        var.SEE_EXPLOSIONS = self.see_explosions_button.draw()  # Check the state of the button

    def erase(self):
        """
        Erase the settings window
        """
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)


SETTINGS = Settings()  # Create the settings window
