import pygame as pg
from vector import Vector

# simulation properties
WINDOW_WIDTH = 500 # pixels
WINDOW_HEIGHT = 500 # pixels
SCALE = 100 # pixel/m  number of pixels per in-universe metre
FPS = 41 # frames/s  maximum framerate of the simulation

clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# universal properties
g = -9.8 # m/s²  gravitational constant
b = 0 # Ns/m  damping constant

Fg = lambda : Vector(0, g*m) # N  force of gravity
Fd = lambda v : -v*b # N  damping force

# spring properties
WIDTH = SCALE # m  width of spring
MID = (WINDOW_WIDTH-WIDTH)/(2*SCALE) # m  midpoint of spring
k = 8 # N/m  spring constant
sr = Vector(MID, -2) # m  rest point of spring

# particle properties
m = 0.6 # kg  mass of particle

# initial conditions
s0 = Vector(MID, -1) # m  initial position
u = Vector(0, 0) # m/s  initial velocity

