import pygame as pg
from math import *

from game_state import *
from entity import *
from input import *

def game_loop(surface):

	quitting = False

	input		= Input({
		"zoom": (pg.K_l, pg.K_o),
	}, {
		"movement": (pg.K_LEFT, pg.K_RIGHT, pg.K_UP, pg.K_DOWN),
	})

	game_state	= GameState(surface, input)
	camera		= game_state.camera

	player_1	= Player(0, 0, "Ressources/standing.png", input)

	bg = Entity(0, 0, RepeatingImage("Ressources/square bg.jpg"))
	game_state.add_entity(bg)

	camera.target = player_1

	game_state.add_entity(player_1)

	for i in range(0, 0):
		for j in range(0, 0):
			#bat = FlyingEnemy(50*i, - 50 * j, f"Ressources/bat{1 + (i + j) % 5}.png", player_1)
			#bat = FlyingEnemy(50*i, - 50 * j, "Ressources/bat1.png", game_state.entities[10*i+j])
			bat = FlyingEnemy(50*i, - 50 * j, "Ressources/bat1.png", player_1)
			bat.image.image = pg.transform.scale_by(bat.image.image, (i+j)%5)
			game_state.add_entity(bat)

	for i in range(0, 1):
		game_state.add_entity(Enemy(50*i, 0, "Ressources/bat1.png", player_1))

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
	window = pg.display.set_mode(size=(800, 500))

	# nom de la fenêtre
	pg.display.set_caption("Premier jeu")

	game_loop(window)

	pg.quit()