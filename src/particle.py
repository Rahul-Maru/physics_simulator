from __future__ import annotations
from numbers import Number
from vector import Vector
from consts import pg, SCALE
import math

class Particle:
	def __init__(self, m: Number, q: Number, s, u, size=(0.4, 0.4),
			  color: tuple = (128, 255, 0), img_src: str = "", flags: str = "",) -> None:
		self.m = m # kg  mass
		self.q = q # C  charge
		self.w, self.h = size[0], size[1]
		self.color = color

		if isinstance(s, Vector):
			self.s = s # m
		else:
			self.s = Vector(s) # m

		if isinstance(u, Vector):
			self.v = u # m/s
		else:
			self.v = Vector(u) # m/s

		self.mobile = 1
		match flags:
			case "i": self.mobile = 0

		if len(img_src) > 0:
			self.img = pg.image.load(img_src) # source: khanacademy

	
	def move(self, F: Vector, dt: Number, Ufn: function = None, o: Particle = None) -> None:
		a = F/self.m # m/s²

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

		return U # J
	
	def draw(self, screen: pg.Surface) -> None:
		if hasattr(self, "img"):
			screen.blit(pg.transform.scale(self.img, (self.w*SCALE, self.h*SCALE)), ((self.s.x() - self.w/2)*SCALE, (-self.s.y() - self.h/2)*SCALE))
		else:
			pg.draw.rect(screen, self.color, pg.Rect((self.s.x() - self.w/2)*SCALE, (-self.s.y() - self.h/2)*SCALE, self.w*SCALE, self.h*SCALE))


	def __str__(self) -> str:
		return f"m: {self.m} || q: {'+' if self.q > 0 else ''}{self.q} || s: {self.s} v: {self.v}"