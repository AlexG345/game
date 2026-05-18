from enum import IntFlag, auto
from util import math2

class CollisionGroup(IntFlag):
	ALLY			= auto()	# 1
	ENEMY			= auto()	# 2
	WEAPON_ALLY		= auto()	# 4
	WEAPON_ENEMY	= auto()	# 8
	

	
class CollisionHandler():

	def __init__(self):
		self.data = {}
		self.cgs = []

	# Assign a collision rule to a collision group, initiates an empty set of entities
	# Also updates the cgs attribute (list of collision groups)
	def create_data(self, collision_group: CollisionGroup, *mask_collision_groups):
		
		mask = 0
		for mask_collision_group in mask_collision_groups:
			mask |= mask_collision_group

		self.data[collision_group] = {
			"entities":	set(),
			"mask":		mask
		}

		self.cgs = self.data.keys()
	

	# Add an entity to a collision group, an entity should only be under one collision group
	def add_entity(self, collision_group: CollisionGroup, ent):
		self.data[collision_group]["entities"].add(ent)

	# Remove an entity from a collision group
	def remove_entity(self, collision_group: CollisionGroup, ent):
		self.data[collision_group]["entities"].remove(ent)

	# Try to make all the entities of a group collide with another
	def test_collisions(self, cg1, cg2):

		data1, data2 = self.data[cg1], self.data[cg2]

		collide1 = data1["mask"] & cg2 # first group initiates collisions
		collide2 = data2["mask"] & cg1 # second group initiates collisions

		if not ( collide1 or collide2 ):
			return

		for ent1 in data1["entities"]:
			for ent2 in data2["entities"]:

				if ent1 is ent2:
					continue

				if ent1.hitbox.collide(ent2.hitbox):
					ent1.health.change(-0.1)
					ent2.health.change(-0.1)


	def test_all_collisions(self):

		num_cgs = len(self.cgs)

		for i, cg1 in enumerate(self.cgs):
			for j, cg2 in enumerate(self.cgs, start=i):
				self.test_collisions(cg1, cg2)


	def tick(self):
		self.test_all_collisions()


class Hitbox():

	# parent should be an Entity (or related)
	def __init__(self, parent):
		self.parent = parent

	def get_pos(self):
		return self.parent.get_pos()

	def get_radius(self):
		return self.parent.radius

	def collide(self, other):
		return math2.circle_to_circle_2p(self.get_pos(), self.get_radius(), other.get_pos(), other.get_radius())
