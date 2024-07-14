from __future__ import annotations

from consts import pg, Vector, WINDOW_WIDTH, WINDOW_HEIGHT, T_SCALE, DAY, FPS, RED, ORANGE, GREEN, MAGENTA, clock

if __name__ != "__main__":
	print(__name__)

class TextObject():
	def __init__(self) -> None:
		pass

	def init_font(self) -> None:
		self.font = pg.font.SysFont(None, 14)
		print(RED)

		self.update_zoom(1.00)
		self.update_center(Vector(0, 0))

		self.ptxt = self.font.render("PAUSED II", True, RED)
		self.ppos = (24, 20)

	def update_zoom(self, zoom):
		self.ztxt = self.font.render(f"Q {zoom:.2f}x", True, ORANGE)
		self.zpos = (WINDOW_WIDTH - self.ztxt.get_width() - 24, WINDOW_HEIGHT - self.ztxt.get_height() - 20)

	def update_center(self, center):
		self.ctxt = self.font.render(f"{center:.2f}", True, ORANGE)
		self.cpos = (WINDOW_WIDTH - self.ctxt.get_width() - 24, WINDOW_HEIGHT - self.ctxt.get_height() - self.ztxt.get_height() - 20)

	def render(self, screen, t, p):
		# display the current simulation time
		ttxt = self.font.render(f"t = {t*T_SCALE/DAY:.0f} days", True, MAGENTA)

		if p:
			screen.blit(self.ptxt, self.ppos)
		else:
			# display the current fps
			current_fps = clock.get_fps()
			fpstxt = self.font.render(f"{round(current_fps, 0)} FPS", True, GREEN if current_fps >= FPS else RED)
			screen.blit(fpstxt, self.ppos) 

		screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))

		# display the current center of viewpoint and zoom
		screen.blit(self.ctxt, self.cpos)
		screen.blit(self.ztxt, self.zpos)

# text enginge
text_engine = TextObject()
