def point_to_circle(x1, y1, x2, y2, r):
	return (x1 - x2) ** 2 + (y1 - y2) ** 2 < r*r

def circle_to_circle(x1, y1, r1, x2, y2, r2):
	return (x1 - x2) ** 2 + (y1 - y2) ** 2 < (r1+r2)**2

def circle_to_circle_2p(p1, r1, p2, r2):
	return circle_to_circle(p1.x, p1.y, r1, p2.x, p2.y, r2)


class CollisionHandler():

	def __init__(self, entities = []):

		self.entities = entities

	def tick(self):
		for i, ent1 in enumerate(self.entities):
			for _, ent2 in enumerate(self.entities, i+1):
				if circle_to_circle_2p(ent1.get_pos(), 10, ent2.get_pos(), 10):
					ent1.die()
					ent2.die()