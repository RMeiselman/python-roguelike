import pygame
pygame.init()
import random

import map
import gui
import player

class Game:
	def __init__(self):
		random.seed()
		self.player				=	player.Player(self)
		self.map_manager	=	map.MapManager(self)
		self.gui					=	gui.GUI(self)
		self.running			=	1
	def load_game(self, filename):
		file = open(filename, 'r')
		
		file.close()
	def save_game(self):
		file = open(self.player.name + '.sav', 'w')
		file.write(self.player)
		file.write(self.map_manager)
		file.write(self.gui)
		file.close()
	def run(self):
		while self.running == 1:
			self.gui.poll_event()
	def process_event(self, event):
		for i in range(self.player.posx-self.player.infravision, self.player.posx+self.player.infravision+1):
			for j in range(self.player.posy-self.player.infravision, self.player.posy+self.player.infravision+1):
				if i>=0 and i<self.map_manager.get_current_map().width and j>=1 and j<self.map_manager.get_current_map().height:
					self.map_manager.get_current_map().data[i][j].explored = 1
		key = event.key
		if key == pygame.K_KP1:
			if self.map_manager.get_current_map().data[self.player.posx-1][self.player.posy+1].walkable == 1:
				self.player.posx	-=1
				self.player.posy	+=1
		elif key == pygame.K_KP2:
			if self.map_manager.get_current_map().data[self.player.posx][self.player.posy+1].walkable == 1:
				self.player.posy	+=1
		elif key == pygame.K_KP3:
			if self.map_manager.get_current_map().data[self.player.posx+1][self.player.posy+1].walkable == 1:
				self.player.posx	+=1
				self.player.posy	+=1
		elif key == pygame.K_KP4:
			if self.map_manager.get_current_map().data[self.player.posx-1][self.player.posy].walkable == 1:
				self.player.posx	-=1
		elif key == pygame.K_KP6:
			if self.map_manager.get_current_map().data[self.player.posx+1][self.player.posy].walkable == 1:
				self.player.posx	+=1
		elif key == pygame.K_KP7:
			if self.map_manager.get_current_map().data[self.player.posx-1][self.player.posy-1].walkable == 1:
				self.player.posx	-=1
				self.player.posy	-=1
		elif key == pygame.K_KP8:
			if self.map_manager.get_current_map().data[self.player.posx][self.player.posy-1].walkable == 1:
				self.player.posy	-=1
		elif key == pygame.K_KP9:
			if self.map_manager.get_current_map().data[self.player.posx+1][self.player.posy-1].walkable == 1:
				self.player.posx	+=1
				self.player.posy	-=1

	def done(self):
		pass

game	=	Game()
game.run()
game.done()

