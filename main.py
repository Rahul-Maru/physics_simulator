"""
——— PHYSICS SIMULATOR (will come up with a good name later) ———
A program to simulate the n-body problem.
"""

from itertools import combinations

from src.particle import Particle
from src.plot import plot
from src.text import text_engine
from src.consts import *
from src.colors import *
from src.vector import I, J

done = False
paused = False
show_barycenter = False
center = v0(2) # The center of the Field of Vision (FOV)
zoom = 1
t = 0 # IRL s

particle_list = []


def main() -> None:
	"""Run the simulation."""

	global t, particle_list
	pg.init()
	text_engine.init_font()

	secs = -LOG_S # IRL s (real life seconds)
	log = False

	sun = Particle(m_s, 0, s0_s, u_s, SIZE_S, img_src=SUN_IMG, name="Sun")
	earth = Particle(m_e, 0, s0_e, u_e, SIZE_E, img_src=EARTH_IMG, name="Earth")
	particle_list = [sun, earth]

	leapfrog_setup(particle_list)

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
				tlist.append(t*T_SCALE/DAY)

			move(particle_list, dt, log)

			log = False

		draw(screen, particle_list)

	pg.quit()

	print(f"{Vector.c} vector objects created")
	plot((tlist, "t/day"), (Ulist, "Potential Energy"), (KElist, "Kinetic Energy"), (Elist, "Energy"), (plist, "|Linear Momentum|"), (Llist, "|Angular momentum|"))


def leapfrog_setup(particle_list: list[Particle]) -> None:
	"""Setup the half-step intervals for velocity required leap-frog integration method."""
	for p1, p2 in combinations(particle_list, 2):
		F0 = (Fg(p1, p2)) # [M][L][T]¯²

		p1.v += F0/(2*FPS*p1.m)
		p1.s += p1.v/FPS

		p2.v -= F0/(2*FPS*p2.m)
		p2.s += p2.v/FPS

tlist = []
Ulist = []
KElist = []
Elist = []
plist = []
Llist = []

def move(particle_list: list[Particle], dt, log) -> None:
	"""Move all the bodies in the system over one timestep."""
	ΣU = 0 # [M][L]²[T]¯²
	ΣKE = 0 # [M][L]²[T]¯²
	Σp = v0(2) # [M][L][T]¯¹
	ΣL = v0(3) # [M][L]²[T]¯¹
	if log: print(f"{t=:.2f}s ({t*T_SCALE/DAY:.0f} days)")
	for p1, p2 in combinations(particle_list, 2):
		# F(a→b) = -F(b→a) so we only need to calculate one force
		F_net = FORCE(p1, p2)

		if log:
			p1.move(F_net, dt)
			p2.move(-F_net, dt)

			ΣU += PE(p1, p2)

			# add momenta to the totals
			Σp += p1.m*p1.v + p2.m*p2.v
			ΣL += p1.m*(p1.v*p1.s) + p2.m*(p2.v*p2.s)

			print(f"{p1.name} ← {p2.name}")
			print(f"{p1:.3f}")

			print(f"{p2.name} ← {p1.name}")
			print(f"{p2:.3f}")

		else: 
			p1.move(F_net, dt)
			p2.move(-F_net, dt)

	if log:
		for p in particle_list:
			ΣKE += KE(p) # add the kinetic energies of the particles
		Ulist.append(ΣU)
		KElist.append(ΣKE)
		ΣE = ΣU + ΣKE
		Elist.append(ΣE)
		plist.append(Σp.mag())
		Llist.append(ΣL.mag())

		print(f"ΣE: {ΣE:0.3E} || Σp: {Σp:0.3E} ({Σp.mag():.3E}) || ΣL: {ΣL.mag():.3E}\n")
		text_engine.update_momenta(ΣE, Σp, ΣL)

def barycenter(particle_list: list[Particle]) -> Vector:
	"""Calculates the barycenter (center of mass) of the system of particles."""
	s = v0(2)
	M = 0
	for p in particle_list:
		s += p.m*p.s
		M += p.m
	return s/M


def draw(screen: pg.Surface, objs: list[Particle]) -> None:
	"""Draws objects, text, etc on the screen."""
	screen.blit(bg, (0, 0))

	pg.draw.line(screen, D_GRAY, \
			  (0, MID.y() + center.y()*RES*zoom), \
			  (WINDOW_WIDTH, MID.y() + center.y()*RES*zoom)) # x-axis
	pg.draw.line(screen, D_GRAY, \
			  (MID.x() - center.x()*RES*zoom, 0), \
			  (MID.x() - center.x()*RES*zoom, WINDOW_HEIGHT)) # y-axis


	# render all objects
	for obj in objs:
		obj.draw(screen, center, zoom)

	if show_barycenter:
		pg.draw.circle(screen, D_RED, (zoom*(RES_MAT@(barycenter(objs) - center)) + MID).tup(), 4*zoom)

	text_engine.draw(screen, t, paused)

	# crosshair
	pg.draw.line(screen, GRAY, (MID.x() - 10, MID.y()), (MID.x() + 10, MID.y()))
	pg.draw.line(screen, GRAY, (MID.x(), MID.y() - 10), (MID.x(), MID.y() + 10))

	pg.display.flip()

last_key = None
last_key_time = 0

def handle_events(dt) -> None:
	"""Handles keyboard and other events."""
	global done, paused, center, zoom, show_barycenter, last_key, last_key_time

	if last_key:
		last_key_time += dt
		if last_key_time >= 0.4:
			last_key = None
			text_engine.last_key = None
			last_key_time = 0

	for event in pg.event.get():
		if event.type == pg.QUIT:
			done = True

		elif event.type == pg.KEYDOWN:
			is_ctrl = last_key == pg.K_LCTRL or last_key == pg.K_RCTRL
			if event.key == pg.K_ESCAPE and last_key == pg.K_ESCAPE:
				done = True

			elif event.key == pg.K_SPACE:
				paused = not paused

			elif event.key == pg.K_b:
				show_barycenter = not show_barycenter

			elif event.key == pg.K_c:
				center = v0(2)
				text_engine.update_center(center)

			elif is_ctrl and event.key == pg.K_b:
				center = barycenter(particle_list)
				text_engine.update_center(center)

			elif is_ctrl and event.key == pg.K_0:
				zoom = 1
				text_engine.update_zoom(zoom)

			elif event.key == pg.K_EQUALS or event.key == pg.K_PLUS or event.key == pg.K_KP_PLUS:
				zoom = min(30.912681, zoom*1.1)
				text_engine.update_zoom(zoom)

			elif event.key == pg.K_MINUS or event.key == pg.K_KP_MINUS:
				zoom = max(0.032349184, zoom/1.1)
				text_engine.update_zoom(zoom)

			else:
				last_key = event.key
				text_engine.last_key = last_key

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
