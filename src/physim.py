from time import time
from itertools import permutations

from particle import Particle
from consts import *
from text import text_engine

done = False
paused = False
center = Vector(0, 0)
zoom = 1

def main():
	pg.init()
	text_engine.init_font()
	
	t = 0 # IRL s
	secs = 10000-LOG_S # IRL s (real life seconds)
	log = False

	sun = Particle(m_s, 0, s0_s, u_s, SIZE_S, img_src="img/sun.png", name="Sun")
	earth = Particle(m_e, 0, s0_e, u_e, SIZE_E, img_src="img/earth.png", name="Earth")
	p_list = [sun, earth]

	# FIXME implement leap-frog for all particles
	a0 = (Fg(earth, sun))/m_e # [L][T]¯²

	# v(dt/2) | setup for the leap-frog integration method
	earth.v += a0/(2*FPS)
	earth.s += earth.v/FPS

	ste = stm = std = n = 0

	# simulator loop
	while not done:
		dt = clock.tick_busy_loop(FPS)/1000  # IRL s
		t += dt
		n += 1

		te = time()
		handle_events(dt)
		dte = time() - te
		ste += dte
		print(f"Event: {dte*1000}ms")

		tm = time()
		# if dt is too large, accuracy will be impaired, so prevent the movement
		#   cycle from occuring if the framerate falls below 24 FPS
		if not paused and dt < 0.42:
			# FIXME t += dt

			# logs data
			if t >= secs + LOG_S:
				secs += LOG_S
				log = True

			move(p_list, dt, log)

			if log: log = False

		dtm = time() - tm
		stm += dtm
		print(f"Movement: {dtm*1000}ms")

		td = time()

		draw(screen, p_list, t)

		dtd = time() - td
		print(f"Draw: {(dtd)*1000}ms")
		std += dtd

		print(f"dt: {dt} || All: {(time() - te)*1000}\n")

	
	print(f"AVG || t: {t} || n: {n} || FPS: {n/t} || dt: {t*1000/n} || event: {ste*1000/n} || movement: {stm*1000/n} || draw: {std*1000/n} || background: {stb*1000/n} ||",
	   f"image: {sti*1000/n} || x-axis: {stx*1000/n} || y-axis: {sty*1000/n} || objects: {sto*1000/n} || text: {stt*1000/n}")



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

stb = sto = stt = 0
sti = stx = sty = 0
def draw(screen: pg.Surface, objs: list[Particle], t):
	# TODO: tutorial text / render before loop
	global stb, sto, stt, sti, stx, sty

	tb = time()

	ti = time()
	screen.blit(bg, (0, 0))
	dti = time() - ti
	print(f"Image: {dti*1000}ms")
	sti += dti

	tx = time()
	pg.draw.line(screen, D_GRAY, \
			  (0, MID.y() + center.y()*RES*zoom), \
			  (WINDOW_WIDTH, MID.y() + center.y()*RES*zoom)) # x-axis
	dtx = time() - tx
	print(f"X-axis: {dtx*1000}ms")
	stx += dtx

	ty = time()
	pg.draw.line(screen, D_GRAY, \
			  (MID.x()  - center.x()*RES*zoom, 0), \
			  (MID.y()  - center.x()*RES*zoom, WINDOW_HEIGHT)) # y-axis
	dty = time() - ty
	print(f"Y-axis: {dty*1000}ms")
	sty += dty

	dtb = time() - tb
	print(f"Background: {dtb*1000}ms")
	stb += dtb

	to = time()

	# render all objects
	for obj in objs:
		obj.draw(screen, center, zoom)
	
	dto = time() - to
	print(f"Object: {dto*1000}ms")
	sto += dto

	tt = time()

	text_engine.render(screen, t, paused)

	pg.display.flip()

	dtt = time() - tt
	print(f"Text: {dtt*1000}ms")
	stt += dtt

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
				text_engine.update_center(center)
			elif ((event.key == pg.K_LCTRL or event.key == pg.K_RCTRL) and last_key == pg.K_0) \
			  or ((last_key == pg.K_LCTRL or last_key == pg.K_RCTRL) and event.key == pg.K_0):
				zoom = 1
				text_engine.update_zoom(zoom)
			elif event.key == pg.K_EQUALS or event.key == pg.K_PLUS:
				zoom *= 1.1
				text_engine.update_zoom(zoom)
			elif event.key == pg.K_MINUS:
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
