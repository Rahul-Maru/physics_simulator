from __future__ import annotations
from vector import Vectoid, Vector
from numbers import Number

class Matrix(Vectoid):
	def __init__(self, *args) -> None:
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
				self.basis = [Vector(1, 0), Vector(0, 1)] # identity matrix
				return


		self.basis = list(args)

	def __len__(self) -> int:
		return len(self.basis)
	
	def h(self) -> int:
		return len(self.basis[0])

	def __str__(self) -> str:
		s = "["
		for j in range(len(self.basis[0])):
			for i in range(len(self.basis)):
				s += f"{self.basis[i].comps[j]}, "
			s = s[:-2] + "]\n["
		
		return s[:-1]
	
	def __repr__(self) -> str:
		return super().__repr__() + f"|| {list(map(lambda v: repr(v), self.basis))}"
	
	def __neg__(self) -> Matrix:
		out = Matrix()
		for base in self.basis:
			out.basis.append(-base)
		return out

	def __add__(self, o: Matrix) -> Matrix:
		if len(self.basis) != len(o.basis) or len(self.basis[0].comps) != len(o.basis[0].comps):
			raise ArithmeticError("Matrices must be of same size to be added or subtracted")

		out = Matrix()
		for base, obase in zip(self.basis, o.basis):
			out.basis.append(base + obase)
		return out
	
	def __iadd__(self, o: Matrix) -> Matrix:
		if len(self.basis) != len(o.basis) or len(self.basis[0].comps) != len(o.basis[0].comps):
			raise ArithmeticError("Matrices must be of same size to be added or subtracted")
		
		for i, obase in enumerate(o.basis):
			self.basis[i] += obase
		return self

	def __sub__(self, o: Matrix) -> Matrix:
		return self + -o
	
	def __isub__(self, o: Matrix) -> Matrix:
		self += -o
		return self

	def __mul__(self, k: Number) -> Matrix:
		out = Matrix()
		for base in self.basis:
			out.basis.append(k*base)
		return out
	
	def __imul__(self, k: Number) -> Matrix:
		for i in range(len(self.basis)):
			self.basis[i] *= k

		return self
			
	def __rmul__(self, k: Number) -> Matrix:
		out = Matrix()
		for base in self.basis:
			out.basis.append(k*base)
		return out

	def __matmul__(self, o: Vectoid) -> Vectoid:
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
		pass

	def __truediv__(self, k: Number) -> Matrix:
		return self*(1/k)
	
	def __itruediv__(self, k: Number) -> Matrix:
		self *= 1/k
		return self
