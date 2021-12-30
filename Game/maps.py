from colors import *
import pygame

cell_margin = 1

class Maps:

	def __init__(self, roomNum=0):
		self.roomNum = roomNum
		self.mapList = []


	def drawMap(self, screen, mapOffsetColumn, mapOffsetRow, font):
		for rowTemp in range(len(self.mapList)):
			for columnTemp in range(len(self.mapList[0])):
				if((self.mapList[rowTemp][columnTemp]) == 1):
					screen.fill(white,self.getCellRect(rowTemp, columnTemp, screen, mapOffsetColumn, mapOffsetRow))
				elif((self.mapList[rowTemp][columnTemp]) == 2):
					door = font.render('D', True, white, black)
					screen.blit(door, (columnTemp*16,rowTemp*16))

	def getCellRect(self, coordRow, coordCol, screen, mapOffsetColumn, mapOffsetRow):
		row = coordRow
		column = coordCol
		cell_width = 16
		adjusted_width = cell_width - cell_margin
		return pygame.Rect((column * cell_width + cell_margin)+(mapOffsetColumn*cell_width), (row * cell_width + cell_margin)+(mapOffsetRow*cell_width), adjusted_width, adjusted_width)
		
	#TILEMAP GLOSSARY:
	# 0 = SPACE
	# 1 = WALL
	# 2 = DOOR
	# 3 = FLOOR
	def setMapList(self, roomNum):
		if(roomNum == 0):
			self.roomName = "Test Room"
			self.mapList = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
							[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,3,3,3,3,1,3,1,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,3,3,3,3,3,3,2,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,3,3,3,3,3,3,1,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,3,3,1,3,3,3,1,3,3,3,3,3,3,3,3,3,1],
							[1,3,1,1,1,1,1,1,1,1,3,3,3,3,3,3,3,3,3,1],
							[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
							[1,3,3,3,3,3,3,1,1,1,1,1,1,1,1,1,3,3,3,1],
							[1,1,1,3,3,3,1,1,1,1,1,3,3,3,3,1,1,1,1,1],
							[1,1,3,3,3,1,1,1,1,1,3,3,3,3,3,3,1,1,1,1],
							[1,3,3,3,1,1,1,1,1,3,3,3,3,3,3,3,1,1,1,1],
							[1,3,3,3,3,3,1,1,3,3,3,3,3,3,3,1,1,1,1,1],
							[1,3,3,3,3,3,3,3,3,3,3,3,3,3,1,1,1,1,1,1],
							[1,1,3,3,3,3,3,3,3,3,3,3,3,1,1,1,3,3,3,1],
							[1,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
							[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

		elif(roomNum == 1):
			self.roomName = "Bridge_Nova"
			self.mapList = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
							[0,0,0,0,0,1,1,3,3,3,3,3,3,1,1,0,0,0,0,0],
							[0,0,0,0,0,1,3,3,3,3,3,3,3,3,1,0,0,0,0,0],
							[0,0,0,0,1,1,3,3,3,3,3,3,3,3,1,1,0,0,0,0],
							[0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,1,0,0,0,0],
							[0,0,0,0,1,3,3,3,3,3,3,3,3,3,3,1,0,0,0,0],
							[0,0,0,0,1,3,3,3,1,1,1,1,3,3,3,1,0,0,0,0],
							[0,0,0,0,1,3,3,3,1,1,1,1,3,3,3,1,0,0,0,0],
							[0,0,0,0,1,1,3,3,3,1,1,3,3,3,1,1,0,0,0,0],
							[0,0,0,0,0,1,3,3,3,3,3,3,3,3,1,0,0,0,0,0],
							[0,0,0,0,0,1,1,3,3,3,3,3,3,1,1,0,0,0,0,0],
							[0,0,0,0,0,0,1,3,3,3,3,3,3,1,0,0,0,0,0,0],
							[0,0,0,0,0,0,2,3,3,3,3,3,3,2,0,0,0,0,0,0],
							[0,0,0,0,0,0,1,3,3,3,3,3,3,1,0,0,0,0,0,0],
							[0,0,0,0,0,0,1,1,3,3,3,3,1,1,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,1,1,2,2,1,1,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
							[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]

		return self.mapList
		
	def getMapList(self):
		return self.mapList
