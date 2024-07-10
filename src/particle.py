from __future__ import annotations
from numbers import Number
from vector import Vector
from consts import pg, SCALE, WIDTH
import math

class Particle:
	def __init__(self, m: Number, q: Number, s, u, l=0.4, w=0.4, color: tuple = (128, 255, 0)) -> None:
		self.m = m # kg  mass
		self.q = q # C  charge
		self.l = l # m  length
		self.w = w # m  width
		self.color = color

		if isinstance(s, Vector):
			self.s = s # m
		else:
			self.s = Vector(s) # m

		if isinstance(u, Vector):
			self.v = u # m/s
		else:
			self.v = Vector(u) # m/s
	
	def move(self, F: Vector, dt: Number, Ufn = lambda : None) -> None:
		a = F/self.m # m/s²

		# update the velocity to be on a whole-numbered time step
		self.v += a*dt/2
		# calculate energy when s, and v are lined up
		if Ufn:
			U = Ufn(self.s, self.v)
		else: 
			U = 0
		# update velocity back to half-step to continue leap-frogging
		self.v += a*dt/2

		self.s += self.v*dt

		return U # J
	
	def draw(self, screen: pg.Surface) -> None:
		pg.draw.rect(screen, self.color, pg.Rect(self.s.x()*SCALE, -self.s.y()*SCALE, self.l*SCALE, self.w*SCALE))


	def __str__(self) -> str:
		return f"m: {self.m} || q: {'+' if self.q > 0 else ''}{self.q} || s: {self.s} v: {self.v}"