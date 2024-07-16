"""Module for the Matrix class."""

from __future__ import annotations

from numbers import Number

from utils.vector import Vectoid, Vector, I, J


class Matrix(Vectoid):
	"""
	A class for creating and manipulation mathematical Matrix objects.

	Attributes
	----------
		basis : list[Vector]
			A list of the basis vectors (columns) that define the matrix.
	"""
	def __init__(self, *args) -> None:
		"""
		Initializes a Matrix.

		Parameters
		----------
		A collection of Vectors as a list, tuple, or passed directly as arguments.
		If a Matrix is passed, it will copy the Matrix.
		If the string "id" is passed, it will create a 2D identity matrix.
		"""
		if len(args) == 0:
			self.basis = []
			return
		elif len(args) == 1:
			if isinstance(args[0], list) or isinstance(args[0], tuple):
				args = args[0]
			elif isinstance(args[0], Matrix):
				for base in args[0].basis:
					self.basis.append(Vector(base))
			elif args[0] == "id":
				self.basis = [I, J] # 2D identity matrix
				return

		self.basis = list(args)


	def __len__(self) -> int:
		"""Number of columns of the matrix."""
		return len(self.basis)
	
	def h(self) -> int:
		"""Number of rows of the matrix."""
		return len(self.basis[0])

	def __str__(self) -> str:
		"""Converts the matrix to a rectangular string."""
		s = "["
		for j in range(len(self.basis[0])):
			for i in range(len(self.basis)):
				s += f"{self.basis[i].comps[j]}, "
			s = s[:-2] + "]\n["
		
		return s[:-1]
	
	def __repr__(self) -> str:
		return super().__repr__() + f"|| {list(map(lambda v: repr(v), self.basis))}"
	
	def __neg__(self) -> Matrix:
		"""Negates (the components of) the matrix."""
		out = Matrix()
		for base in self.basis:
			out.basis.append(-base)
		return out

	def __add__(self, o: Matrix) -> Matrix:
		"""Adds two matrices."""
		if len(self.basis) != len(o.basis) or len(self.basis[0].comps) != len(o.basis[0].comps):
			raise ArithmeticError("Matrices must be of same size to be added or subtracted")

		out = Matrix()
		for base, obase in zip(self.basis, o.basis):
			out.basis.append(base + obase)
		return out
	
	def __iadd__(self, o: Matrix) -> Matrix:
		"""Adds two matrices in place."""
		if len(self.basis) != len(o.basis) or len(self.basis[0].comps) != len(o.basis[0].comps):
			raise ArithmeticError("Matrices must be of same size to be added or subtracted")

		for i, obase in enumerate(o.basis):
			self.basis[i] += obase
		return self

	def __sub__(self, o: Matrix) -> Matrix:
		"""Subtracts two matrices."""
		if len(self.basis) != len(o.basis) or len(self.basis[0].comps) != len(o.basis[0].comps):
			raise ArithmeticError("Matrices must be of same size to be added or subtracted")

		out = Matrix()
		for base, obase in zip(self.basis, o.basis):
			out.basis.append(base - obase)
		return out
	
	def __isub__(self, o: Matrix) -> Matrix:
		"""Subtracts two matrices in place."""
		if len(self.basis) != len(o.basis) or len(self.basis[0].comps) != len(o.basis[0].comps):
			raise ArithmeticError("Matrices must be of same size to be added or subtracted")

		for i, obase in enumerate(o.basis):
			self.basis[i] -= obase
		return self

	def __mul__(self, k: Number) -> Matrix:
		"""Multiplies (the components of) the matrix by a scalar."""

		out = Matrix()
		for base in self.basis:
			out.basis.append(k*base)
		return out
	
	def __imul__(self, k: Number) -> Matrix:
		"""Multiplies (the components of) the matrix by a scalar in place."""

		for i in range(len(self.basis)):
			self.basis[i] *= k

		return self
			
	def __rmul__(self, k: Number) -> Matrix:
		"""Multiplies (the components of) the matrix by a scalar
		when the scalar comes before the matrix."""
		out = Matrix()
		for base in self.basis:
			out.basis.append(k*base)
		return out

	def __matmul__(self, o: Vectoid) -> Vectoid:
		"""Matrix multiplies a Vector or a Matrix."""
		if isinstance(o, Vector):
			out = Vector([0 for _ in range(self.h())] )

			for i, base in enumerate(self.basis):
				for j, comp in enumerate(base.comps):
					out.comps[j] += comp*o.comps[i]
		else:
			out = Matrix()

			for base in o.basis:
				out.basis.append(self@base)
		
		return out

	def __imatmul__(self, o: Vectoid) -> Vectoid:
		raise NotImplementedError

	def __truediv__(self, k: Number) -> Matrix:
		"""Divides (the components of) the Matrix by a scalar."""
		return self*(1/k)
	
	def __itruediv__(self, k: Number) -> Matrix:
		"""Divides (the components of) the Matrix by a scalar in place."""
		self *= 1/k
		return self

	def __floordiv__(self, k: Number) -> Matrix:
		raise NotImplementedError

	def __ifloordiv__(self, k: Number) -> Matrix:
		raise NotImplementedError
