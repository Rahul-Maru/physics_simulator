"""Module for the spring class."""

from numbers import Number

from src.vars.consts import pg, RES
from src.utils.vector import Vector, J

class Spring:
	"""
	A class for creating Spring objects.

	Attributes
	----------
		k : Number
			The spring's spring constant.
		fixed_pos : Vector
			The position of the spring's base/fixed point.
		sr : Vector
			The rest point of the spring's mobile end.
		s : Vector
			The current position of mobile end of spring.
		img : Pygame.Surface
			The sprite of the spring.
		w : Number
			The width of the spring.
	"""

	def __init__(self, k: Number, base_pos: Vector, sr: Vector, width: Number = 1, img_src: str = "img/spring.png") -> None:
		"""
		Creates a spring object.

		Parameters
		----------
			k : Number
				The spring's spring constant.
			base_pos : Vector
				The position of the spring's base/fixed point.
			sr : Vector
				The rest point of the spring's mobile end.
			width : Number
				The width of the spring.
				Default is 1.
			img_src : str
				The path to the sprite of the spring.
		"""

		self.img = pg.image.load(img_src).convert_alpha()

		self.k = k

		self.fixed_pos = base_pos
		self.w = width

		self.sr = sr
		self.s = J
	
	def F(self, s: Vector) -> Vector:
		"""The spring's restorative force."""

		return -self.k*(s-self.sr)
	
	def energy(self, s) -> Number:
		"""The energy stored in the spring."""

		return self.k*(s - self.sr)**2/2
	
	def draw(self, screen: pg.Surface) -> None:
		"""Draws the spring, and the spring's equillibrium point to the screen."""

		# spring image
		screen.blit(pg.transform.scale(self.img, RES@Vector(1, min(self.s.y(), 0))), (RES@self.fixed_pos).tup())
		
		# equillibrium line
		pg.draw.line(screen, (200, 200, 200), RES@Vector(1.5, self.sr.y()), RES@Vector(3.5, self.sr.y()))
