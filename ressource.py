class Ressource:

	def __init__(self, max):
		self.current = max
		self.max = max

	def set_max(self, max):
		self.max = max

	def set(self, current):
		self.current = current

	def get_relative(self):
		if self.max == 0:
			return 1
		return self.current / self.max