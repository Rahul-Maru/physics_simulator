from __future__ import annotations
from numbers import Number
from vector import Vector
import math

class Particle:
	def __init__(self, m: Number, q: Number, s, u, l=0, w=0) -> None:
		self.m = m; self.q = q; self.l = l; self.w = w
		if isinstance(s, Vector):
			self.s = s

		else:
			self.s = Vector(s)

		if isinstance(u, Vector):
			self.v = u
		else:
			self.v = Vector(u)
	
	def move(self, F: Vector, dt: Number, Ufn = lambda : None) -> None:
		a = F/self.m

		self.v += a*dt/2
		if Ufn:
			U = Ufn(self.s, self.v)
		else: 
			U = 0
		self.v += a*dt/2

		self.s += self.v*dt


		return U
	
	def __str__(self) -> str:
		return f"m: {self.m} || q: {'+' if self.q > 0 else ''}{self.q} || s: {self.s} v: {self.v}"