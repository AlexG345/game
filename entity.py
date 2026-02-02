from input import *
from game_image import *
from ressource import *

class Entity:

	def __init__(self, x = 0, y = 0, im = "Ressources/bat1.png"):

		self.pos = pg.Vector2(x, y)
		self.speed = pg.Vector2()

		if isinstance(im, str):
			self.image = GameImage(im)
		else:
			self.image = im

		self.movement_speed = 250

	def move(self, direction, dt=1, speed = None):

		if speed is None:
			speed = self.movement_speed

		if direction.x != 0 or direction.y != 0:
			direction = direction.normalize()

		self.speed = self.speed.lerp(direction * speed, pg.math.clamp(2*dt, 0, 1))


	def tick(self, dt):
		self.pos += self.speed * dt


	def draw(self, surface, camera):
		self.image.draw(surface, self.pos, camera)


class Mortal(Entity):

	def __init__(self, x, y, im, health = 100):
		super().__init__(x, y, im)
		self.health = Ressource(health)


class Player(Mortal):

	def __init__(self, x, y, im, input):
		super().__init__(x, y, im)
		self.input = input


	def tick(self, dt):
		self.move(self.input.action_values["movement"], dt)
		super().tick(dt)


class Enemy(Mortal):

	# set target to None to stop targetting
	def __init__(self, x, y, im, target = None):
		super().__init__(x, y, im)
		self.target = target


	def follow(self, target = None):
		self.target = target


	def move_towards_target(self, dt):
		#t = pg.time.get_ticks()/1000
		#self.move(pg.Vector2(sin(3*t), 1), dt)
		if self.target != None:
			self.move(self.target.pos - self.pos, dt)


	def tick(self, dt):
		self.move_towards_target(dt)
		super().tick(dt)


# useless class
class FlyingEnemy(Enemy):

	def __init__(self, x, y, im, target):
		super().__init__(x, y, im, target)
		self.movement_speed = 100



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

# 			dpos = self.parent.pos - self.pos
# 			sq_dist = dpos.length_squared()

# 			if sq_dist > self.rest_distance ** 2:
# 				speed = self.movement_speed * sq_dist / (self.rest_distance ** 2)
# 				self.move(self.parent.pos - self.pos, dt * 10, speed)
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
# 			self.child = Snake(self.pos.x, self.pos.y, self.image, None, self.length - 1)
# 		else:
# 			self.child.add_segment()

# 	def is_head(self):
# 		return self.parent is None


# 	def is_tail(self):
# 		return self.child is None