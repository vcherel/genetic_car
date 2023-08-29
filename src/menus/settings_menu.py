from render.resizing import convert_to_new_window, scale_image  # Import the functions to resize the window
from data.constants import PATH_IMAGE  # To get the path of the image
from render.button import Button  # Import the button class
import data.variables as var  # Import the data
import pygame  # To use pygame


"""
This file contains the Settings class and all the functions related to it. The settings window is used to change many
different settings of the simulation.
"""


class Settings:
    """
    This class is used to create the settings window, used to change the settings of the simulation
    """
    def __init__(self):
        """
        Initialize the settings window the first time
        """
        self.image = None  # Image of the window
        self.rect = None  # Rect of the window
        self.x = self.y = None  # Position of the window

        self.show_clics_button = None  # The button to see the clics

        # General section
        self.fps_button = None  # The button to change the FPS
        self.seed_button = None  # The button to change the seed
        self.camera_button = None  # The button to change the camera

        # Display section
        self.show_cones_button = None  # The button to activate the debug mode
        self.show_explosions_button = None  # The button to see the explosions
        self.show_checkpoints_button = None  # The button to see the checkpoints

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
        self.rect = pygame.rect.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())  # Create the rect of the window

        self.show_clics_button = Button(x=1340, y=650, image_name='checkbox', scale=0.02)  # Hidden button to see the cursor

        # General section
        self.fps_button = Button(x=292, y=221, image_name='writing', variable=var.FPS, name='FPS', scale_x=0.5, text_displayed="Nombre d'images par seconde")
        self.seed_button = Button(x=300, y=267, image_name='writing', variable=var.SEED, name='SEED', scale_x=0.5, text_displayed="Permet de rejouer la même simulation plusieurs fois")
        self.camera_button = Button(x=330, y=311, image_name='writing', variable=var.NUM_CAMERA, name='CAMERA', scale_x=0.5, text_displayed="Changer de caméra")

        # Display section
        self.show_cones_button = Button(x=474, y=455, image_name='checkbox', scale=0.1, text_displayed="Afficher les triangles devant les voitures")
        self.show_explosions_button = Button(x=401, y=524, image_name='checkbox', scale=0.1, text_displayed="Ça sert à rien mais c'est rigolo")
        self.show_explosions_button.activated = var.SHOW_EXPLOSIONS  # We activate the explosions by default
        self.show_checkpoints_button = Button(x=412, y=597, image_name='checkbox', scale=0.1, text_displayed="Afficher les checkpoints")

        # Car section
        self.max_speed_button = Button(x=847, y=222, image_name='writing', variable=var.MAX_SPEED, name='MAX_SPEED', scale_x=0.5, text_displayed="Changer vitesse maximale des voitures")
        self.turn_angle_button = Button(x=864, y=279, image_name='writing', variable=var.TURN_ANGLE, name='TURN_ANGLE', scale_x=0.5, text_displayed="Changer angle de rotation des voitures")
        self.acceleration_button = Button(x=791, y=342, image_name='writing', name='ACCELERATION', variable=var.ACCELERATION, scale_x=0.5, text_displayed="Plus ce paramètre est grand, plus les voitures accélèrent vite")
        self.deceleration_button = Button(x=742, y=402, image_name='writing', name='DECELERATION', variable=var.DECELERATION, scale_x=0.5, text_displayed="Plus ce paramètre est grand, plus les voitures freinent vite")
        self.drift_button = Button(x=777, y=460, image_name='writing', name='DRIFT_FACTOR', variable=var.DRIFT_FACTOR, scale_x=0.5, text_displayed="Plus ce paramètre est grand, plus les voitures dérapent")

        # Genetic section
        self.proportion_button = Button(x=1280, y=222, image_name='writing', variable=var.PROPORTION_CARS_KEPT, name='PROPORTION_CARS_KEPT', scale_x=0.5, text_displayed="Voitures gardées entre deux runs")
        self.crossover_button = Button(x=1240, y=295, image_name='writing', variable=var.CHANCE_CROSSOVER, name='CHANCE_CROSSOVER', scale_x=0.5, text_displayed="Probabilité de crossover")
        self.mutation_button = Button(x=1222, y=369, image_name='writing', variable=var.CHANCE_MUTATION, name='CHANCE_MUTATION', scale_x=0.5, text_displayed="Probabilité de mutation")
        self.time_generation_button = Button(x=1280, y=446, image_name='writing', variable=var.TIME_GENERATION, name='TIME_GENERATION', scale_x=0.5, text_displayed="Durée d'une génération")

        # Cone section
        self.width_cone_button = Button(x=718, y=610, image_name='writing', variable=var.WIDTH_CONE, name='WIDTH_CONE', scale_x=0.5, text_displayed="Largeur des triangles devant les voitures")
        self.length_cone_button = Button(x=1110, y=610, image_name='writing', variable=var.LENGTH_CONE, name='LENGTH_CONE', scale_x=0.5, text_displayed="Longueur des triangles devant les voitures")

        self.writing_buttons = [self.fps_button, self.seed_button, self.camera_button, self.max_speed_button, self.turn_angle_button,
                                self.acceleration_button, self.deceleration_button, self.drift_button, self.proportion_button,
                                self.mutation_button, self.crossover_button, self.time_generation_button,  self.width_cone_button, self.length_cone_button]

    def update_parameters(self):
        """
        Update the texts of the buttons, used when we change map, because the parameters are different for each map
        """
        self.seed_button.update_text(var.SEED)  # Update the text of the seed button
        self.max_speed_button.update_text(var.MAX_SPEED)  # Update the text of the max speed button
        self.turn_angle_button.update_text(var.TURN_ANGLE)  # Update the text of the turn angle button
        self.acceleration_button.update_text(var.ACCELERATION)  # Update the text of the acceleration button
        self.deceleration_button.update_text(var.DECELERATION)  # Update the text of the deceleration button
        self.drift_button.update_text(var.DRIFT_FACTOR)  # Update the text of the drift button
        self.crossover_button.update_text(var.CHANCE_CROSSOVER)  # Update the text of the crossover button
        self.mutation_button.update_text(var.CHANCE_MUTATION)  # Update the text of the mutation button
        self.proportion_button.update_text(var.PROPORTION_CARS_KEPT)  # Update the text of the proportion button
        self.time_generation_button.update_text(var.TIME_GENERATION)  # Update the text of the time per generation button
        self.width_cone_button.update_text(var.WIDTH_CONE)  # Update the text of the width cone button
        self.length_cone_button.update_text(var.LENGTH_CONE)  # Update the text of the length cone button

    def draw(self):
        """
        Display the settings window
        """
        var.WINDOW.blit(self.image, (self.x, self.y))  # Display the settings window

        # To make the buttons work, you have to add code in the handle_key_press function of the ui.py file
        for button in self.writing_buttons:
            button.draw()  # Draw the buttons
            if button.just_clicked:
                button.text = ''

        var.SHOW_DETECTION_CONES = self.show_cones_button.draw()  # Check the state of the button
        var.SHOW_CLICS_INFO = self.show_clics_button.draw()  # Check the state of the button
        var.SHOW_EXPLOSIONS = self.show_explosions_button.draw()  # Check the state of the button
        var.SHOW_CHECKPOINTS = self.show_checkpoints_button.draw()  # Check the state of the button
        if self.show_checkpoints_button.just_clicked and not var.SHOW_CHECKPOINTS:
            var.WINDOW.blit(var.BACKGROUND, (0, 0))  # Erase the checkpoints when we don't show them anymore

    def erase(self):
        """
        Erase the settings window
        """
        var.WINDOW.blit(var.BACKGROUND, self.rect, self.rect)


SETTINGS = Settings()  # Settings of the game