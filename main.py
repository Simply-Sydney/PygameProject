#Imports
import pygame
from pygame.locals import *
import person
import random
from AI import Pathing
from galaxy import Galaxy
from config import *
from sprites import *
import sys

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
		pygame.display.set_caption("Interstellar Voyage")
		
	def new(self):
		#Start a new game
		self.playing = True
		
		self.all_sprites = pygame.sprite.LayeredUpdates()
		self.blocks = pygame.sprite.LayeredUpdates()
		self.enemies = pygame.sprite.LayeredUpdates()
		self.attacks = pygame.sprite.LayeredUpdates()
		
		self.player = Player(self, 1, 2)
		
	def events(self):
		#Game loop events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.playing = False
				self.running = False
				
	def update(self):
		#Game loop updates
		self.all_sprites.update()
		
	def draw(self):
		#Game loop draw
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen))
		self.clock.tick(FPS)
		pygame.display.update()
		
	def main(self):
		#Game loop itself
		while self.playing:
			self.events()
			self.update()
			self.draw()
		self.running = False
		
	def game_over(self):
		pass
	
	def intro_screen(self):
		pass
		
g = Game()
g.intro_screen(
g.new()
while g.running:
	g.main()
	g.game_over()
	
pygame.quit()
sys.exit()


#---------------------------------------------------


#List containing all sprites to render
all_sprites_list = pygame.sprite.Group()

playerPlayer = Player(WHITE, 32, 32)
playerPlayer.rect.x = (SCREENWIDTH/2) - 64
playerPlayer.rect.y = (SCREENHEIGHT/2) - 64

all_sprites_list.add(playerPlayer)

carryOn = True
bStarSelected = False
mouseClick = False

galaxyOffset_x = 0
galaxyOffset_y = 0
vSelectedStar = ()

#GENERATE HISTORY


while carryOn:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			carryOn = False
		elif event.type==pygame.KEYDOWN:
			if event.key==pygame.K_x:		#'X' key will quit game
				carryOn=False
		elif event.type==pygame.MOUSEBUTTONUP:
			mouseClick = True
	
	#Handle movement
	#ALTER LATER TO MOVE CAMERA INSTEAD OF PLAYER
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		playerPlayer.moveLeft()
		#moveWorld
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		#moveWorld
		playerPlayer.moveRight()
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		#moveWorld
		playerPlayer.moveUp()
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		#moveWorld
		playerPlayer.moveDown()
		
	all_sprites_list.update()
	
	#Fill screen
	screen.fill(BLACK)
	#Draw Character
	all_sprites_list.draw(screen)
	
	#GENERATE GALAXY MAP
	if keys[pygame.K_LEFT] or keys[pygame.K_a]:
		galaxyOffset_x -= 5
	if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
		galaxyOffset_x += 5
	if keys[pygame.K_UP] or keys[pygame.K_w]:
		galaxyOffset_y -= 3
	if keys[pygame.K_DOWN] or keys[pygame.K_s]:
		galaxyOffset_y += 3
	
	nSectorsX = SCREENWIDTH / 16
	nSectorsY = SCREENHEIGHT / 16
	
	screen_sector_x = 0
	screen_sector_y = 0
	
	mouse_x, mouse_y = pygame.mouse.get_pos()
	#mouse_x /= 16
	#mouse_y /= 16
	galaxy_mouse_x = mouse_x + galaxyOffset_x
	galaxy_mouse_y = mouse_y + galaxyOffset_y
	
	while (screen_sector_x < nSectorsX):
		screen_sector_x += 1
		screen_sector_y = 0
		while (screen_sector_y < nSectorsY):
			screen_sector_y += 1
			starSystem = Galaxy(screen_sector_x + galaxyOffset_x, screen_sector_y + galaxyOffset_y)
			
			if (starSystem.starExists):
				pygame.draw.circle(screen, starSystem.color, ((screen_sector_x * 16) + 8, (screen_sector_y * 16) + 8), int(starSystem.starDiameter))
				if(int(mouse_x/16) == screen_sector_x and int(mouse_y/16) == screen_sector_y):
					pygame.draw.circle(screen, RED, ((screen_sector_x * 16) + 8, (screen_sector_y * 16) + 8), int(starSystem.starDiameter)+5, width=2)
					if mouseClick:
						clickedStar_x = screen_sector_x + galaxyOffset_x
						clickedStar_y = screen_sector_y + galaxyOffset_y
						bStarSelected = True
						mouseClick = False


	if bStarSelected:
		star = Galaxy(clickedStar_x, clickedStar_y, True)
		
		drawPos_x = (star.starDiameter*20)+35
		drawPos_y = (SCREENHEIGHT*0.75)-15
		
		pygame.draw.rect(screen, WHITE, pygame.Rect(27,SCREENHEIGHT/2,SCREENWIDTH-54,(SCREENHEIGHT/2)-27), 3)
		pygame.draw.rect(screen, BLUE, pygame.Rect(30,SCREENHEIGHT/2,SCREENWIDTH-60,(SCREENHEIGHT/2)-30))
		pygame.draw.circle(screen, star.color, (drawPos_x, drawPos_y), star.starDiameter*20)
		
		drawPos_x += (star.starDiameter*10 + 30)
		for planet in star.listPlanets:
			drawPos_x += (planet.diameter)
			drawPos_x += planet.distance
			pygame.draw.circle(screen, WHITE, (drawPos_x, drawPos_y), planet.diameter)
		
		if keys[pygame.K_q]:
			bStarSelected = False
	
		
		
		
	
	#pygame.draw.rect(screen, RED, [55, 200, 100, 70], 0)
	#pygame.draw.line(screen, GREEN, [0, 0], [100, 100], 5)
	#pygame.draw.ellipse(screen, BLUE, [20, 20, 250, 100], 2)
	
	pygame.display.flip()
	
	clock.tick(60)
	
pygame.quit()