import pygame as pg
from vector import Vector

# simulation properties
WINDOW_WIDTH = 500 # pixels
WINDOW_HEIGHT = 500 # pixels
SCALE = 100 # pixel/m  number of pixels per in-universe metre
FPS = 41 # frames/s  maximum framerate of the simulation

clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
bg = pg.image.load("img/stars.png")

# universal properties
G = 6.6743e-11 #  m³/kg·s²

Fg = lambda p1, p2: G*p1.m*p2.m/(p1.s-p2.s).mag()**2 * (p2.s-p1.s).unit() # N  force of gravity

# sun properties
m_s = 4.2e10 # kg  mass of sun
s_s = Vector(2.5, -2.5) # m  sun position

# earth properties
m_e = 10 # kg  mass of earth

# initial conditions
s0_e = Vector(0.6, -2) # m  initial position
u = Vector(0, 1) # m/s  initial velocity

