"""Module for the Vector class and related things."""

from __future__ import annotations

from abc import ABC
from typing import Union
from numbers import Number
import math


class Vectoid(ABC):  """Class of things that support matrix multiplication, Vector-likes."""

class Vector(Vectoid):
	"""
	A class for creating and manipulation mathematical Vector objects.

	Attributes
	----------
		comps : list[Number]
			The components of the vector.
		c : int
			A class-wide attribute that counts the number of Vectors created.
			Used for testing.
	"""
	c = 0 # debugging purposes

	def __init__(self, *args) -> None:
		"""
		Initializes a Vector.

		Parameters
		----------
		A collection of Numbers as a list, tuple, or passed directly as arguments.
		If a vector is passed, it will copy the vector.
		"""
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
		"""Returns the x (1st) component of the vector, or 0 if there is none."""
		if len(self) >= 1:
			return self.comps[0]
		return 0

	def y(self) -> Number:
		"""Returns the y (2nd) component of the vector, or 0 if there is none."""
		if len(self) >= 2:
			return self.comps[1]
		return 0

	def z(self) -> Number:
		"""Returns the z (3nd) component of the vector, or 0 if there is none."""
		if len(self) >= 3:
			return self.comps[2]
		return 0

	def mag(self) -> Number:
		"""Calculates the magnitude of the Vector.

		Returns
		-------
		Number
			√(Σ(Vector.comps[i]²)) ∀ i s.t. 0 ≤ i < Vector.length().
			0 if there are no components.
		"""
		if len(self.comps) == 0:
			return 0

		sum2 = 0
		for comp in self.comps:
			sum2 += comp**2
		
		return math.sqrt(sum2)

	def unit(self) -> Vector:
		"""Returns a normalized version/unit vector of the vector.

		Returns
		-------
		Vector
			Vector/Vector.mag().
			Vector() if there are no components."""
		if len(self.comps) == 0:
			return Vector()
		
		return self/self.mag()

	def __eq__(self, o: Vector) -> bool:
		"""Compares components of two vectors to check equality"""

		if isinstance(o, Vector):
			if len(self) == len(o):
				for a, b in zip(self.comps, o.comps):
					if a != b:
						return False
		return False

	def __len__(self) -> int:
		"""The number of components of the vector."""

		return len(self.comps)
	
	def __str__(self) -> str:
		"""Generates a string representing the components of the vector.

		Returns
		-------
		str
			f"{Vector(a,b,c)}" → <a, b, c>.
		"""
		if len(self.comps) == 0:
			return "<>"
		vectstr = "<"
		for comp in self.comps: vectstr += f"{comp}, "
		return vectstr[:-2] + ">"

	def __repr__(self) -> str:
		return super().__repr__() + f"|| {self.comps=}"

	def tup(self) -> tuple:
		"""Converts the vector's components to a tuple."""
		return tuple(self.comps)
	
	def __format__(self, format_spec: str) -> str:
		if len(self.comps) == 0:
			return "<>"
		vectstr = "<"
		for comp in self.comps: vectstr += comp.__format__(format_spec) + ", "
		return vectstr[:-2] + ">"

	def	__neg__(self) -> Vector:
		"""Negates (the components of) the vector."""
		result = Vector()
		for comp in self.comps:
			result.comps.append(-comp)
		return result

	def __add__(self, o: Vector) -> Vector:
		"""Adds two vectors."""
		if len(self.comps) != len(o.comps):
			raise ArithmeticError("Vectors must be of same length to be added or subtracted")
		
		result = Vector()
		for comp, ocomp in zip(self.comps, o.comps):
			result.comps.append(comp + ocomp)

		return result
	
	def __iadd__(self, o: Vector) -> Vector:
		"""Adds two vectors in place."""
		if len(self.comps) != len(o.comps):
			raise ArithmeticError("Vectors must be of same length to be added or subtracted")

		for i, ocomp in enumerate(o.comps):
			self.comps[i] += ocomp

		return self

	def __sub__(self, o: Vector) -> Vector:
		"""Subtracts two vectors."""
		if len(self.comps) != len(o.comps):
			raise ArithmeticError("Vectors must be of same length to be added or subtracted")

		result = Vector()
		for comp, ocomp in zip(self.comps, o.comps):
			result.comps.append(comp - ocomp)

		return result

	def __isub__(self, o: Vector) -> Vector:
		"""Subtracts two vectors in place."""
		if len(self.comps) != len(o.comps):
			raise ArithmeticError("Vectors must be of same length to be added or subtracted")

		for i, ocomp in enumerate(o.comps):
			self.comps[i] -= ocomp

		return self

	def __mul__(self, o: Union[Number, Vector]) -> Vector:
		"""Multiplies (the components of) the vector by a scalar
		OR takes the cross product of two vectors."""
		# scalar multiplication
		if isinstance(o, Number):
			result = Vector()
			for comp in self.comps:
				result.comps.append(o*comp)
			return result
		# cross product
		elif isinstance(o, Vector):
			# only works with 3D vectors. If it has fewer, add 0's.
			#   If it has more, truncate the extra dimensions
			return Vector(self.y()*o.z() - self.z()*o.y(), self.z()*o.x() - self.x()*o.z(), self.x()*o.y() - self.y()*o.x())


	def __imul__(self, k: Union[Number, Vector]) -> Vector:
		"""Multiples (the components of) the vector by a scalar in place."""
		if isinstance(k, Vector):
			raise NotImplementedError

		for i in range(len(self.comps)):
			self.comps[i] *= k
		return self

	def __rmul__(self, k: Number) -> Vector:
		"""Multiplies (the components of) the vector by a scalar
		when the scalar comes before the vector."""
		result = Vector()
		for comp in self.comps:
			result.comps.append(k*comp)
		return result

	def __matmul__(self, o: Vector) -> Number:
		"""Takes the dot product of two vectors."""
		if len(self.comps) == 0:
			return 0

		sum = 0
		for a, b in zip(self.comps, o.comps):
			sum += a*b

		return sum

	def __truediv__(self, k: Number) -> Vector:
		"""Divides (the components of) the vector by a scalar."""
		return self*(1/k)

	def __itruediv__(self, k: Number) -> Vector:
		"""Divides (the components of) the vector by a scalar in place."""
		self *= 1/k
		return self

	def __rtruediv__(self, k: Number) -> Number:
		"""Divides a scalar by the magnitude of the vector."""
		return k/self.mag()

	def __floordiv__(self, k: Number) -> Vector:
		raise NotImplementedError

	def __rfloordiv__(self, k: Number) -> Number:
		"""Divides a scalar by the magnitude of the vector and floors it."""
		return k//self.mag()

	def __ifloordiv__(self, k: Number) -> Vector:
		raise NotImplementedError

	def __pow__(self, k: Number) -> Number:
		"""Raises the magnitude of the vector to a power."""
		return self.mag()**k


def v0(n: int) -> Vector:
	"""
	Generates a zero-vector.

	Parameters
	----------
		n : int
			the length of the vector.
	Returns
	-------
	Vector
		A vector of dimension n containing only 0's.
	"""

	return Vector([0 for _ in range(n)])

# unit vectors
I = Vector(1, 0)
J = Vector(0, 1)
K = Vector(0, 0, 1)
