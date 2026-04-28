import pygame as pg
from math import *
from random import *

from input import *
from entity import *
from game_state import *
from util.config import *


def game_loop(surface):

	quitting = False

	input		= Input({
		"zoom": (pg.K_l, pg.K_o),
	}, {
		"movement": (pg.K_LEFT, pg.K_RIGHT, pg.K_DOWN, pg.K_UP),
	})

	global game_state
	game_state	= GameState(surface, input)
	camera		= game_state.camera

	player_1	= Player(
		pos = (0, 0),
		im = GameImage(CONFIG.get_asset_path("standing.png")),
		cg_name = "Ally",
		input = input
	)

	bg = Entity(
		(0, 0),
		im = RepeatingImage(CONFIG.get_asset_path("hexagons.png"), 4)
	)
	game_state.add_entity(bg)

	camera.target = player_1

	game_state.add_entity(player_1)


	im = pg.transform.scale(pg.image.load(CONFIG.get_asset_path("laser.png")), (100, 20))

	cannons = []
	for i in range(0):
		cannons.append(game_state.add_entity(
			Cannon(
				pos = (1000*sin(i/4), 1000*cos(i/4)),
				im = GameImage(CONFIG.get_asset_path("standing.png")),
				proj_im = GameImage(im, 1),
				proj_speed = 1000,
				proj_dist = 100
			)
		))

	enemy = game_state.add_entity(Enemy(
		im = GameImage(CONFIG.get_asset_path("circle_FF0000.svg"), 1),
		target = player_1,
	))

	cannon = game_state.add_entity(AutoCannon(
			im = GameImage(CONFIG.get_asset_path("arrow.jpg"), 0.1),
			proj_im = GameImage(im, 1),
			proj_speed = 1000,
			proj_dist = 100,
			target = player_1,
	))

	cannon.mvt = enemy.mvt

	while not quitting:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quitting = True

		for cannon in cannons:
			x, y = (cannon.mvt.get_predicted_pos(player_1.mvt, cannon.projectile_speed) - cannon.get_pos())
			cannon.mvt.update_angle(atan2(y, x) + 0*uniform(-0.01, 0.01))

		game_state.tick(120)

		# Calcul de la nouvelle image
		game_state.draw()

		# Affichage
		pg.display.update()


if __name__ == "__main__":

	pg.init()

	# création de la fenêtre du jeu
	window = pg.display.set_mode(size=(800, 500))

	# nom de la fenêtre
	pg.display.set_caption("Premier jeu")

	game_loop(window)

	pg.quit()