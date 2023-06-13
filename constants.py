import time  # To get the time

# Game
START_POSITIONS = [(600, 165)]  # Start position
START_TIME = time.time()  # Start time of the game
RADIUS_CHECKPOINT = 80  # Radius of the checkpoint

# Game
FPS = 60  # Frame per second
SEED = 1  # Seed of the random (None to not use a seed)
WINDOW_SIZE = WIDTH_SCREEN, HEIGHT_SCREEN = 1500, 700  # Screen size (small to avoid lag)

# Debug
DONT_USE_CAMERA = False  # True to not use the camera, False to use the camera
KEYBOARD_CONTROL = False  # True to control the car with the keyboard
SEE_CURSOR = False  # True to see the cursor position and color when clicking

# Car
CAR_SIZES = [0.15]

MAX_SPEED = 8  # Maximum speed of the car
MIN_SPEED = 1  # Minimum speed of the car
TURN_ANGLE = 5  # Angle of rotation of the car

ACCELERATION = 0.2  # Acceleration of the car
DECELERATION = -1  # Deceleration of the car

# To know what is the speed of the car :
"""
Low speed: speed < MIN_MEDIUM_SPEED
Medium speed: MIN_MEDIUM_SPEED < speed < MIN_HIGH_SPEED
High speed: MIN_HIGH_SPEED < speed
"""
MIN_MEDIUM_SPEED = MAX_SPEED / 3
MIN_HIGH_SPEED = MAX_SPEED / 3 * 2

# Cone
WIDTH_MULTIPLIER = 16  # Width multiplier of the cone
HEIGHT_MULTIPLIER = 19  # Height multiplier of the cone

# Genetic algorithm
MUTATION_CHANCE = 0.2  # Chance of mutation
CROSSOVER_CHANCE = 0.2  # Chance of crossover

TIME_GENERATION = 30  # Time of a generation (s)
