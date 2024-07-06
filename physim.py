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
FRAMERATE = 60 # frames/s

spring = pg.image.load("spring.png") # source: khanacademy

g = -9.8 # m/s^2  gravity on earth
k = 3 # N/m  spring constant
b = 0.1 # Ns/m
m = 0.4 # kg
yr = -2 # m
WIDTH = LEN_SCALE


Fs = lambda s : Vector(0, -k*(s.comps[1]-yr))
Fd = lambda v : -v*b
Fg = lambda : Vector(0, g*m)

def main():
	pg.init()  
	screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
	clock = pg.time.Clock()
	done = False

	s0 = Vector((WINDOW_WIDTH-WIDTH)/(2*LEN_SCALE), -0.5)
	u = Vector(0, 0)

	t = 0
	update_t = 0
	s = s0
	a = (Fs(s0) + Fg())/m
	# v(1/2 * dt) | setup for the leap-frog integration method
	v = u + a * 1/(2*FRAMERATE)
	  
	while not done:
		dt = clock.tick_busy_loop(FRAMERATE)/1000  # s
		t += dt # s

		s += v*dt

		F = Fs(s) + Fg() + Fd(v)
		a = F/m

		v = v + a*dt

		if t-1 > update_t:
			update_t += 1
			print(f"{update_t} ||| {s} || {v} || {a}")


		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
		
		screen.fill((0, 0, 0))

		screen.blit(pg.transform.scale(spring, (LEN_SCALE, max(-s.comps[1]*LEN_SCALE, 0))), (s0.comps[0]*LEN_SCALE, 0))

		pg.draw.rect(screen, (128, 255, 0), pg.Rect(s0.comps[0]*LEN_SCALE, -s.comps[1]*LEN_SCALE, WIDTH, LEN_SCALE/9))
		pg.draw.line(screen, (255, 80, 0), (2.01*LEN_SCALE, -s.comps[1]*LEN_SCALE), (2.99*LEN_SCALE, - s.comps[1]*LEN_SCALE), 2)
		pg.draw.line(screen, (200, 200, 200), (1.5*LEN_SCALE, -yr*LEN_SCALE), (3.5*LEN_SCALE, - yr*LEN_SCALE))

		fps = clock.get_fps()
		font = pg.font.SysFont(None, 14)
		fpstxt = font.render(f"{round(fps, 0)} FPS", True, (0, 255, 0) if fps >= FRAMERATE else (255, 0, 0))
		ttxt = font.render(f"t = {t:.1f}s", True, (164, 0, 255))

		screen.blit(fpstxt, (24, 20))
		screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))
		

		pg.display.flip()


if __name__ == "__main__":
	main()