from __future__ import annotations
from numbers import Number
import math

class Vector:
	def __init__(self, *args) -> None:
		if len(args) == 0:
			self.comps = []
			return
		elif len(args) == 1:
			if isinstance(args[0], list):
				args = args[0]
			elif isinstance(args[0], Vector):
				self.comps = args[0].comps.copy()
				return

		for arg in args:
			if not isinstance(arg, Number):
				raise TypeError


		self.comps = list(args)



	def append(self, i: Number) -> None:
		self.comps.append(i)

	def set(self, i: Number, index: int) -> None:
		self.comps[index] = i

	def magnitude(self) -> Number:
		if len(self.comps) == 0:
			return 0

		sum2 = 0
		for comp in self.comps:
			sum2 += comp**2
		
		return math.sqrt(sum2)

	def unitvector(self) -> Vector:
		if len(self.comps) == 0:
			return Vector()
		
		return self/self.magnitude()
	
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
			return "()"
		vectstr = "("
		for comp in self.comps: vectstr += f"{comp}, "
		return vectstr[:-2] + ")"
	
	def __add__(self, o: Vector) -> Vector:
		if len(self.comps) != len(o.comps):
			raise ArithmeticError("Vectors must be of same length to be added or subtracted")
		
		result = Vector()
		for comp, ocomp in zip(self.comps, o.comps):
			result.append(comp + ocomp)

		return result
	
	def __mul__(self, k: Number):
		result = Vector()
		for comp in self.comps:
			result.append(k*comp)
		return result
	
	def __truediv__(self, k: Number):
		return self*(1/k)

	def	__neg__(self):
		result = Vector()
		for comp in self.comps:
			result.append(-comp)
		return result
		
	def __sub__(self, o: Vector):
		return self + -o
	
	def __rsub__(self, o: Vector):
		return -self + o
	
	