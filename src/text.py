from __future__ import annotations

from consts import MID, pg, Vector, WINDOW_WIDTH, WINDOW_HEIGHT, T_SCALE, DAY, FPS, clock, v0
from colors import *


class TextEngine():
	def __init__(self) -> None:
		self.last_key = None

	def init_font(self) -> None:
		self.font = pg.font.SysFont(None, 16)
		print(RED)

		self.update_zoom(1.00)
		self.update_center(v0(2))
		self.update_momenta(0, v0(2), v0(2))

		self.pausetxt = self.font.render("PAUSED II", True, RED)
		self.quittxt = self.font.render("QUITTING... (press Esc again)", True, WHITE)
		self.FPSpos = (24, 20)

		tutorialtxt = "\n Esc ×2 — quit\n Space — pause\n Arrows — scroll\n C — center at origin\n" + \
			" Ctrl + b — center at barycenter\n +/= — zoom in\n - — zoom out\n Ctrl + 0 — reset zoom"
		self.tutorial = TextEngine.render_textrect(tutorialtxt, self.font, pg.Rect(0, 0, 124, 116), WHITE, BLACK)


	def update_zoom(self, zoom: float) -> None:
		self.ztxt = self.font.render(f"zoom: {zoom:.2f}x", True, ORANGE)
		self.zpos = (WINDOW_WIDTH - self.ztxt.get_width() - 24, WINDOW_HEIGHT - self.ztxt.get_height() - 20)

	def update_center(self, center: Vector):
		self.ctxt = self.font.render(f"{center:.2f}", True, ORANGE)
		self.cpos = (WINDOW_WIDTH - self.ctxt.get_width() - 24, self.zpos[1] - self.ctxt.get_height())

	def update_momenta(self, U: float, p: Vector, L: Vector) -> None:
		self.etxt = self.font.render(f"U: {U:.2E}", True, CYAN)
		self.ptxt = self.font.render(f"p: {p:.2E} ({p.mag():.2E})", True, CYAN)
		self.ltxt = self.font.render(f"L: {L.mag():.2E}", True, CYAN)

		self.lpos = (24, WINDOW_HEIGHT - self.ltxt.get_height() - 20)
		self.ppos = (24, self.lpos[1] - self.ptxt.get_height())
		self.epos = (24, self.ppos[1] - self.etxt.get_height())

	def render(self, screen: pg.Surface, t: float, pause: bool) -> None:
		# display the current simulation time
		ttxt = self.font.render(f"t = {t*T_SCALE/DAY:.0f} days", True, MAGENTA)

		if self.last_key == pg.K_ESCAPE:
			screen.blit(self.quittxt, self.FPSpos)
		else:
			if pause:
				screen.blit(self.pausetxt, self.FPSpos)
			else:
				# display the current fps
				current_fps = clock.get_fps()
				fpstxt = self.font.render(f"{round(current_fps, 0)} FPS", True, GREEN if current_fps >= FPS else RED)
				screen.blit(fpstxt, self.FPSpos)

		screen.blit(ttxt, (WINDOW_WIDTH - ttxt.get_width() - 24, 20))

		# display the current center of viewpoint and zoom
		screen.blit(self.ctxt, self.cpos)
		screen.blit(self.ztxt, self.zpos)
		screen.blit(self.etxt, self.epos)
		screen.blit(self.ptxt, self.ppos)
		screen.blit(self.ltxt, self.lpos)
		screen.blit(self.tutorial, (24, MID.x()-100))


	def render_textrect(string: str, font: pg.font.Font, rect: pg.Rect,
						text_color: tuple, background_color: tuple, justification:int[0, 1, 2] = 0):
		# code from: https://pygame.org/pcr/text_rect/index.php
		"""Returns a surface containing the passed text string, reformatted
		to fit within the given rect, word-wrapping as necessary. The text
		will be anti-aliased.

		Takes the following arguments:

		string - the text you wish to render. \n begins a new line.
		font - a Font object
		rect - a rectstyle giving the size of the surface requested.
		text_color - a three-byte tuple of the rgb value of the
					text color. ex (0, 0, 0) = BLACK
		background_color - a three-byte tuple of the rgb value of the surface.
		justification - 0 (default) left-justified
						1 horizontally centered
						2 right-justified

		Returns the following values:

		Success - a surface object with the text rendered onto it.
		Failure - raises a TextRectException if the text won't fit onto the surface.
		"""

		final_lines = []

		requested_lines = string.splitlines()

		# Create a series of lines that will fit on the provided
		# rectangle.

		for requested_line in requested_lines:
			if font.size(requested_line)[0] > rect.width:
				words = requested_line.split(' ')
				# if any of our words are too long to fit, return.
				for word in words:
					if font.size(word)[0] >= rect.width:
						raise TextRectException("The word " + word + " is too long to fit in the rect passed.")
				# Start a new line
				accumulated_line = ""
				for word in words:
					test_line = accumulated_line + word + " "
					# Build the line while the words fit.
					if font.size(test_line)[0] < rect.width:
						accumulated_line = test_line
					else:
						final_lines.append(accumulated_line) 
						accumulated_line = word + " " 
				final_lines.append(accumulated_line)
			else:
				final_lines.append(requested_line)

		# Let's try to write the text out on the surface.

		surface = pg.Surface(rect.size)
		surface.fill(background_color)

		accumulated_height = 0
		for line in final_lines:
			if accumulated_height + font.size(line)[1] >= rect.height:
				raise TextRectException("Once word-wrapped, the text string was too tall to fit in the rect.")
			if line != "":
				tempsurface = font.render(line, 1, text_color)
				if justification == 0:
					surface.blit(tempsurface, (0, accumulated_height))
				elif justification == 1:
					surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
				elif justification == 2:
					surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
				else:
					raise TextRectException("Invalid justification argument: " + str(justification))
			accumulated_height += font.size(line)[1]

		return surface


class TextRectException(BaseException):
	# code from: https://pygame.org/pcr/text_rect/index.php
    def __init__(self, message = None):
        self.message = message
    def __str__(self):
        return self.message

# text enginge
text_engine = TextEngine()
