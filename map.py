from constants import *
from rand import *

class Tile:
	def __init__(self, tile=" "):
		self.tile					=	tile
		self.frontcolor		=	COLOR_WHITE
		self.backcolor		=	COLOR_BLACK
		self.walkable			=	1
		self.explored			=	0
		self.destroyable	=	1
		self.info_visual	=	""
		
class Map:
	def __init__(self, game, width, height):
		self.game			=	game
		self.monsters	=	[]
		self.data			=	[]
		self.width		=	width
		self.height		=	height
		for i in range(self.width):
			self.data.append([])
			for j in range(self.height):
				self.data[i].append(Tile())
		print str(len(self.data)) + " " + str(len(self.data[0]))
	def generate(self):
		pass
	def get_ascii_sheet(self, x, y, w, h):
		ret = []
		for i in range(w):
			ret.append([])
			for j in range(h):
				if i+x < self.width and j+y < self.height and i+x >= 0 and j+y >= 0:
					if self.data[i+x][j+y].explored == 1:
						ret[i].append(self.data[i+x][j+y])
					else:
						ret[i].append(Tile())
				else:
					ret[i].append(Tile())
		ret[self.game.player.posx-x][self.game.player.posy-y] = Tile("@")
		return ret

	def get_minimap(w, h):
		ret = []
		for i in range(w):
			ret.append([])
			for j in range(h):
				pass
		return ret



class MapSimple(Map):
	def __init__(self, game):
		Map.__init__(self, game, 75, 50)

		# generation:
		for i in range(self.width):
			self.data[i][0].tile										=	"#"
			self.data[i][0].walkable								=	0
			self.data[i][0].destroyable							=	0
			self.data[i][self.height-1].tile				=	"#"
			self.data[i][self.height-1].walkable		=	0
			self.data[i][self.height-1].destroyable	=	0
		for i in range(self.height):
			self.data[0][i].tile										=	"#"
			self.data[0][i].walkable								=	0
			self.data[0][i].destroyable							=	0
			self.data[self.width-1][i].tile					=	"#"
			self.data[self.width-1][i].walkable			=	0
			self.data[self.width-1][i].destroyable	=	0
		for i in range(self.width):
			for j in range(self.height):
				if rand(10) == 1:
					self.data[i][j].tile 				= "%"
					self.data[i][j].frontcolor	= COLOR_RED
					self.data[i][j].backcolor		= COLOR_BLACK
				else:
					self.data[i][j].tile 				= "#"
					self.data[i][j].frontcolor	= COLOR_WHITE
					self.data[i][j].backcolor		= COLOR_BLACK
				self.data[i][j].walkable 	= 0

		#for i in range(random.randint(1, 10)):
		for i in range(int(.075*self.width*self.height)):
			self.mining(random.randint(1, self.width-2), random.randint(1, self.height-2), 20)

		# choose players position:
		ok = 0
		while ok == 0:
			x = random.randint(2, self.width-3)
			y = random.randint(2, self.height-3)
			if self.data[x][y].walkable == 1:
				self.game.player.posx = x
				self.game.player.posy = y
				ok = 1
	def mining(self, x, y, maxiter):
		if x > 1 and x < self.width-2 and y > 1 and y < self.height-2 and maxiter>0:
			self.data[x][y].tile 				= " "
			self.data[x][y].walkable 		= 1
			self.data[x][y].frontcolor	= COLOR_WHITE
			self.data[x][y].backcolor		= COLOR_BLACK
			if rand(95) == 1:
				direction = random.randint(1, 8)
				if direction == 1: self.mining(x-1, y+1, maxiter-1)
				elif direction == 2: self.mining(x, y+1, maxiter-1)
				elif direction == 3: self.mining(x+1, y+1, maxiter-1)
				elif direction == 4: self.mining(x-1, y, maxiter-1)
				elif direction == 5: self.mining(x+1, y, maxiter-1)
				elif direction == 6: self.mining(x-1, y-1, maxiter-1)
				elif direction == 7: self.mining(x, y-1, maxiter-1)
				elif direction == 8: self.mining(x+1, y-1, maxiter-1)

class MapManager:
	def __init__(self, game):
		self.game			=	game
		self.maps 		= []
		self.current	=	0
		self.generate()

	def generate(self):
		self.maps.append(MapSimple(self.game))

	def get_current_map(self):
		return self.maps[self.current]

	def save_maps(self):
		pass
