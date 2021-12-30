import pygame
from pygame.locals import *
import person
import random
from AI import Pathing
import maps
from colors import *

pygame.init()


screen = pygame.display.set_mode((320, 320))

#Global Variables
playervel = 16			#Pixel distance between tiles / tile width
cell_margin = 1			#Margin used for drawing wall rect
mapOffsetRow = 0		#Offset added and subracted from based on player movement
mapOffsetColumn = 0		#Offset added and subracted from based on player movement
movement = False		#Whether or not to redraw screen from movement

#Initialize screen space
pygame.display.flip()
pygame.display.set_caption('Tiles')
font = pygame.font.SysFont("timesnewroman", 16)
pygame.display.flip()

#Clock for time based tracking and sync
clock = pygame.time.Clock()

#Set the map class variable and initialize it to the test map
defaultMap = maps.Maps(0)
defaultMap.setMapList(0)

#Set pathing AI to variable and initialize it using the map
pathAI = Pathing(defaultMap.getMapList())

#Set testing officer1 as NPC character
officer1 = person.AI(1, "Maggie", "human_unmod", (6,6))
officer1.setColor(blue)
officer1.text = font.render('@', True, officer1.getColor(), black)

#Initialize player character
player = person.Person("Sydney", "human_unmod", (6,10))
player.setColor(white)
player.text = font.render('@', True, player.getColor(), black)

#List of characters for looping and manipulation
characters = {officer1}

exitKey = False
#Game Loop
while not exitKey:
	#Execution code
	pygame.time.delay(100)

	#Test for game exit key
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			exitKey = True

	keys = pygame.key.get_pressed()

	if keys[pygame.K_LEFT] and (mapList[player.getPos('row')][player.getPos('col')-1] != 1):
		movement = True
		mapOffsetColumn += 1
		player.updatePos((player.getPos('row'),(player.getPos('col')-1)))
		print("LEFT")
	if keys[pygame.K_RIGHT] and (mapList[player.getPos('row')][player.getPos('col')+1] != 1):
		movement = True
		mapOffsetColumn -= 1
		player.updatePos(((player.getPos('row')),(player.getPos('col')+1)))
		print("RIGHT")
	if keys[pygame.K_UP] and (mapList[player.getPos('row')-1][player.getPos('col')] != 1):
		movement = True
		mapOffsetRow += 1
		player.updatePos(((player.getPos('row')-1),(player.getPos('col'))))
		print("UP")
	if keys[pygame.K_DOWN] and (mapList[player.getPos('row')+1][player.getPos('col')] != 1):
		movement = True
		mapOffsetRow -= 1
		player.updatePos(((player.getPos('row')+1),(player.getPos('col'))))
		print("DOWN")

	#Clear the screen for new drawing
	screen.fill(black)

	#Process each character in game one at a time
	for character in characters:
		#If character pos is equal to destination, then get a new destination and path
		if((character.getPos('row'),character.getPos('col')) == character.getDest()):
			if(DEBUG):
				print("Choosing new destination")
				print("Finding path for " + character.name + ", currentPos: ")
				print(character.pos)
			character.setPath(pathAI.astar(1, (character.getPos('row'),character.getPos('col')), character.chooseDestination(defaultMap.getMapList())))
			if(DEBUG):
				print(" newPos: ")
				print(character.dest)
			character.setWaitQ(10)
		#Update officer1 action and pos
		if(character.getWaitQ() == 0):
			character.executeAction(defaultMap.getMapList(), mapOffsetColumn, mapOffsetRow)
		else:
			character.waitQTick()
		if(character.pos == player.startingPos):
			print("Collision detected!")
		if(movement): #and (character.pos != player.startingPos):
			character.updatePos((character.getStartPos('row')+mapOffsetRow,character.getStartPos('col')+mapOffsetColumn))
		screen.blit(character.text, (character.getPos('col')*16,character.getPos('row')*16))
	
	screen.blit(player.text, (player.getStartPos('col')*16,player.getStartPos('row')*16))

	movement = False


	defaultMap.drawMap(screen, mapOffsetColumn, mapOffsetRow, font)


	if keys[pygame.K_ESCAPE]:
		exitKey = True
		print("Exit Game...")

	pygame.display.update()
