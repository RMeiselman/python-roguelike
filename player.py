import random

class Player:
	def __init__(self, game):
		self.game					=	game
		self.name					=	""
		self.race					=	""
		self.inventory		=	[]
		self.posx					=	0
		self.posy					=	0
		self.max_hp				=	random.randint(1,10)
		self.cur_hp				=	self.max_hp
		self.infravision	=	5
