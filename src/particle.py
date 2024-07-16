from __future__ import annotations

from numbers import Number
from src.consts import *
from src.colors import LIME

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

		match flags:
			case "i": self.mobile = False
			case _: self.mobile = True

		if len(img_src) > 0:
			self.has_img = True
			self.img = pg.image.load(img_src).convert_alpha()
		else:
			self.has_img = False
			self.color = color

	def move(self, F: Vector, dt: float) -> None:
		# only move the particle if it can move
		if self.mobile:
			a = F/self.m # [L][T]¯²
			self.v += a*dt
			self.s += self.v*dt

	
	def draw(self, screen: pg.Surface, center: Vector, zoom: float) -> None:
		coords = ((zoom * (RES_MAT@(self.s - center) - self.size/2)) + MID).tup()
		size = (zoom*self.size).tup()

		# only render the particle if it is visible
		if -size[0] < coords[0] < WINDOW_WIDTH and -size[1] < coords[1] < WINDOW_HEIGHT:
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
