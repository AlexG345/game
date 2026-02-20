import pygame as pg

from entity import *


class Camera(Entity):

	def __init__(self,
		input,
		pos = pg.Vector2(),
		zoom = 1,
		center = pg.Vector2(),
		target = None
	):

		super().__init__(pos)
		self.input = input
		self.zoom = zoom
		self.center = center
		self.target = target
		self.offset = pg.Vector2()


	def smooth_zoom(self, mul, dt):
		if mul != 0:
			self.zoom *= 2 ** (mul * dt)


	def to_scr_size(self, value):
		return value * self.zoom

	# returns new vector
	def to_scr_pos(self, pos):
		vec = pos - self.get_pos()
		vec.y *= -1
		return vec * self.zoom + self.center

	def to_world_pos(self, pos):
		pos = (pos - self.center) / self.zoom
		pos.y *= -1
		return pos + self.get_pos()


	def tick(self, dt):
		zoomAmount = self.input.action_values["zoom"]

		doZoom = zoomAmount != 0
		if doZoom:
			self.smooth_zoom(zoomAmount, dt)

		self.offset = self.offset.lerp(
			# TODO: make mouse pos normalized relative to screen size
			(self.to_world_pos(pg.mouse.get_pos()) - self.get_pos()) * 0.2,
			pg.math.clamp(10 * dt, 0, 1)
		)

		if self.target != None:
			self.mvt.update_pos(self.target.get_pos() + self.offset)

		return doZoom


	# draw image on surface after to_scr transforms
	def draw_image(self, surface, image, pos):
		surface.blit(image, self.to_scr_pos(pos))