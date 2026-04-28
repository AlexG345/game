from util import math2


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


class CollisionHandler():

	def __init__(self, groups = {}):
		self.groups = groups

	def tick(self):
		# an ENTITY can ONLY have ONE collision group

		#print("---------------")

		for k1 in self.groups:
			cg1 = self.groups[k1]
			for k2 in self.groups:
				cg2 = self.groups[k2]

				#print(k1, len(cg1.entities), k2, len(cg2.entities))

				if not (cg2 in cg1.mask and cg1 in cg2.mask):
					continue

				#print(" collides")

				for ent1 in cg1.entities:
					for ent2 in cg2.entities:

						# TODO: save ent1 and ent2 collision result in case it's used again?
						if not ent1.hitbox.collide(ent2.hitbox):
							continue

						ent1.health.change(-1)
						ent2.health.change(-1)

class CollisionGroup():

	def __init__(self):
		self.mask = set()
		self.entities = set()

	# mask: { colgroup1, colgroup2, etc... }
	def set_mask(self, mask):
		self.mask = mask

	def add_entity(self, entity):
		self.entities.add(entity)

	def remove_entity(self, entity):
		self.entities.remove(entity)