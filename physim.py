import vpython as vp
import numpy as np

from matplotlib import pyplot as plt
import math
from math import pi, e, sqrt, sin, cos, tan
import pygame as pg
from vector import Vector
from particle import Particle

WINDOW_WIDTH = 500 # pixels
WINDOW_HEIGHT = 500 # pixels
LEN_SCALE = 100 # pixel/m
FPS = 41 # frames/s

clock = pg.time.Clock()

spring = pg.image.load("spring.png") # source: khanacademy

g = -9.8 # m/s^2  gravitational constant
k = 8 # N/m  spring constant
b = 0 # Ns/m
m = 0.6 # kg
yr = -2 # m
WIDTH = LEN_SCALE # m  width of spring

Fs = lambda s : Vector(0, -k*(s.y()-yr))
Fd = lambda v : -v*b
Fg = lambda : Vector(0, g*m)

s0 = Vector((WINDOW_WIDTH-WIDTH)/(2*LEN_SCALE), -1) # m
a0 = (Fs(s0) + Fg())/m # m/2^2
u = Vector(0, 0) # m/s


def main():
	pg.init()  
	screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	done = False

	# v(dt/2) | setup for the leap-frog integration method
	v05 = u + a0/(2*FPS) # m/s

	p = Particle(m, 0, s0 + v05/FPS, v05)

	t = 0
	update_t = 0
	  
	while not done:
		dt = clock.tick_busy_loop(FPS)/1000  # s
		t += dt # s

		F = Fs(p.s) + Fg() + Fd(p.v) # N
		U = p.move(F, dt, lambda s, v: -m*g*s.y() + (m*v.mag()**2 + k*(s.y() - yr)**2)/2) # J

		if t-1 > update_t:
			update_t += 1
			print(f"{update_t} ||| {p.s.y()} || {p.v.y()} || {F.y()/m} || {U}")


		done = handle_events()

		draw(screen, [p], t)
		
def handle_events():
	for event in pg.event.get():
			if event.type == pg.QUIT:
				return True
	return False

def draw(screen, ps, t):
	screen.fill((0, 0, 0))


	for p in ps:
		screen.blit(pg.transform.scale(spring, (LEN_SCALE, max(-p.s.comps[1]*LEN_SCALE, 0))), (s0.comps[0]*LEN_SCALE, 0))
		pg.draw.rect(screen, (128, 255, 0), pg.Rect(s0.comps[0]*LEN_SCALE, -p.s.comps[1]*LEN_SCALE, WIDTH, LEN_SCALE/9))
		pg.draw.line(screen, (255, 80, 0), (2.01*LEN_SCALE, -p.s.comps[1]*LEN_SCALE), (2.99*LEN_SCALE, - p.s.comps[1]*LEN_SCALE), 2)

	pg.draw.line(screen, (200, 200, 200), (1.5*LEN_SCALE, -yr*LEN_SCALE), (3.5*LEN_SCALE, - yr*LEN_SCALE))

	fps = clock.get_fps()
	font = pg.font.SysFont(None, 14)
	fpstxt = font.render(f"{round(fps, 0)} FPS", True, (0, 255, 0) if fps >= FPS else (255, 0, 0))
	ttxt = font.render(f"t = {t:.1f}s", True, (164, 0, 255))

	screen.blit(fpstxt, (24, 20))
	screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))


	pg.display.flip()

if __name__ == "__main__":
	main()
