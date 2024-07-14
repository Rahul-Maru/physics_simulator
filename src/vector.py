from __future__ import annotations

from abc import ABC
from numbers import Number
import math

# Class of things that support matrix multiplication, Vector-likes
class Vectoid(ABC): pass

class Vector(Vectoid):

	c = 0 # debugging purposes

	def __init__(self, *args) -> None:
		Vector.c += 1

		if len(args) == 0:
			self.comps = []
			return
		elif len(args) == 1:
			if isinstance(args[0], list) or isinstance(args[0], tuple):
				args = args[0]
			elif isinstance(args[0], Vector):
				self.comps = args[0].comps.copy()
				return

		for arg in args:
			if not isinstance(arg, Number):
				raise TypeError("Type Mismatch Error: Invalid type for Vector coordinates")

		self.comps = list(args)


	def x(self) -> Number:
		if len(self) >= 1:
			return self.comps[0]
		return 0

	def y(self) -> Number:
		if len(self) >= 2:
			return self.comps[1]
		return 0

	def z(self) -> Number:
		if len(self) >= 3:
			return self.comps[2]
		return 0

	def mag(self) -> Number:
		if len(self.comps) == 0:
			return 0

		sum2 = 0
		for comp in self.comps:
			sum2 += comp**2
		
		return math.sqrt(sum2)

	def unit(self) -> Vector:
		if len(self.comps) == 0:
			return Vector()
		
		return self/self.mag()

	def dot(self, o: Vector) -> Number:
		if len(self.comps) == 0:
			return 0

		sum = 0
		for a, b in zip(self.comps, o.comps):
			sum += a*b

		return sum
	
	def cross(self, o: Vector) -> Vector:
		# only works with 3D vectors. If it has fewer, add 0's.
		#   If it has more, truncate the extra dimensions
		return Vector(self.y()*o.z() - self.z() * o.y(), self.z()*o.x() - self.x()*o.z(), self.x()*o.y() - self.y()*o.x())


	def __eq__(self, o: Vector) -> bool:
		if isinstance(o, Vector):
			if len(self) == len(o):
				for a, b in zip(self.comps, o.comps):
					if a != b:
						return False
		return False

	def __len__(self) -> int:
		return len(self.comps)
	
	def __str__(self) -> str:
		if len(self.comps) == 0:
			return "<>"
		vectstr = "<"
		for comp in self.comps: vectstr += f"{comp}, "
		return vectstr[:-2] + ">"

	def __repr__(self) -> str:
		return super().__repr__() + f"|| {self.comps=}"

	def tup(self) -> tuple:
		return tuple(self.comps)
	
	def __format__(self, format_spec: str) -> str:
		if len(self.comps) == 0:
			return "<>"
		vectstr = "<"
		for comp in self.comps: vectstr += comp.__format__(format_spec) + ", "
		return vectstr[:-2] + ">"

	def	__neg__(self) -> Vector:
		result = Vector()
		for comp in self.comps:
			result.comps.append(-comp)
		return result

	def __add__(self, o: Vector) -> Vector:
		if len(self.comps) != len(o.comps):
			raise ArithmeticError("Vectors must be of same length to be added or subtracted")
		
		result = Vector()
		for comp, ocomp in zip(self.comps, o.comps):
			result.comps.append(comp + ocomp)

		return result
	
	def __iadd__(self, o: Vector) -> Vector:
		if len(self.comps) != len(o.comps):
			raise ArithmeticError("Vectors must be of same length to be added or subtracted")

		for i, ocomp in enumerate(o.comps):
			self.comps[i] += ocomp

		return self

	def __sub__(self, o: Vector) -> Vector:
		return self + -o

	def __isub__(self, o: Vector) -> Vector:
		self += -o
		return self

	def __mul__(self, k: Number) -> Vector:
		result = Vector()
		for comp in self.comps:
			result.comps.append(k*comp)
		return result

	def __imul__(self, k: Number) -> Vector:
		for i in range(len(self.comps)):
			self.comps[i] *= k
		return self

	def __rmul__(self, k: Number) -> Vector:
		result = Vector()
		for comp in self.comps:
			result.comps.append(k*comp)
		return result

	def __truediv__(self, k: Number) -> Vector:
		return self*(1/k)

	def __itruediv__(self, k: Number) -> Vector:
		self *= 1/k
		return self
