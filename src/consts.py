import pygame as pg
from vector import Vector

# simulation properties
WINDOW_WIDTH = 500 # pixels
WINDOW_HEIGHT = 500 # pixels
SCALE = 150 # pixel/AU  number of pixels per in-universe metre
FPS = 82 # frames/ IRL s  maximum framerate of the simulation

clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
bg = pg.image.load("img/stars.png")

# universal properties
G = 1.489273e-30 #  au³/kg·Hday² (hecto-day)

Fg = lambda p1, p2: G*p1.m*p2.m/(p1.s-p2.s).mag()**2 * (p2.s-p1.s).unit() # kg·au²/Hday²  force of gravity

# sun properties
SIZE_S = (0.56, 0.56)
m_s = 1.9891e30 # kg  mass of sun
s_s = Vector(1.6667, -1.6667) # AU  sun position

# earth properties
SIZE_E = (0.1, 0.1)
m_e = 5.97219e24 # kg  mass of earth

# initial conditions
s0_e = Vector(0.6667, -1.6667) # AU  initial position
u = Vector(0, 1.719) # AU/Hday  initial velocity

