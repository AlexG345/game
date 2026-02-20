import pygame as pg

class Ressource:

	def __init__(self, max):
		self.current = max
		self.max = max

	def set_max(self, max):
		self.max = max

	def set(self, current):
		self.current = current

	def fill(self):
		self.current = self.max

	def change(self, amount):
		self.current += amount

	def get_relative(self):
		if self.max == 0:
			return 1
		return self.current / self.max

	def get_relative_clamped(self):
		return pg.math.clamp(self.get_relative(), 0, 1)

	def set_relative(self, rel):
		self.current = rel * self.max

	def draw(self, surface, camera, x, y):

		relative = self.get_relative_clamped()

		mp = camera.to_scr_pos((x, y))
		w = camera.to_scr_size(50)
		h = round(camera.to_scr_size(10))
		y = mp.y + h/2
		x1 = mp.x - w/2
		x2 = x1 + relative * w
		x3 = x1 + w

		if relative > 0:
			pg.draw.line(
				surface,
				(255, 0, 0),
				(x1, y),
				(x2, y),
				h
			)

		if relative < 1:
			pg.draw.line(
				surface,
				(0, 0, 0),
				(x2, y),
				(x3, y),
				h
			)

