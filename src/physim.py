from consts import *

from math import pi, e, sqrt, sin, cos, tan
from vector import Vector
from particle import Particle
# from spring import Spring

done = False
pause = False

def main():
	pg.init()

	t = secs = 0

	earth = Particle(m_e, 0, s0_e, u, 0.1, 0.1, (0, 200, 128))
	SUN = Particle(m_s, 0, s_s, 0, 0.7, 0.7, (255, 128, 0), flags="i")

	# function energy
	E = lambda p1, p2: -G*m_e*m_s/(p1.s-p2.s).mag() + p1.m*p1.v.mag()**2/2 # J
	# TODO angular momentum

	a0 = (Fg(earth, SUN))/m_e # m/s²

	# v(dt/2) | setup for the leap-frog integration method

	earth.v += a0/(2*FPS)
	earth.s += earth.v/FPS

	# simulator loop
	while not done:
		handle_events()

		dt = clock.tick_busy_loop(FPS)/1000  # s
		if not pause:
			t += dt # s

			F_net = Fg(earth, SUN) # N
			U = earth.move(F_net, dt, E, SUN) # J

			# log data every second
			if t > secs + 1:
				secs += 1
				print(f"{secs} ||| {earth.s} || {earth.v} \n {F_net/m_e} || {U}")

		draw(screen, [SUN, earth], t)


def draw(screen, objs, t):
	screen.fill((0, 0, 0))

	for obj in objs:
		obj.draw(screen)

	fps = clock.get_fps()

	font = pg.font.SysFont(None, 14)

	ttxt = font.render(f"t = {t:.1f}s", True, (164, 0, 255))
	screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))

	if pause:
		pausetxt = font.render("PAUSED", True, (255, 24, 0))
		screen.blit(pausetxt, (24, 20))
	else:
		fpstxt = font.render(f"{round(fps, 0)} FPS", True, (0, 255, 0) if fps >= FPS else (255, 0, 0))
		screen.blit(fpstxt, (24, 20))

	pg.display.flip()

def handle_events():
	global done
	global pause

	for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					done = True
				if event.key == pg.K_SPACE:
					pause = not pause


if __name__ == "__main__":
	main()
