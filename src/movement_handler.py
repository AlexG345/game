import pygame as pg
from math import *

class MovementHandler:

	def __init__(self):
		# vectors
		self.pos = pg.Vector2()
		self.velocity = pg.Vector2()
		self.acceleration = pg.Vector2()
		self.angle = 0
		self.velocity_conservation = 0.02
		self.direction = pg.Vector2(cos(self.angle), sin(self.angle))

		# scalars
		# self.speed = 250
		# self.rate = 0.1

	def set_friction(self, friction):
		self.velocity_conservation = 1 / (friction + 1)

	def get_friction(self):
		return (1 / self.velocity_conservation) - 1

	def update_pos(self, *args):
		self.pos.update(*args)

	def update_velocity(self, *args):
		self.velocity.update(*args)

	def update_acceleration(self, *args):
		self.acceleration.update(*args)

	def update_angle(self, angle):
		if angle != self.angle:
			self.angle = angle
			self.direction.update(cos(self.angle), sin(self.angle))

	def turn_towards_angle(self, angle, angular_velocity, dt):
		ang = ((angle - self.angle) + pi) % (2 * pi) - pi
		d_ang = angular_velocity * dt * ((ang > 0) - (ang < 0))
		if abs(d_ang) > abs(ang):
			self.update_angle(angle)
		else:
			self.update_angle(self.angle + d_ang)

	def get_speed(self):
		return self.velocity.length()


	def get_predicted_pos(self, other, reach_speed, base_dist = 0):

		# details on https://docs.google.com/document/d/1soAWMD52LqHPScC6zSZgSGo-leN_NFqEhkB0M1yvOAM/edit?tab=t.0
		# idea originally from https://www.reddit.com/r/gamedev/comments/16ceki/comment/c7vbu2j/

		rA0 = base_dist
		vR = reach_speed # scalar
		vB = other.velocity
		pB0 = other.pos
		pA0 = self.pos
		dPos = pB0 - pA0

		# We solve for the time when a circle growing at the projectile's speed intersects with the target's trajectory.
		# It leads to a quadratic equation: At² + Bt + C = 0
		# It's hard to find a "physical" meaning for the values below.

		A = vB.x ** 2 + vB.y ** 2 - vR ** 2
		B = 2 * vB * dPos - vR * rA0
		C = dPos * dPos - rA0 ** 2

		delta = B * B - 4 * A * C

		if delta < 0:
			return other.pos

		root_delta = sqrt(delta)

		t1 = (B + root_delta) / (- 2 * A)
		t2 = (- B + root_delta) / (2 * A)
		tmin = min(t1, t2)
		tmax = max(t1, t2)

		if tmax < 0:
			return other.pos

		t = tmax
		if tmin >= 0:
			t = tmin

		return other.pos + t * other.velocity


	def move(self, direction, max_speed):

		self.acceleration = direction * max_speed * -log(self.velocity_conservation)

	# def move(self, direction, dt=1, speed = 0, rate = 1):

	# 	if direction.x != 0 or direction.y != 0:
	# 		direction = direction.normalize()

	# 	self.velocity = self.velocity.lerp(direction * speed, pg.math.clamp(rate * dt, 0, 1))


	# def follow(self, other, dt, speed, rate = 1, precision=1):

	# 	direction = other.pos.lerp(self.get_predicted_pos(other, speed), precision) - self.pos

	# 	self.move(direction, dt, speed, rate)

	def follow(self, other, max_speed, prediction_precision = 1):
		direction = other.pos.lerp(self.get_predicted_pos(other, max_speed), prediction_precision) - self.pos
		self.move(direction, max_speed)



	def tick(self, dt):
		self.velocity += self.acceleration * dt
		self.pos += self.velocity * dt

		self.velocity *= self.velocity_conservation ** dt

		self.update_acceleration((0, 0))
