import sys
from os import listdir
from os.path import isfile, join
from random import randint

import pygame

import cells

def mapThis(current, min1, max1, min2, max2):
	x = min1
	max1 -= x
	current -= x
	x = min2
	max2 -= x
	out = (current / max1) * max2
	out += x + 1
	max2 += x
	if out < min2:
		out = min2
	elif out > max2:
		out = max2
	return out

def handleInput():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()


pygame.init()
size = (600, 600)
screen = pygame.display.set_mode(size)
background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background,size)


class main:
	def __init__(self):
		self.grid = self.gridmake([10,10])
		self.imgs = self.load()

	def load(self):
		imgs = {}
		for filename in [f for f in listdir(r"sprits/") if isfile(join("sprits/", f))]:
			x = filename
			filename = "sprits/" + filename
			if filename == "sprits/0.png":
				temp = pygame.image.load(filename).convert_alpha()
				temp.set_alpha(150)
				imgs["0"]=(pygame.transform.scale(temp, (size[0] // len(self.grid[0]), size[1] // len(self.grid))))
				print("got it")
			else:
				temp = pygame.image.load(filename)
				imgs[str(x.replace(".png",""))]=(pygame.transform.scale(temp, (size[0] // len(self.grid[0]), size[1] // len(self.grid))))
		return imgs

	def gridmake(self, ssize):
		grid = []
		for x in range(ssize[0]):
			row = []
			for y in range(ssize[1]):
				# if randint(0,10) >= 1:
				row.append(cells.cells(0, x, y, size, ssize))
				# else:
				# 	row.append(cells.cells(1, x, y, size, ssize))
			grid.append(row)
		return grid

	def spawn(self):
		for y in range(len(self.grid)):
			for x in range(len(self.grid)):
				if self.grid[y][x].item == 0 and not self.grid[y][x].blocked:
					self.grid[y][x].item = randint(2, len(self.imgs))
					# print(str(self.grid[x][0].item),end=", ")

	def draw(self):
		screen.fill((30,30,30))
		screen.blit(background,(0,0))
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				tsize = size[0]//len(self.grid)
				if self.grid[x][y].blocked == 0:
					screen.blit(self.imgs["0"],(tsize*x,tsize*y))
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				self.grid[x][y].draw(screen, self.imgs)

	def move(self):
		for x in range(len(self.grid)):
			for y in range(len(self.grid[0])):
				self.grid[x][y].move()

	def temp(self, temp):
		poes = [(0,1),(1,0),(0,-1),(-1,0)]
		if temp >= 300:
			print('move')
			a = randint(1, len(self.grid)-2)
			b = randint(1, len(self.grid)-2)

			pos = (randint(0, 3))
			pos = poes[pos]
			# print(pos)
			self.grid[a][b].move((pos[0]*-1, pos[1]*-1),self.grid[a-pos[1]][b-pos[0]].item)
			# print((a,b))
			self.grid[a-pos[1]][b-pos[0]].move(pos,self.grid[a][b].item)
			# print((a-pos[1],b-pos[0]))


main = main()
main.spawn()
clock = pygame.time.Clock()
temp = 0
while True:
	clock.tick(60)
	handleInput()
	main.draw()
	main.move()
	main.temp(temp)
	temp += 1
	temp %= 301
	pygame.display.flip()
