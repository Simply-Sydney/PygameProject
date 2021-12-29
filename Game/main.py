import pygame
from pygame.locals import *
import person
import random
from AI import Pathing
import maps

pygame.init()

white = (255,255,255)
blue = (100,100,255)
grey = (128,128,128)
black = (0,0,0)
cell_colors = (255,255,255), (0,0,0)

screen = pygame.display.set_mode((320, 320))

playervel = 16
cell_margin = 1
mapOffsetRow = 0
mapOffsetColumn = 0
DEBUG = True
movement = False

pygame.display.flip()
pygame.display.set_caption('Tiles')
font = pygame.font.SysFont("timesnewroman", 16)
pygame.display.flip()

clock = pygame.time.Clock()


def drawMap(screen):
    for rowTemp in range(len(mapList)):
        for columnTemp in range(len(mapList[0])):
            if((mapList[rowTemp][columnTemp]) == 1):
                screen.fill(white,getCellRect(rowTemp, columnTemp, screen))

def getCellRect(coordRow, coordCol, screen):
    row = coordRow
    column = coordCol
    cell_width = 16
    adjusted_width = cell_width - cell_margin
    return pygame.Rect((column * cell_width + cell_margin)+(mapOffsetColumn*cell_width), (row * cell_width + cell_margin)+(mapOffsetRow*cell_width), adjusted_width, adjusted_width)


def executeAction(character):
    if(character.behaviour == 1):
    #Randomly wander action
        #Character is not done waiting
        if(character.getWaitQ() != 0):
            if(DEBUG):
                print("Waiting tick for " + character.name)
            character.waitQTick()
            return

        #Character is done moving and needs to wait
        if((character.getPos('row'),character.getPos('col')) == (character.dest)):
            chooseDestination(character)
            character.setWaitQ(100)
            return

        #Do one move
        if(DEBUG):
            print("Moving character " + character.name)
            print("Next Pos: ")
            print (character.path[0])
        character.updatePos((character.path[0][0]+mapOffsetRow,character.path[0][1]+mapOffsetColumn))
        character.startingPos = (character.path[0][0]+mapOffsetRow,character.path[0][1]+mapOffsetColumn)
        character.path.pop(0)
        
        
def chooseDestination(character):
    newPathRow = random.randint(0,19)
    newPathCol = random.randint(0,19)
    while(mapList[newPathRow][newPathCol] == 1):
        newPathRow = random.randint(0,19)
        newPathCol = random.randint(0,19)
        if(DEBUG):
            print("Choosing new destination")
    character.setDest((newPathRow,newPathCol))
    if(DEBUG):
        print("Finding path for " + character.name + ", currentPos: ")
        print(character.pos)
        print(" newPos: ")
        print(character.dest)
    path = pathAI.astar(1, character.pos, character.dest)
    character.path = (path)
    if(DEBUG):
        print("New path for " + character.name + ": ")
        print(character.path)

#
#PERSON CLASS ABSTRACTED
#



defaultMap = maps.Maps(0)
mapList = defaultMap.setMapList(0)

#Initialize the pathfinding AI based on the initial mapList
pathAI = Pathing(mapList)

officer1 = person.AI(1, "Maggie", "human_unmod", (6,6))
officer1.setColor(blue)
officer1.text = font.render('@', True, officer1.getColor(), black)

player = person.Person("Sydney", "human_unmod", (6,10))
player.setColor(white)
player.text = font.render('@', True, player.getColor(), black)

characters = {officer1}

exitKey = False
#Game Loop
while not exitKey:
    #Execution code
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exitKey = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and (mapList[player.getPos('row')][player.getPos('col')-1] != 1):
        """print("Moving player to pos: ")
        print(player.getPos('row'))
        print(player.getPos('col')-1)
        print(player.pos)
        print("New col offset:")
        print(mapOffsetColumn+1)"""
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

    screen.fill(black)

    for character in characters:
        #Update officer1 action and pos
        executeAction(character)
        if(character.pos == player.startingPos):
            print("Collision detected!")
        if(movement): #and (character.pos != player.startingPos):
            character.updatePos((character.getStartPos('row')+mapOffsetRow,character.getStartPos('col')+mapOffsetColumn))
        screen.blit(character.text, (character.getPos('col')*16,character.getPos('row')*16))
    
    screen.blit(player.text, (player.getStartPos('col')*16,player.getStartPos('row')*16))

    movement = False

    #tilePosXCounter = 0
    #tilePosYCounter = 0
    #for tiles in mapList:
        #Update map tiles based on char movement
    #    if(tiles == 1):
    #        screen.blit(font.render('#', True, white, black), ((tilePosXCounter*16)+(mapOffsetX*16),(tilePosYCounter*16)+(mapOffsetY*16)))
    #    tilePosXCounter+=1
    #    if(tilePosXCounter == 8):
    #        tilePosXCounter = 0
    #        tilePosYCounter+=1

    drawMap(screen)


    if keys[pygame.K_ESCAPE]:
        exitKey = True
        print("Exit Game...")

    pygame.display.update()
