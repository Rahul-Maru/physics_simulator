from itertools import permutations

from particle import Particle
from consts import *
from text import text_engine

done = False
paused = False
center = Vector(0, 0)
zoom = 1

def main() -> None:
	pg.init()
	text_engine.init_font()

	t = 0 # IRL s
	secs = -LOG_S # IRL s (real life seconds)
	log = False

	sun = Particle(m_s, 0, s0_s, u_s, SIZE_S, img_src="img/sun.png", name="Sun")
	earth = Particle(m_e, 0, s0_e, u_e, SIZE_E, img_src="img/earth.png", name="Earth")
	p_list = [sun, earth]

	leapfrog_setup(p_list)

	while not done:
		dt = clock.tick_busy_loop(FPS)/1000  # IRL s

		handle_events(dt)

		# if dt is too large, accuracy will be impaired, so prevent the movement
		#   cycle from occuring if the framerate falls below 24 FPS
		if not paused and dt < 0.42:
			t += dt

			# logs data
			if t >= secs + LOG_S:
				secs += LOG_S
				log = True

			move(p_list, dt, log)

			if log: log = False

		draw(screen, p_list, t)


def leapfrog_setup(p_list: list[Particle]) -> None:
	# setup the half-step intervals required leap-frog integration method
	for p1, p2 in permutations(p_list, 2):
		a0 = (Fg(p1, p2))/p1.m # [L][T]¯²

		p1.v += a0/(2*FPS)
		p1.s += p1.v/FPS

def move(p_list: list[Particle], dt, log) -> None:
	for p1, p2 in permutations(p_list, 2):
		F_net = Fg(p1, p2)

		if log:
			U = p1.move(F_net, dt, ENERGY, p2)
			L = p1.m*p1.v*(p1.s-p2.s).mag() # [M][L]²[T]¯¹

			print(f"{p1.name} ← {p2.name}")
			print(f"{p1:.3f}")
			# TODO maybe move this out of the for loop
			print(f"a: {F_net/p1.m:.3f}\nU: {U:.3E} || L: {L.mag():.3E}")
		else: 
			p1.move(F_net, dt)

def draw(screen: pg.Surface, objs: list[Particle], t) -> None:
	# TODO: tutorial text

	screen.blit(bg, (0, 0))

	pg.draw.line(screen, D_GRAY, \
			  (0, MID.y() + center.y()*RES*zoom), \
			  (WINDOW_WIDTH, MID.y() + center.y()*RES*zoom)) # x-axis
	pg.draw.line(screen, D_GRAY, \
			  (MID.x() - center.x()*RES*zoom, 0), \
			  (MID.y() - center.x()*RES*zoom, WINDOW_HEIGHT)) # y-axis


	# render all objects
	for obj in objs:
		obj.draw(screen, center, zoom)

	text_engine.render(screen, t, paused)

	# crosshair
	pg.draw.line(screen, GRAY, (MID.x() - 10, MID.y()), (MID.x() + 10, MID.y()))
	pg.draw.line(screen, GRAY, (MID.x(), MID.y() - 10), (MID.x(), MID.y() + 10))

	pg.display.flip()

last_key = None
last_key_time = 0

def handle_events(dt) -> None:
	global done, paused, center, zoom, last_key, last_key_time

	if last_key:
		last_key_time += dt
		if last_key_time >= 0.2:
			last_key = None
			last_key_time = 0

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
				text_engine.update_center(center)

			elif ((event.key == pg.K_LCTRL or event.key == pg.K_RCTRL) and last_key == pg.K_0) \
			  or ((last_key == pg.K_LCTRL or last_key == pg.K_RCTRL) and event.key == pg.K_0):
				zoom = 1
				text_engine.update_zoom(zoom)

			elif event.key == pg.K_EQUALS or event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:
				zoom *= 1.1
				text_engine.update_zoom(zoom)

			elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
				zoom *= 0.9090909091
				text_engine.update_zoom(zoom)

			else:
				last_key = event.key

	keys = pg.key.get_pressed()
	if keys[pg.K_UP]:
		center += J*dt/zoom
		text_engine.update_center(center)

	if keys[pg.K_RIGHT]:
		center += I*dt/zoom
		text_engine.update_center(center)

	if keys[pg.K_DOWN]:
		center -= J*dt/zoom
		text_engine.update_center(center)

	if keys[pg.K_LEFT]:
		center -= I*dt/zoom
		text_engine.update_center(center)


if __name__ == "__main__":
	main()
