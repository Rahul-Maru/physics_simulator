from consts import *
from particle import Particle
from itertools import permutations

done = False
paused = False
center = Vector(0, 0)
zoom = 1

def main():
	pg.init()

	t = 0 # IRL s
	secs = -LOG_S # IRL s (real life seconds)
	log = False

	sun = Particle(m_s, 0, s0_s, u_s, SIZE_S, img_src="img/sun.png", name="Sun")
	earth = Particle(m_e, 0, s0_e, u_e, SIZE_E, img_src="img/earth.png", name="Earth")
	p_list = [sun, earth]

	# FIXME implement leap-frog for all particles
	a0 = (Fg(earth, sun))/m_e # [L][T]¯²

	# v(dt/2) | setup for the leap-frog integration method
	earth.v += a0/(2*FPS)
	earth.s += earth.v/FPS

	# simulator loop
	while not done:
		dt = clock.tick_busy_loop(FPS)/1000  # IRL s

		handle_events(dt)

		# if dt is too large, accuracy will be impaired
		if not paused and dt < 0.8:
			t += dt

			# logs data
			if t >= secs + LOG_S:
				secs += LOG_S
				log = True

			move(p_list, dt, log)

			if log: log = False

		draw(screen, p_list, t)

def move(p_list: list[Particle], dt, log):
	for p1, p2 in permutations(p_list, 2):
		F_net = Fg(p1, p2)

		if log:
			U = p1.move(F_net, dt, ENERGY, p2)
			L = p1.m*p1.v*(p1.s-p2.s).mag() # [M][L]²[T]¯¹

			print(f"{p1.name} <-- {p2.name}")
			print(f"{p1:.3f}")
			# TODO maybe move this out of the for loop
			print(f"a: {F_net/p1.m:.3f} || U: {U:.3E} || L: {L.mag():.3E}\n")
		else: 
			p1.move(F_net, dt)

def draw(screen: pg.Surface, objs: list[Particle], t):
	# TODO: tutorial text / render before loop

	screen.blit(bg, (0, 0))

	pg.draw.line(screen, D_GRAY, \
			  (0, MID.y() + center.y()*RES*zoom), \
			  (WINDOW_WIDTH, MID.y() + center.y()*RES*zoom)) # x-axis
	pg.draw.line(screen, D_GRAY, \
			  (MID.x()  - center.x()*RES*zoom, 0), \
			  (MID.y()  - center.x()*RES*zoom, WINDOW_HEIGHT)) # y-axis

	# render all objects
	for obj in objs:
		obj.draw(screen, center, zoom)

	font = pg.font.SysFont(None, 14)

	# display the current simulation time
	ttxt = font.render(f"t = {t*T_SCALE/DAY:.0f} days", True, MAGENTA)
	screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))

	# display the current center of viewpoint and zoom
	ctxt = font.render(f"{center:.2f}", True, ORANGE)
	ztxt = font.render(f"Q {zoom:.2f}x", True, ORANGE)
	screen.blit(ctxt, (WINDOW_WIDTH - ctxt.get_width() - 24, WINDOW_WIDTH - ctxt.get_height() - ztxt.get_height() - 20))
	screen.blit(ztxt, (WINDOW_WIDTH - ztxt.get_width() - 24, WINDOW_WIDTH - ztxt.get_height() - 20))

	if paused:
		pausetxt = font.render("PAUSED II", True, RED)
		screen.blit(pausetxt, (24, 20))
	else:
		# display the current fps
		current_fps = clock.get_fps()
		fpstxt = font.render(f"{round(current_fps, 0)} FPS", True, GREEN if current_fps >= FPS else RED)
		screen.blit(fpstxt, (24, 20))

	pg.display.flip()

last_key = None
key_time = 0

def handle_events(dt):
	global done, paused, center, zoom, last_key, key_time

	if last_key:
		key_time += dt
		if key_time >= 0.5:
			last_key = None
			key_time = 0

	for event in pg.event.get():
		if event.type == pg.QUIT:
			done = True
		elif event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				done = True
			elif event.key == pg.K_SPACE:
				paused = not paused
			elif event.key == pg.K_c:
				center = Vector(0, 0)
			elif ((event.key == pg.K_LCTRL or event.key == pg.K_RCTRL) and last_key == pg.K_0) \
			  or ((last_key == pg.K_LCTRL or last_key == pg.K_RCTRL) and event.key == pg.K_0):
				zoom = 1
			elif event.key == pg.K_EQUALS or event.key == pg.K_PLUS:
				zoom *= 1.1
			elif event.key == pg.K_MINUS:
				zoom *= 0.9090909091
			else: last_key = event.key

	keys = pg.key.get_pressed()
	if keys[pg.K_UP]:
		center += J*dt/zoom
	if keys[pg.K_RIGHT]:
		center += I*dt/zoom
	if keys[pg.K_DOWN]:
		center -= J*dt/zoom
	if keys[pg.K_LEFT]:
		center -= I*dt/zoom


if __name__ == "__main__":
	main()
