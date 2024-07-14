from __future__ import annotations
from numbers import Number
from consts import *

class Particle:
	def __init__(self, m: Number, q: Number, s, u, size=(0.4, 0.4),
			  color: tuple = LIME, img_src: str = "", flags: str = "", name: str = "Particle") -> None:
		self.m = m # [M]  mass
		self.q = q # [T][I]  charge
		self.size = Vector(size)*RES
		self.name = name

		if isinstance(s, Vector):
			self.s = s # [L]
		else:
			self.s = Vector(s) # [L]

		if isinstance(u, Vector):
			self.v = u # [L][T]¯¹
		else:
			self.v = Vector(u) # [L][T]¯¹

		self.mobile = 1
		match flags:
			case "i": self.mobile = 0

		if len(img_src) > 0:
			self.has_img = True
			self.img = pg.image.load(img_src).convert_alpha()
		else:
			self.has_img = False
			self.color = color

	def move(self, F: Vector, dt: Number, Ufn: function = None, o: Particle = None) -> None:
		a = F/self.m # [L][T]¯²

		# calculate energy when s and v are lined up
		if Ufn:
			# update the velocity to be on a whole-numbered time step
			self.v += a*dt/2

			U = Ufn(self, o)

			# update velocity back to half-step to continue leap-frogging
			self.v += a*dt/2
		else: 
			self.v += a*dt

		self.s += self.v*dt * self.mobile

		return U if Ufn else 0 # [M][L][T]¯²
	
	def draw(self, screen: pg.Surface, center: Vector, zoom: Number) -> None:
		coords = ((zoom * (RES_MAT@(self.s - center) - self.size*0.5)) + MID).tup()
		size = (zoom*self.size).tup()

		if self.has_img:
			screen.blit(pg.transform.scale(self.img, size), coords)
		else:
			pg.draw.rect(screen, self.color, pg.Rect(*coords, *size))


	def __str__(self) -> str:
		return f"{self.name} |||  m: {self.m} || q: {self.q:+} || s: {self.s} || v: {self.v}"

	def __format__(self, f: str) -> str:
		e = lambda x : f.replace("f", "E") if x != 0 and abs(log10(abs(x))) >= 2 else f
		qf= ('+' if '+' not in f else '') + e(self.q)
		return f"{self.name} |||  m: {self.m.__format__(e(self.m))} || q: {self.q.__format__(qf)} || s: {self.s.__format__(e(self.s.mag()))} || v: {self.v.__format__(e(self.s.mag()))}"
