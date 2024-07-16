"""Module containing the Particle class."""

from __future__ import annotations

from numbers import Number
from utils.consts import *
from utils.colors import LIME

class Particle:
	"""
	Class for storing, moving, and rendering particle-like objects.

	Attributes
	----------
		m : Number
			Mass of the particle.
		q : Number
			Charge of the particle.
		s : Vector
			Position of the particle (in simulation coordinates).
		v : Vector
			Velocity of the particle (in simulation coordinates).
		size : Vector
			Size of the particle.
		name : str
			What the particle will be reffered to as in log messages.
		has_img : bool
			Whether the particle has a sprite or not.
		color : tuple [R, G, B]
			RGB color value of the particle (default LIME) if there is no sprite.
		img : Pygame.Surface
			The particle's sprite, if any.
		mobile : bool
			Whether the particle is allowed to move
			(set to false for the center of Force in the 1-body problem).
	"""
	def __init__(self, m: Number, q: Number, s: Vector, u: Vector, size=(0.4, 0.4),
			  color: tuple = LIME, img_src: str = "", flags: str = "", name: str = "Particle") -> None:
		"""
		Creates a particle.

		Parameters
		----------
			m : Number
				Mass of the particle.
			q : Number
				Charge of the particle.
			s : Vector
				Initial position of the particle (in simulation coordinates).
			u : Vector
				Initial velocity of the particle (in simulation coordinates).
			size : tuple
				Size of the particle (in simulation coordinates).
				Default is (0.4, 0.4)
			color : tuple [R, G, B]
				RGB color value of the particle if there is no sprite.
				Default is src.colors.LIME (162, 220, 53).
			img_src : str
				Path to the particle's sprite, if any.
			flags : str
				Special properties of the particle:
					i - Particle is immobile.
			name : str
				What the particle will be reffered to as in log messages.
		"""

		self.m = m # [M]  mass
		self.q = q # [T][I]  charge
		self.size = Vector(size) * RES # [L]
		self.name = name

		self.s = s # [L]
		self.v = u # [L][T]¯¹

		match flags:
			case "i": self.mobile = False
			case _: self.mobile = True

		# if there is an image, load it, otherwise set the color
		if len(img_src) > 0:
			self.has_img = True
			self.img = pg.image.load(img_src).convert_alpha()
		else:
			self.has_img = False
			self.color = color

	def move(self, F: Vector, dt: float) -> None:
		""" Updates the position and velocity of the particle
		given a force and time-step.
		"""
		# only move the particle if it can move
		if self.mobile:
			a = F/self.m # [L][T]¯²
			self.v += a*dt
			self.s += self.v*dt

	
	def draw(self, screen: pg.Surface, center: Vector, zoom: float) -> None:
		"""
		Renders all the particles onto the screen.

		Parameters
		----------
			screen : Pygame.Surface
				The surface to render the text on.
			center : Vector
				The center of the FOV
			zoom : float
				The zoom multiplier
		"""

		# adjust position and size to pygame coordinates, and convert to tuples
		coords = scale_coords(self.s, zoom, center, self.size)
		size = (zoom*self.size).tup()

		# only render the particle if it is visible
		if -size[0] < coords[0] < WINDOW_WIDTH and -size[1] < coords[1] < WINDOW_HEIGHT:
			if self.has_img:
				screen.blit(pg.transform.scale(self.img, size), coords)
			else:
				pg.draw.rect(screen, self.color, pg.Rect(*coords, *size))


	def __str__(self) -> str:
		"""
		Generates a string containing the particle's information.

		Returns
		-------
		str
			Format: "name ||| mass || +/- charge || position || velocity".
		"""

		return f"{self.name} |||  m: {self.m} || q: {self.q:+} || s: {self.s} || v: {self.v}"

	def __format__(self, f: str) -> str:
		# format in float notation if the |x| < 10⁶, otherwise in scientific notation
		e = lambda x : f.replace("f", "E") if x != 0 and abs(log10(abs(x))) >= 2 else f
		# if the format code does not already contain '+', add it
		qf= ('+' if '+' not in f else '') + e(self.q)
		return f"{self.name} |||  m: {self.m.__format__(e(self.m))} || q: {self.q.__format__(qf)} || s: {self.s.__format__(e(self.s.mag()))} || v: {self.v.__format__(e(self.s.mag()))}"
