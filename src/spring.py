from numbers import Number
from consts import pg, RES, WIDTH, s0

from vector import Vector

class Spring:
	def __init__(self, k: Number, base_pos: Vector, sr: Vector, width: Number = WIDTH, img_src: str = "img/spring.png") -> None:
		self.img = pg.image.load(img_src)

		self.k = k # spring constant

		self.fixed_pos = base_pos # fixed point of the spring
		self.w = width # width of spring

		self.sr = sr # rest point of mobile end of spring
		self.s = s0 # current position of mobile end of spring
	
	def F(self, s: Vector) -> Vector:
		return -self.k*(s-self.sr)
	
	def energy(self, s) -> Number:
		return self.k*(s - self.sr)**2/2
	
	def draw(self, screen: pg.Surface) -> None:
		# spring image
		screen.blit(pg.transform.scale(self.img, (RES, max(-self.s.comps[1], 0)*RES)), tuple((self.fixed_pos*RES).comps))
		
		# equillibrium line
		pg.draw.line(screen, (200, 200, 200), (1.5*RES, -self.sr.y()*RES), (3.5*RES, - self.sr.y()*RES))



