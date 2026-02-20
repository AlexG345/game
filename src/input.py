import pygame as pg


class Input:

	def __init__(self, tracked_input_scalars, tracked_input_vectors):
		self.tracked_input_scalars = tracked_input_scalars
		self.tracked_input_vectors = tracked_input_vectors
		self.action_values = {}
		self.tick()


	def get_scalar(self, keys):
		k = self.key_pressed
		return k[keys[1]] - k[keys[0]]


	def get_vector2(self, keys):
		k = self.key_pressed

		vec = pg.Vector2(k[keys[1]] - k[keys[0]], k[keys[3]] - k[keys[2]])

		if vec.x != 0 or vec.y != 0:
			vec.normalize_ip()

		return vec


	def tick(self):
		self.key_pressed = pg.key.get_pressed()

		tiv = self.tracked_input_vectors
		for action in tiv:
			self.action_values[action] = self.get_vector2(tiv[action])

		tis = self.tracked_input_scalars
		for action in tis:
			self.action_values[action] = self.get_scalar(tis[action])

