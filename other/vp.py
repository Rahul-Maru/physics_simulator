import vpython as vp
import numpy as np
from matplotlib import pyplot as plt
import math
from math import pi, e, sqrt, sin, cos, tan

k = 0.5
m = 1
sr = -2

dt = 0.5
tf = 15

def main():
	s0 = 1
	u = 0

	s = s0
	a = A(s0)
	v = u 
	v += a*dt/2

	tlist = []
	slist = []
	vlist = []
	alist = []

	for t in range(round(tf/dt)+1):
		print(f"{round(t*dt,4)} || {round(s, 5)} | {round(v, 5)} | {round(a, 5)}")
		tlist.append(t*dt)
		slist.append(s)
		vlist.append(v)
		alist.append(a)
		s += v*dt
		a = A(s)
		v += a*dt

	f = lambda t : (s0-sr)*cos(sqrt(k/m)*t) + sr
	n = np.linspace(start=0, stop=tf, num=100*tf)
	sx = list(map(f, n))
	# vx = list(map(lambda x : cos(x + pi/2), n))
	# ax = list(map(lambda x : -x, sx))

	sdiff = []
	# vdiff = []

	for t,s,v in zip(tlist, slist, vlist):
		sdiff.append(s-f(t))
		# vdiff.append(v-cos(t + pi/2))
	
	print(max(map(lambda x : abs(x), sdiff)), max(map(lambda x : abs(x), sdiff))/(dt*(s0-sr)))

	plt.axhline(0, 0, tf, color = "grey", linestyle="dashed")
	plt.axhline(sr, 0, tf, color = "maroon", linestyle="dashed")
	plt.plot(tlist, slist)
	plt.plot(tlist, vlist)
	# plt.plot(tlist, alist)
	plt.plot(n, sx, linestyle="dashed", color="blue")
	# plt.plot(n, vx, linestyle="dashed", color="orange")
	# plt.plot(n, ax, linestyle="dashed", color="green")
	plt.plot(tlist, sdiff, linestyle="dotted",  color="blue")
	# plt.plot(tlist, vdiff, linestyle="dotted",  color="orange")
	plt.legend(["0", "rest position", "s", "v", "s(exact)", "error - s"])
	plt.xlabel("t/s")
	plt.show()


def A(s):
	return -k*(s-sr) / m

if __name__ == "__main__":
	main()