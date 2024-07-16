# import vpython as vp
import numpy as np
from matplotlib import pyplot as plt
from math import sqrt, cos

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

def plot(xdata: tuple, *ydatalist) -> None:
	"""
	Plots the given data. Takes in one set of x data (independent variable)
	and multiple sets of y data (dependent variables) and plots line graphs.

	Parameters
	----------
		xdata : tuple [(data, label)]
			data : list
				A list of the x components of the data points to be plotted.
			label : str
				The label for the x-axis.
		*ydatalist : tuple [(data, legend, style)]
			data : list
				A list of the y components of the data points to be plotted.
			legend : str
				The label for this set of data on the legend.
			style : Iterable
				The style to apply on the plot (optional).
	"""

	# plots the line y = 0
	plt.axhline(0, 0, tf, color = "grey", linestyle="dashed")

	xlist = xdata[0]

	# list containing the text for the legend
	legend = ["0"]
	for ydata in ydatalist:
		if len(ydata) == 1:
			# plot the data
			plt.plot(xlist, ydata[0])
			legend.append("")
		elif len(ydata) == 2:
			# plot the data and put text in the legend
			plt.plot(xlist, ydata[0])
			legend.append(ydata[1])
		else:
			# plot the data with a certain style
			plt.plot(xlist, ydata[0], *ydata[2])
			legend.append(ydata[1])

	plt.xlabel(xdata[1])
	plt.legend(legend)

	plt.show()




def A(s):
	return -k*(s-sr) / m

if __name__ == "__main__":
	main()