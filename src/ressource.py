class Ressource:

	def __init__(self, max):
		self.current = max
		self.max = max

	def set_max(self, max):
		self.max = max

	def set(self, current):
		self.current = current

	def fill(self):
		self.current = self.max

	def change(self, amount):
		self.current += amount

	def get_relative(self):
		if self.max == 0:
			return 1
		return self.current / self.max

	def set_relative(self, rel):
		self.current = rel * self.max


