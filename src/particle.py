from __future__ import annotations
from numbers import Number
from vector import Vector
from consts import pg, RES
import math

class Particle:
	def __init__(self, m: Number, q: Number, s, u, size=(0.4, 0.4),
			  color: tuple = (128, 255, 0), img_src: str = "", flags: str = "",) -> None:
		self.m = m # [M]  mass
		self.q = q # [T][I]  charge
		self.w, self.h = size[0], size[1]
		self.color = color

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
			self.img = pg.image.load(img_src)
	
	def move(self, F: Vector, dt: Number, Ufn: function = None, o: Particle = None) -> None:
		a = F/self.m # [L][T]¯²

		# update the velocity to be on a whole-numbered time step
		self.v += a*dt/2
		# calculate energy when s, and v are lined up
		if Ufn:
			U = Ufn(self, o)
		else: 
			U = 0
		# update velocity back to half-step to continue leap-frogging
		self.v += a*dt/2

		self.s += self.v*dt * self.mobile

		return U # [M][L][T]¯²
	
	def draw(self, screen: pg.Surface) -> None:
		if hasattr(self, "img"):
			screen.blit(pg.transform.scale(self.img, (self.w*RES, self.h*RES)), ((self.s.x() - self.w/2)*RES, (-self.s.y() - self.h/2)*RES))
		else:
			pg.draw.rect(screen, self.color, pg.Rect((self.s.x() - self.w/2)*RES, (-self.s.y() - self.h/2)*RES, self.w*RES, self.h*RES))


	def __str__(self) -> str:
		return f"m: {self.m} || q: {'+' if self.q > 0 else ''}{self.q} || s: {self.s} v: {self.v}"