from enum import IntFlag, auto
from util import math2

class CollisionGroup(IntFlag):
    PLAYER	= auto()	# 1
    ENEMY	= auto()	# 2


class CollisionRule():

	def __init__(self, *mask_cgs):

		self.mask = 0
		for mask_cg in mask_cgs:
			mask |= mask_cg

		self.entities = set()

	def add_entity(self, entity):
		self.entities.add(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)

	def test_collisions(self, other):

		collide1 = self.mask & other.layer # first group initiates collision
		collide2 = other.mask & self.layer # second group initiates collision

		if not ( collide1 or collide2 ):
			return

		for ent1 in self.entities:
			for ent2 in other.entities:

				if ent1 is ent2:
					continue

				if ent1.hitbox.collide(ent2.hitbox):
					ent1.health.change(-1)
					ent2.health.change(-1)


class CollisionHandler():

	def __init__(self):
		self.groups = {}

	def create_group(self, cg: CollisionGroup, cr: CollisionRule):
		self.groups[cg] = {
			"entities": set(),
			"rule": cr
		}

	def add_entity(self, cg: CollisionGroup, ent):
		self.groups[cg].entities.add(ent)

	def remove_entity(self, cg: CollisionGroup, ent):
		self.groups[cg].entities.remove(ent)

	def test_collisions(self, cg1, cg2):

		rule1 = self.groups[cg1].rule
		rule1 = self.groups[cg2].rule

		collide1 = self.mask & other.layer # first group initiates collision
		collide2 = other.mask & self.layer # second group initiates collision

		if not ( collide1 or collide2 ):
			return

		for ent1 in self.entities:
			for ent2 in other.entities:

				if ent1 is ent2:
					continue

				if ent1.hitbox.collide(ent2.hitbox):
					ent1.health.change(-1)
					ent2.health.change(-1)


	def test_collisions(self):

		num_groups = len(self.groups)

		for i in range(num_groups):
			for j in range(i, num_groups):

				self.rules[i].test_collisions(self.groups[j])



	def tick(self):
		self.test_collisions()


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
