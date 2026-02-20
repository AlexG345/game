import pygame as pg
from math import *

class MovementHandler:

	def __init__(self):
		# vectors
		self.pos = pg.Vector2()
		self.velocity = pg.Vector2()
		self.direction = pg.Vector2()
		self.angle = 0

		# scalars
		# self.speed = 250
		# self.rate = 0.1

	def update_pos(self, *args):
		self.pos.update(*args)

	def update_velocity(self, *args):
		self.velocity.update(*args)

	def update_angle(self, angle):
		if angle != self.angle:
			self.angle = angle
			self.direction.update(cos(self.angle), sin(self.angle))

	def get_speed(self):
		return self.velocity.length()


	def get_predicted_pos(self, other, reach_speed):
		dpos = other.pos - self.pos
		return other.pos + other.velocity * (dpos.length() / reach_speed)


	def move(self, direction, dt=1, speed = 0, rate = 1):

		if direction.x != 0 or direction.y != 0:
			direction = direction.normalize()

		self.velocity = self.velocity.lerp(direction * speed, pg.math.clamp(rate * dt, 0, 1))


	def follow(self, other, dt, speed, rate = 1, precision=1):

		direction = other.pos.lerp(self.get_predicted_pos(other, speed), precision) - self.pos

		self.move(direction, dt, speed, rate)


	def tick(self, dt):
		self.pos += self.velocity * dt
