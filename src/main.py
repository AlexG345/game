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
		image = RepeatingImage(CONFIG.get_asset_path("background_grass.jpg"), 2)
	)
	game_state.add_entity(bg)

	image = pg.transform.scale(pg.image.load(CONFIG.get_asset_path("Joueur/zeus_corps_dessus.png")), (100, 100))
	image = pg.transform.rotate(image, 180)
	player	= Player(
		pos				= (0, 0),
		image			= GameImage(image),
		collision_group	= CollisionGroup.ALLY,
		input			= input,
		movement_speed	= 600,
		radius			= 40,
	)
	game_state.add_entity(player)

	camera.target = player

	image = pg.transform.scale(pg.image.load(CONFIG.get_asset_path("monstres/hydre/hydre_corps.png")), (100, 100))
	image = pg.transform.rotate(image, 180)

	enemy = game_state.add_entity(Smart(
		image			= GameImage(image, 5),
		collision_group = CollisionGroup.ENEMY,
		target			= player,
		movement_speed	= 500,
		turn_speed		= 1,
		radius			= 200,
	))
	print(enemy.movement_speed)
	enemy.mvt.set_friction(1)

	image				= pg.transform.scale(pg.image.load(CONFIG.get_asset_path("monstres/hydre/hydre_tete.png")), (100, 100))
	tail_segment_image	= pg.transform.scale(pg.image.load(CONFIG.get_asset_path("monstres/hydre/hydre_segment_queue.png")), (100, 100))
	seg_segment_image	= pg.transform.scale(pg.image.load(CONFIG.get_asset_path("monstres/hydre/hydre_cou.png")), (100, 100))
	proj_image			= pg.transform.scale(pg.image.load(CONFIG.get_asset_path("laser.png")), (100, 100))

	# IDEA: function to "heal" a seg segment until it regrows a head
	# to spawn the hydra just heal its segments
	# then have a cooldown that heals the segments while the hydra is alive?
	# + add smooth turn

	for i in range(2):
		root = enemy
		t = (2 * i - 1)
		dx, dy = -200, 40 * t
		base_angle = t * pi / 6
		for j in range(1, 6):
			seg = game_state.add_entity(AutoCannon(
				pos				= (dx, dy),
				image			= GameImage(seg_segment_image, 3 - 0.2 * j),
				target			= player,
				spawn_cooldown	= inf,
				turn_speed		= 0.1 * j,
				parent			= root
			))
			seg.mvt.parent = root.mvt
			seg.mvt.max_angle_amplitude = 0.15 + 0.2 * j
			seg.mvt.base_angle = base_angle

			root = seg
			dx, dy = -80, 0
			base_angle = 0	

	for i in range(-2, 3):
		root = enemy
		dx, dy = 200, 50 * i
		base_angle = i * pi/4
		for j in range(1, 7 - abs(i)):
			seg = game_state.add_entity(AutoCannon(
				pos				= (dx, dy),
				image			= GameImage(seg_segment_image, 3),
				target			= player,
				spawn_cooldown	= inf,
				turn_speed		= 0.1 * j,
				parent			= root
			))
			seg.mvt.parent = root.mvt
			seg.mvt.max_angle_amplitude = 0.15 + 0.2 * abs(i)
			seg.mvt.base_angle = base_angle

			root		= seg
			dx, dy		= 80, 0
			base_angle	= 0

		cannon = game_state.add_entity(AutoCannon(
				pos				= (dx, 0),
				image			= GameImage(image, 2.5),
				spawn_distance	= 100,
				spawn_kwargs	= {
					"image"				: GameImage(proj_image),
					"movement_speed"	: 600,
					"lifetime"			: 1,
					"collision_group"	: CollisionGroup.WEAPON_ENEMY,
				},
			
				target			= player,
				spawn_cooldown	= 0.2,
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