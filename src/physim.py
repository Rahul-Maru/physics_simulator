from consts import *

from math import pi, e, sqrt, sin, cos, tan
from particle import Particle

done = False
paused = False

def main():
	pg.init()

	t = 0 # Hday (hecto day)
	secs = -1 # IRL s (real life seconds)

	SUN = Particle(m_s, 0, s_s, 0, SIZE_S, (255, 128, 0), "img/sun.png", flags="i")
	earth = Particle(m_e, 0, s0_e, u, SIZE_E, (0, 200, 128), "img/earth.png")

	# function energy
	E = lambda p1, p2: -G*m_e*m_s/(p1.s-p2.s).mag() + p1.m*p1.v.mag()**2/2 # kg·AU²/Hday²

	a0 = (Fg(earth, SUN))/m_e # AU/Hday²

	# v(dt/2) | setup for the leap-frog integration method
	earth.v += a0/(2*FPS)
	earth.s += earth.v/FPS

	# simulator loop
	while not done:
		handle_events()

		dt = clock.tick_busy_loop(FPS)/1000  # IRL s
		if not paused:
			t += dt

			F_net = Fg(earth, SUN)
			U = earth.move(F_net, dt, E, SUN)
			L = earth.m*earth.v*(earth.s-SUN.s).mag() # kg·AU²/Hday

			# logs data
			if t > secs + 1:
				secs += 1
				print(f"t {secs*100:.1f} ||| s {earth.s} || v {earth.v} \n a {F_net/m_e} || U {U} || L {L.mag()}")

		draw(screen, [SUN, earth], t)


def draw(screen: pg.Surface, objs, t):
	screen.fill((0, 0, 0))
	screen.blit(pg.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

	pg.draw.circle(screen, GRAY, (250,250), L_SCALE, 2)
	pg.draw.line(screen, GRAY, (0, 250), (500, 250))
	pg.draw.line(screen, GRAY, (250, 0), (250, 500))

	for obj in objs:
		obj.draw(screen)

	fps = clock.get_fps()

	font = pg.font.SysFont(None, 14)

	ttxt = font.render(f"t = {t*100:.1f} days", True, (164, 0, 255))
	screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))

	if paused:
		pausetxt = font.render("PAUSED", True, (255, 24, 0))
		screen.blit(pausetxt, (24, 20))
	else:
		fpstxt = font.render(f"{round(fps, 0)} FPS", True, (0, 255, 0) if fps >= FPS else (255, 0, 0))
		screen.blit(fpstxt, (24, 20))

	pg.display.flip()

def handle_events():
	global done
	global paused

	for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					done = True
				if event.key == pg.K_SPACE:
					paused = not paused


if __name__ == "__main__":
	main()
