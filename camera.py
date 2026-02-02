import pygame as pg

class Camera:

	def __init__(self,
		input,
		pos = pg.Vector2(),
		zoom = 1,
		center = pg.Vector2(),
		target = False
	):

		self.input = input
		self.pos = pos
		self.zoom = zoom
		self.center = center
		self.target = target
		self.offset = pg.Vector2()


	def smooth_zoom(self, mul, dt):
		if mul != 0:
			self.zoom *= 2 ** (mul * dt)


	# returns new vector
	def to_scr_pos(self, pos):
		return (pos - self.pos) * self.zoom + self.center
		#return pos - self.pos * self.zoom + self.center


	def to_scr_size(self, value):
		return value * self.zoom


	def tick(self, dt):
		zoomAmount = self.input.action_values["zoom"]

		doZoom = zoomAmount != 0
		if doZoom:
			self.smooth_zoom(zoomAmount, dt)

		self.offset = self.offset.lerp(
			# TODO: make mouse pos normalized relative to screen size
			(pg.mouse.get_pos() - self.center) * 0.2,
			pg.math.clamp(10 * dt, 0, 1)
		)
		if self.target != False:

			self.pos.update(self.target.pos + self.offset)

		return doZoom


	# draw image on surface after to_scr transforms
	def draw_image(self, surface, image, pos):
		surface.blit(image, self.to_scr_pos(pos))