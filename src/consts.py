import pygame as pg
from math import log10, pi as π

from vector import Vector, v0
from matrix import Matrix


# —simulation properties—
# simulator dimensions
WINDOW_WIDTH = 700 # pixels
WINDOW_HEIGHT = 700 # pixels
MID = Vector(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2) # pixels

RES = 150 # pixel/unit length
RES_MAT = Matrix(Vector(RES, 0), Vector(0, -RES))
FPS = 500 # frames/IRL s (In-Real-Life seconds)  maximum framerate of the simulation
DAY = 86400 # s/day  unit to display time counter
LOG_S = 0.2 # IRL s  how frequently to log the system state

# unit vectors
I = Vector(1, 0)
J = Vector(0, 1)

# unit scale factors
L_SCALE = 149597870700 # m/unit length || 1 AU
T_SCALE = 86400*50 # s/unit time || n Days w. n=50
M_SCALE = 1 # kg/unit mass || 1 kg
A_SCALE = 2.3148148e-7 # A/unit current || 1 C/n days

# —universal properties—
# Newton's Gravitational Constant
G = 6.6743e-11 * T_SCALE**2 / L_SCALE**3 # [M]¯¹[L]³[T]¯²
# Permittivity of free space / Epsilon naught
ε0 = 8.8541878128e-12 * L_SCALE**3 / T_SCALE**4 / A_SCALE**2 # [M]¯¹[L]¯³[T]⁴[A]²
K = 1/(4*π*ε0) # [M][L]³[T]¯⁴[A]¯²  Coulomb's constant

# force of gravity
Fg = lambda p1, p2: G * p1.m * p2.m / (p1.s-p2.s)**2 * (p2.s-p1.s).unit() # [M][L][T]¯²
# electrostatic force
Fc = lambda p1, p2: K * p1.q * p2.q / (p1.s-p2.s)**2 * (p2.s-p1.s).unit() # [M][L][T]¯²
FORCE = lambda p1, p2: Fg(p1, p2) + Fc(p1, p2) # [M][L][T]¯² net force

# energy functions  [M][L]²[T]¯²
GPE = lambda p1, p2: -G * p1.m * p2.m / (p1.s-p2.s) # gravitational potential energy
EPE = lambda p1, p2: -K * p1.q * p2.q / (p1.s-p2.s) # electrostatic potential energy
PE = lambda p1, p2: GPE(p1, p2) + EPE(p1, p2) # total potential energy
KE = lambda p: p.m * p.v**2 / 2 # kinetic energy

# —body properties—
# sun properties
SIZE_S = (0.56, 0.56) # [L]
m_s = 1.9891e30 # [M]  mass of sun
SUN_IMG = "img/sun.png"

# earth properties
SIZE_E = (0.12, 0.12) # [L]
m_e = 5.97219e29 # [M]  mass of earth
EARTH_IMG = "img/earth.png"

# —initial conditions—
s0_s = v0(2) # [L]  sun position
s0_e = Vector(s0_s.x() - 1, s0_s.y()) # [L]  initial position of earth

u_s = v0(2) # [L][T]¯1  inital velocity of sun
u_e = Vector(0, 29722 * T_SCALE / L_SCALE) # [L][T]¯1  inital velocity of earth


# —pygame setup—
clock = pg.time.Clock()
screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
bg = pg.transform.scale(pg.image.load("img/stars.png"), (WINDOW_WIDTH, WINDOW_HEIGHT)).convert_alpha()
