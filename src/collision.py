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


class CollisionHandler():

	def __init__(self):
		self.rules = {}

	def associate_rule(self, cg: CollisionGroup, cr: CollisionRule):
		self.rules[cg] = cr

	def tick(self):

		num_rules = len(self.rules)

		for i in range(num_rules):
			for j in range(i, num_rules):
				rule1 = self.rules[i]
				rule2 = self.rules[j]

				if rule1.mask & rule2.layer:
					pass

				if rule2.mask & rule1.layer:
					pass

class Hitbox():

	# parent should be an Entity (or related)
	def __init__(self, parent):
		self.parent = parent

	def get_pos(self):
		return self.parent.get_pos()

	def get_radius(self):
		return self.parent.radius

	def collide(self, hitbox):
		return math2.circle_to_circle_2p(self.get_pos(), self.get_radius(), hitbox.get_pos(), hitbox.get_radius())