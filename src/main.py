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

	bg = Entity(
		pos = (0, 0),
		im = RepeatingImage(CONFIG.get_asset_path("hexagons.png"), 4)
	)
	game_state.add_entity(bg)

	im = pg.transform.scale(pg.image.load(CONFIG.get_asset_path("Joueur/zeus_corps_dessus.png")), (100, 100))
	im = pg.transform.rotate(im, 180)
	player	= Player(
		pos				= (0, 0),
		im				= GameImage(im),
		collision_group	= CollisionGroup.ALLY,
		input			= input,
		movement_speed	= 600,
		radius			= 40,
	)
	game_state.add_entity(player)

	camera.target = player

	im = pg.transform.scale(pg.image.load(CONFIG.get_asset_path("monstres/hydre/hydre_corps.png")), (100, 100))
	im = pg.transform.rotate(im, 180)

	enemy = game_state.add_entity(Smart(
		im				= GameImage(im, 5),
		collision_group = CollisionGroup.ENEMY,
		target			= player,
		movement_speed	= 500,
		turn_speed		= 1,
		radius			= 200,
	))
	print(enemy.movement_speed)
	enemy.mvt.set_friction(1)

	im				= pg.transform.scale(pg.image.load(CONFIG.get_asset_path("monstres/hydre/hydre_tete.png")), (100, 100))
	neck_segment_im	= pg.transform.scale(pg.image.load(CONFIG.get_asset_path("monstres/hydre/hydre_cou.png")), (100, 100))
	proj_im			= pg.transform.scale(pg.image.load(CONFIG.get_asset_path("laser.png")), (100, 100))

	# IDEA: function to "heal" a neck segment until it regrows a head
	# to spawn the hydra just heal its segments
	# then have a cooldown that heals the segments while the hydra is alive?
	# + add smooth turn
	for i in range(-2, 3):
		root = enemy
		dx, dy = 200, 50 * i
		base_angle = i * pi/4
		for j in range(1, 7 - abs(i)):
			neck = game_state.add_entity(AutoCannon(
				pos				= (dx, dy),
				im				= GameImage(neck_segment_im, 3),
				target			= player,
				cooldown		= 1000000,
				turn_speed		= 0.1 * j,
				parent			= root
			))
			neck.mvt.parent = root.mvt
			neck.mvt.max_angle_amplitude = 0.15 + 0.2 * abs(i)
			neck.mvt.base_angle = base_angle

			root = neck
			dx, dy = 80, 0
			base_angle = 0

		cannon = game_state.add_entity(AutoCannon(
				pos				= (dx, 0),
				im				= GameImage(im, 2.5),
				proj_dist		= 100,
				proj_kwargs		= {
					"image"			: GameImage(proj_im),
					"movement_speed": 500,
					"lifetime"		: 100,
				},
				target			= player,
				cooldown		= 0.1,
				turn_speed		= 8,
				parent			= root
		))
		cannon.mvt.parent = root.mvt
		cannon.mvt.max_angle_amplitude = 0.4

	while not quitting:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				quitting = True

		game_state.tick(120)

		# Calcul de la nouvelle image
		game_state.draw()

		# Affichage
		pg.display.update()


if __name__ == "__main__":

	pg.init()

	# création de la fenêtre du jeu
	window = pg.display.set_mode(size=(1920, 1080))

	# nom de la fenêtre
	pg.display.set_caption("Premier jeu")

	game_loop(window)

	pg.quit()