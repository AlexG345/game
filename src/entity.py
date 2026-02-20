from input import *
from game_image import *
from ressource import *
from movement_handler import *
from util.config import *
from math import *

class Entity:

	def __init__(self, pos = pg.Vector2(), im = None, **kwargs):

		self.mvt = MovementHandler()
		self.mvt.update_pos(pos)
		self.movement_speed = 250
		self.movement_rate = 5
		self.valid = True
		self.image = im

	def die(self):
		self.valid = False

	def set_image(self, im):
		self.image.set_image(im)

	def get_pos(self):
		return self.mvt.pos

	def move(self, direction, dt=1, speed = None):

		if speed is None:
			speed = self.movement_speed

		self.mvt.move(direction, dt, speed, self.movement_rate)

	def tick(self, dt):
		self.mvt.tick(dt)

	def draw(self, surface, camera):
		if self.image != None:
			self.image.draw(surface, self.get_pos(), camera)



class Mortal(Entity):

	def __init__(self, health = 100, **kwargs):
		super().__init__(**kwargs)
		self.health = Ressource(health)
		self.show_health = True

	def draw(self, surface, camera):
		super().draw(surface, camera)

		if self.show_health:
			pos = self.get_pos()
			x, y = pos.x, pos.y
			y -= self.image.image.get_height() * 0.75
			self.health.draw(surface, camera, x, y)


class Player(Mortal):

	def __init__(self, input, **kwargs):
		super().__init__(**kwargs)
		self.input = input
		self.movement_speed = 1000


	def tick(self, dt):
		self.move(self.input.action_values["movement"], dt)
		super().tick(dt)


class Enemy(Mortal):

	# set target to None to stop targetting
	def __init__(self, target = None, **kwargs):
		super().__init__(**kwargs)
		self.target = target


	def follow(self, target = None):
		self.target = target


	def move_towards_target(self, dt):
		if self.target != None:
			self.mvt.follow(self.target.mvt, dt, self.movement_speed, self.movement_rate, 1)


	def tick(self, dt):
		self.move_towards_target(dt)
		super().tick(dt)


# useless class
class FlyingEnemy(Enemy):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.movement_speed = 500


class Projectile(Mortal):

	def __init__(self, angle = 0, **kwargs):
		super().__init__(**kwargs)

		self.show_health = False

		self.movement_speed = 150
		self.lifetime = 3
		self.timeleft = self.lifetime

		self.mvt.update_angle(angle)
		self.mvt.update_velocity(self.mvt.direction * self.movement_speed)

	def tick(self, dt):
		super().tick(dt)

		self.timeleft -= dt
		self.image.rotate_image_rad(self.mvt.angle)

		if self.timeleft <= 0:
			self.die()


class Cannon(Entity):

	def __init__(self, proj_im = None, **kwargs):
		super().__init__(**kwargs)
		self.projectile_image = proj_im

	def tick(self, dt):
		super().tick(dt)

		CONFIG.game_state.add_entity(
			Projectile(
				pos = self.get_pos(),
				angle = self.mvt.angle,
				im = GameImage(self.projectile_image)
			)
		)






# class Snake(Enemy):

# 	def __init__(self, x, y, im, target, length = 0):
# 		super().__init__(x, y, im, target)

# 		self.rest_distance = 50

# 		if self.length > 0:
# 			self.child = Snake(x, y, None, None, self.length - 1)
# 			self.child.parent = self
# 		else:
# 			self.child = None

# 		if self.is_head():
# 			self.set_image(self.image)


# 	def draw(self, *args):
# 		if not self.is_tail():
# 			self.child.draw(*args)
# 		super().draw(*args)


# 	def tick(self, dt):

# 		if self.is_head():
# 			self.move_towards_target(dt)
# 		else:

# 			dpos = self.parent.pos - self.get_pos()
# 			sq_dist = dpos.length_squared()

# 			if sq_dist > self.rest_distance ** 2:
# 				speed = self.movement_speed * sq_dist / (self.rest_distance ** 2)
# 				self.move(self.parent.pos - self.get_pos(), dt * 10, speed)
# 			else:
# 				self.move(pg.Vector2(0, 0), dt * 50, self.movement_speed * 10)

# 		if not self.is_tail():
# 			self.child.tick(dt)

# 		super().tick(dt)



# # SnakeBase is just an Enemy that can have a child and a parent

# class SnakeBase(Enemy):

# 	def __init__(self, x, y, im, target, length = 0):

# 		super().__init__(x, y, im, target)
# 		self.length = length

# 		self.parent = None
# 		self.child = None

# 		self.add_segments(self, length)


# 	def set_image(self, im):
# 		self.image = im
# 		if not self.is_tail():
# 			self.child.set_image(im)


# 	def add_segments(self, length):
# 		if self.is_tail():
# 			self.child = Snake(self.get_pos().x, self.get_pos().y, self.image, None, self.length - 1)
# 		else:
# 			self.child.add_segment()

# 	def is_head(self):
# 		return self.parent is None


# 	def is_tail(self):
# 		return self.child is None