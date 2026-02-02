import pygame as pg
from camera import *
from math import *

class GameImage:

	def __init__(self, im):
		self.image = pg.image.load(im).convert_alpha()
		self.image_scaled = pg.image.load(im).convert_alpha()
		self.update_center()

	def update_center(self):
		self.center = pg.Vector2(self.image_scaled.get_size())/2

	def update_image(self, camera):
		self.image_scaled = pg.transform.scale_by(self.image, camera.zoom)
		self.update_center()

	def draw(self, surface, pos, camera):
		surface.blit(self.image_scaled, camera.to_scr_pos(pos) - self.center)


class RepeatingImage:

	def __init__(self, im):
		self.image = pg.image.load(im).convert_alpha()
		self.image_scaled = pg.image.load(im).convert_alpha()
		self.repeat = pg.Vector2(10, 10)
		self.center = pg.Vector2()
		self.update_center()

	def update_image(self, camera):
		self.image_scaled = pg.transform.scale_by(self.image, camera.zoom)
		self.update_center()

	def update_center(self):
		self.center = self.get_size() / 2

	def get_size(self):
		size = pg.Vector2(self.image_scaled.get_size())
		size.x *= self.repeat.x
		size.y *= self.repeat.y
		return size

	def draw(self, surface, pos, camera):
		# use size from the scaled image to prevent position errors
		dims = self.image_scaled.get_size()
		cur_pos = pg.Vector2()
		for x in range(floor(self.repeat.x)):
			cur_pos.x = dims[0] * x
			for y in range(floor(self.repeat.y)):
				cur_pos.y = dims[1] * y
				surface.blit(self.image_scaled, camera.to_scr_pos(pos) + cur_pos - self.center)