import pygame
import sys
import time

from constants import *

FONT_SIZE											=	20
FONT_SIZEX										=	11
FONT													=	pygame.font.SysFont("consolas", FONT_SIZE)
FONT_BOLD											=	pygame.font.SysFont("consolas", FONT_SIZE, 1)
FONT_ANTIALIASING							=	1


class Element:
	def __init__(self, text, posx, posy, frontcolor, backcolor, highlight):
		self.text				=	text
		self.posx				=	posx
		self.posy				=	posy
		self.frontcolor	=	frontcolor
		self.backcolor	= backcolor
		self.highlight	=	highlight

class Window:
	def __init__(self, game):
		self.game						= game
		self.height 				= 0
		self.width	 				= 0
		self.posx						=	0
		self.posy						= 0
		self.title					=	""
		self.closeable			=	1
		self.resizeable			=	1
		self.moveable				=	1
		self.elements				=	[]
		self.title_bgcolor	=	WINDOW_TITLE_BGCOLOR_ACTIVE
	def close(self):
		self.game.gui.del_window(self)
	def add_element(self, text, posx, posy, frontcolor=COLOR_WHITE, backcolor=WINDOW_BGCOLOR, highlight=0):
		self.elements.append(Element(text, posx, posy, frontcolor, backcolor, highlight))
	def clear(self):
		del self.elements[:]
	def resize(self, width, height):
		self.width	=	width
		self.height	=	height
	def move(self, posx, posy):
		self.posx	=	posx
		self.posy	=	posy
	def center(self):
		self.move((RESX/FONT_SIZEX-self.width)/2-1, (RESY/FONT_SIZE-self.height)/2-1)
	def draw(self, screen):
		shadow = pygame.Surface((FONT_SIZEX*self.width, FONT_SIZE*(self.height+1)))
		shadow_rect = shadow.fill(COLOR_BLACK)
		shadow_rect.top=FONT_SIZE*self.posy+10
		shadow_rect.left=FONT_SIZEX*self.posx+10
		shadow.set_alpha(100)
		screen.blit(shadow, shadow_rect)

		screen.fill(WINDOW_BORDERCOLOR, pygame.Rect(FONT_SIZEX*self.posx-WINDOW_BORDER, FONT_SIZE*self.posy-WINDOW_BORDER, FONT_SIZEX*self.width+2*WINDOW_BORDER, FONT_SIZE*(self.height+1)+2*WINDOW_BORDER))
		screen.fill(WINDOW_BGCOLOR, pygame.Rect(FONT_SIZEX*self.posx, FONT_SIZE*self.posy, FONT_SIZEX*self.width, FONT_SIZE*(self.height+1)))
		screen.fill(self.title_bgcolor, pygame.Rect(FONT_SIZEX*self.posx, FONT_SIZE*self.posy, FONT_SIZEX*self.width, FONT_SIZE))
		screen.blit(FONT_BOLD.render(self.title, 1, (255, 255, 255)), (FONT_SIZEX*self.posx, FONT_SIZE*self.posy))
		if self.closeable == 1:
			screen.fill(WINDOW_BORDERCOLOR, pygame.Rect(FONT_SIZEX*(self.posx+self.width-1), FONT_SIZE*self.posy, FONT_SIZEX, FONT_SIZE))
			pygame.draw.aaline(screen, COLOR_BLACK, (FONT_SIZEX*(self.posx+self.width-.75), FONT_SIZE*(self.posy+.25)), (FONT_SIZEX*(self.posx+self.width-.25), FONT_SIZE*(self.posy+.75)))
			pygame.draw.aaline(screen, COLOR_BLACK, (FONT_SIZEX*(self.posx+self.width-.75), FONT_SIZE*(self.posy+.75)), (FONT_SIZEX*(self.posx+self.width-.25), FONT_SIZE*(self.posy+.25)))
		if self.moveable == 1:
			screen.fill(WINDOW_BORDERCOLOR, pygame.Rect(FONT_SIZEX*(self.posx+self.width-2), FONT_SIZE*self.posy, FONT_SIZEX, FONT_SIZE))
			screen.blit(FONT.render("M", FONT_ANTIALIASING, COLOR_BLACK), (FONT_SIZEX*(self.posx+self.width-2), FONT_SIZE*self.posy))
		if self.resizeable == 1:
			screen.fill(WINDOW_BORDERCOLOR, pygame.Rect(FONT_SIZEX*(self.posx+self.width-3), FONT_SIZE*self.posy, FONT_SIZEX, FONT_SIZE))
			screen.blit(FONT.render("R", FONT_ANTIALIASING, COLOR_BLACK), (FONT_SIZEX*(self.posx+self.width-3), FONT_SIZE*self.posy))
		if len(self.elements) != 0:
			for element in self.elements:
				if element.highlight == 1:
					screen.fill(COLOR_WHITE, pygame.Rect(FONT_SIZEX*(self.posx+element.posx)-BUTTON_BORDER, FONT_SIZE*(self.posy+element.posy+1)-BUTTON_BORDER, FONT_SIZEX*len(element.text)+2*BUTTON_BORDER, FONT_SIZE+2*BUTTON_BORDER))
				screen.fill(element.backcolor, pygame.Rect(FONT_SIZEX*(self.posx+element.posx), FONT_SIZE*(self.posy+element.posy+1), FONT_SIZEX*len(element.text), FONT_SIZE))
				screen.blit(FONT.render(element.text, 1, element.frontcolor), (FONT_SIZEX*(self.posx+element.posx), FONT_SIZE*(self.posy+element.posy+1)))
		self.draw_optional(screen)
	def draw_optional(self, screen):
		pass
	def update_content(self):
		pass
	def process_event(self, event):
		pass

class WindowMain(Window):
	def __init__(self, game):
		Window.__init__(self, game)
		self.height			=	20
		self.width			=	50
		self.title 			= "Main"
		self.closeable	=	0
		self.resizeable	=	1
		self.center()

		self.angleX			=	0
		self.angleY			=	0

	def draw_optional(self, screen):
		pygame.draw.line(screen, COLOR_BLACK, (FONT_SIZEX*self.posx, FONT_SIZE*(self.posy+self.height-1.5)), (FONT_SIZEX*(self.posx+self.width), FONT_SIZE*(self.posy+self.height-1.5)))

	def update_content(self):
		self.angleX	=	self.game.player.posx-self.width/2+1
		self.angleY	=	self.game.player.posy-self.height/2+3

		self.clear()
		self.add_element(self.game.player.name + 5*" " + self.game.player.race + " " + self.game.player.profession, 0, self.height-2, COLOR_BLUE)
		self.add_element("HP:" + str(self.game.player.cur_hp) + "/" + str(self.game.player.max_hp), 0, self.height-1, COLOR_BLUE)

		tiles = self.game.map_manager.get_current_map().get_ascii_sheet(self.angleX, self.angleY, self.width, self.height-2)
		for i in range(self.width):
			for j in range(self.height-2):
				self.add_element(tiles[i][j].tile, i, j, tiles[i][j].frontcolor, tiles[i][j].backcolor)

	def process_event(self, event):
		if event.key == pygame.K_m and event.mod & pygame.KMOD_SHIFT:
			self.game.gui.add_window(WindowMap)
		else:
			self.game.process_event(event)

class WindowMap(Window):
	def __init__(self, game):
		Window.__init__(self, game)
		self.closeable	=	1
		self.moveable		=	1
		self.resizeable	=	0
		self.title			=	"Minimap"
		self.resize(25, 17)

	def update_content(self):
		self.clear()
		tiles = self.game.map_manager.get_current_map().get_minimap(self.width, self.height)
		for i in range(self.width):
			for j in range(self.height):
				self.add_element(tiles[i][j].tile, i, j, tiles[i][j].frontcolor, tiles[i][j].backcolor)

		

class WindowInventory(Window):
	def __init__(self, game):
		self.game	= game

class WindowAbout(Window):
	def __init__(self, game):
		Window.__init__(self, game)
		self.height			=	4
		self.width			=	28
		self.posx				=	(RESX/FONT_SIZEX-self.width)/2-1
		self.posy				=	(RESY/FONT_SIZE-self.height-1)/2-1
		self.title 			= "About..."
		self.closeable	=	1
		self.resizeable	=	0
		self.add_element("Rogue-like engine", 0, 0)
		self.add_element("Version: v1", 0, 1, (0, 0, 200))
		self.add_element("Written by: Stephan Schindel", 0, 2)
		self.add_element("License: GPL v3", 0, 3, (0, 0, 200))
	
class WindowNewGame(Window):
	def __init__(self, game):
		Window.__init__(self, game)
		self.height			=	1
		self.width			=	25
		self.title 			= "Create new game"
		self.closeable	=	0
		self.resizeable	=	0
		self.center()
		self.state			=	0
	def update_content(self):
		self.clear()
		if self.state == 0:
			self.add_element("Your name: ", 0, 0)
			self.add_element(self.game.player.name + "_", 10, 0)
		elif self.state == 1:
			self.add_element("Choose a race:", 0, 0)
			self.add_element("a) Human", 0, 2, COLOR_BLUE)
		elif self.state == 2:
			self.add_element("Choose a profession:", 0, 0)
			self.add_element("a) Warrior", 0, 2, COLOR_BLUE)
	def process_event(self, event):
		if self.state == 0:
			if event.key == pygame.K_BACKSPACE:
				self.game.player.name = self.game.player.name[:len(self.game.player.name)-1]
			elif event.key == pygame.K_RETURN:
				self.state = 1
				self.resize(25, 10)
				self.center()
			if pygame.key.name(event.key) == "space":
				self.game.player.name += " "
			if event.key >= 97 and event.key <= 122:
				self.game.player.name += pygame.key.name(event.key)
		elif self.state == 1:
			if event.key == pygame.K_a:
				self.game.player.race = "Human"
				self.state = 2
		elif self.state == 2:
			if event.key == pygame.K_a:
				self.game.player.profession	=	"Warrior"
				self.game.gui.add_window(WindowMain)
				self.close()

class WindowHelp(Window):
	def __init__(self, game):
		Window.__init__(self, game)
		self.height			=	20
		self.width			=	20
		self.title 			= "Help"
		self.closeable	=	1
		self.resizeable	=	0
		self.center()

class WindowMainMenu(Window):
	def __init__(self, game):
		Window.__init__(self, game)
		self.height			=	20
		self.width			=	25
		self.posx				=	(RESX/FONT_SIZEX-self.width)/2
		self.posy				=	(RESY/FONT_SIZE-self.height-1)/2
		self.title 			= "Main menue"
		self.closeable	=	0
		self.resizeable	=	0
		self.moveable		=	0
		self.add_element("Welcome to ...", 1, 1, COLOR_BLUE)
		self.add_element("Start a new game [n]", 1, 3, COLOR_WHITE, COLOR_BLACK, 1)
		self.add_element("Recover last state  [r]", 1, 5, COLOR_WHITE, COLOR_BLACK, 1)
		self.add_element("Help  [H]", 1, 7, COLOR_WHITE, COLOR_BLACK, 1)
		self.add_element("Quit  [q]", 1, 9, COLOR_WHITE, COLOR_BLACK, 1)
	def process_event(self, event):
		if event.key == pygame.K_q: sys.exit()
		elif event.key == pygame.K_n:
			self.game.gui.add_window(WindowNewGame)
			self.close()

class GUI:
	def __init__(self, game):
		self.game			=	game
		self.windows	=	[]
		self.event		= []
		if USE_FULLSCREEN==1:	self.screen = pygame.display.set_mode((RESX, RESY), pygame.FULLSCREEN)
		else: self.screen = pygame.display.set_mode((RESX, RESY))
		try:
			self.back_image		=	pygame.image.load("back.png")
		except pygame.error(), message:
			sys.exit()
		self.back_image = self.back_image.convert()
		self.add_window(WindowMainMenu)
	def add_window(self, window_class=Window):
		if len(self.windows)!=0: self.windows[-1].title_bgcolor = WINDOW_TITLE_BGCOLOR_INACTIVE
		self.windows.append(window_class(self.game))
		self.draw()
	def del_window(self, window):
		del self.windows[self.windows.index(window)]
	def poll_event(self):
		self.event = pygame.event.get()
		if len(self.event)!=0:
			self.draw()
			for event in self.event:
				if event.type == pygame.QUIT: sys.exit()
				elif event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE and self.windows[-1].closeable==1:
						del self.windows[-1]
						self.windows[-1].title_bgcolor = WINDOW_TITLE_BGCOLOR_ACTIVE
					elif event.key == pygame.K_x and event.mod & pygame.KMOD_CTRL:
						self.game.save_game()
						sys.exit()
					elif event.key == pygame.K_a and event.mod & pygame.KMOD_CTRL: self.add_window(WindowAbout)
					elif event.key == pygame.K_h and event.mod & pygame.KMOD_SHIFT: self.add_window(WindowHelp)
					elif event.key == pygame.K_m and event.mod & pygame.KMOD_ALT and self.windows[-1].resizeable == 1:
						self.windows[-1].resize(RESX/FONT_SIZEX, RESY/FONT_SIZE-1)
						self.windows[-1].move(0, 0)
					if len(self.windows)!=0:
						if event.key == pygame.K_TAB:
							self.windows[0].title_bgcolor = WINDOW_TITLE_BGCOLOR_ACTIVE
							self.windows[-1].title_bgcolor = WINDOW_TITLE_BGCOLOR_INACTIVE
							self.windows.append(self.windows[0])
							del self.windows[0]
						else:
							self.windows[-1].process_event(event)

		if pygame.key.get_pressed()[pygame.K_RIGHT] == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT] == 1:
			if self.windows[-1].moveable == 1:
				self.windows[-1].posx+=1
				if self.windows[-1].posx > RESX/FONT_SIZEX-self.windows[-1].width: self.windows[-1].posx = RESX/FONT_SIZEX-self.windows[-1].width
				self.draw()
				time.sleep(TIME_INPUT)
		if pygame.key.get_pressed()[pygame.K_LEFT] == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT] == 1:
			if self.windows[-1].moveable == 1:
				self.windows[-1].posx-=1
				if self.windows[-1].posx < 0: self.windows[-1].posx = 0
				self.draw()
				time.sleep(TIME_INPUT)
		if pygame.key.get_pressed()[pygame.K_UP] == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT] == 1:
			if self.windows[-1].moveable == 1:
				self.windows[-1].posy-=1
				if self.windows[-1].posy < 0: self.windows[-1].posy = 0
				self.draw()
				time.sleep(TIME_INPUT)
		if pygame.key.get_pressed()[pygame.K_DOWN] == 1 and pygame.key.get_pressed()[pygame.K_LSHIFT] == 1:
			if self.windows[-1].moveable == 1:
				self.windows[-1].posy+=1
				if self.windows[-1].posy > RESY/FONT_SIZE-self.windows[-1].height: self.windows[-1].posy = RESY/FONT_SIZE-self.windows[-1].height
				self.draw()
				time.sleep(TIME_INPUT)

		if pygame.key.get_pressed()[pygame.K_RIGHT] == 1 and pygame.key.get_pressed()[pygame.K_LALT] == 1:
			if self.windows[-1].resizeable==1: self.windows[-1].width+=1
			self.draw()
			time.sleep(TIME_INPUT)
		if pygame.key.get_pressed()[pygame.K_LEFT] == 1 and pygame.key.get_pressed()[pygame.K_LALT] == 1:
			if self.windows[-1].resizeable==1: self.windows[-1].width-=1
			self.draw()
			time.sleep(TIME_INPUT)
		if pygame.key.get_pressed()[pygame.K_UP] == 1 and pygame.key.get_pressed()[pygame.K_LALT] == 1:
			if self.windows[-1].resizeable==1: self.windows[-1].height-=1
			self.draw()
			time.sleep(TIME_INPUT)
		if pygame.key.get_pressed()[pygame.K_DOWN] == 1 and pygame.key.get_pressed()[pygame.K_LALT] == 1:
			if self.windows[-1].resizeable==1: self.windows[-1].height+=1
			self.draw()
			time.sleep(TIME_INPUT)

	def draw(self):
		#self.screen.fill((0, 0, 0))
		self.screen.blit(self.back_image, (0, 0))
		if len(self.windows)!=0:
			for window in self.windows:
				window.update_content()
				window.draw(self.screen)
		pygame.display.flip()

		
