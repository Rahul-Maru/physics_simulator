from consts import *

from math import pi, e, sqrt, sin, cos, tan
from vector import Vector
from particle import Particle
from spring import Spring

done = False
pause = False

def main():
	pg.init()

	t = log_t = 0

	spg = Spring(k, Vector(s0.x(), 0), sr, WIDTH)

	# functions for net force and energy
	F = lambda s, v : spg.F(s) + Fg() + Fd(v) # N
	E = lambda s, v: -m*g*s.y() + m*v.mag()**2/2 + spg.energy(s) # J

	a0 = (F(s0, u))/m # m/s²

	# v(dt/2) | setup for the leap-frog integration method
	v05 = u + a0/(2*FPS) # m/s

	p = Particle(m, 0, s0 + v05/FPS, v05, WIDTH/SCALE, 1/11)

	# simulator loop
	while not done:
		handle_events()

		dt = clock.tick_busy_loop(FPS)/1000  # s
		if not pause:
			t += dt # s

			F_net = F(p.s, p.v) # N
			U = p.move(F_net, dt, E) # J

			spg.s = p.s

			if t > log_t + 1:
				log_t += 1
				print(f"{log_t} ||| {p.s} || {p.v} \n {F_net/m} || {U}")

		draw(screen, [spg, p], t)


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


if __name__ == "__main__":
	main()
