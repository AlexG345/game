import pygame as pg
from camera import *
from util.config import *
from collision import *

class GameState:

	def __init__(self,
			window,
			input,
		):

		self.window = window
		self.input = input
		self.clock = pg.time.Clock()
		self.time = 0
		self.camera = Camera(self.input, center = pg.Vector2(self.window.get_size()) / 2)
		self.entities = []

		cgAlly = CollisionGroup()
		cgEnemy = CollisionGroup()
		cgAlly.set_mask({cgEnemy})
		cgEnemy.set_mask({cgAlly})
		self.collision_handler = CollisionHandler(
			{
				"Ally": cgAlly,
				"Enemy": cgEnemy,
			}
		)

		self.color_bg = pg.Color(0, 0, 0)

		CONFIG.game_state = self

	def set_named_entity(self, ent, name):
		self.player = ent

	def get_player(self):
		return self.player

	def add_entity(self, ent):
		if ent not in self.entities:
			self.entities.append(ent)
			ent.image.update_image(self.camera)
		return ent

	def tick(self, max_fps):

		self.input.tick()

		dt = self.clock.tick(max_fps)/1000
		self.time += dt

		for ent in self.entities:
			ent.tick(dt)

		self.collision_handler.tick()

		self.entities = [ent for ent in self.entities if ent.valid]

		doZoom = self.camera.tick(dt)
		if doZoom:
			for ent in self.entities:
				ent.image.update_image(self.camera)

		return dt


	def draw(self):
		self.window.fill(self.color_bg)
		for ent in self.entities:
			ent.draw(self.window, self.camera)

