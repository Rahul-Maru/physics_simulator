import pygame as pg
from vector import Vector

# simulation properties
WINDOW_WIDTH = 600 # pixels
WINDOW_HEIGHT = 600 # pixels
RES = 150 # pixel/unit length
FPS = 60 # frames/IRL s (In-Real-Life seconds)  maximum framerate of the simulation
DAY = 86400 # s/day  unit to display time counter
LOG_S = 1 # IRL s  how frequently to log the system state

# colors
RED = (255, 24, 0)
GREEN = (0, 255, 0)
LIME = (128, 255, 0)
MAGENTA = (164, 0, 255)

D_YELLOW = (120, 100, 80)
D_GRAY = (60, 60, 60)

# unit scale factors
L_SCALE = 149597870700 # m/unit length || 1 AU
T_SCALE = 86400*50 # s/unit time || n Days
M_SCALE = 1 # kg/unit mass || 1 kg

# universal properties
G = 6.6743e-11*T_SCALE**2/L_SCALE**3 #  [M]¯¹[L]³[T]¯²
Fg = lambda p1, p2: G*p1.m*p2.m/(p1.s-p2.s).mag()**2 * (p2.s-p1.s).unit() # [M][L]²[T]¯² force of gravity
# TODO Fc (coulomb's law)

# sun properties
SIZE_S = (0.56, 0.56)
m_s = 1.9891e30 # [M]  mass of sun
s_s = Vector(WINDOW_WIDTH/(2*RES), -WINDOW_HEIGHT/(2*RES)) # [L]  sun position

# earth properties
SIZE_E = (0.12, 0.12)
m_e = 5.97219e24 # [M]  mass of earth

# initial conditions
s0_e = Vector(s_s.x() - 1, s_s.y()) # [L]  initial position of earth
u = Vector(0, 29722*T_SCALE/L_SCALE) # [L][T]¯1  inital velocity of earth


# pygame setup
clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
bg = pg.image.load("img/stars.png")
