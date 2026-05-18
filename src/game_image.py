import pygame as pg
from math import *

class GameImage:

	def __init__(self, im, base_scale = 1):
		self.angle = 0
		self.base_scale = base_scale
		self.scale = base_scale
		self.set_image(im)

	# TODO: add missing texture if im is None?
	def set_image(self, im = None):

		if isinstance(im, GameImage):
			self.image = im.image.copy()
			self.base_scale = im.base_scale
		elif isinstance(im, pg.surface.Surface):
			self.image = im.copy()
		else:
			self.image = pg.image.load(im)

		self.image = self.image.convert_alpha()
		self.image_scaled = self.image.copy().convert_alpha()
		self.update_center()

	def get_size(self):
		return self.image_scaled.get_size()

	def update_center(self):
		self.center = pg.Vector2(self.image_scaled.get_size())/2

	def update_image(self, camera):
		self.rotozoom_image(self.angle, camera.zoom)

	# does not set self.scale and self.angle
	def rotate_scale_image_noset(self, angle, scale):
		self.image_scaled = pg.transform.rotozoom(self.image, angle, self.base_scale * scale)
		self.update_center()

	def rotate_scale_image(self, angle, scale):
		if scale != self.scale or angle != self.angle:
			self.scale = scale
			self.angle = angle
			self.rotate_scale_image_noset(angle, scale)

	def scale_image(self, scale):
		if scale != self.scale:
			self.scale = scale
			self.rotate_scale_image_noset(self.angle, scale)

	def rotate_image(self, angle):
		if angle != self.angle:
			self.angle = angle
			self.rotate_scale_image_noset(angle, self.scale)

	def rotate_image_rad(self, angle):
		self.rotate_image(180 * angle / pi)

	def update_image(self, camera):
		self.scale_image(camera.zoom)

	def draw(self, surface, pos, camera):
		surface.blit(self.image_scaled, camera.to_scr_pos(pos) - self.center)



class RepeatingImage:

	def __init__(self, im, base_scale = 1):

		self.image = pg.image.load(im).convert_alpha()

		self.base_scale = base_scale
		self.image_scaled = pg.transform.scale_by(self.image, self.base_scale)

		self.repeat = pg.Vector2(10, 10)
		self.center = pg.Vector2()

		self.update_center()

	def update_image(self, camera):
		self.image_scaled = pg.transform.scale_by(self.image, self.base_scale * camera.zoom)
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