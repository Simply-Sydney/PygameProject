import pygame
from collections import defaultdict

BLUE = (0,0,255)
WHITE = (255,255,255)
YELLOW = (255,255,0)
ORANGE = (255,140,0)
RED = (255,0,0)

class Planet:
	distance = 0
	diameter = 0
	foliage = 0
	minerals = 0
	water = 0
	gases = 0
	temperature = 0
	population = 0
	ring = False
	moons = list()


#-----------------------------------
#OLD GALAXY CLASS
#-----------------------------------
class Galaxy:
	nLehmer = 0;
	starExists = False
	starDiameter = 0.0
	color = (255, 255, 255)
	listPlanets = list()

	def __init__(self, x, y, generateFullSystem=False):
		self.nLehmer = (x & 0xFFFF) << 16 | (y & 0xFFFF)
		
		self.starExists = (self.rndInt(0, 20) == 10)
		if (not self.starExists):
			return
		
		self.starDiameter = self.rndInt(1, 8)
		self.color = ((self.rndInt(0, 255)),(self.rndInt(0, 255)),(self.rndInt(0, 255)))
		
		if(not generateFullSystem):
			return
		
		nPlanets = self.rndInt(0, 2)
		for i in range(nPlanets):
			p = Planet()
			p.distance = self.rndInt(20, 200)
			p.diameter = self.rndInt(4, 20)
			p.temperature = self.rndInt(-200, 300)
			p.foliage = self.rndInt(0, 10)
			p.minerals = self.rndInt(0, 10)
			p.water = self.rndInt(0, 10)
			p.gases = self.rndInt(0, 10)
			p.population = self.rndInt(0, 100)
			p.ring = (self.rndInt(0,10) == 1)
			nMoons = max(self.rndInt(-5, 5), 0)
			for n in range(nMoons):
				p.moons.append(self.rndInt(1, 5))
			
			self.listPlanets.append(p)
			
	
	def Lehmer32(self):
		self.nLehmer += 0xe120fc15
		tmp = self.nLehmer * 0x4a39b70d
		m1 = (tmp >> 32) ^ tmp
		tmp = m1 * 0x12fad5c9
		m2 = (tmp >> 32) ^ tmp
		return m2
		
	def rndInt(self, min, max):
		return (self.Lehmer32() % (max-min)) + min
		

#------------------------------------
#GALAXY REWORK W/ HASHMAP
#------------------------------------
class improvedGalaxy:
	nLehmer = 0;					#Random value variable
	starChart = defaultdict(list)	#Hashmap containing all star lists
	listStarValues = list()		#List of star values associated with star
		#Contains:
		# - If Star Exists (Bool)
		# - Diameter
		# - Color
		# - Binary?
		# - Special? (Pulsar / black hole)
		# - Planet list hash-key

	#Constructor
	def __init__(self, xpos, ypos):
		self.nLehmer = (x & 0xFFFF) << 16 | (y & 0xFFFF)
		planets = starSystem(xpos, ypos)
		starExists = rndInt(0,1)
		if(starExists == 1):
			self.listStarValues.append(starExists)			#Append that the star exists
			self.listStarValues.append(rndInt(1,8))			#Gen and append diameter
			colorSelect = rndInt(1,5)						#Generate color chance
			if(colorSelect == 1):
				self.listStarValues.append(BLUE)			#Star is BLUE
			elif(colorSelect == 2):
				self.listStarValues.append(WHITE)			#Star is WHITE
			elif(colorSelect == 3):
				self.listStarValues.append(YELLOW)			#Star is YELLOW
			elif(colorSelect == 4):
				self.listStarValues.append(ORANGE)			#Star is ORANGE
			else:
				self.listStarValues.append(RED)				#Star is RED
			self.listStarValues.append(rndInt(1,25) == 1)	#Gen if star is special (1/25)
			
			#TODO - Add planet list to star
		
	def Lehmer32(self):
		self.nLehmer += 0xe120fc15
		tmp = self.nLehmer * 0x4a39b70d
		m1 = (tmp >> 32) ^ tmp
		tmp = m1 * 0x12fad5c9
		m2 = (tmp >> 32) ^ tmp
		return m2
		
	def rndInt(self, min, max):
		return (self.Lehmer32() % (max-min)) + min
		

#------------------------------------
#STAR SYSTEM GENERATED PER GALACTIC COORDINATE (PLANETS)
#------------------------------------	
class starSystem:
	planetChart = defaultdict(list)	#Hashmap containing all planet lists
	listPlanets = list()			#Planets orbiting star
		#Contains:
		# - Distance
		# - Diameter
		# - Temperature (Influenced by distance)
		# - Minerals
		# - Gases (Small influence from diameter)
		# - Water (Influenced by temp and gases)
		# - Foliage (Influenced by temp, water, and gases)
		# - Population (Influenced by a lot)
		# - Ring? (Boolean, rare)
		# - List of moons
		
	#Constructor
	def __init__(self, xpos, ypos):
		self.nLehmer = (x & 0xFFFF) << 16 | (y & 0xFFFF)
		
	