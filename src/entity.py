from input import *
from game_image import *
from ressource import *
from movement_handler import *
from util.config import *
from math import *
from collision import *

class Entity:

	def __init__(
		self,
		pos				= pg.Vector2(),
		radius			= 10,
		im				= None,
		collision_group = None, # None or a CollisionGroup enum
		movement_speed	= 10,
		**kwargs
	):
		self.mvt = MovementHandler()
		self.mvt.update_pos(pos)
		self.movement_speed	= movement_speed
		self.movement_rate	= 5
		self.valid	= True
		self.image	= im
		self.radius	= radius

		self.hitbox	= Hitbox(parent = self)

		self.collision_group = None
		self.set_collision_group(collision_group)

	def set_collision_group(self, collision_group: CollisionGroup):
		self.clear_collision_group()

		if collision_group is not None:
			CONFIG.game_state.collision_handler.add_entity(collision_group, self)
			self.collision_group = collision_group

	def clear_collision_group(self):
		if self.collision_group is not None:
			CONFIG.game_state.collision_handler.remove_entity(self.collision_group, self)
			self.collision_group = None


	def die(self):
		self.clear_collision_group()
		self.valid = False

	def set_image(self, im):
		self.image.set_image(im)

	def get_pos(self):
		return self.mvt.get_world_pos()

	def move(self, direction, max_speed = None):

		if max_speed is None:
			max_speed = self.movement_speed

		self.mvt.move(direction, max_speed)


	def tick(self, dt):
		x, y = self.mvt.pos.x, self.mvt.pos.y
		self.mvt.tick(dt)
		print(self.__class__, (self.mvt.pos - (x, y)).length()/dt)

	def draw(self, surface, camera):
		if self.image is not None:
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
			y -= self.radius * 1.5
			self.health.draw(surface, camera, x, y)

	def tick(self, dt):
		super().tick(dt)
		if self.health.current < 0:
			self.die()


class Player(Mortal):

	def __init__(self, input, **kwargs):
		super().__init__(**kwargs)
		self.input = input


	def tick(self, dt):
		
		self.move(self.input.action_values["movement"]) # action values vector is already normalized
		
		super().tick(dt)


class Enemy(Mortal):

	# set target to None to stop targetting
	def __init__(self, target = None, **kwargs):
		super().__init__(**kwargs)
		self.target = target


	def follow(self, target = None):
		self.target = target


	def move_towards_target(self, dt):
		if self.target is not None:
			self.mvt.follow(self.target.mvt, self.movement_speed)


	def tick(self, dt):
		self.move_towards_target(dt)
		super().tick(dt)



class Projectile(Mortal):

	def __init__(self, angle = 0, lifetime = 3, **kwargs):
		super().__init__(**kwargs)

		self.health.current = 1
		self.show_health = False

		self.lifetime = lifetime
		self.timeleft = self.lifetime

		self.mvt.update_angle(angle)
		self.mvt.update_velocity(self.mvt.direction * self.movement_speed)

	def tick(self, dt):

		self.mvt.update_velocity(self.mvt.direction * self.movement_speed)
		super().tick(dt)

		self.timeleft -= dt
		self.image.rotate_image_rad(self.mvt.angle)

		if self.timeleft <= 0:
			self.die()


class Cannon(Entity):

	def __init__(self, proj_im = None, proj_speed = 50, proj_dist = 0, **kwargs):
		super().__init__(**kwargs)
		self.projectile_distance = proj_dist
		self.projectile_image = proj_im
		self.projectile_speed = proj_speed

		self.cooldown = 0.01
		self.timeleft = self.cooldown

	def tick(self, dt):
		super().tick(dt)

		angle = self.mvt.get_world_angle()

		self.timeleft -= dt
		self.image.rotate_image_rad(angle)

		if self.timeleft <= 0:
			self.timeleft = self.cooldown

			direction	= pg.Vector2(cos(angle), sin(angle))

			CONFIG.game_state.add_entity(
				Projectile(
					pos				= self.get_pos() + direction * self.projectile_distance,
					angle			= angle,
					collision_group	= CollisionGroup.ENEMY,
					im				= GameImage(self.projectile_image),
					movement_speed	= self.projectile_speed,
				)
			)


class AutoCannon(Cannon):

	def __init__(self, target = None, **kwargs):
		super().__init__(**kwargs)
		self.target = target

	def tick(self, dt):
		if self.target is not None:
			x, y = (self.mvt.get_predicted_pos(self.target.mvt, self.projectile_speed) - self.get_pos())
			self.mvt.turn_towards_angle(atan2(y, x), 1, dt)
		#self.mvt.update_angle(atan2(y, x))#"+ uniform(-0.01, 0.01))
		super().tick(dt)