import pygame as pg
from math import *
from util import math2

class MovementHandler:

	def __init__(self):
		# vectors
		self.pos = pg.Vector2()
		self.velocity = pg.Vector2()
		self.acceleration = pg.Vector2()
		self.angle = 0
		self.velocity_conservation = 0.02
		self.direction = pg.Vector2(cos(self.angle), sin(self.angle))
		self.parent = None
		self.max_angle_amplitude = pi

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
		angle = math2.clamp( math2.simplify_angle(angle), -self.max_angle_amplitude, self.max_angle_amplitude )
		if angle != self.angle:
			self.angle = angle
			self.direction.update(cos(self.angle), sin(self.angle))

	def turn_towards_angle(self, angle, angular_velocity, dt):
		angle_to = math2.simplify_angle(angle - self.get_world_angle())
		d_ang = angular_velocity * dt * ((angle_to > 0) - (angle_to < 0))
		if abs(d_ang) > abs(angle_to):
			self.update_angle(self.angle + angle_to)
		else:
			self.update_angle(self.angle + d_ang)

	def turn_towards_pos(self, pos, angular_velocity, dt):
		x, y = pos - self.get_world_pos()
		angle = atan2(y, x)
		self.turn_towards_angle(angle, angular_velocity, dt)
		return angle

	def get_speed(self):
		return self.velocity.length()

	# the functions below are VERY unoptimized, everything is recalculated at each call
	def get_world_pos(self):
		if self.parent is not None:
			return self.parent.get_world_pos() + self.pos.rotate_rad(self.parent.get_world_angle())
		return self.pos # not a copy

	def get_world_velocity(self):
		if self.parent is not None:
			return self.parent.get_world_velocity() + self.velocity.rotate_rad_ip(self.parent.get_world_angle())
		return self.velocity # not a copy

	def get_world_angle(self):
		if self.parent is not None:
			return self.parent.get_world_angle() + self.angle
		return self.angle



	# get the position at which this mvt handler would reach another mvt handler, assuming no acceleration
	"""
	Arguments:
		other (MovementHandler): The tracked movement handler
		reach_speed (number): The speed at which we're trying to reach the tracked movement handler
		base_dist (number): The distance to the tracked movement handler that has already been crossed (useful for projectiles: they're shot farther away than the center of the cannon)

	Returns:
		(pg.Vector2): The position at which the tracked movement handler will be intercepted, or a fallback position if it's impossible to do so
		(boolean): True if the tracked movement handler can be intercepted
	"""
	def get_predicted_pos(self, other, reach_speed, base_dist = 0):

		# details on https://docs.google.com/document/d/1soAWMD52LqHPScC6zSZgSGo-leN_NFqEhkB0M1yvOAM/edit?tab=t.0
		# idea originally from https://www.reddit.com/r/gamedev/comments/16ceki/comment/c7vbu2j/

		rA0 = base_dist
		vR = reach_speed # scalar
		vB = other.get_world_velocity()
		pB0 = other.get_world_pos()
		pA0 = self.get_world_pos()
		dPos = pB0 - pA0

		# We solve for the time when a circle growing at the projectile's speed intersects with the target's trajectory.
		# It leads to a quadratic equation: At² + Bt + C = 0
		# It's hard to find a "physical" meaning for the values below.

		A = vB.x ** 2 + vB.y ** 2 - vR ** 2
		B = 2 * vB * dPos - vR * rA0
		C = dPos * dPos - rA0 ** 2

		delta = B * B - 4 * A * C

		if delta < 0:
			return pB0, False

		root_delta = sqrt(delta)

		t1 = (B + root_delta) / (- 2 * A)
		t2 = (- B + root_delta) / (2 * A)
		tmin = min(t1, t2)
		tmax = max(t1, t2)

		if tmax < 0:
			return pB0, False

		t = tmax
		if tmin >= 0:
			t = tmin

		return pB0 + t * vB, True


	def move(self, direction, max_speed):
		self.acceleration = direction * max_speed * -log(self.velocity_conservation)

	def move_forwards(self, max_speed):
		self.move(self.direction, max_speed)

	# does not work properly for parented mvts (except if self and other are parented to the same mvt)
	def follow(self, other, max_speed, prediction_precision = 1):

		direction = other.pos.lerp(self.get_predicted_pos(other, max_speed)[0], prediction_precision) - self.pos

		if direction.x == 0 and direction.y == 0:
			return

		direction.normalize_ip()
		print(direction, max_speed)
		self.move(direction, max_speed)



	def tick(self, dt):
		self.velocity	+= self.acceleration * dt
		self.pos		+= self.velocity * dt

		self.velocity	*= self.velocity_conservation ** dt

		self.update_acceleration((0, 0))
