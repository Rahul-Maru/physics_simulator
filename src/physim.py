from consts import *
from particle import Particle

done = False
paused = False

def main():
	pg.init()

	t = 0 # IRL s
	secs = -LOG_S # IRL s (real life seconds)

	SUN = Particle(m_s, 0, s_s, 0, SIZE_S, img_src="img/sun.png")
	earth = Particle(m_e, 0, s0_e, u, SIZE_E, img_src="img/earth.png")

	# function energy
	E = lambda p1, p2: -G*m_e*m_s/(p1.s-p2.s).mag() + p1.m*p1.v.mag()**2/2 # [M][L]²[T]¯²

	a0 = (Fg(earth, SUN))/m_e # [L][T]¯²

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
			L = earth.m*earth.v*(earth.s-SUN.s).mag() # [M][L]²[T]¯¹

			# logs data
			if t >= secs + LOG_S:
				secs += LOG_S
				print(f"t {secs*T_SCALE/DAY:.0f} ||| s {earth.s} || v {earth.v} \n a {F_net/m_e} || U {U} || L {L.mag()}")

		draw(screen, [SUN, earth], t)


def draw(screen: pg.Surface, objs, t):
	screen.blit(pg.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT)), (0, 0))

	pg.draw.line(screen, D_GRAY, (0, WINDOW_HEIGHT/2), (WINDOW_WIDTH, WINDOW_HEIGHT/2)) # x-axis
	pg.draw.line(screen, D_GRAY, (WINDOW_WIDTH/2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT)) # y-axis

	pg.draw.circle(screen, D_YELLOW, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), RES, 2) # expected orbit

	# render all objects
	for obj in objs:
		obj.draw(screen)

	font = pg.font.SysFont(None, 14)

	# display the current simulation time
	ttxt = font.render(f"t = {t*T_SCALE/DAY:.1f} days", True, MAGENTA)
	screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))

	if paused:
		pausetxt = font.render("PAUSED II", True, RED)
		screen.blit(pausetxt, (24, 20))
	else:
		# display the current fps
		current_fps = clock.get_fps()
		fpstxt = font.render(f"{round(current_fps, 0)} FPS", True, GREEN if current_fps >= FPS else RED)
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
